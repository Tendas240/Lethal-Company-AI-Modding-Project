# S1.42AK-TWDIAG1 Source / Pure-Static Findings

**Date:** 2026-10-07  
**Status:** SOURCE / PURE-STATIC PASS / DIAGNOSTIC ONLY / NOT BUILT / NOT ARMED / NEVER ACCEPT  
**Authority:** `Current/302_S1.42AK_PHASE_C_TOWER_TWDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`  
**Implementation base:** `6307dc3830cde384152a78abe2ac4f9085bd5050`

## Implemented contract

The isolated source root is `Patches/S142AKTWDiag1/`. It implements the separately frozen `S1.42AK-TWDIAG1` / `S142AKTWDiag1` / `tendas.lethalcompany.s142aktwdiag1` / `[TWDIAG1]` identity.

Exactly one intended Harmony surface targets `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` as a postfix after the accepted S1.42AB normalizer at `Priority.Last`. The real Offense selection path may retain only the unique already-returned `Tower` wrapper with exact `TowerFlow` asset and final rarity `100`, retaining the same wrapper object.

Pure tests cover the exact positive target plus non-Offense/debug inertness, terminal exclusion, unknown caller, null/empty pool, missing accessors, null wrappers, missing/duplicate Tower, asset mismatch, rarity mismatch and wrapper identity. Refusal paths preserve pool count and object order.

`Patches/S142AKTWDiag1/PATCH_SAFETY_REVIEW.md` preserves LLL registration/viability ownership, accepted-normalizer ownership and all downstream generation/CullFactory/teleport/NavMesh/PathfindingLib/enemy/scrap/cleanup lifecycles. No availability, registration, global rarity, RNG, RPC, generation, BCMER or BMDSFIX1 mutation is introduced.

## Exact PR validation PASS

Exact tested PR head `e219dd3a10aab703e0375623d61132b812672a29` passed both required gates:

- `S1.42AK TWDIAG1 source and pure static gate` — run `37590376145`, run #2 — **success**. Pure Tower policy tests, plugin compile and deterministic source/controller validation passed.
- `Knowledge Architecture` — run `37590376061`, run #2223 — **success**.


The earlier TWDIAG1 source/static run `37590228630` / #1 on superseded head `ae6bcb10ffdf47296627cd5218c001412f4fae46` failed only in the deterministic validator because five Machine-State lookups still used the stale `storehouse_twdiag1_*` prefix. The pure Tower policy tests and plugin compile had already passed on that head. Head `e219dd3a10aab703e0375623d61132b812672a29` changes only that validator-key prefix to the authorized `tower_twdiag1_*` namespace; run #2 then passes the complete gate. The failed #1 run is superseded and is not current source/static authority.

The later evidence-recording/final PR head must also pass both gates before merge.

## Lifecycle boundary

`BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`, S1.42AK remains accepted, and S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED with its selector-free Black Mesa x `DeepSewersFlow` gate outstanding and unwaived. Residual remains 26 until actual Tower runtime evidence exists.

No review profile, publication, Gale import, activation or runtime is authorized by this staged source/static checkpoint.

## Next lifecycle gate

Perform one bounded S1.42AK-TWDIAG1 inactive review-build authorization/recipe decision. Pin any future review recipe to exact parent S1.42AK-BMDSFIX1 profile SHA-256 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0, preserve the frozen short Gale identity LC V1 S1.42AK-TWD1, define the exact one-DLL archive delta and build/static validator contract, and decide whether a later inactive review-artifact construction may be authorized. Do not construct, publish, Gale-import, activate or run the TWDIAG1 profile in that decision; do not change availability or owner restrictions; do not alter BMDSFIX1 or the accepted normalizer; do not rerun AGDIAG1 or DRDIAG1; and do not begin Oxyde, Shatteredrooms/CullFactory, BCMER x all-Pikmin, Herobrine, BMAFR1I1 or a BMDSFIX1 Deep Sewers reroll.
