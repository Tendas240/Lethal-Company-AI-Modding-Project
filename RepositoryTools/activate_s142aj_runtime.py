#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-09-17"
BUILD = "S1.42AJ"
TITLE = "LC Office V81 Integration"
PROFILE = "Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z"
PROFILE_NAME = "LC V1 S1.42AJ LC Office V81 Integration"
PROFILE_SHA = "7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba"
BASE_BUILD = "S1.42AI"
BASE_PROFILE = "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
BASE_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
BUILD_RUN = 35222275686
BUILD_RUN_HEAD = "cbf25e05a75b8d6f3153cfa3a6bca0df396ad677"
BUILD_COMMIT = "7fbaae92523637ae3fec6c1e242ec2538918e7b7"
CANDIDATE = "Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md"
PROJECT_STATUS = "Current/Projektstatus_S1.42AJ_CANDIDATE.json"
STATIC_STATUS = "Current/Projektstatus_S1.42AJ_STATIC_VALIDATED.json"
BUILD_PLAN = "BuildSpecs/S1.42AJ_PLAN.md"
STATIC_EVIDENCE = "BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md"
MARKER = "<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->"
IDLE_ID = "IDLE_AFTER_S1.42AJ_BUILD_AWAITING_RUNTIME_VALIDATION"


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, obj: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_marker(text: str) -> str:
    if not re.search(r"^<!-- LIVE_STATE:.*?-->$", text, re.M):
        raise RuntimeError("live-state marker missing")
    return re.sub(r"^<!-- LIVE_STATE:.*?-->$", MARKER, text, count=1, flags=re.M)


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    s = text.index(start)
    e = text.index(end, s)
    return text[:s] + replacement.rstrip() + "\n\n" + text[e:]


def ready_commands() -> tuple[str, str]:
    gale = "$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content"
    uploader = r'''$src=Join-Path $env:APPDATA 'com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AJ LC Office V81 Integration\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw "Log not found: $src"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api "repos/$repo/contents/$dst" --jq '.sha' 2>$null);$p=@{message='Upload S1.42AJ runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT "repos/$repo/contents/$dst" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}'''
    return gale, uploader


