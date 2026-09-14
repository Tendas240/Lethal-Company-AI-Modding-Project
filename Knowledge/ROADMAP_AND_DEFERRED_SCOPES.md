<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R1 candidate=none runtime_test_outstanding=false -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-14

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1R1**, SHA-256 `b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd`, now explicit **runtime diagnostic failed / repair analysis required / not accepted**. There is no active runtime candidate and no new gameplay test is outstanding.

R1 proved its metadata-derived LethalMin owner-type repair at runtime, then failed because required complex-owner type `ElevatorMod.Patches.EndlessElevator` was absent. DIAG1 invalidated and rolled back all owned Harmony hooks.

## Active scope

Analyze the exact installed EndlessElevator/LethalMin compatibility ownership contract and explain why the static/materialized gate treated `ElevatorMod.Patches.EndlessElevator` as mandatory although the actual R1 runtime profile did not expose that type. Repair source/static validation only after that contract is proven, then build a successor diagnostic only if required. Do not rerun DIAG1 or R1 unchanged.

The observed Shy Guy failure to follow the player from inside to outside is not folded into this repair: accepted S1.42AH and R1 both inherit Scopophobia `Can Exit Facility = false`, so inside-to-outside pursuit remains a separate scope unless explicitly selected.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the diagnostic repair question is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
