<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=S1.42AI-DIAG1R3 runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`, `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`, `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md`, `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-16

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact and active diagnostic candidate: **S1.42AI-DIAG1R3**, SHA-256 `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`. Exact ShyGuy identity, static, materialized applicability and semantic-equivalence validation are green; its runtime diagnostic is now outstanding.

## Active scope

Run the R3 ShyGuy-isolation diagnostic, explicitly confirm no non-ShyGuy enemy appears and exterior ShyGuy visibility when exercised, ingest the fresh runtime log, and make an explicit diagnostic decision.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the R3 diagnostic question is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
