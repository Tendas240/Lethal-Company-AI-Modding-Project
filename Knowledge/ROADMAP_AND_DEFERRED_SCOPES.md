<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`, `Current/173_S1.42AK_BMGHDIAG2_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL_AND_DEEP_SEWERS_INCIDENT.md`, `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`  
**Last-Validated:** 2026-09-28

## Current position

Accepted gameplay baseline remains **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**, SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

Latest built artifact and active gameplay candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted and its exact regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding/unwaived.

The bounded `S1.42AK-BMGHDIAG3` Black Mesa x Greenhouse diagnostic is complete. Exact evidence `RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/` / raw log SHA-256 `e30858fcebce0fc51f092170b50bd439290cf4752bf0917ae28d66e29a37a9f8` establishes the pair-specific runtime-compatibility PASS recorded in `Current/199_S1.42AK_BMGHDIAG3_RUNTIME_COMPATIBILITY_PASS.md`. BMGHDIAG3 remains diagnostic only / NEVER ACCEPT and is no longer the runtime/evidence target. `RuntimeInbox/ACTIVE_BUILD.txt` has returned to exact BMDSFIX1; this routing reset does not release a dedicated Deep Sewers test and does not accept the candidate. `BuildSpecs/current.json` remains disabled.

## Selected scope

**Universal Interior Viability / Equal Availability — SELECTED / PHASE C3 IN PROGRESS / BLACK MESA x GREENHOUSE RUNTIME COMPATIBILITY PASS / BMDSFIX1 GAMEPLAY QUALIFICATION PASSIVE OUTSTANDING.**

The authoritative 30x53 B3 matrix and accepted S1.42AB post-viability normalizer remain unchanged. The Greenhouse decision adds pair-specific Phase-C compatibility evidence; it does not retroactively rewrite the B3 availability matrix and does not authorize a universal override.

Plan: `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`.

## Exact next selected-scope action

Continue the repository-native Phase C3 External target-moon semantics/topology analysis from the completed Black Mesa x Greenhouse runtime-compatibility PASS. Preserve the unchanged Phase-B3 availability matrix, accepted S1.42AK, and unaccepted S1.42AK-BMDSFIX1. No new BMGHDIAG3 run is authorized, and no dedicated BMDSFIX1 Black Mesa reroll is released: its regular exact-byte Black Mesa x DeepSewersFlow qualification remains passive, outstanding and unwaived. If unrelated normal exact-byte BMDSFIX1 evidence naturally selects DeepSewersFlow, ingest it against the existing gate. Do not implement a universal availability override until the remaining Phase C3 external-moon obligations are resolved.

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
