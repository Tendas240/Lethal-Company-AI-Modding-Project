<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER  
**Authority:** primary human topic router for repository knowledge  
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`  
**Current State:** `Current/00_CURRENT_STATE.md`  
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Last-Validated:** 2026-09-08

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

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging**.

Latest built artifact / active candidate: **S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / EXTENDED PARTIAL RUNTIME PASS / FINAL NON-PIKMIN NEIGHBOR REMAINDER OUTSTANDING / NOT ACCEPTED**.

Runtime test outstanding: **yes**. S1.42AH remains neither accepted nor rejected; `BuildSpecs/current.json` is disabled; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`; no successor is armed.

`Current/140` proves first-run installation/collision/player preservation. `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md` advances the runtime gate by proving explicit native Pikmin -> MouthDog attack/death/unlatch/task cleanup, corpse carry, live adapter prevention, preserved noise response and clean known project regression markers.

The exact next action is only the final **MouthDog/Paw -> non-Pikmin `EnemyAI` / native `BiteKillEnemyAI` pass-through** remainder documented in `Current/141`. Do not rebuild or repeat already-proven S1.42AH coverage first.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.