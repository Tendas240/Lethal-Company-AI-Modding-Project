#!/usr/bin/env python3
"""Exact BMDSFIX1 -> BMDSFIX1-DIAG1 ephemeral review-build gate. Never publishes or arms runtime."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE"
STATIC_PATH = EVIDENCE_DIR / "STATIC_VERIFICATION.json"

BASELINE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PARENT_PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
PARENT_BMDS_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
DIAG_DLL = "BepInEx/plugins/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.dll"
BMDS_DLL = "BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"
NORMALIZER_DLL = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
OUTPUT_PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector.r2z"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def members(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), f"Duplicate archive members in {path}")
        return {name: archive.read(name) for name in names}


def stable_export(data: bytes) -> str:
    text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    require(len(re.findall(r"(?m)^profileName:.*$", text)) == 1, "Expected exactly one profileName field")
    return re.sub(r"(?m)^profileName:.*$", "profileName: <identity>", text).rstrip("\n")


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip()

require(spec["enabled"] is True, "Separate DIAG1 review recipe must remain enabled")
require(spec["build_id"] == "S1.42AK-BMDSFIX1-DIAG1", "Build ID drift")
require(spec["base_profile"] == "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z", "Parent profile drift")
require(spec["base_sha256"] == PARENT_PROFILE_SHA, "Parent SHA guard drift")
require(spec["output_profile"] == OUTPUT_PROFILE, "Review output path drift")
require(spec["profile_name"] == "LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector", "Profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections"):
    require(spec[field] == [], "Unauthorized " + field)

expected_local_build = {
    "project": "Patches/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.csproj",
    "configuration": "Release",
    "built_file": "Patches/S142AKBMDSFix1Diag1/bin/Release/netstandard2.1/S142AKBMDSFix1Diag1.dll",
    "archive_path": DIAG_DLL,
}
require(spec["local_plugin_builds"] == [expected_local_build], "Local diagnostic build contract drift")
require(spec["text_assertions"] == [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}], "Text assertion drift")
require(spec["result_json"] == "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json", "Result JSON path drift")
require(spec["result_md"] == "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.md", "Result markdown path drift")

# Review-build stage must leave all live/build controllers on the exact BMDSFIX1 candidate.
require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Current controller ID drift")
require(current_spec["base_profile"] == spec["base_profile"], "Current controller parent profile drift")
require(current_spec["base_sha256"] == PARENT_PROFILE_SHA, "Current controller parent SHA drift")
require(current_spec["local_plugin_builds"] == [], "Current controller must not arm DIAG1")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD must remain the exact BMDSFIX1 candidate")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline ID drift")
require(current_state["accepted_baseline"]["sha256"] == BASELINE_SHA, "Accepted baseline SHA drift")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active candidate ID drift")
require(current_state["active_candidate"]["sha256"] == PARENT_PROFILE_SHA, "Active candidate SHA drift")
require(current_state["runtime_test_outstanding"] is True, "Regular BMDSFIX1 target runtime gate must remain outstanding")

# The generated review profile may exist in the CI workspace, but it must not be tracked/published by this gate.
tracked = subprocess.run(
    ["git", "ls-files", "--error-unmatch", "--", OUTPUT_PROFILE],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
require(tracked.returncode != 0, "DIAG1 review output is already tracked/published; review-build gate refuses")

base = ROOT / spec["base_profile"]
output = ROOT / spec["output_profile"]
require(base.is_file(), "Exact BMDSFIX1 parent profile missing")
require(sha256(base.read_bytes()) == PARENT_PROFILE_SHA, "Exact BMDSFIX1 parent profile SHA mismatch")
require(output.is_file(), "DIAG1 review output profile missing")

original = members(base)
built = members(output)
require(DIAG_DLL not in original, "DIAG1 DLL unexpectedly already present in exact BMDSFIX1 parent")
require(set(built) - set(original) == {DIAG_DLL}, "Added archive member mismatch")
require(set(original) - set(built) == set(), "Archive member removal detected")
changed = [name for name in original if original[name] != built[name]]
require(changed == ["export.r2x"], "Unexpected changed existing members: " + repr(changed))
require(stable_export(original["export.r2x"]) == stable_export(built["export.r2x"]),
        "Package/config/export drift beyond profile identity metadata")
require("LethalLevelLoaderUpdated" not in built["export.r2x"].decode("utf-8-sig"), "Forbidden LLL fork in review export")

# The review build inherits the exact active gameplay candidate bytes unchanged.
require(BMDS_DLL in original and BMDS_DLL in built, "BMDSFIX1 DLL missing from parent/review profile")
require(sha256(original[BMDS_DLL]) == PARENT_BMDS_DLL_SHA, "Parent BMDSFIX1 DLL SHA drift")
require(sha256(built[BMDS_DLL]) == PARENT_BMDS_DLL_SHA, "Review BMDSFIX1 DLL SHA drift")
require(original[BMDS_DLL] == built[BMDS_DLL], "BMDSFIX1 DLL bytes changed in diagnostic review build")
require(NORMALIZER_DLL in original and NORMALIZER_DLL in built, "Accepted normalizer DLL missing from parent/review profile")
require(sha256(original[NORMALIZER_DLL]) == NORMALIZER_SHA, "Parent normalizer SHA drift")
require(sha256(built[NORMALIZER_DLL]) == NORMALIZER_SHA, "Review normalizer SHA drift")
require(original[NORMALIZER_DLL] == built[NORMALIZER_DLL], "Accepted normalizer bytes changed in diagnostic review build")

compiled = ROOT / expected_local_build["built_file"]
require(compiled.is_file(), "Compiled DIAG1 DLL missing")
require(compiled.read_bytes() == built[DIAG_DLL], "Injected DIAG1 DLL differs from compiled DLL")
diag_hash = sha256(built[DIAG_DLL])

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMDSFIX1-DIAG1", "Builder result build ID mismatch")
require(result["base_sha256"] == PARENT_PROFILE_SHA, "Builder result parent SHA mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["added_members"] == [DIAG_DLL], "Builder result added-member mismatch")
require(result["changed_existing_members"] == ["export.r2x"], "Builder result changed-member mismatch")

profile_source_export = ROOT / "ProfileSources/S1.42AK-BMDSFIX1-DIAG1/export.r2x"
profile_source_index = ROOT / "ProfileSources/S1.42AK-BMDSFIX1-DIAG1/FILE_INDEX.json"
require(profile_source_export.is_file(), "Readable DIAG1 ProfileSources export missing")
require(profile_source_index.is_file(), "Readable DIAG1 ProfileSources FILE_INDEX missing")
require(profile_source_export.read_bytes() == built["export.r2x"], "ProfileSources export differs from review archive")
index = json.loads(profile_source_index.read_text(encoding="utf-8"))
require(len(index) == len(built), "FILE_INDEX row count differs from review archive member count")
index_paths = [row.get("path") for row in index]
require(len(index_paths) == len(set(index_paths)), "Duplicate paths in DIAG1 FILE_INDEX")
require(set(index_paths) == set(built), "DIAG1 FILE_INDEX member set differs from review archive")
for row in index:
    path = row["path"]
    data = built[path]
    require(row.get("size") == len(data), f"FILE_INDEX size mismatch for {path}")
    require(row.get("sha256") == sha256(data), f"FILE_INDEX SHA mismatch for {path}")

report = {
    "status": "STATIC_BUILD_PASS_REVIEW_ARTIFACT_NOT_ARMED",
    "build_id": "S1.42AK-BMDSFIX1-DIAG1",
    "diagnostic_only": True,
    "never_accept": True,
    "parent_build_id": "S1.42AK-BMDSFIX1",
    "parent_profile_sha256": PARENT_PROFILE_SHA,
    "output_sha256": sha256(output.read_bytes()),
    "diagnostic_dll_sha256": diag_hash,
    "bmdsfix1_dll_sha256": sha256(built[BMDS_DLL]),
    "normalizer_sha256": sha256(built[NORMALIZER_DLL]),
    "archive_members_verified": len(index),
    "added_members": [DIAG_DLL],
    "changed_existing_members": changed,
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "current_build_controller_enabled": current_spec["enabled"],
    "runtime_active_build": active_build,
    "runtime_armed": False,
    "runtime_authorized_for_diag1": False,
    "qualification": "Ephemeral CI review build only. Exact BMDSFIX1 parent bytes are preserved; only the DIAG1 DLL plus profileName metadata are added. No repository profile publication, Gale activation, runtime execution, acceptance or BMDSFIX1 qualification occurs."
}
STATIC_PATH.parent.mkdir(parents=True, exist_ok=True)
STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
