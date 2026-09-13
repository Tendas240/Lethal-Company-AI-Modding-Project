#!/usr/bin/env python3
"""Bounded S1.42AI-DIAG1 enemy-spawn callsite coverage inventory.

Analysis-only. Consumes exact prior GitHub Actions source artifacts plus the preserved
installed-V81 source captures and emits a machine-readable interception matrix.
It does not implement patches or alter build/runtime controllers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

RUN_LABELS = {
    "34529045495": "shyguy_exact_package",
    "34614454120": "nest_spawncycle_exact",
    "34616289395": "direct_owners_exact",
    "34705834727": "direct_spawn_candidates_exact",
    "34708556035": "tier_a_exact",
    "34709775849": "tier_b_exact",
    "34710724733": "tier_c_exact",
    "34711742173": "tier_d_exact",
    "34713018420": "tier_e_exact",
    "34714066827": "tier_f_exact",
    "34714900794": "tier_g_exact",
    "34716488701": "bcmer_execution_exact",
}
REQUIRED_SOURCE_RUNS = set(RUN_LABELS)
CONTROL_PREFIXES = (
    "if ", "if(", "for ", "for(", "foreach ", "foreach(", "while ", "while(",
    "switch ", "switch(", "catch ", "catch(", "using ", "using(", "lock ", "lock(",
)
PRIMITIVE_PATTERNS = {
    "roundmanager_spawn_enemy_game_object": re.compile(r"\bSpawnEnemyGameObject\s*\("),
    "roundmanager_spawn_enemy_on_server": re.compile(r"\bSpawnEnemyOnServer\s*\("),
    "roundmanager_spawn_enemy_server_rpc": re.compile(r"\bSpawnEnemyServerRpc\s*\("),
    "enemy_prefab_instantiate": re.compile(r"enemyPrefab[\s\S]{0,1200}?\bInstantiate\s*\(|\bInstantiate\s*\([\s\S]{0,1200}?enemyPrefab", re.I),
    "enemytype_reference": re.compile(r"\bEnemyType\b|\benemyType\b"),
    "network_spawn": re.compile(r"\bNetworkObject\b[\s\S]{0,900}?\.Spawn\s*\(|\.Spawn\s*\(\s*true\s*\)"),
    "pikmin_spawn_api": re.compile(r"\bSpawnPikminOnServer\s*\("),
    "enemy_revival": re.compile(r"\bReviveEnemy\s*\("),
    "vent_enemy_assignment": re.compile(r"enemyTypeIndex|\.enemyType\s*=|\.occupied\s*=|\.spawnTime\s*="),
    "pool_mutation": re.compile(r"OutsideEnemies|DaytimeEnemies|WeedEnemies|currentLevel\.Enemies|\.Enemies\b"),
}
NATIVE_POOL_METHODS = {
    "SpawnRandomOutsideEnemy", "SpawnRandomDaytimeEnemy", "SpawnRandomWeedEnemy",
    "SpawnEnemiesOutside", "SpawnDaytimeEnemiesOutside", "SpawnWeedEnemies",
    "PredictAllOutsideEnemies", "BeginEnemySpawning", "PlotOutEnemiesForNextHour",
}
NATIVE_STATEFUL_SELECTION = {"AssignRandomEnemyToVent", "SpawnEnemyFromVent"}
SHARED_SINK_METHODS = {"SpawnEnemyGameObject", "SpawnEnemyOnServer", "SpawnEnemyServerRpc"}
RUNTIME_GATED_RULES = [
    ("MoreCompany", "DebugCommandRegistry", "HandleCommand", "public commandEnabled flag; no internal assignment in exact assembly"),
    ("SnowyLib", "Utils", "ChatCommand", "Debugging / Testing config must remain false; cross-assembly consumers separately closed"),
    ("Bozoros", "EmergencyDice", "", "Theronguard.EmergencyDice provider gate; exact package inventory did not identify provider"),
]
ALLOW_SHYGUY_RULES = [
    ("Scopophobia", "ShyGuyPaintingProp", "SpawnEnemyOnServer"),
    ("BrutalCompanyMinus", "ShyGuy", "Execute"),
]

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def strip_comments_for_header(s: str) -> str:
    return re.sub(r"//.*", "", s).strip()

def class_context(lines: list[str], idx: int) -> tuple[str, bool]:
    pat = re.compile(r"\b(class|struct)\s+([A-Za-z_][\w`<>.]*)\s*(?::\s*([^\{]+))?")
    for j in range(idx, max(-1, idx - 1200), -1):
        m = pat.search(lines[j])
        if m:
            name = m.group(2)
            bases = m.group(3) or ""
            enemy_ai = "EnemyAI" in bases or name.endswith("EnemyAI") or name.endswith("AIServer")
            return name, enemy_ai
    return "<unknown>", False

def method_name_from_header(header: str) -> str | None:
    h = strip_comments_for_header(header)
    if not h or "(" not in h or ")" not in h:
        return None
    lower = h.lstrip().lower()
    if lower.startswith(CONTROL_PREFIXES):
        return None
    pre = h.split("(", 1)[0].strip()
    token = re.split(r"\s+", pre)[-1].split(".")[-1].split("<", 1)[0].strip()
    if not re.match(r"^[A-Za-z_][\w`]*$", token) or token in {"new", "return", "typeof", "nameof", "default"}:
        return None
    return token

def extract_cs_methods(text: str) -> list[dict]:
    lines = text.splitlines()
    out: list[dict] = []
    i = 0
    while i < len(lines):
        if "(" not in lines[i]:
            i += 1
            continue
        start = i
        header_lines = [lines[i]]
        k = i
        while k < len(lines) and k < i + 10 and "{" not in "\n".join(header_lines):
            k += 1
            if k < len(lines):
                header_lines.append(lines[k])
        header = " ".join(x.strip() for x in header_lines)
        if "{" not in header:
            i += 1
            continue
        name = method_name_from_header(header)
        if not name:
            i += 1
            continue
        brace_pos_line = next((n for n in range(start, min(len(lines), k + 1)) if "{" in lines[n]), None)
        if brace_pos_line is None:
            i += 1
            continue
        depth = 0
        seen = False
        end = brace_pos_line
        for j in range(brace_pos_line, len(lines)):
            opens = lines[j].count("{")
            closes = lines[j].count("}")
            if opens:
                seen = True
            depth += opens - closes
            if seen and depth <= 0:
                end = j
                break
        if end <= brace_pos_line:
            i += 1
            continue
        body = "\n".join(lines[start:end + 1])
        cls, enemy_ai = class_context(lines, start)
        out.append({"method": name, "class": cls, "class_enemy_ai_like": enemy_ai,
                    "signature": " ".join(header.split())[:600], "start_line": start + 1,
                    "end_line": end + 1, "body": body})
        i = end + 1
    return out

def extract_il_methods(text: str) -> list[dict]:
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        if not lines[i].lstrip().startswith(".method"):
            i += 1
            continue
        start = i
        header_parts = [lines[i].strip()]
        k = i
        while k + 1 < len(lines) and "{" not in lines[k] and k < i + 12:
            k += 1
            header_parts.append(lines[k].strip())
            if "{" in lines[k]:
                break
        header = " ".join(header_parts)
        m = re.search(r"([A-Za-z_][\w`<>.]*)\s*\(", header)
        name = m.group(1).split(".")[-1] if m else "<unknown>"
        depth = 0
        seen = False
        end = k
        for j in range(k, len(lines)):
            opens = lines[j].count("{")
            closes = lines[j].count("}")
            if opens:
                seen = True
            depth += opens - closes
            if seen and depth <= 0:
                end = j
                break
        body = "\n".join(lines[start:end + 1])
        out.append({"method": name, "class": "<il>", "class_enemy_ai_like": False,
                    "signature": header[:600], "start_line": start + 1, "end_line": end + 1,
                    "body": body})
        i = end + 1
    return out

def primitive_flags(body: str) -> list[str]:
    return sorted(name for name, pat in PRIMITIVE_PATTERNS.items() if pat.search(body))

def is_relevant(flags: list[str]) -> bool:
    f = set(flags)
    if f & {"roundmanager_spawn_enemy_game_object", "roundmanager_spawn_enemy_on_server",
            "roundmanager_spawn_enemy_server_rpc", "pikmin_spawn_api", "enemy_revival"}:
        return True
    if "enemy_prefab_instantiate" in f and ("network_spawn" in f or "enemytype_reference" in f):
        return True
    return "vent_enemy_assignment" in f and "enemytype_reference" in f

def source_tag(path: Path) -> tuple[str, str]:
    run_id = next((p for p in path.parts if p in RUN_LABELS), "repo")
    return run_id, RUN_LABELS.get(run_id, "repository_source")

def classify(row: dict) -> tuple[str, str]:
    joined = f"{row['source_file']} {row['class']} {row['method']} {row['signature']}"
    for src, c, m in ALLOW_SHYGUY_RULES:
        if src.lower() in joined.lower() and c.lower() in joined.lower() and m.lower() in row["method"].lower():
            return "ALLOW_EXACT_SHYGUY_OWNER", "exact Shy Guy identity owner; do not location-filter exterior Shy Guy"
    if row.get("source_kind") == "native_v81":
        if row["method"] in SHARED_SINK_METHODS:
            return "SHARED_SINK_FORBIDDEN", "shared native spawn/RPC sink has mixed caller contracts; never blanket-deny"
        if row["method"] in NATIVE_POOL_METHODS:
            return "POOL_QUARANTINE_COVERED", "ShyGuy-only pool quarantine must run before this native selection/batch path"
        if row["method"] in NATIVE_STATEFUL_SELECTION:
            return "NATIVE_SELECTOR_GUARD_REQUIRED", "stateful vent/queued identity path requires narrow identity-safe handling; whole-method skip forbidden"
    for src, c, m, why in RUNTIME_GATED_RULES:
        if src.lower() in joined.lower() and c.lower() in joined.lower() and (not m or m.lower() in row["method"].lower()):
            return "RUNTIME_GATED_OR_DORMANT", why
    if row.get("class_enemy_ai_like") and "enemy_prefab_instantiate" in row["primitive_flags"]:
        return "PARENT_PREVENTION_CANDIDATE", "direct child spawn owned by an EnemyAI-like parent; prove parent cannot exist under ShyGuy-only guard before omitting child guard"
    if "BrutalCompany" in joined or "BCMER" in joined:
        return "BCMER_EVENT_CONSTRAINED", "BCMER execution gate is already closed to ShyGuy; retain config/static assertions rather than broad Harmony execution patch"
    return "OWNER_GUARD_REQUIRED", "direct/explicit enemy creation or stateful spawn API requires exact owner-level prevention before non-ShyGuy side effects"

def iter_source_files(artifacts_root: Path, repo_root: Path) -> Iterable[tuple[Path, str]]:
    for p in sorted(artifacts_root.rglob("*")):
        if p.is_file() and p.suffix.lower() in {".cs", ".il", ".txt"}:
            yield p, "artifact"
    native_files = [
        repo_root / "SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T143200Z-a693b4b9/ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt",
        repo_root / "SourceEvidence/VanillaV81/VentNestLifecycle/20260912T083127Z-4ebbf70b/V81_VENT_NEST_LIFECYCLE_FOCUSED_IL.txt",
    ]
    for p in native_files:
        if not p.is_file():
            raise SystemExit(f"required native source evidence missing: {p}")
        yield p, "native_v81"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts-root", required=True)
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    artifacts_root = Path(args.artifacts_root).resolve()
    repo_root = Path(args.repo_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    present_runs = {p.name for p in artifacts_root.iterdir() if p.is_dir()}
    missing_runs = sorted(REQUIRED_SOURCE_RUNS - present_runs)
    if missing_runs:
        raise SystemExit(f"missing exact source artifact run directories: {missing_runs}")
    source_inventory = []
    rows = []
    seen_content = set()
    for path, kind in iter_source_files(artifacts_root, repo_root):
        data = path.read_bytes()
        digest = sha256_bytes(data)
        run_id, run_label = source_tag(path)
        source_inventory.append({"path": str(path.relative_to(repo_root) if kind == "native_v81" else path.relative_to(artifacts_root)),
                                 "kind": kind, "run_id": run_id, "run_label": run_label,
                                 "sha256": digest, "bytes": len(data)})
        key = (path.name, digest)
        if key in seen_content:
            continue
        seen_content.add(key)
        text = data.decode("utf-8", errors="replace")
        methods = extract_il_methods(text) if path.suffix.lower() == ".il" else extract_cs_methods(text)
        for m in methods:
            flags = primitive_flags(m["body"])
            if not is_relevant(flags):
                continue
            row = {"source_file": path.name, "source_path": source_inventory[-1]["path"],
                   "source_sha256": digest, "source_kind": kind, "run_id": run_id,
                   "run_label": run_label, "class": m["class"],
                   "class_enemy_ai_like": m["class_enemy_ai_like"], "method": m["method"],
                   "signature": m["signature"], "start_line": m["start_line"],
                   "end_line": m["end_line"],
                   "method_body_sha256": sha256_bytes(m["body"].encode("utf-8")),
                   "primitive_flags": flags}
            row["coverage_category"], row["coverage_rationale"] = classify(row)
            rows.append(row)
    dedup = {}
    for row in rows:
        key = (row["source_sha256"], row["class"], row["method"], row["method_body_sha256"])
        dedup[key] = row
    rows = sorted(dedup.values(), key=lambda r: (r["coverage_category"], r["source_file"], r["class"], r["method"], r["start_line"]))
    categories = {}
    for r in rows:
        categories[r["coverage_category"]] = categories.get(r["coverage_category"], 0) + 1
    unclassified = [r for r in rows if r["coverage_category"] == "UNCLASSIFIED"]
    matrix = {"schema_version": 2, "scope": "S1.42AI-DIAG1 exact enemy-spawn callsite coverage",
              "analysis_only": True, "base_contract": "BuildSpecs/S1.42AI_PLAN.md",
              "source_runs": RUN_LABELS, "source_file_count": len(source_inventory),
              "unique_relevant_callsite_count": len(rows), "category_counts": categories,
              "unclassified_count": len(unclassified), "rows": rows}
    (out_dir / "CALLSITE_MATRIX.json").write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "SOURCE_INVENTORY.json").write_text(json.dumps(source_inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md = ["# S1.42AI-DIAG1 Exact Spawn Callsite Coverage Matrix", "",
          "**Status:** ANALYSIS-ONLY / NO IMPLEMENTATION / NO BUILD AUTHORIZATION", "",
          f"Unique relevant callsites: **{len(rows)}**", f"Source files inventoried: **{len(source_inventory)}**",
          f"Unclassified: **{len(unclassified)}**", "", "## Coverage categories", ""]
    for k in sorted(categories):
        md.append(f"- `{k}`: {categories[k]}")
    md += ["", "## Callsites", "", "| Category | Source | Class | Method | Primitives |", "|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| `{r['coverage_category']}` | `{r['source_file']}` | `{r['class']}` | `{r['method']}` | {', '.join(r['primitive_flags'])} |")
    md += ["", "## Interpretation guard", "",
           "This matrix is a coverage inventory, not patch approval. `OWNER_GUARD_REQUIRED` means the exact owner transaction must be reviewed before coding; `PARENT_PREVENTION_CANDIDATE` must be proven unreachable after parent prevention before omitting a child guard; shared sinks remain forbidden broad targets. Exact Shy Guy owners are allowed by identity regardless of interior/exterior location so an unexpected exterior Shy Guy remains visible and fails the correction gate."]
    (out_dir / "CALLSITE_MATRIX.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"source_file_count": len(source_inventory), "unique_relevant_callsite_count": len(rows),
                      "category_counts": categories, "unclassified_count": len(unclassified)}, indent=2, sort_keys=True))
    if unclassified:
        return 2
    if not rows:
        return 3
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
