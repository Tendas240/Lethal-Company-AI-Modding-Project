#!/usr/bin/env python3
"""Source/static fail-closed gate for the pair-scoped Black Mesa x Deep Sewers size fix."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "Patches/S142AKBMDSFix1"
PLUGIN = PATCH / "Plugin.cs"
POLICY = PATCH / "SizeClampPolicy.cs"
TESTS = PATCH / "Tests/Program.cs"
NUGET_CONFIG = PATCH / "NuGet.Config"
WORKFLOW = ROOT / ".github/workflows/s142ak-bmdsfix1-source-static.yml"
PLAN = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_PLAN.md"
CURRENT_BUILD = ROOT / "BuildSpecs/current.json"
CURRENT_STATE = ROOT / "Current/CURRENT_STATE.json"


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
policy = POLICY.read_text(encoding="utf-8")
tests = TESTS.read_text(encoding="utf-8")
nuget_config = NUGET_CONFIG.read_text(encoding="utf-8")
workflow = WORKFLOW.read_text(encoding="utf-8")
plan = PLAN.read_text(encoding="utf-8")
current_build = json.loads(CURRENT_BUILD.read_text(encoding="utf-8"))
current_state = json.loads(CURRENT_STATE.read_text(encoding="utf-8"))

require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted gameplay baseline drift")
require(current_state["active_candidate"] is None, "Unexpected gameplay active candidate")
require(current_build["enabled"] is False, "BuildSpecs/current.json must remain disabled during source review")

for literal in (
    "S1.42AK Black Mesa Deep Sewers Size Fix",
    "imabatby.lethallevelloader",
    "1.7.12",
    "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
    "LethalLevelLoader.DungeonLoader",
    "GetClampedDungeonSize",
    "[BMDSFIX1] ARMED",
    "[BMDSFIX1] APPLIED",
    "[BMDSFIX1] REFUSED TO ARM",
):
    require(literal in plugin, "Missing plugin contract literal: " + literal)

require(plugin.count("_harmony.Patch(") == 1, "BMDSFIX1 must patch exactly one Harmony surface")
require("PatchAll(" not in plugin_code, "Broad Harmony PatchAll is forbidden")
require("prefix:" not in plugin_code.lower(), "Prefix patching is forbidden")
require("transpiler:" not in plugin_code.lower(), "Transpiler patching is forbidden")
require("LethalLevelLoader.cfg" not in plugin, "Runtime patch must not mutate LLL config")
require("InteriorWeightNormalization" not in plugin, "S1.42AB normalizer must remain out of scope")
require("DeepSewersFlow" in policy and "Black Mesa" in policy and "TargetMultiplier = 1.0f" in policy,
        "Pair-scoped 1.0 clamp contract drift")
require("StringComparison.Ordinal" in policy, "Pair identity comparisons must remain ordinal/exact")

for literal in (
    "target 4.875 clamps",
    "target 1 unchanged",
    "other moon unchanged",
    "other flow unchanged",
    "moon comparison is exact",
    "flow comparison is exact",
    "NaN preserved",
    "positive infinity preserved",
):
    require(literal in tests, "Missing pure policy negative/edge test: " + literal)

for literal in (
    "https://api.nuget.org/v3/index.json",
    "https://nuget.bepinex.dev/v3/index.json",
    "https://nuget.windows10ce.com/nuget/v3/index.json",
):
    require(literal in nuget_config, "Required explicit package source missing: " + literal)

require("profile_builder.py" not in workflow, "Source gate must not build a Gale profile")
require("dotnet run --project Patches/S142AKBMDSFix1/Tests/Policy.Tests.csproj -c Release" in workflow,
        "Pure policy test command missing")
require("dotnet build S142AKBMDSFix1.csproj -c Release" in workflow,
        "Plugin compile command missing")

for literal in (
    "NOT ARMED",
    "S1.42AK",
    "Black Mesa",
    "DeepSewersFlow",
    "4.875",
    "1.0",
    "GetClampedDungeonSize",
    "BMGHDIAG2",
    "manifest module identity mismatch",
):
    require(literal in plan, "Human plan/source boundary missing: " + literal)

print(json.dumps({
    "status": "SOURCE_STATIC_CONTRACT_PASS_PUBLISHED_WORKING_BRANCH_NOT_ARMED",
    "candidate_id": "S1.42AK-BMDSFIX1",
    "base_build_id": "S1.42AK",
    "harmony_surfaces": 1,
    "target": "LethalLevelLoader.DungeonLoader.GetClampedDungeonSize",
    "pair": "Black Mesa x DeepSewersFlow",
    "clamp": 1.0,
    "package_sources_explicit": True,
    "current_build_controller_enabled": current_build["enabled"],
    "qualification": "Source, compile and pure policy only. Exact reviewed bytes may already be branch-published, but this source gate itself never builds a profile, mutates controllers, arms runtime or grants acceptance."
}, indent=2))
