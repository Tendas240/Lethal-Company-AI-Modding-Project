<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-09-29

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

Accepted gameplay baseline: **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**. Active gameplay candidate / latest built gameplay artifact: **S1.42AK-BMDSFIX1 — not accepted**.

The selected **Universal Interior Viability / Equal Availability** scope remains in Phase C3. The fixed Phase-B3 30x53 availability/effective-weight matrix remains an unchanged historical snapshot at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`; pair-specific Phase-C evidence does not rewrite those historical classifications.

The already-ingested External-moon pair evidence that can be reconciled without a new run is now exhausted. Black Mesa has dedicated current pair records for Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation. Greenhouse is the full bounded pair-specific runtime-compatibility PASS; the other records retain narrower topology/traversal boundaries. No additional already-ingested Black Mesa pair is available for the same evidence-only reconciliation path. Decision: `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md`.

Oxyde remains governed by `SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md`: 23 selection-supported metadata pairings exist, but exact V81 skips ordinary dungeon generation while `spawnEnemiesAndScrap=false`, and no independent inspected dungeon/entrance-construction path is established. Those metadata matches are not executable ordinary pair proof.

BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT** and is no longer runtime-active. Runtime/evidence routing remains exact `S1.42AK-BMDSFIX1`. BMDSFIX1 remains the separate active gameplay candidate / **NOT ACCEPTED**; its regular exact-byte Black Mesa x `DeepSewersFlow` qualification remains passive, outstanding and unwaived, with no dedicated reroll released. `BuildSpecs/current.json` remains disabled.

Exact next action: perform the bounded repository-native Phase-C3 **External owner-rule applicability reconciliation** across the 53 selectable interiors using existing source/owner/config evidence only. Classify which current rules legitimately target Black Mesa External semantics without duplicate registration, preserve Oxyde's ordinary-generation boundary, and determine whether C3 can close with an explicit Oxyde exception plus a supported Black Mesa applicability set or whether a narrowly defined additional evidence requirement remains. No runtime/build or universal availability override is authorized by this step.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
