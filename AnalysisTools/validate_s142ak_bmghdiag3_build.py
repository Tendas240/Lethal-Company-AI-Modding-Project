#!/usr/bin/env python3
"""C3F18 exact S1.42AK -> BMGHDIAG3 inactive review-build/archive/lifecycle gate. Never publishes or arms runtime."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG3.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
PROVENANCE_PATH = ROOT / "c3f17-4-s142ak-lll-provenance-output/LLL_PROVENANCE.json"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE"
STATIC_PATH = EVIDENCE_DIR / "STATIC_VERIFICATION.json"
PATCH = ROOT / "Patches/S142AKBMGHDiag3"
PLUGIN = PATCH / "Plugin.cs"
RUNTIME_IDENTITY = PATCH / "RuntimeIdentityPolicy.cs"
HARNESS = ROOT / "AnalysisTools/S142AKBMGHDiag3PolicyTests/Program.cs"

EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
EXPECTED_LLL_DLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
EXPECTED_NORMALIZER_SHA256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
DIAGNOSTIC_DLL = "BepInEx/plugins/S142AKBMGHDiag3/S142AKBMGHDiag3.dll"
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


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip()

require(spec["enabled"] is True, "Separate BMGHDIAG3 review recipe must remain enabled")
require(spec["build_id"] == "S1.42AK-BMGHDIAG3", "Build ID drift")
require(spec["base_profile"] == "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z",
        "BMGHDIAG3 review profile must derive directly from exact accepted S1.42AK")
require(spec["base_sha256"] == EXPECTED_BASE_SHA256, "Accepted S1.42AK base SHA guard drift")
require(spec["output_profile"] == "Profiles/LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic.r2z",
        "Output profile path drift")
require(spec["profile_name"] == "LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic",
        "Review profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections"):
    require(spec[field] == [], "Unauthorized " + field)

expected_local_build = {
    "project": "Patches/S142AKBMGHDiag3/S142AKBMGHDiag3.csproj",
    "configuration": "Release",
    "built_file": "Patches/S142AKBMGHDiag3/bin/Release/netstandard2.1/S142AKBMGHDiag3.dll",
    "archive_path": DIAGNOSTIC_DLL,
}
require(spec["local_plugin_builds"] == [expected_local_build], "Local plugin build contract drift")
require(spec["text_assertions"] == [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}],
        "Text assertion drift")

require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
        "BuildSpecs/current.json idle scope drift")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD must remain S1.42AK-BMDSFIX1")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(current_state["accepted_baseline"]["sha256"] == EXPECTED_BASE_SHA256, "Accepted baseline SHA drift")
require(current_state["latest_built_artifact"]["build_id"] == "S1.42AK-BMDSFIX1",
        "Review build must not replace latest built gameplay artifact")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1",
        "Review build must not replace active gameplay candidate")
require(current_state["runtime_test_outstanding"] is True,
        "Existing BMDSFIX1 runtime gate must remain outstanding")
selected_scope = current_state["selected_scope"]
require(selected_scope["accepted_baseline"] == "S1.42AK", "Selected-scope accepted baseline drift")
require("S1.42AK-BMDSFIX1" in selected_scope["analysis_contract"] and
        "DeepSewersFlow" in selected_scope["analysis_contract"] and
        "outstanding" in selected_scope["analysis_contract"].lower() and
        "passive" in selected_scope["analysis_contract"].lower(),
        "Existing BMDSFIX1 passive runtime gate contract was lost")
require("S1.42AK-BMGHDIAG3" in selected_scope["next_action"] and
        "inactive review-build" in selected_scope["next_action"].lower(),
        "Current lifecycle no longer authorizes the bounded BMGHDIAG3 inactive review build")

expected_source_files = {
    "GameAssemblyProvenance.cs",
    "NuGet.Config",
    "ObservationPolicy.cs",
    "Plugin.cs",
    "README.md",
    "RuntimeIdentityPolicy.cs",
    "S142AKBMGHDiag3.csproj",
    "SelectionPolicy.cs",
}
require({p.name for p in PATCH.iterdir() if p.is_file()} == expected_source_files,
        "BMGHDIAG3 integrated source file set drift")
generated_dirs = {p.name for p in PATCH.iterdir() if p.is_dir()}
require(generated_dirs <= {"bin", "obj"},
        "BMGHDIAG3 source directory contains an unexpected committed/test subdirectory: " + repr(sorted(generated_dirs)))
require(not (PATCH / "Tests").exists(),
        "BMGHDIAG3 policy-test harness must remain outside Patches/S142AKBMGHDiag3")

plugin = PLUGIN.read_text(encoding="utf-8")
runtime_identity = RUNTIME_IDENTITY.read_text(encoding="utf-8")
harness = HARNESS.read_text(encoding="utf-8")
require("runtimeAssembly != null && runtimeAssembly.ManifestModule != null" in plugin,
        "Non-null runtime assembly/module presence guard was weakened")
for forbidden in ("ManifestModule.Name", "manifestModuleName", "ScopeName", "ModuleVersionId", "MetadataToken", "CodeBase"):
    require(forbidden not in runtime_identity, "Forbidden replacement runtime identity predicate in RuntimeIdentityPolicy: " + forbidden)
require('ValidateAssemblyIdentity("EntranceTeleport", "Assembly-CSharp", false)' in harness,
        "Harness does not exercise the BMGHDIAG3 three-argument runtime identity contract")
for forbidden in ("wrong manifest module", "Other.dll", "manifestModuleName"):
    require(forbidden.lower() not in harness.lower(),
            "Harness reintroduced disproven manifest-module-name refusal behavior: " + forbidden)

provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
require(provenance["result"] == "PASS", "Fresh LLL provenance did not pass")
require(provenance["profile_sha256"] == EXPECTED_BASE_SHA256, "LLL provenance profile mismatch")
require(provenance["dependency_version"] == "1.7.12", "LLL provenance version mismatch")
require(provenance["dll_sha256"] == EXPECTED_LLL_DLL_SHA256 and provenance["dll_hash_match"] is True,
        "Fresh LLL DLL identity mismatch")

base = ROOT / spec["base_profile"]
output = ROOT / spec["output_profile"]
require(sha256(base.read_bytes()) == EXPECTED_BASE_SHA256, "Exact S1.42AK base SHA mismatch")
require(output.is_file(), "BMGHDIAG3 review profile missing")

original = members(base)
built = members(output)
require(set(built) - set(original) == {DIAGNOSTIC_DLL}, "Added archive member mismatch")
require(set(original) - set(built) == set(), "Archive member removal detected")
changed = [name for name in original if original[name] != built[name]]
require(changed == ["export.r2x"], "Unexpected changed existing members: " + repr(changed))
require(stable_export(original["export.r2x"]) == stable_export(built["export.r2x"]),
        "Package/config/export drift beyond profile identity metadata")
require("LethalLevelLoaderUpdated" not in built["export.r2x"].decode("utf-8-sig"),
        "Forbidden LethalLevelLoaderUpdated owner in review export")

require(NORMALIZER_DLL in original and NORMALIZER_DLL in built, "Accepted normalizer DLL missing")
require(sha256(original[NORMALIZER_DLL]) == EXPECTED_NORMALIZER_SHA256, "Base normalizer identity drift")
require(sha256(built[NORMALIZER_DLL]) == EXPECTED_NORMALIZER_SHA256, "Review normalizer identity drift")
require(original[NORMALIZER_DLL] == built[NORMALIZER_DLL], "Accepted normalizer bytes changed")

compiled = ROOT / expected_local_build["built_file"]
require(compiled.is_file(), "Compiled BMGHDIAG3 DLL missing")
require(compiled.read_bytes() == built[DIAGNOSTIC_DLL], "Injected BMGHDIAG3 DLL differs from compiled DLL")
diagnostic_hash = sha256(built[DIAGNOSTIC_DLL])

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMGHDIAG3", "Builder result build ID mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["added_members"] == [DIAGNOSTIC_DLL], "Builder result added-member mismatch")
require(result["changed_existing_members"] == ["export.r2x"], "Builder result changed-member mismatch")

profile_source_export = ROOT / "ProfileSources/S1.42AK-BMGHDIAG3/export.r2x"
profile_source_index = ROOT / "ProfileSources/S1.42AK-BMGHDIAG3/FILE_INDEX.json"
require(profile_source_export.is_file(), "Readable ProfileSources export missing")
require(profile_source_index.is_file(), "Readable ProfileSources FILE_INDEX missing")
require(profile_source_export.read_bytes() == built["export.r2x"], "ProfileSources export differs from review archive")
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
    "status": "STATIC_BUILD_PASS_REVIEW_ARTIFACT_NOT_PUBLISHED_NOT_ARMED",
    "build_id": "S1.42AK-BMGHDIAG3",
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
    "runtime_active_build": active_build,
    "active_gameplay_candidate": current_state["active_candidate"]["build_id"],
    "runtime_armed": False,
    "published": False,
    "qualification": (
        "Ephemeral CI inactive review build and exact archive-delta validation only. "
        "Direct parent is exact accepted S1.42AK. BuildSpecs/current.json remains disabled, "
        "RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK-BMDSFIX1, the BMDSFIX1 runtime gate remains outstanding/passive, "
        "and BMGHDIAG3 is not published, Gale-imported or runtime-armed."
    ),
}
STATIC_PATH.parent.mkdir(exist_ok=True)
STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
