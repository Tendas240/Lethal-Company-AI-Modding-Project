#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import re

BUILD = "S1.42AI"
TITLE = "BCMER ShyGuy Interior-Only Event Correction"
PROFILE = "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
PARENT = "S1.42AH"
PARENT_PROFILE = "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z"
PARENT_SHA = "06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e"
BUILD_COMMIT = "2dea753ec48ea2a8f417491ae9a13cf7a6d7b8b9"
WORKFLOW_RUN = 34496960816
CANDIDATE_RECORD = "Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md"
PROJECT_STATUS = "Current/Projektstatus_S1.42AI_CANDIDATE.json"
BUILD_PLAN = "BuildSpecs/S1.42AI_PLAN.md"
STATIC_EVIDENCE = "BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md"
LIVE = "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, obj, compact=False):
    if compact:
        text = json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n"
    else:
        text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    Path(path).write_text(text, encoding="utf-8")


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


assert sha256(PROFILE) == SHA
result = load("BuildSpecs/S1.42AI_BUILD_EVIDENCE/AUTO_BUILD_RESULT.json")
assert result["build_id"] == BUILD
assert result["base_profile"] == PARENT_PROFILE
assert result["base_sha256"] == PARENT_SHA
assert result["output_profile"] == PROFILE
assert result["output_sha256"] == SHA
assert result["zip_members"] == 335
assert set(result["changed_existing_members"]) == {
    "export.r2x",
    "BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg",
}
assert result["added_members"] == []
assert result["mod_state_changes"] == []
assert result["mod_additions"] == []
assert result["mod_removals"] == []
assert Path(STATIC_EVIDENCE).is_file()
assert Path("ProfileSources/S1.42AI/FILE_INDEX.json").is_file()
assert Path("ProfileSources/S1.42AI/export.r2x").is_file()
assert not Path(CANDIDATE_RECORD).exists()
assert not Path(PROJECT_STATUS).exists()

state = load("Current/CURRENT_STATE.json")
assert state["accepted_baseline"]["build_id"] == PARENT
assert state["accepted_baseline"]["sha256"] == PARENT_SHA
assert state["active_candidate"] is None
assert state["runtime_test_outstanding"] is False

# Latest build provenance.
dump("Current/AUTO_BUILD_RESULT.json", result)
Path("Current/AUTO_BUILD_RESULT.md").write_text(
    "# Automated profile build result - S1.42AI\n\n"
    "- Profile: LC V1 S1.42AI ShyGuy Interior Only\n"
    f"- Base: {PARENT_PROFILE}\n"
    f"- Base SHA-256: {PARENT_SHA}\n"
    f"- Output: {PROFILE}\n"
    f"- Output SHA-256: {SHA}\n"
    "- ZIP members: 335\n"
    "- Text snapshot: ProfileSources/S1.42AI (330 readable files)\n\n"
    "## Changed existing members\n\n"
    "- BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg\n"
    "- export.r2x\n\n"
    "## Added members\n\n"
    "- none\n",
    encoding="utf-8",
)

