# S1.42AK-CFDIAG1 Source / Pure-Static Findings

**Date:** 2026-10-07  
**Status:** SOURCE / PURE-STATIC STAGED / PR VALIDATION PENDING / DIAGNOSTIC ONLY / NOT BUILT / NOT ARMED / NEVER ACCEPT  
**Authority:** `Current/315_S1.42AK_PHASE_C_CIRCUS_FACILITY_CFDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`  
**Implementation base:** `052ab8ab5443810917ce0bdf38d611c5362c6cb5`

## Implemented contract

The isolated source root is `Patches/S142AKCFDiag1/`. It implements the separately frozen `S1.42AK-CFDIAG1` / `S142AKCFDiag1` / `tendas.lethalcompany.s142akcfdiag1` / `[CFDIAG1]` identity.

Exactly one intended Harmony surface targets `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` as a postfix after the accepted S1.42AB normalizer at `Priority.Last`. The real Offense selection path may retain only the unique already-returned `Circus Facility` wrapper with exact `CircusFacilityFlow` asset and final rarity `100`, retaining the same wrapper object.

Pure tests cover the exact positive target plus non-Offense/debug inertness, terminal exclusion, unknown caller, null/empty pool, missing accessors, null wrappers, missing/duplicate Circus Facility, asset mismatch, rarity mismatch and wrapper identity. Refusal paths preserve pool count and object order.

`Patches/S142AKCFDiag1/PATCH_SAFETY_REVIEW.md` preserves LLL registration/viability ownership, accepted-normalizer ownership and all downstream generation/CullFactory/teleport/NavMesh/PathfindingLib/enemy/scrap/cleanup lifecycles. No availability, registration, global rarity, RNG, RPC, generation, BCMER or BMDSFIX1 mutation is introduced.

## Validation pending

The dedicated CFDIAG1 source/static gate and Knowledge Architecture must pass on the exact PR head before this staged implementation may be classified SOURCE / PURE-STATIC PASS.

## Lifecycle boundary

`BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`, S1.42AK remains accepted, and S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED with its selector-free Black Mesa x `DeepSewersFlow` gate outstanding and unwaived. Residual remains 25 until actual Circus Facility runtime evidence exists.

No review profile, publication, Gale import, activation or runtime is authorized by this staged source/static checkpoint.
