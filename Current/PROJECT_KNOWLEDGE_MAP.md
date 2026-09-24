<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-09-24

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

Accepted gameplay baseline and latest built artifact: **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**.

Acceptance authority: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`. Full-normal runtime evidence is `RuntimeEvidence/S1.42AK/20260918T172838Z/` with raw log SHA-256 `cc0f0a7a6c6a76ad44266aded11ff9cb2aca21f2623f5fb895d371ad778526b9`. The first attempt in that session was aborted before interior entry. The played second attempt naturally selected Spooky Manor and supplied roughly three minutes of interior coverage without a hostile enemy sighting; that is a documented coverage limitation, not a proven spawn regression.

The targeted LC Office camera-render A/B remains supplied by completed diagnostic-only S1.42AJ-DIAG2 evidence. The later LC Office Scrap Quantity/Distribution Investigation is complete with no gameplay delta under `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`. S1.42AK remains accepted/latest and unchanged.

**Universal Interior Viability / Equal Availability is the selected scope.** Phases A through C2 remain complete with the fixed 30×53 matrix unchanged at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`.

Both exact Black Mesa x Greenhouse diagnostic attempts remain completed failed diagnostic evidence. BMGHDIAG2 is ingested at `RuntimeEvidence/S1.42AK-BMGHDIAG2/20260924T124542Z/` and refused before arming on `EntranceTeleport manifest module identity mismatch`, so Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation remains the **active gameplay runtime candidate / not accepted**. Exact runtime evidence is ingested at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/` with raw log SHA-256 `9a8cf28bbfc050cf9247cffacc890ea1b4e7215329db4ecfc9085f3f8f0ff2cb`. The run armed BMDSFIX1 but Black Mesa selected Substation, so no `APPLIED` marker occurred; this is preserved as the exact-byte non-target control. The remaining gate is only Black Mesa x `DeepSewersFlow`; decision authority: `Current/175_S1.42AK_BMDSFIX1_PARTIAL_RUNTIME_EVIDENCE_NON_TARGET_CONTROL.md`. The same run preserves a separate Substation large-generation/landing-stutter finding without attributing it to BMDSFIX1. `BuildSpecs/current.json` remains disabled while guarding the exact BMDSFIX1 candidate. The separately published/indexed `S1.42AK-BMDSFIX1-DIAG1` is now the active diagnostic runtime target and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1` solely for Gale resolution/evidence attribution. BMDSFIX1 remains the active gameplay candidate / not accepted, its regular Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
