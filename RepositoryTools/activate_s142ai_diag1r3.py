#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = "S1.42AI-DIAG1R3"
TITLE = "ShyGuy Isolation Diagnostic Exact Identity Repair"
PROFILE = "Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z"
PROFILE_NAME = "LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair"
PROFILE_SHA = "13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768"
PLUGIN_PATH = "BepInEx/plugins/Tendas-S142AIDiag1Isolation/S142AIDiag1Isolation.dll"
PLUGIN_SHA = "98b464e559120dc43e8041f163ceab038506e045f4b3cd4c71be8687e9c5da7a"
BASE_PROFILE = "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
BASE_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
BUILD_RUN = 35021307391
BUILD_COMMIT = "19914cff25cb768cffe22694e93df150e45bdd2f"
VALIDATION_RUN = 35023265624
VALIDATION_HEAD = "cd3bf2c6d4fe08267cf12100b61e4dd9e24dcb61"
VALIDATION_EVIDENCE_COMMIT = "bed4e8aa810c01eec608db24bccea5811fbdc7c8"
REQUEST = "BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md"
MAT_JSON = "AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.json"
MAT_MD = "AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md"
MAT_APPLICABILITY = "AnalysisEvidence/S1.42AI-DIAG1R3/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json"
CANDIDATE = "Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md"
PROJECT_STATUS = "Current/Projektstatus_S1.42AI-DIAG1R3_CANDIDATE.json"
PREDECESSOR_FAILURE = "Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md"
MARKER = "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=S1.42AI-DIAG1R3 runtime_test_outstanding=true -->"
IDLE_ID = "IDLE_AFTER_S1.42AI-DIAG1R3_BUILD_AWAITING_RUNTIME"
TODAY = "2026-09-16"
GALE_REVISION = "2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, obj: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_section(text: str, start_heading: str, end_heading: str, replacement: str) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