def verify_preconditions() -> None:
    state = load_json("Current/CURRENT_STATE.json")
    if state.get("accepted_baseline", {}).get("build_id") != BASE_BUILD:
        raise RuntimeError("accepted baseline drifted")
    latest = state.get("latest_built_artifact", {})
    if latest.get("build_id") != BUILD or latest.get("profile") != PROFILE or latest.get("sha256") != PROFILE_SHA:
        raise RuntimeError("latest artifact is not exact S1.42AJ")
    if latest.get("status") != "STATIC_VALIDATED_NOT_RUNTIME_ARMED":
        raise RuntimeError("S1.42AJ is not in exact pre-activation status")
    if state.get("active_candidate") is not None or state.get("runtime_test_outstanding") is not False:
        raise RuntimeError("activation requires no current candidate and no outstanding runtime test")
    selected = state.get("selected_scope", {})
    if selected.get("scope_id") != "LC_OFFICE_V81_INTEGRATION" or selected.get("built_build_id") != BUILD:
        raise RuntimeError("selected LC Office scope drifted")
    if "ready for runtime arming" not in state.get("next_action", "").lower():
        raise RuntimeError("CURRENT_STATE no longer requests S1.42AJ runtime arming")

    buildspec = load_json("BuildSpecs/current.json")
    if buildspec.get("enabled") is not False or buildspec.get("build_id") != "IDLE_AFTER_S1.42AJ_STATIC_VALIDATION_READY_FOR_RUNTIME_ARMING":
        raise RuntimeError("BuildSpecs is not exact pre-activation idle state")
    if buildspec.get("base_profile") != BASE_PROFILE or buildspec.get("base_sha256") != BASE_SHA:
        raise RuntimeError("BuildSpecs accepted-base guard drifted")
    if any(buildspec.get(k) for k in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "local_plugin_builds", "text_assertions")):
        raise RuntimeError("disabled BuildSpecs unexpectedly contains mutations")

    auto = load_json("Current/AUTO_BUILD_RESULT.json")
    if auto.get("build_id") != BUILD or auto.get("output_profile") != PROFILE or auto.get("output_sha256") != PROFILE_SHA:
        raise RuntimeError("AUTO_BUILD_RESULT is not exact S1.42AJ")
    if auto.get("base_profile") != BASE_PROFILE or auto.get("base_sha256") != BASE_SHA:
        raise RuntimeError("AUTO_BUILD_RESULT parent binding drifted")
    if (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() != BASE_BUILD:
        raise RuntimeError("runtime attribution drifted before activation")

    static = load_json(STATIC_STATUS)
    if static.get("build_id") != BUILD or static.get("status") != "STATIC_VALIDATED_NOT_RUNTIME_ARMED" or static.get("sha256") != PROFILE_SHA:
        raise RuntimeError("static project-status authority drifted")
    if static.get("build_workflow_run") != BUILD_RUN or static.get("build_commit") != BUILD_COMMIT:
        raise RuntimeError("static project-status build provenance drifted")

    for rel in (PROFILE, "ProfileSources/S1.42AJ/FILE_INDEX.json", "ProfileSources/S1.42AJ/export.r2x", STATIC_EVIDENCE, BUILD_PLAN, CANDIDATE):
        if not (ROOT / rel).is_file():
            raise RuntimeError(f"missing S1.42AJ artifact/evidence: {rel}")
    if (ROOT / PROJECT_STATUS).exists():
        raise RuntimeError("active S1.42AJ project-status record already exists")


def update_machine_state() -> None:
    state = load_json("Current/CURRENT_STATE.json")
    latest = dict(state["latest_built_artifact"])
    latest["status"] = "STATIC_VALIDATED_RUNTIME_VALIDATION_OUTSTANDING"
    latest["project_status"] = PROJECT_STATUS
    state["latest_built_artifact"] = latest

    active = dict(latest)
    active["status"] = "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
    state["active_candidate"] = active
    state["runtime_test_outstanding"] = True

    selected = state["selected_scope"]
    selected["status"] = "BUILT_ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
    selected["candidate_build_id"] = BUILD
    selected["profile"] = PROFILE
    selected["sha256"] = PROFILE_SHA
    selected["candidate_record"] = CANDIDATE
    selected["project_status"] = PROJECT_STATUS
    selected["build_plan"] = BUILD_PLAN
    selected["static_evidence"] = STATIC_EVIDENCE
    selected["analysis_contract"] = (
        "Runtime-validate S1.42AJ under the full normal stack using the LC Office acceptance contract: exact modern IAmBatby LLL ownership, "
        "single LC Office registration, at least one default/unforced viable moon, final effective viable-pool rarity 100 whenever viable, actual LC Office generation/traversal, "
        "elevator and breaker/power behavior where available, healthy enemy navigation and scrap generation, inherited accepted contracts, and no new critical regression/error flood. "
        "Do not mix universal-moon availability or another deferred Interior scope into S1.42AJ."
    )
    selected["next_action"] = (
        "Import S1.42AJ with the canonical Gale v2.4 replacement helper, perform the full-normal LC Office runtime acceptance gate, then upload the complete fresh S1.42AJ LogOutput.log."
    )
    state["next_action"] = (
        "Import S1.42AJ with the canonical Gale v2.4 replacement helper and run the full-normal LC Office runtime acceptance gate from Current/153 and BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md. "
        "Prove startup/ownership, single registration, default LLL viability on at least one tested moon, final effective rarity 100 whenever viable, actual LC Office generation and traversal, elevator behavior, breaker/power where available, ordinary enemy navigation and scrap generation, inherited accepted contracts, and no new critical regression/error flood. "
        "Then upload the complete fresh S1.42AJ LogOutput.log. Do not accept S1.42AJ from static/build success alone."
    )
    c = state["controllers"]
    c["build_id"] = IDLE_ID
    c["build_base_profile"] = PROFILE
    c["build_base_sha256"] = PROFILE_SHA
    c["runtime_active_build"] = BUILD
    write_json("Current/CURRENT_STATE.json", state)

    buildspec = load_json("BuildSpecs/current.json")
    buildspec["build_id"] = IDLE_ID
    buildspec["base_profile"] = PROFILE
    buildspec["base_sha256"] = PROFILE_SHA
    write_json("BuildSpecs/current.json", buildspec)
    (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD + "\n", encoding="utf-8")


def write_candidate_authorities() -> None:
    gale, uploader = ready_commands()
    candidate = f"""# S1.42AJ Build Candidate — LC Office V81 Integration

**Date:** {TODAY}  
**Status:** BUILD PASS / STATIC DELTA VERIFIED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED  
**Accepted gameplay baseline:** `S1.42AI`

## Candidate identity

- Build: `{BUILD}`
- Profile: `{PROFILE}`
- SHA-256: `{PROFILE_SHA}`
- Parent: `{BASE_BUILD}` / `{BASE_SHA}`
- Build workflow run: `{BUILD_RUN}`
- Build commit: `{BUILD_COMMIT}`
- Build plan: `{BUILD_PLAN}`
- Static evidence: `{STATIC_EVIDENCE}`
- Readable snapshot: `ProfileSources/S1.42AJ/`
- File index: `ProfileSources/S1.42AJ/FILE_INDEX.json`

## Proven static boundary

The built export contains exactly the authorized compatibility-first package delta: LC Office `2.3.4`, V81 compatibility fix `2.0.0`, DestroyItemInSlotFix `1.0.0`, and DungeonGenerationPlus `1.5.0 -> 1.5.1`. Every unrelated package block and every non-export profile member is unchanged. `IAmBatby-LethalLevelLoader 1.7.12` remains the sole LLL owner, `pacoito-LethalLevelLoaderUpdated` remains absent, and the accepted Interior Weight Normalization DLL remains byte-identical.

Universal LC Office moon availability and all unrelated deferred Interior scopes remain excluded from this candidate.

## Full-normal runtime acceptance gate

Runtime acceptance requires all of the following:

1. normal BepInEx -> main menu -> lobby startup with no duplicate LLL owner and no `LethalLevelLoaderUpdated` load;
2. LC Office registers exactly once with modern IAmBatby LLL;
3. LLL reports LC Office viable on at least one tested moon under the candidate's unforced/default matching contract;
4. the project-local final effective viable-pool marker shows LC Office at exactly `100` whenever it is returned viable;
5. an actual LC Office dungeon is selected and generation completes without softlock/fatal error;
6. the player can enter and traverse the generated office;
7. LC Office elevator functionality is exercised successfully;
8. breaker/power interaction is exercised successfully where available;
9. ordinary enemy spawning/navigation inside the office is healthy, including door/elevator pathing where practical to exercise;
10. ordinary scrap/interior generation remains healthy;
11. inherited accepted gameplay contracts remain healthy, including Interior Weight Normalization and Mouth Dog/Pikmin behavior;
12. no new project-critical regression or persistent error flood appears.

If natural equal-weight selection does not produce LC Office, an isolated diagnostic force-selection mechanism may be used for coverage, but it must not become part of the balanced candidate.

## Exact ready-to-test commands

Repository-driven Gale v2.4 replacement/import one-liner:

```powershell
{gale}
```

Exact S1.42AJ runtime-log uploader:

```powershell
{uploader}
```

## Acceptance boundary

S1.42AI remains the sole accepted gameplay baseline until this full-normal runtime gate passes and a later explicit decision promotes S1.42AJ.
"""
    (ROOT / CANDIDATE).write_text(candidate, encoding="utf-8")

    accepted = load_json("Current/CURRENT_STATE.json")["accepted_baseline"]
    project = {
        "schema_version": 4,
        "date": TODAY,
        "repository_is_source_of_truth": True,
        "accepted_baseline": accepted,
        "active_runtime_candidate": load_json("Current/CURRENT_STATE.json")["active_candidate"],
        "runtime_gate": {
            "normal_startup_and_lobby": "MUST_PASS",
            "sole_iambatby_lll_owner": "MUST_PASS",
            "deprecated_lll_fork_load": "MUST_BE_0",
            "lc_office_registration_count": "MUST_BE_EXACTLY_1",
            "default_unforced_viability_on_tested_moon": "MUST_OBSERVE_AT_LEAST_1",
            "final_effective_rarity_when_viable": 100,
            "actual_office_generation": "MUST_PASS",
            "office_traversal": "MUST_PASS",
            "elevator_functionality": "MUST_PASS",
            "breaker_power_where_available": "MUST_EXERCISE_WHERE_AVAILABLE",
            "enemy_spawn_navigation": "MUST_REMAIN_HEALTHY",
            "scrap_interior_generation": "MUST_REMAIN_HEALTHY",
            "inherited_accepted_contracts": "MUST_REMAIN_HEALTHY",
            "project_critical_regression_or_error_flood": "MUST_BE_0"
        },
        "static_gate": {
            "parent": BASE_BUILD,
            "profile_sha256": PROFILE_SHA,
            "package_delta_only": True,
            "sole_lll_owner": "IAmBatby-LethalLevelLoader 1.7.12",
            "deprecated_fork_absent": True,
            "interior_normalizer_byte_preserved": True,
            "static_evidence": STATIC_EVIDENCE
        },
        "controllers": {
            "buildspec_current_enabled": False,
            "buildspec_current_id": IDLE_ID,
            "buildspec_base_profile": PROFILE,
            "buildspec_base_sha256": PROFILE_SHA,
            "runtime_active_build": BUILD,
            "successor_armed": False
        },
        "exact_next_step": load_json("Current/CURRENT_STATE.json")["next_action"]
    }
    write_json(PROJECT_STATUS, project)


def update_integrity() -> None:
    integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
    if any(p.get("build_id") == BUILD for p in integrity.get("pending_profiles", [])):
        raise RuntimeError("S1.42AJ already appears as pending profile")
    if any(p.get("build_id") == BUILD for p in integrity.get("profiles", [])):
        raise RuntimeError("S1.42AJ unexpectedly appears as completed profile")
    integrity["updated"] = TODAY
    integrity.setdefault("pending_profiles", []).append({
        "build_id": BUILD,
        "role": "ACTIVE_RUNTIME_CANDIDATE_PENDING",
        "profile": PROFILE,
        "profile_sha256": PROFILE_SHA,
        "profile_sources": "ProfileSources/S1.42AJ/",
        "file_index": "ProfileSources/S1.42AJ/FILE_INDEX.json",
        "export": "ProfileSources/S1.42AJ/export.r2x",
        "candidate_record": CANDIDATE,
        "project_status": PROJECT_STATUS,
        "build_plan": BUILD_PLAN,
        "static_evidence": STATIC_EVIDENCE,
        "runtime_evidence_required": False,
        "partial_runtime_evidence_present": False
    })
    integrity["last_validated"] = TODAY
    write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

    md = f"""{MARKER}
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** {TODAY}

## Accepted gameplay baseline: S1.42AI

Artifact: `{BASE_PROFILE}`  
SHA-256: `{BASE_SHA}`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

## Active runtime candidate: S1.42AJ

Artifact: `{PROFILE}`  
SHA-256: `{PROFILE_SHA}`  
Candidate: `{CANDIDATE}`  
Static evidence: `{STATIC_EVIDENCE}`  
Readable snapshot: `ProfileSources/S1.42AJ/`

S1.42AJ is pending full-normal runtime validation. It has no runtime evidence claim yet. S1.42AI remains the accepted completed gameplay profile.

## Completed diagnostic evidence: S1.42AI-DIAG1R3

R3 remains completed diagnostic-pass evidence only. It is not a gameplay baseline and does not replace the full-normal S1.42AI acceptance evidence.

## Pending runtime candidates

Exactly one: **S1.42AJ** with role `ACTIVE_RUNTIME_CANDIDATE_PENDING`.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
"""
    (ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md").write_text(md, encoding="utf-8")


def update_lineage() -> None:
    lineage = load_json("Current/BUILD_LINEAGE.json")
    if lineage.get("current_accepted_build_id") != BASE_BUILD or lineage.get("latest_built_artifact_id") != BUILD:
        raise RuntimeError("build lineage head drifted")
    lineage["active_candidate_build_id"] = BUILD
    found = False
    for item in lineage.get("builds", []):
        if item.get("id") == BUILD:
            item["status"] = "active-runtime-candidate-not-accepted"
            item["project_status"] = PROJECT_STATUS
            item["principal_feature"] = "compatibility-first LC Office V81 integration; static validated and now active for full-normal runtime acceptance; universal-moon availability remains deferred"
            found = True
            break
    if not found:
        raise RuntimeError("S1.42AJ missing from build lineage")
    write_json("Current/BUILD_LINEAGE.json", lineage)

    path = ROOT / "Current/BUILD_LINEAGE.md"
    text = path.read_text(encoding="utf-8")
    old = "- **Latest built artifact:** S1.42AJ — LC Office V81 Integration — static validated / runtime not armed.\n- **Active candidate:** none; no runtime test is outstanding.\n- **Current action:** arm S1.42AJ as the sole runtime candidate in a separate lifecycle transition; no runtime test is outstanding yet."
    new = "- **Latest built artifact:** S1.42AJ — LC Office V81 Integration — static validated / active runtime candidate / not accepted.\n- **Active candidate:** S1.42AJ; full-normal runtime validation is outstanding.\n- **Current action:** import/test exact S1.42AJ under the LC Office acceptance contract and upload the fresh runtime log."
    if old not in text:
        raise RuntimeError("BUILD_LINEAGE current-head text drifted")
    text = text.replace(old, new, 1)
    text = text.replace("| S1.42AJ | **STATIC VALIDATED / RUNTIME NOT ARMED** |", "| S1.42AJ | **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** |", 1)
    text = text.replace("- Runtime: not armed / no runtime evidence yet", "- Runtime: armed / full-normal validation outstanding / no runtime evidence yet", 1)
    path.write_text(text, encoding="utf-8")


def update_live_docs() -> None:
    lifecycle = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
    text = replace_marker(lifecycle.read_text(encoding="utf-8"))
    start = "## Latest built artifact"
    end = "## Scope boundary"
    replacement = f"""## Latest built artifact

**S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** is the latest built artifact.

Profile: `{PROFILE}`  
SHA-256: `{PROFILE_SHA}`  
Candidate record: `{CANDIDATE}`  
Static evidence: `{STATIC_EVIDENCE}`

The static gate proves the exact compatibility-first package delta, sole modern IAmBatby LLL ownership, absence of the deprecated fork, no unrelated package drift, and byte-identical accepted Interior Weight Normalization.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest built artifact: **S1.42AJ**.
- Active runtime candidate: **S1.42AJ**.
- Runtime test outstanding: **yes**.
- Selected successor scope: **LC Office V81 Integration — active runtime candidate**.
- `BuildSpecs/current.json` is disabled at `{IDLE_ID}`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` controls runtime-evidence attribution only.

## Exact next project action

Import S1.42AJ with the canonical Gale v2.4 replacement helper, execute the full-normal LC Office runtime acceptance gate from `{CANDIDATE}` and `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`, then upload the complete fresh S1.42AJ `LogOutput.log`. Do not accept S1.42AJ from static/build success alone.
"""
    text = replace_section(text, start, end, replacement)
    lifecycle.write_text(text, encoding="utf-8")

    roadmap = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
    text = replace_marker(roadmap.read_text(encoding="utf-8"))
    text = text.replace("There is no active runtime candidate and no outstanding runtime test. S1.42AJ has passed static validation but is not runtime-armed; `RuntimeInbox/ACTIVE_BUILD.txt` therefore remains S1.42AI.", "S1.42AJ is the sole active runtime candidate and full-normal runtime validation is outstanding. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` provides runtime-evidence attribution; S1.42AI remains the accepted gameplay baseline.", 1)
    text = text.replace("**LC Office V81 Integration — S1.42AJ built / static validated / runtime not armed.**", "**LC Office V81 Integration — S1.42AJ built / static validated / active runtime candidate.**", 1)
    text = text.replace("Static validation is complete; the next separate lifecycle action is runtime arming to prove LC Office registration/viability/generation/traversal/elevator behavior.", "Static validation and runtime arming are complete; the outstanding gate is full-normal runtime proof of LC Office registration/viability/generation/traversal/elevator behavior and the rest of the canonical acceptance contract.", 1)
    roadmap.write_text(text, encoding="utf-8")

    interiors = ROOT / "Knowledge/INTERIORS_AND_LLL.md"
    text = interiors.read_text(encoding="utf-8")
    text = text.replace("LC Office V81 Integration is the currently selected compatibility/integration scope under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`. It is **selected but not armed**; `BuildSpecs/current.json` remains disabled and there is no runtime test outstanding.", "LC Office V81 Integration is the currently selected compatibility/integration scope under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`. Exact S1.42AJ is **built, static validated and armed as the sole active runtime candidate**; `BuildSpecs/current.json` remains disabled and full-normal runtime validation is outstanding.", 1)
    text = text.replace("Planned package contract:", "S1.42AJ package contract (statically verified):", 1)
    text = text.replace("The initial compatibility candidate must not simultaneously force LC Office onto all moons. First prove registration, default/modern-LLL viability, effective normalization to `100`, actual dungeon generation, traversal, elevator/power behavior and ordinary enemy navigation.", "The active compatibility candidate does not force LC Office onto all moons. Runtime must now prove registration, default/modern-LLL viability, effective normalization to `100`, actual dungeon generation, traversal, elevator/power behavior and ordinary enemy navigation.", 1)
    interiors.write_text(text, encoding="utf-8")

    km = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
    text = replace_marker(km.read_text(encoding="utf-8"))
    anchor_start = "## Current lifecycle anchor"
    anchor_end = "## Authority rule"
    anchor = f"""## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK**, SHA-256 `{BASE_SHA}`. Latest built artifact and sole active runtime candidate: **S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**, SHA-256 `{PROFILE_SHA}`.

S1.42AH remains accepted predecessor/rollback provenance. The S1.42AI-DIAG1/R1/R2/R3 chain remains diagnostic evidence only.

`BuildSpecs/current.json` is disabled at `{IDLE_ID}`. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` is runtime-evidence attribution only. Full-normal LC Office runtime validation is outstanding.

The next action is to import exact S1.42AJ via the canonical Gale v2.4 workflow, execute the LC Office acceptance gate, and upload the complete fresh S1.42AJ runtime log. Universal-moon availability and all unrelated Interior scopes remain deferred.
"""
    text = replace_section(text, anchor_start, anchor_end, anchor)
    km.write_text(text, encoding="utf-8")


def update_plan_statuses() -> None:
    deferred = ROOT / "BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md"
    text = deferred.read_text(encoding="utf-8")
    text = text.replace("**Status:** SELECTED / PREPARATION / NOT ARMED", "**Status:** IMPLEMENTED AS S1.42AJ / STATIC VALIDATED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED", 1)
    old = "The S1.42AI package/dependency baseline verification is complete and the minimal delta is fixed above. The next action is to read `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Current/BUILD_LINEAGE.md`, determine the next successor build ID and exact `BuildSpecs/current.json` schema, and prepare exactly one LC Office successor from exact accepted S1.42AI. Keep `BuildSpecs/current.json` disabled until that successor spec is complete; do not arm a runtime test until the built candidate passes static validation."
    new = "The S1.42AI package/dependency baseline verification, S1.42AJ build/static gate, and separate runtime-arming transition are complete. S1.42AJ is the sole active runtime candidate. The outstanding action is the full-normal runtime acceptance gate above, followed by repository-native log ingestion and an explicit acceptance/rejection decision."
    if old not in text:
        raise RuntimeError("deferred-plan arming paragraph drifted")
    deferred.write_text(text.replace(old, new, 1), encoding="utf-8")

    plan = ROOT / BUILD_PLAN
    text = plan.read_text(encoding="utf-8")
    text = text.replace("**Status:** PREPARED / ONE-SHOT BUILD REQUEST PENDING MERGE", "**Status:** BUILT / STATIC VALIDATED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED", 1)
    text = text.replace("`BuildSpecs/current.json` remains in its canonical disabled idle state in the reviewable PR. After merge, `.github/workflows/s142aj-lc-office-v81-build-request.yml` performs the repository-native one-shot atomic build request: it verifies the exact idle/base guards, writes the enabled S1.42AJ controller on `main`, removes itself, commits that transient request, and dispatches the canonical profile-build workflow. Static validation and runtime activation remain separate follow-up gates.", "S1.42AJ has been built repository-natively from exact accepted S1.42AI, passed its static compatibility/package gate, and is now armed as the sole active runtime candidate. `BuildSpecs/current.json` remains disabled and guarded to exact S1.42AJ while runtime validation is outstanding.", 1)
    text = text.replace("Only after this static gate passes may S1.42AJ become an active runtime candidate and `RuntimeInbox/ACTIVE_BUILD.txt` be moved to S1.42AJ. A runtime test is not armed by this plan alone.", "The static gate passed and a separate lifecycle transition armed S1.42AJ. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ`; full-normal runtime validation is outstanding and acceptance still requires an explicit later decision.", 1)
    text = text.replace("If S1.42AJ later passes static validation and is explicitly armed for runtime, use the acceptance contract already defined", "S1.42AJ is statically validated and explicitly armed for runtime. Use the acceptance contract already defined", 1)
    plan.write_text(text, encoding="utf-8")


def main() -> int:
    verify_preconditions()
    update_machine_state()
    write_candidate_authorities()
    update_integrity()
    update_lineage()
    update_live_docs()
    update_plan_statuses()
    print("PASS: prepared exact S1.42AJ runtime-candidate lifecycle transition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
