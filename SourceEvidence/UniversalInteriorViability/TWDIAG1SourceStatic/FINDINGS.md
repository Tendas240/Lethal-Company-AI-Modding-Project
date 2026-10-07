# S1.42AK-TWDIAG1 Source / Pure-Static Findings

**Date:** 2026-10-07  
**Status:** SOURCE / PURE-STATIC STAGED / VALIDATION PENDING / DIAGNOSTIC ONLY / NOT BUILT / NOT ARMED / NEVER ACCEPT  
**Authority:** `Current/290_S1.42AK_PHASE_C_STOREHOUSE_TWDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`  
**Implementation base:** `6307dc3830cde384152a78abe2ac4f9085bd5050`

## Implemented contract

The isolated source root is `Patches/S142AKTWDiag1/`. It implements the separately frozen `S1.42AK-TWDIAG1` / `S142AKTWDiag1` / `tendas.lethalcompany.s142aktwdiag1` / `[TWDIAG1]` identity.

Exactly one intended Harmony surface targets `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` as a postfix after the accepted S1.42AB normalizer at `Priority.Last`. The real Offense selection path may retain only the unique already-returned `Tower` wrapper with exact `TowerFlow` asset and final rarity `100`, retaining the same wrapper object.

Pure tests cover the exact positive target plus non-Offense/debug inertness, terminal exclusion, unknown caller, null/empty pool, missing accessors, null wrappers, missing/duplicate Tower, asset mismatch, rarity mismatch and wrapper identity. Refusal paths preserve pool count and object order.

`Patches/S142AKTWDiag1/PATCH_SAFETY_REVIEW.md` preserves LLL registration/viability ownership, accepted-normalizer ownership and all downstream generation/CullFactory/teleport/NavMesh/PathfindingLib/enemy/scrap/cleanup lifecycles. No availability, registration, global rarity, RNG, RPC, generation, BCMER or BMDSFIX1 mutation is introduced.

## Validation state

Exact PR-head validation through the dedicated TWDIAG1 source/static gate and Knowledge Architecture is pending. No source/static PASS is claimed yet.

## Lifecycle boundary

`BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`, S1.42AK remains accepted, and S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED with its selector-free Black Mesa x `DeepSewersFlow` gate outstanding and unwaived. Residual remains 26 until actual Tower runtime evidence exists.

No review profile, publication, Gale import, activation or runtime is authorized by this staged source/static checkpoint.

## Next lifecycle gate

Validate the staged S1.42AK-TWDIAG1 source/pure-static checkpoint on its exact PR head through the dedicated TWDIAG1 source/static gate and Knowledge Architecture. If both gates pass, reconcile the exact validation evidence into Current/303 and SourceEvidence, mark source/static validated, and advance only to the separate inactive review-build authorization/recipe decision. Do not construct, publish, Gale-import, activate or run a profile; do not change availability or owner restrictions; do not alter BMDSFIX1 or the accepted normalizer; do not rerun AGDIAG1 or DRDIAG1; and do not begin Oxyde, Shatteredrooms/CullFactory, BCMER x all-Pikmin, Herobrine, BMAFR1I1 or a BMDSFIX1 Deep Sewers reroll.
