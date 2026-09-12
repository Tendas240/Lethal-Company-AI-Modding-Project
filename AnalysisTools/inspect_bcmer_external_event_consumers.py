#!/usr/bin/env python3
"""Exact installed-set external consumer scan for BCMER event execution APIs."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAIN = "15cd35a62a995b1895634d40a661a880aa6f087d"
EXPECTED_BUILD = "S1.42AI"
EXPECTED_PROFILE_SHA256 = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
EXPECTED_ENABLED_COUNT = 183
EXPECTED_EMBEDDED_DLL_COUNT = 5
BCMER_PROVIDER_PACKAGE = "SoftDiamond-BrutalCompanyMinusExtraReborn"
ILSPY_VERSION = "11.0.0.9375"
DEFAULT_SHARD_COUNT = 12
MAX_PACKAGE_BYTES = 2 * 1024 * 1024 * 1024
MAX_DLL_BYTES = 512 * 1024 * 1024
MAX_TEXT_CHARS = 100 * 1024 * 1024

PACKAGE_PATTERN = re.compile(
    r"(?m)^- name: ([^\r\n]+)\r?\n"
    r"  version:\r?\n"
    r"    major: (\d+)\r?\n"
    r"    minor: (\d+)\r?\n"
    r"    patch: (\d+)\r?\n"
    r"  enabled: (true|false)"
)

DIRECT_PATTERNS = {
    "api_force_events": re.compile(r".*BrutalCompanyMinus\.Minus\.API::ForceEvents\s*\(.*"),
    "api_regenerate_events": re.compile(r".*BrutalCompanyMinus\.Minus\.API::RegenerateEvents\s*\(.*"),
    "mevent_execute": re.compile(r".*BrutalCompanyMinus\.Minus\.MEvent::Execute\s*\(.*"),
    "mevent_get_event": re.compile(r".*BrutalCompanyMinus\.Minus\.MEvent::GetEvent\s*\(.*"),
    "general_custom_event_ctor": re.compile(r".*BrutalCompanyMinus\.Minus\.CustomEvents\.GeneralCustomEvent::.ctor\s*\(.*"),
}
REFLECTION_SOURCE = re.compile(r"\b(?:GetMethod|GetMethods|GetField|GetFields|GetType|Type\.GetType|Assembly\.Load|GetTypes|Invoke)\b")
REFLECTION_TERMS = ("brutalcompanyminus", "forceevents", "regenerateevents", "mevent", "generalcustomevent", "execute")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr[-3000:]))
    return p.stdout.strip()


def run(args: list[str], timeout: int = 420) -> tuple[str, str]:
    p = subprocess.run(args, text=True, capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(f"{args[0]} failed ({p.returncode}): {p.stderr[-5000:]}")
    return p.stdout, p.stderr


def verify_delta() -> None:
    p = subprocess.run(["git", "merge-base", "--is-ancestor", EXPECTED_MAIN, "HEAD"], cwd=ROOT)
    if p.returncode:
        raise RuntimeError("Expected canonical main is not an ancestor of analysis HEAD")
    allowed = {
        "AnalysisTools/inspect_bcmer_execution_exact.py",
        ".github/workflows/bcmer-execution-exact-review.yml",
        "AnalysisTools/inspect_bcmer_external_event_consumers.py",
        ".github/workflows/bcmer-external-event-consumer-review.yml",
    }
    changed = [x for x in git("diff", "--name-only", EXPECTED_MAIN + "..HEAD").splitlines() if x]
    unexpected = sorted(set(changed) - allowed)
    if unexpected:
        raise RuntimeError("Unexpected analysis-branch delta: " + ", ".join(unexpected))


def is_managed_pe(data: bytes) -> bool:
    if len(data) < 0x100 or data[:2] != b"MZ":
        return False
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if pe + 0x18 >= len(data) or data[pe:pe+4] != b"PE\0\0":
        return False
    opt = pe + 24
    magic = struct.unpack_from("<H", data, opt)[0]
    dd = opt + (96 if magic == 0x10B else 112 if magic == 0x20B else -1)
    if dd < opt:
        return False
    cli = dd + 14 * 8
    if cli + 8 > len(data):
        return False
    rva, size = struct.unpack_from("<II", data, cli)
    return bool(rva and size)


def load_context() -> dict:
    verify_delta()
    state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text(encoding="utf-8"))
    candidate = state["active_candidate"]
    if candidate["build_id"] != EXPECTED_BUILD or candidate["sha256"] != EXPECTED_PROFILE_SHA256:
        raise RuntimeError("Active candidate/profile identity changed")
    profile = ROOT / candidate["profile"]
    profile_bytes = profile.read_bytes()
    if sha256(profile_bytes) != EXPECTED_PROFILE_SHA256:
        raise RuntimeError("Guarded S1.42AI profile SHA mismatch")
    with zipfile.ZipFile(profile) as z:
        export_bytes = z.read("export.r2x")
    readable = (ROOT / "ProfileSources/S1.42AI/export.r2x").read_bytes()
    if export_bytes != readable:
        raise RuntimeError("Readable export differs from guarded profile")
    file_index_bytes = (ROOT / "ProfileSources/S1.42AI/FILE_INDEX.json").read_bytes()
    file_index = json.loads(file_index_bytes)
    record = next((x for x in file_index if x["path"] == "export.r2x"), None)
    if not record or record["sha256"] != sha256(export_bytes):
        raise RuntimeError("export.r2x disagrees with FILE_INDEX")
    text = export_bytes.decode("utf-8-sig")
    packages = [{"package":m[0],"version":".".join(m[1:4]),"enabled":m[4]=="true"} for m in PACKAGE_PATTERN.findall(text)]
    if len(packages) != len(re.findall(r"(?m)^- name: ", text)):
        raise RuntimeError("Some package entries were not parsed")
    enabled = [p for p in packages if p["enabled"]]
    if len(enabled) != EXPECTED_ENABLED_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_ENABLED_COUNT} enabled packages, got {len(enabled)}")
    if BCMER_PROVIDER_PACKAGE not in {p["package"] for p in enabled}:
        raise RuntimeError("BCMER provider package missing")
    embedded = [x for x in file_index if x["path"].lower().endswith(".dll")]
    if len(embedded) != EXPECTED_EMBEDDED_DLL_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_EMBEDDED_DLL_COUNT} embedded DLLs, got {len(embedded)}")
    return {"profile":profile,"enabled":enabled,"embedded":embedded,"export_sha256":sha256(export_bytes),"file_index_sha256":sha256(file_index_bytes)}


def safe_slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s)[:150]


def download(url: str, target: Path) -> tuple[int,str]:
    total = 0; digest = hashlib.sha256()
    req = urllib.request.Request(url, headers={"User-Agent":"s142ai-bcmer-event-consumers/1"})
    with urllib.request.urlopen(req, timeout=180) as r, target.open("wb") as f:
        while True:
            block = r.read(1024*1024)
            if not block: break
            total += len(block)
            if total > MAX_PACKAGE_BYTES: raise RuntimeError("Package exceeds 2 GiB bound: " + url)
            digest.update(block); f.write(block)
    return total, digest.hexdigest()


def raw_candidate(data: bytes) -> bool:
    provider = b"BrutalCompanyMinus" in data
    surface = any(x in data for x in (b"ForceEvents", b"RegenerateEvents", b"MEvent", b"GeneralCustomEvent"))
    return provider and surface


def find_contexts(text: str, regex: re.Pattern, radius: int = 5, limit: int = 80) -> list[dict]:
    lines = text.splitlines(); out=[]
    for i,line in enumerate(lines):
        if not regex.search(line): continue
        lo=max(0,i-radius); hi=min(len(lines),i+radius+1)
        out.append({"line":i+1,"lines":lines[lo:hi]})
        if len(out)>=limit: break
    return out


def inspect_candidate(data: bytes, identity: str, package: str, member: str, out: Path, work: Path) -> dict:
    stem=safe_slug(identity); dll=work/(stem+".dll"); dll.write_bytes(data)
    try:
        il, ilerr = run(["ilspycmd","-il",str(dll)])
        src, srcerr = run(["ilspycmd",str(dll)])
    finally:
        dll.unlink(missing_ok=True)
    if len(il)>MAX_TEXT_CHARS or len(src)>MAX_TEXT_CHARS: raise RuntimeError("Decompiler text bound exceeded: "+identity)
    direct={name:find_contexts(il,pat) for name,pat in DIRECT_PATTERNS.items()}
    reflection=[]; lines=src.splitlines()
    for i,line in enumerate(lines):
        if not REFLECTION_SOURCE.search(line): continue
        window="\n".join(lines[max(0,i-7):min(len(lines),i+8)])
        low=window.lower()
        if "brutalcompanyminus" in low and any(term in low for term in REFLECTION_TERMS[1:]):
            reflection.append({"line":i+1,"context":window})
    cs=stem+".cs"; iln=stem+".il"
    (out/cs).write_text(src,encoding="utf-8"); (out/iln).write_text(il,encoding="utf-8")
    return {"package":package,"member":member,"identity":identity,"dll_sha256":sha256(data),"source_sha256":sha256(src.encode()),"il_sha256":sha256(il.encode()),"source_lines":len(lines),"il_lines":len(il.splitlines()),"direct_contexts":direct,"reflection_contexts":reflection[:50],"outputs":[cs,iln],"source_stderr":srcerr[-2000:],"il_stderr":ilerr[-2000:]}


def scan_package(index:int,p:dict,out:Path,work:Path)->dict:
    name=p["package"]; version=p["version"]; url=f"https://gcdn.thunderstore.io/live/repository/packages/{name}-{version}.zip"; zp=work/f"{index:03d}-{safe_slug(name)}.zip"
    size,zsha=download(url,zp)
    rec={"index":index,"package":name,"version":version,"url":url,"zip_bytes":size,"zip_sha256":zsha,"managed_dll_count":0,"dlls":[],"candidates":[]}
    with zipfile.ZipFile(zp) as z:
        for di,m in enumerate([x for x in z.infolist() if not x.is_dir() and x.filename.lower().endswith('.dll')]):
            if m.file_size>MAX_DLL_BYTES: raise RuntimeError("DLL exceeds 512 MiB bound: "+m.filename)
            data=z.read(m); managed=is_managed_pe(data); cand=managed and raw_candidate(data)
            ent={"member":m.filename,"bytes":len(data),"sha256":sha256(data),"managed_pe":managed,"raw_candidate":cand}
            if managed: rec["managed_dll_count"]+=1
            if cand:
                rec["candidates"].append(inspect_candidate(data,f"{index:03d}-{di:03d}-{name}-{Path(m.filename).name}",name,m.filename,out,work))
            rec["dlls"].append(ent)
    zp.unlink(missing_ok=True); return rec


def scan_embedded(ctx:dict,out:Path,work:Path)->list[dict]:
    res=[]
    with zipfile.ZipFile(ctx["profile"]) as z:
        for i,r in enumerate(ctx["embedded"]):
            data=z.read(r["path"]); actual=sha256(data)
            if actual!=r["sha256"]: raise RuntimeError("Embedded DLL SHA mismatch: "+r["path"])
            managed=is_managed_pe(data); cand=managed and raw_candidate(data)
            e={"index":i,"path":r["path"],"bytes":len(data),"sha256":actual,"managed_pe":managed,"raw_candidate":cand,"candidates":[]}
            if cand: e["candidates"].append(inspect_candidate(data,f"embedded-{i:03d}-{Path(r['path']).name}","__embedded_project__",r["path"],out,work))
            res.append(e)
    return res


def shard(shard_index:int,shard_count:int,out:Path,work:Path)->None:
    ctx=load_context(); records=[]
    for idx,p in enumerate(ctx["enabled"]):
        if idx%shard_count==shard_index: records.append(scan_package(idx,p,out,work))
    embedded=scan_embedded(ctx,out,work) if shard_index==0 else []
    obj={"schema_version":1,"mode":"shard","canonical_main":EXPECTED_MAIN,"repository_commit":os.environ.get("GITHUB_SHA"),"shard_index":shard_index,"shard_count":shard_count,"profile_sha256":EXPECTED_PROFILE_SHA256,"export_sha256":ctx["export_sha256"],"file_index_sha256":ctx["file_index_sha256"],"packages":records,"embedded":embedded}
    (out/f"SHARD_{shard_index:02d}.json").write_text(json.dumps(obj,indent=2)+"\n",encoding="utf-8")


def aggregate(inputs:Path,out:Path)->None:
    files=sorted(inputs.rglob("SHARD_*.json"));
    if len(files)!=DEFAULT_SHARD_COUNT: raise RuntimeError(f"Expected {DEFAULT_SHARD_COUNT} shard manifests, got {len(files)}")
    shards=[json.loads(p.read_text()) for p in files]
    if {s["shard_index"] for s in shards}!=set(range(DEFAULT_SHARD_COUNT)): raise RuntimeError("Shard index coverage mismatch")
    pkgs=[p for s in shards for p in s["packages"]]; embedded=[e for s in shards for e in s["embedded"]]
    if len(pkgs)!=EXPECTED_ENABLED_COUNT: raise RuntimeError(f"Expected {EXPECTED_ENABLED_COUNT} packages, got {len(pkgs)}")
    if len(embedded)!=EXPECTED_EMBEDDED_DLL_COUNT: raise RuntimeError(f"Expected {EXPECTED_EMBEDDED_DLL_COUNT} embedded DLLs, got {len(embedded)}")
    managed=sum(p["managed_dll_count"] for p in pkgs)+sum(1 for e in embedded if e["managed_pe"])
    candidates=[c for p in pkgs for c in p["candidates"]]+[c for e in embedded for c in e["candidates"]]
    external=[c for c in candidates if c["package"]!=BCMER_PROVIDER_PACKAGE]
    counts={k:sum(1 for c in external if c["direct_contexts"][k]) for k in DIRECT_PATTERNS}
    reflection=sum(1 for c in external if c["reflection_contexts"])
    verification={"schema_version":1,"status":"BCMER_EXTERNAL_EVENT_CONSUMER_SCAN_COMPLETE","canonical_main":EXPECTED_MAIN,"profile_sha256":EXPECTED_PROFILE_SHA256,"enabled_packages_scanned":len(pkgs),"embedded_dlls_scanned":len(embedded),"managed_dlls_scanned":managed,"raw_candidate_assemblies":len(candidates),"external_candidate_assemblies":len(external),"external_direct_call_assemblies":counts,"external_reflection_candidate_assemblies":reflection,"external_candidates":external,"provider_self_candidates":[c for c in candidates if c["package"]==BCMER_PROVIDER_PACKAGE],"qualification":"Complete exact enabled-package plus embedded-DLL static scan for BCMER event-execution API/type metadata markers. Direct IL calls and reflection-like contexts are exact for captured binaries; arbitrary runtime-generated reflection strings are outside static proof."}
    (out/"VERIFICATION.json").write_text(json.dumps(verification,indent=2)+"\n",encoding="utf-8")
    # copy candidate C#/IL outputs from downloaded shard artifact tree
    for c in candidates:
        for name in c["outputs"]:
            matches=list(inputs.rglob(name))
            if len(matches)!=1: raise RuntimeError(f"Expected one candidate output {name}, got {len(matches)}")
            (out/name).write_bytes(matches[0].read_bytes())
    print(json.dumps(verification,indent=2))


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--mode',choices=['shard','aggregate'],required=True); ap.add_argument('--shard-index',type=int); ap.add_argument('--shard-count',type=int,default=DEFAULT_SHARD_COUNT); ap.add_argument('--input-root',type=Path); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True); work=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'bcmer-event-consumer-scan'; work.mkdir(parents=True,exist_ok=True)
    if args.mode=='shard':
        if args.shard_index is None: raise RuntimeError('--shard-index required')
        shard(args.shard_index,args.shard_count,args.output,work)
    else:
        if args.input_root is None: raise RuntimeError('--input-root required')
        verify_delta(); aggregate(args.input_root,args.output)

if __name__=='__main__': main()
