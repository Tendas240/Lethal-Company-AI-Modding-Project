# Mouth Dog / Eyeless Dog -> Pikmin Local Patch Safety Review

**Status:** PASS FOR IMPLEMENTATION / NO BUILD YET  
**Policy:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Evidence:** `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`  
**Decision:** `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`

## Result

**PASS.** Exact declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` is a sufficiently narrow prevention-before-mutation boundary.

The exact 1.1.108 source proves that `DoCheckInterval()` is the MouthDog-specific Pikmin selection dispatcher. Returning before it executes prevents nearby-Pikmin collection, bite RPC dispatch, `GrabbedPikmin.Add`, `PikminAI.GrabPikmin(mouthDogAI.mouthGrip, 2.5f, 5)`, and the resulting Pikmin-driven Dog bite animation.

## Policy checks

- **Exact owner:** PASS — `MouthDogPikminEnemy`, not global `EnemyAI`/`PikminEnemy`.
- **Prevention before mutation:** PASS — before target collection, adapter bookkeeping and `GrabPikmin`.
- **Reverse direction preserved:** PASS — no Pikmin attack/latch task is patched.
- **Lifecycle preserved:** PASS — adapter remains enabled, so inherited `PikminEnemy.Update()` death/trigger/unlatch cleanup remains available.
- **No delayed repair:** PASS — no state snapshot, follower/task restoration or forced release.
- **No broad component disable:** PASS.
- **Fail-closed install:** REQUIRED — exact declaring type, `void`, zero parameters and method body must validate; otherwise install no fallback.
- **No unrelated delta:** REQUIRED — S1.42AF remains unchanged except for the rebuilt local compatibility plugin.

## Rejected alternatives

- `Eyeless Dog Bite Limit = 0`: rejected; source checks the limit after admitting a Pikmin.
- extending only the common `PikminAI.GrabPikmin` guard: rejected as incomplete primary protection because MouthDog adapter bookkeeping and bite dispatch have already begun.
- disabling `MouthDogPikminEnemy`: rejected as broader than necessary and lifecycle-risking.
- patching `BiteNearbyPikmin`: later than necessary; `DoCheckInterval()` is the earlier exact adapter-specific prevention point.
- delayed state repair: rejected because a prevention point exists.

## Implementation acceptance criteria

A future S1.42AG code change passes this review only if it:

1. resolves exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`;
2. validates exact declaring type, instance `void`, zero parameters and non-null body;
3. installs `Priority.First`;
4. returns `false` without mutating Pikmin or disabling adapter lifecycle;
5. installs no guessed fallback;
6. leaves Mouth Dog -> player behavior and LethalMin config unchanged.

A future runtime gate must prove both directions: Dog -> Pikmin blocked during a real lunge, Pikmin -> Dog attack/death cleanup still native, and Dog -> player attack still functional. Clean startup alone is not acceptance.
