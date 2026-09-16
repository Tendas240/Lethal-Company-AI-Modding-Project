from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
R3 = "S1.42AI-DIAG1R3"
AI = "S1.42AI"
AH = "S1.42AH"
R3_SHA = "13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768"
AI_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
AH_SHA = "06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e"
RUNTIME = "RuntimeEvidence/S1.42AI-DIAG1R3/20260916T161243Z/"
RUNTIME_INDEX = RUNTIME + "INDEX.json"
RUNTIME_LOG_SHA = "37493170b9f6368bc4700161b8f0759ffaaff57925aed9784bec9a9a65c68084"
DECISION = "Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md"
R3_STATUS = "Current/Projektstatus_S1.42AI-DIAG1R3_RUNTIME_PASS.json"
MARKER = "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=S1.42AI runtime_test_outstanding=true -->"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def dump(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text.rstrip() + "\n", encoding="utf-8")


state = load("Current/CURRENT_STATE.json")
assert state["accepted_baseline"]["build_id"] == AH
assert state["latest_built_artifact"]["build_id"] == R3
assert state["latest_built_artifact"]["sha256"] == R3_SHA
assert state["active_candidate"]["build_id"] == R3
assert state["runtime_test_outstanding"] is True
assert state["controllers"]["runtime_active_build"] == R3
assert (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == R3
idx = load(RUNTIME_INDEX)
assert idx["build_id"] == R3
assert idx["files"][0]["sha256"] == RUNTIME_LOG_SHA
assert idx["files"][0]["size"] == 1466997

write(DECISION, f"""# S1.42AI-DIAG1R3 Runtime Diagnostic Decision — Exact Identity Repair

**Date:** 2026-09-16  
**Status:** DIAGNOSTIC RUNTIME PASS / EXACT SHYGUY IDENTITY + ISOLATION PROVEN / EXTERIOR VISIBILITY NOT EXERCISED / NOT GAMEPLAY ACCEPTED  
**Accepted gameplay baseline remains:** `S1.42AH`  
**Parent full-normal candidate:** `S1.42AI`

## Exact evidence

- Candidate: `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`
- Profile: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`
- Profile SHA-256: `{R3_SHA}`
- Runtime evidence: `{RUNTIME}`
- Runtime INDEX: `{RUNTIME_INDEX}`
- Raw `LogOutput.log` SHA-256: `{RUNTIME_LOG_SHA}`
- Raw log size: `1466997` bytes / `14603` lines

## Technical diagnostic result

The repaired R3 bytes satisfy the diagnostic purpose that failed in R2:

- `[DIAG1_OWNER_TYPE_DERIVED]` succeeds for `LethalMin.Pikmin.PikminType`.
- Dependency-absent EndlessElevator is cleanly classified as `[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]`.
- `[DIAG1_GUARD_LAYERS_INSTALLED]` arms all DIAG1-owned native/simple/complex guard layers without rollback.
- Startup/config assertions complete successfully.
- Exact identity resolves as `[DIAG1_IDENTITY_RESOLVED] asset='ShyGuyDef', enemyName='Shy guy', aiType='ShyGuy.AI.ShyGuyAI'`.
- The first pool guard permits only that exact ShyGuy identity and removes 37 indoor, 16 outside, 8 daytime and 1 weed non-allowed entries.
- No `[DIAG1_INVALID]`, `[DIAG1_INSTALL_ROLLED_BACK]`, `[DIAG1_IDENTITY_INVALID]` or `[DIAG1_ISOLATION_BYPASS]` is present in the completed run.
- The actual enemy-add path records only `ADDING ENEMY #1: Shy guy`.
- Known inherited loaforcsSoundAPI/HarmonyX `TypeLoadException` and SoftMask `NullReferenceException` signatures remain monitor-only under `Knowledge/MONITOR_ONLY_ERRORS.md`; no R3-local fatal/retry regression was established.

## Operator-visible observations

For this exact R3 run the operator reported:

- an interior ShyGuy was found and visibly rendered;
- no non-ShyGuy enemy was observed;
- no exterior ShyGuy was encountered;
- the ship-terminal `enemies` command was not repeated in this run.

The terminal command is not a mandatory R3 acceptance step and its omission does not invalidate the diagnostic. The no-non-ShyGuy observation is additionally supported by the R3 pool/spawn log evidence.

Exterior visibility is recorded exactly as **NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED**. It is neither claimed as passed nor treated as a diagnostic failure, because the R3 contract makes exterior visibility conditional on an exterior ShyGuy actually being encountered.

## Decision boundary

`S1.42AI-DIAG1R3` therefore **passes the temporary diagnostic gate** for exact ShyGuy identity resolution and ShyGuy-only isolation. It remains diagnostic evidence only and is not a gameplay baseline.

This decision does **not** accept `S1.42AI`. The deferred full-normal `S1.42AI` BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` is now reactivated and remains mandatory. `S1.42AH` remains the sole accepted gameplay baseline until that independent full-normal gate is explicitly decided.
""")

r3_status = {
    "schema_version": 1,
    "updated": "2026-09-16",
    "build_id": R3,
    "status": "RUNTIME_DIAGNOSTIC_PASS_EXACT_IDENTITY_ISOLATION_PROVEN_EXTERIOR_VISIBILITY_NOT_EXERCISED_NOT_ACCEPTED",
    "accepted_baseline": AH,
    "parent_full_normal": AI,
    "profile": "Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z",
    "sha256": R3_SHA,
    "candidate_record": "Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md",
    "runtime_decision": DECISION,
    "runtime_evidence": RUNTIME,
    "runtime_log_sha256": RUNTIME_LOG_SHA,
    "identity_result": "PASS_EXACT_SHYGUYDEF_SHY_GUY_SHYGUYAI_ORDINAL",
    "isolation_result": "PASS_NO_NON_SHYGUY_BYPASS_AND_ONLY_SHYGUY_ACTUAL_ADD",
    "interior_visibility_result": "PASS_VISIBLE_INTERIOR_SHYGUY_OBSERVED",
    "exterior_visibility_result": "NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED",
    "terminal_enemies_command": "NOT_REPEATED_NOT_REQUIRED_FOR_R3_GATE",
    "runtime_test_outstanding": False,
    "gameplay_accepted": False,
    "next_runtime_candidate": AI,
    "full_normal_s142ai_gate": "ACTIVE_RUNTIME_GATE_NOT_WAIVED",
}
dump(R3_STATUS, r3_status)

latest = state["latest_built_artifact"]
latest["status"] = "RUNTIME_DIAGNOSTIC_PASS_EXACT_IDENTITY_ISOLATION_PROVEN_EXTERIOR_VISIBILITY_NOT_EXERCISED_NOT_ACCEPTED"
latest["runtime_decision"] = DECISION
latest["runtime_evidence"] = RUNTIME
latest["runtime_log_sha256"] = RUNTIME_LOG_SHA
latest["project_status"] = R3_STATUS
latest["exterior_visibility_result"] = "NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED"

ai_candidate = {
    "build_id": AI,
    "title": "BCMER ShyGuy Interior-Only Event Correction",
    "status": "ACTIVE_FULL_NORMAL_RUNTIME_CANDIDATE_AFTER_DIAG1R3_PASS_NOT_ACCEPTED",
    "profile": "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z",
    "sha256": AI_SHA,
    "candidate_record": "Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md",
    "project_status": "Current/Projektstatus_S1.42AI_CANDIDATE.json",
    "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
    "profile_sources": "ProfileSources/S1.42AI/",
    "file_index": "ProfileSources/S1.42AI/FILE_INDEX.json",
    "workflow_run": 34496960816,
    "build_commit": "2dea753ec48ea2a8f417491ae9a13cf7a6d7b8b9",
    "static_evidence": "BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md",
    "parent": AH,
    "diagnostic_clearance": DECISION,
}
state["active_candidate"] = ai_candidate
state["runtime_test_outstanding"] = True
scope = state["selected_scope"]
scope["status"] = "FULL_NORMAL_S1_42AI_RUNTIME_ACTIVE_AFTER_DIAG1R3_PASS_NOT_ACCEPTED"
scope["finding"] = "S1.42AI-DIAG1R3 passed its exact-identity/ShyGuy-only isolation diagnostic on fresh runtime evidence. Interior ShyGuy visibility was observed; no non-ShyGuy enemy was observed or added; exterior ShyGuy visibility was not exercised because no exterior ShyGuy occurred. The temporary diagnostic path is complete. The independent full-normal S1.42AI BCMER ShyGuy gate is now active and remains required before acceptance."
scope["analysis_contract"] = "Runtime-validate S1.42AI under the full normal stack. Positively exercise the BCMER ShyGuy event, prove intended interior ShyGuy availability, verify no BCMER ShyGuy exterior spawn/list path and no exterior-AI marker from that event, preserve the enabled event, EventType, interior values, ordinary Scopophobia SpawnOutside=false contract and inherited S1.42AH behavior, and require no new project regression markers. Do not mix unrelated deferred scopes."
scope["analysis_status"] = "DIAG1R3_RUNTIME_PASS_FULL_NORMAL_S1_42AI_GATE_ACTIVE"
scope["candidate_build_id"] = AI
scope["profile"] = ai_candidate["profile"]
scope["sha256"] = AI_SHA
scope["candidate_record"] = ai_candidate["candidate_record"]
scope["project_status"] = ai_candidate["project_status"]
scope["static_evidence"] = ai_candidate["static_evidence"]
scope["diagnostic_result"] = {
    "build_id": R3,
    "status": "RUNTIME_DIAGNOSTIC_PASS_EXTERIOR_VISIBILITY_NOT_EXERCISED",
    "decision": DECISION,
    "runtime_evidence": RUNTIME,
    "runtime_log_sha256": RUNTIME_LOG_SHA,
    "exterior_visibility_result": "NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED",
}
scope["operator_observations"] = {
    "non_shyguy_enemies_observed": False,
    "visible_interior_shyguy_observed": True,
    "terminal_enemies_command_repeated": False,
    "terminal_enemies_command_required": False,
    "exterior_shyguy_observed": False,
    "exterior_visibility_result": "NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED",
}
scope["currently_irrelevant_actions"] = [
    "Do not rerun S1.42AI-DIAG1, R1, R2 or R3 unchanged; the diagnostic path is explicitly decided.",
    "Do not treat R3 diagnostic success as acceptance of S1.42AI; the full-normal S1.42AI gate is now active.",
    "Do not require another R3 run solely to force an exterior ShyGuy; exterior visibility remains explicitly not exercised.",
    "Do not broaden ShyGuy identity matching beyond the exact runtime-proven ordinal triple.",
    "Do not treat RuntimeInbox/ACTIVE_BUILD.txt as acceptance authority; it is runtime/evidence attribution only.",
]
scope["successor_build_id"] = AI
scope["build_request_record"] = None
scope["materialized_validation"] = None
state["next_action"] = "Import S1.42AI with the canonical Gale v2.4 replacement helper and run the full-normal BCMER ShyGuy runtime gate from Current/143. Positively obtain or force the BCMER ShyGuy event, confirm ShyGuy remains available through the intended interior event path, verify that BCMER adds no ShyGuy to the exterior path and that no 'ShyGuy(Clone) spawned outside; Switching to exterior AI' marker occurs from that event, then upload the complete fresh S1.42AI LogOutput.log with the build-specific uploader in Current/143. Do not accept S1.42AI from diagnostic success alone."
state["controllers"] = {
    "buildspec": "BuildSpecs/current.json",
    "build_enabled": False,
    "build_id": "IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION",
    "build_base_profile": ai_candidate["profile"],
    "build_base_sha256": AI_SHA,
    "runtime_active_build_file": "RuntimeInbox/ACTIVE_BUILD.txt",
    "runtime_active_build": AI,
}
dump("Current/CURRENT_STATE.json", state)

dump("BuildSpecs/current.json", {
    "enabled": False,
    "build_id": "IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION",
    "base_profile": ai_candidate["profile"],
    "base_sha256": AI_SHA,
    "output_profile": "Profiles/DO_NOT_BUILD.r2z",
    "profile_name": "DO_NOT_BUILD",
    "overwrite": False,
    "mod_state_changes": [],
    "mod_additions": [],
    "mod_removals": [],
    "config_patches": [],
    "local_plugin_builds": [],
    "text_assertions": [],
})
write("RuntimeInbox/ACTIVE_BUILD.txt", AI)
dump("Current/AUTO_BUILD_RESULT.json", {
    "build_id": AI,
    "profile_name": "LC V1 S1.42AI ShyGuy Interior Only",
    "base_profile": "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z",
    "base_sha256": AH_SHA,
    "output_profile": ai_candidate["profile"],
    "output_sha256": AI_SHA,
    "zip_members": 335,
    "changed_existing_members": ["BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg", "export.r2x"],
    "added_members": [],
    "mod_state_changes": [],
    "mod_additions": [],
    "mod_removals": [],
    "snapshot_dir": "ProfileSources/S1.42AI",
    "snapshot": {"entries": 335, "text_entries": 330},
})

ai_status = load("Current/Projektstatus_S1.42AI_CANDIDATE.json")
ai_status["date"] = "2026-09-16"
ai_status["active_runtime_candidate"]["status"] = "ACTIVE_FULL_NORMAL_RUNTIME_CANDIDATE_AFTER_DIAG1R3_PASS_NOT_ACCEPTED"
ai_status["controllers"] = {
    "buildspec_current_enabled": False,
    "buildspec_current_id": "IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION",
    "buildspec_base_profile": ai_candidate["profile"],
    "buildspec_base_sha256": AI_SHA,
    "runtime_active_build": AI,
    "successor_armed": False,
}
ai_status["exact_next_step"] = state["next_action"]
ai_status["diagnostic_revision"] = {
    "build_id": R3,
    "status": "RUNTIME_DIAGNOSTIC_PASS_EXTERIOR_VISIBILITY_NOT_EXERCISED",
    "decision": DECISION,
    "runtime_evidence": RUNTIME,
    "runtime_log_sha256": RUNTIME_LOG_SHA,
    "exterior_visibility_result": "NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED",
}
dump("Current/Projektstatus_S1.42AI_CANDIDATE.json", ai_status)

integ = load("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
pending = integ["pending_profiles"]
r3_items = [x for x in pending if x.get("build_id") == R3]
ai_items = [x for x in pending if x.get("build_id") == AI]
assert len(r3_items) == 1 and len(ai_items) == 1
r3_entry = r3_items[0]
pending.remove(r3_entry)
r3_entry["role"] = "RUNTIME_DIAGNOSTIC_PASS_NOT_GAMEPLAY_BASE"
r3_entry["project_status"] = R3_STATUS
r3_entry["decision"] = DECISION
r3_entry["runtime_index"] = RUNTIME_INDEX
r3_entry["runtime_log_sha256"] = RUNTIME_LOG_SHA
r3_entry["exterior_visibility_result"] = "NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED"
r3_entry.pop("runtime_evidence_required", None)
r3_entry.pop("partial_runtime_evidence_present", None)
r3_entry["note"] = "R3 runtime passed exact identity resolution and ShyGuy-only isolation. Interior ShyGuy visibility was observed; no non-ShyGuy enemy was observed; exterior visibility was not exercised because no exterior ShyGuy occurred. Diagnostic evidence only; not a gameplay base."
integ["profiles"].append(r3_entry)
ai_entry = ai_items[0]
ai_entry["role"] = "ACTIVE_RUNTIME_CANDIDATE_PENDING"
ai_entry["runtime_evidence_required"] = False
ai_entry["partial_runtime_evidence_present"] = False
ai_entry["note"] = "The diagnostic path is explicitly complete with R3 pass evidence. The independent full-normal S1.42AI BCMER ShyGuy runtime gate is now active and remains mandatory before acceptance."
integ["updated"] = "2026-09-16"
integ["last_validated"] = "2026-09-16"
integ.setdefault("verified_repository_api_observations", []).append(
    f"{R3} runtime diagnostic pass evidence is {RUNTIME} with raw LogOutput.log SHA-256 {RUNTIME_LOG_SHA}; exterior ShyGuy visibility was not exercised because no exterior ShyGuy occurred."
)
dump("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integ)

lineage = load("Current/BUILD_LINEAGE.json")
lineage["date"] = "2026-09-16"
lineage["active_candidate_build_id"] = AI
assert lineage["latest_built_artifact_id"] == R3
byid = {x["id"]: x for x in lineage["builds"]}
byid[AI]["status"] = "active-full-normal-runtime-candidate-not-accepted"
byid[AI]["principal_feature"] = "single-variable BCMER ShyGuy interior-only event correction; diagnostic repair path is complete and the independent full-normal runtime gate is now active"
r3l = byid[R3]
r3l["status"] = "runtime-diagnostic-pass-exterior-visibility-not-exercised"
r3l["decision_record"] = DECISION
r3l["project_status"] = R3_STATUS
r3l["runtime_evidence"] = RUNTIME
r3l["runtime_log_sha256"] = RUNTIME_LOG_SHA
r3l["principal_feature"] = "R3 proved exact runtime ShyGuy identity resolution and ShyGuy-only isolation; interior visibility observed, exterior visibility not exercised; diagnostic complete and full-normal S1.42AI gate reactivated"
dump("Current/BUILD_LINEAGE.json", lineage)

write("Knowledge/CURRENT_LIFECYCLE.md", f"""{MARKER}
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `{DECISION}`, `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`, `{R3_STATUS}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/Projektstatus_S1.42AI_CANDIDATE.json`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** 2026-09-16

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Latest built artifact / completed diagnostic

**S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — DIAGNOSTIC RUNTIME PASS / NOT GAMEPLAY ACCEPTED.**

R3 runtime evidence proves clean owner derivation, dependency-absent EndlessElevator `NOT_APPLICABLE`, guard-layer installation, exact `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` ordinal identity resolution and ShyGuy-only pool/spawn behavior without DIAG1 invalidation, rollback, identity failure or isolation bypass. The operator again saw a visible interior ShyGuy and no non-ShyGuy enemy. No exterior ShyGuy occurred, so exterior visibility remains **NOT_EXERCISED**, not passed or failed. The ship-terminal `enemies` command was not repeated and is not required by the R3 gate.

Decision: `{DECISION}`. Runtime: `{RUNTIME}`.

## Active candidate

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACTIVE FULL-NORMAL RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `{AI_SHA}`  
Candidate authority: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`

R3 diagnostic success only clears the temporary diagnostic question; it does not substitute for this independent full-normal gate.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R3** (completed diagnostic evidence).
- Active runtime candidate: **S1.42AI**.
- Runtime test outstanding: **yes — full-normal S1.42AI**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION`; no successor build is armed.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` controls the next runtime-evidence attribution and is not acceptance authority.
- `Current/AUTO_BUILD_RESULT.json.build_id = S1.42AI` identifies the exact artifact to import/test.

## Exact full-normal gate

Run `S1.42AI` under the full normal stack according to `Current/143...`: positively obtain or force the BCMER `ShyGuy` event; confirm intended interior ShyGuy availability; verify BCMER does not add ShyGuy to the exterior list/path and no `ShyGuy(Clone) spawned outside; Switching to exterior AI` marker is produced by that event; preserve exact BCMER 1.71.0/EventType values, ordinary Scopophobia `SpawnOutside=false`, inherited S1.42AH contracts and absence of new project regression markers.

## Exact next project action

{state['next_action']}
""")

km_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
km = km_path.read_text(encoding="utf-8")
km = re.sub(r"^<!-- LIVE_STATE:.*?-->$", MARKER, km, count=1, flags=re.M)
anchor = f"""## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.

Latest built artifact: **S1.42AI-DIAG1R3 — completed diagnostic runtime pass / not gameplay accepted**. Decision: `{DECISION}`; runtime evidence: `{RUNTIME}`. R3 proves the exact `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` ordinal identity and ShyGuy-only isolation. Interior visibility was observed; exterior visibility remains explicitly **not exercised** because no exterior ShyGuy occurred.

Active full-normal runtime candidate: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — NOT ACCEPTED**. Exact profile SHA-256: `{AI_SHA}`. Candidate authority: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`.

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION`. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` and `Current/AUTO_BUILD_RESULT.json.build_id = S1.42AI` identify the exact ready candidate for import/evidence attribution; ACTIVE_BUILD is not acceptance authority.

The next action is the full-normal S1.42AI runtime gate followed by the exact S1.42AI log upload and repository-native decision. Diagnostic success did not waive this gate."""
km, n = re.subn(r"## Current lifecycle anchor\n.*?(?=\n## Authority rule)", anchor, km, count=1, flags=re.S)
assert n == 1
write("Current/PROJECT_KNOWLEDGE_MAP.md", km)

write("Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md", f"""{MARKER}
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{DECISION}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-16

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1R3**, now completed diagnostic-pass evidence rather than an active candidate. Its exterior-visibility condition remains explicitly not exercised because no exterior ShyGuy occurred. Active full-normal runtime candidate: **S1.42AI**, SHA-256 `{AI_SHA}`.

## Active scope

Run the independent full-normal S1.42AI BCMER ShyGuy gate from `Current/143...`, then ingest the complete fresh S1.42AI log and make an explicit acceptance/rejection decision. R3 must not be rerun merely to force a rare exterior ShyGuy and must not be treated as S1.42AI acceptance.

## Remaining deferred independent scopes

- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
""")

write("Current/ARTIFACT_EVIDENCE_INTEGRITY.md", f"""{MARKER}
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-16

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `{AH_SHA}`

## Latest built artifact / completed diagnostic: S1.42AI-DIAG1R3

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `{R3_SHA}`  
Decision: `{DECISION}`  
Runtime evidence: `{RUNTIME}`  
Raw runtime log SHA-256: `{RUNTIME_LOG_SHA}`

R3 is completed diagnostic-pass evidence, not a gameplay base. It proves exact ShyGuy identity resolution and ShyGuy-only isolation. Interior visibility was positively observed. Exterior visibility is **NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED**.

## Active full-normal runtime candidate: S1.42AI

Artifact: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `{AI_SHA}`  
Candidate: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Readable snapshot: `ProfileSources/S1.42AI/`

The machine index records S1.42AI as `ACTIVE_RUNTIME_CANDIDATE_PENDING` with `runtime_evidence_required=false` until a final full-normal runtime decision exists. That sentinel does not make the gameplay gate optional.

## Completed failed diagnostic predecessors

DIAG1, DIAG1R1 and DIAG1R2 remain preserved as explicit failed diagnostic evidence. R3 supersedes their repair questions; they must not be rerun unchanged.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
""")

bl_path = ROOT / "Current/BUILD_LINEAGE.md"
bl = bl_path.read_text(encoding="utf-8")
bl = bl.replace("**Last-Validated:** 2026-09-15", "**Last-Validated:** 2026-09-16", 1)
head = """## Current lineage head

- **Accepted gameplay baseline:** S1.42AH — Mouth Dog Pikmin Dual Prevention — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact:** S1.42AI-DIAG1R3 — completed diagnostic runtime pass / not gameplay accepted.
- **Active candidate:** S1.42AI — full-normal BCMER ShyGuy Interior-Only Event Correction / not accepted.
- **Diagnostic result:** R3 exact identity and ShyGuy-only isolation passed; exterior visibility was not exercised because no exterior ShyGuy occurred.
- **Current action:** run the independent full-normal S1.42AI gate from `Current/143...`, then ingest and decide that build.
"""
bl, n = re.subn(r"## Current lineage head\n.*?(?=\nFor live lifecycle state)", head, bl, count=1, flags=re.S)
assert n == 1
old_parentage = "- S1.42AI remains unaccepted; its full-normal BCMER ShyGuy runtime gate is deferred but not waived while the DIAG1 repair path is resolved."
new_parentage = "- S1.42AI remains unaccepted; the DIAG1 repair path is now explicitly complete via `Current/151...`, and its independent full-normal BCMER ShyGuy runtime gate is active and not waived."
assert old_parentage in bl
bl = bl.replace(old_parentage, new_parentage, 1)
old_feature = "| ShyGuy isolation diagnostic owner-type resolution repair, runtime-proved but later complex-owner failure | S1.42AI-DIAG1R1 / `Current/147...` |"
assert old_feature in bl
bl = bl.replace(old_feature, old_feature + "\n| ShyGuy exact-identity/isolation diagnostic completed; exterior visibility not exercised | S1.42AI-DIAG1R3 / `Current/151...` |", 1)
write("Current/BUILD_LINEAGE.md", bl)

print("PASS: prepared R3 diagnostic decision and full-normal S1.42AI activation")
