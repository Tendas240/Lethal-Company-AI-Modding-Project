#!/usr/bin/env python3
"""BMAFDIAG1 repository-only source/static gate. Never compiles, builds, changes config, publishes or arms runtime."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "Patches/S142AKBMGHDiag3"
PATCH = ROOT / "Patches/S142AKBMAFDiag1"
PLUGIN = PATCH / "Plugin.cs"
PROVENANCE = PATCH / "GameAssemblyProvenance.cs"
RUNTIME_IDENTITY = PATCH / "RuntimeIdentityPolicy.cs"
SELECTION = PATCH / "SelectionPolicy.cs"
OBSERVATION = PATCH / "ObservationPolicy.cs"
PROJECT = PATCH / "S142AKBMAFDiag1.csproj"
README = PATCH / "README.md"
NUGET = PATCH / "NuGet.Config"
PLAN = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1_PLAN.md"
EVIDENCE = ROOT / "SourceEvidence/UniversalInteriorViability/PhaseC3F19_BMAFDIAG1/IMPLEMENTATION_FINDINGS.md"
WORKFLOW = ROOT / ".github/workflows/s142ak-bmafdiag1-source-static.yml"
CURRENT_BUILD = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE = ROOT / "Current/CURRENT_STATE.json"
OWNER_LLL = ROOT / "RuntimeEvidence/S1.42A/20260902T224318Z/extracted/config/config/LethalLevelLoader.cfg"
ACCEPTED_LLL = ROOT / "ProfileSources/S1.42AK/BepInEx/config/LethalLevelLoader.cfg"

EXPECTED_BASE_SHA256 = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
EXPECTED_GAME_SHA256 = "5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731"
EXPECTED_LLL_SHA256 = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
EXPECTED_NORMALIZER_SHA256 = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
OWNER_MANUAL_LEVELS = (
    "Experimentation:100,Assurance:150,Offense:250,Vow:25,March:25,Adamance:25,"
    "Rend:0,Dine:0,Titan:175,Embrion:200,Artifice:300,Halation:50,Makron:300,"
    "Pandoramus:300,Silence:250,Condemned:150,Pareidolia:25,Acheron:225,"
    "Deadlock:50,Terra:175,Veld:25,Oldred:300,Infernis:200,Descent:50,Trite:150,"
    "Sierra:300,Victory:100"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    require(path.exists(), "Missing required path: " + str(path.relative_to(ROOT)))
    return path.read_text(encoding="utf-8")


def successor_namespace(text):
    return text.replace("namespace S142AKBMGHDiag3", "namespace S142AKBMAFDiag1")


def strip_csharp_noncode(text):
    pattern = re.compile(
        r'//[^\n]*|/\*.*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
        re.DOTALL,
    )
    return pattern.sub("", text)


def ascii_visible(line):
    return "".join(c for c in line if 32 <= ord(c) <= 126).strip()


def extract_section(text, header, required=True):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if ascii_visible(line) == header:
            require(start is None, "Duplicate config section: " + header)
            start = i
    if start is None:
        if required:
            raise RuntimeError("Missing config section: " + header)
        return None
    body = []
    for line in lines[start + 1:]:
        visible = ascii_visible(line)
        if visible.startswith("[") and visible.endswith("]"):
            break
        body.append(visible)
    return "\n".join(body)


def assignment(section, key):
    prefix = key + " = "
    values = [line[len(prefix):] for line in section.splitlines() if line.startswith(prefix)]
    require(len(values) == 1, "Expected exactly one assignment for " + key)
    return values[0]


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
owner_lll = read(OWNER_LLL)
accepted_lll = read(ACCEPTED_LLL)
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
    "S142AKBMAFDiag1.csproj",
    "SelectionPolicy.cs",
}
require({p.name for p in PATCH.iterdir() if p.is_file()} == expected_files,
        "BMAFDIAG1 source directory contains unexpected/missing top-level files")
require(not any(p.is_dir() for p in PATCH.iterdir()),
        "BMAFDIAG1 source/static checkpoint must not contain build/test output or compiled-test directories")

# Live lifecycle/controller state must remain untouched by this source checkpoint.
require(current_build["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "current build idle scope drift")
require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD must remain S1.42AK-BMDSFIX1")
require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(current_state["accepted_baseline"]["sha256"] == EXPECTED_BASE_SHA256, "Accepted baseline SHA drift")
require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active gameplay candidate drift")
require(current_state["runtime_test_outstanding"] is True, "Existing BMDSFIX1 runtime gate must remain outstanding")
require("31 MATCH / 22 NON-MATCH / 0 UNRESOLVED" in current_state["selected_scope"]["finding"],
        "Owner-rule applicability closure drift")

# Proven BMGHDIAG3 architecture may change only by namespace for these helpers.
for name, actual in (
    ("GameAssemblyProvenance.cs", provenance),
    ("RuntimeIdentityPolicy.cs", runtime_identity),
    ("ObservationPolicy.cs", observation),
):
    expected = successor_namespace(read(PREDECESSOR / name))
    require(actual == expected, name + " drifted beyond successor namespace identity")

# Project/NuGet metadata is a namespace/assembly successor only.
expected_project = read(PREDECESSOR / "S142AKBMGHDiag3.csproj").replace("S142AKBMGHDiag3", "S142AKBMAFDiag1")
require(project == expected_project, "BMAFDIAG1 project metadata drift")
require(read(NUGET) == read(PREDECESSOR / "NuGet.Config"), "NuGet source policy drift")

# Selection policy must be deterministic Greenhouse->Foundry target substitution only.
expected_selection = successor_namespace(read(PREDECESSOR / "SelectionPolicy.cs"))
expected_selection = expected_selection.replace("FindGreenhouse", "FindFoundry")
expected_selection = expected_selection.replace("GreenhouseFlow", "FoundryFlow")
expected_selection = expected_selection.replace("Greenhouse", "Abandoned Foundry")
expected_selection = expected_selection.replace("greenhouse", "foundry")
require(selection == expected_selection, "SelectionPolicy contains delta beyond exact Foundry target substitution")

# Plugin must preserve predecessor mechanics; only successor identity/target and one log clarification may differ.
expected_plugin = successor_namespace(read(PREDECESSOR / "Plugin.cs"))
expected_plugin = expected_plugin.replace(
    "S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic",
    "S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic",
).replace(
    "tendas.lethalcompany.s142akbmghdiag3",
    "tendas.lethalcompany.s142akbmafdiag1",
).replace(
    "[BMGHDIAG3]",
    "[BMAFDIAG1]",
).replace(
    "SelectionPolicy.FindGreenhouse",
    "SelectionPolicy.FindFoundry",
).replace(
    "GreenhouseFlow",
    "FoundryFlow",
).replace(
    "Greenhouse",
    "Abandoned Foundry",
).replace(
    "greenhouse",
    "foundry",
)
expected_plugin = expected_plugin.replace(
    "Abandoned Foundry / FoundryFlow; normalized rarity=100;",
    "Abandoned Foundry / FoundryFlow; pre-reduction viable wrapper confirmed; normalized rarity=100;",
    1,
)
require(plugin == expected_plugin,
        "Plugin.cs contains delta beyond successor identity + exact Foundry target + log clarification")

# Exact dependency/runtime/selection/observation contracts.
for literal in (
    "S1.42AK-BMAFDIAG1",
    "tendas.lethalcompany.s142akbmafdiag1",
    "GetValidExtendedDungeonFlows",
    "GetRandomExtendedDungeonFlowServerRpc",
    "GetSimulationResultsText",
    "NumberlessPlanetName",
    "Black Mesa",
    "Abandoned Foundry",
    "FoundryFlow",
    "TeleportPlayer",
    EXPECTED_LLL_SHA256,
    EXPECTED_NORMALIZER_SHA256,
    EXPECTED_GAME_SHA256,
    "GameAssemblyProvenance.Validate(Paths.ManagedPath, GameAssemblySha)",
    "runtimeAssembly.IsDynamic",
    "runtimeAssembly.ManifestModule != null",
    "[BMAFDIAG1] ARMED",
    "[BMAFDIAG1] SELECTED",
    "[BMAFDIAG1] TRAVERSED",
    "[BMAFDIAG1] TOPOLOGY_OK",
    "[BMAFDIAG1] TOPOLOGY_INCONCLUSIVE",
    "[BMAFDIAG1] REFUSED TO ARM",
    "[BMAFDIAG1] REFUSED selection",
    "pre-reduction viable wrapper confirmed",
):
    require(literal in plugin, "Missing preserved runtime contract literal: " + literal)

require("BMGHDIAG3" not in plugin and "Greenhouse" not in plugin,
        "Successor retains predecessor diagnostic target identity")
require(plugin.count("harmony.Patch(") == 2, "Plugin must install exactly two Harmony patch surfaces")
require("after = new[] { NormalizerGuid }" in plugin and "priority = Priority.Last" in plugin,
        "Selection postfix lost after-normalizer/Priority.Last ordering")
require("pool.Clear();" in plugin and "pool.Add(foundry);" in plugin,
        "Same-wrapper diagnostic singleton reduction is missing")
require("pool.Count == 31" not in plugin and "pool.Count == 32" not in plugin,
        "Diagnostic must not assert a fixed pre-reduction pool count")
require(plugin.count("assembly.Location") == 1,
        "Assembly.Location must remain dependency-only and occur exactly once")

for forbidden in (
    ".SetValue(",
    "PatchAll(",
    "prefix:",
    "transpiler:",
    ".TeleportPlayer(",
    "ConfigFile",
    "ConfigEntry",
    "File.Write",
    "WriteAllText",
    "WriteAllLines",
    "AppendAllText",
    "RegisterExtendedDungeonFlow",
):
    require(forbidden.lower() not in plugin_code.lower(),
            "Forbidden broader executable mutation/config surface present: " + forbidden)

# Owner-config provenance: exact historical owner surface exists; accepted S1.42AK has no direct Foundry section.
header = "[Custom Dungeon:  Abandoned Foundry]"
owner_section = extract_section(owner_lll, header, required=True)
require(extract_section(accepted_lll, header, required=False) is None,
        "Accepted S1.42AK unexpectedly contains a direct Abandoned Foundry config section")
require(assignment(owner_section, "Enable Content Configuration") == "false", "Owner Foundry content-config default drift")
require(assignment(owner_section, "General Settings - Enable Dynamic Dungeon Size Restriction") == "false",
        "Owner Foundry size-restriction default drift")
require(assignment(owner_section, "General Settings - Minimum Dungeon Size Multiplier") == "1",
        "Owner Foundry minimum size drift")
require(assignment(owner_section, "General Settings - Maximum Dungeon Size Multiplier") == "1",
        "Owner Foundry maximum size drift")
require(assignment(owner_section, "General Settings - Restrict Dungeon Size Scaler") == "1",
        "Owner Foundry size scaler drift")
require(assignment(owner_section, "Dungeon Injection Settings - Manual Mod Names List") == "Default Values Were Empty",
        "Owner Foundry Mod Names drift")
require(assignment(owner_section, "Dungeon Injection Settings - Manual Level Names List") == OWNER_MANUAL_LEVELS,
        "Owner Foundry Manual Level Names drift")
require(assignment(owner_section, "Dungeon Injection Settings - Dynamic Level Tags List") == "Murica:300,Canyon:50,Wasteland:150",
        "Owner Foundry Dynamic Level Tags drift")
require(assignment(owner_section, "Dungeon Injection Settings - Dynamic Route Price List") == "Default Values Were Empty",
        "Owner Foundry Route Price drift")
require("Black Mesa:" not in OWNER_MANUAL_LEVELS, "Owner Foundry rule already contains Black Mesa unexpectedly")

# Plan/evidence must bind the later config transform without applying it now.
for text, label in ((plan, "plan"), (evidence, "implementation evidence"), (readme, "README")):
    for literal in (
        "Black Mesa:100",
        "Enable Content Configuration = true",
        "Abandoned Foundry",
        "FoundryFlow",
        "S1.42AK-BMDSFIX1",
    ):
        require(literal in text, label + " missing required boundary literal: " + literal)

for literal in (
    "NO BUILD",
    "NOT RUNTIME-ARMED",
    EXPECTED_BASE_SHA256,
    "RuntimeEvidence/S1.42A/20260902T224318Z/extracted/config/config/LethalLevelLoader.cfg",
    "ProfileSources/S1.42AK/BepInEx/config/LethalLevelLoader.cfg",
    "External:100",
    "No fixed pre-reduction pool count",
    "Patch Safety Review",
):
    require(literal in plan, "Plan missing required boundary: " + literal)

# Workflow must remain source-text-only.
require("python AnalysisTools/validate_s142ak_bmafdiag1_source.py" in workflow,
        "Source-static workflow does not invoke exact validator")
for forbidden in ("dotnet", "build_profile", "upload-artifact", "RuntimeInbox", "Gale", "r2z"):
    require(forbidden.lower() not in workflow.lower(),
            "Source-static workflow contains forbidden build/runtime action: " + forbidden)

print("PASS: S1.42AK-BMAFDIAG1 source/static contract is bounded, fail-closed, config-separated and lifecycle-inert.")
