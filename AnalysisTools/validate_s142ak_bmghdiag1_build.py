#!/usr/bin/env python3
"""C3F17.4 exact S1.42AK -> BMGHDIAG1 archive/build gate. Never arms runtime."""
from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
PROVENANCE_PATH = ROOT / "c3f17-4-s142ak-lll-provenance-output/LLL_PROVENANCE.json"
PUBLICATION_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
STATIC_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
EXPECTED_OUTPUT_SHA256 = "7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90"
EXPECTED_DIAGNOSTIC_DLL_SHA256 = "4a1f304a716bf7cacb6496f5047bb0e498ed68bde00fc9f4128fa001adaa30b2"
EXPECTED_LLL_DLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
EXPECTED_NORMALIZER_SHA256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
EXPECTED_REVIEW_RUN = "35849491391"
EXPECTED_REVIEW_ARTIFACT_ID = "10745290545"
DIAGNOSTIC_DLL = "BepInEx/plugins/S142AKBMGHDiag1/S142AKBMGHDiag1.dll"
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


gate_mode = os.environ.get("BMGHDIAG1_GATE_MODE", "review-build")
require(gate_mode in {"review-build", "published"}, f"Unsupported gate mode: {gate_mode!r}")

spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))

require(spec["enabled"] is True, "Separate review build request must be enabled when invoked explicitly")
require(spec["build_id"] == "S1.42AK-BMGHDIAG1", "Build ID drift")
require(spec["base_profile"] == "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z", "Base profile drift")
require(spec["base_sha256"] == EXPECTED_BASE_SHA256, "Base SHA guard drift")
require(spec["output_profile"] == "Profiles/LC V1 S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic.r2z", "Output path drift")
require(spec["profile_name"] == "LC V1 S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic", "Profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections"):
    require(spec[field] == [], "Unauthorized " + field)

expected_local_build = {
    "project": "Patches/S142AKBMGHDiag1/S142AKBMGHDiag1.csproj",
    "configuration": "Release",
    "built_file": "Patches/S142AKBMGHDiag1/bin/Release/netstandard2.1/S142AKBMGHDiag1.dll",
    "archive_path": DIAGNOSTIC_DLL,
}
require(spec["local_plugin_builds"] == [expected_local_build], "Local plugin build contract drift")
require(spec["text_assertions"] == [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}], "Text assertion drift")

require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "BuildSpecs/current.json must remain the idle controller")
require(ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip() == "S1.42AK", "Runtime ACTIVE_BUILD drift")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(current_state["active_candidate"] is None, "Lifecycle unexpectedly has an active candidate")
require(current_state["runtime_test_outstanding"] is False, "Lifecycle unexpectedly authorizes runtime testing")

provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
require(provenance["result"] == "PASS", "Fresh LLL provenance did not pass")
require(provenance["profile_sha256"] == EXPECTED_BASE_SHA256, "Provenance profile mismatch")
require(provenance["dependency_version"] == "1.7.12", "Provenance LLL version mismatch")
require(provenance["dll_sha256"] == EXPECTED_LLL_DLL_SHA256 and provenance["dll_hash_match"] is True,
        "Fresh LLL DLL identity mismatch")

base = ROOT / spec["base_profile"]
output = ROOT / spec["output_profile"]
require(sha256(base.read_bytes()) == EXPECTED_BASE_SHA256, "Exact S1.42AK base SHA mismatch")
require(output.is_file(), "Diagnostic output profile missing")

original = members(base)
built = members(output)
require(set(built) - set(original) == {DIAGNOSTIC_DLL}, "Added archive member mismatch")
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

diagnostic_hash = sha256(built[DIAGNOSTIC_DLL])
if gate_mode == "review-build":
    compiled = ROOT / expected_local_build["built_file"]
    require(compiled.is_file(), "Compiled diagnostic DLL missing")
    require(compiled.read_bytes() == built[DIAGNOSTIC_DLL], "Injected diagnostic DLL differs from compiled DLL")
