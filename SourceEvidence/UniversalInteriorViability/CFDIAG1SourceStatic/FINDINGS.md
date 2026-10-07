# S1.42AK-CFDIAG1 Source / Pure-Static Findings

**Date:** 2026-10-07  
**Status:** SOURCE / PURE-STATIC PASS / DIAGNOSTIC ONLY / NOT BUILT / NOT ARMED / NEVER ACCEPT  
**Authority:** `Current/315_S1.42AK_PHASE_C_CIRCUS_FACILITY_CFDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`  
**Implementation base:** `052ab8ab5443810917ce0bdf38d611c5362c6cb5`

## Implemented contract

The isolated source root is `Patches/S142AKCFDiag1/`. It implements the separately frozen `S1.42AK-CFDIAG1` / `S142AKCFDiag1` / `tendas.lethalcompany.s142akcfdiag1` / `[CFDIAG1]` identity.

Exactly one intended Harmony surface targets `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` as a postfix after the accepted S1.42AB normalizer at `Priority.Last`. The real Offense selection path may retain only the unique already-returned `Circus Facility` wrapper with exact `CircusFacilityFlow` asset and final rarity `100`, retaining the same wrapper object.

Pure tests cover the exact positive target plus non-Offense/debug inertness, terminal exclusion, unknown caller, null/empty pool, missing accessors, null wrappers, missing/duplicate Circus Facility, asset mismatch, rarity mismatch and wrapper identity. Refusal paths preserve pool count and object order.

`Patches/S142AKCFDiag1/PATCH_SAFETY_REVIEW.md` preserves LLL registration/viability ownership, accepted-normalizer ownership and all downstream generation/CullFactory/teleport/NavMesh/PathfindingLib/enemy/scrap/cleanup lifecycles. No availability, registration, global rarity, RNG, RPC, generation, BCMER or BMDSFIX1 mutation is introduced.

## Exact PR validation PASS

Exact tested PR head `85bbd2177610f1afd42f79bc112b8cea6e70a951` passed both required gates:

- `S1.42AK CFDIAG1 source and pure static gate` — run `37652145272`, run #1 — **success**. Pure Circus Facility policy tests, plugin compile and deterministic source/controller validation passed.
- `Knowledge Architecture` — run `37652145042`, run #1327 — **success**.

The later evidence-recording/final PR head must also pass both gates before merge.

## Lifecycle boundary

`BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`, S1.42AK remains accepted, and S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED with its selector-free Black Mesa x `DeepSewersFlow` gate outstanding and unwaived. Residual remains 25 until actual Circus Facility runtime evidence exists.

No review profile, publication, Gale import, activation or runtime is authorized by this staged source/static checkpoint.

## Next lifecycle gate

Perform one bounded S1.42AK-CFDIAG1 inactive review-build authorization/recipe decision. Pin any future review recipe to exact parent S1.42AK-BMDSFIX1 profile SHA-256 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0, preserve the frozen short Gale identity LC V1 S1.42AK-CFD1, define the exact one-DLL archive delta and build/static validator contract, and decide whether a later inactive review-artifact construction may be authorized. Do not construct, publish, Gale-import, activate or run the CFDIAG1 profile in that decision; do not change availability or owner restrictions; do not alter BMDSFIX1 or the accepted normalizer; do not rerun TWDIAG1, SHDIAG1, LFDIAG1, DRDIAG1 or AGDIAG1; do not reopen the completed post-recurrence array attribution or Oxyde; and do not begin Shatteredrooms/CullFactory, BCMER x all-Pikmin, Herobrine, BMAFR1I1 or a BMDSFIX1 Deep Sewers reroll.
