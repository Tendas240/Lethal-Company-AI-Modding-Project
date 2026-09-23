#!/usr/bin/env python3
"""C3F17.3 source-only contract gate. It must never build or arm a Gale profile."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "Patches/S142AKBMGHDiag1/Plugin.cs"
SELECTION = ROOT / "Patches/S142AKBMGHDiag1/SelectionPolicy.cs"
OBSERVATION = ROOT / "Patches/S142AKBMGHDiag1/ObservationPolicy.cs"
WORKFLOW = ROOT / ".github/workflows/s142ak-bmghdiag1-source-static.yml"
PLAN = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG1_PLAN.md"
CONTRACT = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F17/CANDIDATE_CONTRACT.json"
BUILD_REQUEST = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG1.json"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


plugin = PLUGIN.read_text(encoding="utf-8")
selection = SELECTION.read_text(encoding="utf-8")
observation = OBSERVATION.read_text(encoding="utf-8")
workflow = WORKFLOW.read_text(encoding="utf-8")
plan = PLAN.read_text(encoding="utf-8")
contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

require(contract["proposed_candidate_id"] == "S1.42AK-BMGHDIAG1", "Candidate contract ID drift")
require(contract["lifecycle"]["candidate_built"] is False, "Contract unexpectedly claims built candidate")
require(contract["lifecycle"]["candidate_armed"] is False, "Contract unexpectedly claims armed candidate")
require(contract["lifecycle"]["runtime_test_authorized"] is False, "Contract unexpectedly authorizes runtime")
require(not BUILD_REQUEST.exists(), "C3F17.3 must not author a Gale candidate build request")

for literal in (
    "GetValidExtendedDungeonFlows",
    "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText",
    "NumberlessPlanetName",
    "Black Mesa",
    "GreenhouseFlow",
    "TeleportPlayer",
    "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
    "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
    "5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731",
    "[BMGHDIAG1] ARMED",
    "[BMGHDIAG1] SELECTED",
    "[BMGHDIAG1] TRAVERSED",
    "[BMGHDIAG1] TOPOLOGY_OK",
    "[BMGHDIAG1] TOPOLOGY_INCONCLUSIVE",
    "[BMGHDIAG1] REFUSED TO ARM",
    "[BMGHDIAG1] REFUSED selection",
):
    require(literal in plugin, "Missing runtime contract literal: " + literal)

require(plugin.count("harmony.Patch(") == 2, "Plugin must install exactly two Harmony patch surfaces")
require("after = new[] { NormalizerGuid }" in plugin and "priority = Priority.Last" in plugin,
        "Selection patch ordering contract missing")
require(".SetValue(" not in plugin, "Observer/selection implementation must not reflection-write game/mod fields")
require("PatchAll(" not in plugin, "Broad Harmony PatchAll is forbidden")
require("prefix:" not in plugin.lower(), "Prefix patching is forbidden")
require("transpiler:" not in plugin.lower(), "Transpiler patching is forbidden")
require(".FindExitPoint(" not in plugin, "Observer must not manually invoke FindExitPoint")
require(".TeleportPlayer(" not in plugin, "Observer must not manually invoke TeleportPlayer")
require("FindObjectsOfType" in plugin and "topologySnapshotDone" in plugin,
        "One-time typed topology observation surface missing")

for literal in ("Black Mesa", "Greenhouse", "GreenhouseFlow", "Duplicate viable Greenhouse", "normalized rarity 100"):
    require(literal in selection, "Selection policy contract missing: " + literal)
for literal in ("TraversalDecision", "OutOfScope", "MissingPair", "InvalidPair", "Valid", "CheckTopology", "outside>inside", "inside>outside"):
    require(literal in observation, "Observation policy contract missing: " + literal)

require("profile_builder.py" not in workflow, "Source-only CI must not invoke the Gale profile builder")
require("S1.42AK-BMGHDIAG1.json" not in workflow, "Source-only CI must not consume a candidate build request")
require("dotnet run --project Patches/S142AKBMGHDiag1/Tests/Policy.Tests.csproj" in workflow,
        "Pure policy test command missing")
require("dotnet build S142AKBMGHDiag1.csproj -c Release" in workflow,
        "Plugin compile command missing")
require("NOT BUILT" in plan and "NOT ARMED" in plan, "Human contract lifecycle boundary drift")

report = {
    "status": "SOURCE_STATIC_CONTRACT_PASS_NOT_BUILT_NOT_ARMED",
    "candidate_id": "S1.42AK-BMGHDIAG1",
    "harmony_surfaces": 2,
    "gameplay_mutating_surfaces": 1,
    "observation_surfaces": 1,
    "candidate_build_request_present": False,
    "profile_builder_invoked_by_source_ci": False,
    "qualification": "Source/compile/pure-policy validation only. No Gale candidate, runtime arming or gameplay evidence is produced."
}
print(json.dumps(report, indent=2))
