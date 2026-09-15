#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = "S1.42AI-DIAG1R2"
PROFILE = "Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z"
PROFILE_NAME = "LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair"
PROFILE_SHA = "9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15"
PLUGIN_PATH = "BepInEx/plugins/Tendas-S142AIDiag1Isolation/S142AIDiag1Isolation.dll"
PLUGIN_SHA = "099a54571dc0595638fbd2f338c67137f42734b8aedf80478005dff314a0a3b3"
BASE_PROFILE = "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
BASE_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
BUILD_RUN = 34958254886
BUILD_COMMIT = "854e4435676ef32648407dae9ba1e2e704a420d1"
VALIDATION_RUN = 34990530260
VALIDATION_EVIDENCE_COMMIT = "aa78a0f6c7da14f9caa8bacd1e0f2d2a0d2b709c"
REQUEST = "BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md"
MAT_JSON = "AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.json"
MAT_MD = "AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md"
MAT_APPLICABILITY = "AnalysisEvidence/S1.42AI-DIAG1R2/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json"
CONTRACT = "AnalysisEvidence/S1.42AI-DIAG1R1/MINIMAL_GUARD_CONTRACT.md"
CANDIDATE = "Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md"
PROJECT_STATUS = "Current/Projektstatus_S1.42AI-DIAG1R2_CANDIDATE.json"
MARKER = "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=S1.42AI-DIAG1R2 runtime_test_outstanding=true -->"
IDLE_ID = "IDLE_AFTER_S1.42AI-DIAG1R2_BUILD_AWAITING_RUNTIME"
TODAY = "2026-09-15"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(rel: str, obj: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def verify_preconditions() -> None:
    state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text(encoding="utf-8"))
    if state.get("active_candidate") is not None or state.get("runtime_test_outstanding") is not False:
        raise RuntimeError("R2 activation requires no active candidate and runtime_test_outstanding=false")
    if state.get("accepted_baseline", {}).get("build_id") != "S1.42AH":
        raise RuntimeError("Accepted baseline drifted")
    latest = state.get("latest_built_artifact", {})
    if latest.get("build_id") != BUILD or latest.get("profile") != PROFILE or latest.get("sha256") != PROFILE_SHA:
        raise RuntimeError("CURRENT_STATE latest artifact is not exact R2")
    if state.get("next_action", "").find("coordinated lifecycle transition") < 0:
        raise RuntimeError("CURRENT_STATE no longer requests the coordinated R2 lifecycle transition")
    if (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() != "S1.42AI-DIAG1R1":
        raise RuntimeError("Runtime attribution drifted before R2 activation")
    buildspec = json.loads((ROOT / "BuildSpecs/current.json").read_text(encoding="utf-8"))
    if buildspec.get("enabled") is not False or buildspec.get("build_id") != "IDLE_AFTER_S1.42AI-DIAG1R2_MATERIALIZED_VALIDATION_AWAITING_RUNTIME_CANDIDATE_ACTIVATION":
        raise RuntimeError("BuildSpecs guard is not the exact pre-activation R2 idle state")
    auto = json.loads((ROOT / "Current/AUTO_BUILD_RESULT.json").read_text(encoding="utf-8"))
    if auto.get("build_id") != BUILD or auto.get("output_profile") != PROFILE or auto.get("output_sha256") != PROFILE_SHA:
        raise RuntimeError("AUTO_BUILD_RESULT is not exact R2")
    if auto.get("zip_members") != 337 or auto.get("snapshot_dir") != "ProfileSources/S1.42AI-DIAG1R2":
        raise RuntimeError("AUTO_BUILD_RESULT R2 materialization metadata drift")
    validation = json.loads((ROOT / MAT_JSON).read_text(encoding="utf-8"))
    if validation.get("status") != "PASS_CANONICAL_DIAG1R2_MATERIALIZED_APPLICABILITY_EQUIVALENCE":
        raise RuntimeError("R2 materialized validation is not PASS")
    if validation.get("canonical_profile_sha256") != PROFILE_SHA or validation.get("canonical_build_commit") != BUILD_COMMIT:
        raise RuntimeError("R2 materialized validation profile/build binding drifted")
    if validation.get("validation_workflow_run") != VALIDATION_RUN or validation.get("canonical_plugin_sha256") != PLUGIN_SHA:
        raise RuntimeError("R2 validation run/plugin binding drifted")
    if validation.get("materialized_applicability_status") != "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY":
        raise RuntimeError("R2 EndlessElevator materialized applicability is not PASS")
    applicability = validation.get("endless_elevator_applicability", {})
    if applicability.get("applicability") != "NOT_APPLICABLE_DEPENDENCY_ABSENT" or applicability.get("dependency_guid") != "kite.ZelevatorCode":
        raise RuntimeError("R2 dependency-absent applicability contract drifted")
    if validation.get("runtime_state_modified") is not False:
        raise RuntimeError("Materialized validation must not have modified runtime state")
    profile_path = ROOT / PROFILE
    if not profile_path.is_file() or sha256_file(profile_path) != PROFILE_SHA:
        raise RuntimeError("Canonical R2 profile bytes/SHA are not exact")
    for rel in (
        "ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json",
        "ProfileSources/S1.42AI-DIAG1R2/export.r2x",
        MAT_MD,
        MAT_APPLICABILITY,
        REQUEST,
    ):
        if not (ROOT / rel).is_file():
            raise RuntimeError(f"Missing exact R2 evidence/snapshot file: {rel}")
    with zipfile.ZipFile(profile_path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or len(names) != 337:
            raise RuntimeError("Canonical R2 ZIP member identity/count invalid")
        if hashlib.sha256(archive.read(PLUGIN_PATH)).hexdigest() != PLUGIN_SHA:
            raise RuntimeError("Canonical R2 plugin SHA mismatch")
        cfg = archive.read("BepInEx/config/tendas.s142ai.diag1.isolation.cfg").decode("utf-8-sig")
        if "S1.42AI-DIAG1 Enabled = true" not in cfg:
            raise RuntimeError("Canonical R2 diagnostic configuration is not enabled")
        export = archive.read("export.r2x").decode("utf-8-sig")
        if f"profileName: {PROFILE_NAME}" not in export:
            raise RuntimeError("Canonical R2 export profileName mismatch")
    if (ROOT / CANDIDATE).exists() or (ROOT / PROJECT_STATUS).exists():
        raise RuntimeError("R2 candidate/project-status record already exists unexpectedly")


def write_candidate_records() -> None:
    gale = "$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content"
    uploader = r'''$src=Join-Path $env:APPDATA 'com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw "Log not found: $src"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api "repos/$repo/contents/$dst" --jq '.sha' 2>$null);$p=@{message='Upload S1.42AI-DIAG1R2 runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT "repos/$repo/contents/$dst" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}'''
    candidate = f"""# S1.42AI-DIAG1R2 Build Candidate — EndlessElevator Applicability Repair

**Date:** {TODAY}  
**Status:** BUILD PASS / STATIC + MATERIALIZED APPLICABILITY + SEMANTIC EQUIVALENCE PASS / ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED  
**Accepted gameplay baseline:** `S1.42AH`  
**Failed predecessor diagnostic:** `S1.42AI-DIAG1R1`  
**Parent full-normal candidate:** `S1.42AI`

## Candidate identity

- Build: `{BUILD}`
- Profile: `{PROFILE}`
- SHA-256: `{PROFILE_SHA}`
- Canonical build workflow run: `{BUILD_RUN}`
- Automated build commit: `{BUILD_COMMIT}`
- Readable snapshot: `ProfileSources/S1.42AI-DIAG1R2/`
- File index: `ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json`
- Canonical diagnostic plugin DLL SHA-256: `{PLUGIN_SHA}`
- Build request / repair contract: `{REQUEST}`
- Preserved DIAG1 runtime guard contract: `{CONTRACT}`
- Materialized validation: `{MAT_MD}`
- Validation workflow run: `{VALIDATION_RUN}`

## Repair proven before runtime

R2 is rebuilt directly from exact full-normal S1.42AI after the landed `kite.ZelevatorCode` EndlessElevator applicability repair. The canonical materialized gate proves the dependency is absent in this profile and therefore the exact complex-owner target is `NOT_APPLICABLE_DEPENDENCY_ABSENT`; the diagnostic must not invalidate merely because that foreign target is absent. If the dependency is present in a future materialization, the exact provider assembly/type/signature remain required and fail closed.

The metadata-derived LethalMin owner repair from R1 remains present. Static/materialized validation also proves semantic equivalence of the canonical diagnostic DLL to the repaired green-gate build. These facts qualify the exact R2 bytes for runtime testing but do not constitute gameplay acceptance.

## Exact R2 runtime gate

Perform one diagnostic gameplay run with this exact profile. Require all of the following:

1. startup reaches `[DIAG1_OWNER_TYPE_DERIVED]` and, for the absent Elevator dependency, `[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]` without `[DIAG1_INVALID]` or `[DIAG1_INSTALL_ROLLED_BACK]`;
2. all approved DIAG1 isolation layers arm and no required target-install failure occurs;
3. no `[DIAG1_ISOLATION_BYPASS]` identifies a live non-ShyGuy `EnemyAI`, and no unexpected non-ShyGuy enemy is observed while isolation is armed;
4. exact Shy Guy remains visibly observable, including outside when an exterior Shy Guy is present; do not treat its inherited `Can Exit Facility = false` lack of inside-to-outside pursuit as this diagnostic's failure;
5. exercised owner-prevention/isolation markers remain bounded without exception/retry flood or broad shared-spawn/network regression.

After the run, upload the complete fresh R2 `LogOutput.log` for repository-native ingestion and decision.

## Exact ready-to-test commands

Repository-driven Gale v2.4 replacement/import one-liner:

```powershell
{gale}
```

Exact R2 runtime-log uploader:

```powershell
{uploader}
```

## Retained full-normal S1.42AI gate

R2 diagnostic success cannot itself accept S1.42AI. The full-normal gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory afterward and is deferred, not waived.

## Acceptance boundary

`S1.42AH` remains the sole accepted gameplay baseline. `{BUILD}` is diagnostic evidence only until an explicit runtime decision is recorded.
"""
    (ROOT / CANDIDATE).write_text(candidate, encoding="utf-8")
    write_json(PROJECT_STATUS, {
        "schema_version": 1,
        "updated": TODAY,
        "build_id": BUILD,
        "status": "BUILD_PASS_STATIC_MATERIALIZED_APPLICABILITY_EQUIVALENCE_PASS_ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED",
        "accepted_baseline": "S1.42AH",
        "failed_predecessor_diagnostic": "S1.42AI-DIAG1R1",
        "parent_full_normal": "S1.42AI",
        "profile": PROFILE,
        "sha256": PROFILE_SHA,
        "candidate_record": CANDIDATE,
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R2/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json",
        "workflow_run": BUILD_RUN,
        "build_commit": BUILD_COMMIT,
        "plugin_dll_sha256": PLUGIN_SHA,
        "build_request": REQUEST,
        "guard_contract": CONTRACT,
        "materialized_validation": MAT_JSON,
        "materialized_validation_workflow_run": VALIDATION_RUN,
        "materialized_applicability": "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY",
        "metadata_derived_pikmin_type": "LethalMin.Pikmin.PikminType",
        "runtime_test_outstanding": True,
        "repair_required": False,
        "next_action": "Run the exact S1.42AI-DIAG1R2 diagnostic gameplay gate, then upload the fresh complete R2 LogOutput.log for repository-native ingestion and decision.",
        "full_normal_s142ai_gate": "DEFERRED_NOT_WAIVED",
        "full_normal_candidate_record": "Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md"
    })


def update_machine_state() -> None:
    state_path = ROOT / "Current/CURRENT_STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["updated"] = TODAY
    latest = state["latest_built_artifact"]
    latest["status"] = "BUILD_PASS_STATIC_MATERIALIZED_APPLICABILITY_EQUIVALENCE_PASS_RUNTIME_PENDING_NOT_ACCEPTED"
    latest["candidate_record"] = CANDIDATE
    latest["project_status"] = PROJECT_STATUS
    state["active_candidate"] = {
        "build_id": BUILD,
        "title": "ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair",
        "status": "ACTIVE_DIAGNOSTIC_RUNTIME_CANDIDATE_NOT_ACCEPTED",
        "profile": PROFILE,
        "sha256": PROFILE_SHA,
        "candidate_record": CANDIDATE,
        "project_status": PROJECT_STATUS,
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R2/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json",
        "workflow_run": BUILD_RUN,
        "build_commit": BUILD_COMMIT,
        "analysis_contract": REQUEST,
        "guard_contract": CONTRACT,
        "materialized_validation": MAT_JSON,
        "materialized_applicability": MAT_APPLICABILITY,
        "plugin_dll_sha256": PLUGIN_SHA
    }
    state["runtime_test_outstanding"] = True
    selected = state["selected_scope"]
    selected["status"] = "DIAGNOSTIC_R2_ACTIVE_RUNTIME_PENDING_FULL_NORMAL_GATE_DEFERRED_NOT_WAIVED"
    selected["finding"] = (
        "S1.42AI-DIAG1R2 is the exact active diagnostic runtime candidate. It was rebuilt directly from S1.42AI after the landed "
        "kite.ZelevatorCode applicability repair; canonical post-build validation proves static, materialized dependency-absent "
        "NOT_APPLICABLE semantics and semantic DLL equivalence. Runtime must now prove DIAG1 arms without invalidation/rollback, "
        "suppresses all non-ShyGuy enemies, and keeps exact Shy Guy visibly observable."
    )
    selected["analysis_contract"] = REQUEST
    selected["analysis_status"] = "DIAG1R2_STATIC_MATERIALIZED_VALIDATION_PASS_RUNTIME_PENDING"
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
        "Do not rerun failed S1.42AI-DIAG1 or S1.42AI-DIAG1R1 unchanged; only R2 is the active diagnostic candidate.",
        "Do not rebuild S1.42AI-DIAG1R2 unchanged; the exact validated artifact is already active for runtime.",
        "Do not execute the deferred full-normal S1.42AI acceptance gate until the R2 diagnostic runtime decision is recorded; that gate remains mandatory and is not waived.",
        "Do not treat RuntimeInbox/ACTIVE_BUILD.txt as acceptance authority; it is runtime/evidence attribution only.",
        "Do not fold Shy Guy inside-to-outside pursuit into the current failure root cause; inherited Can Exit Facility = false is a separate behavior."
    ]
    state["next_action"] = (
        "Run one exact S1.42AI-DIAG1R2 diagnostic gameplay gate. Require the repaired owner path and dependency-absent EndlessElevator "
        "NOT_APPLICABLE path to arm without DIAG1 invalidation/rollback, verify no unexpected non-ShyGuy enemy appears while isolation is armed, "
        "and verify exact Shy Guy remains visibly observable including outside when an exterior Shy Guy is present. Then upload the fresh complete "
        "R2 LogOutput.log for repository-native ingestion and decision. Do not execute the deferred full-normal S1.42AI gate yet."
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
    path = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.json"
    integrity = json.loads(path.read_text(encoding="utf-8"))
    entry = {
        "build_id": BUILD,
        "role": "ACTIVE_RUNTIME_CANDIDATE_PENDING",
        "profile": PROFILE,
        "profile_sha256": PROFILE_SHA,
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R2/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json",
        "export": "ProfileSources/S1.42AI-DIAG1R2/export.r2x",
        "candidate_record": CANDIDATE,
        "project_status": PROJECT_STATUS,
        "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
        "build_request": REQUEST,
        "guard_contract": CONTRACT,
        "materialized_validation": MAT_JSON,
        "materialized_applicability": MAT_APPLICABILITY,
        "plugin_dll_sha256": PLUGIN_SHA,
        "runtime_evidence_required": False,
        "partial_runtime_evidence_present": False,
        "note": "Exact R2 profile/readable snapshot and static/materialized applicability/equivalence validation are complete; runtime evidence is now outstanding before any diagnostic decision."
    }
    pending = [p for p in integrity.get("pending_profiles", []) if p.get("build_id") != BUILD]
    integrity["pending_profiles"] = [entry] + pending
    observations = [str(x) for x in integrity.get("verified_repository_api_observations", [])]
    obs = f"{BUILD} is materialized at {PROFILE} SHA-256 {PROFILE_SHA} with readable ProfileSources/S1.42AI-DIAG1R2 and canonical validation run {VALIDATION_RUN} SUCCESS."
    if obs not in observations:
        observations.append(obs)
    integrity["verified_repository_api_observations"] = observations
    integrity["last_validated"] = TODAY
    write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)


def update_lineage() -> None:
    path = ROOT / "Current/BUILD_LINEAGE.json"
    lineage = json.loads(path.read_text(encoding="utf-8"))
    lineage["date"] = TODAY
    lineage["active_candidate_build_id"] = BUILD
    found = False
    for item in lineage.get("builds", []):
        if item.get("id") == BUILD:
            item["status"] = "active-runtime-candidate-pending"
            item["decision_record"] = CANDIDATE
            item["safe_as_gameplay_base"] = False
            found = True
            break
    if not found:
        raise RuntimeError("BUILD_LINEAGE.json lacks pre-activation R2 entry")
    write_json("Current/BUILD_LINEAGE.json", lineage)

    md_path = ROOT / "Current/BUILD_LINEAGE.md"
    text = md_path.read_text(encoding="utf-8")
    replacements = {
        "- **Latest built artifact:** S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**.":
        "- **Latest built artifact:** S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — **ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**.",
        "- **Active candidate:** none.": "- **Active candidate:** S1.42AI-DIAG1R2.",
        "- **Current action:** perform a separate coordinated lifecycle transition to activate exact verified R2 as the runtime diagnostic candidate; do not import/test before `runtime_test_outstanding = true`.":
        "- **Current action:** run one exact R2 diagnostic gameplay gate, then upload the fresh complete R2 log for repository-native ingestion and decision.",
        "| S1.42AI-DIAG1R2 | **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME ACTIVATION / NOT ACCEPTED** | Rebuilt directly from exact S1.42AI with the landed `kite.ZelevatorCode` applicability repair; canonical profile SHA `9dd67d6e...` passed static, materialized applicability and semantic DLL-equivalence gates. |":
        "| S1.42AI-DIAG1R2 | **ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED** | Rebuilt directly from exact S1.42AI with the landed `kite.ZelevatorCode` applicability repair; canonical profile SHA `9dd67d6e...` passed static, materialized applicability and semantic DLL-equivalence gates. Runtime diagnostic now outstanding. |"
    }
    for old, new in replacements.items():
        if old not in text:
            raise RuntimeError(f"BUILD_LINEAGE.md expected pre-activation text missing: {old[:80]}")
        text = text.replace(old, new, 1)
    md_path.write_text(text, encoding="utf-8")


def update_live_docs() -> None:
    lifecycle = f"""{MARKER}
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `{CANDIDATE}`, `{PROJECT_STATUS}`, `{REQUEST}`, `{MAT_MD}`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** {TODAY}

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact and active candidate

**{BUILD} — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `{PROFILE}`  
SHA-256: `{PROFILE_SHA}`  
Candidate: `{CANDIDATE}`  
Materialized validation: `{MAT_MD}`

R2 preserves the metadata-derived owner repair and fixes the R1 complex-owner failure by making the exact `kite.ZelevatorCode` EndlessElevator target conditional on dependency applicability. Canonical materialized evidence proves this profile has the dependency absent and therefore records the exact target as `NOT_APPLICABLE_DEPENDENCY_ABSENT`; static/materialized semantic equivalence is green.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **{BUILD}**.
- Active candidate: **{BUILD}**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `{IDLE_ID}`; no successor build is armed during the runtime gate.
- `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD}` controls attribution for the next uploaded runtime log and is not acceptance authority.

## Exact runtime gate

Run one R2 diagnostic profile. Require `[DIAG1_OWNER_TYPE_DERIVED]` and the dependency-absent `[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]` path to arm without DIAG1 invalidation or rollback; all approved isolation layers must install; no live non-ShyGuy isolation bypass or unexpected non-ShyGuy enemy may appear; exact Shy Guy must remain visibly observable, including outside when an exterior Shy Guy is present; exercised guards must remain bounded without broad shared-spawn/network regression.

The inherited `Can Exit Facility = false` behavior explains why an interior Shy Guy may not follow a player outside and is not itself the current diagnostic failure condition.

Use `{CONTRACT}` plus `{REQUEST}` for the exact guard/applicability boundary and `{CANDIDATE}` for ready-to-test commands.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**. R2 diagnostic success cannot replace it.

## Exact next project action

Perform one R2 diagnostic gameplay run, then upload the complete fresh R2 log for repository-native ingestion and decision. Do not rerun failed DIAG1 or R1 profiles.
"""
    (ROOT / "Knowledge/CURRENT_LIFECYCLE.md").write_text(lifecycle, encoding="utf-8")

    roadmap = f"""{MARKER}
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{CANDIDATE}`, `{REQUEST}`, `{MAT_MD}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** {TODAY}

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact and active diagnostic candidate: **{BUILD}**, SHA-256 `{PROFILE_SHA}`. Static, materialized applicability and semantic-equivalence validation are green; its runtime diagnostic is now outstanding.

## Active scope

Run the R2 ShyGuy-isolation diagnostic, ingest its fresh runtime log, and make an explicit diagnostic decision. Failed DIAG1 and R1 profiles must not be rerun unchanged.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the R2 diagnostic question is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.
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
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R2/`  
Plugin DLL SHA-256: `{PLUGIN_SHA}`  
Materialized validation: `{MAT_MD}`  
Runtime evidence required now: **yes, pending upload after gameplay**.

The machine index records R2 as `ACTIVE_RUNTIME_CANDIDATE_PENDING` with `runtime_evidence_required=false` until a final runtime decision exists; this sentinel means runtime evidence is intentionally deferred at the artifact-integrity layer, not that gameplay evidence is unnecessary.

## Failed predecessor diagnostics

S1.42AI-DIAG1 and S1.42AI-DIAG1R1 remain preserved as completed failed diagnostic evidence. R1 failure authority is `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md` with runtime evidence under `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the R2 diagnostic decision.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
"""
    (ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md").write_text(artifact_md, encoding="utf-8")

    map_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
    map_text = map_path.read_text(encoding="utf-8")
    map_text = re.sub(r"^<!-- LIVE_STATE:.*?-->$", MARKER, map_text, count=1, flags=re.M)
    anchor = f"""## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.

Latest built artifact and active diagnostic runtime candidate: **{BUILD} — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — NOT ACCEPTED**. Runtime test outstanding: **yes**. Candidate authority: `{CANDIDATE}`; repair/applicability contract: `{REQUEST}`; preserved guard contract: `{CONTRACT}`; materialized validation: `{MAT_MD}`.

`BuildSpecs/current.json` is disabled at `{IDLE_ID}`. `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD}` and `Current/AUTO_BUILD_RESULT.json.build_id = {BUILD}` identify the exact ready candidate for import and evidence attribution; ACTIVE_BUILD is not acceptance authority.

The next action is one R2 diagnostic gameplay run followed by the exact R2 log upload and repository-native ingestion. Failed DIAG1/R1 profiles must not be rerun unchanged. The ordinary S1.42AI full-normal BCMER ShyGuy acceptance gate remains explicitly deferred and not waived.
"""
    map_text, count = re.subn(r"## Current lifecycle anchor\n.*?(?=\n## Authority rule)", anchor, map_text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("Could not replace PROJECT_KNOWLEDGE_MAP lifecycle anchor exactly once")
    map_path.write_text(map_text, encoding="utf-8")

    map_json_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.json"
    map_json = json.loads(map_json_path.read_text(encoding="utf-8"))
    for topic in map_json.get("topics", []):
        if topic.get("id") == "active_candidate_and_next_test":
            aliases = list(topic.get("aliases", []))
            for alias in (BUILD, "DIAG1R2", "ShyGuy isolation applicability diagnostic"):
                if alias not in aliases:
                    aliases.append(alias)
            topic["aliases"] = aliases
            topic["last_validated"] = TODAY
    write_json("Current/PROJECT_KNOWLEDGE_MAP.json", map_json)


def main() -> int:
    verify_preconditions()
    write_candidate_records()
    update_machine_state()
    update_integrity()
    update_lineage()
    update_live_docs()
    print("PASS: staged exact S1.42AI-DIAG1R2 runtime-candidate activation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
