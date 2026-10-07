#!/usr/bin/env python3
"""Read-only, version-bound evidence capture for the S1.42AI ShyGuy isolation review.
Outputs bounded type/method evidence and hashes only; never changes a profile or controller.
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
OUT = ROOT / "inspection-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "shyguy-contract-inspection"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)
manifest = {"purpose": "S1.42AI-DIAG1 pre-implementation identity and spawn contract review",
            "repository_commit": os.environ["GITHUB_SHA"], "packages": [], "decompiles": [],
            "qualification": "Static inspection only. V81 NuGet references are not proof of installed game method bodies."}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(args):
    p = subprocess.run(args, capture_output=True, text=True, timeout=180)
    if p.returncode:
        raise RuntimeError(f"Command failed: {args[0]}: {p.stderr[-2500:]}")
    return p.stdout

def write(name, text):
    (OUT / name).write_text(text, encoding="utf-8")

def focused(source, pattern):
    lines = source.splitlines()
    indices = set()
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            indices.update(range(max(0, i - 8), min(len(lines), i + 36)))
    if len(indices) > 1800:
        raise RuntimeError("Focused source scope exceeded 1800 lines; narrow the selector")
    return "\n".join(f"{i+1}: {lines[i]}" for i in sorted(indices)) + "\n"

state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text())
candidate = state["active_candidate"]
assert candidate["build_id"] == "S1.42AI"
profile = ROOT / candidate["profile"]
assert sha(profile.read_bytes()) == candidate["sha256"]
manifest["profile"] = {"path": candidate["profile"], "sha256": candidate["sha256"]}
with zipfile.ZipFile(profile) as z:
    export = z.read("export.r2x").decode("utf-8-sig")
    patch_member = "BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll"
    patch = z.read(patch_member)
    manifest["existing_patch"] = {"member": patch_member, "sha256": sha(patch),
        "source_sha256": sha((ROOT / "Patches/S139CompatibilityFixes/Plugin.cs").read_bytes()),
        "csproj_sha256": sha((ROOT / "Patches/S139CompatibilityFixes/S139CompatibilityFixes.csproj").read_bytes())}
    (WORK / "S139CompatibilityFixes.dll").write_bytes(patch)
    expected_export = (ROOT / "ProfileSources/S1.42AI/export.r2x").read_bytes()
    assert z.read("export.r2x") == expected_export

package_ids = ("theunknowncod3r-Scopophobia", "SoftDiamond-BrutalCompanyMinusExtraReborn")
for package in package_ids:
    match = re.search(r"(?m)^- name: " + re.escape(package) +
        r"\r?\n  version:\r?\n    major: (\d+)\r?\n    minor: (\d+)\r?\n    patch: (\d+)\r?\n  enabled: true", export)
    if not match:
        raise RuntimeError("Exact enabled package not found in candidate: " + package)
    version = ".".join(match.groups())
    url = f"https://gcdn.thunderstore.io/live/repository/packages/{package}-{version}.zip"
    archive = WORK / (package + ".zip")
    urllib.request.urlretrieve(url, archive)
    package_record = {"package": package, "version": version, "url": url,
                      "zip_sha256": sha(archive.read_bytes()), "assemblies": []}
    with zipfile.ZipFile(archive) as z:
        for index, member in enumerate(z.namelist()):
            if not member.lower().endswith(".dll"):
                continue
            data = z.read(member)
            dll = WORK / (package + "-" + str(index) + ".dll")
            dll.write_bytes(data)
            listing = run(["ilspycmd", "-l", "c", str(dll)])
            types = [line.removeprefix("Class ").strip() for line in listing.splitlines() if line.startswith("Class ")]
            package_record["assemblies"].append({"member": member, "sha256": sha(data), "types": types})
            write(package + "-types.json", json.dumps(package_record, indent=2) + "\n")
            if "Scopophobia" in package:
                selected = [t for t in types if t in ("ShyGuy.AI.ShyGuyAI", "Scopophobia.ScopophobiaPlugin", "Scopophobia.EnemyDataManager", "Scopophobia.EnemyHelper", "Scopophobia.Patches.GetShyGuyPrefabForLaterUse", "Scopophobia.ShyGuyPaintingProp")]
                markers = r"class |EnemyType|enemyName|enemyPrefab|ShyGuy|Register|Spawn|spawn|Awake\(|Start\(|OnNetwork"
            else:
                selected = [t for t in types if t in ("BrutalCompanyMinus.Minus.Events.ShyGuy",
                    "BrutalCompanyMinus.Minus.EventManager", "BrutalCompanyMinus.Minus.Manager",
                    "BrutalCompanyMinus.Minus.MEvent", "BrutalCompanyMinus.Assets")]
                markers = r"class |ShyGuy|GetEnemy\(|EnemyList|ChooseEvents|RandomWeightedEvent|ApplyEvents|forcedEvents|EventsToSpawnWith|Execute\(|InsideEnemies\(|OutsideEnemies\(|DoSpawn|Instantiate|AddEnemyToPool"
            for typename in selected:
                source = run(["ilspycmd", "-t", typename, str(dll)])
                name = re.sub(r"[^A-Za-z0-9_.-]", "_", package + "-" + typename) + ".txt"
                report = focused(source, markers)
                write(name, report)
                manifest["decompiles"].append({"package": package, "type": typename, "report": name,
                    "source_sha256": sha(source.encode()), "report_sha256": sha(report.encode())})
    manifest["packages"].append(package_record)

# Inspect only the exact game reference version already used by the project.
cache = Path.home() / ".nuget/packages/lethalcompany.gamelibs.steam/81.0.5-ngd.0"
game_dlls = list(cache.rglob("Assembly-CSharp.dll"))
if len(game_dlls) != 1:
    raise RuntimeError(f"Expected one exact V81 reference Assembly-CSharp, found {len(game_dlls)}")
game_dll = game_dlls[0]
source = run(["ilspycmd", "-t", "RoundManager", str(game_dll)])
report = focused(source, r"class RoundManager|SpawnEnemy|SpawnRandom|BeginEnemySpawning|PredictAllOutsideEnemies|FinishGeneratingNewLevel|Instantiate")
write("V81_REFERENCE_RoundManager.txt", report)
manifest["game_reference"] = {"package": "LethalCompany.GameLibs.Steam", "version": "81.0.5-ngd.0",
    "assembly_sha256": sha(game_dll.read_bytes()),
    "report": "V81_REFERENCE_RoundManager.txt",
    "source_sha256": sha(source.encode()),
    "has_instantiate_token": "Instantiate" in source,
    "qualification": "Reference metadata only unless nonstub method bodies and installed-game provenance are separately verified."}

# Inspect the actual compatibility DLL extracted from the guarded profile, not a loose historic copy.
source = run(["ilspycmd", "-t", "S139CompatibilityFixes.DiagnosticEnemyIsolation", str(WORK / "S139CompatibilityFixes.dll")])
report = focused(source, r"class |Targets|Allowed|Pikmin|FilterPool|ShouldRun|ApplyToCurrentLevel|RemoveEscaped|Spawn|Enabled|Gordion")
write("S1.42AI_embedded_DiagnosticEnemyIsolation.txt", report)
manifest["existing_patch"]["decompile_sha256"] = sha(source.encode())
manifest["existing_patch"]["report"] = "S1.42AI_embedded_DiagnosticEnemyIsolation.txt"

write("MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"profile": manifest["profile"], "packages": [
    {"package": p["package"], "version": p["version"], "assemblies": [
        {"member": a["member"], "sha256": a["sha256"]} for a in p["assemblies"]]} for p in manifest["packages"]],
    "decompiled_types": [d["type"] for d in manifest["decompiles"]],
    "game_reference": manifest["game_reference"]}, indent=2))
