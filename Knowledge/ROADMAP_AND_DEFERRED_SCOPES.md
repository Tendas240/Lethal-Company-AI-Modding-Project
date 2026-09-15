<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md`, `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-15

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1R2**, SHA-256 `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`, is built and repository-natively static/materialized validated but is not accepted and is not yet an active runtime candidate. There is no new gameplay test outstanding.

R2 is the rebuilt successor of failed R1 and contains the landed `kite.ZelevatorCode` EndlessElevator applicability repair. Canonical R2 materialization proves dependency absent => this compat target is `NOT_APPLICABLE`; dependency present => the exact provider/owner/signature/install contract remains required and fail-closed.

## Active scope

Perform the separate coordinated lifecycle transition that activates exact verified R2 as the runtime diagnostic candidate. Until that transition sets `runtime_test_outstanding = true`, do not import/test R2 and do not move runtime attribution away from the last completed R1 run.

The observed Shy Guy failure to follow the player from inside to outside remains a separate scope explained by inherited Scopophobia `Can Exit Facility = false`; it is not part of the current BCMER interior-only spawn correction.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the diagnostic path is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
