<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`, `Current/173_S1.42AK_BMGHDIAG2_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL_AND_DEEP_SEWERS_INCIDENT.md`, `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`, `Current/206_S1.42AK_EXTERNAL_OWNER_RULE_APPLICABILITY_CLOSURE_RECONCILIATION.md`  
**Last-Validated:** 2026-10-02

## Current position

Accepted gameplay baseline remains **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**, SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

Latest built artifact and active gameplay candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted and its exact regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding/unwaived.

The long-name BMAFDIAG1 remains preloader-blocked / **DO NOT RERUN** and BMAFDIAG1PATH1 remains completed failed config-binding diagnostic provenance / **DO NOT RERUN / NEVER ACCEPT**. Repaired **S1.42AK-BMAFR1** now has a completed bounded Black Mesa x Abandoned Foundry runtime-compatibility PASS under `Current/226_S1.42AK_BMAFR1_RUNTIME_COMPATIBILITY_PASS_AND_PERFORMANCE_FINDING.md`. Supplemental evidence `RuntimeEvidence/S1.42AK-BMAFR1/20261002T164741Z/` / raw log SHA-256 `ca2d83a56115f66623c3dfb38d2cdd47085b3c0a368efc3ace29321a323b4d90` closes the missing ID-2 gate and reaches final bidirectional IDs 0..3 coverage. BMAFR1 remains DIAGNOSTIC ONLY / NEVER ACCEPT and is no longer runtime-active. The supplemental run also exposes a separate 6696-array-index-error / reduced-frame-rate finding whose root cause remains unattributed. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`; `BuildSpecs/current.json` remains disabled and `AUTO_BUILD_RESULT` remains BMDSFIX1.

## Selected scope

**Universal Interior Viability / Equal Availability — SELECTED / PHASE C3 EXTERNAL OWNER-RULE APPLICABILITY CLOSED / PAIR COMPATIBILITY-SAFETY EVIDENCE REMAINS GATED / BMDSFIX1 GAMEPLAY QUALIFICATION PASSIVE OUTSTANDING.**

The authoritative 30x53 B3 matrix remains an unchanged historical snapshot at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`. Black Mesa's new `31 MATCH / 22 NON-MATCH / 0 UNRESOLVED` result is a Phase-C3 current-applicability classification only and does not rewrite B3. `MATCH` is selection/availability support, not runtime compatibility; `NON-MATCH` is absence of a current positive owner/matching rule, not a technical incompatibility finding.

Oxyde retains 23 positive selection/metadata matches, but ordinary executable dungeon generation remains outside current proved applicability because `spawnEnemiesAndScrap=false` keeps exact V81 on the early-return path and no inspected independent ordinary dungeon/entrance-construction path is established. No universal override is authorized.

Plan: `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`.

## Exact next selected-scope action

After this BMAFR1 runtime-compatibility reconciliation is integrated to `main` and permanent exact-head Knowledge Architecture is green, perform one bounded repository-native performance-attribution triage of the supplemental-run `Array index (0) is out of bounds (size=0)` flood. Compare the first and supplemental exact BMAFR1 evidence, identify the emitting call path/owner as far as repository/source evidence permits, and test the observed Janitor-lifetime temporal correlation against alternative explanations before proposing any patch or new runtime build. Do not rerun BMAFR1 solely for pair qualification and do not release a dedicated BMDSFIX1 reroll; its regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding/unwaived. After the bounded performance triage, continue the remaining Phase C3 compatibility/safety work under the existing universal-interior plan.

BMAFR1 remains diagnostic-only / NEVER ACCEPT and requires no further pair-qualification rerun. The separate performance finding must be attributed before any patch or new runtime build is proposed. BMDSFIX1 remains NOT ACCEPTED; its regular DeepSewersFlow gate stays passive/outstanding/unwaived, and no universal availability override is authorized. BMAFDIAG1PATH1 remains DO NOT RERUN.

## Completed LC Office scrap scope

**LC Office Scrap Quantity/Distribution Investigation — COMPLETE / NO GAMEPLAY DELTA.**

`Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md` records the valid placement capture. No quantity increase or broad placement patch is authorized; accepted S1.42AK remains unchanged.

## Remaining deferred independent scopes

- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.

Do not silently combine these deferred scopes into the selected viability investigation.
