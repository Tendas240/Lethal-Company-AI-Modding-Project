#!/usr/bin/env python3
"""Exact S1.42AK -> BMAFR1 raw-LLL-config inactive review gate. Never publishes or arms runtime."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-BMAFR1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
PROVENANCE_PATH = ROOT / "c3f17-4-s142ak-lll-provenance-output/LLL_PROVENANCE.json"
OWNER_EVIDENCE_PATH = ROOT / "RuntimeEvidence/S1.42A/20260902T224318Z/extracted/config/config/LethalLevelLoader.cfg"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMAFR1_BUILD_EVIDENCE"
STATIC_PATH = EVIDENCE_DIR / "STATIC_VERIFICATION.json"

EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
EXPECTED_DONOR_PROFILE_SHA256 = "b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2"
EXPECTED_DIAGNOSTIC_DLL_SHA256 = "c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1"
EXPECTED_LLL_DLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
EXPECTED_NORMALIZER_SHA256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"

LLL_CONFIG = "BepInEx/config/LethalLevelLoader.cfg"
FOUNDRY_VISIBLE_SECTION = "Custom Dungeon:  Abandoned Foundry"
LLL_SORTING_PREFIX = "\u200b" * 9
FOUNDRY_RAW_SECTION = LLL_SORTING_PREFIX + FOUNDRY_VISIBLE_SECTION
FOUNDRY_RAW_HEADER = f"[{FOUNDRY_RAW_SECTION}]"
DIAGNOSTIC_DLL = "BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll"
NORMALIZER_DLL = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
MANUAL_LEVEL_KEY = "Dungeon Injection Settings - Manual Level Names List"
ENABLE_KEY = "Enable Content Configuration"

DONOR_PROFILE = ROOT / "Profiles/LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic.r2z"


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
    """Visible-equivalence helper only; raw identity checks must never use this."""
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


def is_ini_header(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def is_exact_foundry_header(line: str) -> bool:
    return line.strip().casefold() == FOUNDRY_RAW_HEADER.casefold()


def is_visible_foundry_header(line: str) -> bool:
    stripped = line.strip()
    return (
        is_ini_header(line)
        and visible(stripped).casefold() == f"[{FOUNDRY_VISIBLE_SECTION}]".casefold()
    )


def section_values(text: str) -> tuple[list[str], int, int, dict[str, str]]:
    data = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    visible_starts = [i for i, line in enumerate(data) if is_visible_foundry_header(line)]
    require(
        len(visible_starts) == 1,
        "Expected exactly one visible-equivalent Abandoned Foundry section, found "
        + str(len(visible_starts)),
    )
    start = visible_starts[0]
    require(
        is_exact_foundry_header(data[start]),
        "Abandoned Foundry raw category mismatch: exact nine-U+200B LLL header required",
    )

    raw_inner = data[start].strip()[1:-1]
    prefix = raw_inner[: -len(FOUNDRY_VISIBLE_SECTION)]
    require(prefix == LLL_SORTING_PREFIX, "Foundry sorting prefix is not exactly nine U+200B")
    require(len(prefix) == 9, "Foundry sorting prefix length drift")
    require(all(ord(ch) == 0x200B for ch in prefix), "Foundry sorting prefix contains a non-U+200B code point")

    end = len(data)
    for i in range(start + 1, len(data)):
        if is_ini_header(data[i]):
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


def exact_member(profile: Path, member: str) -> bytes:
    archive = members(profile)
    require(member in archive, f"Missing {member} in {profile}")
    return archive[member]


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip()

require(spec["enabled"] is True, "BMAFR1 review recipe must be enabled")
require(spec["build_id"] == "S1.42AK-BMAFR1", "Build ID drift")
require(spec["base_profile"] == "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z",
        "BMAFR1 must derive directly from exact accepted S1.42AK")
require(spec["base_sha256"] == EXPECTED_BASE_SHA256, "Accepted S1.42AK base SHA guard drift")
require(spec["output_profile"] == "Profiles/LC V1 S1.42AK-BMAFR1.r2z", "Output profile path drift")
require(spec["profile_name"] == "LC V1 S1.42AK-BMAFR1", "Short review profile identity drift")
require(spec["overwrite"] is False, "Overwrite must remain disabled")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "file_injections", "local_plugin_builds"):
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
    {
        "path": LLL_CONFIG,
        "section": FOUNDRY_RAW_SECTION,
        "forbid_visible_equivalent_duplicates": True,
        "key": key,
        "value": review_values[key],
    }
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
require(spec["config_patches"] == expected_config_patches, "Raw Foundry config patch contract drift")

expected_archive_injection = {
    "source_profile": "Profiles/LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic.r2z",
    "source_profile_sha256": EXPECTED_DONOR_PROFILE_SHA256,
    "source_member": DIAGNOSTIC_DLL,
    "source_member_sha256": EXPECTED_DIAGNOSTIC_DLL_SHA256,
    "archive_path": DIAGNOSTIC_DLL,
}
require(spec.get("archive_member_injections") == [expected_archive_injection],
        "Exact diagnostic DLL reuse contract drift")
require(spec["text_assertions"] == [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}],
        "Text assertion drift")
require(spec.get("snapshot_dir") == "ProfileSources/S1.42AK-BMAFR1", "Snapshot path drift")

require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
        "BuildSpecs/current.json idle scope drift")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD must remain S1.42AK-BMDSFIX1")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(current_state["accepted_baseline"]["sha256"] == EXPECTED_BASE_SHA256, "Accepted baseline SHA drift")
require(current_state["latest_built_artifact"]["build_id"] == "S1.42AK-BMDSFIX1",
        "Inactive review must not replace latest built gameplay artifact")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1",
        "Inactive review must not replace active gameplay candidate")
require(current_state["runtime_test_outstanding"] is True, "Existing BMDSFIX1 runtime gate must remain outstanding")
selected_scope = current_state["selected_scope"]
require(selected_scope["accepted_baseline"] == "S1.42AK", "Selected-scope accepted baseline drift")
require("DO_NOT_RERUN" in selected_scope["finding"], "PATH1 DO_NOT_RERUN lifecycle finding lost")
require("do not rerun path1" in selected_scope["analysis_contract"].lower(),
        "PATH1 no-rerun analysis contract lost")
require("nine U+200B" in selected_scope["analysis_contract"], "Raw nine-U+200B repair contract lost")
require("repair successor" in selected_scope["next_action"].lower(), "Repair-successor authorization lost")
require("inactive review artifact" in selected_scope["next_action"].lower(), "Inactive-review authorization lost")

provenance = json.loads(PROVENANCE_PATH.read_text(encoding="utf-8"))
require(provenance["result"] == "PASS", "Fresh LLL provenance did not pass")
require(provenance["profile_sha256"] == EXPECTED_BASE_SHA256, "LLL provenance profile mismatch")
require(provenance["dependency_version"] == "1.7.12", "LLL provenance version mismatch")
require(provenance["dll_sha256"] == EXPECTED_LLL_DLL_SHA256 and provenance["dll_hash_match"] is True,
        "Fresh LLL DLL identity mismatch")

base = ROOT / spec["base_profile"]
output = ROOT / spec["output_profile"]
require(sha256(base.read_bytes()) == EXPECTED_BASE_SHA256, "Exact S1.42AK base SHA mismatch")
require(output.is_file(), "BMAFR1 inactive review profile missing")
require(sha256(DONOR_PROFILE.read_bytes()) == EXPECTED_DONOR_PROFILE_SHA256, "Diagnostic donor profile SHA drift")

donor_dll = exact_member(DONOR_PROFILE, DIAGNOSTIC_DLL)
require(sha256(donor_dll) == EXPECTED_DIAGNOSTIC_DLL_SHA256, "Diagnostic donor DLL SHA drift")

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
base_visible_foundry = [line for line in base_config_text.split("\n") if is_visible_foundry_header(line)]
require(base_visible_foundry == [], "Accepted S1.42AK unexpectedly contains a visible-equivalent Foundry section")
review_lines, review_start, review_end, actual_review_values = section_values(review_config_text)
require(actual_review_values == review_values, "Materialized Foundry owner values / authorized Black Mesa delta mismatch")
require(actual_review_values[MANUAL_LEVEL_KEY].count("Black Mesa:100") == 1,
        "Black Mesa:100 must occur exactly once in Foundry Manual Level Names")
require("External:100" not in actual_review_values[MANUAL_LEVEL_KEY],
        "Unauthorized External:100 Foundry availability delta")
require(trim_blank_tail(review_lines[:review_start]) == trim_blank_tail(base_config_text.split("\n")),
        "LLL config content before materialized raw Foundry section drifted")
require(review_end == len(review_lines), "Raw Foundry review section must be the only appended section at file tail")
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

require(DIAGNOSTIC_DLL in built, "Reused BMAFDIAG1 diagnostic DLL missing")
require(built[DIAGNOSTIC_DLL] == donor_dll, "BMAFR1 diagnostic DLL differs from exact published BMAFDIAG1 bytes")
diagnostic_hash = sha256(built[DIAGNOSTIC_DLL])
require(diagnostic_hash == EXPECTED_DIAGNOSTIC_DLL_SHA256, "BMAFR1 diagnostic DLL SHA drift")

result_path = ROOT / spec["result_json"]
require(result_path.is_file(), "Build result JSON missing")
result = json.loads(result_path.read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AK-BMAFR1", "Builder result build ID mismatch")
require(result["output_sha256"] == sha256(output.read_bytes()), "Builder result output SHA mismatch")
require(result["added_members"] == [DIAGNOSTIC_DLL], "Builder result added-member mismatch")
require(set(result["changed_existing_members"]) == {"export.r2x", LLL_CONFIG},
        "Builder result changed-member mismatch")

profile_source_export = ROOT / "ProfileSources/S1.42AK-BMAFR1/export.r2x"
profile_source_config = ROOT / "ProfileSources/S1.42AK-BMAFR1/BepInEx/config/LethalLevelLoader.cfg"
profile_source_index = ROOT / "ProfileSources/S1.42AK-BMAFR1/FILE_INDEX.json"
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
    "status": "STATIC_BUILD_PASS_RAW_LLL_BINDING_REVIEW_ARTIFACT_NOT_PUBLISHED_NOT_ARMED",
    "build_id": "S1.42AK-BMAFR1",
    "base_sha256": sha256(base.read_bytes()),
    "output_sha256": sha256(output.read_bytes()),
    "diagnostic_dll_sha256": diagnostic_hash,
    "diagnostic_dll_reused_byte_exact": True,
    "diagnostic_donor_profile_sha256": sha256(DONOR_PROFILE.read_bytes()),
    "lll_dll_sha256": provenance["dll_sha256"],
    "normalizer_sha256": sha256(built[NORMALIZER_DLL]),
    "archive_members_verified": len(index),
    "added_members": [DIAGNOSTIC_DLL],
    "changed_existing_members": changed,
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 1,
    "foundry_raw_section_u200b_count": 9,
    "foundry_plain_section_present": False,
    "foundry_visible_equivalent_section_count": 1,
    "foundry_content_configuration_enabled": True,
    "foundry_manual_level_names_delta": "Black Mesa:100",
    "foundry_owner_values_preserved": True,
    "runtime_active_build": active_build,
    "active_gameplay_candidate": current_state["active_candidate"]["build_id"],
    "runtime_armed": False,
    "published": False,
    "qualification": (
        "Ephemeral repository-native inactive review build only. Direct parent is exact accepted S1.42AK. "
        "The single Foundry category uses the exact LLL 1.7.12 nine-U+200B raw identity; plain or duplicate "
        "visible-equivalent categories fail closed. The exact published BMAFDIAG1 diagnostic DLL is reused "
        "byte-for-byte. Only Enable Content Configuration=true and exact Black Mesa:100 are semantic owner-config "
        "deltas. BuildSpecs/current.json and RuntimeInbox/ACTIVE_BUILD.txt remain unchanged."
    ),
}
STATIC_PATH.parent.mkdir(exist_ok=True)
STATIC_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
