<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R1 candidate=none runtime_test_outstanding=false -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-09-14

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

Latest built artifact: **S1.42AI-DIAG1R1 — ShyGuy Isolation Diagnostic Owner Type Resolution Repair — RUNTIME DIAGNOSTIC FAILED / ENDLESSELEVATOR APPLICABILITY REPAIR LANDED / NOT ACCEPTED**. There is **no active runtime candidate** and no new runtime test is outstanding. Historical failure authority: `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`; runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`; landed repair evidence: `AnalysisEvidence/S1.42AI-DIAG1R1/ENDLESS_ELEVATOR_APPLICABILITY.md`.

R1 proved the repaired metadata-derived owner type path works, then failed because it treated `ElevatorMod.Patches.EndlessElevator` as unconditionally required. Repository-native evidence proved the exact LethalMin compat dependency is BepInEx GUID `kite.ZelevatorCode`: dependency absent means only that compat target is `NOT_APPLICABLE`; dependency present keeps the exact provider/owner/signature/install contract REQUIRED and fail-closed. PR #91 landed this permanent repair on `main` at `ef3842e5e1766afdd5db77c232b34c0e7c7d3105`.

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R1_APPLICABILITY_REPAIR_LANDED_AWAITING_SUCCESSOR_DETERMINATION` and guards accepted S1.42AH. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R1` remains evidence-attribution metadata only.

The next action is to verify the canonical Current/Lifecycle transition on the final `main` Exact-HEAD `Knowledge Architecture` gate. Only after that gate is green may the repository-native successor diagnostic question be determined. Do not build or request gameplay yet. The ordinary S1.42AI full-normal BCMER ShyGuy acceptance gate remains explicitly deferred and not waived.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
