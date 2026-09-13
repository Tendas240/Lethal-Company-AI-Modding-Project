#!/usr/bin/env python3
"""Analysis-only exact enemy-spawn callsite coverage for S1.42AI-DIAG1.

Consumes only prior exact-review Actions artifacts and preserved Installed-V81 source
captures. Emits an auditable callsite matrix; never modifies profiles/controllers.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

RUNS = {
  "34529045495":"shyguy_exact_package", "34614454120":"nest_spawncycle_exact",
  "34616289395":"direct_owners_exact", "34705834727":"direct_spawn_candidates_exact",
  "34708556035":"tier_a_exact", "34709775849":"tier_b_exact",
  "34710724733":"tier_c_exact", "34711742173":"tier_d_exact",
  "34713018420":"tier_e_exact", "34714066827":"tier_f_exact",
  "34714900794":"tier_g_exact", "34716488701":"bcmer_execution_exact",
}
CONTROL=("if ","if(","for ","for(","foreach ","foreach(","while ","while(","switch ","switch(","catch ","catch(","using ","using(","lock ","lock(")
PATS={
 "spawn_game_object":re.compile(r"\bSpawnEnemyGameObject\s*\("),
 "spawn_on_server":re.compile(r"\bSpawnEnemyOnServer\s*\("),
 "spawn_server_rpc":re.compile(r"\bSpawnEnemyServerRpc\s*\("),
 "enemy_prefab_instantiate":re.compile(r"(?:enemyPrefab[\s\S]{0,1400}?\bInstantiate(?:<[^>]+>)?\s*\(|\bInstantiate(?:<[^>]+>)?\s*\([\s\S]{0,1400}?enemyPrefab)",re.I),
 "network_spawn":re.compile(r"(?:GetComponent(?:InChildren)?<NetworkObject>\s*\(\)[\s\S]{0,300}?\.Spawn\s*\(|\bNetworkObject\b[\s\S]{0,900}?\.Spawn\s*\(|\.Spawn\s*\(\s*true\s*\))"),
 "enemy_type":re.compile(r"\bEnemyType\b|\benemyType\b|enemyPrefab"),
 "pikmin_spawn":re.compile(r"\bSpawnPikminOnServer\s*\("),
 "enemy_revival":re.compile(r"\bReviveEnemy\s*\("),
 "vent_state":re.compile(r"enemyTypeIndex|\.enemyType\s*=|\.occupied\s*=|\.spawnTime\s*="),
}
NATIVE_POOL={"SpawnRandomOutsideEnemy","SpawnRandomDaytimeEnemy","SpawnRandomWeedEnemy"}
NATIVE_SHARED={"SpawnEnemyGameObject","SpawnEnemyOnServer","SpawnEnemyServerRpc"}
SCHEDULER_RULES={
 ("ButteRyBalance-0.7.0.cs","InfestationOverrides","SpawnInfestationWave"),
 ("SpawnCycleFixes-1.2.2.cs","Patches","RoundManager_Post_AssignRandomEnemyToVent"),
}
NO_ACTIVE_CONSUMER_RULES={
 ("InteractiveTerminalAPI-1.3.3.cs","Tools","SpawnMob"),
}
RUNTIME_GATED_METHODS={
 ("MoreCompany-1.14.0.cs","HandleCommand"):"host debug command; exact assembly has no internal commandEnabled assignment",
 ("Bozoros-2.9.3.cs","SpawnPufferServerRpc"):"EmergencyDice provider-gated; provider not identified in exact S1.42AI package inventory",
 ("Bozoros-2.9.3.cs","SpawnButlerServerRpc"):"EmergencyDice provider-gated; provider not identified in exact S1.42AI package inventory",
}
PARENT_METHODS={
 ("Haunted_Harpist-1.3.24.cs","SpawnEscorts"),
 ("CodeRebirth-1.6.9.cs","HandleSpawningMonarch"),
 ("CodeRebirth-1.6.9.cs","OnNetworkSpawn"),
}

def h(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def class_ranges(lines:list[str]):
    decl=re.compile(r"\bclass\s+([A-Za-z_][\w`]*)\s*(?::\s*([^\{]+))?")
    out=[]
    for i,line in enumerate(lines):
        m=decl.search(line)
        if not m: continue
        # opening brace may be same/next few lines
        k=i
        while k<min(len(lines),i+5) and "{" not in lines[k]: k+=1
        if k>=len(lines) or "{" not in lines[k]: continue
        depth=0; end=k
        for j in range(k,len(lines)):
            depth+=lines[j].count("{")-lines[j].count("}")
            if depth<=0 and j>k: end=j; break
        bases=m.group(2) or ""
        out.append((i,end,m.group(1),"EnemyAI" in bases or m.group(1).endswith(("EnemyAI","AIServer"))))
    return out

def enclosing_class(ranges,idx):
    c=[x for x in ranges if x[0]<=idx<=x[1]]
    if not c:return "<unknown>",False
    x=max(c,key=lambda q:q[0]); return x[2],x[3]

def method_name(header:str):
    s=re.sub(r"//.*","",header).strip()
    if "(" not in s or ")" not in s or s.lower().startswith(CONTROL): return None
    pre=s.split("(",1)[0].strip(); tok=re.split(r"\s+",pre)[-1].split(".")[-1].split("<",1)[0]
    return tok if re.fullmatch(r"[A-Za-z_][\w`]*",tok or "") and tok not in {"new","return","typeof","nameof"} else None

def cs_methods(text:str):
    lines=text.splitlines(); ranges=class_ranges(lines); out=[]; i=0
    while i<len(lines):
        if "(" not in lines[i]: i+=1; continue
        start=i; parts=[lines[i].strip()]; k=i
        while k<min(len(lines)-1,i+9) and "{" not in " ".join(parts): k+=1; parts.append(lines[k].strip())
        header=" ".join(parts); name=method_name(header)
        if not name or "{" not in header: i+=1; continue
        op=next((n for n in range(start,k+1) if "{" in lines[n]),None)
        if op is None: i+=1; continue
        depth=0; end=op
        for j in range(op,len(lines)):
            depth+=lines[j].count("{")-lines[j].count("}")
            if depth<=0 and j>op: end=j; break
        body="\n".join(lines[start:end+1]); cls,enemy=enclosing_class(ranges,start)
        out.append({"method":name,"class":cls,"class_enemy_ai_like":enemy,"signature":" ".join(header.split())[:700],"start_line":start+1,"end_line":end+1,"body":body})
        i=end+1
    return out

def il_methods(text:str):
    lines=text.splitlines(); out=[]; i=0
    while i<len(lines):
        if not lines[i].lstrip().startswith(".method"): i+=1; continue
        start=i; parts=[lines[i].strip()]; k=i
        while k<min(len(lines)-1,i+12) and "{" not in " ".join(parts): k+=1; parts.append(lines[k].strip())
        hdr=" ".join(parts); names=re.findall(r"([A-Za-z_][\w`]*)\s*\(",hdr); name=names[-1] if names else "<unknown>"
        depth=0; end=k
        for j in range(k,len(lines)):
            depth+=lines[j].count("{")-lines[j].count("}")
            if depth<=0 and j>k: end=j; break
        out.append({"method":name,"class":"RoundManager" if "RoundManager" in text[max(0,text.find(hdr)-500):text.find(hdr)+50] else "<il>","class_enemy_ai_like":False,"signature":hdr[:700],"start_line":start+1,"end_line":end+1,"body":"\n".join(lines[start:end+1])})
        i=end+1
    return out

def flags(body):return sorted(k for k,p in PATS.items() if p.search(body))

def direct_relevant(f):
    s=set(f)
    if s & {"spawn_game_object","spawn_on_server","spawn_server_rpc","pikmin_spawn","enemy_revival"}: return True
    return "enemy_prefab_instantiate" in s and "network_spawn" in s

def source_run(path:Path):
    rid=next((x for x in path.parts if x in RUNS),"repo"); return rid,RUNS.get(rid,"repository_source")

def classify(r):
    fn,cls,m=r["source_file"],r["class"],r["method"]
    joined=f"{fn} {cls} {m} {r['signature']}"
    if fn.startswith("theunknowncod3r-Scopophobia-") and cls=="ShyGuyPaintingProp":
        return "ALLOW_EXACT_SHYGUY_OWNER","painting route resolves exact Shy Guy; allowed by identity but cannot prove BCMER event execution"
    if fn=="BrutalCompanyMinus-1.71.0.cs":
        return "BCMER_EVENT_CONFIG_CONSTRAINED","exact BCMER execution gate is closed to ShyGuy-only config; no broad MEvent/EventManager Harmony patch"
    if r["source_kind"]=="native_v81":
        if m in NATIVE_SHARED:return "SHARED_SINK_FORBIDDEN","mixed caller/return/state contracts; never blanket-deny"
        if m in NATIVE_POOL:return "POOL_QUARANTINE_COVERED","identity comes from quarantined native pool before direct creation"
        if m=="AssignRandomEnemyToVent":return "NATIVE_SELECTOR_GUARD_REQUIRED","stateful vent assignment must reject non-ShyGuy identity without skipping assignment lifecycle wholesale"
        if m=="SpawnEnemyFromVent":return "NATIVE_QUEUE_CONSUMER_COVERED","safe only after vent assignment queue is proven ShyGuy-only; preserve vent completion"
    if (fn,m) in RUNTIME_GATED_METHODS:return "RUNTIME_GATED_ASSERTION",RUNTIME_GATED_METHODS[(fn,m)]
    if fn=="SnowyLib-1.13.1.cs" and m in {"SpawnEnemy","SpawnEnemyRpc","ChatCommand"}:
        return "NO_ACTIVE_CONSUMER_STATIC_SET","cross-assembly review found zero external SnowyLib spawn API consumers; internal chat route requires Testing=false assertion"
    if (fn,cls,m) in NO_ACTIVE_CONSUMER_RULES:
        return "NO_ACTIVE_CONSUMER_STATIC_SET","installed-set review found zero external InteractiveTerminalAPI.Tools.SpawnMob consumers and exact DLL has no autonomous caller"
    if (fn,cls,m) in SCHEDULER_RULES:
        return "STATEFUL_SCHEDULER_GUARD_REQUIRED","queues/reserves non-ShyGuy identity before native spawn; guard must precede committed vent/power/count state"
    if (fn,m) in PARENT_METHODS or (r["class_enemy_ai_like"] and "enemy_prefab_instantiate" in r["primitive_flags"]):
        return "PARENT_PREVENTION_CANDIDATE","child creation owned by non-ShyGuy EnemyAI-like parent; must prove parent cannot exist before omitting child guard"
    return "OWNER_GUARD_REQUIRED","direct/explicit enemy creation path requires exact owner-level prevention before destructive/stateful side effects"

def sources(root:Path,repo:Path):
    # Inventory every exact artifact source, but analyze C# as primary. Earlier ShyGuy capture is text-only.
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in {".cs",".il",".txt"}: continue
        analyze=False
        if p.suffix.lower()==".cs" and not p.name.startswith("V81_REFERENCE_"): analyze=True
        if "34529045495" in p.parts and p.suffix.lower()==".txt" and "Scopophobia" in p.name: analyze=True
        if analyze: yield p,"artifact",True
        else: yield p,"artifact",False
    native=[
      repo/"SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T143200Z-a693b4b9/ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt",
      repo/"SourceEvidence/VanillaV81/VentNestLifecycle/20260912T083127Z-4ebbf70b/V81_VENT_NEST_LIFECYCLE_FOCUSED_IL.txt",
    ]
    for p in native:
        if not p.is_file(): raise SystemExit(f"missing native source evidence: {p}")
        yield p,"native_v81",True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--artifacts-root",required=True); ap.add_argument("--repo-root",required=True); ap.add_argument("--out-dir",required=True); a=ap.parse_args()
    root=Path(a.artifacts_root).resolve(); repo=Path(a.repo_root).resolve(); out=Path(a.out_dir).resolve(); out.mkdir(parents=True,exist_ok=True)
    missing=set(RUNS)-{p.name for p in root.iterdir() if p.is_dir()}
    if missing: raise SystemExit(f"missing exact run dirs: {sorted(missing)}")
    inventory=[]; rows=[]; seen=set()
    for p,kind,analyze in sources(root,repo):
        b=p.read_bytes(); digest=h(b); rid,label=source_run(p)
        rel=str(p.relative_to(repo) if kind=="native_v81" else p.relative_to(root))
        inventory.append({"path":rel,"kind":kind,"run_id":rid,"run_label":label,"sha256":digest,"bytes":len(b),"analyzed":analyze})
        if not analyze or (p.name,digest) in seen: continue
        seen.add((p.name,digest)); text=b.decode("utf-8","replace")
        methods=il_methods(text) if p.name.endswith("V81_VENT_NEST_LIFECYCLE_FOCUSED_IL.txt") else cs_methods(text)
        for x in methods:
            f=flags(x["body"])
            explicit_scheduler=(p.name,x["class"],x["method"]) in SCHEDULER_RULES
            if not direct_relevant(f) and not explicit_scheduler and not (kind=="native_v81" and x["method"] in {"AssignRandomEnemyToVent","SpawnEnemyFromVent"}): continue
            if x["method"].startswith("__rpc_handler_"): continue
            r={"source_file":p.name,"source_path":rel,"source_sha256":digest,"source_kind":kind,"run_id":rid,"run_label":label,"class":x["class"],"class_enemy_ai_like":x["class_enemy_ai_like"],"method":x["method"],"signature":x["signature"],"start_line":x["start_line"],"end_line":x["end_line"],"method_body_sha256":h(x["body"].encode()),"primitive_flags":f}
            r["coverage_category"],r["coverage_rationale"]=classify(r); rows.append(r)
    # semantic C# matrix: one row per exact source method/body, no C#/IL duplicate inflation
    dedup={(r["source_sha256"],r["class"],r["method"],r["method_body_sha256"]):r for r in rows}; rows=sorted(dedup.values(),key=lambda r:(r["coverage_category"],r["source_file"],r["class"],r["method"],r["start_line"]))
    counts={}
    for r in rows: counts[r["coverage_category"]]=counts.get(r["coverage_category"],0)+1
    matrix={"schema_version":3,"scope":"S1.42AI-DIAG1 exact enemy-spawn callsite coverage","analysis_only":True,"base_contract":"BuildSpecs/S1.42AI_PLAN.md","source_runs":RUNS,"source_file_count":len(inventory),"analyzed_source_file_count":sum(1 for i in inventory if i["analyzed"]),"unique_relevant_callsite_count":len(rows),"category_counts":counts,"unclassified_count":0,"rows":rows}
    (out/"CALLSITE_MATRIX.json").write_text(json.dumps(matrix,indent=2,sort_keys=True)+"\n")
    (out/"SOURCE_INVENTORY.json").write_text(json.dumps(inventory,indent=2,sort_keys=True)+"\n")
    md=["# S1.42AI-DIAG1 Exact Spawn Callsite Coverage Matrix","","**Status:** ANALYSIS-ONLY / NO IMPLEMENTATION / NO BUILD AUTHORIZATION","",f"Relevant semantic callsites: **{len(rows)}**",f"Analyzed primary source files: **{matrix['analyzed_source_file_count']}** / inventoried exact source files: **{len(inventory)}**","Unclassified: **0**","","## Categories",""]
    for k in sorted(counts): md.append(f"- `{k}`: {counts[k]}")
    md += ["","## Callsites","","| Category | Source | Class | Method | Primitives |","|---|---|---|---|---|"]
    for r in rows: md.append(f"| `{r['coverage_category']}` | `{r['source_file']}` | `{r['class']}` | `{r['method']}` | {', '.join(r['primitive_flags'])} |")
    md += ["","## Guard","","This is a callsite coverage matrix, not implementation approval. Parent-prevention candidates require explicit reachability proof before their child guard may be omitted. Runtime-gated/no-consumer rows require static/runtime assertions in DIAG1. Shared native sinks remain forbidden blanket targets. Exact Shy Guy is allowed by identity regardless of interior/exterior location; an exterior Shy Guy must remain visible and fail the correction gate."]
    (out/"CALLSITE_MATRIX.md").write_text("\n".join(md)+"\n")
    print(json.dumps({k:matrix[k] for k in ("source_file_count","analyzed_source_file_count","unique_relevant_callsite_count","category_counts","unclassified_count")},indent=2,sort_keys=True))
    if not rows:return 3
    return 0

if __name__=="__main__": raise SystemExit(main())
