# Mouth Dog / Eyeless Dog -> Pikmin Patch Boundary and Successor Plan

**Status:** ANALYSIS COMPLETE / SUCCESSOR MAY BE PLANNED, NOT YET BUILT  
**Baseline:** S1.42AF — Path-Length-Safe Microwave Packaging  
**Source evidence:** `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`  
**Compatibility finding:** `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`  
**Patch safety authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  

## Decision

The S1.42AF Mouth Dog / Eyeless Dog -> Pikmin compatibility gap has an exact, narrow prevention point in LethalMinNightly 1.1.108.

The preferred patch boundary is the exact declared method:

`LethalMin.MouthDogPikminEnemy.DoCheckInterval()`

A `Priority.First` prevention-only Harmony prefix may return `false` from this method so the Mouth Dog adapter does not select nearby Pikmin, send bite RPCs, append them to its `GrabbedPikmin` list, invoke `PikminAI.GrabPikmin(...)`, or start its bite/kill animation because of Pikmin.

Do **not** disable `MouthDogPikminEnemy` itself. Do **not** perform delayed Pikmin-state repair. Do **not** use a broad `PikminEnemy` or `EnemyAI` patch.

## Config result

The exact S1.42AF LethalMin config exposes only:

- `Eyeless Dog Bite Cooldown`
- `Eyeless Dog Bite Limit`

The exact LethalMin 1.1.108 source correspondingly declares only `MouthDog_BiteCooldown` and `MouthDog_BiteLimit` for this interaction. There is no native boolean configuration that disables Mouth Dog / Eyeless Dog -> Pikmin targeting or biting while preserving Pikmin -> Mouth Dog combat.

`Bite Limit = 0` is not a valid disable mechanism. `MouthDogPikminEnemy.DoCheckInterval()` adds a nearby eligible Pikmin to `PikminRefs` before checking whether `PikminRefs.Count >= BiteLimmit`; a zero limit can therefore still admit the first Pikmin.

## Exact ownership and call path

LethalMin 1.1.108 registers the adapter mapping:

`MouthDogAI -> MouthDogPikminEnemy`

and `MouthDogPikminEnemy` inherits `PikminEnemy`.

The exact harmful path is:

1. `MouthDogPikminEnemy.LateUpdate()` runs only for the network owner while the Mouth Dog is lunging, not already in kill animation, and not dead.
2. Once the bite/check cooldown permits, it calls `DoCheckInterval()`.
3. `DoCheckInterval()` enumerates `PikminEnemy.GetNearbyPikmin()`.
4. Eligible nearby Pikmin are added to `PikminRefs` up to the configured bite limit.
5. The adapter sends `BiteNearbyPikminServerRpc(...)` / `BiteNearbyPikminClientRpc(...)`.
6. `BiteNearbyPikmin(List<PikminAI>)` performs, for each victim:
   - `GrabbedPikmin.Add(Pikmin)`;
   - `Pikmin.GrabPikmin(mouthDogAI.mouthGrip, 2.5f, 5)`.
7. The adapter then starts `DoBiteAnim()`.

This exactly matches the S1.42AF runtime evidence where two White Pikmin were attached to `EnemyAttackMouth` and received 2.5-second grab/death timers.

## Why the existing common GrabPikmin guard is necessary but not sufficient

`Patches/S139CompatibilityFixes/Plugin.cs` already patches the exact declared:

`LethalMin.PikminAI.GrabPikmin(Transform,float,int)`

with a `Priority.First` prevention-only prefix for proven enemy-specific gaps.

The decompiled `GrabPikmin` body confirms that the harmful Pikmin state mutation occurs inside this method. In the lethal branch it sets or drives state including:

- `IsGrabbedByEnemy = true`;
- `grabDeathTimer = deathDelay`;
- `DeathSnapToPos = snapPos`;
- `Laying = true`;
- reset/removal of leader, item, enemy, latch, task and override-position state;
- `Pintent.Stuck`.

Therefore the existing guard is correctly positioned before the core Pikmin mutation.

