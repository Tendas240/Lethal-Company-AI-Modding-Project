#!/usr/bin/env python3
"""Exact BMAFDIAG1 -> BMAFDIAG1PATH1 identity-only ephemeral review-build gate. Never publishes or arms runtime."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RepositoryTools"))
import gale_profile_path_length_guard as path_guard

SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1PATH1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_BUILD_EVIDENCE"
STATIC_PATH = EVIDENCE_DIR / "STATIC_VERIFICATION.json"

BASE_PROFILE = "Profiles/LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic.r2z"
OUTPUT_PROFILE = "Profiles/LC V1 S1.42AK-BMAFD1P1.r2z"
OLD_PROFILE_NAME = "LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic"
NEW_PROFILE_NAME = "LC V1 S1.42AK-BMAFD1P1"
BASE_SHA = "b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2"
DIAG_DLL = "BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll"
DIAG_DLL_SHA = "c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1"
LLL_CONFIG = "BepInEx/config/LethalLevelLoader.cfg"
LLL_CONFIG_SHA = "c9f03e7839c70ce21fae37ff597085175de35a9c176b97aed40798401ce66c0e"
NORMALIZER_DLL = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
EXPECTED_MEMBERS = 337
EXPECTED_PATHS = (219, 221)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def members(path: Path) -> tuple[list[str], dict[str, bytes]]:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), f"Duplicate archive members in {path}")
        return names, {name: archive.read(name) for name in names}


def normalized_export(data: bytes) -> str:
    text = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    require(len(re.findall(r"(?m)^profileName:.*$", text)) == 1, "Expected exactly one profileName field")
    return re.sub(r"(?m)^profileName:.*$", "profileName: <identity>", text).rstrip("\n")


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip()

require(spec["enabled"] is True, "Separate BMAFDIAG1PATH1 review recipe must remain enabled")
require(spec["build_id"] == "S1.42AK-BMAFDIAG1PATH1", "Build ID drift")
require(spec["base_profile"] == BASE_PROFILE, "Exact BMAFDIAG1 base profile drift")
require(spec["base_sha256"] == BASE_SHA, "Exact BMAFDIAG1 base SHA guard drift")
require(spec["output_profile"] == OUTPUT_PROFILE, "Review output path drift")
require(spec["profile_name"] == NEW_PROFILE_NAME, "Short profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections", "local_plugin_builds"):
    require(spec[field] == [], "Unauthorized " + field)
require(spec["text_assertions"] == [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}], "Text assertion drift")
require(spec["result_json"] == "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_BUILD_EVIDENCE/BUILD_RESULT.json", "Result JSON path drift")
require(spec["result_md"] == "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_BUILD_EVIDENCE/BUILD_RESULT.md", "Result markdown path drift")

# Review-build stage must remain lifecycle-neutral.
require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Current controller ID drift")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD must remain S1.42AK-BMDSFIX1")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline ID drift")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active gameplay candidate drift")
require(current_state["runtime_test_outstanding"] is True, "Passive BMDSFIX1 target gate must remain outstanding")
require(current_state["controllers"]["runtime_active_build"] == "S1.42AK-BMDSFIX1", "Runtime controller drift")
successor = current_state["selected_scope"].get("diagnostic_successor_revision")
require(isinstance(successor, dict), "BMAFDIAG1PATH1 successor revision missing")
require(successor.get("build_id") == "S1.42AK-BMAFDIAG1PATH1", "Successor revision ID drift")
require(successor.get("base_sha256") == BASE_SHA, "Successor parent SHA drift")
require(successor.get("profile_name") == NEW_PROFILE_NAME, "Successor profile identity drift")
require(successor.get("runtime_armed") is False, "Inactive review successor must not be runtime armed")
require(successor.get("published") is False and successor.get("indexed") is False, "Review successor must remain unpublished/unindexed")

# The generated review profile may exist only inside CI; refuse an already-published successor.
tracked = subprocess.run(
    ["git", "ls-files", "--error-unmatch", "--", OUTPUT_PROFILE],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
require(tracked.returncode != 0, "BMAFDIAG1PATH1 output is already tracked/published; inactive review-build gate refuses")

base = ROOT / BASE_PROFILE
output = ROOT / OUTPUT_PROFILE
require(base.is_file(), "Exact published BMAFDIAG1 base profile missing")
require(sha256(base.read_bytes()) == BASE_SHA, "Exact published BMAFDIAG1 base profile SHA mismatch")
require(output.is_file(), "BMAFDIAG1PATH1 review output profile missing")

original_names, original = members(base)
built_names, built = members(output)
require(len(original_names) == EXPECTED_MEMBERS, f"Unexpected BMAFDIAG1 base member count: {len(original_names)}")
require(built_names == original_names, "Identity-only successor changed archive member order/set")
changed = [name for name in original_names if original[name] != built[name]]
require(changed == ["export.r2x"], "Unexpected changed members: " + repr(changed))
require(normalized_export(original["export.r2x"]) == normalized_export(built["export.r2x"]),
        "export.r2x drift beyond profileName identity metadata")

old_export = original["export.r2x"].decode("utf-8-sig")
new_export = built["export.r2x"].decode("utf-8-sig")
require(old_export.splitlines()[0] == f"profileName: {OLD_PROFILE_NAME}", "Published BMAFDIAG1 profileName mismatch")
require(new_export.splitlines()[0] == f"profileName: {NEW_PROFILE_NAME}", "BMAFDIAG1PATH1 profileName mismatch")
require("LethalLevelLoaderUpdated" not in new_export, "Forbidden LLL fork in review export")

for path, expected in (
    (DIAG_DLL, DIAG_DLL_SHA),
    (LLL_CONFIG, LLL_CONFIG_SHA),
    (NORMALIZER_DLL, NORMALIZER_SHA),
):
    require(path in original and path in built, f"Required protected member missing: {path}")
    require(sha256(original[path]) == expected, f"Published BMAFDIAG1 protected member SHA drift: {path}")
    require(sha256(built[path]) == expected, f"BMAFDIAG1PATH1 protected member SHA drift: {path}")
    require(original[path] == built[path], f"Identity-only successor changed protected bytes: {path}")

projected = tuple(row[2] for row in path_guard.projections(NEW_PROFILE_NAME))
require(projected == EXPECTED_PATHS, "Unexpected successor Gale path projection: " + repr(projected))
require(path_guard.violations(NEW_PROFILE_NAME) == [], "Successor violates permanent Gale path budget")

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMAFDIAG1PATH1", "Builder result build ID mismatch")
require(result["base_sha256"] == BASE_SHA, "Builder result base SHA mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["zip_members"] == EXPECTED_MEMBERS, "Builder result archive member count mismatch")
require(result["added_members"] == [], "Identity-only successor unexpectedly added members")
require(result["changed_existing_members"] == ["export.r2x"], "Builder result changed-member mismatch")
require(result["mod_state_changes"] == [], "Builder result mod-state drift")
require(result["mod_additions"] == [], "Builder result mod-addition drift")
require(result["mod_removals"] == [], "Builder result mod-removal drift")

profile_source_dir = ROOT / "ProfileSources/S1.42AK-BMAFDIAG1PATH1"
profile_source_export = profile_source_dir / "export.r2x"
profile_source_config = profile_source_dir / LLL_CONFIG
profile_source_index = profile_source_dir / "FILE_INDEX.json"
require(profile_source_export.is_file(), "Readable BMAFDIAG1PATH1 ProfileSources export missing")
require(profile_source_config.is_file(), "Readable BMAFDIAG1PATH1 LLL config missing")
require(profile_source_index.is_file(), "Readable BMAFDIAG1PATH1 FILE_INDEX missing")
require(profile_source_export.read_bytes() == built["export.r2x"], "ProfileSources export differs from review archive")
require(profile_source_config.read_bytes() == built[LLL_CONFIG], "ProfileSources LLL config differs from review archive")

index = json.loads(profile_source_index.read_text(encoding="utf-8"))
require(len(index) == EXPECTED_MEMBERS, "FILE_INDEX row count differs from review archive member count")
index_paths = [row.get("path") for row in index]
require(index_paths == built_names, "BMAFDIAG1PATH1 FILE_INDEX order/member set differs from review archive")
for row in index:
    path = row["path"]
    data = built[path]
    require(row.get("size") == len(data), f"FILE_INDEX size mismatch for {path}")
    require(row.get("sha256") == sha256(data), f"FILE_INDEX SHA mismatch for {path}")

report = {
    "status": "STATIC_BUILD_PASS_IDENTITY_ONLY_REVIEW_ARTIFACT_NOT_PUBLISHED_NOT_ARMED",
    "build_id": "S1.42AK-BMAFDIAG1PATH1",
    "diagnostic_only": True,
    "never_accept": True,
    "base_build_id": "S1.42AK-BMAFDIAG1",
    "base_profile_sha256": BASE_SHA,
    "output_sha256": sha256(output.read_bytes()),
    "diagnostic_dll_sha256": sha256(built[DIAG_DLL]),
    "foundry_lll_config_sha256": sha256(built[LLL_CONFIG]),
    "normalizer_sha256": sha256(built[NORMALIZER_DLL]),
    "archive_members_verified": EXPECTED_MEMBERS,
    "added_members": [],
    "changed_existing_members": changed,
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "local_plugin_builds": 0,
    "old_profile_name": OLD_PROFILE_NAME,
    "new_profile_name": NEW_PROFILE_NAME,
    "projected_runtime_path_lengths": list(projected),
    "path_length_budget": path_guard.SAFE_RUNTIME_PATH_CHARS,
    "current_build_controller_enabled": current_spec["enabled"],
    "runtime_active_build": active_build,
    "runtime_armed_for_bmafdiag1path1": False,
    "published": False,
    "indexed": False,
    "qualification": (
        "Ephemeral CI inactive review build only. Exact published BMAFDIAG1 bytes are preserved "
        "member-for-member except export.r2x profileName metadata. No DLL rebuild, package/config "
        "change, publication, indexing, Gale import, runtime activation, gameplay execution, "
        "BMDSFIX1 acceptance or Black Mesa x Abandoned Foundry qualification occurs."
    ),
}
STATIC_PATH.parent.mkdir(parents=True, exist_ok=True)
STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