controller = {
    "enabled": False,
    "build_id": "IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION",
    "base_profile": PROFILE,
    "base_sha256": SHA,
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
dump("BuildSpecs/current.json", controller)
Path("RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD + "\n", encoding="utf-8")

plan_path = Path(BUILD_PLAN)
plan = plan_path.read_text(encoding="utf-8")
plan = plan.replace(
    "**Status:** PRE-BUILD / PREPARED / NOT ARMED / NOT YET BUILT  ",
    "**Status:** BUILT / STATIC-VERIFIED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED",
    1,
)
plan = plan.replace(
    "**Status:** PRE-BUILD / PREPARED / NOT ARMED / NOT YET BUILT",
    "**Status:** BUILT / STATIC-VERIFIED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED",
    1,
)
if "## Static build result" not in plan:
    plan += (
        "\n## Static build result\n\n"
        f"- Built profile: `{PROFILE}`\n"
        f"- SHA-256: `{SHA}`\n"
        f"- Build checkpoint commit: `{BUILD_COMMIT}`\n"
        f"- Build workflow run: `{WORKFLOW_RUN}`\n"
        f"- Static evidence: `{STATIC_EVIDENCE}`\n"
        "- Changed existing archive members: exactly `export.r2x` and `BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`.\n"
        "- Added/removed members: none.\n"
        "- Runtime status: active candidate; explicit gameplay validation is still required before acceptance.\n"
    )
plan_path.write_text(plan, encoding="utf-8")

next_step = (
    "Import S1.42AI with the canonical Gale v2.4 replacement helper and run the full-normal BCMER ShyGuy runtime gate from Current/143. "
    "Positively obtain or force the BCMER ShyGuy event, confirm ShyGuy remains available through the intended interior event path, verify that BCMER adds no ShyGuy to the exterior path and that no 'ShyGuy(Clone) spawned outside; Switching to exterior AI' marker occurs from that event, then upload the complete fresh S1.42AI LogOutput.log with the build-specific uploader in Current/143. "
    "Do not accept S1.42AI from static/build success alone."
)

candidate = {
    "build_id": BUILD,
    "title": TITLE,
    "status": "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED",
    "profile": PROFILE,
    "sha256": SHA,
    "candidate_record": CANDIDATE_RECORD,
    "project_status": PROJECT_STATUS,
    "build_plan": BUILD_PLAN,
    "profile_sources": "ProfileSources/S1.42AI/",
    "file_index": "ProfileSources/S1.42AI/FILE_INDEX.json",
    "workflow_run": WORKFLOW_RUN,
    "build_commit": BUILD_COMMIT,
    "static_evidence": STATIC_EVIDENCE,
    "parent": PARENT,
}
latest = dict(candidate)
latest["status"] = "BUILD_PASS_STATIC_DELTA_VERIFIED_RUNTIME_VALIDATION_OUTSTANDING"

state["schema_version"] = max(int(state.get("schema_version", 0)), 8)
state["updated"] = "2026-09-10"
state["latest_built_artifact"] = latest
state["active_candidate"] = candidate
state["runtime_test_outstanding"] = True
state["selected_scope"] = {
    "scope_id": "BCMER_SHYGUY_INTERIOR_ONLY_CORRECTION",
    "title": TITLE,
    "status": "BUILT_ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED",
    "accepted_baseline": PARENT,
    "plan": "BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md",
    "topic_authority": "Knowledge/BCMER.md",
    "runtime_finding": "RuntimeEvidence/S1.42AH/20260908T202138Z/",
    "finding": "S1.42AI is built directly from accepted S1.42AH with an exact static single-config delta: only export.r2x profile identity and the BCMER ModdedEvents.cfg member changed, and the semantic config delta is exactly the three ShyGuy exterior values set to zero. Every other archive member is byte-identical to S1.42AH, including Scopophobia.cfg. Runtime validation is now required before any acceptance.",
    "analysis_contract": "Runtime-validate S1.42AI as the active candidate under the full normal stack. Positively exercise the BCMER ShyGuy event, prove intended interior ShyGuy availability, verify no BCMER ShyGuy exterior spawn/list path and no exterior-AI marker from that event, preserve the enabled event, EventType, interior values, ordinary Scopophobia SpawnOutside=false contract and inherited S1.42AH behavior, and require no new project regression markers. Do not mix unrelated deferred scopes.",
    "candidate_build_id": BUILD,
    "profile": PROFILE,
    "sha256": SHA,
    "candidate_record": CANDIDATE_RECORD,
    "project_status": PROJECT_STATUS,
    "build_plan": BUILD_PLAN,
    "static_evidence": STATIC_EVIDENCE,
}
state["next_action"] = next_step
state["controllers"] = {
    "buildspec": "BuildSpecs/current.json",
    "build_enabled": False,
    "build_id": controller["build_id"],
    "build_base_profile": PROFILE,
    "build_base_sha256": SHA,
    "runtime_active_build_file": "RuntimeInbox/ACTIVE_BUILD.txt",
    "runtime_active_build": BUILD,
}
dump("Current/CURRENT_STATE.json", state)

uploader = r'''$src=Join-Path $env:APPDATA 'com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AI ShyGuy Interior Only\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $src)){throw "Log not found: $src"};$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1};if(!$gh){winget install --id GitHub.cli -e --source winget --accept-package-agreements --accept-source-agreements;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh){$gh=@("$env:ProgramFiles\GitHub CLI\gh.exe","$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe","${env:ProgramFiles(x86)}\GitHub CLI\gh.exe")|Where-Object{$_ -and (Test-Path -LiteralPath $_)}|Select-Object -First 1}};if(!$gh){throw 'GitHub CLI gh.exe could not be found after resolution/install attempt'};& $gh auth status --hostname github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login --hostname github.com --git-protocol https --web;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dst='RuntimeInbox/Current/LogOutput.log';$sha=(& $gh api "repos/$repo/contents/$dst" --jq '.sha' 2>$null);$p=@{message='Upload S1.42AI runtime log';content=[Convert]::ToBase64String([IO.File]::ReadAllBytes($src));branch='main'};if($sha){$p['sha']=$sha};($p|ConvertTo-Json -Compress)|& $gh api --method PUT "repos/$repo/contents/$dst" --input -;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}'''

candidate_md = f'''# S1.42AI Build Candidate — BCMER ShyGuy Interior-Only Event Correction

**Date:** 2026-09-10
**Status:** BUILD PASS / STATIC DELTA VERIFIED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED
**Accepted gameplay baseline:** `S1.42AH`

## Candidate identity

- Build: `S1.42AI`
- Profile: `{PROFILE}`
- SHA-256: `{SHA}`
- Parent: `S1.42AH`
- Build checkpoint commit: `{BUILD_COMMIT}`
- Build workflow run: `{WORKFLOW_RUN}`
- Build plan: `{BUILD_PLAN}`
- Static evidence: `{STATIC_EVIDENCE}`

## Exact static delta

Relative to accepted S1.42AH, the only changed existing archive members are:

1. `export.r2x` — profile identity only;
2. `BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`.

There are no added or removed archive members and no package-state changes. The semantic `ModdedEvents.cfg` delta is exactly:

```text
ShyGuyDef OutsideEnemyRarity = 10, 0.4, 10, 50 -> 0, 0, 0, 0
ShyGuyDef MinOutsideEnemy = 1, 0.02, 1, 3 -> 0, 0, 0, 0
ShyGuyDef MaxOutsideEnemy = 2, 0.04, 2, 6 -> 0, 0, 0, 0
```

The `[ShyGuy]` event remains enabled, retains `Event Type = VeryBad`, and keeps all three interior values unchanged. Every other archive member is byte-identical to S1.42AH, including `BepInEx/config/Scopophobia.cfg`; ordinary Scopophobia `SpawnOutside = false` is therefore preserved.

## Runtime acceptance gate

Run S1.42AI under the full normal stack and deliberately obtain or force the BCMER `ShyGuy` event. Acceptance requires all of the following:

1. positively observe the `ShyGuy` event being selected/executed;
2. positively observe ShyGuy remaining available through the intended interior event path;
3. observe no ShyGuy being added/spawned through the BCMER exterior list/path;
4. observe no `ShyGuy(Clone) spawned outside; Switching to exterior AI` marker attributable to that event;
5. retain exact BCMER 1.71.0 and the accepted EventType architecture;
6. retain ordinary Scopophobia `SpawnOutside = false` behavior and inherited S1.42AH contracts;
7. require no new project-patch errors, known regression-marker burst, fatal or retry flood attributable to this delta.

The disappearance of the prior invisible exterior symptom is useful corroboration, but the exact renderer/material cause was never proven and is not part of the acceptance claim.

## Exact ready-to-test commands

Canonical Gale v2.4 replacement/import one-liner:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

After the test, upload the complete fresh S1.42AI log with this exact self-contained one-liner:

```powershell
{uploader}
```

## Acceptance boundary

S1.42AI is build-safe and static-delta-verified only. S1.42AH remains the sole accepted gameplay baseline until this runtime gate passes and a later explicit runtime decision promotes S1.42AI.
'''
Path(CANDIDATE_RECORD).write_text(candidate_md, encoding="utf-8")

project_status = {
    "schema_version": 4,
    "date": "2026-09-10",
    "repository_is_source_of_truth": True,
    "accepted_baseline": state["accepted_baseline"],
    "active_runtime_candidate": candidate,
    "runtime_gate": {
        "bcmer_1_71_0": "MUST_LOAD_EXACT",
        "shyguy_event_selected_executed": "MUST_OBSERVE",
        "interior_shyguy_available": "MUST_OBSERVE",
        "bcmer_shyguy_exterior_spawn_or_list": "MUST_BE_0",
        "shyguy_exterior_ai_marker_from_event": "MUST_BE_0",
        "scopophobia_ordinary_spawnoutside": "MUST_REMAIN_FALSE",
        "inherited_s1_42ah_contracts": "MUST_REMAIN_FUNCTIONAL",
        "project_patch_errors": "MUST_BE_0",
        "fatal_or_retry_flood": "MUST_BE_0",
    },
    "archive_gate": {
        "parent": PARENT,
        "changed_existing_members": [
            "BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg",
            "export.r2x",
        ],
        "added_members": [],
        "removed_members": [],
        "unrelated_members_byte_preserved": True,
        "profile_sha256": SHA,
        "static_evidence": STATIC_EVIDENCE,
    },
    "controllers": {
        "buildspec_current_enabled": False,
        "buildspec_current_id": controller["build_id"],
        "buildspec_base_profile": PROFILE,
        "buildspec_base_sha256": SHA,
        "runtime_active_build": BUILD,
        "successor_armed": False,
    },
    "exact_next_step": next_step,
}
dump(PROJECT_STATUS, project_status)

integrity = load("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
assert not any(x.get("build_id") == BUILD for x in integrity.get("profiles", []))
pending = [x for x in integrity.get("pending_profiles", []) if x.get("build_id") != BUILD]
pending.append({
    "build_id": BUILD,
    "role": "ACTIVE_RUNTIME_CANDIDATE_PENDING",
    "profile": PROFILE,
    "profile_sha256": SHA,
    "profile_sources": "ProfileSources/S1.42AI/",
    "file_index": "ProfileSources/S1.42AI/FILE_INDEX.json",
    "export": "ProfileSources/S1.42AI/export.r2x",
    "candidate_record": CANDIDATE_RECORD,
    "project_status": PROJECT_STATUS,
    "build_plan": BUILD_PLAN,
    "static_evidence": STATIC_EVIDENCE,
    "runtime_evidence_required": False,
    "partial_runtime_evidence_present": False,
})
integrity["pending_profiles"] = pending
integrity["updated"] = "2026-09-10"
integrity["last_validated"] = "2026-09-10"
dump("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity, compact=True)

Path("Current/ARTIFACT_EVIDENCE_INTEGRITY.md").write_text(f'''{LIVE}
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`
**Last-Validated:** 2026-09-10

## Accepted gameplay baseline: S1.42AH

Artifact: `{PARENT_PROFILE}`
SHA-256: `{PARENT_SHA}`
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`
Final decisive evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

S1.42AH remains the accepted full-normal-stack gameplay base while the independent ShyGuy correction is runtime-validated.

## Latest built artifact / active runtime candidate: S1.42AI

Artifact: `{PROFILE}`
SHA-256: `{SHA}`
Candidate record: `{CANDIDATE_RECORD}`
Project status: `{PROJECT_STATUS}`
Build plan: `{BUILD_PLAN}`
Static evidence: `{STATIC_EVIDENCE}`
Readable snapshot: `ProfileSources/S1.42AI/`

S1.42AI is build-pass and static-delta-verified. Runtime validation is outstanding, so it is indexed in `pending_profiles` with `runtime_evidence_required=false` until a final explicit acceptance or rejection decision exists.

The exact static delta from S1.42AH changes only `export.r2x` and `BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`; the semantic config change is exactly the three `[ShyGuy]` exterior values set to zero. Every other archive member is byte-identical to S1.42AH, including `Scopophobia.cfg`.

## Preserved accepted/rejected evidence chain

S1.42AH retains its three-stage runtime evidence chain and remains the accepted baseline. S1.42AF remains an accepted historical predecessor/rollback point. S1.42AG remains `RUNTIME_REJECTED_PARTIAL_FIX` and is not a gameplay/build base.

## Retrieval invariant

No future decision may depend only on opaque `.r2z`, DLL or giant-log bytes. A reasoning-critical fact must also exist in readable `ProfileSources`, `FILE_INDEX`, runtime `INDEX`/analysis, source, build record, or canonical documentation. The pending S1.42AI entry deliberately contains no runtime-log claim before the user performs the authorized runtime gate.
''', encoding="utf-8")

lineage = load("Current/BUILD_LINEAGE.json")
lineage["date"] = "2026-09-10"
lineage["current_accepted_build_id"] = PARENT
lineage["active_candidate_build_id"] = BUILD
lineage["latest_built_artifact_id"] = BUILD
builds = lineage.get("builds", [])
assert not any(x.get("id") == BUILD for x in builds)
builds.append({
    "id": BUILD,
    "title": TITLE,
    "status": "active-runtime-candidate",
    "parent": PARENT,
    "profile": PROFILE,
    "sha256": SHA,
    "build_plan": BUILD_PLAN,
    "candidate_record": CANDIDATE_RECORD,
    "decision_record": CANDIDATE_RECORD,
    "project_status": PROJECT_STATUS,
    "workflow_run": WORKFLOW_RUN,
    "build_commit": BUILD_COMMIT,
    "static_evidence": STATIC_EVIDENCE,
    "safe_as_gameplay_base": False,
    "principal_feature": "single-variable BCMER ShyGuy interior-only event correction; three exterior event values zeroed while all interior/event/type and Scopophobia contracts remain unchanged",
})
lineage["builds"] = builds
lineage.setdefault("feature_index", {})["BCMER_ShyGuy_interior_only_event_correction"] = BUILD
dump("Current/BUILD_LINEAGE.json", lineage)

lineage_md_path = Path("Current/BUILD_LINEAGE.md")
lm = lineage_md_path.read_text(encoding="utf-8")
lm = lm.replace("**Last-Validated:** 2026-09-09", "**Last-Validated:** 2026-09-10", 1)
old_head = '''- **Accepted gameplay baseline:** S1.42AH — Mouth Dog Pikmin Dual Prevention — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact:** S1.42AH.
- **Active candidate:** none.
- **Accepted predecessor / rollback point:** S1.42AF — Path-Length-Safe Microwave Packaging.
- **Next build:** none armed; BCMER ShyGuy interior-only successor preparation is next.'''
new_head = '''- **Accepted gameplay baseline:** S1.42AH — Mouth Dog Pikmin Dual Prevention — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact:** S1.42AI — BCMER ShyGuy Interior-Only Event Correction.
- **Active candidate:** S1.42AI — **RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**.
- **Accepted predecessor / rollback point:** S1.42AF — Path-Length-Safe Microwave Packaging.
- **Current gate:** run the S1.42AI full-normal BCMER ShyGuy runtime validation from `Current/143`.'''
assert old_head in lm
lm = lm.replace(old_head, new_head, 1)
ahrow = "| S1.42AH | **ACCEPTED CURRENT BASELINE** | Dual exact MouthDog adapter + Vanilla Pikmin collision prevention; targeted runtime preserved player, reverse Pikmin lifecycle and final non-Pikmin EnemyAI neighbor behavior. |"
airow = "| S1.42AI | **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** | Single-variable BCMER ShyGuy interior-only correction from accepted S1.42AH; exact static delta verified, runtime gate outstanding. |"
assert ahrow in lm
lm = lm.replace(ahrow, ahrow + "\n" + airow, 1)
lineage_md_path.write_text(lm, encoding="utf-8")

Path("Knowledge/CURRENT_LIFECYCLE.md").write_text(f'''{LIVE}
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `{CANDIDATE_RECORD}`, `{STATIC_EVIDENCE}`, `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`
**Last-Validated:** 2026-09-10

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**

Profile: `{PARENT_PROFILE}`
Profile SHA-256: `{PARENT_SHA}`
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`
Final decisive runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

S1.42AH remains the sole accepted gameplay base. Its MouthDog/Pikmin scope is closed and inherited unchanged by the new config-only candidate.

## Latest built artifact / active candidate

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**

Profile: `{PROFILE}`
Profile SHA-256: `{SHA}`
Parent: `S1.42AH`
Candidate: `{CANDIDATE_RECORD}`
Project status: `{PROJECT_STATUS}`
Static evidence: `{STATIC_EVIDENCE}`

Static verification proves exactly two changed existing archive members: `export.r2x` and `BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`. The semantic config delta is exactly the three ShyGuy exterior values changed to `0, 0, 0, 0`. All interior ShyGuy event values, EventType, event enable state, package state and every unrelated archive member are preserved; `Scopophobia.cfg` is byte-identical to S1.42AH.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI**.
- Active candidate: **S1.42AI**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION` and guards the exact S1.42AI profile/SHA.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` is the runtime/evidence-attribution pointer.
- S1.42AI is not accepted until an explicit runtime decision closes the gate.

## Canonical Gale workflow

Use the repository-driven **v2.4** Gale replacement path in `Knowledge/GALE_PROFILE_WORKFLOW.md`, implemented by `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`. For this candidate, pair it with the exact S1.42AI runtime-log uploader recorded in `{CANDIDATE_RECORD}`, as required by `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`.

## Exact next project action

{next_step}
''', encoding="utf-8")

Path("Current/PROJECT_KNOWLEDGE_MAP.md").write_text(f'''{LIVE}
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-09-10

Before performing project work, read and follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. Route normal questions through the registered canonical topic; current lifecycle facts come from `Current/CURRENT_STATE.json` plus that topic, not old handovers.

## Immediate routing

| User question / topic | Topic ID | Canonical source |
|---|---|---|
| How must ChatGPT execute project work? | `chatgpt_segmented_execution` | `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` |
| What is accepted/active and what happens next? | `accepted_baseline`, `active_candidate_and_next_test` | `Knowledge/CURRENT_LIFECYCLE.md` |
| How do I hand the project to a new ChatGPT chat? | `chat_handover` | `Current/HANDOVER_PREPARATION_PROMPT.md` |
| How are profiles built and logs ingested? | `build_pipeline`, `runtime_upload_and_ingest` | `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` |
| How do I replace/import the active Gale profile? | `gale_import` | `Knowledge/GALE_PROFILE_WORKFLOW.md` |
| Which BCMER rules are current? | `bcmer` | `Knowledge/BCMER.md` |
| How do interiors/LLL/CullFactory work? | `interiors_and_lll` | `Knowledge/INTERIORS_AND_LLL.md` |
| What is the enemy-spawn baseline? | `enemy_spawn_baseline` | `Knowledge/ENEMY_SPAWN_BASELINE.md` |
| How should Pikmin interact with enemies/Mouth Dog? | `pikmin_enemy_compatibility` | `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md` |
| What are the Jetpack values? | `jetpack` | `Knowledge/JETPACK.md` |
| How is CodeRebirth configured? | `coderebirth` | `Knowledge/CODEREBIRTH.md` |
| What are Microwave/Snail values? | `functional_microwave`, `immortal_snail` | `Knowledge/ITEM_TUNING.md` |
| Which errors are monitor-only? | `monitor_only_errors` | `Knowledge/MONITOR_ONLY_ERRORS.md` |
| What is the Black Mesa/Pikmin routing problem? | `black_mesa_pikmin_routing` | `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md` |
| What remains on the roadmap? | `roadmap_and_deferred_scopes` | `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md` |
| What rules govern local patches? | `patch_safety_policy` | `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` |
| Which build introduced/rejected/fixed something? | `build_lineage` | `Current/BUILD_LINEAGE.md` |

## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.

Latest built artifact and active runtime candidate: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — NOT ACCEPTED**. Runtime validation is outstanding. Candidate authority: `{CANDIDATE_RECORD}`; static evidence: `{STATIC_EVIDENCE}`.

`BuildSpecs/current.json` is disabled and guards S1.42AI; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` attributes the next runtime evidence to the candidate.

The exact next action is the S1.42AI full-normal BCMER ShyGuy runtime gate: positively exercise the event, preserve interior ShyGuy behavior and prove the BCMER exterior path/marker is absent. Use `Knowledge/CURRENT_LIFECYCLE.md` and `{CANDIDATE_RECORD}` for the exact test/upload contract.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
''', encoding="utf-8")

Path("Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md").write_text(f'''{LIVE}
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC
**Authority:** live selected/deferred-scope list only
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{CANDIDATE_RECORD}`, `{STATIC_EVIDENCE}`, `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`
**Last-Validated:** 2026-09-10

## Current position

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**, SHA-256 `{PARENT_SHA}`.

Latest built artifact and active runtime candidate: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction**, SHA-256 `{SHA}`. Runtime validation is outstanding; S1.42AI is not yet accepted.

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION`; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI`.

## Active independent scope — S1.42AI BCMER ShyGuy interior-only correction

S1.42AI implements the previously selected config-only correction directly from accepted S1.42AH. Static verification proves the only semantic gameplay/config change is the `[ShyGuy]` exterior triplet becoming zero while Event Enabled, EventType, all three interior values and ordinary Scopophobia `SpawnOutside = false` remain unchanged. Every unrelated archive member is byte-identical to S1.42AH.

The current gate is runtime-only: positively execute the BCMER ShyGuy event, prove intended interior ShyGuy availability, and prove BCMER does not create an exterior ShyGuy or emit the prior exterior-AI marker from that event. Exact authority is `{CANDIDATE_RECORD}`.

The earlier user-observed invisible exterior ShyGuy remains a symptom whose exact renderer/material mechanism was not proven; S1.42AI claims only to correct the proven BCMER exterior-spawn configuration defect.

## Remaining deferred independent scopes

- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation; treat inside -> outside transition compatibility separately and do not enable ordinary Scopophobia `SpawnOutside` merely to emulate escape behavior.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible user-facing evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.

## Repository-integrity boundary

Handover/governance repair must preserve gameplay artifacts/controllers and pass the permanent Knowledge Architecture gates before final handover. Historical planning files do not override this live roadmap.
''', encoding="utf-8")

bp = Path("Knowledge/BCMER.md")
bt = bp.read_text(encoding="utf-8")
bt = bt.replace("**Last-Validated:** 2026-09-09", "**Last-Validated:** 2026-09-10", 1)
replacement = f'''## ShyGuy event exterior-spawn guard — S1.42AI active runtime candidate

S1.42AH runtime evidence `RuntimeEvidence/S1.42AH/20260908T202138Z/` proved that BCMER event `ShyGuy` could create `ShyGuy(Clone) spawned outside; Switching to exterior AI` even while ordinary Scopophobia v1.3.4 retained `SpawnOutside = false`.

S1.42AI is now built directly from accepted S1.42AH to correct only that proven event configuration defect. Its exact static evidence is `{STATIC_EVIDENCE}` and its active candidate authority is `{CANDIDATE_RECORD}`.

The S1.42AI `[ShyGuy]` event retains `Event Enabled? = true`, `Event Type = VeryBad`, and all three accepted interior values, while the exterior triplet is exactly:

```text
ShyGuyDef OutsideEnemyRarity = 0, 0, 0, 0
ShyGuyDef MinOutsideEnemy = 0, 0, 0, 0
ShyGuyDef MaxOutsideEnemy = 0, 0, 0, 0
```

`Scopophobia.cfg` is byte-identical to accepted S1.42AH, so ordinary `SpawnInside = true` / `SpawnOutside = false` ownership is preserved. No package state or unrelated BCMER event changed.

Runtime validation is now outstanding and must positively exercise the BCMER ShyGuy event, preserve intended interior ShyGuy availability, and prove no BCMER exterior ShyGuy path/marker from that event. The exact renderer/material cause of the prior invisible exterior symptom remains unproven and must not be overstated.

The deferred `woah25-LethalEscapeUpdated 2.5.0` evaluation remains separate: inside -> outside transition compatibility is not equivalent to ordinary exterior spawning and must not be emulated by changing Scopophobia `SpawnOutside`.

Full contract: `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`.
'''
bt, n = re.subn(
    r"## ShyGuy event exterior-spawn guard — confirmed correction pending\n.*?(?=\n## Accepted equal EventType static model)",
    replacement.rstrip(),
    bt,
    flags=re.S,
)
assert n == 1
bp.write_text(bt, encoding="utf-8")

dp = Path("BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md")
dt = dp.read_text(encoding="utf-8")
dt = dt.replace(
    "**Status:** DEFERRED / CONFIRMED RUNTIME DEFECT / NOT ARMED  ",
    "**Status:** IMPLEMENTED AS S1.42AI / STATIC-VERIFIED / RUNTIME VALIDATION PENDING",
    1,
)
dt = dt.replace("**Last-Validated:** 2026-09-09", "**Last-Validated:** 2026-09-10", 1)
lifecycle = f'''## Lifecycle / provenance boundary

The S1.42AH MouthDog lifecycle gate is closed and S1.42AH remains the accepted gameplay baseline. This independent correction has been implemented as active runtime candidate S1.42AI without modifying S1.42AH bytes or readable snapshot.

S1.42AI profile: `{PROFILE}`
SHA-256: `{SHA}`
Static evidence: `{STATIC_EVIDENCE}`
Candidate authority: `{CANDIDATE_RECORD}`

The pending decision is now runtime-only. Do not mix LC Office, CullFactory, fog, Black Mesa, LethalEscape or other deferred scopes into S1.42AI. A final acceptance/rejection must preserve S1.42AH as the rollback/provenance base until S1.42AI explicitly passes.

This preserves provenance while ensuring the defect is not lost.
'''
dt, n = re.subn(
    r"## Lifecycle / provenance boundary\n.*?(?=\n## Validation contract for the future corrected build)",
    lifecycle.rstrip(),
    dt,
    flags=re.S,
)
assert n == 1
dt = dt.replace("## Validation contract for the future corrected build", "## Validation contract for S1.42AI", 1)
dp.write_text(dt, encoding="utf-8")

print("Atomic S1.42AI candidate state authored.")
