#!/usr/bin/env python3
"""BMGHDIAG3 repository-only source/static gate. Never compiles, builds, publishes or arms runtime."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "Patches/S142AKBMGHDiag2"
PATCH = ROOT / "Patches/S142AKBMGHDiag3"
PLUGIN = PATCH / "Plugin.cs"
PROVENANCE = PATCH / "GameAssemblyProvenance.cs"
RUNTIME_IDENTITY = PATCH / "RuntimeIdentityPolicy.cs"
SELECTION = PATCH / "SelectionPolicy.cs"
OBSERVATION = PATCH / "ObservationPolicy.cs"
PROJECT = PATCH / "S142AKBMGHDiag3.csproj"
README = PATCH / "README.md"
NUGET = PATCH / "NuGet.Config"
PLAN = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG3_PLAN.md"
EVIDENCE = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F18_BMGHDIAG3/IMPLEMENTATION_FINDINGS.md"
WORKFLOW = ROOT / ".github/workflows/s142ak-bmghdiag3-source-static.yml"
CURRENT_BUILD = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE = ROOT / "Current/CURRENT_STATE.json"
ROOT_CAUSE = ROOT / "Current/193_S1.42AK_BMGHDIAG2_RUNTIME_IDENTITY_ROOT_CAUSE_RECONCILIATION.md"

EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
EXPECTED_GAME_SHA256 = "5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731"
EXPECTED_LLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
EXPECTED_NORMALIZER_SHA256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    require(path.exists(), "Missing required path: " + str(path.relative_to(ROOT)))
    return path.read_text(encoding="utf-8")


def successor_namespace(text):
    return text.replace("namespace S142AKBMGHDiag2", "namespace S142AKBMGHDiag3")


def strip_csharp_noncode(text):
    pattern = re.compile(
        r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
        re.DOTALL,
    )
    return pattern.sub("", text)


plugin = read(PLUGIN)
plugin_code = strip_csharp_noncode(plugin)
provenance = read(PROVENANCE)
runtime_identity = read(RUNTIME_IDENTITY)
selection = read(SELECTION)
observation = read(OBSERVATION)
project = read(PROJECT)
readme = read(README)
plan = read(PLAN)
evidence = read(EVIDENCE)
workflow = read(WORKFLOW)
root_cause = read(ROOT_CAUSE)
current_build = json.loads(read(CURRENT_BUILD))
current_state = json.loads(read(CURRENT_STATE))
active_build = read(ACTIVE_BUILD).strip()

expected_files = {
    "GameAssemblyProvenance.cs",
    "NuGet.Config",
    "ObservationPolicy.cs",
    "Plugin.cs",
    "README.md",
    "RuntimeIdentityPolicy.cs",
    "S142AKBMGHDiag3.csproj",
    "SelectionPolicy.cs",
}
require({p.name for p in PATCH.iterdir() if p.is_file()} == expected_files,
        "BMGHDIAG3 source directory contains unexpected/missing top-level files")
require(not any(p.is_dir() for p in PATCH.iterdir()),
        "BMGHDIAG3 source/static checkpoint must not contain build/test output or compiled-test directories")

require(current_build["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
        "BuildSpecs/current.json idle scope drift")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD must remain S1.42AK-BMDSFIX1")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(current_state["accepted_baseline"]["sha256"] == EXPECTED_BASE_SHA256, "Accepted baseline SHA drift")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active gameplay candidate drift")
require(current_state["runtime_test_outstanding"] is True,
        "Existing BMDSFIX1 runtime gate must remain outstanding")
require("Current/193_S1.42AK_BMGHDIAG2_RUNTIME_IDENTITY_ROOT_CAUSE_RECONCILIATION.md"
        in current_state["selected_scope"]["finding"], "Root-cause authority lost from selected scope")
require("source/static" in current_state["selected_scope"]["next_action"].lower(),
        "Current next_action no longer authorizes the bounded successor source/static checkpoint")

for name, actual in (
    ("GameAssemblyProvenance.cs", provenance),
    ("SelectionPolicy.cs", selection),
    ("ObservationPolicy.cs", observation),
):
    require(actual == successor_namespace(read(PREDECESSOR / name)),
            name + " drifted beyond successor namespace identity")

predecessor_runtime = successor_namespace(read(PREDECESSOR / "RuntimeIdentityPolicy.cs"))
expected_runtime = predecessor_runtime.replace(
    "            bool assemblyIsDynamic,\n            string manifestModuleName)\n",
    "            bool assemblyIsDynamic)\n",
)
expected_runtime = expected_runtime.replace(
    "            if (manifestModuleName != \"Assembly-CSharp.dll\")\n"
    "                throw new InvalidOperationException(\"EntranceTeleport manifest module identity mismatch.\");\n",
    "",
)
require(expected_runtime != predecessor_runtime, "Approved runtime-identity transformation was not applied")
require(runtime_identity == expected_runtime,
        "RuntimeIdentityPolicy contains delta beyond namespace + approved filename predicate removal")

predecessor_plugin = successor_namespace(read(PREDECESSOR / "Plugin.cs"))
expected_plugin = predecessor_plugin.replace(
    "S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic",
    "S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic",
).replace(
    "tendas.lethalcompany.s142akbmghdiag2",
    "tendas.lethalcompany.s142akbmghdiag3",
).replace(
    "[BMGHDIAG2]",
    "[BMGHDIAG3]",
)
old_call = (
    "            RuntimeIdentityPolicy.ValidateAssemblyIdentity(\n"
    "                entranceTeleportType.FullName,\n"
    "                runtimeAssembly.GetName().Name,\n"
    "                runtimeAssembly.IsDynamic,\n"
    "                runtimeAssembly.ManifestModule.Name);"
)
new_call = (
    "            RuntimeIdentityPolicy.ValidateAssemblyIdentity(\n"
    "                entranceTeleportType.FullName,\n"
    "                runtimeAssembly.GetName().Name,\n"
    "                runtimeAssembly.IsDynamic);"
)
require(old_call in expected_plugin, "Predecessor plugin call-site shape drift")
expected_plugin = expected_plugin.replace(old_call, new_call, 1)
require(plugin == expected_plugin,
        "Plugin.cs contains delta beyond successor identity + approved ManifestModule.Name argument removal")

predecessor_project = read(PREDECESSOR / "S142AKBMGHDiag2.csproj")
expected_project = predecessor_project.replace("S142AKBMGHDiag2", "S142AKBMGHDiag3").replace(
    "    <Compile Remove=\"Tests/**/*.cs\" />\n", ""
)
require(project == expected_project, "Successor project metadata drift")
require(read(NUGET) == read(PREDECESSOR / "NuGet.Config"), "NuGet source policy drift")

for literal in (
    "S1.42AK-BMGHDIAG3",
    "tendas.lethalcompany.s142akbmghdiag3",
    "GetValidExtendedDungeonFlows",
    "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText",
    "NumberlessPlanetName",
    "Black Mesa",
    "GreenhouseFlow",
    "TeleportPlayer",
    EXPECTED_LLL_SHA256,
    EXPECTED_NORMALIZER_SHA256,
    EXPECTED_GAME_SHA256,
    "GameAssemblyProvenance.Validate(Paths.ManagedPath, GameAssemblySha)",
    "runtimeAssembly.IsDynamic",
    "runtimeAssembly.ManifestModule != null",
    "[BMGHDIAG3] ARMED",
    "[BMGHDIAG3] SELECTED",
    "[BMGHDIAG3] TRAVERSED",
    "[BMGHDIAG3] TOPOLOGY_OK",
    "[BMGHDIAG3] TOPOLOGY_INCONCLUSIVE",
    "[BMGHDIAG3] REFUSED TO ARM",
    "[BMGHDIAG3] REFUSED selection",
):
    require(literal in plugin, "Missing preserved runtime contract literal: " + literal)

require("[BMGHDIAG2]" not in plugin, "Successor must not emit predecessor markers")
require("s142akbmghdiag2" not in plugin.lower(), "Successor retains predecessor external identity")
require(plugin.count("harmony.Patch(") == 2, "Plugin must install exactly two Harmony patch surfaces")
require("after = new[] { NormalizerGuid }" in plugin and "priority = Priority.Last" in plugin,
        "Selection postfix lost after-normalizer/Priority.Last ordering")
for forbidden in (".SetValue(", "PatchAll(", "prefix:", "transpiler:", ".FindExitPoint(", ".TeleportPlayer("):
    require(forbidden.lower() not in plugin_code.lower(),
            "Forbidden broader executable patch/mutation surface present: " + forbidden)
require(plugin.count("assembly.Location") == 1,
        "Assembly.Location must remain dependency-only and occur exactly once")

observation_match = re.search(r"private static void ResolveObservationContract\(\)\s*\{(?P<body>.*?)\n        \}", plugin, re.DOTALL)
require(observation_match is not None, "ResolveObservationContract method not found")
observation_body = observation_match.group("body")
require("runtimeAssembly != null && runtimeAssembly.ManifestModule != null" in observation_body,
        "Runtime assembly/module existence guard was weakened")
for forbidden in ("ManifestModule.Name", "ScopeName", "ModuleVersionId", "MetadataToken", ".Location", "CodeBase"):
    require(forbidden not in observation_body,
            "Forbidden/unproven loaded-game identity predicate present: " + forbidden)
for forbidden in ("manifestModuleName", "Assembly-CSharp.dll", "ScopeName", "ModuleVersionId", "MetadataToken", "Location", "CodeBase"):
    require(forbidden not in runtime_identity,
            "RuntimeIdentityPolicy contains forbidden replacement identity: " + forbidden)

for literal in (
    "Path.Combine(canonicalManagedPath, FileName)",
    "Path.GetFullPath(managedPath)",
    "Directory.Exists(canonicalManagedPath)",
    "File.Exists(assemblyPath)",
    "FileName = \"Assembly-CSharp.dll\"",
):
    require(literal in provenance, "Installed-game provenance contract missing: " + literal)
for forbidden in ("Assembly.Location", "CodeBase", "Directory.GetFiles", "EnumerateFiles", "SearchOption", "Environment.CurrentDirectory"):
    require(forbidden not in provenance, "Forbidden physical-provenance fallback present: " + forbidden)

for literal in ("EntranceTeleport", "Assembly-CSharp", "assemblyIsDynamic", "System.Void"):
    require(literal in runtime_identity, "Runtime structural identity contract missing: " + literal)
for literal in ("Black Mesa", "Greenhouse", "GreenhouseFlow", "Duplicate viable Greenhouse", "normalized rarity 100"):
    require(literal in selection, "Selection policy contract missing: " + literal)
for literal in ("TraversalDecision", "OutOfScope", "MissingPair", "InvalidPair", "Valid", "CheckTopology", "outside>inside", "inside>outside"):
    require(literal in observation, "Observation policy contract missing: " + literal)

require('ManifestModule.Name == "Assembly-CSharp.dll"' in root_cause,
        "Root-cause authority no longer identifies the disproven filename predicate")
require("ScopeName" in root_cause and
        ("not replace it" in root_cause.lower() or "do not substitute" in root_cause.lower()),
        "Root-cause authority no longer forbids guessed substitute identity predicates")

for literal in (
    "S1.42AK-BMGHDIAG3",
    EXPECTED_BASE_SHA256,
    EXPECTED_GAME_SHA256,
    "ManifestModule.Name == \"Assembly-CSharp.dll\"",
    "runtimeAssembly.ManifestModule` is non-null",
    "NO BUILD",
    "NOT RUNTIME-ARMED",
    "S1.42AK-BMDSFIX1",
    "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
    "SourceEvidence/UniversalInteriorViability/PhaseC3F18_BMGHDIAG3/IMPLEMENTATION_FINDINGS.md",
):
    require(literal in plan, "Plan missing required boundary: " + literal)
require("CI PASSED" not in evidence and "STATIC PASS" not in evidence,
        "Implementation evidence must not claim PR/static success before the gate runs")
require("NO BUILD" in evidence and "S1.42AK-BMDSFIX1" in evidence,
        "Implementation evidence does not preserve source-only/current-controller boundary")
require("BMGHDIAG3" in readme and "NEVER ACCEPT" in readme,
        "Successor README identity/diagnostic boundary missing")

require("python AnalysisTools/validate_s142ak_bmghdiag3_source.py" in workflow,
        "Static validator command missing from workflow")
for forbidden in ("dotnet", "profile_builder.py", "build_profile", "actions/upload-artifact", "gale"):
    require(forbidden.lower() not in workflow.lower(),
            "Source/static workflow contains forbidden build/publication/runtime action: " + forbidden)

print(json.dumps({
    "status": "SOURCE_STATIC_DESIGN_CONTRACT_PASS_NO_BUILD",
    "candidate_id": "S1.42AK-BMGHDIAG3",
    "behavioral_delta": "remove only ManifestModule.Name == Assembly-CSharp.dll runtime equality",
    "runtime_module_presence_required": True,
    "replacement_identity_predicate_added": False,
    "harmony_surfaces": 2,
    "gameplay_mutating_surfaces": 1,
    "observation_surfaces": 1,
    "physical_game_provenance": "Paths.ManagedPath/Assembly-CSharp.dll + exact SHA-256",
    "current_build_controller_enabled": current_build["enabled"],
    "runtime_active_build": active_build,
    "active_gameplay_candidate": current_state["active_candidate"]["build_id"],
    "compiler_invoked_by_gate": False,
    "profile_builder_invoked_by_gate": False,
    "runtime_authorized_for_successor": False,
}, indent=2))
