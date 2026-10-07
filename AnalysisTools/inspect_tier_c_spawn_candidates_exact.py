#!/usr/bin/env python3
"""Exact full-source capture for the next six prioritized unreviewed S1.42AI spawn-owner candidates.

Read-only patch-safety evidence generation. Re-downloads the exact Thunderstore
versions, verifies package/DLL/source hashes from discovery run 34705334804,
and preserves complete C#/IL for method/caller/state/lifecycle review.
No profile, build controller, runtime controller, or gameplay state is changed.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tier-c-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-tier-c-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = "94be00f2ca31cb2caa4d0125e2bebb7573d22a50"
DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_tier_c_spawn_candidates_exact.py",
    ".github/workflows/tier-c-spawn-candidates-exact-review.yml",
}

EXPECTED = (
    {
        "package": "coderCleric-Poltergeist",
        "version": "1.2.12",
        "zip_sha256": "56e9c656ff9a17b9c1db4a22d0c1b739c32fb2f15a381464774ff41307ea4a45",
        "member": "BepInEx/plugins/Poltergeist.dll",
        "dll_sha256": "18d5f6c9251972b130decbac01141e467dc3259bc8754b660f6f0180c255e98f",
        "source_sha256": "f71a1a04d663f3240bac88bb2954449bcd18a6693a932dfaf0af08893e662505",
        "stem": "Poltergeist-1.2.12",
    },
    {
        "package": "Entity378-SellBodiesFixed",
        "version": "1.14.0",
        "zip_sha256": "55048f43733f19a6305441befee228e586c475eb340f1dfea3b01a8bae487522",
        "member": "BepInEx/plugins/SellBodies/SellBodies.dll",
        "dll_sha256": "3c3e43d8c27e55f9b4289b7f2d047aa1b1624c084c16c22a7f3a172345ad13c0",
        "source_sha256": "218c73d29adcc1c23a202958396942a5ec8267bfe8577e48b8f51cf852c194c7",
        "stem": "SellBodiesFixed-1.14.0",
    },
    {
        "package": "347956-JPOGRaptor",
        "version": "1.0.6",
        "zip_sha256": "57c9650f1d6a7cbdc449ee69427f84d1f065c506dffac3185d311f2f988f06a7",
        "member": "plugins/JPOGRaptor.dll",
        "dll_sha256": "ae2b8c752e229aa5a76083e1c4c641156f3a8294802a7edbebac325b4793b983",
        "source_sha256": "4bbe16720fe19ac4a5c1ad03b7c34f08e5f5b1f29486e49e8c673ecdbe462d78",
        "stem": "JPOGRaptor-1.0.6",
    },
    {
        "package": "ScienceBird-ScienceBird_Tweaks",
        "version": "4.7.5",
        "zip_sha256": "ebab97d5ab882e630f310bd1eedb23528402552c624365bcd3854de0684acd09",
        "member": "ScienceBird.ScienceBirdTweaks.dll",
        "dll_sha256": "ab9d87a037b090b3f80afbbaebd409254a024b81442d0280a9164a7811324059",
        "source_sha256": "2d53ffff42d3fe41a921980c459aaf791565099d249e075d86c29778da860686",
        "stem": "ScienceBird_Tweaks-4.7.5",
    },
    {
        "package": "ShaosilGaming-GeneralImprovements",
        "version": "1.5.5",
        "zip_sha256": "98d2791c715484aa190e326df6fc1a793aa57f36685678c0e55248ed49554d34",
        "member": "GeneralImprovements.dll",
        "dll_sha256": "5b7199e2b92b2880e2bf12f5198a4905a63b0a4633f1ad16c1ed43dd981f86c4",
        "source_sha256": "4d530ad36a7d1248a115b30bea3f74ba8a3d00ce1c70644b313613f2990e22d2",
        "stem": "GeneralImprovements-1.5.5",
    },
    {
        "package": "HQ_Team-LethalThingsReloaded",
        "version": "0.11.7",
        "zip_sha256": "c54671537ca04e6665570f56924cb5ceeeb63639e154d89e6d7e6440cf38d347",
        "member": "plugins/LethalThings.dll",
        "dll_sha256": "1f1923b2f104fc5b90774ef4369fa7c46f70c13159110096550fa61bf56dec62",
        "source_sha256": "4992a4e75b54e2544174b72af143d12b399994e7bd876d3510f48a75df2141aa",
        "stem": "LethalThingsReloaded-0.11.7",
    },
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), result.stderr[-2000:]))
    return result.stdout.strip()


def verify_analysis_branch_delta() -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", CANONICAL_MAIN, "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode:
        raise RuntimeError("Canonical main is not an ancestor of analysis HEAD")
    changed = [x for x in git("diff", "--name-only", CANONICAL_MAIN + "..HEAD").splitlines() if x]
    unexpected = sorted(set(changed) - ALLOWED_DELTA)
    if unexpected:
        raise RuntimeError("Unexpected analysis-branch delta: " + ", ".join(unexpected))


def run(args: list[str]) -> tuple[bytes, bytes]:
    result = subprocess.run(args, capture_output=True, timeout=420)
    if result.returncode:
        raise RuntimeError(
            f"{args[0]} failed ({result.returncode}): "
            + result.stderr.decode("utf-8", errors="replace")[-4000:]
        )
    if len(result.stdout) > MAX_OUTPUT_BYTES:
        raise RuntimeError(f"Decompiler output exceeded bounded {MAX_OUTPUT_BYTES} bytes")
    return result.stdout, result.stderr


def download(url: str, path: Path) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "s142ai-tier-c-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as response:
        data = response.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data


verify_analysis_branch_delta()
verification = {
    "schema_version": 1,
    "purpose": "S1.42AI-DIAG1 exact review capture for next six prioritized remaining discovery-positive spawn-owner candidates",
    "canonical_main": CANONICAL_MAIN,
    "repository_commit": os.environ.get("GITHUB_SHA"),
    "discovery_run": DISCOVERY_RUN,
    "discovery_head": DISCOVERY_HEAD,
    "decompiler": {"tool": "ilspycmd", "version": ILSPY_VERSION},
    "assemblies": [],
    "qualification": (
        "Complete C#/IL decompile of exactly six ZIP/DLL/source-SHA-anchored candidates from the prior discovery. "
        "This is method/caller/state/lifecycle evidence only; it does not authorize DIAG1 implementation, build, "
        "controller transition, Gale import, or gameplay."
    ),
}

for item in EXPECTED:
    url = f"https://gcdn.thunderstore.io/live/repository/packages/{item['package']}-{item['version']}.zip"
    zip_path = WORK / (item["package"] + "-" + item["version"] + ".zip")
    package_bytes = download(url, zip_path)
    actual_zip = sha256(package_bytes)
    if actual_zip != item["zip_sha256"]:
        raise RuntimeError(f"ZIP SHA mismatch for {item['package']}: {actual_zip}")
    with zipfile.ZipFile(zip_path) as archive:
        if item["member"] not in archive.namelist():
            raise RuntimeError("Exact DLL member missing: " + item["member"])
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
            f"Source SHA mismatch for {item['member']}: {actual_source}; refusing review against decompile drift"
        )
    il, il_stderr = run(["ilspycmd", "-il", str(dll_path)])

    cs_name = item["stem"] + ".cs"
    il_name = item["stem"] + ".il"
    (OUT / cs_name).write_bytes(source)
    (OUT / il_name).write_bytes(il)
    verification["assemblies"].append({
        "package": item["package"],
        "version": item["version"],
        "package_zip_sha256": actual_zip,
        "member": item["member"],
        "dll_sha256": actual_dll,
        "source_sha256": actual_source,
        "source_bytes": len(source),
        "source_lines": len(source.decode("utf-8", errors="replace").splitlines()),
        "il_sha256": sha256(il),
        "il_bytes": len(il),
        "il_lines": len(il.decode("utf-8", errors="replace").splitlines()),
        "source_occurrences": {
            "EnemyAI": source.count(b"EnemyAI"),
            "EnemyType": source.count(b"EnemyType"),
            "Instantiate": source.count(b"Instantiate"),
            "NetworkObject": source.count(b"NetworkObject"),
            "SpawnEnemyOnServer": source.count(b"SpawnEnemyOnServer"),
            "SpawnEnemyGameObject": source.count(b"SpawnEnemyGameObject"),
            "EnemyVent": source.count(b"EnemyVent"),
            "HarmonyPatch": source.count(b"HarmonyPatch"),
        },
        "source_stderr": source_stderr.decode("utf-8", errors="replace")[-4000:],
        "il_stderr": il_stderr.decode("utf-8", errors="replace")[-4000:],
        "outputs": [cs_name, il_name],
    })
    dll_path.unlink(missing_ok=True)

(OUT / "VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
print(json.dumps(verification, indent=2))
