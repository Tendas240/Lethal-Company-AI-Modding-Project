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

Concrete Black Mesa pair evidence now includes Greenhouse and Abandoned Foundry as full bounded pair-specific runtime-compatibility PASS records, alongside narrower Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation topology/traversal evidence. `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` remains the historical checkpoint that exhausted evidence available at that time; later BMAFR1 evidence adds Abandoned Foundry without rewriting that historical decision.

Oxyde remains governed by `SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md`: 23 positive selection/metadata matches exist, but exact V81 skips ordinary dungeon generation while `spawnEnemiesAndScrap=false`, and no independent inspected dungeon/entrance-construction path is established. Those metadata matches are not executable ordinary pair proof.

The bounded **S1.42AK-BMAFDIAG1** Black Mesa x Abandoned Foundry diagnostic has completed source/static integration, inactive review build, exact-byte publication and canonical profile indexing. Authorities: `Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md` through `Current/210_S1.42AK_BMAFDIAG1_PROFILE_INDEX_RECONCILIATION.md`. Exact profile SHA-256 is `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2`; exact diagnostic DLL SHA-256 is `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`.

Runtime activation from `Current/211_S1.42AK_BMAFDIAG1_RUNTIME_ACTIVATION.md` was integrated and exact-head CI-green, but the first local launch subsequently exposed the path-length blocker reconciled by `Current/212_S1.42AK_BMAFDIAG1_PATH_LENGTH_BLOCK_AND_GUARD_RECONCILIATION.md`. The named runtime DLLs were physically present, while their full local paths were exactly 260 and 262 characters. The current long BMAFDIAG1 identity is therefore **DO NOT RERUN** and is no longer an executable diagnostic target. This is preloader launch-block evidence, not a runtime rejection; Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Runtime/evidence routing has been returned to `S1.42AK-BMDSFIX1` without accepting it.

The separately versioned identity-only successor **S1.42AK-BMAFDIAG1PATH1** is published and canonically indexed, but its bounded Black Mesa x Abandoned Foundry runtime attempt is now completed failed diagnostic evidence under `Current/219_S1.42AK_BMAFDIAG1PATH1_RUNTIME_REFUSAL_AND_CONFIG_BINDING_ROOT_CAUSE_RECONCILIATION.md`. Exact evidence `RuntimeEvidence/S1.42AK-BMAFDIAG1PATH1/20261001T195721Z/` / raw log SHA-256 `ccb38f7173a109a103f5dbc67e06d4acf60f86f95652a2db566f8b2c63a98521` shows BMAFDIAG1 armed, then LLL returned Abandoned Foundry as unviable on Black Mesa and the diagnostic correctly emitted `REFUSED`. The root cause is the LLL config-category identity: real LLL 1.7.12 Custom Dungeon categories use exactly nine U+200B sorting characters, while the published Foundry section used a plain header; the generic builder created the wrong category and the BMAFDIAG1 validator removed Unicode `Cf` characters during header comparison, masking the mismatch. PATH1 is therefore **DO NOT RERUN / DIAGNOSTIC ONLY / NEVER ACCEPT** and Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Runtime/evidence routing is returned to S1.42AK-BMDSFIX1 without accepting it.

