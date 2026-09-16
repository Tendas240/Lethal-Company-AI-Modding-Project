<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-16

## Current position

Accepted gameplay baseline: **S1.42AH**. Completed diagnostic evidence: **S1.42AI-DIAG1R3**, with exterior visibility explicitly not exercised because no exterior ShyGuy occurred. Latest built artifact and active full-normal runtime candidate: **S1.42AI**, SHA-256 `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`.

## Active scope

Run the independent full-normal S1.42AI BCMER ShyGuy gate from `Current/143...`, then ingest the complete fresh S1.42AI log and make an explicit acceptance/rejection decision. R3 must not be rerun merely to force a rare exterior ShyGuy and must not be treated as S1.42AI acceptance.

## Remaining deferred independent scopes

- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
