# Mouth Dog / Eyeless Dog -> Pikmin Local Patch Safety Review

**Status:** PASS FOR IMPLEMENTATION PLANNING / NO BUILD YET  
**Baseline:** S1.42AF  
**Policy authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Primary evidence:** `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`  
**Patch-boundary decision:** `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`

## Review question

Can the inherited Mouth Dog / Eyeless Dog -> Pikmin compatibility gap be corrected with a narrow, prevention-before-mutation local patch without taking ownership of native Pikmin -> Mouth Dog combat or broad LethalMin lifecycle behavior?

## Result

**PASS.** The exact declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` method is a sufficiently narrow prevention boundary for implementation.

## Evidence chain

The exact LethalMinNightly 1.1.108 source establishes:

- `MouthDogAI` is explicitly mapped to `MouthDogPikminEnemy`;
- `MouthDogPikminEnemy` inherits `PikminEnemy`;
- its `LateUpdate()` calls `DoCheckInterval()` only while the local owner controls a live, lunging Mouth Dog that is not already in kill animation and after bite/check cooldown conditions permit;
- `DoCheckInterval()` is the MouthDog-specific function that enumerates nearby Pikmin and populates `PikminRefs`;
- only after that selection does the adapter enter its bite RPC path;
- `BiteNearbyPikmin(List<PikminAI>)` adds each Pikmin to the adapter's `GrabbedPikmin` list and calls `PikminAI.GrabPikmin(mouthDogAI.mouthGrip, 2.5f, 5)`;
- `PikminAI.GrabPikmin(...)` performs the harmful grabbed/death-timer/task/leader/latch state mutation observed in S1.42AF.

Therefore returning `false` before `DoCheckInterval()` executes prevents target collection and all downstream Dog -> Pikmin bite/grab state while leaving the adapter component and its inherited lifecycle enabled.

## Policy checks

### Narrowest proven owner
PASS — patch targets `MouthDogPikminEnemy`, not global `EnemyAI`, `PikminEnemy`, `PikminAI.Update` or scene scans.

### Prevention before harmful mutation
PASS — suppression occurs before `PikminRefs` population, bite RPC dispatch, `GrabbedPikmin.Add` and `PikminAI.GrabPikmin`.

### Preserve native opposite direction
PASS — native Pikmin latch/attack behavior against Mouth Dog is owned by the still-enabled `PikminEnemy` adapter lifecycle and is not patched by the proposed guard.

### Preserve cleanup lifecycle
PASS — `MouthDogPikminEnemy` remains enabled; inherited `PikminEnemy.Update()` remains available for enemy death, trigger removal, grabbed-Pikmin release and latch cleanup.

### No delayed repair
PASS — proposal performs no state snapshot, leader/task restoration, forced `ReleaseFromGrab`, coroutine cleanup or post-damage repair.

### No broad component disable
PASS — proposal does not disable `MouthDogPikminEnemy` or its colliders/triggers.

### Fail-closed target resolution
PASS CONDITION — implementation must install only if the exact declared zero-parameter `void DoCheckInterval()` with an implementation body validates. Failure must log and install no guessed fallback.

### No unrelated behavior change
PASS CONDITION — S1.42AG must carry forward S1.42AF unchanged except for the rebuilt local compatibility plugin. Mouth Dog -> player behavior and all LethalMin config values remain untouched.

## Rejected alternatives

### Config-only `Eyeless Dog Bite Limit = 0`
Rejected. The exact source adds a Pikmin to `PikminRefs` before evaluating the configured limit, so zero is not a reliable disable contract and would also encode intent through an undocumented numeric edge case.

### Extend only the common `PikminAI.GrabPikmin` guard
Rejected as incomplete primary protection. It would prevent core Pikmin grab/death state but only after the MouthDog adapter has already appended the victim to its `GrabbedPikmin` list; the bite animation path would still be entered.

### Disable `MouthDogPikminEnemy`
Rejected. This would be broader than necessary and risks suppressing native `PikminEnemy` lifecycle responsibilities required for the preserved Pikmin -> Mouth Dog direction.

### Patch `BiteNearbyPikmin` instead
Technically possible but not preferred. It is later than the proven targeting dispatcher and would still allow nearby Pikmin collection and network bite-dispatch activity. `DoCheckInterval()` prevents the interaction earlier with a smaller behavioral surface.

### Delayed state repair
Rejected. A clean prevention point exists before mutation.

## Implementation acceptance criteria

A future code change passes this review only if it:

1. resolves exact type `LethalMin.MouthDogPikminEnemy`;
2. resolves exact declared instance `DoCheckInterval()`;
3. validates `void`, zero parameters, exact declaring type and non-null method body;
4. installs a `Priority.First` prefix;
5. the prefix returns `false` without mutating Pikmin, Mouth Dog or adapter lifecycle state;
6. no generic fallback is installed on contract mismatch;
7. no unrelated plugin/config/profile delta is introduced.

## Runtime regression requirements

The eventual candidate must demonstrate both sides of the asymmetric contract:

- Dog -> Pikmin interaction is absent during a real Dog lunge with Pikmin in range;
- Pikmin -> Dog attack/latch/death cleanup remains functional;
- Dog -> player attack remains functional.

A clean startup alone is insufficient for acceptance.

## Review conclusion

The local patch safety boundary is proven sufficiently to proceed to implementation/build planning. This review does not itself authorize acceptance, does not build a candidate and does not arm the build controller.
