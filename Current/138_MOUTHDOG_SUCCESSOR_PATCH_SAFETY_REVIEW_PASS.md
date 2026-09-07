# MouthDog Successor Patch Safety Review — PASS

**Status:** CURRENT / PASS FOR IMPLEMENTATION / SUCCESSOR NOT ARMED / NO BUILD YET  
**Policy:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Supersedes current-analysis role of:** `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`  
**Historical predecessor review:** `Current/132_MOUTHDOG_PATCH_SAFETY_REVIEW.md`  
**Accepted baseline:** S1.42AF — Path-Length-Safe Microwave Packaging  
**Rejected partial fix:** S1.42AG — Mouth Dog Pikmin One-Way Protection  
**Last-Validated:** 2026-09-07

## Decision

**PASS FOR IMPLEMENTATION.**

The successor-specific MouthDog safety review is complete. The smallest evidence-supported one-way protection contract is a dual prevention-only boundary:

1. retain the proven `Priority.First` Prefix on exact declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`;
2. add one exact `Priority.First` Prefix on declared Vanilla V81 `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` which skips only when the supplied `collidedEnemy` is a validated `LethalMin.PikminAI`.

No successor is armed by this decision and no runtime test is pending.

## Exact owners and harmful paths

### LethalMin adapter path

Exact LethalMin 1.1.108 evidence proves:

`MouthDogPikminEnemy.LateUpdate()`
-> `DoCheckInterval()`
-> nearby Pikmin collection
-> bite RPC dispatch
-> `BiteNearbyPikmin(...)`
-> `GrabbedPikmin.Add(...)`
-> `PikminAI.GrabPikmin(mouthDogAI.mouthGrip, 2.5f, 5)`
-> harmful grab/death-timer/task/leader mutation.

S1.42AG runtime evidence proves that blocking exact `DoCheckInterval()` before this mutation is effective. The prior `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab signature disappeared and `Work state with no task assigned!` fell from 707 in the exposure baseline to 0.

Therefore this guard remains required in the successor.

### Vanilla collision path

Exact Vanilla V81 evidence proves:

`MouthDogAI.OnCollideWithEnemy(Collider other, EnemyAI collidedEnemy = null)`

can, for a different enemy type after its cooldown:

- rotate toward the collided enemy;
- set `inLunge = true` and call `EnterLunge()`;
- reset `timeSinceHittingOtherEnemy`;
- call `collidedEnemy.HitEnemy(2, null, playHitSFX: true)`.

Exact LethalMin source proves `PikminAI : EnemyAI`, so Pikmin can enter this generic Vanilla path through inheritance alone.

Exact V81 `EnemyAI.OnCollideWithEnemy()` is debug-only and performs no gameplay, navigation, targeting, damage, grab, cleanup or lifecycle mutation. Skipping the MouthDog override for an exactly identified Pikmin therefore does not suppress hidden base gameplay responsibilities.

## Exact Harmony target validation

### Retained LethalMin target

Resolve only:

`LethalMin.MouthDogPikminEnemy.DoCheckInterval()`

Required checks before patch installation:

- exact type resolution;
- `BindingFlags.DeclaredOnly`;
- exact declaring type;
- instance / non-static;
- return type `void`;
- zero parameters;
- non-null implementation body;
- no guessed fallback.

Install the Prefix at `Priority.First`.

### New Vanilla target

Resolve only declared:

`MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)`

Required checks before patch installation:

- exact declaring type `MouthDogAI`;
- declared-only instance method;
- return type `void`;
- exactly two parameters;
- parameter 1 exactly `UnityEngine.Collider`;
- parameter 2 exactly `EnemyAI`;
- non-null implementation body;
- no method-name scan or fallback.

Resolve `LethalMin.PikminAI` once through the established optional-runtime contract and verify it is assignable to `EnemyAI`.

The Prefix must return `false` only when `collidedEnemy != null` and the resolved `PikminAI` type identifies that supplied object. Every other `EnemyAI` and null collision must return `true`.

No name heuristics, `enemyType.enemyName` filtering, global object search, per-frame reflection or broad `EnemyAI` patch is permitted.

## Inheritance, lifecycle and state ownership

`MouthDogPikminEnemy` must remain enabled.

It inherits `LethalMin.PikminEnemy`, whose native lifecycle owns:

- latch trigger setup;
- Pikmin -> enemy damage routing;
- enemy-death detection;
- trigger removal;
- `GrabbedPikmin` release;
- native unlatch/cleanup.

Native LethalMin also owns Pikmin attack tasks, latch state, task completion, follow/idle restoration, enemy-body handling and Onion delivery.

The project patch must not reconstruct or manually mutate these states.

### Preserved directions

- MouthDog -> player: unchanged; `MouthDogAI.OnCollideWithPlayer(...)` remains unpatched.
- Pikmin -> MouthDog: unchanged; native `PikminEnemy` + `AttackEnemyTask` ownership remains active.
- MouthDog -> non-Pikmin EnemyAI: unchanged; the new Prefix passes through.
- MouthDog audible-noise perception: unchanged.

## Noise-position pursuit interpretation

`MouthDogAI.DetectNoise(...)` consumes a world-space `Vector3`, not a Pikmin target handle.

Exact LethalMin evidence proves item-carry audio can emit `RoundManager.PlayAudibleNoise(...)` at the carrying Pikmin's transform when `Dont Make Audible Noises = false`, which is the accepted configuration.

