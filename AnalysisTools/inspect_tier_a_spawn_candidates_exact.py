#!/usr/bin/env python3
"""Exact full-source capture for the six strongest remaining S1.42AI spawn-owner candidates.

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
OUT = ROOT / "tier-a-spawn-candidates-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-tier-a-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = "2915f2f04505581bec5056b3801130cc649aa1cf"
DISCOVERY_RUN = 34705334804
DISCOVERY_HEAD = "45d22c3fa1abb3bbd95dd137cd3903eb053f87c7"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 768 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_tier_a_spawn_candidates_exact.py",
    ".github/workflows/tier-a-spawn-candidates-exact-review.yml",
}

EXPECTED = (
    {
        "package": "ButteryStancakes-ButteRyBalance",
        "version": "0.7.0",
        "zip_sha256": "bf5bc41311a05bae25350704bf522884645f55050f1966330a825ffe5b941fc2",
        "member": "ButteRyBalance.dll",
        "dll_sha256": "d13c7996645c9cf34e2806acbd511972229aaf8874991524a56077390a63cf0e",
        "source_sha256": "0d46e2dc3f2231d00644871685d4a6c5336f3d60ce34dceec69e36ca6aef03ad",
        "stem": "ButteRyBalance-0.7.0",
    },
    {
        "package": "malco-Lategame_Upgrades",
        "version": "3.14.1",
        "zip_sha256": "8ffa3a987e2626526406673825d5523a044e6e6cf68581edba844b24f2f2c79a",
        "member": "BepInEx/plugins/MoreShipUpgrades/MoreShipUpgrades.dll",
        "dll_sha256": "c3c6da8a2ad57930ec91db9df24223379a27bd0e0dcc60cf21fb1c9472f20465",
        "source_sha256": "c027768e0b850573fb6ef4b90d86bd89baa557f739a91371fd49d30e6d86961a",
        "stem": "Lategame_Upgrades-3.14.1",
    },
    {
        "package": "Sparble-FacelessStalker",
        "version": "1.2.1",
        "zip_sha256": "3440b8c02f342d291a4e1f341a7c3ace4e87ec8a77b264ba7e0352178648a518",
        "member": "FacelessStalker/SlendermanMod.dll",
        "dll_sha256": "0957f55e0aa69f83167d4f1e7e6b261c174d1412b1d06fcf4df0e708e83dbce8",
        "source_sha256": "7cf665b6252da443d950bebc7ef6fb64e8cebff8ec10a8c0834aa8cce02abdd6",
        "stem": "FacelessStalker-1.2.1",
    },
    {
        "package": "Snowlance-SnowyLib",
        "version": "1.13.1",
        "zip_sha256": "60c64b5df528d62491b7f584d8ec3d14c41c9c3cd46b8d9c3fb1f6e230dec95b",
        "member": "Snowlance.SnowyLib.dll",
        "dll_sha256": "cdbb80c8b0afa3e65acae83e25bd00fb704cefbeb2e14ccc561f1d959b0c3c95",
        "source_sha256": "0b9b13fdc95cfb827eb5de2cdbd3ba94b6405d315af29e5ba1b13210f1e68d36",
        "stem": "SnowyLib-1.13.1",
    },
    {
        "package": "IAmBatby-LethalLevelLoader",
        "version": "1.7.12",
        "zip_sha256": "e01eadec8b1df3a1bc331e98b29d94baffa572cb7379953f1fa4e46df0aa6451",
        "member": "LethalLevelLoader.dll",
        "dll_sha256": "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
        "source_sha256": "88baea660b8a5e1fd65201ccf742331fd1017322998736f8cc187aec71a507a3",
        "stem": "LethalLevelLoader-1.7.12",
    },
    {
        "package": "Bob123-Haunted_Harpist",
        "version": "1.3.24",
        "zip_sha256": "cdddec7566a1374cc3c0e7df70a7c7906f16122219a6fc2d7084d7fd4c7df933",
        "member": "BepInEx/plugins/HauntedHarpist/LethalCompanyHarpGhost.dll",
        "dll_sha256": "d8d35767d74e3226c6adf8728fc4269a2fac4e05e11da2842f22858fc23c2ac0",
        "source_sha256": "00e2aa67044d4b330bc7a0647847d645a994b7c71e01819d584ebc149d462030",
        "stem": "Haunted_Harpist-1.3.24",
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
    req = urllib.request.Request(url, headers={"User-Agent": "s142ai-tier-a-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as response:
        data = response.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 768 MiB: " + url)
    path.write_bytes(data)
    return data


verify_analysis_branch_delta()
verification = {
    "schema_version": 1,
    "purpose": "S1.42AI-DIAG1 exact review capture for six strongest remaining discovery-positive spawn-owner candidates",
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
