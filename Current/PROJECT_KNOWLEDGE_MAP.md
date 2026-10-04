<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Project Knowledge Map

**Status:** CURRENT / CANONICAL ROUTER
**Authority:** primary human topic router for repository knowledge
**Machine Mirror:** `Current/PROJECT_KNOWLEDGE_MAP.json`
**Current State:** `Current/00_CURRENT_STATE.md`
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
**Last-Validated:** 2026-10-04

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

Concrete Black Mesa pair evidence now includes Greenhouse and Abandoned Foundry as full bounded pair-specific runtime-compatibility PASS records, alongside narrower Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation topology/traversal evidence. `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` remains the historical checkpoint that exhausted evidence available at that time; later BMAFR1 evidence adds Abandoned Foundry without rewriting that historical decision.

Oxyde remains governed by `SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md`: 23 positive selection/metadata matches exist, but exact V81 skips ordinary dungeon generation while `spawnEnemiesAndScrap=false`, and no independent inspected dungeon/entrance-construction path is established. Those metadata matches are not executable ordinary pair proof.

The bounded **S1.42AK-BMAFDIAG1** Black Mesa x Abandoned Foundry diagnostic has completed source/static integration, inactive review build, exact-byte publication and canonical profile indexing. Authorities: `Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md` through `Current/210_S1.42AK_BMAFDIAG1_PROFILE_INDEX_RECONCILIATION.md`. Exact profile SHA-256 is `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2`; exact diagnostic DLL SHA-256 is `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`.

Runtime activation from `Current/211_S1.42AK_BMAFDIAG1_RUNTIME_ACTIVATION.md` was integrated and exact-head CI-green, but the first local launch subsequently exposed the path-length blocker reconciled by `Current/212_S1.42AK_BMAFDIAG1_PATH_LENGTH_BLOCK_AND_GUARD_RECONCILIATION.md`. The named runtime DLLs were physically present, while their full local paths were exactly 260 and 262 characters. The current long BMAFDIAG1 identity is therefore **DO NOT RERUN** and is no longer an executable diagnostic target. This is preloader launch-block evidence, not a runtime rejection; Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Runtime/evidence routing has been returned to `S1.42AK-BMDSFIX1` without accepting it.

The separately versioned identity-only successor **S1.42AK-BMAFDIAG1PATH1** is published and canonically indexed, but its bounded Black Mesa x Abandoned Foundry runtime attempt is now completed failed diagnostic evidence under `Current/219_S1.42AK_BMAFDIAG1PATH1_RUNTIME_REFUSAL_AND_CONFIG_BINDING_ROOT_CAUSE_RECONCILIATION.md`. Exact evidence `RuntimeEvidence/S1.42AK-BMAFDIAG1PATH1/20261001T195721Z/` / raw log SHA-256 `ccb38f7173a109a103f5dbc67e06d4acf60f86f95652a2db566f8b2c63a98521` shows BMAFDIAG1 armed, then LLL returned Abandoned Foundry as unviable on Black Mesa and the diagnostic correctly emitted `REFUSED`. The root cause is the LLL config-category identity: real LLL 1.7.12 Custom Dungeon categories use exactly nine U+200B sorting characters, while the published Foundry section used a plain header; the generic builder created the wrong category and the BMAFDIAG1 validator removed Unicode `Cf` characters during header comparison, masking the mismatch. PATH1 is therefore **DO NOT RERUN / DIAGNOSTIC ONLY / NEVER ACCEPT** and Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Runtime/evidence routing is returned to S1.42AK-BMDSFIX1 without accepting it.

The repaired **S1.42AK-BMAFR1** retains its completed Black Mesa x Abandoned Foundry runtime-compatibility PASS and remains DIAGNOSTIC ONLY / NEVER ACCEPT.

The separately versioned **S1.42AK-BMAFR1I1** attribution diagnostic has now completed its authorized runtime attempt under `Current/239_S1.42AK_BMAFR1I1_RUNTIME_ATTRIBUTION_RECONCILIATION.md`. Exact evidence `RuntimeEvidence/S1.42AK-BMAFR1I1/20261003T232317Z/` / raw log SHA-256 `0f28ad24f0279cd18a039bc4e1de695e9590d1c70e98d2a6a2aa318b30674ce3` proves successful `[BMAFR1I1] ARMED` operation but zero recurrence of the exact array-index signature. Required Janitor direct-write/equal-scope evidence and SpringMan equal-scope evidence did not occur. This is **inconclusive negative reproduction**, not emitter/root-cause proof; Janitor/Princess and SpringMan remain unresolved at the target-instance boundary. BMAFR1I1 remains DIAGNOSTIC ONLY / NEVER ACCEPT and is no longer runtime-active.

`Current/241_S1.42AK_BMAFR1I1_POST_RUNTIME_ATTRIBUTION_DECISION.md` now closes the immediate repeat-run question: attribution remains unresolved and **no further BMAFR1I1 runtime attempt is authorized**. Repeating the same correctly armed diagnostic would still depend on stochastic Janitor/SpringMan target acquisition and flood recurrence; deliberately forcing those conditions would materially change the experiment and requires a new separately versioned scope. Phase C3 therefore resumes without another BMAFR1I1 run.

