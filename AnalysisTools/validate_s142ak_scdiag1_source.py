#!/usr/bin/env python3
"""Fail-closed S1.42AK-SCDIAG1 source-only and live-controller consistency gate."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    file = ROOT / path
    if not file.is_file():
        raise RuntimeError("SCDIAG1 missing required file: " + path)
    return file.read_text(encoding="utf-8")

def require(condition, explanation):
    if not condition:
        raise RuntimeError("SCDIAG1 source/static guard: " + explanation)

root = "Patches/S142AKSCDiag1/"
plugin = read(root + "Plugin.cs")
policy = read(root + "SelectionPolicy.cs")
tests = read(root + "Tests/Program.cs")
project = read(root + "S142AKSCDiag1.csproj")
test_project = read(root + "Tests/Policy.Tests.csproj")
safety = read(root + "PATCH_SAFETY_REVIEW.md")
workflow = read(".github/workflows/s142ak-scdiag1-source-static.yml")
findings = read("SourceEvidence/UniversalInteriorViability/SCDIAG1SourceStatic/FINDINGS.md")
checkpoint = read("Current/343_S1.42AK_PHASE_C_STORAGE_COMPLEX_SCDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md")
authority = read("Current/342_S1.42AK_PHASE_C_STORAGE_COMPLEX_SCDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md")
state = json.loads(read("Current/CURRENT_STATE.json"))
build = json.loads(read("BuildSpecs/current.json"))
active = read("RuntimeInbox/ACTIVE_BUILD.txt").strip()

require(state["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline changed")
require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "active gameplay candidate changed")
require(state["runtime_test_outstanding"] is True, "passive Black Mesa runtime gate changed")
p = state["selected_scope"]["phase_c"]
require(p["storage_complex_selector_source_implementation_authorized"] is True, "source authorization absent")
require(p["storage_complex_scdiag1_implemented"] is True, "source implementation not recorded")
require(p["storage_complex_scdiag1_built"] is False, "profile construction incorrectly claimed")
runtime_stage = p["storage_complex_scdiag1_runtime_armed"] is True
if runtime_stage:
    require(p["storage_complex_runtime_test_authorized"] is True, "runtime stage not authorized")
    require(p["storage_complex_scdiag1_runtime_activation"] == "Current/355_S1.42AK_SCDIAG1_RUNTIME_ACTIVATION.md",
            "wrong exact diagnostic activation record")
    require(p["storage_complex_scdiag1_profile_index_status"] ==
            "PROFILE_INDEX_GREEN_CANONICALLY_INDEXED_RUNTIME_INACTIVE", "published/indexed source gate missing")
    diag = state["selected_scope"]["diagnostic_revision"]
    require(diag["build_id"] == "S1.42AK-SCDIAG1" and
            diag["status"] == "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED" and
            diag["classification"] == "DIAGNOSTIC_ONLY_NEVER_ACCEPT" and
            diag["runtime_armed"] is True, "diagnostic stage/identity drift")
    require(diag["sha256"] == "6be6865a7fde205280439503680ac910401c20b997f757ffbedbddc963c704f4" and
            diag["base_sha256"] == "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0",
            "exact reviewed diagnostic/parent hash drift")
    require(diag["build_result"] == "BuildSpecs/S1.42AK-SCDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json",
            "runtime-routing build metadata missing")
    metadata = json.loads(read(diag["build_result"]))
    require(metadata["build_id"] == diag["build_id"] and
            metadata["output_profile"] == diag["profile"] and
            metadata["output_sha256"] == diag["sha256"] and
            metadata["base_profile"] == diag["base_profile"] and
            metadata["base_sha256"] == diag["base_sha256"], "direct Gale routing mismatch")
else:
    require(p["storage_complex_scdiag1_runtime_armed"] is False and
            p["storage_complex_runtime_test_authorized"] is False,
            "unauthorized source-stage runtime mutation")
# Stage-aware: a PR-local implementation must not pre-claim validation, but once
# the exact PR-head and permanent main-head CI have succeeded, canonical state
# must retain the independently verified evidence rather than remain pending.
if p["storage_complex_scdiag1_source_static_validated"] is True:
    require(p["storage_complex_scdiag1_source_static_validation_pending"] is False,
            "integrated source cannot be both verified and pending")
    require(p["storage_complex_scdiag1_source_pr"] == 372, "wrong original source PR")
    require(p["storage_complex_scdiag1_source_pr_final_head"] ==
            "973b8648644bcfc9fb42ff4943b3ca38b5d82a5e",
            "source validation must pin exact final PR head")
    require(p["storage_complex_scdiag1_source_static_run"] == 37843419333 and
            p["storage_complex_scdiag1_source_knowledge_architecture_run"] == 37843419371,
            "original exact-head CI evidence mismatch")
    require(p["storage_complex_scdiag1_source_main_integration_commit"] ==
            "3f69dac8b09844bc3112122675580bc0e33ee679" and
            p["storage_complex_scdiag1_source_main_knowledge_architecture_run"] == 37845920307,
            "permanent exact-main-head CI integration evidence mismatch")
    require(p["storage_complex_scdiag1_source_integration_reconciliation"] ==
            "Current/344_S1.42AK_SCDIAG1_SOURCE_STATIC_POST_MERGE_RECONCILIATION.md",
            "integrated source reconciliation reference missing")
else:
    require(p["storage_complex_scdiag1_source_static_validated"] is False and
            p["storage_complex_scdiag1_source_static_validation_pending"] is True,
            "staged source must remain CI pending and not pre-claim PASS")
require(p["storage_complex_scdiag1_source_checkpoint"] ==
        "Current/343_S1.42AK_PHASE_C_STORAGE_COMPLEX_SCDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md",
        "checkpoint routing mismatch")
require(p["storage_complex_scdiag1_implementation_findings"] ==
        "SourceEvidence/UniversalInteriorViability/SCDIAG1SourceStatic/FINDINGS.md",
        "findings routing mismatch")
for name, value in {
    "storage_complex_scdiag1_build_id": "S1.42AK-SCDIAG1",
    "storage_complex_scdiag1_source_root": "Patches/S142AKSCDiag1/",
    "storage_complex_scdiag1_project": "S142AKSCDiag1",
    "storage_complex_scdiag1_assembly": "S142AKSCDiag1",
    "storage_complex_scdiag1_guid": "tendas.lethalcompany.s142akscdiag1",
    "storage_complex_scdiag1_version": "1.0.0",
    "storage_complex_scdiag1_marker": "[SCDIAG1]",
    "storage_complex_scdiag1_future_short_profile_identity": "LC V1 S1.42AK-SCD1",
    "storage_complex_scdiag1_parent_sha256": "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0",
}.items():
    require(p[name] == value, "frozen independent identity drift: " + name)
# Fail closed across both lifecycle stages. The original no-proof requirement
# remains binding until a single canonical, ingested, exact-byte SCDIAG1 run
# is reconciled, and a completed proof must not reopen runtime authorization.
completed_proof = p["storage_complex_target_generation_status"] == (
    "PASS_DIAGNOSTIC_GENERATED_STORAGECOMPLEX_GENERATION_MATERIALIZATION_PROOF_NATURAL_SELECTION_NOT_PROVEN"
)
if completed_proof:
    require(runtime_stage is False and p["storage_complex_runtime_test_authorized"] is False,
            "completed SCDIAG1 cannot stay armed or authorize another runtime")
    require(p["storage_complex_scdiag1_runtime_status"] ==
            "RUNTIME_COMPLETE_PASS_DIAGNOSTIC_GENERATION_MATERIALIZATION_PROOF_NEVER_ACCEPT",
            "completed proof status/classification drift")
    require(p["storage_complex_scdiag1_runtime_attempts_consumed"] == 1 and
            p["storage_complex_scdiag1_runtime_attempts_authorized"] == 1,
            "exactly one diagnostic attempt must be consumed")
    evidence = "RuntimeEvidence/S1.42AK-SCDIAG1/20261009T093411Z/"
    require(p["storage_complex_scdiag1_runtime_reconciliation"] ==
            "Current/357_S1.42AK_SCDIAG1_STORAGE_COMPLEX_RUNTIME_EVIDENCE_RECONCILIATION.md" and
            p["storage_complex_scdiag1_runtime_evidence"] == evidence and
            p["storage_complex_scdiag1_runtime_index"] == evidence + "INDEX.json",
            "completed proof not bound to canonical reconciliation and evidence")
    index = json.loads(read(evidence + "INDEX.json"))
    expected_hash = "39dfe45721befd6e256a341497100534c45d37868de14dc29ba6a58c08ce207e"
    require(index["build_id"] == "S1.42AK-SCDIAG1" and
            len(index["files"]) == 1 and index["files"][0]["name"] == "LogOutput.log" and
            index["files"][0]["sha256"] == expected_hash and
            p["storage_complex_scdiag1_runtime_log_sha256"] == expected_hash,
            "completed proof has inconsistent exact original log provenance")
    require(p["storage_complex_scdiag1_runtime_proof_status"] ==
            "PASS_DIAGNOSTIC_GENERATED_STORAGE_COMPLEX_STORAGECOMPLEX_GENERATION_MATERIALIZATION" and
            p["storage_complex_scdiag1_runtime_seed"] == 75941614 and
            p["storage_complex_scdiag1_runtime_pathfinding_logical_connections"] == 4 and
            p["storage_complex_scdiag1_runtime_refused_to_arm_count"] == 0 and
            p["storage_complex_scdiag1_runtime_selection_refusal_count"] == 0 and
            p["storage_complex_scdiag1_runtime_bmdsfix1_applied_count"] == 0,
            "completed proof witness markers incomplete or invalid")
    require(p["residual_no_trusted_actual_generation_proof"] == 22 and
            p["residual_viable_equal_100"] == 10 and
            p["residual_owner_hard_block"] == 12,
            "reconciled proof-gap count mismatch")
    require(state["selected_scope"]["diagnostic_revision"]["runtime_armed"] is False,
            "completed diagnostic still armed in canonical state")
else:
    require(p["storage_complex_target_generation_status"] == "STILL_NO_TRUSTED_ACTUAL_GENERATION_PROOF",
            "unearned Storage Complex generation proof")
require(build["enabled"] is False and build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "live build controller armed")
require(build["base_sha256"] == "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0",
        "guarded parent hash changed")
require(build["local_plugin_builds"] == [] and build["config_patches"] == [] and
        build["mod_additions"] == [] and build["mod_removals"] == [],
        "build controller injected changes")
require(active == ("S1.42AK-SCDIAG1" if runtime_stage else "S1.42AK-BMDSFIX1") and
        state["controllers"]["runtime_active_build"] == active,
        "runtime pointer is inconsistent with exact frozen lifecycle stage")
require("DIAGNOSTIC ONLY / NEVER ACCEPT" in authority, "authorization class absent")
for literal in (
    "namespace S142AKSCDiag1", "tendas.lethalcompany.s142akscdiag1",
    "S1.42AK-SCDIAG1 Deterministic Storage Complex Selector",
    'PluginVersion = "1.0.0"', "imabatby.lethallevelloader", "1.7.12",
    "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
    "tendas.lethalcompany.s142abinteriorweightnormalization",
    "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
    "GetValidExtendedDungeonFlows", "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText", "NumberlessPlanetName",
    "after = new[] { NormalizerGuid }", "priority = Priority.Last",
    "diagnostic.priority == Priority.Last",
    "prior.Postfixes.Count(p => p.owner == NormalizerGuid) == 1",
    "GetMethodBody() != null", "[SCDIAG1] ARMED", "[SCDIAG1] REFUSED TO ARM",
    "[SCDIAG1] REFUSED selection", "[SCDIAG1] SELECTED Offense Storage Complex / StorageComplex",
    "pool[index]", "pool.Clear();", "pool.Add(selected);",
    "_harmony?.UnpatchSelf()", "FindStorageComplex",
):
    require(literal in plugin, "missing plugin contract: " + literal)
require(plugin.count("_harmony.Patch(") == 1, "exactly one Harmony patch allowed")
require(plugin.count("private static void SelectionPostfix(") == 1, "exactly one selection postfix allowed")
require('BepInPlugin(PluginGuid, PluginName, PluginVersion)' in plugin, "BepInEx identity contract missing")
# Exclude literals and comments for executable forbidden-surface checks.
code = re.sub(r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|"(\\.|[^"\\])*"', "", plugin, flags=re.S)
for banned in (
    "PatchAll(", "prefix:", "transpiler:", ".SetValue(", "EntranceTeleport", "TeleportPlayer",
    "CullFactory", "NavMesh", "PathfindingLib", "GetClampedDungeonSize",
    "RoundManager", "UnityEngine.Random", "System.Random", "RegisterExtendedDungeonFlow",
    "BepInEx/config", "BrutalCompany", "BCMER"
):
    require(banned not in code, "forbidden executable surface: " + banned)
for literal in (
    "FindStorageComplex", 'moon, "Offense"', "StringComparison.Ordinal",
    '"Storage Complex"', '"StorageComplex"', "nameMatches != assetMatches",
    "pool.IsReadOnly || pool.IsFixedSize", "object.ReferenceEquals(pool[j], entry)",
    "new HashSet<string>(StringComparer.Ordinal)", "!names.Add(name) || !assets.Add(asset)",
    "effectiveRarity <= 0", "effectiveRarity != 100", "return selected;"
):
    require(literal in policy, "pure fail-closed contract absent: " + literal)
for literal in (
    "selected index must retain existing wrapper identity", "expected fail-closed refusal",
    "refusal changed pool count", "refusal changed pool identity/order",
    "terminal simulation must remain normal", "non-Offense moon must remain normal",
    "ArrayList.ReadOnly", "ArrayList.FixedSize", "repeated decisions mutated pools",
    "missing dungeon-name accessor", "missing asset accessor", "missing rarity accessor"
):
    require(literal in tests, "missing pure test: " + literal)
require('AssemblyName>S142AKSCDiag1<' in project and
        'RootNamespace>S142AKSCDiag1<' in project, "assembly identity mismatch")
require('Compile Include="../SelectionPolicy.cs"' in test_project, "pure tests do not compile real source policy")
require("Exactly one Harmony surface exists" in safety and "LLL remains owner" in safety,
        "mandatory patch safety review incomplete")
require("SOURCE / PURE-STATIC" in findings and "SOURCE / PURE-STATIC" in checkpoint,
        "source implementation checkpoint evidence absent")
require("ref: ${{ github.event.pull_request.head.sha }}" in workflow,
        "GitHub workflow must checkout exact PR head")
require("dotnet run --project Patches/S142AKSCDiag1/Tests/Policy.Tests.csproj -c Release" in workflow,
        "pure-policy CI step missing")
require("dotnet build S142AKSCDiag1.csproj -c Release" in workflow,
        "source compile CI step missing")
require("python AnalysisTools/validate_s142ak_scdiag1_source.py" in workflow,
        "dedicated validator CI step missing")
require("profile_builder.py" not in workflow and "profile-build" not in workflow,
        "forbidden runtime profile build")
print(json.dumps({"status": "SCDIAG1_SOURCE_CONTRACT_PASS",
                  "patch_surfaces": 1, "target": "Offense / Storage Complex / StorageComplex / 100",
                  "pure_tests_and_source_compile": "dedicated PR workflow gates",
                  "profile_build_authorized": False, "runtime_authorized": False,
                  "active_runtime_pointer": active}, indent=2))
