#!/usr/bin/env python3
"""Exact DIAG1 -> DIAG1PATH1 identity-only ephemeral review-build gate. Never publishes or arms runtime."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE"
STATIC_PATH = EVIDENCE_DIR / "STATIC_VERIFICATION.json"

BASELINE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
BMDS_PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
DIAG1_PROFILE_SHA = "31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e"
DIAG_DLL_SHA = "3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1"
BMDS_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
DIAG_DLL = "BepInEx/plugins/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.dll"
BMDS_DLL = "BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"
NORMALIZER_DLL = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
BASE_PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector.r2z"
OUTPUT_PROFILE = "Profiles/LC V1 S1.42AK-D1P1.r2z"
OLD_PROFILE_NAME = "LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector"
NEW_PROFILE_NAME = "LC V1 S1.42AK-D1P1"


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


def normalized_export(data: bytes) -> str:
    text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    require(len(re.findall(r"(?m)^profileName:.*$", text)) == 1, "Expected exactly one profileName field")
    return re.sub(r"(?m)^profileName:.*$", "profileName: <identity>", text).rstrip("\n")


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip()

require(spec["enabled"] is True, "Separate DIAG1PATH1 review recipe must remain enabled")
require(spec["build_id"] == "S1.42AK-BMDSFIX1-DIAG1PATH1", "Build ID drift")
require(spec["base_profile"] == BASE_PROFILE, "Exact DIAG1 base profile drift")
require(spec["base_sha256"] == DIAG1_PROFILE_SHA, "Exact DIAG1 base SHA guard drift")
require(spec["output_profile"] == OUTPUT_PROFILE, "Review output path drift")
require(spec["profile_name"] == NEW_PROFILE_NAME, "Short profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections", "local_plugin_builds"):
    require(spec[field] == [], "Unauthorized " + field)
require(spec["text_assertions"] == [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}], "Text assertion drift")
require(spec["result_json"] == "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/BUILD_RESULT.json", "Result JSON path drift")
require(spec["result_md"] == "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/BUILD_RESULT.md", "Result markdown path drift")

# Review-build stage is deliberately lifecycle-neutral: the blocked long-name DIAG1 remains the runtime pointer until a later publication/activation checkpoint replaces it.
require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Current controller ID drift")
require(current_spec["base_profile"] == "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z", "Current controller base profile drift")
require(current_spec["base_sha256"] == BMDS_PROFILE_SHA, "Current controller base SHA drift")
require(current_spec["local_plugin_builds"] == [], "Current controller must not build DIAG1PATH1")
require(active_build == "S1.42AK-BMDSFIX1-DIAG1", "Runtime ACTIVE_BUILD must remain blocked DIAG1 until later lifecycle replacement")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline ID drift")
require(current_state["accepted_baseline"]["sha256"] == BASELINE_SHA, "Accepted baseline SHA drift")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active gameplay candidate ID drift")
require(current_state["active_candidate"]["sha256"] == BMDS_PROFILE_SHA, "Active gameplay candidate SHA drift")
require(current_state["runtime_test_outstanding"] is True, "Regular BMDSFIX1 target gate must remain outstanding")
require(current_state["controllers"]["runtime_active_build"] == "S1.42AK-BMDSFIX1-DIAG1", "Runtime controller drift")
diag = current_state["selected_scope"].get("diagnostic_revision")
require(isinstance(diag, dict), "Active diagnostic revision missing")
require(diag.get("build_id") == "S1.42AK-BMDSFIX1-DIAG1", "Active diagnostic revision ID drift")
require(diag.get("sha256") == DIAG1_PROFILE_SHA, "Active diagnostic revision SHA drift")

# The generated review profile may exist only inside CI; this gate refuses an already-published successor.
tracked = subprocess.run(
    ["git", "ls-files", "--error-unmatch", "--", OUTPUT_PROFILE],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
require(tracked.returncode != 0, "DIAG1PATH1 output is already tracked/published; inactive review-build gate refuses")

base = ROOT / BASE_PROFILE
output = ROOT / OUTPUT_PROFILE
require(base.is_file(), "Exact published DIAG1 base profile missing")
require(sha256(base.read_bytes()) == DIAG1_PROFILE_SHA, "Exact published DIAG1 base profile SHA mismatch")
require(output.is_file(), "DIAG1PATH1 review output profile missing")

original = members(base)
built = members(output)
require(len(original) == 338, f"Unexpected DIAG1 base member count: {len(original)}")
require(set(built) == set(original), "Identity-only successor changed archive member set")
changed = [name for name in original if original[name] != built[name]]
require(changed == ["export.r2x"], "Unexpected changed members: " + repr(changed))
require(normalized_export(original["export.r2x"]) == normalized_export(built["export.r2x"]),
        "export.r2x drift beyond profileName identity metadata")
old_export = original["export.r2x"].decode("utf-8-sig")
new_export = built["export.r2x"].decode("utf-8-sig")
require(f"profileName: {OLD_PROFILE_NAME}" in old_export, "Published DIAG1 profileName mismatch")
require(f"profileName: {NEW_PROFILE_NAME}" in new_export, "DIAG1PATH1 profileName mismatch")
require("LethalLevelLoaderUpdated" not in new_export, "Forbidden LLL fork in review export")

for path, expected in ((DIAG_DLL, DIAG_DLL_SHA), (BMDS_DLL, BMDS_DLL_SHA), (NORMALIZER_DLL, NORMALIZER_SHA)):
    require(path in original and path in built, f"Required DLL missing: {path}")
    require(sha256(original[path]) == expected, f"Published DIAG1 inherited DLL SHA drift: {path}")
    require(sha256(built[path]) == expected, f"DIAG1PATH1 inherited DLL SHA drift: {path}")
    require(original[path] == built[path], f"Identity-only successor changed DLL bytes: {path}")

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMDSFIX1-DIAG1PATH1", "Builder result build ID mismatch")
require(result["base_sha256"] == DIAG1_PROFILE_SHA, "Builder result base SHA mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["added_members"] == [], "Identity-only successor unexpectedly added members")
require(result["changed_existing_members"] == ["export.r2x"], "Builder result changed-member mismatch")
require(result["mod_state_changes"] == [], "Builder result mod-state drift")
require(result["mod_additions"] == [], "Builder result mod-addition drift")
require(result["mod_removals"] == [], "Builder result mod-removal drift")

profile_source_export = ROOT / "ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/export.r2x"
profile_source_index = ROOT / "ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/FILE_INDEX.json"
require(profile_source_export.is_file(), "Readable DIAG1PATH1 ProfileSources export missing")
require(profile_source_index.is_file(), "Readable DIAG1PATH1 ProfileSources FILE_INDEX missing")
require(profile_source_export.read_bytes() == built["export.r2x"], "ProfileSources export differs from review archive")
index = json.loads(profile_source_index.read_text(encoding="utf-8"))
require(len(index) == len(built), "FILE_INDEX row count differs from review archive member count")
index_paths = [row.get("path") for row in index]
require(len(index_paths) == len(set(index_paths)), "Duplicate paths in DIAG1PATH1 FILE_INDEX")
require(set(index_paths) == set(built), "DIAG1PATH1 FILE_INDEX member set differs from review archive")
for row in index:
    path = row["path"]
    data = built[path]
    require(row.get("size") == len(data), f"FILE_INDEX size mismatch for {path}")
    require(row.get("sha256") == sha256(data), f"FILE_INDEX SHA mismatch for {path}")

report = {
    "status": "STATIC_BUILD_PASS_IDENTITY_ONLY_REVIEW_ARTIFACT_NOT_ARMED",
    "build_id": "S1.42AK-BMDSFIX1-DIAG1PATH1",
    "diagnostic_only": True,
    "never_accept": True,
    "base_build_id": "S1.42AK-BMDSFIX1-DIAG1",
    "base_profile_sha256": DIAG1_PROFILE_SHA,
    "output_sha256": sha256(output.read_bytes()),
    "diagnostic_dll_sha256": sha256(built[DIAG_DLL]),
    "bmdsfix1_dll_sha256": sha256(built[BMDS_DLL]),
    "normalizer_sha256": sha256(built[NORMALIZER_DLL]),
    "archive_members_verified": len(index),
    "added_members": [],
    "changed_existing_members": changed,
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "local_plugin_builds": 0,
    "old_profile_name": OLD_PROFILE_NAME,
    "new_profile_name": NEW_PROFILE_NAME,
    "current_build_controller_enabled": current_spec["enabled"],
    "runtime_active_build": active_build,
    "runtime_armed_for_diag1path1": False,
    "qualification": "Ephemeral CI review build only. Exact published DIAG1 bytes are preserved member-for-member except export.r2x profileName metadata. No DLL rebuild, package/config change, publication, Gale activation, runtime execution, BMDSFIX1 acceptance or qualification occurs."
}
STATIC_PATH.parent.mkdir(parents=True, exist_ok=True)
STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
