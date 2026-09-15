#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "prepare/s142ai-diag1r3"
EXPECTED_BASE = "bb237637de167c042b406d967715adb06c51dda2"
R2 = "S1.42AI-DIAG1R2"
R3 = "S1.42AI-DIAG1R3"
R2_PROFILE = "Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z"
R2_PROFILE_SHA = "9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15"
R2_DLL_SHA = "099a54571dc0595638fbd2f338c67137f42734b8aedf80478005dff314a0a3b3"
R2_RUNTIME = "RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/"
R2_LOG_SHA = "6d913ac6788c72b7c2afb5092297a9070f5efb44bc33053d1ff6869a72019232"
R2_FAILURE = "Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md"
R2_STATUS = "Current/Projektstatus_S1.42AI-DIAG1R2_RUNTIME_FAILED.json"
R3_REQUEST = "BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md"
S142AI_PROFILE = "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
S142AI_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
AH_PROFILE = "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z"
AH_SHA = "06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e"


def fail(message: str) -> None:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, obj) -> None:
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected one exact replacement anchor, found {count}")
    return text.replace(old, new, 1)


def regex_replace_once(text: str, pattern: str, replacement: str, label: str, flags=0) -> str:
    out, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    require(count == 1, f"{label}: expected one regex replacement, found {count}")
    return out


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def verify_preconditions() -> None:
    require(os.environ.get("GITHUB_REF_NAME") == BRANCH, "wrong preparation branch")
    merge_base = git("merge-base", "HEAD", "origin/main")
    require(merge_base == EXPECTED_BASE, f"unexpected merge base: {merge_base}")

    state = load_json("Current/CURRENT_STATE.json")
    require(state["accepted_baseline"]["build_id"] == "S1.42AH", "accepted baseline drift")
    require(state["latest_built_artifact"]["build_id"] == R2, "latest artifact drift")
    require(isinstance(state.get("active_candidate"), dict) and state["active_candidate"].get("build_id") == R2, "R2 is not the pre-transition active candidate")
    require(state.get("runtime_test_outstanding") is True, "R2 runtime gate is not pre-transition pending")
    require(state["controllers"]["runtime_active_build"] == R2, "runtime attribution drift")

    controller = load_json("BuildSpecs/current.json")
    require(controller.get("enabled") is False, "build controller unexpectedly enabled")
    require(controller.get("build_id") == "IDLE_AFTER_S1.42AI-DIAG1R2_BUILD_AWAITING_RUNTIME", "build controller state drift")

    index = load_json(R2_RUNTIME + "INDEX.json")
    require(index.get("build_id") == R2, "R2 runtime evidence build id drift")
    log_entry = next((x for x in index.get("files", []) if x.get("name") == "LogOutput.log"), None)
    require(log_entry is not None and log_entry.get("sha256") == R2_LOG_SHA, "R2 runtime INDEX log SHA drift")
    raw = ROOT / R2_RUNTIME / "raw/LogOutput.log"
    require(raw.is_file(), "R2 raw runtime log missing")
    require(sha256_file(raw) == R2_LOG_SHA, "R2 raw runtime log bytes drift")

    runtime = raw.read_text(encoding="utf-8", errors="replace")
    for marker in (
        "[DIAG1_OWNER_TYPE_DERIVED]",
        "[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]",
        "[DIAG1_GUARD_LAYERS_INSTALLED]",
        "[DIAG1_IDENTITY_PENDING]",
        "[DIAG1_IDENTITY_INVALID]",
        "[DIAG1_ISOLATION_BYPASS]",
    ):
        require(marker in runtime, f"R2 runtime log missing required decision marker {marker}")
    require("[DIAG1_INSTALL_ROLLED_BACK]" not in runtime, "R2 unexpectedly contains DIAG1 install rollback")
    require("enemyType='ShyGuyDef/Shy guy'" in runtime, "R2 runtime does not prove exact Shy guy enemyName")
    bypass = [line for line in runtime.splitlines() if "[DIAG1_ISOLATION_BYPASS]" in line]
    require(len(bypass) >= 2, "R2 bypass evidence unexpectedly sparse")
    require(all("type='ShyGuy.AI.ShyGuyAI'" in line and "enemyType='ShyGuyDef/Shy guy'" in line for line in bypass), "R2 bypass markers include an identity other than the exact ShyGuy runtime object")

    source = (ROOT / "Patches/S142AIDiag1Isolation/Plugin.cs").read_text(encoding="utf-8")
    require(source.count('private const string ExpectedEnemyName = "Shy Guy";') == 1, "pre-repair Shy Guy literal drift")
    require('private const string ExpectedEnemyName = "Shy guy";' not in source, "R3 identity repair already present unexpectedly")


