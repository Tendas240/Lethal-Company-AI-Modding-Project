#!/usr/bin/env python3
"""C3F17.4 read-only S1.42AK / LethalLevelLoader 1.7.12 provenance gate."""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z"
PROFILE_SOURCE_EXPORT = ROOT / "ProfileSources/S1.42AK/export.r2x"
OUT = ROOT / "c3f17-4-s142ak-lll-provenance-output"

EXPECTED_PROFILE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PACKAGE_URL = "https://gcdn.thunderstore.io/live/repository/packages/IAmBatby-LethalLevelLoader-1.7.12.zip"
EXPECTED_PACKAGE_SHA256 = "e01eadec8b1df3a1bc331e98b29d94baffa572cb7379953f1fa4e46df0aa6451"
EXPECTED_DLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
MAX_PACKAGE_BYTES = 64 * 1024 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def exact_lll_block(export_text: str) -> str:
    blocks = re.findall(r"(?ms)^- name: IAmBatby-LethalLevelLoader\s*$.*?(?=^- name: |\Z)", export_text)
    require(len(blocks) == 1, f"Expected exactly one IAmBatby-LethalLevelLoader block, found {len(blocks)}")
    block = blocks[0]
    require(re.search(r"(?m)^\s+major: 1\s*$", block) is not None, "LLL major version is not 1")
    require(re.search(r"(?m)^\s+minor: 7\s*$", block) is not None, "LLL minor version is not 7")
    require(re.search(r"(?m)^\s+patch: 12\s*$", block) is not None, "LLL patch version is not 12")
    require(re.search(r"(?m)^\s+enabled: true\s*$", block) is not None, "LLL is not enabled")
    require(re.search(r"(?m)^\s+source: Thunderstore\s*$", block) is not None, "LLL source is not Thunderstore")
    return block


def main() -> None:
    OUT.mkdir(exist_ok=True)

    profile_bytes = PROFILE.read_bytes()
    profile_hash = sha256(profile_bytes)
    require(profile_hash == EXPECTED_PROFILE_SHA256,
            f"S1.42AK profile SHA-256 mismatch: {profile_hash}")

    with zipfile.ZipFile(io.BytesIO(profile_bytes)) as profile_zip:
        names = profile_zip.namelist()
        require(names.count("export.r2x") == 1, f"Expected exactly one export.r2x in S1.42AK profile, got {names.count('export.r2x')}")
        archived_export_bytes = profile_zip.read("export.r2x")

    source_export_bytes = PROFILE_SOURCE_EXPORT.read_bytes()
    require(archived_export_bytes == source_export_bytes,
            "ProfileSources/S1.42AK/export.r2x is not byte-identical to the export embedded in the exact S1.42AK archive")

    export_text = archived_export_bytes.decode("utf-8-sig")
    exact_lll_block(export_text)
    require("LethalLevelLoaderUpdated" not in export_text,
            "Deprecated/alternate LethalLevelLoaderUpdated owner is present in S1.42AK export")

    request = urllib.request.Request(PACKAGE_URL, headers={"User-Agent": "LC-AI-Modding-Project-C3F17.4/1"})
    with urllib.request.urlopen(request, timeout=180) as response:
        package_bytes = response.read(MAX_PACKAGE_BYTES + 1)
    require(len(package_bytes) <= MAX_PACKAGE_BYTES, "Pinned LLL package exceeded bounded download size")

    package_hash = sha256(package_bytes)
    require(package_hash == EXPECTED_PACKAGE_SHA256,
            f"LLL 1.7.12 package SHA-256 mismatch: {package_hash}")

    with zipfile.ZipFile(io.BytesIO(package_bytes)) as package_zip:
        manifest = json.loads(package_zip.read("manifest.json"))
        require(manifest.get("name") == "LethalLevelLoader", f"Unexpected package manifest name: {manifest.get('name')!r}")
        require(manifest.get("version_number") == "1.7.12",
                f"Unexpected package manifest version: {manifest.get('version_number')!r}")
        dll_members = [name for name in package_zip.namelist() if name.rsplit("/", 1)[-1] == "LethalLevelLoader.dll"]
        require(len(dll_members) == 1,
                f"Expected exactly one LethalLevelLoader.dll in pinned package, found {dll_members}")
        dll_member = dll_members[0]
        dll_bytes = package_zip.read(dll_member)

    dll_hash = sha256(dll_bytes)
    require(dll_hash == EXPECTED_DLL_SHA256,
            f"LethalLevelLoader.dll SHA-256 mismatch: {dll_hash}")

    record = {
        "gate": "C3F17.4_S142AK_LLL_1.7.12_PROVENANCE",
        "repository_commit": os.environ.get("GITHUB_SHA", "local"),
        "profile_path": PROFILE.relative_to(ROOT).as_posix(),
        "profile_sha256": profile_hash,
        "profile_source_export_path": PROFILE_SOURCE_EXPORT.relative_to(ROOT).as_posix(),
        "profile_source_export_sha256": sha256(source_export_bytes),
        "profile_export_byte_identical": True,
        "dependency_name": "IAmBatby-LethalLevelLoader",
        "dependency_version": "1.7.12",
        "dependency_enabled": True,
        "dependency_source": "Thunderstore",
        "alternate_lll_owner_present": False,
        "package_url": PACKAGE_URL,
        "package_sha256": package_hash,
        "package_sha256_expected": EXPECTED_PACKAGE_SHA256,
        "package_hash_match": True,
        "package_manifest_name": manifest["name"],
        "package_manifest_version": manifest["version_number"],
        "dll_member": dll_member,
        "dll_sha256": dll_hash,
        "dll_sha256_expected": EXPECTED_DLL_SHA256,
        "dll_hash_match": True,
        "result": "PASS",
        "qualification": "Fresh CI materialization of the exact package selected by exact S1.42AK dependency metadata; validates package and DLL byte identity only. It does not arm or authorize runtime testing."
    }
    (OUT / "LLL_PROVENANCE.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
