#!/usr/bin/env python3
"""C3F18 BMGHDIAG2 source/static fail-closed contract gate. Never builds or arms a Gale profile."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "Patches/S142AKBMGHDiag2"
PLUGIN = PATCH / "Plugin.cs"
PROVENANCE = PATCH / "GameAssemblyProvenance.cs"
RUNTIME_IDENTITY = PATCH / "RuntimeIdentityPolicy.cs"
SELECTION = PATCH / "SelectionPolicy.cs"
OBSERVATION = PATCH / "ObservationPolicy.cs"
TESTS = PATCH / "Tests/Program.cs"
WORKFLOW = ROOT / ".github/workflows/s142ak-bmghdiag2-source-static.yml"
PLAN = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md"
BUILD_REQUEST = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2.json"
CURRENT_BUILD_REQUEST = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE = ROOT / "Current/CURRENT_STATE.json"
EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"


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
provenance = PROVENANCE.read_text(encoding="utf-8")
runtime_identity = RUNTIME_IDENTITY.read_text(encoding="utf-8")
selection = SELECTION.read_text(encoding="utf-8")
observation = OBSERVATION.read_text(encoding="utf-8")
tests = TESTS.read_text(encoding="utf-8")
workflow = WORKFLOW.read_text(encoding="utf-8")
plan = PLAN.read_text(encoding="utf-8")
current_build = json.loads(CURRENT_BUILD_REQUEST.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE.read_text(encoding="utf-8"))
build_request_present = BUILD_REQUEST.exists()

if build_request_present:
    build_request = json.loads(BUILD_REQUEST.read_text(encoding="utf-8"))
    require(build_request["enabled"] is True, "Separate BMGHDIAG2 review build request must be explicitly enabled")
    require(build_request["build_id"] == "S1.42AK-BMGHDIAG2", "Separate build request ID drift")
    require(build_request["base_profile"] == "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z", "Separate build request base drift")
    require(build_request["base_sha256"] == EXPECTED_BASE_SHA256, "Separate build request base SHA drift")
    require(build_request["output_profile"] == "Profiles/LC V1 S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic.r2z", "Separate build request output drift")
    require(build_request["overwrite"] is False, "Separate review build must not overwrite")
    for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections"):
        require(build_request[field] == [], "Separate review build contains unauthorized " + field)
    require(build_request["local_plugin_builds"] == [{
        "project": "Patches/S142AKBMGHDiag2/S142AKBMGHDiag2.csproj",
        "configuration": "Release",
        "built_file": "Patches/S142AKBMGHDiag2/bin/Release/netstandard2.1/S142AKBMGHDiag2.dll",
        "archive_path": "BepInEx/plugins/S142AKBMGHDiag2/S142AKBMGHDiag2.dll",
    }], "Separate review build local plugin contract drift")

require(current_build["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "BuildSpecs/current.json must remain idle")
require(ACTIVE_BUILD.read_text(encoding="utf-8").strip() == "S1.42AK", "Runtime ACTIVE_BUILD must remain S1.42AK")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(current_state["active_candidate"] is None, "Lifecycle unexpectedly has an active candidate")
require(current_state["runtime_test_outstanding"] is False, "Lifecycle unexpectedly authorizes runtime testing")

for literal in (
    "S1.42AK-BMGHDIAG2",
    "tendas.lethalcompany.s142akbmghdiag2",
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
    "GameAssemblyProvenance.Validate(Paths.ManagedPath, GameAssemblySha)",
    "runtimeAssembly.IsDynamic",
    "runtimeAssembly.ManifestModule.Name",
    "[BMGHDIAG2] ARMED",
    "[BMGHDIAG2] SELECTED",
    "[BMGHDIAG2] TRAVERSED",
    "[BMGHDIAG2] TOPOLOGY_OK",
    "[BMGHDIAG2] TOPOLOGY_INCONCLUSIVE",
    "[BMGHDIAG2] REFUSED TO ARM",
    "[BMGHDIAG2] REFUSED selection",
):
    require(literal in plugin, "Missing successor runtime contract literal: " + literal)

require("[BMGHDIAG1]" not in plugin, "Successor DLL source must not emit predecessor markers")
require(plugin.count("harmony.Patch(") == 2, "Plugin must install exactly two Harmony patch surfaces")
require("after = new[] { NormalizerGuid }" in plugin and "priority = Priority.Last" in plugin,
        "Selection patch ordering contract missing")
require(".SetValue(" not in plugin_code, "Observer/selection implementation must not reflection-write game/mod fields")
require("PatchAll(" not in plugin_code, "Broad Harmony PatchAll is forbidden")
require("prefix:" not in plugin_code.lower(), "Prefix patching is forbidden")
require("transpiler:" not in plugin_code.lower(), "Transpiler patching is forbidden")
require(".FindExitPoint(" not in plugin_code, "Observer must not manually invoke FindExitPoint")
require(".TeleportPlayer(" not in plugin_code, "Observer must not manually invoke TeleportPlayer")
require(plugin.count("assembly.Location") == 1, "Assembly.Location must remain dependency-only and occur exactly once")

observation_match = re.search(r"private static void ResolveObservationContract\(\)\s*\{(?P<body>.*?)\n        \}", plugin, re.DOTALL)
require(observation_match is not None, "ResolveObservationContract method not found")
observation_body = observation_match.group("body")
require(".Location" not in observation_body and "CodeBase" not in observation_body,
        "Loaded game observation contract must not use Assembly.Location/CodeBase")
require("ValidateDependencyAssemblyHash" not in observation_body,
        "Loaded game observation contract must not reuse dependency-file hash logic")

for literal in (
    "Path.Combine(canonicalManagedPath, FileName)",
    "Path.GetFullPath(managedPath)",
    "Directory.Exists(canonicalManagedPath)",
    "File.Exists(assemblyPath)",
    "FileName = \"Assembly-CSharp.dll\"",
):
    require(literal in provenance, "Installed-game provenance contract missing: " + literal)
for forbidden in ("Assembly.Location", "CodeBase", "Directory.GetFiles", "EnumerateFiles", "SearchOption", "Environment.CurrentDirectory"):
    require(forbidden not in provenance, "Forbidden game-binary provenance fallback present: " + forbidden)

for literal in ("EntranceTeleport", "Assembly-CSharp", "Assembly-CSharp.dll", "assemblyIsDynamic", "System.Void"):
    require(literal in runtime_identity, "Runtime identity policy missing: " + literal)
for literal in ("Black Mesa", "Greenhouse", "GreenhouseFlow", "Duplicate viable Greenhouse", "normalized rarity 100"):
    require(literal in selection, "Selection policy contract missing: " + literal)
for literal in ("TraversalDecision", "OutOfScope", "MissingPair", "InvalidPair", "Valid", "CheckTopology", "outside>inside", "inside>outside"):
    require(literal in observation, "Observation policy contract missing: " + literal)
for literal in ("blank managed path", "missing managed directory", "no recursive/fallback assembly search", "wrong installed SHA", "unreadable exact file", "dynamic runtime assembly", "wrong manifest module"):
    require(literal in tests, "Required pure negative test missing: " + literal)

require("profile_builder.py" not in workflow, "Source-only CI must not invoke the Gale profile builder")
require("dotnet run --project Patches/S142AKBMGHDiag2/Tests/Policy.Tests.csproj" in workflow,
        "Pure policy test command missing")
require("dotnet build S142AKBMGHDiag2.csproj -c Release" in workflow,
        "Plugin compile command missing")
require("NOT BUILT" in plan and "NOT ARMED" in plan, "Human plan runtime/build boundary drift")

report = {
    "status": "SOURCE_STATIC_CONTRACT_PASS_NOT_BUILT_NOT_ARMED",
    "candidate_id": "S1.42AK-BMGHDIAG2",
    "harmony_surfaces": 2,
    "gameplay_mutating_surfaces": 1,
    "observation_surfaces": 1,
    "installed_game_provenance_source": "BepInEx Paths.ManagedPath/Assembly-CSharp.dll",
    "loaded_game_assembly_location_used": False,
    "candidate_build_request_present": build_request_present,
    "current_build_controller_enabled": current_build["enabled"],
    "runtime_active_build": ACTIVE_BUILD.read_text(encoding="utf-8").strip(),
    "profile_builder_invoked_by_source_ci": False,
    "qualification": "Source/compile/pure-policy validation only. A separate inactive review-build spec may exist, but this source gate never builds, publishes, arms lifecycle or authorizes runtime."
}
print(json.dumps(report, indent=2))
