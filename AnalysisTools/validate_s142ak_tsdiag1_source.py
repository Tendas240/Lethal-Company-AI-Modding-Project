#!/usr/bin/env python3
"""TSDIAG1 source-only fail-closed patch and controller contract."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    p = ROOT / path
    if not p.is_file():
        raise RuntimeError("TSDIAG1 required file absent: " + path)
    return p.read_text(encoding="utf-8")

def require(ok, reason):
    if not ok:
        raise RuntimeError("TSDIAG1 source contract: " + reason)

root = "Patches/S142AKTSDiag1/"
plugin = read(root + "Plugin.cs")
policy = read(root + "SelectionPolicy.cs")
tests = read(root + "Tests/Program.cs")
project = read(root + "S142AKTSDiag1.csproj")
test_project = read(root + "Tests/Policy.Tests.csproj")
safety = read(root + "PATCH_SAFETY_REVIEW.md")
workflow = read(".github/workflows/s142ak-tsdiag1-source-static.yml")
checkpoint = read("Current/361_S1.42AK_PHASE_C_TOY_STORE_TSDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md")
findings = read("SourceEvidence/UniversalInteriorViability/TSDIAG1SourceStatic/FINDINGS.md")
authority = read("Current/360_S1.42AK_PHASE_C_TOY_STORE_TSDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md")
state = json.loads(read("Current/CURRENT_STATE.json"))
build = json.loads(read("BuildSpecs/current.json"))
auto = json.loads(read("Current/AUTO_BUILD_RESULT.json"))
active = read("RuntimeInbox/ACTIVE_BUILD.txt").strip()
p = state["selected_scope"]["phase_c"]

require(state["accepted_baseline"]["build_id"] == "S1.42AK", "baseline changed")
require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1" and
        state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED",
        "active gameplay promotion")
require(state["runtime_test_outstanding"] is True, "independent passive proof waived")
require(p["residual_no_trusted_actual_generation_proof"] == 22 and
        p["residual_viable_equal_100"] == 10 and p["residual_owner_hard_block"] == 12,
        "residual changed without runtime proof")
require(p["toy_store_source_implementation_authorized"] is True and
        p["toy_store_tsdiag1_source_implemented"] is True and
        p["toy_store_tsdiag1_built"] is False and
        p["toy_store_tsdiag1_runtime_armed"] is False and
        p["toy_store_runtime_test_authorized"] is False,
        "source-only stage boundaries")
# Fail closed in both PR-staged and independently exact-CI-validated stages.
if p["toy_store_tsdiag1_source_static_validated"] is True:
    require(p["toy_store_tsdiag1_source_static_validation_pending"] is False,
            "source validated/pending conflict")
    require(p["toy_store_tsdiag1_source_pr"] == 392 and
            p["toy_store_tsdiag1_source_pr_final_head"] ==
            "332bfb2c53d3052e8af15db93b0554722ac0fce9",
            "original PR/head provenance")
    require(p["toy_store_tsdiag1_source_static_run"] == 37922570863 and
            p["toy_store_tsdiag1_source_knowledge_architecture_run"] == 37922570675,
            "original exact-head PR CI provenance")
    require(p["toy_store_tsdiag1_source_main_integration_commit"] ==
            "253873eda94b9e7775c7eb4ca9176ef810f56d00" and
            p["toy_store_tsdiag1_source_main_knowledge_architecture_run"] == 37924201026,
            "exact-main-head permanent push provenance")
    if p.get("toy_store_tsdiag1_review_build_authorized", False):
        recipe_path = "BuildSpecs/S1.42AK-TSDIAG1.json"
        recipe = json.loads(read(recipe_path))
        require(p["toy_store_tsdiag1_review_build_authorization"] ==
                "Current/362_S1.42AK_TSDIAG1_INACTIVE_REVIEW_BUILD_AUTHORIZATION_DECISION.md" and
                p["toy_store_tsdiag1_review_build_recipe"] == recipe_path and
                p["toy_store_tsdiag1_review_build_plan"] ==
                "BuildSpecs/S1.42AK-TSDIAG1_PLAN.md", "review-only decision references")
        require(p["toy_store_tsdiag1_review_build_executed"] is False and
                p["toy_store_tsdiag1_review_build_pass"] is False and
                p["toy_store_tsdiag1_built"] is False, "review output falsely claimed")
        require(recipe["enabled"] is True and recipe["review_only"] is True and
                recipe["build_id"] == "S1.42AK-TSDIAG1" and
                recipe["base_sha256"] == "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0" and
                recipe["output_profile"] == "Profiles/LC V1 S1.42AK-TS1.r2z" and
                recipe["profile_name"] == "LC V1 S1.42AK-TS1" and
                recipe["overwrite"] is False and
                len(recipe["local_plugin_builds"]) == 1 and
                recipe["local_plugin_builds"][0]["archive_path"] ==
                "BepInEx/plugins/S142AKTSDiag1/S142AKTSDiag1.dll" and
                all(recipe[x] == [] for x in
                    ("mod_state_changes", "mod_additions", "mod_removals",
                     "config_patches", "file_injections")), "review recipe boundary")
else:
    require(p["toy_store_tsdiag1_source_static_validated"] is False and
            p["toy_store_tsdiag1_source_static_validation_pending"] is True and
            p.get("toy_store_tsdiag1_review_build_authorized") is not True,
            "staged source cannot claim proof or review authorization")
expected = {
    "toy_store_tsdiag1_build_id": "S1.42AK-TSDIAG1",
    "toy_store_tsdiag1_source_root": root,
    "toy_store_tsdiag1_project": "S142AKTSDiag1",
    "toy_store_tsdiag1_assembly": "S142AKTSDiag1",
    "toy_store_tsdiag1_guid": "tendas.lethalcompany.s142aktsdiag1",
    "toy_store_tsdiag1_version": "1.0.0",
    "toy_store_tsdiag1_marker": "[TSDIAG1]",
    "toy_store_tsdiag1_future_short_profile_identity": "LC V1 S1.42AK-TS1",
    "toy_store_tsdiag1_parent_sha256":
        "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0",
}
for key, value in expected.items():
    require(p[key] == value, "frozen identity: " + key)
require(p["toy_store_tsdiag1_source_checkpoint"] ==
        "Current/361_S1.42AK_PHASE_C_TOY_STORE_TSDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md" and
        p["toy_store_tsdiag1_implementation_findings"] ==
        "SourceEvidence/UniversalInteriorViability/TSDIAG1SourceStatic/FINDINGS.md",
        "checkpoint/findings mapping")
require(state["next_action"] == state["selected_scope"]["next_action"] and
        state["next_action"] in read("Current/00_CURRENT_STATE.md"),
        "generated navigation diverged")
require(build["enabled"] is False and
        build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS" and
        build["base_sha256"] == expected["toy_store_tsdiag1_parent_sha256"] and
        all(build[key] == [] for key in
            ("local_plugin_builds", "config_patches", "mod_additions", "mod_removals")),
        "build controller drift")
require(state["controllers"]["runtime_active_build"] == active == "S1.42AK-BMDSFIX1" and
        auto["build_id"] == active, "runtime controller or auto-build drift")
require("DIAGNOSTIC ONLY / NEVER ACCEPT" in authority and
        "SOURCE / PURE-STATIC" in checkpoint and
        "SOURCE / PURE-STATIC" in findings, "stage documentation missing")

for value in (
    "namespace S142AKTSDiag1",
    'PluginGuid = "tendas.lethalcompany.s142aktsdiag1"',
    'PluginVersion = "1.0.0"',
    "S1.42AK-TSDIAG1 Deterministic Toy Store Selector",
    "imabatby.lethallevelloader",
    "tendas.lethalcompany.s142abinteriorweightnormalization",
    "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
    "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
    "GetValidExtendedDungeonFlows", "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText", "NumberlessPlanetName",
    "after = new[] { NormalizerGuid }", "priority = Priority.Last",
    "diagnostic.priority == Priority.Last",
    "prior.Postfixes.Count(p => p.owner == NormalizerGuid) == 1",
    "GetMethodBody() != null", "FindToyStore",
    "[TSDIAG1] ARMED", "[TSDIAG1] REFUSED TO ARM",
    "[TSDIAG1] REFUSED selection",
    "[TSDIAG1] SELECTED Offense Toy Store / ToystoreFlow",
    "pool[index]", "pool.Clear();", "pool.Add(selected);",
    "_harmony?.UnpatchSelf()",
):
    require(value in plugin, "plugin contract: " + value)
require(plugin.count("_harmony.Patch(") == 1 and
        plugin.count("private static void SelectionPostfix(") == 1,
        "exactly one Harmony postfix")
# Ignore comments and strings when excluding prohibited executable surface.
code = re.sub(r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"', "", plugin, flags=re.S)
for banned in ("PatchAll(", "prefix:", "transpiler:", ".SetValue(",
               "EntranceTeleport", "TeleportPlayer", "CullFactory",
               "NavMesh", "PathfindingLib", "GetClampedDungeonSize",
               "RoundManager", "UnityEngine.Random", "System.Random",
               "RegisterExtendedDungeonFlow"):
    require(banned not in code, "forbidden wider source patch: " + banned)
for value in (
    "FindToyStore", 'moon, "Offense"', "StringComparison.Ordinal",
    '"Toy Store"', '"ToystoreFlow"', "nameMatches != assetMatches",
    "effectiveRarity != 100", "effectiveRarity <= 0",
    "pool.IsReadOnly || pool.IsFixedSize",
    "object.ReferenceEquals(pool[j], entry)",
    "new HashSet<string>(StringComparer.Ordinal)",
    "!names.Add(name) || !assets.Add(asset)", "return selected;",
):
    require(value in policy, "pure fail-closed policy: " + value)
for value in ("selected index must retain existing wrapper identity",
              "expected fail-closed refusal", "refusal changed pool count",
              "refusal changed pool identity/order",
              "terminal simulation must remain normal",
              "non-Offense moon must remain normal",
              "ArrayList.ReadOnly", "ArrayList.FixedSize",
              "repeated decisions mutated pools",
              "missing dungeon-name accessor",
              "missing asset accessor", "missing rarity accessor"):
    require(value in tests, "pure regression tests: " + value)
require("<AssemblyName>S142AKTSDiag1</AssemblyName>" in project and
        "<RootNamespace>S142AKTSDiag1</RootNamespace>" in project and
        'Compile Include="../SelectionPolicy.cs"' in test_project,
        "project assembly / pure source linkage")
require("Exactly one Harmony surface exists" in safety and
        "LLL remains owner" in safety, "patch safety review")
require("ref: ${{ github.event.pull_request.head.sha }}" in workflow and
        "dotnet run --project Patches/S142AKTSDiag1/Tests/Policy.Tests.csproj -c Release" in workflow and
        "dotnet build S142AKTSDiag1.csproj -c Release" in workflow and
        "python AnalysisTools/validate_s142ak_tsdiag1_source.py" in workflow,
        "exact-head source-only workflow")
require("profile_builder.py" not in workflow, "profile builder prohibited")
print(json.dumps({"status": "TSDIAG1_SOURCE_STATIC_PASS",
                  "postfix_count": 1, "profile_build": False,
                  "runtime_armed": False, "residual": 22,
                  "active_runtime": active}, indent=2))
