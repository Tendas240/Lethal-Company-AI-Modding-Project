<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-10-02

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

The selected **Universal Interior Viability / Equal Availability** scope remains in Phase C3. The fixed Phase-B3 30x53 availability/effective-weight matrix remains an unchanged historical snapshot at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`; pair-specific Phase-C evidence and current applicability findings do not rewrite those historical classifications.

`Current/206_S1.42AK_EXTERNAL_OWNER_RULE_APPLICABILITY_CLOSURE_RECONCILIATION.md` closes the Phase-C3 External owner-rule applicability / External semantics gate from existing repository-native source/owner/config evidence. Black Mesa current applicability is `31 MATCH / 22 NON-MATCH / 0 UNRESOLVED`. This is selection/availability-layer evidence only: the 31 matches are not automatic runtime-compatibility passes and the 22 non-matches are not technical-incompatibility findings. No duplicate Black Mesa registration is needed or authorized.

The already-ingested concrete Black Mesa pair evidence remains bounded to Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation. Greenhouse is the full bounded pair-specific runtime-compatibility PASS; the other records retain narrower topology/traversal boundaries. No additional already-ingested Black Mesa pair is available for the same evidence-only reconciliation path. Decision: `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md`.

Oxyde remains governed by `SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md`: 23 positive selection/metadata matches exist, but exact V81 skips ordinary dungeon generation while `spawnEnemiesAndScrap=false`, and no independent inspected dungeon/entrance-construction path is established. Those metadata matches are not executable ordinary pair proof.

The bounded **S1.42AK-BMAFDIAG1** Black Mesa x Abandoned Foundry diagnostic has completed source/static integration, inactive review build, exact-byte publication and canonical profile indexing. Authorities: `Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md` through `Current/210_S1.42AK_BMAFDIAG1_PROFILE_INDEX_RECONCILIATION.md`. Exact profile SHA-256 is `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2`; exact diagnostic DLL SHA-256 is `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`.

Runtime activation from `Current/211_S1.42AK_BMAFDIAG1_RUNTIME_ACTIVATION.md` was integrated and exact-head CI-green, but the first local launch subsequently exposed the path-length blocker reconciled by `Current/212_S1.42AK_BMAFDIAG1_PATH_LENGTH_BLOCK_AND_GUARD_RECONCILIATION.md`. The named runtime DLLs were physically present, while their full local paths were exactly 260 and 262 characters. The current long BMAFDIAG1 identity is therefore **DO NOT RERUN** and is no longer an executable diagnostic target. This is preloader launch-block evidence, not a runtime rejection; Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Runtime/evidence routing has been returned to `S1.42AK-BMDSFIX1` without accepting it.

The separately versioned identity-only successor **S1.42AK-BMAFDIAG1PATH1** is published and canonically indexed, but its bounded Black Mesa x Abandoned Foundry runtime attempt is now completed failed diagnostic evidence under `Current/219_S1.42AK_BMAFDIAG1PATH1_RUNTIME_REFUSAL_AND_CONFIG_BINDING_ROOT_CAUSE_RECONCILIATION.md`. Exact evidence `RuntimeEvidence/S1.42AK-BMAFDIAG1PATH1/20261001T195721Z/` / raw log SHA-256 `ccb38f7173a109a103f5dbc67e06d4acf60f86f95652a2db566f8b2c63a98521` shows BMAFDIAG1 armed, then LLL returned Abandoned Foundry as unviable on Black Mesa and the diagnostic correctly emitted `REFUSED`. The root cause is the LLL config-category identity: real LLL 1.7.12 Custom Dungeon categories use exactly nine U+200B sorting characters, while the published Foundry section used a plain header; the generic builder created the wrong category and the BMAFDIAG1 validator removed Unicode `Cf` characters during header comparison, masking the mismatch. PATH1 is therefore **DO NOT RERUN / DIAGNOSTIC ONLY / NEVER ACCEPT** and Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Runtime/evidence routing is returned to S1.42AK-BMDSFIX1 without accepting it.

The separately versioned short repair successor **S1.42AK-BMAFR1** has completed inactive raw config-binding review, exact-byte publication, canonical profile mapping and profile indexing. Publication authority remains `Current/221_S1.42AK_BMAFR1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md`; publication integration closure is `Current/222_S1.42AK_BMAFR1_PUBLICATION_INTEGRATION_RECONCILIATION.md`; profile-index closure authority is `Current/223_S1.42AK_BMAFR1_PROFILE_INDEX_RECONCILIATION.md`. Exact profile `Profiles/LC V1 S1.42AK-BMAFR1.r2z` remains SHA-256 `8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5`. Mapping PR #220 exact head `a1559e4b0fa0cd82f2a138a0870739c45389c517` passed Knowledge Architecture run `37012840553` / #950 and merged as `beaabff986443e538dfa0c98d2c9f1a09f0ef0c0`; direct main Knowledge Architecture run `37013064060` / #951 passed. Profile-index run `37013063791` / #32 succeeded and committed canonical `ProfileSources/S1.42AK-BMAFR1/PROFILE_INDEX_RESULT.json` as `328e4b99786916dd2b5d030f448ac5321a8913a6`. Exact-head Knowledge Architecture run `37013099855` / #952 was correctly registered as `workflow_dispatch` and passed. The earlier publication-triggered failure `36989414554` / #31 is superseded mapping-gate evidence only. BMAFR1 is therefore published and canonically indexed, but remains not Gale-imported and not runtime-armed. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`.

BMGHDIAG3 remains completed Black Mesa x Greenhouse runtime-compatibility PASS evidence / **DIAGNOSTIC ONLY / NEVER ACCEPT** and is not runtime-active. S1.42AK-BMDSFIX1 remains the separate active gameplay candidate / **NOT ACCEPTED**; its regular exact-byte Black Mesa x `DeepSewersFlow` qualification remains passive, outstanding and unwaived. `BuildSpecs/current.json` and `AUTO_BUILD_RESULT` remain BMDSFIX1 authorities.

Exact next action: Execute the separately bounded S1.42AK-BMAFR1 runtime-activation checkpoint for the already-published and canonically indexed exact bytes. Re-verify profile Profiles/LC V1 S1.42AK-BMAFR1.r2z at SHA-256 8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5 and ProfileSources/S1.42AK-BMAFR1/PROFILE_INDEX_RESULT.json, then update runtime/evidence routing only as required for that diagnostic activation. Do not rebuild or alter profile/DLL/config/package bytes, do not accept S1.42AK-BMDSFIX1 or waive its passive Black Mesa x DeepSewersFlow qualification, and do not rerun BMAFDIAG1PATH1.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
