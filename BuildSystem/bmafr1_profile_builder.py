#!/usr/bin/env python3
"""BMAFR1 bounded raw-LLL config-binding review builder.

This wrapper keeps the generic profile builder unchanged. It fail-closes on
visible-equivalent/raw-different LLL section identities, materializes the exact
nine-U+200B Foundry section through the existing builder, and supplies the
already-reviewed BMAFDIAG1 DLL from a hash-guarded published donor profile.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERIC_BUILDER = ROOT / "BuildSystem/profile_builder.py"
UTF8 = "utf-8"
LLL_CONFIG = "BepInEx/config/LethalLevelLoader.cfg"
FOUNDRY_VISIBLE_SECTION = "Custom Dungeon:  Abandoned Foundry"
FOUNDRY_RAW_SECTION = "\u200b" * 9 + FOUNDRY_VISIBLE_SECTION


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def visible(text: str) -> str:
    """Visible-equivalence helper only; never establishes raw config identity."""
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


def is_ini_header(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def visible_equivalent_headers(text: str, raw_section: str) -> list[str]:
    target = visible(f"[{raw_section}]").casefold()
    return [
        line.strip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if is_ini_header(line) and visible(line.strip()).casefold() == target
    ]


def validate_raw_section_state(text: str, raw_section: str, expected_exact_count: int) -> None:
    headers = visible_equivalent_headers(text, raw_section)
    exact = [line for line in headers if line.casefold() == f"[{raw_section}]".casefold()]
    if len(headers) != expected_exact_count or len(exact) != expected_exact_count:
        raise RuntimeError(
            "Raw INI section identity state mismatch: "
            f"visible_equivalent={len(headers)}, raw_exact={len(exact)}, "
            f"expected_raw_exact={expected_exact_count}, headers={headers!r}"
        )


def zip_member(profile: Path, member: str) -> bytes:
    with zipfile.ZipFile(profile, "r") as archive:
        names = archive.namelist()
        if names.count(member) != 1:
            raise RuntimeError(
                f"Archive member count for {member} in {profile} is "
                f"{names.count(member)}, expected 1"
            )
        return archive.read(member)


def validate_spec(spec: dict) -> None:
    if spec.get("build_id") != "S1.42AK-BMAFR1":
        raise RuntimeError("This bounded builder only accepts S1.42AK-BMAFR1")
    if spec.get("base_profile") != "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z":
        raise RuntimeError("BMAFR1 must derive directly from exact accepted S1.42AK")
    if spec.get("base_sha256") != "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee":
        raise RuntimeError("BMAFR1 accepted-baseline SHA guard drift")
    if spec.get("output_profile") != "Profiles/LC V1 S1.42AK-BMAFR1.r2z":
        raise RuntimeError("BMAFR1 output profile drift")
    if spec.get("profile_name") != "LC V1 S1.42AK-BMAFR1":
        raise RuntimeError("BMAFR1 short profile identity drift")
    if spec.get("file_injections") != [] or spec.get("local_plugin_builds") != []:
        raise RuntimeError("BMAFR1 direct file/local-plugin injection is not authorized")

    patches = spec.get("config_patches", [])
    if len(patches) != 9:
        raise RuntimeError(f"BMAFR1 expected 9 Foundry config patches, got {len(patches)}")
    for patch in patches:
        if patch.get("path") != LLL_CONFIG:
            raise RuntimeError("BMAFR1 may patch only LethalLevelLoader.cfg")
        if patch.get("section") != FOUNDRY_RAW_SECTION:
            raise RuntimeError("BMAFR1 Foundry raw section is not exact nine-U+200B identity")
        if patch.get("forbid_visible_equivalent_duplicates") is not True:
            raise RuntimeError("BMAFR1 visible-equivalent duplicate guard is not enabled")

    donors = spec.get("archive_member_injections", [])
    if len(donors) != 1:
        raise RuntimeError("BMAFR1 requires exactly one hash-guarded archive-member donor")


def prepare_donor_file(item: dict, temp_root: Path) -> Path:
    source_profile = ROOT / item["source_profile"]
    if not source_profile.is_file():
        raise RuntimeError(f"Archive-member donor profile missing: {source_profile}")
    actual_profile_sha = sha_file(source_profile)
    expected_profile_sha = str(item["source_profile_sha256"]).lower()
    if actual_profile_sha != expected_profile_sha:
        raise RuntimeError(
            f"Archive-member donor profile SHA mismatch: expected {expected_profile_sha}, "
            f"got {actual_profile_sha}"
        )

    member = item["source_member"]
    payload = zip_member(source_profile, member)
    actual_member_sha = sha_bytes(payload)
    expected_member_sha = str(item["source_member_sha256"]).lower()
    if actual_member_sha != expected_member_sha:
        raise RuntimeError(
            f"Archive-member donor SHA mismatch for {member}: expected {expected_member_sha}, "
            f"got {actual_member_sha}"
        )

    donor_file = temp_root / "S142AKBMAFDiag1.dll"
    donor_file.write_bytes(payload)
    return donor_file


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()

    spec_path = args.spec if args.spec.is_absolute() else ROOT / args.spec
    spec = json.loads(spec_path.read_text(encoding=UTF8))
    validate_spec(spec)

    base_profile = ROOT / spec["base_profile"]
    if sha_file(base_profile) != str(spec["base_sha256"]).lower():
        raise RuntimeError("Exact accepted S1.42AK base SHA mismatch")

    base_lll = zip_member(base_profile, LLL_CONFIG).decode("utf-8-sig")
    validate_raw_section_state(base_lll, FOUNDRY_RAW_SECTION, expected_exact_count=0)

    with tempfile.TemporaryDirectory(prefix="bmafr1-review-") as temp_name:
        temp_root = Path(temp_name)
        donor = prepare_donor_file(spec["archive_member_injections"][0], temp_root)

        transient = copy.deepcopy(spec)
        transient.pop("archive_member_injections", None)
        for patch in transient["config_patches"]:
            patch.pop("forbid_visible_equivalent_duplicates", None)
        transient["file_injections"] = [{
            "source": str(donor),
            "archive_path": spec["archive_member_injections"][0]["archive_path"],
        }]

        transient_path = temp_root / "BMAFR1_TRANSIENT_BUILD_SPEC.json"
        transient_path.write_text(json.dumps(transient, indent=2, ensure_ascii=False) + "\n", encoding=UTF8)

        subprocess.run(
            [sys.executable, str(GENERIC_BUILDER), str(transient_path)],
            cwd=ROOT,
            check=True,
        )

    output = ROOT / spec["output_profile"]
    review_lll = zip_member(output, LLL_CONFIG).decode("utf-8-sig")
    validate_raw_section_state(review_lll, FOUNDRY_RAW_SECTION, expected_exact_count=1)

    print(
        "PASS: BMAFR1 bounded builder materialized exactly one raw nine-U+200B "
        "Foundry section and reused the hash-guarded diagnostic DLL."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
