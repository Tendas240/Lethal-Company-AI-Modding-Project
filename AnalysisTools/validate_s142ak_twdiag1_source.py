#!/usr/bin/env python3
"""Validate the staged S1.42AK-TWDIAG1 source-only fail-closed selector contract."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "Patches/S142AKTWDiag1"
plugin = (PATCH / "Plugin.cs").read_text(encoding="utf-8")
policy = (PATCH / "SelectionPolicy.cs").read_text(encoding="utf-8")
tests = (PATCH / "Tests/Program.cs").read_text(encoding="utf-8")
project = (PATCH / "S142AKTWDiag1.csproj").read_text(encoding="utf-8")
safety = (PATCH / "PATCH_SAFETY_REVIEW.md").read_text(encoding="utf-8")
workflow = (ROOT / ".github/workflows/s142ak-twdiag1-source-static.yml").read_text(encoding="utf-8")
findings = (ROOT / "SourceEvidence/UniversalInteriorViability/TWDIAG1SourceStatic/FINDINGS.md").read_text(encoding="utf-8")
checkpoint = (ROOT / "Current/303_S1.42AK_PHASE_C_TOWER_TWDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md").read_text(encoding="utf-8")
state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text(encoding="utf-8"))
build = json.loads((ROOT / "BuildSpecs/current.json").read_text(encoding="utf-8"))
active = (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()

def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)

require(build["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "build controller drift")
require(build["base_sha256"] == "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0", "parent SHA drift")
require(build["local_plugin_builds"] == [], "source stage must not arm a plugin build")
require(active == "S1.42AK-BMDSFIX1", "runtime pointer drift")
require(state["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline drift")
require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "active candidate drift")
require(state["runtime_test_outstanding"] is True, "BMDSFIX1 runtime gate must remain outstanding")

phase = state["selected_scope"]["phase_c"]
require(phase["tower_twdiag1_implemented"] is True, "TWDIAG1 source must be staged")
require(phase["tower_twdiag1_built"] is False, "TWDIAG1 must remain unbuilt")
require(phase["tower_twdiag1_runtime_authorized"] is False, "TWDIAG1 runtime must remain unauthorized")
require(phase["tower_twdiag1_source_static_validation_pending"] is True, "staged validation pending flag missing")
require(phase["tower_twdiag1_source_static_validated"] is False, "staged source must not claim validated")

m = re.search(r"<RestoreAdditionalProjectSources>\s*(.*?)\s*</RestoreAdditionalProjectSources>", project, re.S)
require(m is not None, "restore sources missing")
feeds = [x.strip() for x in m.group(1).split(";") if x.strip()]
require(feeds == ["https://api.nuget.org/v3/index.json", "https://nuget.bepinex.dev/v3/index.json"], "restore sources drift")

for literal in (
    "tendas.lethalcompany.s142aktwdiag1",
    "S1.42AK-TWDIAG1 Deterministic Tower Selector",
    "imabatby.lethallevelloader",
    "tendas.lethalcompany.s142abinteriorweightnormalization",
    "1.7.12",
    "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
    "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
    "GetValidExtendedDungeonFlows",
    "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText",
    "NumberlessPlanetName",
    "Offense",
    "Tower",
    "TowerFlow",
    "after = new[] { NormalizerGuid }",
    "priority = Priority.Last",
    "diagnostic.priority == Priority.Last",
    "[TWDIAG1] ARMED",
    "[TWDIAG1] SELECTED Offense Tower / TowerFlow",
    "[TWDIAG1] REFUSED TO ARM; normal behavior preserved",
    "[TWDIAG1] REFUSED selection; normal viable pool preserved",
):
    require(literal in plugin, "missing plugin contract literal: " + literal)

require(plugin.count("_harmony.Patch(") == 1, "exactly one Harmony patch required")
code = re.sub(r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"', "", plugin, flags=re.S)
for forbidden in (
    "PatchAll(", "prefix:", "transpiler:", ".SetValue(",
    "EntranceTeleport", "TeleportPlayer", "CullFactory", "NavMesh", "PathfindingLib",
    "GetClampedDungeonSize", "RoundManager", "UnityEngine.Random", "System.Random",
    "RegisterExtendedDungeonFlow", "BepInEx/config", "BrutalCompany", "BCMER",
):
    require(forbidden not in code, "forbidden code surface: " + forbidden)
require("[BMDSFIX1] APPLIED" not in plugin, "must not emit BMDSFIX1 APPLIED")

for literal in (
    "FindTower", "Duplicate viable Tower entries",
    "Tower not returned as viable", "Tower flow asset mismatch",
    "accepted normalized rarity 100", "Null viable wrapper",
    "Unrecognized Offense debug-results caller",
):
    require(literal in policy, "missing policy contract: " + literal)

for literal in (
    "exact Tower target index", "selected index must retain existing wrapper identity",
    "debugResults=false must remain normal", "non-Offense moon must remain normal",
    "terminal simulation must remain normal", "expected fail-closed refusal",
    "refusal changed pool count", "refusal changed pool identity/order",
    "missing dungeon-name accessor", "missing asset accessor", "missing rarity accessor",
    'TowerFlow", 65', 'TowerFlow", 0', "null, storehouse", "storehouse, null",
):
    require(literal in tests, "missing pure test: " + literal)

require("Exactly one Harmony surface exists" in safety, "safety review surface count missing")
require("LLL remains owner" in safety, "safety review ownership boundary missing")
require("DIAGNOSTIC ONLY / NEVER ACCEPT" in safety, "diagnostic-only boundary missing")
require("SOURCE / PURE-STATIC STAGED" in checkpoint and "VALIDATION PENDING" in checkpoint, "checkpoint staged state missing")
require("SOURCE / PURE-STATIC STAGED" in findings and "VALIDATION PENDING" in findings, "findings staged state missing")
require("profile_builder.py" not in workflow, "source workflow must not build a Gale profile")
require("ref: ${{ github.event.pull_request.head.sha }}" in workflow, "workflow must checkout exact PR head")
require("dotnet run --project Patches/S142AKTWDiag1/Tests/Policy.Tests.csproj -c Release" in workflow, "pure test command missing")
require("dotnet build S142AKTWDiag1.csproj -c Release" in workflow, "compile command missing")
require("python AnalysisTools/validate_s142ak_twdiag1_source.py" in workflow, "validator command missing")

print(json.dumps({
    "status": "SOURCE_PURE_STATIC_STAGED_VALIDATION_PENDING_NOT_BUILT_NOT_ARMED",
    "candidate_id": "S1.42AK-TWDIAG1",
    "harmony_surfaces": 1,
    "selection_target": "Offense / Tower / TowerFlow / rarity 100",
    "runtime_active_build": active,
    "profile_builder_invoked": False
}, indent=2))
