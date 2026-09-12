#!/usr/bin/env python3
"""Exact S1.42AI cross-assembly consumer scan for SnowyLib and InteractiveTerminalAPI spawn APIs.

This is a bounded static consumer-coverage tool. It scans every enabled Thunderstore
package in the exact guarded S1.42AI export plus every embedded managed DLL in the
guarded profile archive. It first uses raw .NET metadata-string markers, then fully
decompiles only candidates with pinned ILSpy and records exact call/reflection evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MAIN = "8b4e6f832a6fee38dc92d17f491f4060f390e336"
EXPECTED_BUILD = "S1.42AI"
EXPECTED_PROFILE_SHA256 = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
EXPECTED_ENABLED_COUNT = 183
EXPECTED_EMBEDDED_DLL_COUNT = 5
ILSPY_VERSION = "11.0.0.9375"
DEFAULT_SHARD_COUNT = 12
MAX_PACKAGE_BYTES = 2 * 1024 * 1024 * 1024
MAX_DLL_BYTES = 512 * 1024 * 1024
MAX_TEXT_CHARS = 100 * 1024 * 1024

SNOWY_PROVIDER_PACKAGE = "Snowlance-SnowyLib"
ITA_PROVIDER_PACKAGE = "WhiteSpike-Interactive_Terminal_API"

PACKAGE_PATTERN = re.compile(
    r"(?m)^- name: ([^\r\n]+)\r?\n"
    r"  version:\r?\n"
    r"    major: (\d+)\r?\n"
    r"    minor: (\d+)\r?\n"
    r"    patch: (\d+)\r?\n"
    r"  enabled: (true|false)"
)

SNOWY_DIRECT_IL = re.compile(
    r"(?P<line>.*SnowyLib\.(?:NetworkHandler|Utils)::SpawnEnemy(?:Rpc)?\s*\(.*)"
)
ITA_DIRECT_IL = re.compile(
    r"(?P<line>.*InteractiveTerminalAPI\.Util\.Tools::SpawnMob\s*\(.*)"
)
REFLECTION_SOURCE = re.compile(r"\b(?:GetMethod|GetMethods|GetType|Type\.GetType|Assembly\.Load|GetTypes)\b")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr[-2000:]))
    return result.stdout.strip()

def run(args: list[str], timeout: int = 360) -> tuple[str, str]:
    result = subprocess.run(args, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed ({result.returncode}): {result.stderr[-5000:]}")
    return result.stdout, result.stderr

def verify_analysis_branch_delta() -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_MAIN, "HEAD"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode:
        raise RuntimeError("Expected canonical main is not an ancestor of analysis HEAD")
    changed = [x for x in git("diff", "--name-only", EXPECTED_MAIN + "..HEAD").splitlines() if x]
    allowed = {
        "AnalysisTools/inspect_spawn_api_cross_consumers.py",
        ".github/workflows/spawn-api-cross-consumer-review.yml",
    }
    unexpected = sorted(set(changed) - allowed)
    if unexpected:
        raise RuntimeError("Unexpected analysis-branch delta: " + ", ".join(unexpected))

def is_managed_pe(data: bytes) -> bool:
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

def load_context() -> dict:
    verify_analysis_branch_delta()
    state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text(encoding="utf-8"))
    candidate = state["active_candidate"]
    if candidate["build_id"] != EXPECTED_BUILD or candidate["sha256"] != EXPECTED_PROFILE_SHA256:
        raise RuntimeError("Active candidate/profile identity changed; reroute before scanning")
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
    enabled = [p for p in packages if p["enabled"]]
    if len(enabled) != EXPECTED_ENABLED_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_ENABLED_COUNT} enabled packages, got {len(enabled)}")
    enabled_names = {p["package"] for p in enabled}
    for required in (SNOWY_PROVIDER_PACKAGE, ITA_PROVIDER_PACKAGE):
        if required not in enabled_names:
            raise RuntimeError(f"Required provider package missing from exact S1.42AI: {required}")
    embedded_dlls = [x for x in file_index if x["path"].lower().endswith(".dll")]
    if len(embedded_dlls) != EXPECTED_EMBEDDED_DLL_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_EMBEDDED_DLL_COUNT} embedded DLLs, got {len(embedded_dlls)}"
        )
    return {
        "candidate": candidate,
        "profile": profile,
        "profile_sha256": sha256(profile_bytes),
        "export_sha256": sha256(export_bytes),
        "file_index_sha256": sha256(file_index_bytes),
        "enabled": enabled,
        "embedded_dlls": embedded_dlls,
    }

def safe_slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)[:150]

def download(url: str, target: Path) -> tuple[int, str]:
    total = 0
    digest = hashlib.sha256()
    req = urllib.request.Request(url, headers={"User-Agent": "s142ai-cross-consumer-review/1"})
    with urllib.request.urlopen(req, timeout=180) as response, target.open("wb") as output:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            total += len(block)
            if total > MAX_PACKAGE_BYTES:
                raise RuntimeError("Package exceeds bounded 2 GiB limit: " + url)
            digest.update(block)
            output.write(block)
    return total, digest.hexdigest()

def raw_markers(data: bytes) -> dict:
    snowy_provider = b"SnowyLib" in data or b"Snowlance.SnowyLib" in data
    snowy_method = b"SpawnEnemy" in data or b"SpawnEnemyRpc" in data
    ita_provider = b"InteractiveTerminalAPI" in data
    ita_method = b"SpawnMob" in data
    return {
        "snowylib_provider_marker": snowy_provider,
        "snowylib_spawn_method_marker": snowy_method,
        "interactive_terminal_api_provider_marker": ita_provider,
        "interactive_terminal_api_spawnmob_marker": ita_method,
        "snowylib_candidate": snowy_provider and snowy_method,
        "interactive_terminal_api_candidate": ita_provider and ita_method,
    }

def contexts(text: str, regex: re.Pattern, radius: int = 5, limit: int = 60) -> list[dict]:
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        if not regex.search(line):
            continue
        start = max(0, i - radius)
        end = min(len(lines), i + radius + 1)
        out.append({
            "line": i + 1,
            "start_line": start + 1,
            "end_line": end,
            "lines": lines[start:end],
        })
        if len(out) >= limit:
            break
    return out

def inspect_candidate(
    data: bytes,
    identity: str,
    package: str,
    member: str,
    out: Path,
    work: Path,
) -> dict:
    stem = safe_slug(identity)
    dll_path = work / f"{stem}.dll"
    dll_path.write_bytes(data)
    try:
        il, il_stderr = run(["ilspycmd", "-il", str(dll_path)])
        source, source_stderr = run(["ilspycmd", str(dll_path)])
    finally:
        dll_path.unlink(missing_ok=True)
    if len(il) > MAX_TEXT_CHARS or len(source) > MAX_TEXT_CHARS:
        raise RuntimeError(f"Decompiler output exceeds bounded limit: {identity}")
    snowy_direct = contexts(il, SNOWY_DIRECT_IL)
    ita_direct = contexts(il, ITA_DIRECT_IL)
    source_lines = source.splitlines()
    snowy_reflection = []
    ita_reflection = []
    for i, line in enumerate(source_lines):
        if REFLECTION_SOURCE.search(line):
            window = "\n".join(source_lines[max(0, i-6):min(len(source_lines), i+7)])
            if "snowylib" in window.lower() and "spawnenemy" in window.lower():
                snowy_reflection.append({"line": i+1, "context": window})
            if "interactiveterminalapi" in window.lower() and "spawnmob" in window.lower():
                ita_reflection.append({"line": i+1, "context": window})
    cs_name = f"{stem}.cs"
    il_name = f"{stem}.il"
    (out / cs_name).write_text(source, encoding="utf-8")
    (out / il_name).write_text(il, encoding="utf-8")
    return {
        "package": package,
        "member": member,
        "identity": identity,
        "dll_sha256": sha256(data),
        "source_sha256": sha256(source.encode("utf-8")),
        "il_sha256": sha256(il.encode("utf-8")),
        "source_lines": len(source_lines),
        "il_lines": len(il.splitlines()),
        "snowylib_direct_call_contexts": snowy_direct,
        "interactive_terminal_api_direct_call_contexts": ita_direct,
        "snowylib_reflection_contexts": snowy_reflection[:30],
        "interactive_terminal_api_reflection_contexts": ita_reflection[:30],
        "source_stderr": source_stderr[-4000:],
        "il_stderr": il_stderr[-4000:],
        "outputs": [cs_name, il_name],
    }

def manifest_dependencies(archive: zipfile.ZipFile) -> list[str]:
    candidates = [n for n in archive.namelist() if n.lower().endswith("manifest.json")]
    for name in candidates:
        try:
            obj = json.loads(archive.read(name).decode("utf-8-sig"))
            deps = obj.get("dependencies")
            if isinstance(deps, list):
                return [str(x) for x in deps]
        except Exception:
            continue
    return []

def inspect_package(index: int, package: dict, out: Path, work: Path) -> dict:
    name = package["package"]
    version = package["version"]
    url = f"https://gcdn.thunderstore.io/live/repository/packages/{name}-{version}.zip"
    archive_path = work / f"{index:03d}-{safe_slug(name)}.zip"
    print(f"[{index:03d}] {name} {version}", flush=True)
    zip_bytes, zip_sha = download(url, archive_path)
    rec = {
        "index": index,
        "package": name,
        "version": version,
        "url": url,
        "zip_sha256": zip_sha,
        "zip_bytes": zip_bytes,
        "dependencies": [],
        "managed_dll_count": 0,
        "dlls": [],
        "candidates": [],
    }
    with zipfile.ZipFile(archive_path) as archive:
        rec["dependencies"] = manifest_dependencies(archive)
        dll_members = [m for m in archive.infolist() if not m.is_dir() and m.filename.lower().endswith(".dll")]
        for di, member in enumerate(dll_members):
            if member.file_size > MAX_DLL_BYTES:
                raise RuntimeError(f"DLL exceeds bounded 512 MiB limit: {name}/{member.filename}")
            data = archive.read(member)
            managed = is_managed_pe(data)
            entry = {
                "member": member.filename,
                "bytes": len(data),
                "sha256": sha256(data),
                "managed_pe": managed,
                "raw_markers": {},
            }
            if managed:
                rec["managed_dll_count"] += 1
                markers = raw_markers(data)
                entry["raw_markers"] = markers
                if markers["snowylib_candidate"] or markers["interactive_terminal_api_candidate"]:
                    identity = f"{index:03d}-{di:03d}-{name}-{Path(member.filename).name}"
                    detail = inspect_candidate(data, identity, name, member.filename, out, work)
                    rec["candidates"].append(detail)
            rec["dlls"].append(entry)
    archive_path.unlink(missing_ok=True)
    return rec

def inspect_embedded(context: dict, out: Path, work: Path) -> list[dict]:
    results = []
    with zipfile.ZipFile(context["profile"]) as archive:
        for i, record in enumerate(context["embedded_dlls"]):
            path = record["path"]
            data = archive.read(path)
            actual = sha256(data)
            if actual != record["sha256"]:
                raise RuntimeError(f"Embedded DLL SHA mismatch: {path}")
            managed = is_managed_pe(data)
            entry = {
                "index": i,
                "path": path,
                "bytes": len(data),
                "sha256": actual,
                "managed_pe": managed,
                "raw_markers": {},
                "candidates": [],
            }
            if managed:
                markers = raw_markers(data)
                entry["raw_markers"] = markers
                if markers["snowylib_candidate"] or markers["interactive_terminal_api_candidate"]:
                    identity = f"embedded-{i:02d}-{Path(path).name}"
                    detail = inspect_candidate(data, identity, "__EMBEDDED_PROJECT_DLL__", path, out, work)
                    entry["candidates"].append(detail)
            results.append(entry)
    return results

def scan(args: argparse.Namespace) -> None:
    context = load_context()
    shard = args.shard_index
    count = args.shard_count
    if not (0 <= shard < count):
        raise RuntimeError("Invalid shard index/count")
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    work = Path(os.environ.get("RUNNER_TEMP", str(out / ".work"))) / f"cross-consumers-{shard:02d}"
    work.mkdir(parents=True, exist_ok=True)
    assigned = [(i, p) for i, p in enumerate(context["enabled"]) if i % count == shard]
    packages = [inspect_package(i, p, out, work) for i, p in assigned]
    embedded = inspect_embedded(context, out, work) if shard == 0 else []
    result = {
        "schema_version": 1,
        "purpose": "S1.42AI exact cross-assembly consumer scan for SnowyLib and InteractiveTerminalAPI spawn APIs",
        "canonical_main": EXPECTED_MAIN,
        "repository_commit": git("rev-parse", "HEAD"),
        "profile_sha256": context["profile_sha256"],
        "export_sha256": context["export_sha256"],
        "file_index_sha256": context["file_index_sha256"],
        "enabled_package_count": len(context["enabled"]),
        "embedded_dll_count": len(context["embedded_dlls"]),
        "shard_index": shard,
        "shard_count": count,
        "package_indices": [i for i, _ in assigned],
        "packages": packages,
        "embedded_dlls": embedded,
        "decompiler": {"tool": "ilspycmd", "version": ILSPY_VERSION},
        "qualification": "Static exact-byte consumer coverage. Direct IL calls and reflection-like marker contexts are captured; arbitrary runtime-generated reflection strings cannot be disproven by static analysis.",
    }
    (out / "SHARD.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    shutil.rmtree(work, ignore_errors=True)

def aggregate(args: argparse.Namespace) -> None:
    root = Path(args.aggregate).resolve()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    shard_files = sorted(root.rglob("SHARD.json"))
    if len(shard_files) != args.shard_count:
        raise RuntimeError(f"Expected {args.shard_count} SHARD.json files, got {len(shard_files)}")
    shards = [json.loads(p.read_text(encoding="utf-8")) for p in shard_files]
    for s in shards:
        if s["canonical_main"] != EXPECTED_MAIN or s["profile_sha256"] != EXPECTED_PROFILE_SHA256:
            raise RuntimeError("Shard provenance mismatch")
        if s["shard_count"] != args.shard_count:
            raise RuntimeError("Shard-count mismatch")
    packages = [p for s in shards for p in s["packages"]]
    if len(packages) != EXPECTED_ENABLED_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_ENABLED_COUNT} package records, got {len(packages)}")
    indices = sorted(p["index"] for p in packages)
    if indices != list(range(EXPECTED_ENABLED_COUNT)):
        raise RuntimeError("Enabled package coverage is not exact 0..182")
    names = [p["package"] for p in packages]
    if len(set(names)) != len(names):
        raise RuntimeError("Duplicate enabled package records")
    embedded = [e for s in shards for e in s["embedded_dlls"]]
    if len(embedded) != EXPECTED_EMBEDDED_DLL_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_EMBEDDED_DLL_COUNT} embedded DLL records, got {len(embedded)}")
    all_candidates = [c for p in packages for c in p["candidates"]]
    all_candidates += [c for e in embedded for c in e["candidates"]]
    external = [
        c for c in all_candidates
        if c["package"] not in {SNOWY_PROVIDER_PACKAGE, ITA_PROVIDER_PACKAGE}
    ]
    snowy_direct = [c for c in external if c["snowylib_direct_call_contexts"]]
    ita_direct = [c for c in external if c["interactive_terminal_api_direct_call_contexts"]]
    snowy_reflection = [c for c in external if c["snowylib_reflection_contexts"]]
    ita_reflection = [c for c in external if c["interactive_terminal_api_reflection_contexts"]]
    dependency_declared = []
    for p in packages:
        deps = [d for d in p.get("dependencies", []) if "SnowyLib" in d or "Interactive_Terminal_API" in d or "InteractiveTerminalAPI" in d]
        if deps:
            dependency_declared.append({"package": p["package"], "version": p["version"], "dependencies": deps})
    copied = []
    for sfile in shard_files:
        parent = sfile.parent
        for ext in ("*.cs", "*.il"):
            for path in parent.glob(ext):
                target = out / path.name
                if target.exists() and target.read_bytes() != path.read_bytes():
                    raise RuntimeError(f"Candidate output name collision: {path.name}")
                shutil.copy2(path, target)
                copied.append(path.name)
    summary = {
        "schema_version": 1,
        "status": "CROSS_ASSEMBLY_CONSUMER_SCAN_COMPLETE",
        "canonical_main": EXPECTED_MAIN,
        "profile_sha256": EXPECTED_PROFILE_SHA256,
        "enabled_packages_scanned": EXPECTED_ENABLED_COUNT,
        "embedded_dlls_scanned": EXPECTED_EMBEDDED_DLL_COUNT,
        "managed_dlls_scanned": sum(p["managed_dll_count"] for p in packages) + sum(1 for e in embedded if e["managed_pe"]),
        "raw_candidate_assemblies": len(all_candidates),
        "external_candidate_assemblies": len(external),
        "snowylib_external_direct_call_assemblies": len(snowy_direct),
        "interactive_terminal_api_external_direct_call_assemblies": len(ita_direct),
        "snowylib_external_reflection_candidate_assemblies": len(snowy_reflection),
        "interactive_terminal_api_external_reflection_candidate_assemblies": len(ita_reflection),
        "provider_dependency_declarations": dependency_declared,
        "external_candidates": external,
        "provider_self_candidates": [c for c in all_candidates if c["package"] in {SNOWY_PROVIDER_PACKAGE, ITA_PROVIDER_PACKAGE}],
        "candidate_outputs": sorted(set(copied)),
        "qualification": "Complete exact enabled-package plus embedded-DLL static scan for provider/method metadata markers. Direct IL calls and reflection-like contexts are exact for captured binaries; arbitrary runtime-generated reflection strings are outside static proof.",
    }
    (out / "VERIFICATION.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# S1.42AI cross-assembly spawn-API consumer scan",
        "",
        f"- Enabled packages scanned: **{EXPECTED_ENABLED_COUNT}**",
        f"- Embedded DLLs scanned: **{EXPECTED_EMBEDDED_DLL_COUNT}**",
        f"- Managed DLLs scanned: **{summary['managed_dlls_scanned']}**",
        f"- External raw candidate assemblies: **{len(external)}**",
        f"- SnowyLib external direct-call assemblies: **{len(snowy_direct)}**",
        f"- InteractiveTerminalAPI SpawnMob external direct-call assemblies: **{len(ita_direct)}**",
        f"- SnowyLib reflection-like external candidates: **{len(snowy_reflection)}**",
        f"- InteractiveTerminalAPI reflection-like external candidates: **{len(ita_reflection)}**",
        "",
        "## External candidates",
    ]
    if not external:
        lines.append("")
        lines.append("No external assembly contained the provider+spawn-method metadata combination after exact scan.")
    else:
        for c in external:
            lines.extend([
                "",
                f"### {c['package']} / `{c['member']}`",
                f"- DLL SHA-256: `{c['dll_sha256']}`",
                f"- SnowyLib direct call contexts: {len(c['snowylib_direct_call_contexts'])}",
                f"- InteractiveTerminalAPI direct call contexts: {len(c['interactive_terminal_api_direct_call_contexts'])}",
                f"- SnowyLib reflection contexts: {len(c['snowylib_reflection_contexts'])}",
                f"- InteractiveTerminalAPI reflection contexts: {len(c['interactive_terminal_api_reflection_contexts'])}",
            ])
    lines.extend([
        "",
        "## Qualification",
        "",
        summary["qualification"],
        "",
    ])
    (out / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--shard-index", type=int, default=int(os.environ.get("SHARD_INDEX", "0")))
    p.add_argument("--shard-count", type=int, default=int(os.environ.get("SHARD_COUNT", str(DEFAULT_SHARD_COUNT))))
    p.add_argument("--output", default=os.environ.get("CONSUMER_OUTPUT", "cross-consumer-output"))
    p.add_argument("--aggregate")
    args = p.parse_args()
    if args.aggregate:
        aggregate(args)
    else:
        scan(args)

if __name__ == "__main__":
    main()