Therefore a MouthDog may legitimately move toward a position where a Pikmin produced audible noise. Visual movement toward a Pikmin is not, by itself, proof of semantic Pikmin targeting.

The successor must **not** patch `DetectNoise()` or infer source identity from a world-space position.

Runtime failure is instead defined by either:

- the LethalMin MouthDog adapter again selecting/biting/grabbing Pikmin; or
- the Vanilla `MouthDogAI.OnCollideWithEnemy()` path processing a real `PikminAI` collision.

## Secondary responsibilities

When an exact Pikmin collision is skipped, the MouthDog override will not:

- rotate toward that Pikmin as a generic enemy;
- enter the generic enemy-collision lunge for that Pikmin;
- reset `timeSinceHittingOtherEnemy` because of that Pikmin;
- call `PikminAI.HitEnemy(2, ...)`;
- execute the optional base debug log.

The missing base debug log is non-gameplay and accepted.

Not resetting the generic other-enemy cooldown for an ignored Pikmin collision is also intentional: a protected Pikmin must not consume the Dog's generic cooldown and thereby alter a subsequent legitimate MouthDog-vs-other-enemy collision.

Do not manually reproduce any of these skipped mutations.

## One-variable build delta

Any successor must be built from exact accepted:

`Profiles/LC V1 S1.42AF Microwave Fix.r2z`

SHA-256:

`6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`

Functional delta:

- only the local `S139CompatibilityFixes` DLL changes to implement the reviewed MouthDog protection;
- `export.r2x` may change only as necessary for the new profile identity;
- no package version changes;
- no unrelated config changes;
- do not build from rejected S1.42AG.

## Mandatory build gate

Before runtime testing:

1. local plugin compiles cleanly;
2. both exact Harmony targets validate;
3. `LethalMin.PikminAI : EnemyAI` validation passes;
4. no guessed fallback installs;
5. generated profile contains the expected compatibility DLL;
6. exact DLL SHA-256 is recorded;
7. exact profile SHA-256 is recorded;
8. archive diff against S1.42AF contains only intended files;
9. unrelated packages/configs are byte-preserved;
10. startup diagnostics prove both intended patch paths loaded;
11. old/forbidden broad-patch markers are absent;
12. a bounded Harmony patch-info diagnostic for the exact Vanilla collision target records co-patch ownership without performing a global scan.

Passing this gate is build-safe only, not gameplay-safe.

## Mandatory runtime regression gate

### A — Target behavior

Deliberately provoke MouthDog/Pikmin collision.

Required:

- exact collision-block marker appears;
- no MouthDog `Biting N Pikmin`;
- no `EnemyAttackMouth`;
- no 2.5-second MouthDog `GrabPikmin(..., 2.5f, 5)` state;
- no Vanilla MouthDog generic-enemy `HitEnemy(2)` processing of the Pikmin.

A noise-driven lunge toward a Pikmin position is not automatically a failure.

### B — Adjacent lifecycle

After a protected collision:

- Pikmin leader/follow/work state remains valid;
- `MouthDogPikminEnemy` remains enabled;
- no manual state repair is required.

### C — Reverse direction

Explicitly command/throw Pikmin onto the MouthDog.

Required:

- Pikmin can latch;
- Pikmin can attack;
- MouthDog can die through native Pikmin combat;
- native death -> unlatch -> task finish -> follow/idle cleanup succeeds.

Passive follower non-aggression is not this test.

### D — Repetition

Exercise at least two real MouthDog/Pikmin collision opportunities where practical. Do not infer pass from one non-event.

### E — Neighbor behavior

Verify:

- MouthDog -> player still functions normally;
- ordinary MouthDog audible-noise response remains present;
- non-Pikmin `EnemyAI` collisions are not filtered by the new Prefix;
- inherited S1.42AF gameplay/config contracts remain healthy.

### F — Logs

Require:

- both patch-install markers;
- at least one bounded collision-block marker;
- native task-completion evidence for the reverse test when expected;
- no `Work state with no task assigned!` burst;
- no `Leader is null when following`;
- no new `[Error  :S1.39 Compatibility Fixes]`;
- no new fatal/exception/retry flood attributable to the patch.

`Heard noise!`, `targetPos` and `lastheardnoisePosition` are not failures by themselves.

## Forbidden broader alternatives

Do not:

- patch `MouthDogAI.DetectNoise(...)` based on inferred source identity;
- patch `EnterLunge()` globally;
- patch `MouthDogAI.OnCollideWithPlayer(...)`;
- patch the base `EnemyAI.OnCollideWithEnemy(...)`;
- scan/patch broad `EnemyAI` surfaces;
- disable `MouthDogPikminEnemy`;
- reconstruct Pikmin state manually;
- add delayed repair layers;
- build from rejected S1.42AG.

## Current lifecycle decision

The successor-specific Patch Safety Review is complete and **PASS FOR IMPLEMENTATION**.

Current state remains:

- accepted baseline: S1.42AF;
- latest built artifact: S1.42AG, rejected partial fix;
- active candidate: none;
- runtime test outstanding: no;
- successor armed: no.

The exact next project action is a later explicit implementation/build segment: implement the reviewed dual prevention-only contract from S1.42AF, validate the build gates, and only after a successful candidate artifact exists begin runtime preparation.
