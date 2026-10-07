#!/usr/bin/env python3
"""Exact-byte S1.42AI remaining enabled-package spawn-owner discovery.

This is a discovery/screening tool, not a patch-safety approval. It scans every
remaining enabled Thunderstore package not already covered by named canonical
source-evidence authorities, hashes exact package/DLL bytes, screens managed IL for
enemy/spawn ownership surfaces, and emits bounded source excerpts only for positive
DLL candidates. Absence of a discovery hit is never treated as proof of safety.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAIN = "a9e508aabb2111f511ddf2790c0a4929092bdb15"
EXPECTED_BUILD = "S1.42AI"
EXPECTED_PROFILE_SHA256 = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
EXPECTED_ENABLED_COUNT = 183
ILSPY_VERSION = "11.0.0.9375"
DEFAULT_SHARD_COUNT = 12
MAX_PACKAGE_BYTES = 2 * 1024 * 1024 * 1024
MAX_DLL_BYTES = 128 * 1024 * 1024
MAX_IL_CHARS = 80 * 1024 * 1024
MAX_SOURCE_CHARS = 80 * 1024 * 1024

# Batch-1 discovery is already canonical evidence. These identities are excluded
# from repeat discovery, not declared safe.
PRIOR_BATCH_PACKAGES = {
    "NotezyTeam-LethalMinNightly": "SourceEvidence/NativeSpawnOwners/20260911T144505Z/REVIEW.md",
    "XuXiaolan-CodeRebirth": "SourceEvidence/NativeSpawnOwners/20260911T152805Z-DirectOwnersNativeGaps/REVIEW.md",
    "TeamXiaolan-DawnLib": "SourceEvidence/NativeSpawnOwners/20260911T152805Z-DirectOwnersNativeGaps/REVIEW.md",
    "SoftDiamond-RollingGiant": "SourceEvidence/NativeSpawnOwners/20260911T144505Z/REVIEW.md",
    "Ccode_lang-SirenHead": "SourceEvidence/NativeSpawnOwners/20260911T144505Z/REVIEW.md",
    "PureFPSZac-NestFix": "SourceEvidence/NativeSpawnOwners/20260911T150936Z-NestSpawnCycleExact/REVIEW.md",
    "ButteryStancakes-SpawnCycleFixes": "SourceEvidence/NativeSpawnOwners/20260911T150936Z-NestSpawnCycleExact/REVIEW.md",
}

# These packages already have separate exact source authorities for the current
# diagnostic and are intentionally routed outside this remaining-package screen.
SEPARATE_AUTHORITY_PACKAGES = {
    "theunknowncod3r-Scopophobia": "SourceEvidence/ShyGuyIsolation/20260910T205433Z/REVIEW.md",
    "SoftDiamond-BrutalCompanyMinusExtraReborn": "BuildSpecs/S1.42AI_PLAN.md",
}

PACKAGE_PATTERN = re.compile(
    r"(?m)^- name: ([^\r\n]+)\r?\n"
    r"  version:\r?\n"
    r"    major: (\d+)\r?\n"
    r"    minor: (\d+)\r?\n"
    r"    patch: (\d+)\r?\n"
    r"  enabled: (true|false)"
)

IL_FEATURES = {
    "enemy_ai_ref": re.compile(r"\bEnemyAI\b"),
    "enemy_ai_subclass": re.compile(r"extends\s+(?:class\s+)?(?:\[[^\]]+\])?EnemyAI\b"),
    "enemy_type_ref": re.compile(r"\bEnemyType\b"),
    "enemy_prefab_ref": re.compile(r"\benemyPrefab\b", re.I),
    "roundmanager_spawn_enemy": re.compile(r"RoundManager::SpawnEnemyGameObject\b"),
    "unity_instantiate": re.compile(r"(?:UnityEngine\.)?(?:Object|GameObject)::Instantiate\b"),
    "networkobject_spawn": re.compile(r"NetworkObject::(?:Spawn|SpawnWithOwnership|SpawnAsPlayerObject)\b"),
    "register_enemy": re.compile(r"\bRegisterEnemy\b|\bAddEnemyToPool\b"),
    "spawn_enemy_named_member": re.compile(r"\bSpawn\w*Enemy\w*\b|\bSpawnEnemy\w*\b"),
    "enemy_vent": re.compile(r"\bEnemyVent\b|\bAssignRandomEnemyToVent\b"),
    "enemy_nest": re.compile(r"\bEnemyAINestSpawnObject\b|\bUseNestSpawnObject\b|\bSpawnNestObjectForOutsideEnemy\b"),
    "roundmanager_spawn_batches": re.compile(r"\bSpawn(?:RandomOutsideEnemy|EnemiesOutside|DaytimeEnemiesOutside|WeedEnemies)\b"),
    "patch_or_detour": re.compile(r"HarmonyPatch|MonoMod|Detour|HookEndpoint|ILHook|NativeDetour"),
}

SOURCE_HIT = re.compile(
    r"SpawnEnemyGameObject|Instantiate\s*[<(]|NetworkObject|\.Spawn\s*\(|"
    r"SpawnWithOwnership|SpawnAsPlayerObject|enemyPrefab|EnemyAI|EnemyType|"
    r"EnemyVent|AssignRandomEnemyToVent|EnemyAINestSpawnObject|UseNestSpawnObject|"
    r"SpawnNestObjectForOutsideEnemy|SpawnRandomOutsideEnemy|SpawnEnemiesOutside|"
    r"SpawnDaytimeEnemiesOutside|SpawnWeedEnemies|RegisterEnemy|AddEnemyToPool|"
    r"HarmonyPatch|MonoMod|Detour|ILHook"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr[-2000:]))
    return result.stdout.strip()


def run(args: list[str], timeout: int = 240) -> tuple[str, str]:
    result = subprocess.run(args, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed ({result.returncode}): {result.stderr[-4000:]}")
    return result.stdout, result.stderr


def verify_analysis_branch_delta() -> None:
    # The exact canonical main must remain an ancestor, and this analysis branch may
    # change only the discovery tool/workflow. This prevents accidental project-state
    # changes from being folded into discovery evidence.
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_MAIN, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError("Expected canonical main is not an ancestor of analysis HEAD")
    changed = [x for x in git("diff", "--name-only", EXPECTED_MAIN + "..HEAD").splitlines() if x]
    allowed = {
        "AnalysisTools/inspect_remaining_spawn_owners.py",
        ".github/workflows/remaining-spawn-owner-discovery.yml",
    }
    unexpected = sorted(set(changed) - allowed)
    if unexpected:
        raise RuntimeError("Unexpected analysis-branch delta: " + ", ".join(unexpected))


def load_context() -> dict:
    verify_analysis_branch_delta()
    state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text(encoding="utf-8"))
    candidate = state["active_candidate"]
    if candidate["build_id"] != EXPECTED_BUILD:
        raise RuntimeError("Active candidate is no longer exact S1.42AI; reroute before discovery")
    if candidate["sha256"] != EXPECTED_PROFILE_SHA256:
        raise RuntimeError("S1.42AI profile identity changed")
    profile = ROOT / candidate["profile"]
    profile_bytes = profile.read_bytes()
    if sha256(profile_bytes) != EXPECTED_PROFILE_SHA256:
        raise RuntimeError("Guarded S1.42AI archive SHA mismatch")
    with zipfile.ZipFile(profile) as archive:
        export_bytes = archive.read("export.r2x")
    readable_export = (ROOT / "ProfileSources/S1.42AI/export.r2x").read_bytes()
    if export_bytes != readable_export:
        raise RuntimeError("Readable S1.42AI export differs from guarded archive")
    file_index_bytes = (ROOT / "ProfileSources/S1.42AI/FILE_INDEX.json").read_bytes()
    file_index = json.loads(file_index_bytes)
    export_record = next((x for x in file_index if x["path"] == "export.r2x"), None)
    if not export_record or sha256(export_bytes) != export_record["sha256"]:
        raise RuntimeError("export.r2x SHA disagrees with FILE_INDEX.json")
    export_text = export_bytes.decode("utf-8-sig")
    packages = [
        {
            "package": m[0],
            "version": ".".join(m[1:4]),
            "enabled": m[4] == "true",
        }
        for m in PACKAGE_PATTERN.findall(export_text)
    ]
    if len(packages) != len(re.findall(r"(?m)^- name: ", export_text)):
        raise RuntimeError("Some export package entries were not parsed")
    if len({p["package"] for p in packages}) != len(packages):
        raise RuntimeError("Duplicate package identities in export")
    enabled = [p for p in packages if p["enabled"]]
    if len(enabled) != EXPECTED_ENABLED_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_ENABLED_COUNT} enabled packages, got {len(enabled)}")
    enabled_names = {p["package"] for p in enabled}
    all_exclusions = set(PRIOR_BATCH_PACKAGES) | set(SEPARATE_AUTHORITY_PACKAGES)
    missing = sorted(all_exclusions - enabled_names)
    if missing:
        raise RuntimeError("Evidence-routed exclusion is not enabled in exact S1.42AI: " + ", ".join(missing))
    remaining = [p for p in enabled if p["package"] not in all_exclusions]
    embedded_dlls = [x for x in file_index if x["path"].lower().endswith(".dll")]
    return {
        "candidate": candidate,
        "profile_sha256": sha256(profile_bytes),
        "export_sha256": sha256(export_bytes),
        "file_index_sha256": sha256(file_index_bytes),
        "packages": packages,
        "enabled": enabled,
        "remaining": remaining,
        "embedded_dlls": embedded_dlls,
    }


def is_managed_pe(data: bytes) -> bool:
    # PE CLI metadata directory check. This distinguishes managed assemblies from
    # native DLLs without relying on file names or package names.
    if len(data) < 0x100 or data[:2] != b"MZ":
        return False
    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if pe_offset + 0x18 >= len(data) or data[pe_offset:pe_offset + 4] != b"PE\0\0":
        return False
    optional = pe_offset + 24
    magic = struct.unpack_from("<H", data, optional)[0]
    if magic == 0x10B:
        data_dir = optional + 96
    elif magic == 0x20B:
        data_dir = optional + 112
    else:
        return False
    cli = data_dir + 14 * 8
    if cli + 8 > len(data):
        return False
    rva, size = struct.unpack_from("<II", data, cli)
    return rva != 0 and size != 0


def classify(features: dict[str, bool]) -> list[str]:
    reasons: list[str] = []
    enemy_context = (
        features["enemy_ai_ref"]
        or features["enemy_ai_subclass"]
        or features["enemy_type_ref"]
        or features["enemy_prefab_ref"]
        or features["enemy_nest"]
    )
    if features["roundmanager_spawn_enemy"]:
        reasons.append("direct_roundmanager_spawn_enemy")
    if features["unity_instantiate"] and enemy_context:
        reasons.append("enemy_context_instantiate")
    if features["networkobject_spawn"] and enemy_context:
        reasons.append("enemy_context_network_spawn")
    if features["enemy_ai_subclass"] and features["spawn_enemy_named_member"]:
        reasons.append("enemyai_subclass_spawn_named_surface")
    if features["patch_or_detour"] and (
        features["enemy_vent"]
        or features["enemy_nest"]
        or features["roundmanager_spawn_batches"]
        or features["roundmanager_spawn_enemy"]
    ):
        reasons.append("enemy_spawn_lifecycle_patch_or_detour")
    if features["spawn_enemy_named_member"] and enemy_context:
        reasons.append("enemy_context_spawn_named_surface")
    return sorted(set(reasons))


def matched_il_lines(il: str, limit: int = 240) -> list[dict]:
    hits = []
    for number, line in enumerate(il.splitlines(), 1):
        names = [name for name, regex in IL_FEATURES.items() if regex.search(line)]
        if names:
            hits.append({"line": number, "features": names, "text": line[:1200]})
            if len(hits) >= limit:
                break
    return hits


def bounded_source_excerpts(source: str, limit_blocks: int = 180, radius: int = 2) -> list[dict]:
    lines = source.splitlines()
    blocks = []
    seen = set()
    for i, line in enumerate(lines):
        if not SOURCE_HIT.search(line):
            continue
        start = max(0, i - radius)
        end = min(len(lines), i + radius + 1)
        key = (start, end)
        if key in seen:
            continue
        seen.add(key)
        blocks.append({
            "start_line": start + 1,
            "end_line": end,
            "lines": lines[start:end],
        })
        if len(blocks) >= limit_blocks:
            break
    return blocks


def safe_slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)[:140]


def download(url: str, target: Path) -> tuple[int, str]:
    total = 0
    digest = hashlib.sha256()
    request = urllib.request.Request(url, headers={"User-Agent": "s142ai-spawn-owner-discovery/2"})
    with urllib.request.urlopen(request, timeout=180) as response, target.open("wb") as output:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > MAX_PACKAGE_BYTES:
                raise RuntimeError("Package exceeds bounded 2 GiB archive limit: " + url)
            digest.update(block)
            output.write(block)
    return total, digest.hexdigest()


def inspect_package(index: int, package: dict, work: Path) -> dict:
    name = package["package"]
    version = package["version"]
    url = f"https://gcdn.thunderstore.io/live/repository/packages/{name}-{version}.zip"
    archive_path = work / f"{index:03d}-{safe_slug(name)}.zip"
    print(f"[{index:03d}] downloading exact package {name} {version}", flush=True)
    zip_bytes, zip_sha = download(url, archive_path)
    record = {
        "index": index,
        "package": name,
        "version": version,
        "url": url,
        "zip_sha256": zip_sha,
        "zip_bytes": zip_bytes,
        "dll_members": [],
        "managed_dll_count": 0,
        "positive_candidate_dll_count": 0,
        "positive_reasons": [],
        "qualification": "Exact-byte static discovery only. No positive hit means no configured signature matched; it does not prove package safety or absence of every possible spawn path.",
    }
    with zipfile.ZipFile(archive_path) as archive:
        dll_members = [m for m in archive.infolist() if not m.is_dir() and m.filename.lower().endswith(".dll")]
        for dll_index, member in enumerate(dll_members):
            if member.file_size > MAX_DLL_BYTES:
                raise RuntimeError(f"DLL exceeds bounded 128 MiB limit: {name}/{member.filename}")
            data = archive.read(member)
            managed = is_managed_pe(data)
            dll = {
                "member": member.filename,
                "bytes": len(data),
                "sha256": sha256(data),
                "managed_pe": managed,
                "features": {},
                "positive_reasons": [],
            }
            if not managed:
                record["dll_members"].append(dll)
                continue
            record["managed_dll_count"] += 1
            dll_path = work / f"{index:03d}-{dll_index:03d}.dll"
            dll_path.write_bytes(data)
            try:
                il, il_stderr = run(["ilspycmd", "-il", str(dll_path)], timeout=300)
                if len(il) > MAX_IL_CHARS:
                    raise RuntimeError(f"IL output exceeds bounded 80 MiB limit: {name}/{member.filename}")
                features = {key: bool(regex.search(il)) for key, regex in IL_FEATURES.items()}
                reasons = classify(features)
                dll.update({
                    "il_sha256": sha256(il.encode("utf-8")),
                    "il_chars": len(il),
                    "il_decompiler_stderr": il_stderr[-4000:],
                    "features": features,
                    "il_feature_lines": matched_il_lines(il),
                    "positive_reasons": reasons,
                })
                if reasons:
                    source, source_stderr = run(["ilspycmd", str(dll_path)], timeout=300)
                    if len(source) > MAX_SOURCE_CHARS:
                        raise RuntimeError(f"Source output exceeds bounded 80 MiB limit: {name}/{member.filename}")
                    dll.update({
                        "source_sha256": sha256(source.encode("utf-8")),
                        "source_line_count": len(source.splitlines()),
                        "source_decompiler_stderr": source_stderr[-4000:],
                        "source_excerpts": bounded_source_excerpts(source),
                    })
                    record["positive_candidate_dll_count"] += 1
                    record["positive_reasons"].extend(reasons)
            finally:
                dll_path.unlink(missing_ok=True)
            record["dll_members"].append(dll)
    record["positive_reasons"] = sorted(set(record["positive_reasons"]))
    archive_path.unlink(missing_ok=True)
    return record


def scan(args: argparse.Namespace) -> None:
    context = load_context()
    shard_index = args.shard_index
    shard_count = args.shard_count
    if not (0 <= shard_index < shard_count):
        raise RuntimeError("Invalid shard index/count")
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = Path(os.environ.get("RUNNER_TEMP", str(out / ".work"))) / f"s142ai-remaining-owner-{shard_index:02d}"
    work.mkdir(parents=True, exist_ok=True)
    remaining = context["remaining"]
    assigned = [(i, p) for i, p in enumerate(remaining) if i % shard_count == shard_index]
    manifest = {
        "schema_version": 2,
        "purpose": "S1.42AI-DIAG1 remaining enabled-package EnemyAI/spawn-owner discovery",
        "analysis_head": git("rev-parse", "HEAD"),
        "canonical_main": EXPECTED_MAIN,
        "profile": {
            "path": context["candidate"]["profile"],
            "sha256": context["profile_sha256"],
            "export_sha256": context["export_sha256"],
            "file_index_sha256": context["file_index_sha256"],
        },
        "decompiler": {"tool": "ilspycmd", "version": ILSPY_VERSION},
        "enabled_package_count": len(context["enabled"]),
        "remaining_package_count": len(remaining),
        "prior_batch_exclusions": PRIOR_BATCH_PACKAGES,
        "separate_authority_exclusions": SEPARATE_AUTHORITY_PACKAGES,
        "embedded_profile_dlls_not_thunderstore_package_scan": context["embedded_dlls"],
        "shard_index": shard_index,
        "shard_count": shard_count,
        "assigned": [{"index": i, **p} for i, p in assigned],
        "reports": [],
        "qualification": "Discovery only. Exclusions are routed to existing exact authorities, not declared safe. Negative scan results are not patch-safety approvals.",
    }
    for index, package in assigned:
        record = inspect_package(index, package, work)
        name = f"PACKAGE_{index:03d}_{safe_slug(package['package'])}.json"
        payload = (json.dumps(record, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        (out / name).write_bytes(payload)
        manifest["reports"].append({
            "file": name,
            "sha256": sha256(payload),
            "bytes": len(payload),
            "package": package["package"],
            "version": package["version"],
            "zip_sha256": record["zip_sha256"],
            "positive_candidate_dll_count": record["positive_candidate_dll_count"],
            "positive_reasons": record["positive_reasons"],
        })
        # Persist the shard manifest after every package so a failed shard still
        # retains precise progress for diagnosis, while the aggregate job remains
        # fail-closed and will not run unless all shards succeed.
        manifest_path = out / f"SHARD_{shard_index:02d}_MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not assigned:
        (out / f"SHARD_{shard_index:02d}_MANIFEST.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(json.dumps({
        "shard": shard_index,
        "assigned": len(assigned),
        "completed": len(manifest["reports"]),
        "positive_packages": sum(bool(x["positive_reasons"]) for x in manifest["reports"]),
    }, indent=2))


def aggregate(args: argparse.Namespace) -> None:
    context = load_context()
    root = Path(args.aggregate).resolve()
    shard_manifests = sorted(root.rglob("SHARD_*_MANIFEST.json"))
    if len(shard_manifests) != args.shard_count:
        raise RuntimeError(f"Expected {args.shard_count} shard manifests, found {len(shard_manifests)}")
    package_reports = sorted(root.rglob("PACKAGE_*.json"))
    records = [json.loads(path.read_text(encoding="utf-8")) for path in package_reports]
    expected = context["remaining"]
    if len(records) != len(expected):
        raise RuntimeError(f"Expected {len(expected)} package reports, found {len(records)}")
    by_index = {record["index"]: record for record in records}
    if len(by_index) != len(records):
        raise RuntimeError("Duplicate package report indices")
    for index, package in enumerate(expected):
        record = by_index.get(index)
        if not record:
            raise RuntimeError(f"Missing package report at index {index}: {package['package']}")
        if record["package"] != package["package"] or record["version"] != package["version"]:
            raise RuntimeError(f"Package identity mismatch at index {index}")
    positive = [r for r in records if r["positive_candidate_dll_count"]]
    registration_only = []
    no_positive = []
    managed_dll_count = 0
    positive_dll_count = 0
    for record in records:
        managed_dll_count += record["managed_dll_count"]
        positive_dll_count += record["positive_candidate_dll_count"]
        if record["positive_candidate_dll_count"]:
            continue
        any_registration = any(
            d.get("managed_pe") and d.get("features", {}).get("register_enemy")
            for d in record["dll_members"]
        )
        if any_registration:
            registration_only.append(record)
        else:
            no_positive.append(record)
    summary = {
        "schema_version": 2,
        "status": "DISCOVERY_COMPLETE_REVIEW_REQUIRED",
        "purpose": "S1.42AI-DIAG1 remaining enabled-package EnemyAI/spawn-owner discovery aggregate",
        "canonical_main": EXPECTED_MAIN,
        "analysis_head": git("rev-parse", "HEAD"),
        "profile": {
            "path": context["candidate"]["profile"],
            "sha256": context["profile_sha256"],
            "export_sha256": context["export_sha256"],
            "file_index_sha256": context["file_index_sha256"],
        },
        "enabled_package_count": len(context["enabled"]),
        "excluded_prior_batch_count": len(PRIOR_BATCH_PACKAGES),
        "excluded_separate_authority_count": len(SEPARATE_AUTHORITY_PACKAGES),
        "scanned_remaining_package_count": len(records),
        "managed_dll_count": managed_dll_count,
        "positive_candidate_package_count": len(positive),
        "positive_candidate_dll_count": positive_dll_count,
        "registration_only_package_count": len(registration_only),
        "no_positive_signature_package_count": len(no_positive),
        "positive_packages": [
            {
                "index": r["index"],
                "package": r["package"],
                "version": r["version"],
                "zip_sha256": r["zip_sha256"],
                "positive_reasons": r["positive_reasons"],
                "candidate_dlls": [
                    {
                        "member": d["member"],
                        "sha256": d["sha256"],
                        "positive_reasons": d.get("positive_reasons", []),
                    }
                    for d in r["dll_members"] if d.get("positive_reasons")
                ],
            }
            for r in positive
        ],
        "registration_only_packages": [
            {"index": r["index"], "package": r["package"], "version": r["version"], "zip_sha256": r["zip_sha256"]}
            for r in registration_only
        ],
        "prior_batch_exclusions": PRIOR_BATCH_PACKAGES,
        "separate_authority_exclusions": SEPARATE_AUTHORITY_PACKAGES,
        "qualification": (
            "Only positive discovery candidates are eligible for escalation into exact method/caller/state/lifecycle review. "
            "Registration-only and no-positive-signature results are not declarations of safety; they mean only that this exact-byte static signature pass found no direct owner candidate."
        ),
    }
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "AGGREGATE.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "scanned": len(records),
        "managed_dlls": managed_dll_count,
        "positive_packages": len(positive),
        "positive_dlls": positive_dll_count,
        "registration_only": len(registration_only),
        "no_positive_signature": len(no_positive),
    }, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-index", type=int, default=int(os.environ.get("SHARD_INDEX", "0")))
    parser.add_argument("--shard-count", type=int, default=int(os.environ.get("SHARD_COUNT", str(DEFAULT_SHARD_COUNT))))
    parser.add_argument("--output", default=os.environ.get("OWNER_OUTPUT", "remaining-owner-output"))
    parser.add_argument("--aggregate", help="Aggregate directory containing all shard artifacts")
    args = parser.parse_args()
    if args.aggregate:
        aggregate(args)
    else:
        scan(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
