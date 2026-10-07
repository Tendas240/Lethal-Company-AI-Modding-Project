#!/usr/bin/env python3
"""Bounded source-discovery pass for seven exact S1.42AI native spawn-owner packages.
This inventories candidate source locations; it does not approve patches or prove coverage.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "native-owner-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-native-owner-inspection"
SELECTED = (
    "NotezyTeam-LethalMinNightly", "XuXiaolan-CodeRebirth", "TeamXiaolan-DawnLib",
    "SoftDiamond-RollingGiant", "Ccode_lang-SirenHead",
    "PureFPSZac-NestFix", "ButteryStancakes-SpawnCycleFixes",
)
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)
def sha(data):
    return hashlib.sha256(data).hexdigest()
def run(args):
    result = subprocess.run(args, capture_output=True, text=True, timeout=240)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed ({result.returncode}): {result.stderr[-3000:]}")
    return result.stdout, result.stderr
def write(name, value):
    data = (json.dumps(value, indent=2) + "\n").encode()
    (OUT / name).write_bytes(data)
    return {"file": name, "sha256": sha(data), "bytes": len(data)}

state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text())
candidate = state["active_candidate"]
if candidate["build_id"] != "S1.42AI":
    raise RuntimeError("Expected exact S1.42AI active artifact; reroute before inspection")
profile = ROOT / candidate["profile"]
if sha(profile.read_bytes()) != candidate["sha256"]:
    raise RuntimeError("Profile SHA mismatch")
with zipfile.ZipFile(profile) as archive:
    export_bytes = archive.read("export.r2x")
if export_bytes != (ROOT / "ProfileSources/S1.42AI/export.r2x").read_bytes():
    raise RuntimeError("Readable export differs from guarded archive")
file_index = json.loads((ROOT / "ProfileSources/S1.42AI/FILE_INDEX.json").read_text())
export_record = next(x for x in file_index if x["path"] == "export.r2x")
if sha(export_bytes) != export_record["sha256"]:
    raise RuntimeError("Export SHA disagrees with file index")
export = export_bytes.decode("utf-8-sig")
pattern = r"(?m)^- name: ([^\r\n]+)\r?\n  version:\r?\n    major: (\d+)\r?\n    minor: (\d+)\r?\n    patch: (\d+)\r?\n  enabled: (true|false)"
packages = [{"package": m[0], "version": ".".join(m[1:4]), "enabled": m[4] == "true"}
            for m in re.findall(pattern, export)]
if len(packages) != len(re.findall(r"(?m)^- name: ", export)):
    raise RuntimeError("Some package entries were not parsed")
if len({p["package"] for p in packages}) != len(packages):
    raise RuntimeError("Duplicate package identities")
by_name = {p["package"]: p for p in packages}
for name in SELECTED:
    if name not in by_name or not by_name[name]["enabled"]:
        raise RuntimeError("Selected owner package is not enabled: " + name)
manifest = {
    "schema_version": 1,
    "purpose": "S1.42AI-DIAG1 bounded native spawn-owner discovery, batch 1",
    "repository_commit": os.environ["GITHUB_SHA"],
    "profile": {"path": candidate["profile"], "sha256": candidate["sha256"],
                "export_sha256": sha(export_bytes)},
    "decompiler": {"tool": "ilspycmd", "version": "11.0.0.9375"},
    "selected_packages": list(SELECTED), "packages": [], "reports": [],
    "qualification": "Source token discovery only: hits include non-enemy spawns, declarations and inactive code. No patch approval or exhaustive game/mod coverage. Dependencies may remain unresolved.",
}
manifest["reports"].append(write("PROFILE_PACKAGE_INVENTORY.json", {
    "packages": packages,
    "enabled_count": sum(p["enabled"] for p in packages),
    "excluded_from_this_batch": [p["package"] for p in packages if p["enabled"] and p["package"] not in SELECTED],
    "embedded_dlls": [p for p in file_index if p["path"].lower().endswith(".dll")],
}))
spawn_pattern = re.compile(r"\b(?:Instantiate(?:<[^>]+>)?|Spawn(?:AsPlayerObject|WithOwnership)?|SpawnEnemy\w*|Spawn\w*(?:Server|Client)Rpc|RegisterEnemy|AddEnemyToPool)\s*\(")
owner_pattern = re.compile(r"\b(?:RoundManager|EnemyAINestSpawnObject|EnemyVent|EnemyAI|WeedEnemies|specialEnemyRarity|HarmonyPatch)\b")
declaration_pattern = re.compile(r"^\s*(?:namespace\s+|(?:(?:public|private|internal|protected|abstract|sealed|static|partial)\s+)*class\s+)")
for name in SELECTED:
    package = by_name[name]
    url = f"https://gcdn.thunderstore.io/live/repository/packages/{name}-{package['version']}.zip"
    archive_path = WORK / (name + ".zip")
    print("Downloading exact package " + name + " " + package["version"], flush=True)
    with urllib.request.urlopen(url, timeout=120) as response, archive_path.open("wb") as output:
        size = 0
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            size += len(block)
            if size > 1536 * 1024 * 1024:
                raise RuntimeError("Package download exceeds bounded 1.5 GiB limit")
            output.write(block)
    record = {"package": name, "version": package["version"], "url": url,
              "zip_sha256": sha(archive_path.read_bytes()), "zip_bytes": size, "assemblies": []}
    with zipfile.ZipFile(archive_path) as archive:
        dlls = [m for m in archive.infolist() if m.filename.lower().endswith(".dll")]
        if not dlls:
            raise RuntimeError("Expected managed owner DLLs in " + name)
        for index, member in enumerate(dlls):
            if member.file_size > 64 * 1024 * 1024:
                raise RuntimeError("DLL exceeds bounded 64 MiB limit")
            data = archive.read(member)
            path = WORK / f"{name}-{index}.dll"
            path.write_bytes(data)
            print("Inspecting " + name + " / " + member.filename, flush=True)
            listing, listing_stderr = run(["ilspycmd", "-l", "c", str(path)])
            source, decompile_stderr = run(["ilspycmd", str(path)])
            lines = source.splitlines()
            def hits(regex):
                return [{"line": i + 1, "text": line} for i, line in enumerate(lines) if regex.search(line)]
            report = {"package": name, "version": package["version"], "member": member.filename,
                      "assembly_sha256": sha(data), "source_sha256": sha(source.encode()),
                      "source_line_count": len(lines),
                      "class_listing": listing.splitlines(),
                      "declarations": hits(declaration_pattern),
                      "spawn_surface_hits": hits(spawn_pattern),
                      "owner_or_patch_hits": hits(owner_pattern),
                      "decompiler_stderr": listing_stderr + decompile_stderr,
                      "decompiler_annotation_count": sum("Unknown result type" in line or "Expected O" in line for line in lines),
                      "qualification": manifest["qualification"]}
            if sum(len(report[k]) for k in ("declarations", "spawn_surface_hits", "owner_or_patch_hits")) > 12000:
                raise RuntimeError("Bounded discovery report exceeds 12000 source records")
            report_name = f"{name}-{index}-DISCOVERY.json"
            metadata = write(report_name, report)
            manifest["reports"].append(metadata)
            record["assemblies"].append({"member": member.filename, "sha256": sha(data),
                "source_sha256": report["source_sha256"], "report": report_name,
                "spawn_hits": len(report["spawn_surface_hits"]),
                "owner_hits": len(report["owner_or_patch_hits"]),
                "classes": len(report["class_listing"])})
            path.unlink()
    manifest["packages"].append(record)
    write("MANIFEST.json", manifest)
    archive_path.unlink()
print(json.dumps({"profile": manifest["profile"], "packages": manifest["packages"]}, indent=2))
