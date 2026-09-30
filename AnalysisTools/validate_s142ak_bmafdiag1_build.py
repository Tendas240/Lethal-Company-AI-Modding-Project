#!/usr/bin/env python3
"""C3F19 exact S1.42AK -> BMAFDIAG1 inactive review-build/archive/config/lifecycle gate. Never publishes or arms runtime."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
PROVENANCE_PATH = ROOT / "c3f17-4-s142ak-lll-provenance-output/LLL_PROVENANCE.json"
OWNER_EVIDENCE_PATH = ROOT / "RuntimeEvidence/S1.42A/20260902T224318Z/extracted/config/config/LethalLevelLoader.cfg"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE"
STATIC_PATH = EVIDENCE_DIR / "STATIC_VERIFICATION.json"
PATCH = ROOT / "Patches/S142AKBMAFDiag1"
HARNESS = ROOT / "AnalysisTools/S142AKBMAFDiag1PolicyTests/Program.cs"

EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
EXPECTED_LLL_DLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
EXPECTED_NORMALIZER_SHA256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
LLL_CONFIG = "BepInEx/config/LethalLevelLoader.cfg"
FOUNDRY_SECTION = "Custom Dungeon:  Abandoned Foundry"
DIAGNOSTIC_DLL = "BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll"
NORMALIZER_DLL = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
MANUAL_LEVEL_KEY = "Dungeon Injection Settings - Manual Level Names List"
ENABLE_KEY = "Enable Content Configuration"


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


def normalized_text(data: bytes) -> str:
    return data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def visible(text: str) -> str:
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


def is_target_header(line: str) -> bool:
    return visible(line.strip()).casefold() == f"[{FOUNDRY_SECTION}]".casefold()


def section_values(text: str) -> tuple[list[str], int, int, dict[str, str]]:
    data = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    starts = [i for i, line in enumerate(data) if is_target_header(line)]
    require(len(starts) == 1, "Expected exactly one canonical Abandoned Foundry section")
    start = starts[0]
    end = len(data)
    for i in range(start + 1, len(data)):
        stripped = visible(data[i].strip())
        if stripped.startswith("[") and stripped.endswith("]"):
            end = i
            break
    values: dict[str, str] = {}
    for line in data[start + 1:end]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        require(key not in values, "Duplicate Foundry config key: " + key)
        values[key] = value
    return data, start, end, values


def stable_export(data: bytes) -> str:
    text = normalized_text(data)
    require(len(re.findall(r"(?m)^profileName:.*$", text)) == 1, "Expected exactly one profileName field")
    return re.sub(r"(?m)^profileName:.*$", "profileName: <identity>", text).rstrip("\n")


def trim_blank_tail(items: list[str]) -> list[str]:
    out = list(items)
    while out and out[-1].strip() == "":
        out.pop()
    return out


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip()

require(spec["enabled"] is True, "Separate BMAFDIAG1 review recipe must remain enabled")
require(spec["build_id"] == "S1.42AK-BMAFDIAG1", "Build ID drift")
require(spec["base_profile"] == "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z",
        "BMAFDIAG1 review profile must derive directly from exact accepted S1.42AK")
require(spec["base_sha256"] == EXPECTED_BASE_SHA256, "Accepted S1.42AK base SHA guard drift")
require(spec["output_profile"] == "Profiles/LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic.r2z",
        "Output profile path drift")
require(spec["profile_name"] == "LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic",
        "Review profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "file_injections"):
    require(spec[field] == [], "Unauthorized " + field)

owner_text = OWNER_EVIDENCE_PATH.read_text(encoding="utf-8-sig")
_owner_lines, _owner_start, _owner_end, owner_values = section_values(owner_text)
expected_owner_keys = {
    ENABLE_KEY,
    "General Settings - Enable Dynamic Dungeon Size Restriction",
    "General Settings - Minimum Dungeon Size Multiplier",
    "General Settings - Maximum Dungeon Size Multiplier",
    "General Settings - Restrict Dungeon Size Scaler",
    "Dungeon Injection Settings - Manual Mod Names List",
    MANUAL_LEVEL_KEY,
    "Dungeon Injection Settings - Dynamic Level Tags List",
    "Dungeon Injection Settings - Dynamic Route Price List",
}
require(set(owner_values) == expected_owner_keys, "Owner-default Foundry key set drift")
require(owner_values[ENABLE_KEY] == "false", "Owner-default Foundry Enable Content Configuration drift")
require(owner_values["General Settings - Enable Dynamic Dungeon Size Restriction"] == "false", "Owner dynamic-size enable drift")
require(owner_values["General Settings - Minimum Dungeon Size Multiplier"] == "1", "Owner minimum size drift")
require(owner_values["General Settings - Maximum Dungeon Size Multiplier"] == "1", "Owner maximum size drift")
require(owner_values["General Settings - Restrict Dungeon Size Scaler"] == "1", "Owner size scaler drift")
require(owner_values["Dungeon Injection Settings - Manual Mod Names List"] == "Default Values Were Empty", "Owner Manual Mod Names drift")
require(owner_values["Dungeon Injection Settings - Dynamic Level Tags List"] == "Murica:300,Canyon:50,Wasteland:150", "Owner Dynamic Level Tags drift")
require(owner_values["Dungeon Injection Settings - Dynamic Route Price List"] == "Default Values Were Empty", "Owner Route Price drift")
owner_manual_levels = owner_values[MANUAL_LEVEL_KEY]
require("Black Mesa:" not in owner_manual_levels, "Owner default unexpectedly already contains Black Mesa")

review_values = dict(owner_values)
review_values[ENABLE_KEY] = "true"
review_values[MANUAL_LEVEL_KEY] = owner_manual_levels + ",Black Mesa:100"
expected_config_patches = [
    {"path": LLL_CONFIG, "section": FOUNDRY_SECTION, "key": key, "value": review_values[key]}
    for key in [
        ENABLE_KEY,
        "General Settings - Enable Dynamic Dungeon Size Restriction",
        "General Settings - Minimum Dungeon Size Multiplier",
        "General Settings - Maximum Dungeon Size Multiplier",
        "General Settings - Restrict Dungeon Size Scaler",
        "Dungeon Injection Settings - Manual Mod Names List",
        MANUAL_LEVEL_KEY,
        "Dungeon Injection Settings - Dynamic Level Tags List",
        "Dungeon Injection Settings - Dynamic Route Price List",
    ]
]
require(spec["config_patches"] == expected_config_patches, "Foundry config patch contract drift")

expected_local_build = {
    "project": "Patches/S142AKBMAFDiag1/S142AKBMAFDiag1.csproj",
    "configuration": "Release",
    "built_file": "Patches/S142AKBMAFDiag1/bin/Release/netstandard2.1/S142AKBMAFDiag1.dll",
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
next_action = selected_scope["next_action"]
next_action_lower = next_action.lower()
phase_c = selected_scope["phase_c"]
pre_review_authorized = (
    "S1.42AK-BMAFDIAG1" in next_action and
    "inactive review-build" in next_action_lower
)
post_review_reconciled = (
    "S1.42AK-BMAFDIAG1" in next_action and
    "exact-byte publication" in next_action_lower and
    phase_c.get("bmafdiag1_review_checkpoint") == "Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md" and
    phase_c.get("bmafdiag1_review_status") == "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED_EXACT_BYTE_PUBLICATION_NEXT" and
    phase_c.get("bmafdiag1_review_run") == 36735131025 and
    phase_c.get("bmafdiag1_review_artifact_id") == 11106178288 and
    phase_c.get("bmafdiag1_review_evidence") == "BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json" and
    phase_c.get("bmafdiag1_review_published") is False and
    phase_c.get("bmafdiag1_review_runtime_armed") is False and
    phase_c.get("black_mesa_abandoned_foundry_status") == "INACTIVE_REVIEW_BUILD_PASS_PAIR_NOT_YET_PROVEN_EXACT_BYTE_PUBLICATION_NEXT"
)
require(pre_review_authorized or post_review_reconciled,
        "Current lifecycle is neither the authorized BMAFDIAG1 inactive review build nor its exact reconciled review-PASS publication-next state")

expected_source_files = {
    "GameAssemblyProvenance.cs",
    "NuGet.Config",
    "ObservationPolicy.cs",
    "Plugin.cs",
    "README.md",
    "RuntimeIdentityPolicy.cs",
    "S142AKBMAFDiag1.csproj",
    "SelectionPolicy.cs",
}
require({p.name for p in PATCH.iterdir() if p.is_file()} == expected_source_files,
        "BMAFDIAG1 integrated source file set drift")
generated_dirs = {p.name for p in PATCH.iterdir() if p.is_dir()}
require(generated_dirs <= {"bin", "obj"},
        "BMAFDIAG1 source directory contains an unexpected committed/test subdirectory: " + repr(sorted(generated_dirs)))
require(not (PATCH / "Tests").exists(),
        "BMAFDIAG1 policy-test harness must remain outside Patches/S142AKBMAFDiag1")
harness = HARNESS.read_text(encoding="utf-8")
require("SelectionPolicy.FindFoundry" in harness, "Harness does not exercise BMAFDIAG1 Foundry policy")
require('new Entry("Abandoned Foundry", "FoundryFlow", 100)' in harness,
        "Harness does not exercise exact Abandoned Foundry / FoundryFlow rarity-100 target")
require('ValidateAssemblyIdentity("EntranceTeleport", "Assembly-CSharp", false)' in harness,
        "Harness does not exercise the structural runtime identity contract")

provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
require(provenance["result"] == "PASS", "Fresh LLL provenance did not pass")
require(provenance["profile_sha256"] == EXPECTED_BASE_SHA256, "LLL provenance profile mismatch")
require(provenance["dependency_version"] == "1.7.12", "LLL provenance version mismatch")
require(provenance["dll_sha256"] == EXPECTED_LLL_DLL_SHA256 and provenance["dll_hash_match"] is True,
        "Fresh LLL DLL identity mismatch")

base = ROOT / spec["base_profile"]
output = ROOT / spec["output_profile"]
require(sha256(base.read_bytes()) == EXPECTED_BASE_SHA256, "Exact S1.42AK base SHA mismatch")
require(output.is_file(), "BMAFDIAG1 review profile missing")

original = members(base)
built = members(output)
require(set(built) - set(original) == {DIAGNOSTIC_DLL}, "Added archive member mismatch")
require(set(original) - set(built) == set(), "Archive member removal detected")
changed = [name for name in original if original[name] != built[name]]
require(len(changed) == 2 and set(changed) == {"export.r2x", LLL_CONFIG},
        "Unexpected changed existing members: " + repr(changed))
require(stable_export(original["export.r2x"]) == stable_export(built["export.r2x"]),
        "Package/export drift beyond profile identity metadata")
require("LethalLevelLoaderUpdated" not in built["export.r2x"].decode("utf-8-sig"),
        "Forbidden LethalLevelLoaderUpdated owner in review export")

require(LLL_CONFIG in original and LLL_CONFIG in built, "LLL config missing")
base_config_text = normalized_text(original[LLL_CONFIG])
review_config_text = normalized_text(built[LLL_CONFIG])
base_headers = [line for line in base_config_text.split("\n") if is_target_header(line)]
require(base_headers == [], "Accepted S1.42AK unexpectedly contains direct Abandoned Foundry section")
review_lines, review_start, review_end, actual_review_values = section_values(review_config_text)
require(actual_review_values == review_values, "Materialized Foundry owner values / authorized Black Mesa delta mismatch")
require(actual_review_values[MANUAL_LEVEL_KEY].count("Black Mesa:100") == 1,
        "Black Mesa:100 must occur exactly once in Foundry Manual Level Names")
require("External:100" not in actual_review_values[MANUAL_LEVEL_KEY],
        "Unauthorized External:100 Foundry availability delta")
require(trim_blank_tail(review_lines[:review_start]) == trim_blank_tail(base_config_text.split("\n")),
        "LLL config content before materialized Foundry section drifted")
require(review_end == len(review_lines), "Foundry review section must be the only appended section at file tail")
unchanged_owner_keys = expected_owner_keys - {ENABLE_KEY, MANUAL_LEVEL_KEY}
for key in unchanged_owner_keys:
    require(actual_review_values[key] == owner_values[key], "Owner-default value changed: " + key)
require(actual_review_values[ENABLE_KEY] == "true", "Foundry content configuration was not enabled")
require(actual_review_values[MANUAL_LEVEL_KEY] == owner_manual_levels + ",Black Mesa:100",
        "Foundry Manual Level Names is not exact owner mapping plus Black Mesa:100")

require(NORMALIZER_DLL in original and NORMALIZER_DLL in built, "Accepted normalizer DLL missing")
require(sha256(original[NORMALIZER_DLL]) == EXPECTED_NORMALIZER_SHA256, "Base normalizer identity drift")
require(sha256(built[NORMALIZER_DLL]) == EXPECTED_NORMALIZER_SHA256, "Review normalizer identity drift")
require(original[NORMALIZER_DLL] == built[NORMALIZER_DLL], "Accepted normalizer bytes changed")

compiled = ROOT / expected_local_build["built_file"]
require(compiled.is_file(), "Compiled BMAFDIAG1 DLL missing")
require(compiled.read_bytes() == built[DIAGNOSTIC_DLL], "Injected BMAFDIAG1 DLL differs from compiled DLL")
diagnostic_hash = sha256(built[DIAGNOSTIC_DLL])

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMAFDIAG1", "Builder result build ID mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["added_members"] == [DIAGNOSTIC_DLL], "Builder result added-member mismatch")
require(set(result["changed_existing_members"]) == {"export.r2x", LLL_CONFIG},
        "Builder result changed-member mismatch")

profile_source_export = ROOT / "ProfileSources/S1.42AK-BMAFDIAG1/export.r2x"
profile_source_config = ROOT / "ProfileSources/S1.42AK-BMAFDIAG1/BepInEx/config/LethalLevelLoader.cfg"
profile_source_index = ROOT / "ProfileSources/S1.42AK-BMAFDIAG1/FILE_INDEX.json"
require(profile_source_export.is_file(), "Readable ProfileSources export missing")
require(profile_source_config.is_file(), "Readable ProfileSources LLL config missing")
require(profile_source_index.is_file(), "Readable ProfileSources FILE_INDEX missing")
require(profile_source_export.read_bytes() == built["export.r2x"], "ProfileSources export differs from review archive")
require(profile_source_config.read_bytes() == built[LLL_CONFIG], "ProfileSources LLL config differs from review archive")
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
    "build_id": "S1.42AK-BMAFDIAG1",
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
    "config_changes": 1,
    "foundry_section_materialized": True,
    "foundry_content_configuration_enabled": True,
    "foundry_manual_level_names_delta": "Black Mesa:100",
    "foundry_owner_values_preserved": True,
    "runtime_active_build": active_build,
    "active_gameplay_candidate": current_state["active_candidate"]["build_id"],
    "runtime_armed": False,
    "published": False,
    "qualification": (
        "Ephemeral CI inactive review build and exact archive/config-delta validation only. "
        "Direct parent is exact accepted S1.42AK. The only availability semantic delta is the "
        "owner-default Abandoned Foundry LLL section enabled with exactly Black Mesa:100 appended "
        "to its preserved Manual Level Names mapping. BuildSpecs/current.json remains disabled, "
        "RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK-BMDSFIX1, the BMDSFIX1 runtime gate remains "
        "outstanding/passive, and BMAFDIAG1 is not published, Gale-imported or runtime-armed."
    ),
}
STATIC_PATH.parent.mkdir(exist_ok=True)
STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
