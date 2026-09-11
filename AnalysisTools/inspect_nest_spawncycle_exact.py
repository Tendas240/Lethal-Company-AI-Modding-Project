#!/usr/bin/env python3
"""Capture complete exact decompiles for S1.42AI-DIAG1 patch-safety review.

Fail closed against the already-merged NativeSpawnOwners package/DLL/source hashes.
This is read-only evidence generation: it does not build or modify a profile.
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
OUT = ROOT / "nest-spawncycle-exact-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-nest-spawncycle-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

EXPECTED = (
    {
        "package": "PureFPSZac-NestFix",
        "version": "1.3.0",
        "url": "https://gcdn.thunderstore.io/live/repository/packages/PureFPSZac-NestFix-1.3.0.zip",
        "zip_sha256": "a9cf704b463fab1cc988f6872ba4faa641ac9eb6dae52372fa13d61b80a28a4c",
        "member": "NestFix.dll",
        "dll_sha256": "0a4072618c2a089283933b8aeebe4962c4e45d465518760c90b4c18eb2b70f20",
        "source_sha256": "0e986b4d7d968c914b3d1c9376e5bfe739b3d6e56f94292a139f7d40246982b0",
        "stem": "NestFix-1.3.0",
    },
    {
        "package": "ButteryStancakes-SpawnCycleFixes",
        "version": "1.2.2",
        "url": "https://gcdn.thunderstore.io/live/repository/packages/ButteryStancakes-SpawnCycleFixes-1.2.2.zip",
        "zip_sha256": "ccc66892f996890c9a24dbe430d394262911ad576d2dd797d5535daf196e1c2f",
        "member": "SpawnCycleFixes.dll",
        "dll_sha256": "aa41f4bb8a8e2dedd75f7987d85c0e0a6792d92bd1fecbffa278f5f4dc9c52a0",
        "source_sha256": "c7a7e300be873f5d4271fb673332143a1eb9c5e0dd1521dc2787aa07ed939651",
        "stem": "SpawnCycleFixes-1.2.2",
    },
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(args: list[str]) -> tuple[bytes, bytes]:
    result = subprocess.run(args, capture_output=True, timeout=240)
    if result.returncode != 0:
        raise RuntimeError(
            f"{args[0]} failed ({result.returncode}): "
            + result.stderr.decode("utf-8", errors="replace")[-4000:]
        )
    return result.stdout, result.stderr


def download(url: str, path: Path) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read(256 * 1024 * 1024 + 1)
    if len(data) > 256 * 1024 * 1024:
        raise RuntimeError("Bounded package download exceeded 256 MiB")
    path.write_bytes(data)
    return data


verification = {
    "schema_version": 1,
    "purpose": "S1.42AI-DIAG1 exact NestFix/SpawnCycleFixes patch-body review",
    "repository_commit": os.environ.get("GITHUB_SHA"),
    "decompiler": {"tool": "ilspycmd", "version": "11.0.0.9375"},
    "packages": [],
    "qualification": (
        "Complete decompile/IL capture of two exact SHA-anchored assemblies for patch-safety review. "
        "This evidence does not itself authorize a diagnostic build or gameplay test."
    ),
}

for item in EXPECTED:
    zip_path = WORK / (item["stem"] + ".zip")
    package_bytes = download(item["url"], zip_path)
    actual_zip = sha256(package_bytes)
    if actual_zip != item["zip_sha256"]:
        raise RuntimeError(f"Package ZIP SHA mismatch for {item['package']}: {actual_zip}")

    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        if item["member"] not in names:
            raise RuntimeError(f"Exact DLL member missing for {item['package']}: {item['member']}")
        dll_bytes = archive.read(item["member"])

    actual_dll = sha256(dll_bytes)
    if actual_dll != item["dll_sha256"]:
        raise RuntimeError(f"DLL SHA mismatch for {item['package']}: {actual_dll}")

    dll_path = WORK / (item["stem"] + ".dll")
    dll_path.write_bytes(dll_bytes)

    source, source_stderr = run(["ilspycmd", str(dll_path)])
    actual_source = sha256(source)
    if actual_source != item["source_sha256"]:
        raise RuntimeError(
            f"Decompiler source SHA mismatch for {item['package']}: {actual_source}; "
            "refusing review against bytes different from merged discovery evidence"
        )

    il, il_stderr = run(["ilspycmd", "-il", str(dll_path)])
    cs_name = item["stem"] + ".cs"
    il_name = item["stem"] + ".il"
    (OUT / cs_name).write_bytes(source)
    (OUT / il_name).write_bytes(il)

    verification["packages"].append(
        {
            "package": item["package"],
            "version": item["version"],
            "url": item["url"],
            "zip_sha256": actual_zip,
            "member": item["member"],
            "dll_sha256": actual_dll,
            "decompiled_source_sha256": actual_source,
            "expected_discovery_source_sha256": item["source_sha256"],
            "source_bytes": len(source),
            "source_lines": len(source.decode("utf-8").splitlines()),
            "il_sha256": sha256(il),
            "il_bytes": len(il),
            "il_lines": len(il.decode("utf-8").splitlines()),
            "source_stderr": source_stderr.decode("utf-8", errors="replace"),
            "il_stderr": il_stderr.decode("utf-8", errors="replace"),
            "outputs": [cs_name, il_name],
        }
    )

(OUT / "VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
print(json.dumps(verification, indent=2))