def patch_source_and_static_gate() -> None:
    plugin_path = ROOT / "Patches/S142AIDiag1Isolation/Plugin.cs"
    source = plugin_path.read_text(encoding="utf-8")
    source = replace_once(
        source,
        'private const string ExpectedEnemyName = "Shy Guy";',
        'private const string ExpectedEnemyName = "Shy guy";',
        "Plugin.cs exact enemyName repair",
    )
    plugin_path.write_text(source, encoding="utf-8")

    validator_path = ROOT / "AnalysisTools/validate_s142ai_diag1_static.py"
    validator = validator_path.read_text(encoding="utf-8")
    anchor = '    if "private const bool ImplementationComplete = true;" not in source:\n'
    insertion = '''    identity_literals = (\n        'private const string ExpectedAssetName = "ShyGuyDef";',\n        'private const string ExpectedEnemyName = "Shy guy";',\n        'private const string ExpectedAiType = "ShyGuy.AI.ShyGuyAI";',\n    )\n    for literal in identity_literals:\n        if source.count(literal) != 1:\n            fail(f"Exact runtime-proven ShyGuy identity literal missing/ambiguous: {literal}")\n    if 'private const string ExpectedEnemyName = "Shy Guy";' in source:\n        fail("Known-bad pre-R3 Shy Guy enemyName capitalization regression is present")\n    if 'string.Equals(candidate.enemyName, ExpectedEnemyName, StringComparison.Ordinal);' not in source:\n        fail("ShyGuy enemyName comparison is no longer exact ordinal")\n'''
    validator = replace_once(validator, anchor, insertion + anchor, "static identity gate insertion")
    old_report = '        "metadata_bound_pikmin_resolution_present": True,\n'
    new_report = old_report + '        "shyguy_identity_contract": {"asset": "ShyGuyDef", "enemyName": "Shy guy", "aiType": "ShyGuy.AI.ShyGuyAI", "comparison": "StringComparison.Ordinal"},\n'
    validator = replace_once(validator, old_report, new_report, "static report identity binding")
    validator_path.write_text(validator, encoding="utf-8")


