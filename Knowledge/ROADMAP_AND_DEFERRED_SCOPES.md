<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1 candidate=S1.42AI-DIAG1 runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md`  
**Last-Validated:** 2026-09-13

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact and active temporary diagnostic candidate: **S1.42AI-DIAG1**, SHA-256 `22e2132669a790756f2a1e2bd10b14fd05144b3ecdd55233d8d57f1d6dd9f3fd`. Runtime validation is outstanding.

## Active scope

Runtime-test the exact DIAG1 profile under `AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md`. The diagnostic must isolate exact Shy Guy while preserving narrow owner/native lifecycle and fail visibly on any non-ShyGuy bypass.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after DIAG1; diagnostic success cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