However, adding Mouth Dog detection only to that common guard would still allow `MouthDogPikminEnemy.BiteNearbyPikmin()` to append Pikmin to `GrabbedPikmin` before the guarded call and would still allow the Mouth Dog bite/kill animation path to start. That is narrower than the observed damage but does not fully satisfy the desired one-way contract.

The MouthDog-specific dispatcher is therefore the preferred primary prevention point. The existing exact `GrabPikmin` guard may remain unchanged as a separate failsafe for already-proven Crawler/Thumper and Baboon Hawk paths.

## Patch-safety boundary proof

The proposed patch satisfies the local patch safety policy because it is:

- **owner-specific:** exact LethalMin owner `MouthDogPikminEnemy`;
- **method-specific:** exact declared `DoCheckInterval()`;
- **prevention-before-mutation:** no Pikmin is collected or passed into the bite/grab pipeline;
- **asymmetric:** only Mouth Dog -> Pikmin behavior is blocked;
- **lifecycle-preserving:** `MouthDogPikminEnemy` remains enabled and continues inheriting native `PikminEnemy.Update()` lifecycle behavior;
- **non-repairing:** no delayed state restoration, forced release, task reconstruction or leader repair;
- **non-global:** no broad `EnemyAI`, `PikminEnemy`, collider or scene scan patch;
- **fail-closed at installation:** the local plugin must refuse to install a guessed fallback if the exact 1.1.108 method contract cannot be resolved.

## Required exact runtime reflection contract

A successor implementation should resolve:

- type: `LethalMin.MouthDogPikminEnemy`;
- method name: `DoCheckInterval`;
- binding scope: instance, public/non-public, `DeclaredOnly`;
- return type: `void`;
- parameter count: `0`;
- implementation body: non-null;
- declaring type: exactly `MouthDogPikminEnemy`.

Install a `Priority.First` prefix that logs initialization once and returns `false` when invoked.

No alternate method-name probing, base-type fallback, component disabling or generic target discovery should be used if validation fails.

## Preserved native direction: Pikmin -> Mouth Dog

The patch must not alter:

- LethalMin's `MouthDogAI -> MouthDogPikminEnemy` adapter registration;
- native Pikmin latch triggers and attack tasks against Mouth Dog;
- `PikminEnemy.Update()` death detection / trigger removal / unlatch lifecycle;
- enemy-body conversion/carry or Onion delivery behavior owned by LethalMin;
- Mouth Dog behavior toward players or non-Pikmin targets.

The desired contract remains:

- Mouth Dog / Eyeless Dog -> Pikmin: blocked before target selection / bite / grab state mutation.
- Pikmin -> Mouth Dog / Eyeless Dog: native LethalMin combat retained.

## Minimal successor plan

The next successor may be named **S1.42AG — Mouth Dog Pikmin One-Way Protection**.

It should be based only on the accepted guarded base:

`Profiles/LC V1 S1.42AF Microwave Fix.r2z`

SHA-256:

`6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`

Planned delta:

1. update `Patches/S139CompatibilityFixes/Plugin.cs` only as needed to install the exact `MouthDogPikminEnemy.DoCheckInterval()` `Priority.First` prevention prefix;
2. keep all S1.42AF mod/config/profile contents otherwise unchanged;
3. rebuild the local compatibility plugin through the existing repository-native build pipeline;
4. package the result on top of S1.42AF;
5. require a focused runtime test that proves Mouth Dog lunges near Pikmin without producing LethalMin Mouth Dog bite/grab/death-timer state while Pikmin can still attack the Dog;
6. also verify normal Mouth Dog -> player behavior remains intact and no new lifecycle/log-spam regression appears.

## Controller state

This document authorizes planning only. It does **not** arm `BuildSpecs/current.json` and does **not** create a candidate.

Until an explicit later implementation/build segment:

- accepted baseline remains S1.42AF;
- latest built artifact remains S1.42AF;
- active candidate remains none;
- runtime test remains none outstanding;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains S1.42AF;
- `BuildSpecs/current.json` remains disabled.

## Next action

In the next explicit segment, implement the exact local-plugin patch and prepare the S1.42AG build specification atomically. Do not perform runtime acceptance or promote any result without a new built artifact and its dedicated runtime evidence.