def write_failure_and_request() -> None:
    failure = f'''# S1.42AI-DIAG1R2 Runtime Diagnostic Failure — ShyGuy EnemyName Identity Case Mismatch\n\n**Date:** 2026-09-15  \n**Status:** DIAGNOSTIC RUNTIME FAILURE / EXACT IDENTITY REPAIR REQUIRED / NOT ACCEPTED  \n**Accepted gameplay baseline:** `S1.42AH`  \n**Failed diagnostic build:** `{R2}`  \n**Parent full-normal candidate:** `S1.42AI`\n\n## Evidence identity\n\n- Profile: `{R2_PROFILE}`\n- Profile SHA-256: `{R2_PROFILE_SHA}`\n- Plugin DLL SHA-256: `{R2_DLL_SHA}`\n- Candidate record: `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`\n- Build request: `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md`\n- Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`\n- Runtime evidence: `{R2_RUNTIME}`\n- Runtime log SHA-256: `{R2_LOG_SHA}`\n\n## Runtime decision\n\nThis run does **not** satisfy the R2 diagnostic gate and `{R2}` must not be rerun unchanged.\n\nThe two predecessor repair questions are resolved positively in these exact R2 bytes. Runtime reaches `[DIAG1_OWNER_TYPE_DERIVED]`, the dependency-absent `[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]` path, and `[DIAG1_GUARD_LAYERS_INSTALLED]`. The run contains no `[DIAG1_INSTALL_ROLLED_BACK]`. Therefore the R1 owner/applicability failure is not recurring.\n\nThe new failure is the exact ShyGuy allowlist identity. The plugin source used:\n\n```text\nasset     = ShyGuyDef\nenemyName = Shy Guy\naiType    = ShyGuy.AI.ShyGuyAI\ncomparison = StringComparison.Ordinal\n```\n\nThe actual runtime `EnemyType` is logged as `ShyGuyDef/Shy guy`. Asset name and AI type agree; the only contradicted field is the case of the second word in `enemyName`. Because ordinal comparison rejects `Shy guy` against `Shy Guy`, DIAG1 first emits `[DIAG1_IDENTITY_PENDING]`, then `[DIAG1_IDENTITY_INVALID]`, leaves the verified allowlist unresolved, and subsequently reports the real `ShyGuy.AI.ShyGuyAI` objects as `[DIAG1_ISOLATION_BYPASS] live non-ShyGuy EnemyAI`. Every bypass marker in this run identifies `ShyGuy.AI.ShyGuyAI` with `ShyGuyDef/Shy guy`; the markers are therefore false-positive diagnostic classification caused by the exact-name mismatch, not evidence that a different enemy bypassed an armed ShyGuy allowlist.\n\n## Operator observations\n\nThe player reported one visible ShyGuy found inside the facility, no other enemy observed, and the ship-terminal `enemies` command reporting two ShyGuys. No exterior ShyGuy was observed in this run, so exterior ShyGuy visibility was **not exercised** and must not be claimed as proven by this evidence.\n\nThese observations are directionally consistent with the log: two live exact ShyGuy AI instances are present when the diagnostic misclassifies them. They do not override the technical diagnostic failure above.\n\n## Minimal successor repair\n\nThe smallest evidence-backed repair is one exact literal correction in `Patches/S142AIDiag1Isolation/Plugin.cs`:\n\n```text\nExpectedEnemyName = "Shy guy"\n```\n\nKeep `ExpectedAssetName = "ShyGuyDef"`, `ExpectedAiType = "ShyGuy.AI.ShyGuyAI"`, and `StringComparison.Ordinal` unchanged. Do **not** broaden the allowlist to `OrdinalIgnoreCase`, substring matching, aliases, or a name-only predicate. The current runtime evidence proves an exact value; patch-safety policy therefore favors binding that exact value rather than increasing the accepted identity surface.\n\nThe prebuild/static gate must also bind all three exact identity literals and reject the known-bad `"Shy Guy"` capitalization so this failure cannot silently recur. No Harmony target, spawn interception, BCMER event rule, package set, owner-resolution rule, or EndlessElevator applicability behavior is changed by this repair.\n\n## Lifecycle effect\n\n- `S1.42AH` remains the sole accepted gameplay baseline.\n- `{R2}` becomes completed failed diagnostic evidence and is no longer an active candidate.\n- No gameplay/runtime test is outstanding after this decision.\n- `S1.42AI-DIAG1` / `R1` / `R2` must not be rerun unchanged.\n- The determined successor is `{R3}`, built directly from exact full-normal `S1.42AI`, not from failed R2 bytes.\n- `{R3_REQUEST}` prepares that successor but does not arm or build it.\n- The ordinary full-normal `S1.42AI` runtime gate remains deferred and **not waived**.\n'''
    (ROOT / R2_FAILURE).write_text(failure, encoding="utf-8")

    status = {
        "schema_version": 1,
        "updated": "2026-09-15",
        "build_id": R2,
        "status": "RUNTIME_DIAGNOSTIC_FAILED_SHYGUY_ENEMYNAME_IDENTITY_CASE_MISMATCH_REPAIR_REQUIRED_NOT_ACCEPTED",
        "accepted_baseline": "S1.42AH",
        "parent_full_normal": "S1.42AI",
        "profile": R2_PROFILE,
        "sha256": R2_PROFILE_SHA,
        "candidate_record": "Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md",
        "runtime_failure": R2_FAILURE,
        "runtime_evidence": R2_RUNTIME,
        "runtime_log_sha256": R2_LOG_SHA,
        "plugin_dll_sha256": R2_DLL_SHA,
        "materialized_validation": "AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.json",
        "runtime_test_outstanding": False,
        "repair_required": True,
        "successor_build_id": R3,
        "successor_build_request": R3_REQUEST,
        "full_normal_s142ai_gate": "DEFERRED_NOT_WAIVED",
        "next_action": "Merge and exact-head validate the R2 failure/R3 preparation state; then use a separate coordinated controller transition to build R3. No gameplay is authorized before a built, statically/materially verified R3 artifact is explicitly activated.",
    }
    write_json(R2_STATUS, status)

    request = f'''# S1.42AI-DIAG1R3 Build Request\n\n**Status:** SUCCESSOR DETERMINED / SOURCE REPAIR PREPARED / BUILD REQUEST PREPARED / NOT BUILT / NOT A RUNTIME CANDIDATE  \n**Date:** 2026-09-15  \n**Accepted gameplay baseline:** `S1.42AH`  \n**Parent full-normal candidate:** `S1.42AI`  \n**Failed predecessor diagnostic:** `{R2}`\n\n## Decision\n\nThe next diagnostic artifact is `{R3}`. It remains the same temporary exact ShyGuy-isolation diagnostic scope. R3 changes only the runtime-proven ShyGuy `EnemyType.enemyName` identity literal and strengthens the static anti-regression gate around that exact triple.\n\nR2 must not be rerun unchanged because its compiled plugin requires `enemyName == "Shy Guy"` with `StringComparison.Ordinal`, while exact R2 runtime evidence proves `ShyGuyDef/Shy guy` on the real `ShyGuy.AI.ShyGuyAI` instances. Failure authority: `{R2_FAILURE}`.\n\nThe ordinary full-normal `S1.42AI` runtime gate remains deferred and is not waived. Diagnostic success cannot accept the full-normal candidate.\n\n## Exact future build identity\n\n- Build ID: `{R3}`\n- Base profile: `{S142AI_PROFILE}`\n- Base SHA-256: `{S142AI_SHA}`\n- Planned output profile: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`\n- Planned Gale profile name: `LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair`\n- Planned readable snapshot: `ProfileSources/S1.42AI-DIAG1R3/`\n- Local diagnostic project: `Patches/S142AIDiag1Isolation/S142AIDiag1Isolation.csproj`\n- Diagnostic configuration source: `BuildSpecs/S1.42AI-DIAG1_OVERLAY.json` plus `BuildSpecs/generate_s142ai_diag1_spec.py`\n\nThe future artifact must be built directly from exact full-normal `S1.42AI`. Failed DIAG1/R1/R2 profiles are evidence only and must not be used as the archive base.\n\n## Exact identity repair binding\n\nThe prepared source contract is exactly:\n\n```text\nExpectedAssetName = "ShyGuyDef"\nExpectedEnemyName = "Shy guy"\nExpectedAiType = "ShyGuy.AI.ShyGuyAI"\nenemyName comparison = StringComparison.Ordinal\n```\n\nOnly `ExpectedEnemyName` changes relative to R2. Asset identity, prefab AI type, reference-equality allowlisting, ambiguity/contradiction fail-closed behavior and every isolation interception remain unchanged. No case-insensitive, substring, alias or fallback identity is permitted.\n\n`AnalysisTools/validate_s142ai_diag1_static.py` must require exactly these three literals, require the ordinal `candidate.enemyName` comparison and reject the known-bad pre-R3 literal `ExpectedEnemyName = "Shy Guy"`.\n\n## Preserved predecessor repairs\n\nR3 must preserve without weakening:\n\n- metadata-derived `LethalMin.Onion.WithdrawPikminFromOnion List<T>` owner resolution and `[DIAG1_OWNER_TYPE_DERIVED]`;\n- exact `kite.ZelevatorCode` applicability handling: dependency absent => `[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]`, dependency present => exact provider/owner/signature still required fail-closed;\n- all existing native/simple/complex DIAG1 guard targets and bounded marker behavior;\n- exact ShyGuy-only BCMER event/config isolation;\n- no package/version changes and no unrelated profile changes.\n\n## Patch Safety Review\n\nThis repair does not add or broaden a Harmony patch. It changes one identity constant to the exact value observed in the R2 runtime object and adds static assertions preventing broader or stale identity semantics. The smallest safe surface is therefore the existing allowlist predicate; no lifecycle, network, spawn-owner or component behavior is newly intercepted.\n\nThe forbidden broader alternatives are `OrdinalIgnoreCase`, substring/name-fragment matching, asset-only or AI-type-only allowlisting, additional aliases, post-spawn cleanup, or any new shared spawn/network hook.\n\n## Controller and validation boundary\n\nThis document is preparation only. `BuildSpecs/current.json` remains disabled; no profile build is armed by this commit. `RuntimeInbox/ACTIVE_BUILD.txt` remains `{R2}` for runtime/evidence attribution until a later coordinated candidate activation explicitly changes it.\n\nA future R3 build transition must be separate and fail closed. Before R3 can become a runtime candidate it must at minimum prove:\n\n1. exact `{S142AI_PROFILE}` / `{S142AI_SHA}` base binding;\n2. clean local plugin compile;\n3. exact runtime-proven ShyGuy identity literals and ordinal comparison;\n4. absence of the known-bad `"Shy Guy"` identity literal;\n5. preserved owner-resolution and EndlessElevator applicability gates;\n6. exact intended archive delta and profile/readable-snapshot integrity;\n7. generated DLL SHA-256 and materialized semantic validation;\n8. no controller/runtime-attribution change until the built artifact is explicitly verified and activated.\n\nOnly after those gates and a later coordinated lifecycle transition may `runtime_test_outstanding` become true for R3.\n'''
    (ROOT / R3_REQUEST).write_text(request, encoding="utf-8")