The same session adds a separate Black Mesa/Pikmin routing finding: BCMER `SafeOutside` explicitly suppressed outside spawning, while pluck/Onion Pikmin creation still entered LethalMin paths and then encountered immediate removal and repeated staging/NavMesh failures. It also proves Herobrine active/spawned; the user requests Herobrine disabled, with whole-mod removal to be considered only after exact dependency/config analysis.

Runtime/evidence routing is back on `S1.42AK-BMDSFIX1`. BMDSFIX1 remains the separate active gameplay candidate / **NOT ACCEPTED**; its exact Black Mesa x `DeepSewersFlow` gate remains passive, outstanding and unwaived. `BuildSpecs/current.json` remains disabled.

`Current/242_S1.42AK_PHASE_C3_OXYDE_ORDINARY_GENERATION_PRIORITY_SELECTION.md` selects the **Oxyde ordinary-generation semantic restriction** as the next Phase-C3 compatibility/safety target. Oxyde's 23 selection-supported metadata pairings remain non-executable through the inspected ordinary path while `spawnEnemiesAndScrap=false` returns exact V81 before `RuntimeDungeon` / `GenerateNewFloor`, and no independent inspected dungeon/entrance-construction path is established. Because this blocks the whole Oxyde row, it takes priority over selecting another arbitrary unseen Black Mesa `MATCH` that would require fresh pair evidence acquisition.

That selected analysis is now completed by record 243 below. Once this documentation-only checkpoint is integrated, the exact next action is the bounded remaining Phase-C3 priority reassessment described below. No implementation, build or runtime test is authorized.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.


## Oxyde static safety decision — current exception preserved

`Current/243_S1.42AK_OXYDE_ORDINARY_GENERATION_STATIC_SAFETY_DECISION.md` completes the bounded source/static analysis selected by record 242 and supersedes its analysis-next instruction. No safe config/single-flag conversion is established: normal generation requires live generator and exterior entrance proof, while CodeRebirth retains the crane dungeon-type writer, outside-enemy classification and special ship/time semantics. Oxyde remains an explicit current-architecture exception, not a proven permanently incompatible or broken moon. Its 23 metadata matches and the historical B3 matrix remain unchanged.

Perform one bounded Phase-C3 remaining compatibility/safety priority reassessment using existing repository evidence, with the Oxyde current-architecture exception preserved under Current/243_S1.42AK_OXYDE_ORDINARY_GENERATION_STATIC_SAFETY_DECISION.md. Select and justify the next exact unresolved pairing/restriction or evidence prerequisite; do not reopen the completed Oxyde flag analysis without new evidence, implement a change, build/publish a candidate, or authorize/start a runtime run in that reassessment. Preserve BMDSFIX1 passive/outstanding/unwaived DeepSewersFlow and the closed-unresolved BMAFR1I1 attribution.

S1.42AK remains accepted; BMDSFIX1 remains active / NOT ACCEPTED with its passive, outstanding and unwaived DeepSewersFlow gate. No further BMAFR1I1 run is authorized. Build and runtime controllers are unchanged.

## Phase-C3 remaining-priority reassessment — interior-side existing-evidence refresh next

`Current/244_S1.42AK_PHASE_C3_REMAINING_PRIORITY_REASSESSMENT_INTERIOR_PROOF_REFRESH.md` completes the requested remaining compatibility/safety priority reassessment without authorizing gameplay work.

The External-moon branch is sufficiently bounded for the current architecture: Black Mesa applicability is closed at 31 MATCH / 22 NON-MATCH / 0 UNRESOLVED with existing pair-specific evidence exhausted unless new evidence is acquired, while Oxyde remains the explicit ordinary-generation exception from record 243. C2 already classified the 14 owner hard blocks without authorizing their removal.

The next prerequisite therefore returns to C1 Priority 2: refresh the exact 34 flows that record 168 listed as lacking trusted actual-generation proof against all already-ingested later/omitted repository evidence. That list is demonstrably historical rather than a current residual set because later Black Mesa work supplies concrete post-C1 proof for at least Slaughterhouse and Decrepit store. Do not select a new runtime target until the refreshed residual set is known. C1 Priority 3 route/NavMesh attribution remains subsequent and separate.

No new runtime acquisition, implementation, candidate build/publication, owner-restriction removal or controller change is authorized. Oxyde, Shatteredrooms/CullFactory, Black Mesa/Pikmin, Herobrine, BMAFR1I1 and the passive/outstanding/unwaived BMDSFIX1 DeepSewersFlow gate remain separate and unchanged.

Exact next action: Perform one bounded Phase-C interior-side existing-evidence refresh over the exact 34 flows listed in Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md as having no trusted actual-generation proof at C1. Reconcile only already-ingested repository evidence acquired after or omitted by C1; classify each flow's current generation/traversal proof status, preserve route/NavMesh signals as separate obligations, and produce a current residual proof-gap set before selecting any new runtime target. Do not acquire new runtime evidence, implement changes, build/publish a candidate, remove owner restrictions, reopen Oxyde, or turn BMDSFIX1 DeepSewersFlow into a dedicated reroll. Preserve separate Shatteredrooms/CullFactory, Black Mesa/Pikmin, Herobrine and BMAFR1I1 scopes.
