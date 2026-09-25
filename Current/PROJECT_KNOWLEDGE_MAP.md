<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-09-25

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

Acceptance authority: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`. Full-normal runtime evidence is `RuntimeEvidence/S1.42AK/20260918T172838Z/` with raw log SHA-256 `cc0f0a7a6c6a76ad44266aded11ff9cb2aca21f2623f5fb895d371ad778526b9`. The first attempt in that session was aborted before interior entry. The played second attempt naturally selected Spooky Manor and supplied roughly three minutes of interior coverage without a hostile enemy sighting; that is a documented coverage limitation, not a proven spawn regression.

The targeted LC Office camera-render A/B remains supplied by completed diagnostic-only S1.42AJ-DIAG2 evidence. The later LC Office Scrap Quantity/Distribution Investigation is complete with no gameplay delta under `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`. S1.42AK remains accepted/latest and unchanged.

**Universal Interior Viability / Equal Availability is the selected scope.** Phases A through C2 remain complete with the fixed 30×53 matrix unchanged at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`.

Both exact Black Mesa x Greenhouse diagnostic attempts remain completed failed diagnostic evidence. BMGHDIAG2 is ingested at `RuntimeEvidence/S1.42AK-BMGHDIAG2/20260924T124542Z/` and refused before arming on `EntranceTeleport manifest module identity mismatch`, so Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

The pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation remains the **active gameplay candidate / not accepted**. Its exact Black Mesa x Substation run remains the first preserved regular non-target control. The identity-only `S1.42AK-BMDSFIX1-DIAG1PATH1` successor supplied successful supporting Black Mesa x `DeepSewersFlow` evidence at `RuntimeEvidence/S1.42AK-BMDSFIX1-DIAG1PATH1/20260925T085104Z/` (raw log SHA-256 `ec7631dc6baa3ef6cff502767d56356fe62943b362271f45add8807381a63ae4`): selector ARMED and `pool=31->1`, BMDSFIX1 ARMED, target `APPLIED 4.875->1`, final multiplier 1, completed dungeon generation and normal post-generation gameplay; the user reported no atmosphere-screen problem or noticeable issue. Decision authority: `Current/186_S1.42AK_BMDSFIX1_DIAG1PATH1_RUNTIME_SUPPORTING_PASS.md`.

A later **regular exact-byte** BMDSFIX1 run is ingested at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260925T092937Z/` with raw log SHA-256 `936858e50ec27fcbca9ca09b1b863ca1940d860ea3d44d2b5623431e221b9b6e`. Black Mesa returned a normalized 31-flow viable pool including `Deep Sewers(100)`, but naturally selected `Expanded facility`. Generation completed and the user reported normal landing, acceptable atmosphere-screen duration, normal movement and no noticeable entrance/exit issue. This is an additional clean regular non-target control only; decision authority: `Current/187_S1.42AK_BMDSFIX1_REGULAR_EXPANDED_FACILITY_NON_TARGET_CONTROL.md`.

DIAG1PATH1 remains diagnostic support only / **NEVER ACCEPT** and cannot qualify BMDSFIX1 because the deterministic selector DLL was present. Runtime/evidence routing is exact `S1.42AK-BMDSFIX1`; DIAG1PATH1 is not runtime-armed. The regular exact-byte gameplay Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived, and no further non-target control is required solely for that gate. The long-name DIAG1 remains preloader-blocked historical provenance and must not be rerun. Black Mesa x Greenhouse/BMGHDIAG remains separate.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
