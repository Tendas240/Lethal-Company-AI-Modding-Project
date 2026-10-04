#!/usr/bin/env python3
"""S1.42AK-AGDIAG1 source/static fail-closed contract gate. Never builds, publishes or arms a Gale profile."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "Patches/S142AKAGDiag1"
PLUGIN = PATCH / "Plugin.cs"
SELECTION = PATCH / "SelectionPolicy.cs"
TESTS = PATCH / "Tests/Program.cs"
SAFETY = PATCH / "PATCH_SAFETY_REVIEW.md"
WORKFLOW = ROOT / ".github/workflows/s142ak-agdiag1-source-static.yml"
FINDINGS = ROOT / "SourceEvidence/UniversalInteriorViability/AGDIAG1SourceStatic/FINDINGS.md"
CHECKPOINT = ROOT / "Current/255_S1.42AK_PHASE_C_ART_GALLERY_AGDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md"
CURRENT_BUILD = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE = ROOT / "Current/CURRENT_STATE.json"

BASELINE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
BMDS_PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
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
findings = FINDINGS.read_text(encoding="utf-8")
checkpoint = CHECKPOINT.read_text(encoding="utf-8")
current_build = json.loads(CURRENT_BUILD.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE.read_text(encoding="utf-8"))
active_build = ACTIVE_BUILD.read_text(encoding="utf-8").strip()

# Source work must preserve all live/build controllers and accepted gameplay bytes.
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
require(current_state["runtime_test_outstanding"] is True, "BMDSFIX1 regular runtime gate must remain outstanding")

# Frozen identity, provenance and one-patch selector contract.
for literal in (
    "tendas.lethalcompany.s142akagdiag1",
    "S1.42AK-AGDIAG1 Deterministic Art Gallery Selector",
    "1.0.0",
    "imabatby.lethallevelloader",
    "tendas.lethalcompany.s142abinteriorweightnormalization",
    "1.7.12",
    LLL_SHA,
    NORMALIZER_SHA,
    "GetValidExtendedDungeonFlows",
    "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText",
    "NumberlessPlanetName",
    "Offense",
    "Art Gallery",
    "MuseumInteriorFlow",
    "after = new[] { NormalizerGuid }",
    "priority = Priority.Last",
    "diagnostic.priority == Priority.Last",
    "[AGDIAG1] ARMED",
    "[AGDIAG1] SELECTED Offense Art Gallery / MuseumInteriorFlow",
    "[AGDIAG1] REFUSED TO ARM; normal behavior preserved",
    "[AGDIAG1] REFUSED selection; normal viable pool preserved",
):
    require(literal in plugin, "Missing AGDIAG1 source contract literal: " + literal)

require(plugin.count("_harmony.Patch(") == 1, "AGDIAG1 must install exactly one Harmony patch surface")
for forbidden in (
    "PatchAll(",
    "prefix:",
    "transpiler:",
    ".SetValue(",
    "EntranceTeleport",
    "TeleportPlayer",
    "NavMesh",
    "PathfindingLib",
    "GetClampedDungeonSize",
    "RoundManager",
    "UnityEngine.Random",
    "System.Random",
    "RegisterExtendedDungeonFlow",
    "BepInEx/config",
    "BrutalCompany",
    "BCMER",
):
    require(forbidden not in plugin_code, "Forbidden AGDIAG1 code surface present: " + forbidden)
require("[BMDSFIX1] APPLIED" not in plugin, "AGDIAG1 must never emit or simulate BMDSFIX1 APPLIED")

for literal in (
    "Art Gallery",
    "MuseumInteriorFlow",
    "Duplicate viable Art Gallery entries",
    "accepted normalized rarity 100",
    "Null viable wrapper",
    "Unrecognized Offense debug-results caller",
    "Selection accessors are missing",
):
    require(literal in selection, "Pure selection policy contract missing: " + literal)

for literal in (
    "exact Art Gallery target index",
    "selected index must retain existing wrapper identity",
    "debugResults=false must remain normal",
    "non-Offense moon must remain normal",
    "terminal simulation must remain normal",
    "expected fail-closed refusal",
    "refusal changed pool count",
    "refusal changed pool identity/order",
    "missing dungeon-name accessor",
    "missing asset accessor",
    "missing rarity accessor",
    "MuseumInteriorFlow\", 65",
    "MuseumInteriorFlow\", 0",
    "null, artGallery",
    "artGallery, null",
):
    require(literal in tests, "Required AGDIAG1 pure negative test missing: " + literal)

require("Exactly one Harmony surface exists" in safety, "Patch Safety Review surface count missing")
require("LLL remains owner" in safety, "Patch Safety Review LLL ownership boundary missing")
require("DIAGNOSTIC ONLY / NEVER ACCEPT" in safety, "Patch Safety Review diagnostic boundary missing")
require("PR VALIDATION PENDING" in checkpoint, "Canonical checkpoint must not pre-claim CI success")
require("PR validation pending" in findings, "Source findings must preserve pending-validation status")

require("profile_builder.py" not in workflow, "Source-only CI must not invoke the Gale profile builder")
require("dotnet run --project Patches/S142AKAGDiag1/Tests/Policy.Tests.csproj -c Release" in workflow,
        "Pure policy test command missing")
require("dotnet build S142AKAGDiag1.csproj -c Release" in workflow,
        "Plugin source compile command missing")
require("python AnalysisTools/validate_s142ak_agdiag1_source.py" in workflow,
        "Static validator command missing")

report = {
    "status": "SOURCE_PURE_STATIC_CONTRACT_READY_FOR_PR_VALIDATION",
    "candidate_id": "S1.42AK-AGDIAG1",
    "diagnostic_only": True,
    "harmony_surfaces": 1,
    "selection_target": "Offense / Art Gallery / MuseumInteriorFlow / rarity 100",
    "parent_profile_sha256": BMDS_PROFILE_SHA,
    "current_build_controller_enabled": current_build["enabled"],
    "runtime_active_build": active_build,
    "profile_builder_invoked_by_source_ci": False,
    "qualification": "Source compile/pure-policy/static validation only; no review profile, publication, Gale activation, runtime qualification or acceptance."
}
print(json.dumps(report, indent=2))
