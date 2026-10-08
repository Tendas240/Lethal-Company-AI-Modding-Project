#!/usr/bin/env python3
"""Check FXDIAG1 source-only identity, one-postfix boundary, and live controllers."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return (ROOT / path).read_text(encoding="utf-8")
def require(ok, why):
    if not ok:
        raise RuntimeError(why)

plugin = read("Patches/S142AKFXDiag1/Plugin.cs")
policy = read("Patches/S142AKFXDiag1/SelectionPolicy.cs")
tests = read("Patches/S142AKFXDiag1/Tests/Program.cs")
project = read("Patches/S142AKFXDiag1/S142AKFXDiag1.csproj")
safety = read("Patches/S142AKFXDiag1/PATCH_SAFETY_REVIEW.md")
workflow = read(".github/workflows/s142ak-fxdiag1-source-static.yml")
findings = read("SourceEvidence/UniversalInteriorViability/FXDIAG1SourceStatic/FINDINGS.md")
checkpoint = read("Current/328_S1.42AK_PHASE_C_FRACTURED_COMPLEX_FXDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md")
state = json.loads(read("Current/CURRENT_STATE.json"))
build = json.loads(read("BuildSpecs/current.json"))
active = read("RuntimeInbox/ACTIVE_BUILD.txt").strip()

require(state["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline drift")
require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "active candidate drift")
require(state["runtime_test_outstanding"] is True, "passive BMDSFIX1 gate drift")
phase = state["selected_scope"]["phase_c"]
require(phase["fractured_complex_fxdiag1_implemented"] is True, "source checkpoint marker missing")
require(phase["fractured_complex_fxdiag1_built"] is False, "source checkpoint cannot build a profile")
require(phase["fractured_complex_fxdiag1_runtime_authorized"] is False, "runtime not authorized")
require(phase["fractured_complex_fxdiag1_source_static_validation_pending"] is False, "reviewed source static CI must be reconciled")
require(phase["fractured_complex_fxdiag1_source_static_validated"] is True, "reviewed source static PASS missing")
require(phase["fractured_complex_fxdiag1_source_pr"] == 354, "source PR authority drift")
require(phase["fractured_complex_fxdiag1_source_validated_head"] == "ccba2a774dcb99e2b3f88a2c1ed595af12627d31", "source reviewed head drift")
require(phase["fractured_complex_fxdiag1_source_static_run"] == 37784693536, "dedicated source run drift")
require(phase["fractured_complex_fxdiag1_source_knowledge_architecture_run"] == 37784693474, "knowledge architecture run drift")
require(build["enabled"] is False and build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "live build changed")
require(build["base_sha256"] == "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0", "parent drift")
require(build["local_plugin_builds"] == [] and build["mod_additions"] == [] and build["config_patches"] == [], "live builder change")
require(active == "S1.42AK-BMDSFIX1", "runtime pointer drift")
require(not (ROOT / "Profiles/LC V1 S1.42AK-FXD1.r2z").exists(), "profile must not exist")

for word in (
    "S142AKFXDiag1", "tendas.lethalcompany.s142akfxdiag1",
    "S1.42AK-FXDIAG1 Deterministic Fractured Complex Selector",
    'PluginVersion = "1.0.0"', "imabatby.lethallevelloader", "1.7.12",
    "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
    "tendas.lethalcompany.s142abinteriorweightnormalization",
    "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
    "GetValidExtendedDungeonFlows", "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText", "NumberlessPlanetName",
    "Fractured Complex", "FracturedComplexFlow",
    "after = new[] { NormalizerGuid }", "priority = Priority.Last",
    "diagnostic.priority == Priority.Last", "[FXDIAG1] ARMED",
    "[FXDIAG1] SELECTED Offense Fractured Complex / FracturedComplexFlow",
    "[FXDIAG1] REFUSED TO ARM", "[FXDIAG1] REFUSED selection",
    "pool.Clear();", "pool.Add(selected);", "pool[index]",
    "prior.Postfixes.Count(p => p.owner == NormalizerGuid) == 1",
):
    require(word in plugin, "missing plugin literal: " + word)
require(plugin.count("_harmony.Patch(") == 1, "one Harmony patch required")
require("_harmony?.UnpatchSelf()" in plugin, "startup own patch cleanup missing")
require("GetMethodBody() != null" in plugin, "target/caller body validation missing")
# Remove comments and strings before forbidden executable symbol checks.
code = re.sub(r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"', "", plugin, flags=re.S)
for banned in (
    "PatchAll(", "prefix:", "transpiler:", ".SetValue(", "EntranceTeleport", "TeleportPlayer",
    "CullFactory", "NavMesh", "PathfindingLib", "GetClampedDungeonSize", "RoundManager",
    "UnityEngine.Random", "System.Random", "RegisterExtendedDungeonFlow", "BepInEx/config",
    "BrutalCompany", "BCMER",
):
    require(banned not in code, "forbidden patch surface: " + banned)
require("[BMDSFIX1] APPLIED" not in plugin, "cannot emit BMDSFIX1 marker")
for word in (
    "FindFracturedComplex", 'moon, "Offense"', "StringComparison.Ordinal",
    '"Fractured Complex"', '"FracturedComplexFlow"', "nameMatches != assetMatches",
    "Duplicate viable Fractured Complex entries", "rarity(entry) != 100",
    "if (entry == null)", "string.IsNullOrEmpty(name)", "return selected;",
):
    require(word in policy, "missing pure guard: " + word)
for word in (
    "selected index must retain existing wrapper identity", "debugResults=false must remain normal",
    "terminal simulation must remain normal", "expected fail-closed refusal",
    "refusal changed pool count", "refusal changed pool identity/order",
    "missing dungeon-name accessor", "missing asset accessor", "missing rarity accessor",
    'new Entry("Other Dungeon", "FracturedComplexFlow", 100)',
    'new Entry("Fractured Complex", "WrongFlow", 100)',
    'new Entry("Other Dungeon", null, 100)', 'new Entry(null, "OtherFlow", 100)',
):
    require(word in tests, "missing regression case: " + word)
m = re.search(r"<RestoreAdditionalProjectSources>\s*(.*?)\s*</RestoreAdditionalProjectSources>", project, re.S)
require(m is not None and [x.strip() for x in m.group(1).split(";")] ==
    ["https://api.nuget.org/v3/index.json", "https://nuget.bepinex.dev/v3/index.json"], "restore feed drift")
require("Exactly one Harmony surface exists" in safety and "LLL remains owner" in safety, "Patch Safety Review incomplete")
require("SOURCE / PURE-STATIC PASS" in findings and "SOURCE / PURE-STATIC PASS" in checkpoint, "reviewed source CI evidence missing")
for evidence in ("ccba2a774dcb99e2b3f88a2c1ed595af12627d31", "37784693536", "37784693474"):
    require(evidence in findings and evidence in checkpoint, "exact reviewed-head CI evidence missing: " + evidence)
require("LC V1 S1.42AK-FXD1" in findings and "LC V1 S1.42AK-FXD1" in checkpoint, "short identity drift")
require("profile_builder.py" not in workflow, "profile builder forbidden")
require("ref: ${{ github.event.pull_request.head.sha }}" in workflow, "CI must pin PR head")
require("dotnet run --project Patches/S142AKFXDiag1/Tests/Policy.Tests.csproj -c Release" in workflow, "pure test missing")
require("dotnet build S142AKFXDiag1.csproj -c Release" in workflow, "compile gate missing")
require("python AnalysisTools/validate_s142ak_fxdiag1_source.py" in workflow, "validator missing")
print(json.dumps({"status":"FXDIAG1_SOURCE_STATIC_CONTRACT_PASS_REVIEWED_PR_HEAD_GREEN",
    "harmony_surfaces":1,"target":"Offense / FracturedComplexFlow / rarity 100",
    "profile_build_authorized":False,"runtime_authorized":False,"active":active}, indent=2))