def verify_preconditions() -> None:
    state = load_json("Current/CURRENT_STATE.json")
    if state.get("active_candidate") is not None or state.get("runtime_test_outstanding") is not False:
        raise RuntimeError("R3 activation requires no active candidate and runtime_test_outstanding=false")
    if state.get("accepted_baseline", {}).get("build_id") != "S1.42AH":
        raise RuntimeError("Accepted baseline drifted")
    latest = state.get("latest_built_artifact", {})
    if latest.get("build_id") != BUILD or latest.get("profile") != PROFILE or latest.get("sha256") != PROFILE_SHA:
        raise RuntimeError("CURRENT_STATE latest artifact is not exact R3")
    if state.get("selected_scope", {}).get("candidate_build_id") is not None:
        raise RuntimeError("selected_scope unexpectedly already names a candidate")
    if "coordinated lifecycle transition" not in state.get("next_action", ""):
        raise RuntimeError("CURRENT_STATE no longer requests the coordinated R3 lifecycle transition")
    if (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() != "S1.42AI-DIAG1R2":
        raise RuntimeError("Runtime attribution drifted before R3 activation")
    buildspec = load_json("BuildSpecs/current.json")
    if buildspec.get("enabled") is not False or buildspec.get("build_id") != "IDLE_AFTER_S1.42AI-DIAG1R3_MATERIALIZED_VALIDATION_AWAITING_RUNTIME_CANDIDATE_ACTIVATION":
        raise RuntimeError("BuildSpecs guard is not the exact pre-activation R3 idle state")
    if buildspec.get("base_profile") != "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z":
        raise RuntimeError("Pre-activation BuildSpecs base profile drifted")
    auto = load_json("Current/AUTO_BUILD_RESULT.json")
    if auto.get("build_id") != BUILD or auto.get("output_profile") != PROFILE or auto.get("output_sha256") != PROFILE_SHA:
        raise RuntimeError("AUTO_BUILD_RESULT is not exact R3")
    if auto.get("base_profile") != BASE_PROFILE or auto.get("base_sha256") != BASE_SHA:
        raise RuntimeError("AUTO_BUILD_RESULT R3 base binding drifted")
    if auto.get("zip_members") != 337 or auto.get("snapshot_dir") != "ProfileSources/S1.42AI-DIAG1R3":
        raise RuntimeError("AUTO_BUILD_RESULT R3 materialization metadata drift")

    validation = load_json(MAT_JSON)
    if validation.get("status") != "PASS_CANONICAL_DIAG1R3_MATERIALIZED_IDENTITY_APPLICABILITY_EQUIVALENCE":
        raise RuntimeError("R3 materialized validation is not PASS")
    if validation.get("canonical_profile_sha256") != PROFILE_SHA or validation.get("canonical_build_commit") != BUILD_COMMIT:
        raise RuntimeError("R3 materialized validation profile/build binding drifted")
    if validation.get("validation_workflow_run") != VALIDATION_RUN or validation.get("validation_head_sha") != VALIDATION_HEAD:
        raise RuntimeError("R3 validation workflow binding drifted")
    if validation.get("canonical_plugin_sha256") != PLUGIN_SHA:
        raise RuntimeError("R3 canonical plugin SHA binding drifted")
    if validation.get("static_gate_status") != "PASS_PREBUILD_STATIC_GATE":
        raise RuntimeError("R3 static gate is not PASS")
    if validation.get("materialized_applicability_status") != "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY":
        raise RuntimeError("R3 EndlessElevator materialized applicability is not PASS")
    identity = validation.get("shyguy_identity_contract", {})
    expected_identity = {
        "asset": "ShyGuyDef",
        "enemyName": "Shy guy",
        "aiType": "ShyGuy.AI.ShyGuyAI",
        "comparison": "StringComparison.Ordinal",
    }
    if identity != expected_identity:
        raise RuntimeError(f"R3 exact ShyGuy identity contract drifted: {identity!r}")
    if validation.get("known_bad_source_identity_literal_absent") is not True:
        raise RuntimeError("Known-bad R2 identity literal is not proven absent")
    if validation.get("plugin_class_inventory_identical") is not True or validation.get("plugin_decompiled_csharp_identical_per_type") is not True or validation.get("plugin_normalized_il_identical_per_type") is not True:
        raise RuntimeError("R3 semantic DLL-equivalence proof is incomplete")
    applicability = validation.get("endless_elevator_applicability", {})
    if applicability.get("applicability") != "NOT_APPLICABLE_DEPENDENCY_ABSENT" or applicability.get("dependency_guid") != "kite.ZelevatorCode":
        raise RuntimeError("R3 dependency-absent applicability contract drifted")
    if validation.get("runtime_state_modified") is not False:
        raise RuntimeError("R3 validation unexpectedly modified runtime state")

    profile_path = ROOT / PROFILE
    if not profile_path.is_file() or sha256_file(profile_path) != PROFILE_SHA:
        raise RuntimeError("Canonical R3 profile bytes/SHA are not exact")
    for rel in (
        "ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json",
        "ProfileSources/S1.42AI-DIAG1R3/export.r2x",
        MAT_MD,
        MAT_APPLICABILITY,
        REQUEST,
        PREDECESSOR_FAILURE,
    ):
        if not (ROOT / rel).is_file():
            raise RuntimeError(f"Missing exact R3 evidence/snapshot file: {rel}")
    with zipfile.ZipFile(profile_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or len(names) != 337:
            raise RuntimeError("Canonical R3 ZIP member identity/count invalid")
        if hashlib.sha256(archive.read(PLUGIN_PATH)).hexdigest() != PLUGIN_SHA:
            raise RuntimeError("Canonical R3 plugin SHA mismatch")
        cfg = archive.read("BepInEx/config/tendas.s142ai.diag1.isolation.cfg").decode("utf-8-sig")
        if "S1.42AI-DIAG1 Enabled = true" not in cfg:
            raise RuntimeError("Canonical R3 diagnostic configuration is not enabled")
        export = archive.read("export.r2x").decode("utf-8-sig")
        if f"profileName: {PROFILE_NAME}" not in export:
            raise RuntimeError("Canonical R3 export profileName mismatch")
    if (ROOT / CANDIDATE).exists() or (ROOT / PROJECT_STATUS).exists():
        raise RuntimeError("R3 candidate/project-status record already exists unexpectedly")


def ready_commands() -> tuple[str, str]:
    gale = "$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content"
    uploader = r'''$src=Join-Path $env:APPDATA 'com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw "Log not found: $src"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api "repos/$repo/contents/$dst" --jq '.sha' 2>$null);$p=@{message='Upload S1.42AI-DIAG1R3 runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT "repos/$repo/contents/$dst" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}'''
    return gale, uploader


def write_candidate_records() -> None:
    gale, uploader = ready_commands()
    candidate = f"""# S1.42AI-DIAG1R3 Build Candidate — Exact ShyGuy Identity Repair

**Date:** {TODAY}  
**Status:** BUILD PASS / STATIC + MATERIALIZED IDENTITY + APPLICABILITY + SEMANTIC EQUIVALENCE PASS / ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED  
**Accepted gameplay baseline:** `S1.42AH`  
**Failed predecessor diagnostic:** `S1.42AI-DIAG1R2`  
**Parent full-normal candidate:** `S1.42AI`

## Candidate identity

- Build: `{BUILD}`
- Profile: `{PROFILE}`
- SHA-256: `{PROFILE_SHA}`
- Canonical build workflow run: `{BUILD_RUN}`
- Automated build commit: `{BUILD_COMMIT}`
- Readable snapshot: `ProfileSources/S1.42AI-DIAG1R3/`
- File index: `ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json`
- Canonical diagnostic plugin DLL SHA-256: `{PLUGIN_SHA}`
- Build request / exact repair contract: `{REQUEST}`
- Materialized validation: `{MAT_MD}`
- Validation workflow run: `{VALIDATION_RUN}`

## Repair proven before runtime

R3 was rebuilt directly from exact full-normal S1.42AI, never from failed R2 bytes. Canonical validation proves the runtime-proven exact ShyGuy identity triple `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` with `StringComparison.Ordinal`, proves the known-bad R2 `Shy Guy` literal absent, preserves metadata-derived LethalMin owner resolution, preserves dependency-absent `kite.ZelevatorCode` EndlessElevator `NOT_APPLICABLE` behavior, and proves decompiled C# plus normalized IL semantic equivalence to the repaired green-gate build.

These facts qualify the exact R3 bytes for diagnostic runtime testing. They do not constitute gameplay acceptance and do not waive the later full-normal S1.42AI gate.

## Exact R3 runtime gate

Perform one diagnostic gameplay run with this exact profile. Require all of the following:

1. startup reaches `[DIAG1_OWNER_TYPE_DERIVED]`, dependency-absent `[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]`, and `[DIAG1_GUARD_LAYERS_INSTALLED]` without `[DIAG1_INVALID]` or `[DIAG1_INSTALL_ROLLED_BACK]`;
2. the real ShyGuy identity `ShyGuyDef/Shy guy` on `ShyGuy.AI.ShyGuyAI` resolves without the R2 `[DIAG1_IDENTITY_INVALID]` failure;
3. no `[DIAG1_ISOLATION_BYPASS]` identifies any live non-ShyGuy `EnemyAI`, and no unexpected non-ShyGuy enemy is observed while isolation is armed;
4. ShyGuy remains visibly observable inside and, when an exterior ShyGuy is present, visibly observable outside; inherited `Can Exit Facility = false` means an interior ShyGuy need not follow the player outside;
5. exercised owner-prevention/isolation markers remain bounded without exception/retry flood or broad shared-spawn/network regression.

For the operator-visible portion of the run, explicitly confirm: **(a)** no enemy other than ShyGuy appears, and **(b)** if an exterior ShyGuy spawns, it is visible rather than invisible. If no exterior ShyGuy is encountered, report that condition rather than claiming exterior visibility passed.

After the run, upload the complete fresh R3 `LogOutput.log` for repository-native ingestion and decision.

## Exact ready-to-test commands

Repository-driven Gale v2.4 replacement/import one-liner:

```powershell
{gale}
```

Exact R3 runtime-log uploader:

```powershell
{uploader}
```

## Retained full-normal S1.42AI gate

R3 diagnostic success cannot itself accept S1.42AI. The full-normal gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory afterward and is deferred, not waived.

## Acceptance boundary

`S1.42AH` remains the sole accepted gameplay baseline. `{BUILD}` is diagnostic evidence only until an explicit runtime decision is recorded.
"""
    (ROOT / CANDIDATE).write_text(candidate, encoding="utf-8")
    write_json(PROJECT_STATUS, {
        "schema_version": 1,
        "updated": TODAY,
        "build_id": BUILD,
        "status": "BUILD_PASS_STATIC_MATERIALIZED_IDENTITY_APPLICABILITY_EQUIVALENCE_PASS_ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED",
        "accepted_baseline": "S1.42AH",
        "failed_predecessor_diagnostic": "S1.42AI-DIAG1R2",
        "parent_full_normal": "S1.42AI",
        "profile": PROFILE,
        "sha256": PROFILE_SHA,
        "candidate_record": CANDIDATE,
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R3/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json",
        "workflow_run": BUILD_RUN,
        "build_commit": BUILD_COMMIT,
        "plugin_dll_sha256": PLUGIN_SHA,
        "build_request": REQUEST,
        "materialized_validation": MAT_JSON,
        "materialized_validation_workflow_run": VALIDATION_RUN,
        "exact_shyguy_identity": {
            "asset": "ShyGuyDef",
            "enemyName": "Shy guy",
            "aiType": "ShyGuy.AI.ShyGuyAI",
            "comparison": "StringComparison.Ordinal"
        },
        "materialized_applicability": "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY",
        "metadata_derived_pikmin_type": "LethalMin.Pikmin.PikminType",
        "runtime_test_outstanding": True,
        "repair_required": False,
        "next_action": "Run the exact S1.42AI-DIAG1R3 diagnostic gameplay gate, explicitly confirm ShyGuy-only spawning and exterior ShyGuy visibility when exercised, then upload the fresh complete R3 LogOutput.log for repository-native ingestion and decision.",
        "full_normal_s142ai_gate": "DEFERRED_NOT_WAIVED",
        "full_normal_candidate_record": "Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md"
    })


def update_machine_state() -> None:
    state = load_json("Current/CURRENT_STATE.json")
    state["updated"] = TODAY
    latest = state["latest_built_artifact"]
    latest["status"] = "BUILD_PASS_STATIC_MATERIALIZED_IDENTITY_APPLICABILITY_EQUIVALENCE_PASS_RUNTIME_PENDING_NOT_ACCEPTED"
    latest["candidate_record"] = CANDIDATE
    latest["project_status"] = PROJECT_STATUS
    state["active_candidate"] = {
        "build_id": BUILD,
        "title": TITLE,
        "status": "ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED",
        "profile": PROFILE,
        "sha256": PROFILE_SHA,
        "candidate_record": CANDIDATE,
        "project_status": PROJECT_STATUS,
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R3/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json",
        "workflow_run": BUILD_RUN,
        "build_commit": BUILD_COMMIT,
        "analysis_contract": REQUEST,
        "materialized_validation": MAT_JSON,
        "materialized_applicability": MAT_APPLICABILITY,
        "plugin_dll_sha256": PLUGIN_SHA,
        "shyguy_identity": {
            "asset": "ShyGuyDef",
            "enemyName": "Shy guy",
            "aiType": "ShyGuy.AI.ShyGuyAI",
            "comparison": "StringComparison.Ordinal"
        }
    }
    state["runtime_test_outstanding"] = True
    selected = state["selected_scope"]
    selected["status"] = "DIAGNOSTIC_R3_ACTIVE_RUNTIME_PENDING_FULL_NORMAL_GATE_DEFERRED_NOT_WAIVED"
    selected["finding"] = (
        "S1.42AI-DIAG1R3 is the exact active diagnostic runtime candidate. It was rebuilt directly from S1.42AI after the R2 exact-identity case failure. "
        "Canonical validation proves the exact ShyGuyDef / enemyName 'Shy guy' / ShyGuy.AI.ShyGuyAI ordinal identity, preserves metadata-derived owner resolution and dependency-absent EndlessElevator NOT_APPLICABLE behavior, and proves semantic DLL equivalence. Runtime must now prove the repaired identity arms cleanly, no non-ShyGuy enemy appears, and exterior ShyGuy remains visible when exercised."
    )
    selected["analysis_contract"] = REQUEST
    selected["analysis_status"] = "DIAG1R3_STATIC_MATERIALIZED_VALIDATION_PASS_RUNTIME_PENDING"
    selected["candidate_build_id"] = BUILD
    selected["profile"] = PROFILE
    selected["sha256"] = PROFILE_SHA
    selected["candidate_record"] = CANDIDATE
    selected["project_status"] = PROJECT_STATUS
    selected["static_evidence"] = MAT_MD
    selected["materialized_validation"] = MAT_JSON
    selected["diagnostic_revision"]["status"] = "ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED"
    selected["diagnostic_revision"]["candidate_record"] = CANDIDATE
    selected["currently_irrelevant_actions"] = [
        "Do not rerun S1.42AI-DIAG1, S1.42AI-DIAG1R1 or S1.42AI-DIAG1R2 unchanged; only R3 is the active diagnostic candidate.",
        "Do not rebuild S1.42AI-DIAG1R3 unchanged; the exact validated artifact is already active for runtime.",
        "Do not broaden ShyGuy identity matching beyond the exact runtime-proven ordinal triple.",
        "Do not execute the deferred full-normal S1.42AI acceptance gate until the R3 diagnostic runtime decision is recorded; that gate remains mandatory and is not waived.",
        "Do not treat RuntimeInbox/ACTIVE_BUILD.txt as acceptance authority; it is runtime/evidence attribution only."
    ]
    state["next_action"] = (
        "Run one exact S1.42AI-DIAG1R3 diagnostic gameplay gate. Require clean DIAG1 owner/applicability/guard-layer startup and repaired exact ShyGuy identity resolution, verify no unexpected non-ShyGuy enemy appears while isolation is armed, and verify an exterior ShyGuy is visible when that condition is exercised. Then upload the fresh complete R3 LogOutput.log for repository-native ingestion and decision. If no exterior ShyGuy is encountered, report it as not exercised rather than passed. Do not execute the deferred full-normal S1.42AI gate yet."
    )
    state["controllers"] = {
        "buildspec": "BuildSpecs/current.json",
        "build_enabled": False,
        "build_id": IDLE_ID,
        "build_base_profile": PROFILE,
        "build_base_sha256": PROFILE_SHA,
        "runtime_active_build_file": "RuntimeInbox/ACTIVE_BUILD.txt",
        "runtime_active_build": BUILD
    }
    write_json("Current/CURRENT_STATE.json", state)
    write_json("BuildSpecs/current.json", {
        "enabled": False,
        "build_id": IDLE_ID,
        "base_profile": PROFILE,
        "base_sha256": PROFILE_SHA,
        "output_profile": "Profiles/DO_NOT_BUILD.r2z",
        "profile_name": "DO_NOT_BUILD",
        "overwrite": False,
        "mod_state_changes": [],
        "mod_additions": [],
        "mod_removals": [],
        "config_patches": [],
        "local_plugin_builds": [],
        "text_assertions": []
    })
    (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD + "\n", encoding="utf-8")


def update_integrity() -> None:
    integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
    entry = {
        "build_id": BUILD,
        "role": "ACTIVE_RUNTIME_CANDIDATE_PENDING",
        "profile": PROFILE,
        "profile_sha256": PROFILE_SHA,
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R3/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json",
        "export": "ProfileSources/S1.42AI-DIAG1R3/export.r2x",
        "candidate_record": CANDIDATE,
        "project_status": PROJECT_STATUS,
        "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
        "build_request": REQUEST,
        "materialized_validation": MAT_JSON,
        "materialized_applicability": MAT_APPLICABILITY,
        "plugin_dll_sha256": PLUGIN_SHA,
        "runtime_evidence_required": False,
        "partial_runtime_evidence_present": False,
        "note": "Exact R3 profile/readable snapshot plus static/materialized exact-identity, applicability and semantic-equivalence validation are complete; diagnostic runtime evidence is now outstanding before any decision."
    }
    pending = [p for p in integrity.get("pending_profiles", []) if p.get("build_id") != BUILD]
    integrity["pending_profiles"] = [entry] + pending
    observations = [str(x) for x in integrity.get("verified_repository_api_observations", [])]
    obs = f"{BUILD} is materialized at {PROFILE} SHA-256 {PROFILE_SHA} with readable ProfileSources/S1.42AI-DIAG1R3 and canonical validation run {VALIDATION_RUN} SUCCESS."
    if obs not in observations:
        observations.append(obs)
    integrity["verified_repository_api_observations"] = observations
    integrity["last_validated"] = TODAY
    write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)


def update_lineage() -> None:
    lineage = load_json("Current/BUILD_LINEAGE.json")
    lineage["date"] = TODAY
    lineage["active_candidate_build_id"] = BUILD
    found = False
    for item in lineage.get("builds", []):
        if item.get("id") == BUILD:
            item["status"] = "active-runtime-candidate-pending"
            item["candidate_record"] = CANDIDATE
            item["decision_record"] = CANDIDATE
            item["project_status"] = PROJECT_STATUS
            item["safe_as_gameplay_base"] = False
            found = True
            break
    if not found:
        raise RuntimeError("BUILD_LINEAGE.json lacks pre-activation R3 entry")
    write_json("Current/BUILD_LINEAGE.json", lineage)

    path = ROOT / "Current/BUILD_LINEAGE.md"
    text = path.read_text(encoding="utf-8")
    replacements = {
        "- **Latest built artifact:** S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**.":
        "- **Latest built artifact:** S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — **ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**.",
        "- **Active candidate:** none.": "- **Active candidate:** S1.42AI-DIAG1R3.",
        "- **Prepared successor:** none; R3 is already built/verified and awaits a separate runtime-candidate activation transition.": "- **Prepared successor:** none; R3 is the active diagnostic runtime candidate.",
        "- **Current action:** perform a separate coordinated lifecycle transition to activate exact verified R3 as the runtime diagnostic candidate; do not import/test before `runtime_test_outstanding = true`.":
        "- **Current action:** run one exact R3 diagnostic gameplay gate, then upload the fresh complete R3 log for repository-native ingestion and decision.",
        "| S1.42AI-DIAG1R3 | **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME ACTIVATION / NOT ACCEPTED** | Built directly from exact S1.42AI with the literal-only runtime-proven `Shy guy` identity repair; canonical profile SHA `13d73d8a...` passed static, materialized applicability, decompiled-C# and normalized-IL semantic gates. No runtime candidate is active yet. |":
        "| S1.42AI-DIAG1R3 | **ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED** | Built directly from exact S1.42AI with the literal-only runtime-proven `Shy guy` identity repair; canonical profile SHA `13d73d8a...` passed static, materialized applicability, decompiled-C# and normalized-IL semantic gates. Runtime diagnostic is now outstanding. |"
    }
    for old, new in replacements.items():
        if old not in text:
            raise RuntimeError(f"BUILD_LINEAGE.md expected pre-activation text missing: {old[:90]}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


def update_live_docs() -> None:
    lifecycle = f"""{MARKER}
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `{CANDIDATE}`, `{PROJECT_STATUS}`, `{REQUEST}`, `{MAT_MD}`, `{MAT_APPLICABILITY}`, `{PREDECESSOR_FAILURE}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** {TODAY}

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Latest built artifact and active candidate

**{BUILD} — {TITLE} — ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `{PROFILE}`  
SHA-256: `{PROFILE_SHA}`  
Candidate: `{CANDIDATE}`  
Materialized validation: `{MAT_MD}`

R3 was built directly from exact full-normal S1.42AI. Canonical validation proves the exact runtime identity `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` with `StringComparison.Ordinal`, preserves the metadata-derived LethalMin owner repair and dependency-absent EndlessElevator `NOT_APPLICABLE` path, and proves decompiled C# plus normalized IL semantic equivalence to the repaired green gate.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **{BUILD}**.
- Active candidate: **{BUILD}**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `{IDLE_ID}`; no successor build is armed during the runtime gate.
- `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD}` controls attribution for the next uploaded runtime log and is not acceptance authority.
- `Current/AUTO_BUILD_RESULT.json.build_id = {BUILD}` identifies the exact built candidate.

## Canonical Gale workflow

Import/replace the active R3 profile only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` using canonical helper revision `{GALE_REVISION}`. The ready-to-test command is recorded in `{CANDIDATE}` together with the exact R3 log uploader.

## Exact runtime gate

Run one R3 diagnostic profile. Require owner derivation, dependency-absent EndlessElevator `NOT_APPLICABLE`, and all guard layers to arm without DIAG1 invalidation/rollback; require the real exact ShyGuy identity to resolve without the R2 identity failure; no live non-ShyGuy isolation bypass or unexpected non-ShyGuy enemy may appear. ShyGuy must remain visibly observable, and exterior visibility is only considered exercised if an exterior ShyGuy is actually encountered.

Operator-visible confirmations for this run are: **(1)** no enemy other than ShyGuy spawns/appears while isolation is armed; **(2)** an exterior ShyGuy, when present, is visible rather than invisible. An interior ShyGuy not following the player outside is separately explained by inherited `Can Exit Facility = false` and is not this diagnostic's failure condition.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate remains mandatory and is **deferred, not waived**. R3 diagnostic success cannot replace it.

## Exact next project action

Perform one R3 diagnostic gameplay run, explicitly record the two operator-visible confirmations above, then upload the complete fresh R3 log for repository-native ingestion and decision. If no exterior ShyGuy is encountered, report exterior visibility as not exercised rather than passed.
"""
    (ROOT / "Knowledge/CURRENT_LIFECYCLE.md").write_text(lifecycle, encoding="utf-8")

    roadmap = f"""{MARKER}
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{CANDIDATE}`, `{REQUEST}`, `{MAT_MD}`, `{PREDECESSOR_FAILURE}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** {TODAY}

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact and active diagnostic candidate: **{BUILD}**, SHA-256 `{PROFILE_SHA}`. Exact ShyGuy identity, static, materialized applicability and semantic-equivalence validation are green; its runtime diagnostic is now outstanding.

## Active scope

Run the R3 ShyGuy-isolation diagnostic, explicitly confirm no non-ShyGuy enemy appears and exterior ShyGuy visibility when exercised, ingest the fresh runtime log, and make an explicit diagnostic decision.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the R3 diagnostic question is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
"""
    (ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md").write_text(roadmap, encoding="utf-8")

    artifact_md = f"""{MARKER}
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** {TODAY}

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact / active runtime candidate: {BUILD}

Artifact: `{PROFILE}`  
SHA-256: `{PROFILE_SHA}`  
Candidate record: `{CANDIDATE}`  
Project status: `{PROJECT_STATUS}`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R3/`  
Plugin DLL SHA-256: `{PLUGIN_SHA}`  
Materialized validation: `{MAT_MD}`  
Runtime evidence required now: **yes, pending upload after gameplay**.

The machine index records R3 as `ACTIVE_RUNTIME_CANDIDATE_PENDING` with `runtime_evidence_required=false` until a final runtime decision exists; this artifact-integrity sentinel means no completed runtime evidence is required yet, not that the gameplay gate is optional.

## Completed failed predecessor: S1.42AI-DIAG1R2

R2 remains preserved as completed failed diagnostic evidence under `{PREDECESSOR_FAILURE}` and `RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
"""
    (ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md").write_text(artifact_md, encoding="utf-8")

    map_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
    map_text = map_path.read_text(encoding="utf-8")
    map_text = re.sub(r"^<!-- LIVE_STATE:.*?-->$", MARKER, map_text, count=1, flags=re.M)
    anchor = f"""## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.

Latest built artifact and active diagnostic runtime candidate: **{BUILD} — {TITLE} — NOT ACCEPTED**. Runtime test outstanding: **yes**. Exact profile SHA-256: `{PROFILE_SHA}`. Candidate authority: `{CANDIDATE}`; build/repair contract: `{REQUEST}`; materialized validation: `{MAT_MD}`.

R3 binds the exact runtime-proven identity `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` with `StringComparison.Ordinal`; owner/applicability and semantic-equivalence gates are green.

`BuildSpecs/current.json` is disabled at `{IDLE_ID}`. `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD}` and `Current/AUTO_BUILD_RESULT.json.build_id = {BUILD}` identify the exact ready candidate for import and evidence attribution; ACTIVE_BUILD is not acceptance authority.

The next action is one R3 diagnostic gameplay run followed by the exact R3 log upload and repository-native ingestion. Explicitly confirm no non-ShyGuy enemy appears and exterior ShyGuy visibility when exercised. The ordinary S1.42AI full-normal BCMER ShyGuy acceptance gate remains explicitly deferred and not waived.
"""
    map_text = replace_section(map_text, "## Current lifecycle anchor", "## Authority rule", anchor)
    map_path.write_text(map_text, encoding="utf-8")


def main() -> int:
    verify_preconditions()
    write_candidate_records()
    update_machine_state()
    update_integrity()
    update_lineage()
    update_live_docs()
    print("PASS: staged exact S1.42AI-DIAG1R3 runtime-candidate activation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
