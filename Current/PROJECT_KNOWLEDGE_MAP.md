<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-09-23

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

**Universal Interior Viability / Equal Availability is the selected scope.** Phases A through C1 are complete. Phase C2 is complete under `Current/169_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C2_OWNER_HARD_BLOCK_REASON_ANALYSIS.md`: all 14 current owner hard blocks are reason-reconciled without changing the 30×53 matrix. Twelve Offense exclusions are package/asset default targeting or balance rules; Shatteredrooms × Experimentation and × Embrion are explicit owner exclusions whose technical cause remains unproven. No hard-block cell is currently proven to be a technical compatibility safeguard or `KNOWN_TECHNICAL_RESTRICTION`. The matrix remains 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`. The first exact `S1.42AK-BMGHDIAG1` Black Mesa run remains ingested as a fail-closed diagnostic refusal: normal LLL matching proved Greenhouse viable at effective rarity 100, normal selection chose Decrepit store, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN`. C3F18 has now established and repaired the startup provenance defect at source/static level under separately versioned `S1.42AK-BMGHDIAG2`: the physical V81 `Assembly-CSharp.dll` is hashed via BepInEx `Paths.ManagedPath` while loaded `EntranceTeleport` identity is validated structurally. Exact source/static PR head `c767b27c64def300907cf617b4971b2b91024291` passed BMGHDIAG2 source/static run `35921973472` and Knowledge Architecture run `35921973492`. BMGHDIAG2 is not built, published or armed. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no runtime test is outstanding, and the next action is a separate inactive BMGHDIAG2 review-build checkpoint from exact S1.42AK. The B3 matrix remains unchanged.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
