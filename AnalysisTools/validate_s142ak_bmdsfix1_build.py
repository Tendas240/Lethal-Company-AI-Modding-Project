#!/usr/bin/env python3
"""Exact S1.42AK -> BMDSFIX1 review/published archive gate. Never arms runtime."""
from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
PROVENANCE_PATH = ROOT / "c3f17-4-s142ak-lll-provenance-output/LLL_PROVENANCE.json"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE"
STATIC_PATH = EVIDENCE_DIR / "STATIC_VERIFICATION.json"
PUBLICATION_PATH = EVIDENCE_DIR / "PUBLICATION_VERIFICATION.md"
REVIEW_PATH = EVIDENCE_DIR / "REVIEW_BUILD_CHECKPOINT.md"
EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
EXPECTED_OUTPUT_SHA256 = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
EXPECTED_FIX_DLL_SHA256 = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
EXPECTED_LLL_DLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
EXPECTED_NORMALIZER_SHA256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
EXPECTED_REVIEW_RUN = "36014932493"
EXPECTED_REVIEW_ARTIFACT_ID = "10813908176"
EXPECTED_ARTIFACT_ZIP_SHA256 = "b22e14b07455f722202cfaaf915ee362786c1a05c090aff0939f5a61b9de5db1"
EXPECTED_PUBLICATION_RUN = 36017880276
EXPECTED_PUBLICATION_COMMIT = "80057f75a253961449a4e92e27a16cbd83997f8a"
FIX_DLL = "BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"
NORMALIZER_DLL = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"


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


gate_mode = os.environ.get("BMDSFIX1_GATE_MODE", "review-build")
require(gate_mode in {"review-build", "published"}, f"Unsupported gate mode: {gate_mode!r}")

spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))

require(spec["enabled"] is True, "Separate review build request must remain enabled as immutable build recipe")
require(spec["build_id"] == "S1.42AK-BMDSFIX1", "Build ID drift")
require(spec["base_profile"] == "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z", "Base profile drift")
require(spec["base_sha256"] == EXPECTED_BASE_SHA256, "Base SHA guard drift")
require(spec["output_profile"] == "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z", "Output path drift")
require(spec["profile_name"] == "LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix", "Profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections"):
    require(spec[field] == [], "Unauthorized " + field)

expected_local_build = {
    "project": "Patches/S142AKBMDSFix1/S142AKBMDSFix1.csproj",
    "configuration": "Release",
    "built_file": "Patches/S142AKBMDSFix1/bin/Release/netstandard2.1/S142AKBMDSFix1.dll",
    "archive_path": FIX_DLL,
}
require(spec["local_plugin_builds"] == [expected_local_build], "Local plugin build contract drift")
require(spec["text_assertions"] == [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}], "Text assertion drift")

require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "BuildSpecs/current.json must remain the idle controller")
require(ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip() == "S1.42AK", "Runtime ACTIVE_BUILD drift")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(current_state["active_candidate"] is None, "Lifecycle unexpectedly has an active candidate")
require(current_state["runtime_test_outstanding"] is False, "Lifecycle unexpectedly authorizes runtime testing")

if gate_mode == "published":
    review_state = current_state["selected_scope"].get("bmdsfix1_review")
    require(isinstance(review_state, dict), "Published mode requires canonical BMDSFIX1 review state")
    require(review_state.get("published") is True, "Canonical lifecycle does not mark BMDSFIX1 published")
    require(review_state.get("main_integrated") is False, "Publication integration must not already be complete in PR validation")
    require(review_state.get("runtime_armed") is False, "Published BMDSFIX1 unexpectedly runtime-armed")
    require(review_state.get("publication_workflow_run") == EXPECTED_PUBLICATION_RUN, "Publication workflow run drift")
    require(review_state.get("published_profile_commit") == EXPECTED_PUBLICATION_COMMIT, "Published profile commit drift")

provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
require(provenance["result"] == "PASS", "Fresh LLL provenance did not pass")
require(provenance["profile_sha256"] == EXPECTED_BASE_SHA256, "Provenance profile mismatch")
require(provenance["dependency_version"] == "1.7.12", "Provenance LLL version mismatch")
require(provenance["dll_sha256"] == EXPECTED_LLL_DLL_SHA256 and provenance["dll_hash_match"] is True,
        "Fresh LLL DLL identity mismatch")

base = ROOT / spec["base_profile"]
output = ROOT / spec["output_profile"]
require(sha256(base.read_bytes()) == EXPECTED_BASE_SHA256, "Exact S1.42AK base SHA mismatch")
require(output.is_file(), "BMDSFIX1 output profile missing")

original = members(base)
built = members(output)
require(FIX_DLL not in original, "BMDSFIX1 DLL unexpectedly already present in accepted base")
require(set(built) - set(original) == {FIX_DLL}, "Added archive member mismatch")
require(set(original) - set(built) == set(), "Archive member removal detected")
changed = [name for name in original if original[name] != built[name]]
require(len(changed) == 1 and changed[0] == "export.r2x", "Unexpected changed existing members: " + repr(changed))
require(stable_export(original["export.r2x"]) == stable_export(built["export.r2x"]),
        "Package/config/export drift beyond profile identity metadata")
require("LethalLevelLoaderUpdated" not in built["export.r2x"].decode("utf-8-sig"), "Forbidden LLL fork in output export")

require(NORMALIZER_DLL in original and NORMALIZER_DLL in built, "Accepted normalizer DLL missing")
require(sha256(original[NORMALIZER_DLL]) == EXPECTED_NORMALIZER_SHA256, "Base normalizer identity drift")
require(sha256(built[NORMALIZER_DLL]) == EXPECTED_NORMALIZER_SHA256, "Output normalizer identity drift")
require(original[NORMALIZER_DLL] == built[NORMALIZER_DLL], "Normalizer bytes changed")

fix_hash = sha256(built[FIX_DLL])
if gate_mode == "review-build":
    compiled = ROOT / expected_local_build["built_file"]
    require(compiled.is_file(), "Compiled BMDSFIX1 DLL missing")
    require(compiled.read_bytes() == built[FIX_DLL], "Injected BMDSFIX1 DLL differs from compiled DLL")
else:
    require(sha256(output.read_bytes()) == EXPECTED_OUTPUT_SHA256, "Published profile SHA drift")
    require(fix_hash == EXPECTED_FIX_DLL_SHA256, "Published BMDSFIX1 DLL SHA drift")
    require(PUBLICATION_PATH.is_file(), "Published mode requires publication verification evidence")
    publication = PUBLICATION_PATH.read_text(encoding="utf-8")
    for marker in (
        "EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH",
        f"**Review workflow run:** `{EXPECTED_REVIEW_RUN}`",
        f"**Actions artifact ID:** `{EXPECTED_REVIEW_ARTIFACT_ID}`",
        f"**Artifact ZIP SHA-256:** `{EXPECTED_ARTIFACT_ZIP_SHA256}`",
        f"published profile SHA-256: `{EXPECTED_OUTPUT_SHA256}`",
        f"published `S142AKBMDSFix1.dll` SHA-256: `{EXPECTED_FIX_DLL_SHA256}`",
        "zero package changes, zero config changes",
    ):
        require(marker in publication, "Publication evidence drift or missing marker: " + marker)

    require(STATIC_PATH.is_file(), "Published mode requires committed static verification evidence")
    committed_static = json.loads(STATIC_PATH.read_text(encoding="utf-8"))
    require(committed_static["status"] == "STATIC_BUILD_PASS_REVIEW_ARTIFACT_NOT_ARMED", "Committed static status drift")
    require(committed_static["output_sha256"] == EXPECTED_OUTPUT_SHA256, "Committed static profile SHA drift")
    require(committed_static["bmdsfix1_dll_sha256"] == EXPECTED_FIX_DLL_SHA256, "Committed static BMDSFIX1 DLL SHA drift")
    require(committed_static["lll_dll_sha256"] == EXPECTED_LLL_DLL_SHA256, "Committed static LLL SHA drift")
    require(committed_static["normalizer_sha256"] == EXPECTED_NORMALIZER_SHA256, "Committed static normalizer SHA drift")
    require(committed_static["runtime_armed"] is False, "Committed static evidence unexpectedly runtime-armed")

    require(REVIEW_PATH.is_file(), "Published mode requires persisted review checkpoint")
    review = REVIEW_PATH.read_text(encoding="utf-8")
    for marker in (
        f"**Review workflow run:** `{EXPECTED_REVIEW_RUN}`",
        f"**Actions artifact ID:** `{EXPECTED_REVIEW_ARTIFACT_ID}`",
        f"**Artifact ZIP SHA-256:** `{EXPECTED_ARTIFACT_ZIP_SHA256}`",
        f"review profile SHA-256: `{EXPECTED_OUTPUT_SHA256}`",
        f"compiled/injected `S142AKBMDSFix1.dll` SHA-256: `{EXPECTED_FIX_DLL_SHA256}`",
    ):
        require(marker in review, "Review checkpoint drift or missing marker: " + marker)

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMDSFIX1", "Builder result build ID mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["added_members"] == [FIX_DLL], "Builder result added-member mismatch")
require(result["changed_existing_members"] == ["export.r2x"], "Builder result changed-member mismatch")