def update_state_and_controller() -> None:
    state = load_json("Current/CURRENT_STATE.json")
    latest = state["latest_built_artifact"]
    latest["status"] = "RUNTIME_DIAGNOSTIC_FAILED_SHYGUY_ENEMYNAME_IDENTITY_CASE_MISMATCH_REPAIR_REQUIRED_NOT_ACCEPTED"
    latest["runtime_failure"] = R2_FAILURE
    latest["runtime_evidence"] = R2_RUNTIME
    latest["runtime_log_sha256"] = R2_LOG_SHA
    latest["project_status"] = R2_STATUS

    state["active_candidate"] = None
    state["runtime_test_outstanding"] = False
    state["selected_scope"] = {
        "scope_id": "BCMER_SHYGUY_INTERIOR_ONLY_CORRECTION",
        "title": "BCMER ShyGuy Interior-Only Event Correction",
        "status": "DIAGNOSTIC_R2_RUNTIME_FAILED_SHYGUY_IDENTITY_CASE_MISMATCH_R3_PREPARED_NOT_BUILT_FULL_NORMAL_GATE_DEFERRED_NOT_WAIVED",
        "accepted_baseline": "S1.42AH",
        "plan": "BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md",
        "topic_authority": "Knowledge/BCMER.md",
        "prior_runtime_failure": "RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/",
        "latest_runtime_failure": R2_RUNTIME,
        "finding": "R2 proves the metadata-derived LethalMin owner repair and dependency-absent EndlessElevator NOT_APPLICABLE path arm without install rollback. It then fails exact ShyGuy identity resolution because the source requires enemyName 'Shy Guy' ordinally while the real runtime EnemyType is ShyGuyDef/Shy guy with ShyGuy.AI.ShyGuyAI. All R2 isolation-bypass markers identify that exact real ShyGuy identity, so they are false-positive diagnostic classification rather than evidence of another enemy bypass. R3 is determined as a literal-only exact identity repair plus static anti-regression binding and is prepared but not built.",
        "analysis_contract": R3_REQUEST,
        "analysis_status": "DIAG1R2_RUNTIME_FAILED_R3_EXACT_IDENTITY_REPAIR_PREPARED_NOT_BUILT",
        "failed_candidate_build_id": R2,
        "profile": R2_PROFILE,
        "sha256": R2_PROFILE_SHA,
        "candidate_record": "Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md",
        "runtime_failure_record": R2_FAILURE,
        "project_status": R2_STATUS,
        "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
        "static_evidence": "AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md",
        "applicability_repair": {
            "status": "RUNTIME_PROVEN_ARMED_DEPENDENCY_ABSENT_NOT_APPLICABLE",
            "evidence_json": "AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.json",
            "evidence_md": "AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.md",
            "dependency_guid": "kite.ZelevatorCode",
            "provider_assembly": "kite.ZelevatorCode",
            "provider_type": "ElevatorMod.Patches.EndlessElevator",
            "runtime_result": "PASS_NOT_APPLICABLE_DEPENDENCY_ABSENT",
        },
        "identity_failure": {
            "asset": "ShyGuyDef",
            "runtime_enemy_name": "Shy guy",
            "failed_source_enemy_name": "Shy Guy",
            "ai_type": "ShyGuy.AI.ShyGuyAI",
            "comparison": "StringComparison.Ordinal",
            "repair": "Change only ExpectedEnemyName to exact runtime-proven 'Shy guy'; keep exact ordinal triple and fail-closed ambiguity handling.",
            "runtime_failure_record": R2_FAILURE,
        },
        "diagnostic_revision": {
            "build_id": R3,
            "status": "SUCCESSOR_DETERMINED_SOURCE_AND_STATIC_GATE_REPAIR_PREPARED_NOT_BUILT_NOT_RUNTIME_CANDIDATE",
            "request_record": R3_REQUEST,
            "base_build_id": "S1.42AI",
            "base_profile": S142AI_PROFILE,
            "base_sha256": S142AI_SHA,
            "enemy_allowlist": "Exact runtime-proven ShyGuy identity only: ShyGuyDef asset, enemyName Shy guy, prefab component ShyGuy.AI.ShyGuyAI, all exact/ordinal and fail closed if missing, ambiguous or contradictory",
            "bcmer_event_allowlist": ["ShyGuy"],
            "full_normal_validation": "DEFERRED_UNTIL_AFTER_DIAGNOSTIC_NOT_WAIVED",
            "planned_profile": "Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z",
        },
        "operator_observations": {
            "non_shyguy_enemies_observed": False,
            "visible_interior_shyguy_observed": True,
            "terminal_enemies_reported_shyguys": 2,
            "exterior_shyguy_observed": False,
            "exterior_visibility_result": "NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED",
            "interpretation": "Gameplay was directionally consistent with ShyGuy-only isolation, but the technical R2 diagnostic still fails because its exact identity allowlist rejected the real ShyGuy enemyName capitalization.",
        },
        "currently_irrelevant_actions": [
            "Do not rerun S1.42AI-DIAG1, S1.42AI-DIAG1R1 or S1.42AI-DIAG1R2 unchanged.",
            "Do not run a gameplay test now; R3 is prepared but not built or activated.",
            "Do not broaden ShyGuy identity matching to case-insensitive, substring, alias, asset-only or AI-type-only matching; exact R2 runtime evidence already proves the required value.",
            "Do not execute the deferred full-normal S1.42AI acceptance gate until the diagnostic repair path is resolved; that gate remains mandatory and is not waived.",
            "Do not treat RuntimeInbox/ACTIVE_BUILD.txt as acceptance authority or proof of a pending test.",
        ],
        "successor_build_id": R3,
        "build_request_record": R3_REQUEST,
        "candidate_build_id": None,
    }
    state["next_action"] = "S1.42AI-DIAG1R3 is determined and its exact identity source/static-gate repair plus build request are prepared, but no build is armed. Next perform a separate coordinated repository-native R3 build-controller transition from exact S1.42AI, then verify the generated artifact and materialized semantics before any runtime activation. Do not run gameplay now. The full-normal S1.42AI gate remains deferred, not waived."
    state["controllers"] = {
        "buildspec": "BuildSpecs/current.json",
        "build_enabled": False,
        "build_id": "IDLE_AFTER_S1.42AI-DIAG1R2_RUNTIME_FAILURE_R3_PREPARED_NOT_ARMED",
        "build_base_profile": AH_PROFILE,
        "build_base_sha256": AH_SHA,
        "runtime_active_build_file": "RuntimeInbox/ACTIVE_BUILD.txt",
        "runtime_active_build": R2,
    }
    write_json("Current/CURRENT_STATE.json", state)

    controller = {
        "enabled": False,
        "build_id": "IDLE_AFTER_S1.42AI-DIAG1R2_RUNTIME_FAILURE_R3_PREPARED_NOT_ARMED",
        "base_profile": AH_PROFILE,
        "base_sha256": AH_SHA,
        "output_profile": "Profiles/DO_NOT_BUILD.r2z",
        "profile_name": "DO_NOT_BUILD",
        "overwrite": False,
        "mod_state_changes": [],
        "mod_additions": [],
        "mod_removals": [],
        "config_patches": [],
        "local_plugin_builds": [],
        "text_assertions": [],
    }
    write_json("BuildSpecs/current.json", controller)


