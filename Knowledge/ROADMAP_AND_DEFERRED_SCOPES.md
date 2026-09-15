<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=S1.42AI-DIAG1R2 runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`, `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md`, `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-15

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact and active diagnostic candidate: **S1.42AI-DIAG1R2**, SHA-256 `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`. Static, materialized applicability and semantic-equivalence validation are green; its runtime diagnostic is now outstanding.

## Active scope

Run the R2 ShyGuy-isolation diagnostic, ingest its fresh runtime log, and make an explicit diagnostic decision. Failed DIAG1 and R1 profiles must not be rerun unchanged.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the R2 diagnostic question is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
