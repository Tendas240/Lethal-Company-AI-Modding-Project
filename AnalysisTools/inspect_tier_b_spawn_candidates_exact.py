#!/usr/bin/env python3
"""Exact full-source capture for the next six strongest unreviewed S1.42AI spawn-owner candidates.

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
OUT = ROOT / "tier-b-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-tier-b-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = "a7a6958d9e82ee657aea65a72011eb7e0d44b86b"
DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_tier_b_spawn_candidates_exact.py",
    ".github/workflows/tier-b-spawn-candidates-exact-review.yml",
}

EXPECTED = (
    {
        "package": "Flowprojects-Mirage_v81",
        "version": "1.29.1",
        "zip_sha256": "19d6c1f31647c32a3011e858524a9c3f93b23b160a0015f19a80daad696ebcb9",
        "member": "Mirage.dll",
        "dll_sha256": "271a4a8a77c1c4317ae146e524bcd91089917a2a0d3720feb92dc42dca5b1e80",
        "source_sha256": "bf6bc0674b1639bf802d9627439fc8ab966eec51cb458f41b4079be62e1d22c5",
        "stem": "Mirage_v81-1.29.1",
    },
    {
        "package": "Alice-DungeonGenerationPlus",
        "version": "1.5.0",
        "zip_sha256": "c5b5d79d5054f4388a9e50cd73770e97fa2e1cb62c7fad7fd5a1e69ee6195586",
        "member": "DunGenPlus.dll",
        "dll_sha256": "9d488d7bb98c87bbdb3967d7f9c6c5cb8ab9b82284467fe1c2dddefed1bc1765",
        "source_sha256": "97b3f041a37ee36abec5e62505a7aba9d85f904bbf6b65db7d56556d16a36e0e",
        "stem": "DungeonGenerationPlus-1.5.0",
    },
    {
        "package": "KawaiiBone-Remnants",
        "version": "1.4.4",
        "zip_sha256": "4a41157f3530b802edbf8623c72b93b09e27f7cd7c8fbcac1970a690f634c635",
        "member": "Remnants.dll",
        "dll_sha256": "49d8e65a2bd6d451a552c12ec62d87d112b5cb7930859a8c72b8021e203f7ad5",
        "source_sha256": "d67f0ee26c1a50d90697a313c04110cba78c16f218f143479f2d64493bdd2eff",
        "stem": "Remnants-1.4.4",
    },
    {
        "package": "LethalMatt-Bozoros",
        "version": "2.9.3",
        "zip_sha256": "e7f8851d0a0cf1c1106526b2c171af36287a9bbd161d13dec33634c1c33fda44",
        "member": "BepInEx/plugins/Bozoros.dll",
        "dll_sha256": "87feb32c19c5c9e5fbc42f6af5211baa169239994c6dafed4236545ee3a47265",
        "source_sha256": "387e597f0cf5f7fe64025d88f155f5a29ef180197df78ee108ce80a00d00844b",
        "stem": "Bozoros-2.9.3",
    },
    {
        "package": "AntlerShed-EnemySkinRegistry",
        "version": "1.5.1",
        "zip_sha256": "3386bfd5c57c00f43c7e84c5ab88f5a0dbfd960fe52cac21c243a2dd0ebcaaf1",
        "member": "plugins/EnemySkinRegistry/EnemySkinRegistry.dll",
        "dll_sha256": "6b53db95bfc15b7d71539126c79e32861d3255e4aa73d6f06de7a65ce8edb733",
        "source_sha256": "cf5e447e7f8f4c8b3eab4dde479c5330a5ec2c868d82c1350d1de172e58821ee",
        "stem": "EnemySkinRegistry-1.5.1",
    },
    {
        "package": "ButteryStancakes-EnemySoundFixes",
        "version": "1.9.14",
        "zip_sha256": "4d01f6c57e707fc2939c34bd9a052d260947c34d8e82c8f87591a4b9fd9b0cf1",
        "member": "EnemySoundFixes.dll",
        "dll_sha256": "b295c812646df1ff8b102d2c1f95d66040beb4176b38f93cebaeadc24a017b65",
        "source_sha256": "df5b03147d27e0970eec994e7059b763b6de0afbc327dbbb5f91a3e4ae2ed470",
        "stem": "EnemySoundFixes-1.9.14",
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
    req = urllib.request.Request(url, headers={"User-Agent": "s142ai-tier-b-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as response:
        data = response.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data


verify_analysis_branch_delta()
verification = {
    "schema_version": 1,
    "purpose": "S1.42AI-DIAG1 exact review capture for next six strongest remaining discovery-positive spawn-owner candidates",
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
