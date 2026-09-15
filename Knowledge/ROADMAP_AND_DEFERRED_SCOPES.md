<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC
**Authority:** live selected/deferred-scope list only
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`, `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`
**Last-Validated:** 2026-09-15

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1R2**, now completed failed diagnostic evidence. There is no active runtime candidate and no runtime test outstanding.

R2 successfully armed the owner/applicability repairs, but its exact ShyGuy classifier rejected the real runtime `enemyName = Shy guy` because source expected `Shy Guy` ordinally. `S1.42AI-DIAG1R3` is determined as the exact-literal repair and its source/static-gate/build request are prepared, but it is not built.

## Active scope

Next, perform a separate repository-native R3 build-controller transition from exact full-normal S1.42AI, validate the generated artifact/materialized semantics, and only then decide whether R3 may become the active runtime candidate. Do not rerun DIAG1/R1/R2 unchanged and do not request gameplay yet.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the diagnostic repair path is resolved; diagnostic success cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
