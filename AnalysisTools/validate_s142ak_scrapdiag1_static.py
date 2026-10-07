#!/usr/bin/env python3
"""Static gate for S1.42AK-SCRAPDIAG1. Never arms or promotes runtime."""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-SCRAPDIAG1.json"
SOURCE_PATH = ROOT / "Patches/S142AKDiagScrapPlacement/Plugin.cs"
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-SCRAPDIAG1_BUILD_EVIDENCE"

BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
BASE_PROFILE_NAME = "LC V1 S1.42AK LC Office Camera Enemy Balance"
S139_PATH = "BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll"
S139_SHA = "bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573"
NORMALIZER_PATH = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
SELECTOR_DLL = "BepInEx/plugins/S142AJDiag1OfficeSelection/S142AJDiag1OfficeSelection.dll"
LOGGER_DLL = "BepInEx/plugins/S142AKDiagScrapPlacement/S142AKDiagScrapPlacement.dll"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def members(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate archive members")
        return {name: archive.read(name) for name in names}


spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
require(spec["enabled"] is True, "Separate diagnostic request must be enabled for review build")
require(spec["build_id"] == "S1.42AK-SCRAPDIAG1", "Build ID mismatch")
require(spec["base_sha256"] == BASE_SHA, "Spec base SHA mismatch")
require(spec["profile_name"] == BASE_PROFILE_NAME, "Internal profile identity must remain byte-stable")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections"):
    require(spec[field] == [], "Unauthorized " + field)

plugins = spec["local_plugin_builds"]
require(len(plugins) == 2, "Exactly two local plugin builds required")
require(
    [(p["project"], p["archive_path"]) for p in plugins] == [
        (
            "Patches/S142AJDiag1OfficeSelection/S142AJDiag1OfficeSelection.csproj",
            SELECTOR_DLL,
        ),
        (
            "Patches/S142AKDiagScrapPlacement/S142AKDiagScrapPlacement.csproj",
            LOGGER_DLL,
        ),
    ],
    "Local plugin build contract mismatch",
)

source = SOURCE_PATH.read_text(encoding="utf-8")
source_checks = {
    "plugin_guid": 'tendas.lethalcompany.s142akdiagscrapplacement' in source,
    "selector_hard_dependency": '[BepInDependency(SelectionGuid, BepInDependency.DependencyFlags.HardDependency)]' in source,
    "s139_hard_dependency": '[BepInDependency(S139Guid, BepInDependency.DependencyFlags.HardDependency)]' in source,
    "declared_only_lookup": "BindingFlags.DeclaredOnly" in source,
    "exact_target_name": '"SpawnScrapInLevel"' in source,
    "exact_declaring_type": "target.DeclaringType == typeof(RoundManager)" in source,
    "instance_method": "!target.IsStatic" in source,
    "zero_parameters": "target.GetParameters().Length == 0" in source,
    "void_return": "target.ReturnType == typeof(void)" in source,
    "non_null_body": "target.GetMethodBody() != null" in source,
    "single_harmony_patch": source.count("harmony.Patch(") == 1,
    "no_prefix": "HarmonyPrefix" not in source,
    "no_transpiler": "HarmonyTranspiler" not in source,
    "ordered_after_s139": "after = new[] { S139Guid }" in source and "priority = Priority.Last" in source,
    "owner_verification": "installed.Postfixes.SingleOrDefault(p => p.owner == Guid)" in source,
    "bounded_delays": "SnapshotADelaySeconds = 16f" in source and "SnapshotBDelaySeconds = 4f" in source,
    "stable_instance_ids": "idsA.SetEquals(idsB)" in source,
    "scrap_filter": "x.itemProperties.isScrap" in source,
    "anchor_scan": "FindObjectsOfType<EntranceTeleport>()" in source,
    "support_query": "Physics.RaycastAll(" in source,
    "self_collider_ignored": "GetComponentInParent<GrabbableObject>()" in source and "if (owner == scrap)" in source,
    "no_spawn_pool_reference": "spawnableScrap" not in source,
    "no_rpc_reference": re.search(r"\b(?:Rpc|RPC)\b", source) is None,
    "no_network_reference": re.search(r"\bNetwork(?:Object|Behaviour|Manager|Variable|List)?\b", source) is None,
    "no_transform_position_assignment": re.search(r"\.transform\.position\s*=", source) is None,
    "no_scrap_value_assignment": re.search(r"\.scrapValue\s*=", source) is None,
    "no_is_scrap_assignment": re.search(r"\.isScrap\s*=", source) is None,
    "no_component_disable": re.search(r"\.enabled\s*=\s*false", source) is None,
    "no_per_frame_lifecycle": re.search(r"\b(?:Update|LateUpdate|FixedUpdate)\s*\(", source) is None,
    "armed_marker": "[ScrapPlacementDiag] ARMED exact RoundManager.SpawnScrapInLevel read-only postfix" in source,
    "refused_marker": "[ScrapPlacementDiag] REFUSED " in source,
    "inconclusive_marker": "[ScrapPlacementDiag] INCONCLUSIVE" in source,
    "item_marker": "[ScrapPlacementDiag][ITEM]" in source,
    "anchor_marker": "[ScrapPlacementDiag][ANCHOR]" in source,
    "complete_marker": "[ScrapPlacementDiag] COMPLETE stable=" in source,
}
failed_checks = sorted(name for name, ok in source_checks.items() if not ok)
require(not failed_checks, "Source contract failures: " + ", ".join(failed_checks))

base = ROOT / spec["base_profile"]
output = ROOT / spec["output_profile"]
require(sha_file(base) == BASE_SHA, "Exact S1.42AK base SHA mismatch")

original = members(base)
built = members(output)
expected_added = {SELECTOR_DLL, LOGGER_DLL}
added = set(built) - set(original)
removed = set(original) - set(built)
changed = sorted(name for name in original if original[name] != built[name])

require(added == expected_added, "Added member mismatch: " + repr(sorted(added)))
require(not removed, "Removed archive members: " + repr(sorted(removed)))
require(not changed, "Changed existing archive members: " + repr(changed))
require(built["export.r2x"] == original["export.r2x"], "export.r2x must remain byte-identical")

require(sha_bytes(original[S139_PATH]) == S139_SHA, "Base S139 hash mismatch")
require(sha_bytes(built[S139_PATH]) == S139_SHA, "Built S139 drift")
require(original[S139_PATH] == built[S139_PATH], "S139 bytes changed")
require(sha_bytes(original[NORMALIZER_PATH]) == NORMALIZER_SHA, "Base normalizer hash mismatch")
require(sha_bytes(built[NORMALIZER_PATH]) == NORMALIZER_SHA, "Built normalizer drift")
require(original[NORMALIZER_PATH] == built[NORMALIZER_PATH], "Normalizer bytes changed")

dll_hashes = {}
for plugin, archive_path in zip(plugins, (SELECTOR_DLL, LOGGER_DLL)):
    compiled = ROOT / plugin["built_file"]
    require(compiled.exists(), "Compiled DLL missing: " + str(compiled))
    require(compiled.read_bytes() == built[archive_path], "Injected DLL differs from compiled DLL: " + archive_path)
    dll_hashes[archive_path] = sha_bytes(built[archive_path])

result = json.loads((ROOT / spec["result_json"]).read_text(encoding="utf-8"))
require(result["build_id"] == spec["build_id"], "Build result ID mismatch")
require(result["base_sha256"] == BASE_SHA, "Build result base SHA mismatch")
require(result["output_sha256"] == sha_file(output), "Build result output SHA mismatch")
require(result["changed_existing_members"] == [], "Builder reported changed existing members")
require(set(result["added_members"]) == expected_added, "Builder added-members mismatch")

report = {
    "status": "STATIC_PASS_NOT_ARMED",
    "build_id": spec["build_id"],
    "base_profile": spec["base_profile"],
    "base_sha256": BASE_SHA,
    "output_profile": spec["output_profile"],
    "output_sha256": sha_file(output),
    "changed_existing_members": changed,
    "removed_members": sorted(removed),
    "added_members": sorted(added),
    "diagnostic_dll_sha256": {
        "S142AJDiag1OfficeSelection.dll": dll_hashes[SELECTOR_DLL],
        "S142AKDiagScrapPlacement.dll": dll_hashes[LOGGER_DLL],
    },
    "preserved_accepted_dll_sha256": {
        "S139CompatibilityFixes.dll": S139_SHA,
        "S142ABInteriorWeightNormalization.dll": NORMALIZER_SHA,
    },
    "source_checks": source_checks,
    "qualification": (
        "Build/source/archive validation only. Runtime is not armed; startup ordering, "
        "LC Office selection, snapshot stability and placement observations remain unproven."
    ),
}

EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
(EVIDENCE_DIR / "STATIC_VERIFICATION.json").write_text(
    json.dumps(report, indent=2) + "\n", encoding="utf-8"
)
(EVIDENCE_DIR / "STATIC_VERIFICATION.md").write_text(
    "# S1.42AK-SCRAPDIAG1 Static Verification\n\n"
    f"- Status: {report['status']}\n"
    f"- Base SHA-256: `{BASE_SHA}`\n"
    f"- Output SHA-256: `{report['output_sha256']}`\n"
    f"- AJDIAG1 selector DLL SHA-256: `{dll_hashes[SELECTOR_DLL]}`\n"
    f"- Scrap placement logger DLL SHA-256: `{dll_hashes[LOGGER_DLL]}`\n"
    f"- Preserved S139 SHA-256: `{S139_SHA}`\n"
    f"- Preserved normalizer SHA-256: `{NORMALIZER_SHA}`\n"
    "- Changed existing archive members: none\n"
    "- Removed archive members: none\n"
    "- Added archive members: exactly the two diagnostic DLLs\n"
    "- Runtime state: NOT ARMED\n\n"
    + report["qualification"]
    + "\n",
    encoding="utf-8",
)

print(json.dumps(report, indent=2))