profile_source_export = ROOT / "ProfileSources/S1.42AK-BMDSFIX1/export.r2x"
profile_source_index = ROOT / "ProfileSources/S1.42AK-BMDSFIX1/FILE_INDEX.json"
require(profile_source_export.is_file(), "Readable ProfileSources export missing")
require(profile_source_index.is_file(), "Readable ProfileSources FILE_INDEX missing")
require(profile_source_export.read_bytes() == built["export.r2x"], "ProfileSources export differs from archive")
index = json.loads(profile_source_index.read_text(encoding="utf-8"))
require(len(index) == len(built), "FILE_INDEX row count differs from archive member count")
index_paths = [row.get("path") for row in index]
require(len(index_paths) == len(set(index_paths)), "Duplicate paths in FILE_INDEX")
require(set(index_paths) == set(built), "FILE_INDEX member set differs from archive")
for row in index:
    path = row["path"]
    data = built[path]
    require(row.get("size") == len(data), f"FILE_INDEX size mismatch for {path}")
    require(row.get("sha256") == sha256(data), f"FILE_INDEX SHA mismatch for {path}")

report = {
    "status": "STATIC_BUILD_PASS_REVIEW_ARTIFACT_NOT_ARMED" if gate_mode == "review-build" else "PUBLISHED_STATIC_PASS_NOT_RUNTIME_ARMED",
    "gate_mode": gate_mode,
    "build_id": "S1.42AK-BMDSFIX1",
    "base_sha256": sha256(base.read_bytes()),
    "output_sha256": sha256(output.read_bytes()),
    "bmdsfix1_dll_sha256": fix_hash,
    "lll_dll_sha256": provenance["dll_sha256"],
    "normalizer_sha256": sha256(built[NORMALIZER_DLL]),
    "archive_members_verified": len(index),
    "added_members": [FIX_DLL],
    "changed_existing_members": changed,
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "runtime_armed": False,
    "qualification": (
        "Ephemeral CI review build and exact archive-delta validation only. BuildSpecs/current.json and RuntimeInbox/ACTIVE_BUILD.txt remain unchanged; no runtime test is authorized."
        if gate_mode == "review-build"
        else "Post-publication exact-byte validation of the pinned reviewed profile, all FILE_INDEX rows, publication/review evidence, archive delta and inactive lifecycle. No rebuild, replacement artifact or runtime authorization is performed."
    ),
}
if gate_mode == "review-build":
    STATIC_PATH.parent.mkdir(exist_ok=True)
    STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
