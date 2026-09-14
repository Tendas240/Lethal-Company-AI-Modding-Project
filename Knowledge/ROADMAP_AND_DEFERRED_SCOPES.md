<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1 candidate=none runtime_test_outstanding=false -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md`, `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md`  
**Last-Validated:** 2026-09-14

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1**, SHA-256 `22e2132669a790756f2a1e2bd10b14fd05144b3ecdd55233d8d57f1d6dd9f3fd`, but its diagnostic runtime attempt failed during exact owner prevalidation and rolled back the DIAG1 Harmony hooks. It is not an active runtime candidate.

## Active scope

Repair the DIAG1 owner type-resolution/static-validation contract described in `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md`. Do not rerun the current DIAG1 profile unchanged. After the repair passes repository-native static/materialized validation, build a successor diagnostic candidate and only then request another runtime test.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the diagnostic question is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
