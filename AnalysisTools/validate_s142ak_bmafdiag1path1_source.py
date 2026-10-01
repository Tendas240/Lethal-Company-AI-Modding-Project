#!/usr/bin/env python3
"""BMAFDIAG1PATH1 source/static identity-only successor gate. Never builds, publishes or arms runtime."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "RepositoryTools"))
import gale_profile_path_length_guard as path_guard

SPEC = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1PATH1.json"
PLAN = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_PLAN.md"
BASE = ROOT / "Profiles/LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic.r2z"
CURRENT_BUILD = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE = ROOT / "Current/CURRENT_STATE.json"
BLOCK_RECORD = ROOT / "Current/212_S1.42AK_BMAFDIAG1_PATH_LENGTH_BLOCK_AND_GUARD_RECONCILIATION.md"
EXPECTED_HASHES = ROOT / "Profiles/EXPECTED_HASHES.json"

EXPECTED_BUILD_ID = "S1.42AK-BMAFDIAG1PATH1"
EXPECTED_BASE_SHA256 = "b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2"
EXPECTED_PARENT_NAME = "LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic"
EXPECTED_PROFILE_NAME = "LC V1 S1.42AK-BMAFD1P1"
EXPECTED_OUTPUT = "Profiles/LC V1 S1.42AK-BMAFD1P1.r2z"
EXPECTED_DLL = "BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll"
EXPECTED_DLL_SHA256 = "c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1"
EXPECTED_LLL = "BepInEx/config/LethalLevelLoader.cfg"
EXPECTED_LLL_SHA256 = "c9f03e7839c70ce21fae37ff597085175de35a9c176b97aed40798401ce66c0e"
EXPECTED_MEMBERS = 337
EXPECTED_OLD_PATHS = (260, 262)
EXPECTED_NEW_PATHS = (219, 221)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    require(path.exists(), "Missing required path: " + str(path.relative_to(ROOT)))
    return path.read_text(encoding="utf-8")


spec = json.loads(read(SPEC))
plan = read(PLAN)
state = json.loads(read(CURRENT_STATE))
current_build = json.loads(read(CURRENT_BUILD))
active_build = read(ACTIVE_BUILD).strip()
block_record = read(BLOCK_RECORD)
expected_hashes = read(EXPECTED_HASHES)

# Exact separately versioned identity-only recipe.
require(spec["enabled"] is True, "Successor source spec must be explicitly enabled for later isolated review use")
require(spec["build_id"] == EXPECTED_BUILD_ID, "Unexpected successor build_id")
require(spec["base_profile"] == str(BASE.relative_to(ROOT)).replace("\\", "/"), "Successor must derive directly from exact published BMAFDIAG1")
require(spec["base_sha256"] == EXPECTED_BASE_SHA256, "Unexpected immutable BMAFDIAG1 parent SHA")
require(spec["output_profile"] == EXPECTED_OUTPUT, "Unexpected successor output profile")
require(spec["profile_name"] == EXPECTED_PROFILE_NAME, "Unexpected short successor profile identity")
require(spec["overwrite"] is False, "Successor output must not overwrite an existing profile")
for key in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections", "local_plugin_builds"):
    require(spec[key] == [], "Identity-only successor must keep " + key + " empty")

# Immutable exact parent bytes.
base_bytes = BASE.read_bytes()
require(sha256(base_bytes) == EXPECTED_BASE_SHA256, "Exact published BMAFDIAG1 parent SHA mismatch")
with zipfile.ZipFile(BASE) as zf:
    names = zf.namelist()
    require(len(names) == EXPECTED_MEMBERS, "Unexpected BMAFDIAG1 parent archive member count")
    require(len(names) == len(set(names)), "BMAFDIAG1 parent contains duplicate archive member names")
    export = zf.read("export.r2x").decode("utf-8-sig")
    require(export.startswith("profileName: " + EXPECTED_PARENT_NAME + "\n"), "Parent export profileName drift")
    require(sha256(zf.read(EXPECTED_DLL)) == EXPECTED_DLL_SHA256, "BMAFDIAG1 diagnostic DLL bytes drift")
    require(sha256(zf.read(EXPECTED_LLL)) == EXPECTED_LLL_SHA256, "Frozen BMAFDIAG1 Foundry LLL config bytes drift")

# Permanent path guard is the authority; pin the observed parent and proposed successor projections.
old_paths = tuple(row[2] for row in path_guard.projections(EXPECTED_PARENT_NAME))
new_paths = tuple(row[2] for row in path_guard.projections(EXPECTED_PROFILE_NAME))
require(old_paths == EXPECTED_OLD_PATHS, "Blocked parent path projection drift: " + repr(old_paths))
require(new_paths == EXPECTED_NEW_PATHS, "Short successor path projection drift: " + repr(new_paths))
require(path_guard.violations(EXPECTED_PROFILE_NAME) == [], "Short successor violates permanent Gale path budget")
require(max(new_paths) <= path_guard.SAFE_RUNTIME_PATH_CHARS, "Short successor exceeds project path budget")

# Collision/provenance boundary: historical D1P1 exists, this successor must remain distinct and not yet indexed here.
require(EXPECTED_PROFILE_NAME != "LC V1 S1.42AK-D1P1", "BMAF successor collides with historical Deep-Sewers D1P1 identity")
require("LC V1 S1.42AK-D1P1" in expected_hashes, "Historical DIAG1PATH1 index provenance unexpectedly missing")

# Live controllers and acceptance remain inert.
require(current_build["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Current build controller drift")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime attribution must remain S1.42AK-BMDSFIX1")
require(state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active gameplay candidate drift")
require(state["runtime_test_outstanding"] is True, "Passive BMDSFIX1 target gate must remain outstanding")
diag = state["selected_scope"]["diagnostic_revision"]
require(diag["build_id"] == "S1.42AK-BMAFDIAG1", "Current diagnostic parent drift")
require(diag["sha256"] == EXPECTED_BASE_SHA256, "Current diagnostic parent SHA drift")
require(diag["diagnostic_dll_sha256"] == EXPECTED_DLL_SHA256, "Current diagnostic DLL SHA drift")
require(diag["runtime_armed"] is False, "Blocked long-name BMAFDIAG1 must remain de-armed")
require("DO_NOT_RERUN" in diag["status"], "Blocked long-name BMAFDIAG1 lost DO_NOT_RERUN status")

# Documentation binds the exact source/static boundary without authorizing later gates.
for literal in (
    EXPECTED_BUILD_ID,
    EXPECTED_BASE_SHA256,
    EXPECTED_PROFILE_NAME,
    EXPECTED_DLL_SHA256,
    EXPECTED_LLL_SHA256,
    "219 / 221",
    "260 / 262",
    "DIAGNOSTIC ONLY / NEVER ACCEPT",
    "inactive review build",
    "DO NOT RERUN",
):
    require(literal in plan, "Plan missing required contract literal: " + literal)
for literal in (
    EXPECTED_BASE_SHA256,
    EXPECTED_DLL_SHA256,
    "identity-only",
    "DO NOT RERUN",
):
    require(literal in block_record, "Path-length authority missing required parent boundary: " + literal)

print("PASS: S1.42AK-BMAFDIAG1PATH1 source/static identity-only contract; paths", old_paths, "->", new_paths)
