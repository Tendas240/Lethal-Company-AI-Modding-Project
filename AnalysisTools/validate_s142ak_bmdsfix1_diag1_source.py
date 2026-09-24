#!/usr/bin/env python3
"""S1.42AK-BMDSFIX1-DIAG1 source/static fail-closed contract gate. Never builds or arms a Gale profile."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "Patches/S142AKBMDSFix1Diag1"
PLUGIN = PATCH / "Plugin.cs"
SELECTION = PATCH / "SelectionPolicy.cs"
TESTS = PATCH / "Tests/Program.cs"
SAFETY = PATCH / "PATCH_SAFETY_REVIEW.md"
WORKFLOW = ROOT / ".github/workflows/s142ak-bmdsfix1-diag1-source-static.yml"
PLAN = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_PLAN.md"
CURRENT_BUILD = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE = ROOT / "Current/CURRENT_STATE.json"

BASELINE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
BMDS_PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
BMDS_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def strip_csharp_noncode(text):
    pattern = re.compile(
        r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
        re.DOTALL,
    )
    return pattern.sub("", text)


plugin = PLUGIN.read_text(encoding="utf-8")
plugin_code = strip_csharp_noncode(plugin)
selection = SELECTION.read_text(encoding="utf-8")
tests = TESTS.read_text(encoding="utf-8")
safety = SAFETY.read_text(encoding="utf-8")
workflow = WORKFLOW.read_text(encoding="utf-8")
plan = PLAN.read_text(encoding="utf-8")
current_build = json.loads(CURRENT_BUILD.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD.read_text(encoding="utf-8").strip()

# Live/build controller invariants: source work must not arm or replace anything.
require(current_build["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Current build controller ID drift")
require(current_build["base_profile"] == "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z", "Current build base profile drift")
require(current_build["base_sha256"] == BMDS_PROFILE_SHA, "Current build base SHA drift")
require(current_build["local_plugin_builds"] == [], "Source stage must not arm a local plugin build")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD drift")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline ID drift")
require(current_state["accepted_baseline"]["sha256"] == BASELINE_SHA, "Accepted baseline SHA drift")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active candidate ID drift")
require(current_state["active_candidate"]["sha256"] == BMDS_PROFILE_SHA, "Active candidate profile SHA drift")
require(current_state["runtime_test_outstanding"] is True, "BMDSFIX1 target runtime gate must remain outstanding")
require(current_state["selected_scope"]["baseline_inventory"]["accepted_normalizer_sha256"] == NORMALIZER_SHA,
        "Accepted S1.42AB normalizer SHA drift")
require(BMDS_DLL_SHA in current_state["selected_scope"]["analysis_contract"], "BMDSFIX1 DLL SHA missing from canonical analysis contract")

# Exact one-patch source contract and provenance guards.
for literal in (
    "S1.42AK-BMDSFIX1-DIAG1",
    "com.tendas240.s142ak.bmdsfix1.diag1",
    "GetValidExtendedDungeonFlows",
    "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText",
    "NumberlessPlanetName",
    "Black Mesa",
    "DeepSewersFlow",
    "1.7.12",
    LLL_SHA,
    NORMALIZER_SHA,
    "after = new[] { NormalizerGuid }",
    "priority = Priority.Last",
    "diagnostic.priority == Priority.Last",
    "[BMDSFIX1-DIAG1] ARMED",
    "[BMDSFIX1-DIAG1] SELECTED Black Mesa / DeepSewersFlow",
    "[BMDSFIX1-DIAG1] REFUSED TO ARM; normal behavior preserved",
    "[BMDSFIX1-DIAG1] REFUSED selection; normal viable pool preserved",
):
    require(literal in plugin, "Missing diagnostic source contract literal: " + literal)

require(plugin.count("_harmony.Patch(") == 1, "Diagnostic must install exactly one Harmony patch surface")
for forbidden in (
    "PatchAll(",
    "prefix:",
    "transpiler:",
    ".SetValue(",
    "EntranceTeleport",
    "TeleportPlayer",
    "NavMesh",
    "GetClampedDungeonSize",
    "RoundManager",
    "UnityEngine.Random",
    "System.Random",
    "RegisterExtendedDungeonFlow",
):
    require(forbidden not in plugin_code, "Forbidden diagnostic code surface present: " + forbidden)
require("[BMDSFIX1] APPLIED" not in plugin, "Diagnostic must never emit or simulate the BMDSFIX1 APPLIED marker")
require("BMGHDIAG" not in plugin, "Greenhouse diagnostic implementation leaked into DIAG1")

for literal in (
    "Deep Sewers",
    "DeepSewersFlow",
    "Duplicate viable Deep Sewers entries",
    "accepted normalized rarity 100",
    "Null viable wrapper",
    "Unrecognized Black Mesa debug-results caller",
):
    require(literal in selection, "Pure selection policy contract missing: " + literal)

for literal in (
    "terminal simulation must remain normal",
    "expected fail-closed refusal",
    "refusal changed pool count",
    "refusal changed pool identity/order",
    "DeepSewersFlow\", 65",
    "DeepSewersFlow\", 0",
    "null, deepSewers",
    "deepSewers, null",
):
    require(literal in tests, "Required pure negative test missing: " + literal)

require("Exactly one Harmony surface exists" in safety, "Patch Safety Review surface count missing")
require("GetClampedDungeonSize()" in safety and "sole owner" in safety, "Patch Safety Review BMDS ownership boundary missing")
require("DIAGNOSTIC ONLY / NEVER ACCEPT" in plan, "Plan diagnostic acceptance boundary missing")
require(BMDS_PROFILE_SHA in plan and BMDS_DLL_SHA in plan and BASELINE_SHA in plan, "Plan fixed-byte provenance missing")
require("No review `.r2z` is produced by this stage." in plan, "Plan source/build boundary missing")

require("profile_builder.py" not in workflow, "Source-only CI must not invoke the Gale profile builder")
require("dotnet run --project Patches/S142AKBMDSFix1Diag1/Tests/Policy.Tests.csproj" in workflow,
        "Pure policy test command missing")
require("dotnet build S142AKBMDSFix1Diag1.csproj -c Release" in workflow,
        "Plugin source compile command missing")
require("python AnalysisTools/validate_s142ak_bmdsfix1_diag1_source.py" in workflow,
        "Static validator command missing")

report = {
    "status": "SOURCE_PURE_STATIC_CONTRACT_PASS_NOT_BUILT_NOT_ARMED",
    "candidate_id": "S1.42AK-BMDSFIX1-DIAG1",
    "diagnostic_only": True,
    "harmony_surfaces": 1,
    "gameplay_mutating_surfaces": 1,
    "parent_profile_sha256": BMDS_PROFILE_SHA,
    "parent_bmdsfix1_dll_sha256": BMDS_DLL_SHA,
    "current_build_controller_enabled": current_build["enabled"],
    "runtime_active_build": active_build,
    "profile_builder_invoked_by_source_ci": False,
    "qualification": "Source/compile/pure-policy validation only; no review profile, Gale activation, runtime qualification or acceptance."
}
print(json.dumps(report, indent=2))