def update_integrity() -> None:
    integ = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
    require(not any(x.get("build_id") == R2 for x in integ.get("profiles", [])), "R2 already completed in artifact integrity")
    pending = [x for x in integ.get("pending_profiles", []) if x.get("build_id") != R2]
    require(len(pending) + 1 == len(integ.get("pending_profiles", [])), "R2 pending artifact entry missing")
    r2_entry = {
        "build_id": R2,
        "role": "RUNTIME_FAILED_DIAGNOSTIC_REPAIR_REQUIRED",
        "profile": R2_PROFILE,
        "profile_sha256": R2_PROFILE_SHA,
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R2/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json",
        "export": "ProfileSources/S1.42AI-DIAG1R2/export.r2x",
        "candidate_record": "Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md",
        "project_status": R2_STATUS,
        "rejection": R2_FAILURE,
        "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
        "build_request": "BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md",
        "guard_contract": "AnalysisEvidence/S1.42AI-DIAG1R1/MINIMAL_GUARD_CONTRACT.md",
        "materialized_validation": "AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.json",
        "materialized_applicability": "AnalysisEvidence/S1.42AI-DIAG1R2/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json",
        "plugin_dll_sha256": R2_DLL_SHA,
        "runtime_index": R2_RUNTIME + "INDEX.json",
        "runtime_log_sha256": R2_LOG_SHA,
        "note": "R2 armed the repaired owner and dependency-absent EndlessElevator paths without install rollback, then failed exact ShyGuy identity resolution because source enemyName 'Shy Guy' did not match runtime 'Shy guy'. Every isolation-bypass marker identified the exact ShyGuy AI object. R3 exact-literal repair is prepared before any successor build/runtime activation.",
    }
    integ["profiles"].append(r2_entry)
    integ["pending_profiles"] = pending
    integ["updated"] = "2026-09-15"
    write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integ)

    md = f'''<!-- LIVE_STATE: accepted=S1.42AH latest={R2} candidate=none runtime_test_outstanding=false -->\n# Artifact and Runtime Evidence Integrity\n\n**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  \n**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  \n**Last-Validated:** 2026-09-15\n\n## Accepted gameplay baseline: S1.42AH\n\nArtifact: `{AH_PROFILE}`  \nSHA-256: `{AH_SHA}`\n\n## Latest built artifact: {R2} — runtime failed diagnostic\n\nArtifact: `{R2_PROFILE}`  \nSHA-256: `{R2_PROFILE_SHA}`  \nCandidate record: `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`  \nRuntime failure: `{R2_FAILURE}`  \nRuntime evidence: `{R2_RUNTIME}`  \nRuntime log SHA-256: `{R2_LOG_SHA}`  \nReadable snapshot: `ProfileSources/S1.42AI-DIAG1R2/`  \nPlugin DLL SHA-256: `{R2_DLL_SHA}`\n\nR2 is now a completed `RUNTIME_FAILED_DIAGNOSTIC_REPAIR_REQUIRED` entry. Its owner/applicability repairs armed, but its exact identity classifier used `enemyName = Shy Guy` while runtime proves `Shy guy`; the resulting ShyGuy bypass markers are false-positive diagnostic classification.\n\n## Prepared successor — no artifact yet\n\n`{R3}` is determined by `{R3_REQUEST}`. The source/static-gate identity repair is prepared, but no R3 profile, DLL SHA, runtime candidate or runtime test exists yet. `BuildSpecs/current.json` remains disabled.\n\n## Earlier failed diagnostics\n\nS1.42AI-DIAG1, S1.42AI-DIAG1R1 and {R2} remain preserved as completed failed diagnostic evidence and must not be rerun unchanged.\n\n## Deferred full-normal S1.42AI gate\n\nS1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic repair path is resolved.\n\n## Retrieval invariant\n\nReasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.\n'''
    (ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md").write_text(md, encoding="utf-8")


def update_live_topics() -> None:
    lifecycle = f'''<!-- LIVE_STATE: accepted=S1.42AH latest={R2} candidate=none runtime_test_outstanding=false -->\n# Current Project Lifecycle\n\n**Status:** CURRENT / CANONICAL TOPIC  \n**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  \n**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  \n**Evidence:** `{R2_FAILURE}`, `{R3_REQUEST}`, `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`, `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  \n**Last-Validated:** 2026-09-15\n\n## Accepted gameplay baseline\n\n**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.\n\n## Latest built artifact\n\n**{R2} — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — RUNTIME DIAGNOSTIC FAILED / NOT ACCEPTED**  \nProfile: `{R2_PROFILE}`  \nSHA-256: `{R2_PROFILE_SHA}`  \nFailure: `{R2_FAILURE}`  \nRuntime evidence: `{R2_RUNTIME}`\n\nR2 proved the repaired metadata-derived LethalMin owner path and the dependency-absent EndlessElevator `NOT_APPLICABLE` path arm without DIAG1 install rollback. It then failed exact ShyGuy identity resolution because the diagnostic required ordinal `enemyName = "Shy Guy"` while the real runtime object is `ShyGuyDef/Shy guy` with AI type `ShyGuy.AI.ShyGuyAI`. Every R2 isolation-bypass marker identifies that exact ShyGuy object, so this is a diagnostic identity-classification failure, not evidence that another enemy bypassed the allowlist.\n\n## Live execution state\n\n- Accepted baseline: **S1.42AH**.\n- Latest built artifact: **{R2}**, failed diagnostic evidence.\n- Active candidate: **none**.\n- Runtime test outstanding: **no**.\n- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R2_RUNTIME_FAILURE_R3_PREPARED_NOT_ARMED`.\n- `RuntimeInbox/ACTIVE_BUILD.txt = {R2}` remains runtime/evidence attribution only and is not acceptance authority.\n- Prepared successor: **{R3}**, not built and not a runtime candidate.\n\n## R3 successor boundary\n\n`{R3_REQUEST}` binds the smallest exact repair: `ExpectedEnemyName = "Shy guy"` while preserving exact `ShyGuyDef`, `ShyGuy.AI.ShyGuyAI`, `StringComparison.Ordinal`, reference-equality allowlisting, all existing spawn-owner guards, the metadata-derived owner repair, and the EndlessElevator applicability contract. The static gate now rejects the known-bad `"Shy Guy"` capitalization. No broader case-insensitive/substring/alias identity is allowed.\n\nThere is **no gameplay test to run now**. R3 must first be built repository-native from exact full-normal S1.42AI, then pass compile/static/archive/materialized validation, and only a later coordinated lifecycle transition may activate it and set `runtime_test_outstanding=true`.\n\n## Retained full-normal gate\n\nS1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**. Diagnostic work cannot replace it.\n\n## Exact next project action\n\nPerform a separate coordinated R3 build-controller transition from exact S1.42AI using `{R3_REQUEST}`. Do not run gameplay before a built and repository-natively verified R3 artifact is explicitly activated.\n'''
    (ROOT / "Knowledge/CURRENT_LIFECYCLE.md").write_text(lifecycle, encoding="utf-8")

    roadmap = f'''<!-- LIVE_STATE: accepted=S1.42AH latest={R2} candidate=none runtime_test_outstanding=false -->\n# Live Roadmap and Deferred Scopes\n\n**Status:** CURRENT / CANONICAL TOPIC  \n**Authority:** live selected/deferred-scope list only  \n**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{R2_FAILURE}`, `{R3_REQUEST}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  \n**Last-Validated:** 2026-09-15\n\n## Current position\n\nAccepted gameplay baseline: **S1.42AH**. Latest built artifact: **{R2}**, now completed failed diagnostic evidence. There is no active runtime candidate and no runtime test outstanding.\n\nR2 successfully armed the owner/applicability repairs, but its exact ShyGuy classifier rejected the real runtime `enemyName = Shy guy` because source expected `Shy Guy` ordinally. `{R3}` is determined as the exact-literal repair and its source/static-gate/build request are prepared, but it is not built.\n\n## Active scope\n\nNext, perform a separate repository-native R3 build-controller transition from exact full-normal S1.42AI, validate the generated artifact/materialized semantics, and only then decide whether R3 may become the active runtime candidate. Do not rerun DIAG1/R1/R2 unchanged and do not request gameplay yet.\n\n## Remaining deferred independent scopes\n\n- Full-normal S1.42AI BCMER ShyGuy acceptance after the diagnostic repair path is resolved; diagnostic success cannot replace it.\n- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.\n- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.\n- MelanieMausoleum fog reduction only for that interior.\n- Black Mesa/interior/Pikmin route recovery.\n- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.\n- Final long full-stack acceptance.\n- AdditionalNetworking repair only with reproducible evidence.\n- Broader LethalMin teardown/despawn repair only with stronger evidence.\n'''
    (ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md").write_text(roadmap, encoding="utf-8")

    bcmer_path = ROOT / "Knowledge/BCMER.md"
    bcmer = bcmer_path.read_text(encoding="utf-8")
    section = f'''## ShyGuy event exterior-spawn guard — S1.42AI diagnostic repair path\n\nS1.42AH runtime evidence `RuntimeEvidence/S1.42AH/20260908T202138Z/` proved that BCMER event `ShyGuy` could create `ShyGuy(Clone) spawned outside; Switching to exterior AI` even while ordinary Scopophobia v1.3.4 retained `SpawnOutside = false`.\n\nS1.42AI is built directly from accepted S1.42AH to correct only that proven event configuration defect. The `[ShyGuy]` event retains `Event Enabled? = true`, `Event Type = VeryBad`, and all three accepted interior values, while the exterior triplet is exactly zero. `Scopophobia.cfg` remains byte-identical to accepted S1.42AH, preserving ordinary `SpawnInside = true` / `SpawnOutside = false` ownership.\n\nThe temporary ShyGuy-only diagnostic lineage is evidence, not a replacement for the full-normal gate. DIAG1 failed owner type resolution; R1 repaired that path but failed an incorrectly unconditional optional EndlessElevator target; R2 repaired applicability and runtime proved both predecessor repairs arm without install rollback. R2 then failed only the diagnostic identity contract because its ordinal literal `enemyName = "Shy Guy"` did not match the real runtime `ShyGuyDef/Shy guy` object with AI `ShyGuy.AI.ShyGuyAI`. Failure authority: `{R2_FAILURE}`.\n\nThe user observed no non-ShyGuy enemy, one visible interior ShyGuy, and two ShyGuys in the terminal enemy census. No exterior ShyGuy was observed, so exterior visibility was not exercised in that run. These gameplay observations are directionally positive but do not override the R2 diagnostic identity failure.\n\nR3 is determined by `{R3_REQUEST}` as a one-literal exact identity repair: `ExpectedEnemyName = "Shy guy"`; exact asset `ShyGuyDef`, AI type `ShyGuy.AI.ShyGuyAI`, ordinal comparison, reference-equality allowlisting, all spawn-owner guards, BCMER-only event isolation and fail-closed ambiguity behavior remain unchanged. Do not broaden to case-insensitive/substring/alias matching. R3 is not built or active yet, so no gameplay test is currently authorized.\n\nThe deferred `woah25-LethalEscapeUpdated 2.5.0` evaluation remains separate: inside -> outside transition compatibility is not equivalent to ordinary exterior spawning and must not be emulated by changing Scopophobia `SpawnOutside`.\n\nFull contract: `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`.\n'''
    bcmer = regex_replace_once(
        bcmer,
        r"## ShyGuy event exterior-spawn guard.*?(?=## Accepted equal EventType static model — S1\.42AC)",
        section,
        "BCMER ShyGuy current section",
        flags=re.S,
    )
    bcmer_path.write_text(bcmer, encoding="utf-8")


def update_routers_and_lineage() -> None:
    map_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
    km = map_path.read_text(encoding="utf-8")
    km = replace_once(
        km,
        "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=S1.42AI-DIAG1R2 runtime_test_outstanding=true -->",
        "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->",
        "knowledge map live marker",
    )
    anchor = f'''## Current lifecycle anchor\n\nAccepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.\n\nLatest built artifact: **{R2} — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — RUNTIME FAILED / NOT ACCEPTED**. Active candidate: **none**. Runtime test outstanding: **no**. Failure authority: `{R2_FAILURE}`; runtime evidence: `{R2_RUNTIME}`.\n\nR2 proves the metadata-derived owner repair and dependency-absent EndlessElevator applicability path arm, then fails the exact ShyGuy identity classifier because runtime `enemyName = Shy guy` does not match the old ordinal `Shy Guy` literal. `{R3}` is the determined successor; `{R3_REQUEST}` and the exact source/static-gate literal repair are prepared, but no R3 artifact or runtime candidate exists yet.\n\n`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R2_RUNTIME_FAILURE_R3_PREPARED_NOT_ARMED`. `RuntimeInbox/ACTIVE_BUILD.txt = {R2}` remains evidence attribution only and is not acceptance authority.\n\nThe next action is a separate coordinated repository-native R3 build-controller transition from exact S1.42AI, followed by generated-artifact/materialized validation. Do not run gameplay until a later lifecycle transition explicitly activates a verified R3 candidate. The ordinary S1.42AI full-normal BCMER ShyGuy acceptance gate remains deferred and not waived.\n\n'''
    km = regex_replace_once(km, r"## Current lifecycle anchor\n.*?(?=## Authority rule)", anchor, "knowledge map lifecycle anchor", flags=re.S)
    map_path.write_text(km, encoding="utf-8")

    kmj = load_json("Current/PROJECT_KNOWLEDGE_MAP.json")
    topic = next(x for x in kmj["topics"] if x.get("id") == "active_candidate_and_next_test")
    for alias in (R3, "DIAG1R3", "ShyGuy exact identity repair"):
        if alias not in topic["aliases"]:
            topic["aliases"].append(alias)
    topic["last_validated"] = "2026-09-15"
    write_json("Current/PROJECT_KNOWLEDGE_MAP.json", kmj)

    lineage = load_json("Current/BUILD_LINEAGE.json")
    lineage["date"] = "2026-09-15"
    lineage["active_candidate_build_id"] = None
    lineage["latest_built_artifact_id"] = R2
    r2 = next(x for x in lineage["builds"] if x.get("id") == R2)
    r2.update({
        "status": "runtime-failed-diagnostic-repair-required",
        "decision_record": R2_FAILURE,
        "project_status": R2_STATUS,
        "runtime_evidence": R2_RUNTIME,
        "runtime_log_sha256": R2_LOG_SHA,
        "safe_as_gameplay_base": False,
        "principal_feature": "R2 preserved and runtime-proved the metadata-derived LethalMin owner repair plus dependency-absent EndlessElevator NOT_APPLICABLE behavior, then failed exact ShyGuy identity classification because source enemyName 'Shy Guy' did not match runtime 'Shy guy'; all bypass markers identified the exact ShyGuy AI object, so R3 exact-literal repair is required before another diagnostic runtime.",
    })
    fi = lineage.setdefault("feature_index", {})
    fi["BCMER_ShyGuy_DIAG1_endless_elevator_applicability_repair"] = R2
    fi["BCMER_ShyGuy_DIAG1_exact_identity_repair_prepared"] = R3_REQUEST
    inv = lineage.setdefault("lineage_invariants", [])
    new_inv = "S1.42AI-DIAG1R2 was built directly from exact S1.42AI and runtime-failed only after the owner/applicability repairs armed: its ordinal enemyName literal 'Shy Guy' rejected the real ShyGuyDef/Shy guy identity. S1.42AI-DIAG1R3 is determined as a literal-only repair and, when built, must again use exact S1.42AI as the archive base rather than failed R2 bytes."
    if new_inv not in inv:
        inv.append(new_inv)
    write_json("Current/BUILD_LINEAGE.json", lineage)

    lineage_md_path = ROOT / "Current/BUILD_LINEAGE.md"
    lmd = lineage_md_path.read_text(encoding="utf-8")
    head = f'''## Current lineage head\n\n- **Accepted gameplay baseline:** S1.42AH — Mouth Dog Pikmin Dual Prevention — **ACCEPTED FULL NORMAL STACK**.\n- **Latest built artifact:** {R2} — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — **RUNTIME DIAGNOSTIC FAILED / NOT ACCEPTED**.\n- **Active candidate:** none.\n- **Prepared successor:** {R3} exact ShyGuy identity repair — **NOT BUILT / NOT ACTIVE**; request `{R3_REQUEST}`.\n- **Deferred full-normal gate:** S1.42AI — still mandatory after the diagnostic repair path is resolved.\n- **Current action:** perform a separate coordinated R3 build-controller transition from exact S1.42AI, then validate the generated artifact before any runtime activation.\n\nFor live lifecycle state use `Knowledge/CURRENT_LIFECYCLE.md`. This file is the build-history router; use the linked build-specific evidence for exact forensic detail.\n'''
    lmd = regex_replace_once(lmd, r"## Current lineage head\n.*?For live lifecycle state use `Knowledge/CURRENT_LIFECYCLE\.md`\. This file is the build-history router; use the linked build-specific evidence for exact forensic detail\.\n", head, "build lineage head", flags=re.S)
    lmd = regex_replace_once(
        lmd,
        r"\| S1\.42AI-DIAG1R2 \|[^\n]*\|",
        f"| S1.42AI-DIAG1R2 | **RUNTIME DIAGNOSTIC FAILED / REPAIR REQUIRED / NOT ACCEPTED** | R2 armed the metadata-derived owner repair and dependency-absent EndlessElevator applicability path, but exact ShyGuy identity resolution failed because source required ordinal `Shy Guy` while runtime proves `Shy guy`; all bypass markers were the exact ShyGuy AI object. Failure: `Current/149...`; R3 exact-literal repair is prepared, not built. |",
        "R2 build-lineage row",
    )
    lineage_md_path.write_text(lmd, encoding="utf-8")


def update_plan() -> None:
    path = ROOT / "BuildSpecs/S1.42AI_PLAN.md"
    text = path.read_text(encoding="utf-8")
    text = regex_replace_once(
        text,
        r"\*\*Current planning status:\*\*[^\n]*",
        "**Current planning status:** DIAG1R3_EXACT_IDENTITY_REPAIR_PREPARED_NOT_BUILT",
        "S1.42AI plan status",
    )
    heading = "## R3 exact runtime identity repair — 2026-09-15"
    require(heading not in text, "R3 plan amendment already present unexpectedly")
    insertion = f'''\n{heading}\n\nR2 runtime authority `{R2_FAILURE}` supersedes the earlier unverified display-name capitalization assumption. Exact runtime `EnemyType` identity is `ShyGuyDef` / `enemyName = Shy guy` / prefab AI `ShyGuy.AI.ShyGuyAI`. R2 had `ExpectedEnemyName = "Shy Guy"` with `StringComparison.Ordinal`; therefore it invalidated the allowlist and falsely classified the real ShyGuy objects as non-ShyGuy bypasses.\n\nR3 is determined by `{R3_REQUEST}`. The only runtime behavior change is `ExpectedEnemyName = "Shy guy"`; exact asset, AI type, ordinal comparison, reference-equality allowlisting, all spawn-owner/BCMER guards, owner-type derivation and EndlessElevator applicability remain unchanged. The static gate now binds the exact triple and rejects the known-bad `"Shy Guy"` literal. No R3 build/controller/runtime activation is authorized by this planning amendment.\n\n'''
    marker = "## Enemy isolation contract\n"
    text = replace_once(text, marker, insertion + marker, "R3 plan amendment insertion")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    verify_preconditions()
    patch_source_and_static_gate()
    write_failure_and_request()
    update_state_and_controller()
    update_integrity()
    update_live_topics()
    update_routers_and_lineage()
    update_plan()
    subprocess.check_call(["python", "RepositoryTools/render_current_navigation.py"], cwd=ROOT)
    print("PASS: R2 failure/R3 preparation state rendered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