else:
    require(sha256(output.read_bytes()) == EXPECTED_OUTPUT_SHA256, "Published profile SHA drift")
    require(diagnostic_hash == EXPECTED_DIAGNOSTIC_DLL_SHA256, "Published diagnostic DLL SHA drift")
    require(PUBLICATION_PATH.is_file(), "Published mode requires publication verification evidence")
    publication = PUBLICATION_PATH.read_text(encoding="utf-8")
    for marker in (
        f"Static/build gate: run `{EXPECTED_REVIEW_RUN}` (#2).",
        f"artifact ID `{EXPECTED_REVIEW_ARTIFACT_ID}`",
        f"Published profile SHA-256: `{EXPECTED_OUTPUT_SHA256}`",
        f"Published diagnostic DLL SHA-256: `{EXPECTED_DIAGNOSTIC_DLL_SHA256}`",
        "Status: `PUBLISHED_STATIC_PASS_NOT_RUNTIME_ARMED`.",
    ):
        require(marker in publication, "Publication evidence drift or missing marker: " + marker)
    require(STATIC_PATH.is_file(), "Published mode requires committed static verification evidence")
    committed_static = json.loads(STATIC_PATH.read_text(encoding="utf-8"))
    require(committed_static["status"] == "STATIC_BUILD_PASS_REVIEW_ARTIFACT_NOT_ARMED", "Committed static status drift")
    require(committed_static["output_sha256"] == EXPECTED_OUTPUT_SHA256, "Committed static profile SHA drift")
    require(committed_static["diagnostic_dll_sha256"] == EXPECTED_DIAGNOSTIC_DLL_SHA256, "Committed static DLL SHA drift")
    require(committed_static["lll_dll_sha256"] == EXPECTED_LLL_DLL_SHA256, "Committed static LLL SHA drift")
    require(committed_static["normalizer_sha256"] == EXPECTED_NORMALIZER_SHA256, "Committed static normalizer SHA drift")
    require(committed_static["runtime_armed"] is False, "Committed static evidence unexpectedly runtime-armed")

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMGHDIAG1", "Builder result build ID mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["added_members"] == [DIAGNOSTIC_DLL], "Builder result added-member mismatch")
require(result["changed_existing_members"] == ["export.r2x"], "Builder result changed-member mismatch")

profile_source_export = ROOT / "ProfileSources/S1.42AK-BMGHDIAG1/export.r2x"
profile_source_index = ROOT / "ProfileSources/S1.42AK-BMGHDIAG1/FILE_INDEX.json"
require(profile_source_export.is_file(), "Readable ProfileSources export missing")
require(profile_source_index.is_file(), "Readable ProfileSources FILE_INDEX missing")
require(profile_source_export.read_bytes() == built["export.r2x"], "ProfileSources export differs from built archive")
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
    "build_id": "S1.42AK-BMGHDIAG1",
    "base_sha256": sha256(base.read_bytes()),
    "output_sha256": sha256(output.read_bytes()),
    "diagnostic_dll_sha256": diagnostic_hash,
    "lll_dll_sha256": provenance["dll_sha256"],
    "normalizer_sha256": sha256(built[NORMALIZER_DLL]),
    "archive_members_verified": len(index),
    "added_members": [DIAGNOSTIC_DLL],
    "changed_existing_members": changed,
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "runtime_armed": False,
    "qualification": (
        "Ephemeral CI review build and exact archive-delta validation only. BuildSpecs/current.json and RuntimeInbox/ACTIVE_BUILD.txt remain unchanged; no runtime test is authorized."
        if gate_mode == "review-build"
        else "Post-publication exact-byte validation of the pinned reviewed profile, all FILE_INDEX rows, publication evidence, archive delta and inactive lifecycle. No rebuild, replacement artifact or runtime authorization is performed."
    ),
}
if gate_mode == "review-build":
    STATIC_PATH.parent.mkdir(exist_ok=True)
    STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
