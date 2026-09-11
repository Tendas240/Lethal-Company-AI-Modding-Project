#!/usr/bin/env python3
"""Capture exact decompiles for S1.42AI-DIAG1 direct-owner patch-safety review.

Fail closed against the SHA-anchored NativeSpawnOwners discovery for LethalMin,
CodeRebirth and DawnLib/Dusk. Also probe the exact project V81 reference for the
remaining native vent/nest methods, explicitly without treating reference stubs as
installed-game source. Read-only evidence generation; no profile mutation.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "direct-owner-exact-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-direct-owner-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

EXPECTED = (
    {
        "package": "NotezyTeam-LethalMinNightly",
        "version": "1.1.108",
        "url": "https://gcdn.thunderstore.io/live/repository/packages/NotezyTeam-LethalMinNightly-1.1.108.zip",
        "zip_sha256": "7e5c62ecf39c950a6fa46c722ce3a77e3efd7328a71c32a6c5e4cf87a1f50fe1",
        "member": "NoteBoxz.LethalMin.dll",
        "dll_sha256": "9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df",
        "source_sha256": "6eb8f99dc6b6d72a705959aa2dfd452638561e1b4376b3c1e662ddd7d8c67939",
        "stem": "LethalMinNightly-1.1.108",
    },
    {
        "package": "XuXiaolan-CodeRebirth",
        "version": "1.6.9",
        "url": "https://gcdn.thunderstore.io/live/repository/packages/XuXiaolan-CodeRebirth-1.6.9.zip",
        "zip_sha256": "a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6",
        "member": "plugins/CodeRebirth/CodeRebirth.dll",
        "dll_sha256": "a35a06cf55a42dd1db9f3bcf68448d74590fdac8d9e80f57a811e78628c8fd36",
        "source_sha256": "da9399bca105f905c5c1995a222534f1c3672f971bd322ca9bd36aebb34614f3",
        "stem": "CodeRebirth-1.6.9",
    },
    {
        "package": "XuXiaolan-CodeRebirth",
        "version": "1.6.9",
        "url": "https://gcdn.thunderstore.io/live/repository/packages/XuXiaolan-CodeRebirth-1.6.9.zip",
        "zip_sha256": "a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6",
        "member": "plugins/CodeRebirth/com.local.Rodriguez.DuskReplacementEntities.CodeRebirth.dll",
        "dll_sha256": "308ddf095d807b719c204c48bee3ce26795281c6b399baf3ac105e6b9d258163",
        "source_sha256": "c8acb8d1c4f1bc6f2810ae660170910abce9181bf979d3896e46dedcff46338b",
        "stem": "CodeRebirth-DuskReplacement-1.6.9",
    },
    {
        "package": "TeamXiaolan-DawnLib",
        "version": "0.9.25",
        "url": "https://gcdn.thunderstore.io/live/repository/packages/TeamXiaolan-DawnLib-0.9.25.zip",
        "zip_sha256": "c33c608869763f916f07e5ddf47224134f98bab15d044bd809a46ef2d3d538c3",
        "member": "BepInEx/plugins/DawnLib/com.github.teamxiaolan.dawnlib.dll",
        "dll_sha256": "9b4826a16eec1fa5091fb4246d010005bc9c3e04282034e8d067b499ab5c125b",
        "source_sha256": "f9a1f2311803a02f67eeba3ed367fcbcd7d6aed8947f9fab709306391eae075e",
        "stem": "DawnLib-Core-0.9.25",
    },
    {
        "package": "TeamXiaolan-DawnLib",
        "version": "0.9.25",
        "url": "https://gcdn.thunderstore.io/live/repository/packages/TeamXiaolan-DawnLib-0.9.25.zip",
        "zip_sha256": "c33c608869763f916f07e5ddf47224134f98bab15d044bd809a46ef2d3d538c3",
        "member": "BepInEx/plugins/DawnLib/com.github.teamxiaolan.dawnlib.dusk.dll",
        "dll_sha256": "3582f1a35efe3753004d7b209aea355a6c02b646b61cc1629c53a311ba8d1f03",
        "source_sha256": "84aff93064e8bb27b05b80222fe0198bd631a7811547cd809651ce1b021072cb",
        "stem": "DawnLib-Dusk-0.9.25",
    },
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(args: list[str]) -> tuple[bytes, bytes]:
    result = subprocess.run(args, capture_output=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(
            f"{args[0]} failed ({result.returncode}): "
            + result.stderr.decode("utf-8", errors="replace")[-4000:]
        )
    return result.stdout, result.stderr


def download(url: str, path: Path) -> bytes:
    with urllib.request.urlopen(url, timeout=180) as response:
        data = response.read(384 * 1024 * 1024 + 1)
    if len(data) > 384 * 1024 * 1024:
        raise RuntimeError("Bounded package download exceeded 384 MiB")
    path.write_bytes(data)
    return data

verification = {
    "schema_version": 1,
    "purpose": "S1.42AI-DIAG1 exact LethalMin/CodeRebirth/DawnLib-Dusk direct-owner and native-reference-gap review",
    "repository_commit": os.environ.get("GITHUB_SHA"),
    "decompiler": {"tool": "ilspycmd", "version": "11.0.0.9375"},
    "assemblies": [],
    "game_reference": {},
    "qualification": (
        "Complete decompile/IL capture of five exact SHA-anchored mod assemblies for bounded patch-safety review. "
        "The V81 NuGet reference probe is metadata/reference evidence only and is not installed-game source. "
        "This evidence does not itself authorize a diagnostic build or gameplay test."
    ),
}

package_cache: dict[str, tuple[Path, bytes]] = {}
for item in EXPECTED:
    cache_key = item["url"]
    if cache_key not in package_cache:
        zip_path = WORK / (item["package"] + "-" + item["version"] + ".zip")
        package_bytes = download(item["url"], zip_path)
        actual_zip = sha256(package_bytes)
        if actual_zip != item["zip_sha256"]:
            raise RuntimeError(f"Package ZIP SHA mismatch for {item['package']}: {actual_zip}")
        package_cache[cache_key] = (zip_path, package_bytes)
    zip_path, package_bytes = package_cache[cache_key]

    with zipfile.ZipFile(zip_path) as archive:
        if item["member"] not in archive.namelist():
            raise RuntimeError(f"Exact DLL member missing: {item['member']}")
        dll_bytes = archive.read(item["member"])
    actual_dll = sha256(dll_bytes)
    if actual_dll != item["dll_sha256"]:
        raise RuntimeError(f"DLL SHA mismatch for {item['member']}: {actual_dll}")

    dll_path = WORK / (item["stem"] + ".dll")
    dll_path.write_bytes(dll_bytes)
    source, source_stderr = run(["ilspycmd", str(dll_path)])
    actual_source = sha256(source)
    if actual_source != item["source_sha256"]:
        raise RuntimeError(
            f"Decompiler source SHA mismatch for {item['member']}: {actual_source}; "
            "refusing review against bytes different from merged discovery evidence"
        )
    il, il_stderr = run(["ilspycmd", "-il", str(dll_path)])
    cs_name = item["stem"] + ".cs"
    il_name = item["stem"] + ".il"
    (OUT / cs_name).write_bytes(source)
    (OUT / il_name).write_bytes(il)
    verification["assemblies"].append({
        "package": item["package"], "version": item["version"], "member": item["member"],
        "package_zip_sha256": sha256(package_bytes), "dll_sha256": actual_dll,
        "decompiled_source_sha256": actual_source,
        "expected_discovery_source_sha256": item["source_sha256"],
        "source_bytes": len(source), "source_lines": len(source.decode("utf-8").splitlines()),
        "il_sha256": sha256(il), "il_bytes": len(il), "il_lines": len(il.decode("utf-8").splitlines()),
        "source_stderr": source_stderr.decode("utf-8", errors="replace"),
        "il_stderr": il_stderr.decode("utf-8", errors="replace"),
        "outputs": [cs_name, il_name],
    })

# Probe only the exact project reference version already restored by the project csproj.
cache = Path.home() / ".nuget/packages/lethalcompany.gamelibs.steam/81.0.5-ngd.0"
game_dlls = list(cache.rglob("Assembly-CSharp.dll"))
if len(game_dlls) != 1:
    raise RuntimeError(f"Expected one exact V81 reference Assembly-CSharp, found {len(game_dlls)}")
game_dll = game_dlls[0]
reference_record = {
    "package": "LethalCompany.GameLibs.Steam",
    "version": "81.0.5-ngd.0",
    "assembly_sha256": sha256(game_dll.read_bytes()),
    "types": [],
    "qualification": "Reference metadata only; stub bodies do not close installed V81 patch safety.",
}
for type_name in ("RoundManager", "EnemyAINestSpawnObject"):
    source, stderr = run(["ilspycmd", "-t", type_name, str(game_dll)])
    name = "V81_REFERENCE_" + type_name + ".cs"
    (OUT / name).write_bytes(source)
    text = source.decode("utf-8", errors="replace")
    reference_record["types"].append({
        "type": type_name,
        "source_sha256": sha256(source),
        "source_bytes": len(source),
        "source_lines": len(text.splitlines()),
        "throw_null_count": text.count("throw null"),
        "contains_AssignRandomEnemyToVent": "AssignRandomEnemyToVent" in text,
        "contains_specialEnemyRarity": "specialEnemyRarity" in text,
        "contains_Awake": "Awake(" in text,
        "contains_UseNestSpawnObject": "UseNestSpawnObject" in text,
        "stderr": stderr.decode("utf-8", errors="replace"),
        "output": name,
    })
verification["game_reference"] = reference_record

(OUT / "VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
print(json.dumps(verification, indent=2))
