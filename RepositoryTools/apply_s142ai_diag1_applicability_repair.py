#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected exactly one replacement anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def main() -> int:
    cs = ROOT / "Patches/S142AIDiag1Isolation/ComplexOwnerGuardInstaller.cs"
    replace_once(cs, "using HarmonyLib;\n", "using BepInEx.Bootstrap;\nusing HarmonyLib;\n")

    old_endless = '''            // LethalMinNightly 1.1.108 remaining iterator owner. Exact installed source
            // anchors the foreign parameter type as ElevatorMod.Patches.EndlessElevator.
            Type endlessElevator = ResolveRequiredType("ElevatorMod.Patches.EndlessElevator");
            if (endlessElevator == null)
            {
                valid = false;
            }
            else
            {
                valid &= AddPrefix(
                    targets,
                    "LethalMin EndlessElevatorPatch.WaitRespawnPikmin(EndlessElevator)",
                    "LethalMin.Compats.EndlessElevatorPatch",
                    "WaitRespawnPikmin",
                    new[] { endlessElevator },
                    typeof(IEnumerator),
                    expectedStatic: true,
                    nameof(ComplexOwnerGuardPatches.BlockIteratorOwnerPrefix));
            }
'''
    new_endless = '''            // LethalMinNightly 1.1.108 compiles this compatibility owner even when its
            // foreign provider is absent. Mirror LethalMin's exact CompatClass gate:
            // kite.ZelevatorCode absent => NOT_APPLICABLE; present => exact target required.
            valid &= AddEndlessElevatorCompatTarget(targets);
'''
    replace_once(cs, old_endless, new_endless)

    addprefix_anchor = '''        private static bool AddPrefix(
            List<Target> targets,
'''
    helper = '''        private const string EndlessElevatorDependencyGuid = "kite.ZelevatorCode";
        private const string EndlessElevatorProviderAssemblyName = "kite.ZelevatorCode";
        private const string EndlessElevatorProviderTypeName = "ElevatorMod.Patches.EndlessElevator";
        private const string EndlessElevatorOwnerTypeName = "LethalMin.Compats.EndlessElevatorPatch";
        private const string EndlessElevatorOwnerAssemblyName = "NoteBoxz.LethalMin";

        private static bool AddEndlessElevatorCompatTarget(List<Target> targets)
        {
            const string label = "LethalMin EndlessElevatorPatch.WaitRespawnPikmin(EndlessElevator)";

            // Exact LethalMin 1.1.108 source uses CompatClass("kite.ZelevatorCode") and
            // IsDependencyLoaded -> Chainloader.PluginInfos.ContainsKey. Do not touch the
            // foreign CLR type unless that exact dependency is applicable in this runtime.
            if (!Chainloader.PluginInfos.TryGetValue(EndlessElevatorDependencyGuid, out var pluginInfo))
            {
                Plugin.Log.LogInfo(
                    $"[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE] {label}: exact LethalMin CompatClass dependency '{EndlessElevatorDependencyGuid}' is not loaded.");
                return true;
            }

            if (pluginInfo == null ||
                pluginInfo.Metadata == null ||
                !string.Equals(pluginInfo.Metadata.GUID, EndlessElevatorDependencyGuid, StringComparison.Ordinal) ||
                pluginInfo.Instance == null)
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: dependency '{EndlessElevatorDependencyGuid}' is registered but its exact loaded PluginInfo/instance contract did not validate.");
                return false;
            }

            Assembly providerAssembly = pluginInfo.Instance.GetType().Assembly;
            string providerAssemblyName = providerAssembly.GetName().Name;
            if (!string.Equals(providerAssemblyName, EndlessElevatorProviderAssemblyName, StringComparison.Ordinal))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: dependency '{EndlessElevatorDependencyGuid}' resolved from assembly '{providerAssemblyName}', expected exact provider assembly '{EndlessElevatorProviderAssemblyName}'.");
                return false;
            }

            Type endlessElevator = providerAssembly.GetType(
                EndlessElevatorProviderTypeName,
                throwOnError: false,
                ignoreCase: false);
            if (endlessElevator == null ||
                endlessElevator.Assembly != providerAssembly ||
                !string.Equals(endlessElevator.FullName, EndlessElevatorProviderTypeName, StringComparison.Ordinal))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: applicable provider assembly '{EndlessElevatorProviderAssemblyName}' did not expose exact CLR type '{EndlessElevatorProviderTypeName}'.");
                return false;
            }

            Type owner = ResolveRequiredType(EndlessElevatorOwnerTypeName);
            if (owner == null ||
                !string.Equals(owner.Assembly.GetName().Name, EndlessElevatorOwnerAssemblyName, StringComparison.Ordinal))
            {
                Plugin.Log.LogError(
                    $"[DIAG1_COMPLEX_TARGET_INVALID] {label}: exact owner '{EndlessElevatorOwnerTypeName}' was not resolved from assembly '{EndlessElevatorOwnerAssemblyName}'.");
                return false;
            }

            MethodInfo original = ResolveExactDeclaredMethod(
                label,
                EndlessElevatorOwnerTypeName,
                "WaitRespawnPikmin",
                new[] { endlessElevator },
                typeof(IEnumerator),
                expectedStatic: true);
            MethodInfo prefix = ResolveOwnPatchMethod(nameof(ComplexOwnerGuardPatches.BlockIteratorOwnerPrefix));
            if (original == null || original.DeclaringType != owner || prefix == null)
                return false;

            targets.Add(new Target
            {
                Label = label,
                Original = original,
                Prefix = new HarmonyMethod(prefix) { priority = Priority.First }
            });
            Plugin.Log.LogInfo(
                $"[DIAG1_COMPLEX_TARGET_APPLICABLE] {label}: dependency='{EndlessElevatorDependencyGuid}', providerAssembly='{providerAssemblyName}', providerType='{endlessElevator.FullName}'.");
            return true;
        }

'''
    replace_once(cs, addprefix_anchor, helper + addprefix_anchor)

    validator = ROOT / "AnalysisTools/validate_s142ai_diag1_static.py"
    constants_anchor = '''KNOWN_BAD_PIKMIN_RESOLVER = 'ResolveRequiredType("LethalMin.PikminType")'\n'''
    constants = '''KNOWN_BAD_PIKMIN_RESOLVER = 'ResolveRequiredType("LethalMin.PikminType")'
ENDLESS_APPLICABILITY_EVIDENCE = ROOT / "AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.json"
R1_PROFILE = ROOT / "Profiles/LC V1 S1.42AI-DIAG1R1 ShyGuy Isolation Repair.r2z"
R1_RUNTIME_LOG = ROOT / "RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/raw/LogOutput.log"
EXPECTED_R1_PROFILE_SHA = "b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd"
EXPECTED_R1_RUNTIME_LOG_SHA = "173eefaea3a81f84e82f210066a2b034655220d951b5a66c7bb7614895737635"
EXPECTED_LETHALMIN_SHA = "9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df"
ENDLESS_OWNER_TYPE = "LethalMin.Compats.EndlessElevatorPatch"
ENDLESS_DEPENDENCY_GUID = "kite.ZelevatorCode"
ENDLESS_PROVIDER_ASSEMBLY = "kite.ZelevatorCode"
ENDLESS_PROVIDER_TYPE = "ElevatorMod.Patches.EndlessElevator"
'''
    replace_once(validator, constants_anchor, constants)

    target_anchor = "\n\nTARGETS = [\n"
    proof_fn = r'''

def prove_endless_elevator_applicability_contract(dll_path: Path, digest: str) -> dict:
    if digest != EXPECTED_LETHALMIN_SHA:
        fail(f"LethalMin exact DLL SHA changed: {digest} != {EXPECTED_LETHALMIN_SHA}")

    owner_source = run(
        ["ilspycmd", "-t", ENDLESS_OWNER_TYPE, str(dll_path)],
        timeout=120,
    ).stdout.decode("utf-8", errors="replace")
    exact_attr = f'[CompatClass("{ENDLESS_DEPENDENCY_GUID}")]'
    if owner_source.count(exact_attr) != 1:
        fail(f"EndlessElevator exact CompatClass attribute mismatch: {exact_attr}")
    if owner_source.count("[HarmonyPatch(typeof(EndlessElevator))]") != 1:
        fail("EndlessElevator owner no longer has one exact HarmonyPatch(typeof(EndlessElevator)) anchor")
    method_signature(owner_source, "WaitRespawnPikmin", "IEnumerator", ["EndlessElevator"], True)

    owner_il = run(
        ["ilspycmd", "--ilcode", "-t", ENDLESS_OWNER_TYPE, str(dll_path)],
        timeout=120,
    ).stdout.decode("utf-8", errors="replace")
    header = il_declared_method_header(owner_il, "WaitRespawnPikmin")
    exact_typeref = f"[{ENDLESS_PROVIDER_ASSEMBLY}]{ENDLESS_PROVIDER_TYPE}"
    if exact_typeref not in header:
        fail(f"EndlessElevator CLR TypeRef mismatch; expected {exact_typeref} in {header}")

    plugin_source = run(
        ["ilspycmd", "-t", "LethalMin.LethalMin", str(dll_path)],
        timeout=120,
    ).stdout.decode("utf-8", errors="replace")
    _dep_match, dep_body = method_signature(plugin_source, "IsDependencyLoaded", "bool", ["string"], True)
    dep_compact = re.sub(r"\s+", "", dep_body)
    if "returnChainloader.PluginInfos.ContainsKey(pluginGUID);" not in dep_compact:
        fail("LethalMin IsDependencyLoaded no longer maps exactly to Chainloader.PluginInfos.ContainsKey(pluginGUID)")

    _patch_match, patch_body = method_signature(plugin_source, "Patch", "void", [], False)
    patch_compact = re.sub(r"\s+", "", patch_body)
    for token in (
        "GetCustomAttribute<CompatClassAttribute>()",
        "stringmodGUID=customAttribute.ModGUID;",
        "if(!IsDependencyLoaded(modGUID))",
        "Harmony.PatchAll(type);",
    ):
        if token not in patch_compact:
            fail(f"LethalMin CompatClass activation lifecycle drifted; missing token {token}")

    if not ENDLESS_APPLICABILITY_EVIDENCE.exists():
        fail("Canonical EndlessElevator applicability evidence is missing")
    evidence = json.loads(ENDLESS_APPLICABILITY_EVIDENCE.read_text(encoding="utf-8"))
    required = {
        "dependency_guid": ENDLESS_DEPENDENCY_GUID,
        "provider_assembly": ENDLESS_PROVIDER_ASSEMBLY,
        "provider_type": ENDLESS_PROVIDER_TYPE,
        "owner_type": ENDLESS_OWNER_TYPE,
        "owner_assembly_sha256": EXPECTED_LETHALMIN_SHA,
        "r1_profile_sha256": EXPECTED_R1_PROFILE_SHA,
        "r1_runtime_log_sha256": EXPECTED_R1_RUNTIME_LOG_SHA,
    }
    for key, expected in required.items():
        if evidence.get(key) != expected:
            fail(f"EndlessElevator applicability evidence drift for {key}: {evidence.get(key)!r} != {expected!r}")
    if evidence.get("applicability") != "NOT_APPLICABLE_DEPENDENCY_ABSENT":
        fail("EndlessElevator canonical applicability is not dependency-absent NOT_APPLICABLE")

    if sha256_file(R1_PROFILE) != EXPECTED_R1_PROFILE_SHA:
        fail("R1 profile SHA drift while proving EndlessElevator applicability")
    if sha256_file(R1_RUNTIME_LOG) != EXPECTED_R1_RUNTIME_LOG_SHA:
        fail("R1 runtime log SHA drift while proving EndlessElevator applicability")
    runtime_text = R1_RUNTIME_LOG.read_text(encoding="utf-8", errors="replace")
    runtime_needle = (
        "Skipping method WaitRespawnPikmin due to missing dependency: "
        "System.IO.FileNotFoundException: Could not load file or assembly 'kite.ZelevatorCode, Version=1.0.0.0"
    )
    if runtime_needle not in runtime_text:
        fail("R1 runtime log no longer proves WaitRespawnPikmin was skipped for missing kite.ZelevatorCode")

    return {
        "owner_assembly_sha256": digest,
        "owner_type": ENDLESS_OWNER_TYPE,
        "method": "WaitRespawnPikmin",
        "compat_attribute": exact_attr,
        "dependency_gate": "Chainloader.PluginInfos.ContainsKey(pluginGUID)",
        "dependency_guid": ENDLESS_DEPENDENCY_GUID,
        "provider_assembly": ENDLESS_PROVIDER_ASSEMBLY,
        "provider_type": ENDLESS_PROVIDER_TYPE,
        "clr_typeref": exact_typeref,
        "r1_profile_sha256": EXPECTED_R1_PROFILE_SHA,
        "r1_runtime_log_sha256": EXPECTED_R1_RUNTIME_LOG_SHA,
        "applicability": "NOT_APPLICABLE_DEPENDENCY_ABSENT",
        "required_when_dependency_present": True,
        "missing_or_drifted_target_when_applicable": "FAIL_CLOSED",
    }
'''
    replace_once(validator, target_anchor, proof_fn + target_anchor)

    bad_resolver_anchor = '''    if KNOWN_BAD_PIKMIN_RESOLVER in source:
        fail("Known-bad hardcoded LethalMin PikminType resolver regression is present")
'''
    bad_resolver_new = '''    if KNOWN_BAD_PIKMIN_RESOLVER in source:
        fail("Known-bad hardcoded LethalMin PikminType resolver regression is present")
    if 'ResolveRequiredType("ElevatorMod.Patches.EndlessElevator")' in source:
        fail("EndlessElevator optional compat regressed to unconditional global type resolution")
    if "EndlessElevatorDependencyGuid" not in source or "Chainloader.PluginInfos.TryGetValue" not in source:
        fail("EndlessElevator exact dependency applicability gate is missing from runtime source")
'''
    replace_once(validator, bad_resolver_anchor, bad_resolver_new)

    marker_anchor = '''        "[DIAG1_COMPLEX_TARGET_INSTALLED]",
        "[DIAG1_TRANSPILER_MATCH]",
'''
    marker_new = '''        "[DIAG1_COMPLEX_TARGET_INSTALLED]",
        "[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]",
        "[DIAG1_COMPLEX_TARGET_APPLICABLE]",
        "[DIAG1_TRANSPILER_MATCH]",
'''
    replace_once(validator, marker_anchor, marker_new)

    export_anchor = '''    if "LC V1 S1.42AI-DIAG1 ShyGuy Isolation" not in final_names_hit[0]:
        fail("Validation export profileName mismatch")
'''
    export_new = '''    if "LC V1 S1.42AI-DIAG1 ShyGuy Isolation" not in final_names_hit[0]:
        fail("Validation export profileName mismatch")
    r1 = read_zip(R1_PROFILE)
    r1_export, r1_names_hit = normalize_export_without_profile_name(r1["export.r2x"].decode("utf-8-sig"))
    if len(r1_names_hit) != 1 or r1_export != base_export:
        fail("R1 runtime profile package/export set differs from exact S1.42AI base package set")
'''
    replace_once(validator, export_anchor, export_new)

    lethal_anchor = '''    report["checks"]["lethalmin_withdraw_clr_contract"]["archive_member"] = lethalmin_archive

    premium_record = type_to_assembly["PremiumScraps.Utils.Effects"]
'''
    lethal_new = '''    report["checks"]["lethalmin_withdraw_clr_contract"]["archive_member"] = lethalmin_archive
    report["checks"]["endless_elevator_applicability"] = prove_endless_elevator_applicability_contract(
        lethalmin_dll,
        lethalmin_digest,
    )
    report["checks"]["endless_elevator_applicability"]["package_set_binding"] = {
        "base_profile_sha256": EXPECTED_BASE_SHA,
        "r1_profile_sha256": EXPECTED_R1_PROFILE_SHA,
        "validation_export_equals_base_export_except_profile_name": True,
        "r1_export_equals_base_export_except_profile_name": True,
        "draft_mod_state_changes": [],
        "draft_mod_additions": [],
        "draft_mod_removals": [],
    }

    premium_record = type_to_assembly["PremiumScraps.Utils.Effects"]
'''
    replace_once(validator, lethal_anchor, lethal_new)

    md_anchor = '''        f"- LethalMin WithdrawPikminFromOnion CLR generic argument: `{report['checks']['lethalmin_withdraw_clr_contract']['parameter_0_generic_argument']}`",
        "- Known-bad hardcoded LethalMin PikminType resolver: absent",
'''
    md_new = '''        f"- LethalMin WithdrawPikminFromOnion CLR generic argument: `{report['checks']['lethalmin_withdraw_clr_contract']['parameter_0_generic_argument']}`",
        f"- LethalMin EndlessElevator applicability: **{report['checks']['endless_elevator_applicability']['applicability']}** via `{report['checks']['endless_elevator_applicability']['dependency_guid']}`",
        "- Known-bad hardcoded LethalMin PikminType resolver: absent",
'''
    replace_once(validator, md_anchor, md_new)

    materialized = ROOT / "AnalysisTools/validate_s142ai_diag1_materialized_applicability.py"
    materialized.write_text(r'''#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PROFILE = ROOT / "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
PROFILE = Path(os.environ["DIAG1_MATERIALIZED_PROFILE"]).resolve()
STATIC = Path(os.environ["DIAG1_STATIC_OUT"]).resolve() / "STATIC_VALIDATION.json"
OUT = Path(os.environ["DIAG1_MATERIALIZED_APPLICABILITY_OUT"]).resolve()
EXPECTED_BASE_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
EXPECTED_GUID = "kite.ZelevatorCode"
EXPECTED_ASSEMBLY = "kite.ZelevatorCode"
EXPECTED_TYPE = "ElevatorMod.Patches.EndlessElevator"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized_export(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        text = z.read("export.r2x").decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    hits = [line for line in text.split("\n") if re.match(r"^\s*profileName\s*:", line)]
    if len(hits) != 1:
        raise RuntimeError(f"Expected exactly one profileName in {path}, found {len(hits)}")
    return re.sub(r"(?m)^(\s*)profileName\s*:.*$", r"\1profileName: <NORMALIZED>", text)


def main() -> int:
    if sha256_file(BASE_PROFILE) != EXPECTED_BASE_SHA:
        raise RuntimeError("S1.42AI base profile SHA mismatch")
    static = json.loads(STATIC.read_text(encoding="utf-8"))
    if static.get("status") != "PASS_PREBUILD_STATIC_GATE":
        raise RuntimeError(f"Static gate is not green: {static.get('status')}")
    contract = static.get("checks", {}).get("endless_elevator_applicability", {})
    expected = {
        "applicability": "NOT_APPLICABLE_DEPENDENCY_ABSENT",
        "dependency_guid": EXPECTED_GUID,
        "provider_assembly": EXPECTED_ASSEMBLY,
        "provider_type": EXPECTED_TYPE,
        "required_when_dependency_present": True,
        "missing_or_drifted_target_when_applicable": "FAIL_CLOSED",
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            raise RuntimeError(f"Materialized applicability contract drift for {key}: {contract.get(key)!r} != {value!r}")
    if normalized_export(PROFILE) != normalized_export(BASE_PROFILE):
        raise RuntimeError("Materialized profile package/export set differs from exact S1.42AI applicability-bound base")
    report = {
        "status": "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY",
        "materialized_profile": str(PROFILE),
        "materialized_profile_sha256": sha256_file(PROFILE),
        "base_profile_sha256": EXPECTED_BASE_SHA,
        "applicability": contract["applicability"],
        "dependency_guid": EXPECTED_GUID,
        "provider_assembly": EXPECTED_ASSEMBLY,
        "provider_type": EXPECTED_TYPE,
        "required_when_dependency_present": True,
        "missing_or_drifted_target_when_applicable": "FAIL_CLOSED",
        "package_set_equals_bound_base": True,
        "static_gate_status": static["status"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''', encoding="utf-8")

    evidence_json = ROOT / "AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.json"
    evidence_json.write_text(json.dumps({
        "schema_version": 1,
        "status": "PROVEN_OPTIONAL_COMPAT_APPLICABILITY_CONTRACT",
        "applicability": "NOT_APPLICABLE_DEPENDENCY_ABSENT",
        "dependency_guid": "kite.ZelevatorCode",
        "provider_assembly": "kite.ZelevatorCode",
        "provider_assembly_runtime_identity": "kite.ZelevatorCode, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null",
        "provider_type": "ElevatorMod.Patches.EndlessElevator",
        "owner_package": "NotezyTeam-LethalMinNightly",
        "owner_package_version": "1.1.108",
        "owner_assembly": "NoteBoxz.LethalMin.dll",
        "owner_assembly_sha256": "9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df",
        "owner_type": "LethalMin.Compats.EndlessElevatorPatch",
        "owner_method": "WaitRespawnPikmin",
        "compat_attribute": "CompatClass(kite.ZelevatorCode)",
        "dependency_gate": "Chainloader.PluginInfos.ContainsKey(pluginGUID)",
        "source_evidence_workflow_run": 34616289395,
        "source_evidence_artifact": 10270990899,
        "r1_profile_sha256": "b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd",
        "r1_runtime_log_sha256": "173eefaea3a81f84e82f210066a2b034655220d951b5a66c7bb7614895737635",
        "r1_runtime_evidence": "RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/",
        "r1_build_workflow_run": 34822019162,
        "contract": {
            "dependency_absent": "NOT_APPLICABLE; do not resolve the foreign type and do not invalidate the complex-owner layer",
            "dependency_present": "REQUIRED; resolve exact provider assembly/type and exact LethalMin owner signature, fail closed on any drift",
            "generic_missing_target_fallback": False,
        },
        "package_name_qualification": "The concrete Thunderstore package name for kite.ZelevatorCode is not proven and is intentionally not guessed; package name is not required by LethalMin's runtime applicability contract.",
    }, indent=2) + "\n", encoding="utf-8")

    evidence_md = ROOT / "AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.md"
    evidence_md.write_text('''# S1.42AI-DIAG1R1 EndlessElevator applicability proof

**Status:** PROVEN OPTIONAL-COMPAT APPLICABILITY CONTRACT / REPAIR INPUT

Exact LethalMinNightly `1.1.108` evidence binds `LethalMin.Compats.EndlessElevatorPatch` to `[CompatClass("kite.ZelevatorCode")]`. LethalMin activates CompatClass owners only when `IsDependencyLoaded(modGUID)` is true, and that method is exactly `Chainloader.PluginInfos.ContainsKey(pluginGUID)`.

The same owner IL binds `WaitRespawnPikmin` to CLR TypeRef `[kite.ZelevatorCode]ElevatorMod.Patches.EndlessElevator`. R1 runtime evidence then proves that `kite.ZelevatorCode, Version=1.0.0.0` was absent: LethalMin logged that `WaitRespawnPikmin` was skipped for the missing dependency and continued loading normally.

Therefore, for the exact unchanged S1.42AI package set, this target is `NOT_APPLICABLE_DEPENDENCY_ABSENT`. If the exact BepInEx GUID `kite.ZelevatorCode` is present, the target becomes REQUIRED and provider assembly, CLR type, exact owner signature and patch installation must all validate fail-closed. There is no generic `missing target => ignore` rule.

The concrete Thunderstore package name that supplies `kite.ZelevatorCode` is not proven by current repository evidence and is deliberately not guessed.
''', encoding="utf-8")

    wf = ROOT / ".github/workflows/s142ai-diag1-static-validation.yml"
    replace_once(
        wf,
        "      - 'AnalysisTools/validate_s142ai_diag1_static_bound.py'\n",
        "      - 'AnalysisTools/validate_s142ai_diag1_static_bound.py'\n      - 'AnalysisTools/validate_s142ai_diag1_materialized_applicability.py'\n      - 'AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.json'\n",
    )
    replace_once(
        wf,
        '''      - name: Assert live controllers/results were not modified
        run: git diff --exit-code -- BuildSpecs/current.json RuntimeInbox/ACTIVE_BUILD.txt Current/AUTO_BUILD_RESULT.json Current/AUTO_BUILD_RESULT.md
''',
        '''      - name: Prove materialized EndlessElevator applicability semantics
        env:
          DIAG1_MATERIALIZED_PROFILE: ${{ env.DIAG1_VALIDATION_PROFILE }}
          DIAG1_MATERIALIZED_APPLICABILITY_OUT: ValidationArtifacts/materialized-applicability.json
        run: python AnalysisTools/validate_s142ai_diag1_materialized_applicability.py

      - name: Assert live controllers/results were not modified
        run: git diff --exit-code -- BuildSpecs/current.json RuntimeInbox/ACTIVE_BUILD.txt Current/AUTO_BUILD_RESULT.json Current/AUTO_BUILD_RESULT.md
''',
    )
    replace_once(
        wf,
        "            ValidationArtifacts/diag1-validation-result.md\n",
        "            ValidationArtifacts/diag1-validation-result.md\n            ValidationArtifacts/materialized-applicability.json\n",
    )

    (ROOT / ".github/workflows/s142ai-diag1-applicability-repair.yml").unlink()
    Path(__file__).unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
