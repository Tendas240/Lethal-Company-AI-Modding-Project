# Mouth Dog / Eyeless Dog -> Pikmin Patch Boundary and Successor Plan

**Status:** ANALYSIS COMPLETE / SUCCESSOR PLANNED / NOT BUILT / NOT ARMED  
**Baseline:** S1.42AF — Path-Length-Safe Microwave Packaging  
**Exact source evidence:** `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`  
**Original runtime finding:** `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`  
**Patch safety:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Decision

The preferred primary prevention boundary is exact declared:

`LethalMin.MouthDogPikminEnemy.DoCheckInterval()`

A `Priority.First` prevention-only prefix should return `false` before the Mouth Dog adapter selects nearby Pikmin. Do not disable `MouthDogPikminEnemy`, do not patch a generic base class, and do not repair Pikmin state after mutation.

## Config result

LethalMinNightly 1.1.108 exposes only `Eyeless Dog Bite Cooldown` and `Eyeless Dog Bite Limit` for this interaction. There is no native one-way boolean disable. `Bite Limit = 0` is not a safe disable mechanism because `DoCheckInterval()` adds a Pikmin before checking the limit.

## Exact source path

LethalMin registers `MouthDogAI -> MouthDogPikminEnemy`, with `MouthDogPikminEnemy : PikminEnemy`.

The harmful path is:

`MouthDogPikminEnemy.LateUpdate()`
-> `DoCheckInterval()`
-> `PikminEnemy.GetNearbyPikmin()`
-> bite RPCs
-> `BiteNearbyPikmin(List<PikminAI>)`
-> `GrabbedPikmin.Add(Pikmin)`
-> `Pikmin.GrabPikmin(mouthDogAI.mouthGrip, 2.5f, 5)`
-> `DoBiteAnim()`.

The exact `PikminAI.GrabPikmin(Transform,float,int)` body then performs the harmful grabbed/death-timer/task/leader/latch mutation observed in S1.42AF.

## Why the common GrabPikmin guard alone is insufficient

`Patches/S139CompatibilityFixes/Plugin.cs` already applies an exact `Priority.First` guard to `PikminAI.GrabPikmin(Transform,float,int)` for proven Crawler/Thumper and Baboon Hawk gaps. That position is before core Pikmin mutation, but a Mouth Dog reaches it only after `MouthDogPikminEnemy.BiteNearbyPikmin()` has already appended the Pikmin to its own `GrabbedPikmin` list; the Dog bite-animation path also remains active.

Therefore the common guard is a valid lower-level failsafe concept but not the preferred complete Mouth Dog contract. `DoCheckInterval()` prevents the interaction earlier, before target collection, RPC dispatch, adapter bookkeeping and Pikmin grab mutation.

## Exact implementation contract

A successor must resolve and validate:

- type: `LethalMin.MouthDogPikminEnemy`;
- method: `DoCheckInterval`;
- exact declaring type: `MouthDogPikminEnemy`;
- instance method;
- return type `void`;
- zero parameters;
- non-null method body.

Install a `Priority.First` prefix only after all checks pass. On mismatch, log an error and install no guessed fallback.

## Preserved native direction

Keep `MouthDogPikminEnemy` enabled so native `PikminEnemy.Update()` lifecycle remains available. Do not alter native Pikmin -> Mouth Dog latch/attack/death cleanup, enemy-body handling, or Mouth Dog -> player behavior.

Desired asymmetric contract:

- Mouth Dog / Eyeless Dog -> Pikmin: blocked before targeting/bite/grab state mutation;
- Pikmin -> Mouth Dog / Eyeless Dog: native LethalMin combat retained.

## Minimal successor

Planned successor: **S1.42AG — Mouth Dog Pikmin One-Way Protection**.

Guarded base:

`Profiles/LC V1 S1.42AF Microwave Fix.r2z`

SHA-256:

`6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`

Only the local compatibility plugin should change functionally. All S1.42AF mod/config/profile behavior remains otherwise unchanged.

This planning decision does not arm `BuildSpecs/current.json`, does not create an artifact, does not create an active candidate and does not create an outstanding runtime test.

## Next action

In the next explicit segment, implement the exact guard and prepare/arm the S1.42AG build specification atomically, then build repository-native from S1.42AF. Runtime acceptance begins only after a successful candidate artifact exists.
