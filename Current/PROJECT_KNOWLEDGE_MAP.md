<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-09-17

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

Accepted gameplay baseline: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK**, SHA-256 `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`. Latest balanced built artifact and sole active runtime candidate/evidence target: **S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**, SHA-256 `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`.

S1.42AH remains accepted predecessor/rollback provenance. The S1.42AI-DIAG1/R1/R2/R3 chain remains diagnostic evidence only.

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AJ_BUILD_AWAITING_RUNTIME_VALIDATION`. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` is runtime-evidence attribution only. Full-normal LC Office runtime validation remains outstanding, but `RuntimeEvidence/S1.42AJ/20260917T171109Z/` already proves unforced Offense viability (`LC Office (65)`) and final normalized effective rarity `100`; that run selected Facility rather than LC Office.

The strictly diagnostic **S1.42AJ-DIAG1** artifact is already published from exact S1.42AJ and statically verified, profile SHA-256 `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`. Its publication/static evidence is under `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/` and its readable snapshot is `ProfileSources/S1.42AJ-DIAG1/`. It is **not armed**, is not acceptance authority, and has no runtime evidence yet.

The next action is the separate atomic runtime/lifecycle activation of S1.42AJ-DIAG1 so its diagnostic run is attributed correctly, followed by exact-head CI verification and then the runtime instructions with the repository-driven Gale import one-liner plus the exact S1.42AJ-DIAG1 one-line log uploader in the same response. The test scope is only actual LC Office generation/traversal/elevator/power/enemy-navigation/scrap coverage on Offense after normal viability. Balanced S1.42AJ remains unchanged and not accepted. Universal-moon availability and all unrelated Interior scopes remain deferred.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