The separately versioned short repair successor **S1.42AK-BMAFR1** now has completed cumulative Black Mesa x Abandoned Foundry runtime evidence. First evidence `RuntimeEvidence/S1.42AK-BMAFR1/20261002T154834Z/` / raw log SHA-256 `3113a1c9df2e1db231cf6aa0e7dc20699894a8646da3eaf7fd1ce0c3d89ac42b` established exact target selection, completed generation, four-pair topology and bidirectional IDs 0,1,3. Supplemental evidence `RuntimeEvidence/S1.42AK-BMAFR1/20261002T164741Z/` / raw log SHA-256 `ca2d83a56115f66623c3dfb38d2cdd47085b3c0a368efc3ace29321a323b4d90` directly traversed ID 2 / outside `EntranceTeleportC` in both directions and reached final bidirectional IDs 0..3 coverage with no diagnostic invalidator or post-generation persistent target-attributable routing/NavMesh failure. `Current/226_S1.42AK_BMAFR1_RUNTIME_COMPATIBILITY_PASS_AND_PERFORMANCE_FINDING.md` therefore records a **Black Mesa x Abandoned Foundry runtime-compatibility PASS**. BMAFR1 remains **DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**. The supplemental-run performance finding is now statically reconciled through `Current/227_S1.42AK_BMAFR1_PERFORMANCE_ATTRIBUTION_PARTIAL_RECONCILIATION.md` plus `Current/228_S1.42AK_BMAFR1_ASSET_LEVEL_ATTRIBUTION_RECONCILIATION.md` / `SourceEvidence/BMAFR1AssetAttribution/20261002T214700Z/`. The asset layer resolves a concrete Janitor/Princess Dusk mechanism: hierarchy `Janitor`, original three-material renderer with one serialized blendshape-weight slot, Princess shared-mesh replacement sourced from an importer with `importBlendShapes=0`, and DawnLib 0.9.25 mesh/bone transfer without blendshape compatibility validation. The supplemental `got 3, need 4` warning strongly matches that action shape but still does not prove Princess selection, the observed live mesh state, the exact array emitter or root cause. No CodeRebirth 1.6.9 Dusk SpringMan target is established and exact vanilla SpringMan asset provenance is unavailable, so SpringMan remains an unresolved contemporaneous alternative. Static asset attribution is exhausted to the current provenance boundary. `Current/229_S1.42AK_BMAFR1_NARROW_INSTRUMENTATION_DESIGN.md` now completes the bounded design for the minimum fail-closed observational surface: Dusk selection state, exact Janitor/SpringMan instance correlation, Dusk skinned-mesh pre/post state, Janitor index-0 write probes, SpringMan peer snapshots and stackless-array log-pipeline correlation. The design authorizes no implementation, build, publication, activation or runtime. Runtime/evidence routing remains `S1.42AK-BMDSFIX1`; accepted S1.42AK and the passive/unwaived BMDSFIX1 DeepSewersFlow gate remain unchanged.

BMGHDIAG3 remains completed Black Mesa x Greenhouse runtime-compatibility PASS evidence / **DIAGNOSTIC ONLY / NEVER ACCEPT** and is not runtime-active. S1.42AK-BMDSFIX1 remains the separate active gameplay candidate / **NOT ACCEPTED**; its regular exact-byte Black Mesa x `DeepSewersFlow` qualification remains passive, outstanding and unwaived. `BuildSpecs/current.json` and `AUTO_BUILD_RESULT` remain BMDSFIX1 authorities.

Exact next action: After the BMAFR1 narrow instrumentation design is integrated to main and permanent exact-head Knowledge Architecture is green, perform one separately bounded inactive-review-build justification / source-static authorization decision for the exact design in Current/229_S1.42AK_BMAFR1_NARROW_INSTRUMENTATION_DESIGN.md. Decide only whether the fail-closed observational surface is justified and implementable against the exact deployed CodeRebirth 1.6.9 and DawnLib.Dusk 0.9.25 contracts. Do not implement the patch, create an inactive review build, publish, Gale-import, activate or run anything in that decision segment. Preserve the Black Mesa x Abandoned Foundry BMAFR1 pair PASS with no qualification rerun, BMAFR1 DIAGNOSTIC ONLY / NEVER ACCEPT / inactive, S1.42AK accepted, and S1.42AK-BMDSFIX1 active/not accepted with its passive outstanding unwaived DeepSewersFlow gate and no dedicated reroll.

## Authority rule

`Current/CURRENT_STATE.json` is the global machine lifecycle authority. This map chooses semantic topics. Build-specific records/runtime evidence prove decisions and observations but historical files never override later current state.

When the user requests a new-chat handover, route to `Current/HANDOVER_PREPARATION_PROMPT.md` and re-verify repository/CI state before producing it.

## Historical navigation

Use `Current/03_PROJECT_CHRONOLOGY.md`, `Current/BUILD_LINEAGE.md/.json`, numbered build-specific `Current/*S1.*` files, `ProfileSources/`, and `RuntimeEvidence/` for history. `Current/02_TECHNICAL_BASELINE.md` and `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are not unqualified current-state authority.
