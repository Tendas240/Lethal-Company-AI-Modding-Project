# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `RuntimeEvidence/S1.42AF/20260905T223738Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
**Code:** `Patches/S139CompatibilityFixes/Plugin.cs`  
**Related:** `Knowledge/ENEMY_SPAWN_BASELINE.md`, `Knowledge/CURRENT_LIFECYCLE.md`  
**Last-Validated:** 2026-09-07

## Ownership principle

Native LethalMin owns normal Pikmin -> enemy combat, enemy death handling, latch removal, task completion, dead-body carry and Onion delivery. Project-local code blocks only proven Enemy -> Pikmin gaps and must preserve that native lifecycle.

Prefer prevention before mutation. Never disable an entire foreign component merely to suppress one interaction unless its complete lifecycle has been proven safe to lose.

## Accepted neighboring contracts

### Baboon Hawk

- Baboon Hawk -> Pikmin collision/bite/grab: blocked narrowly.
- Pikmin -> Baboon Hawk attack: allowed/native.
- `BaboonBirdPikminEnemy`: remains enabled.
- Native death/unlatch lifecycle: preserved.

### Thumper / Crawler

The proven Enemy -> Pikmin broken grab path is blocked before it mutates leader/grab/death-timer state. `Thumper Bite Limit = 3`; Crawler remains available for intended Pikmin counterattack.

### Puffer / Spore Lizard

Puffer -> Pikmin smoke/effect interaction is protected through a targeted compatibility boundary, not a broad enemy disable.

## Mouth Dog / Eyeless Dog — current boundary

S1.42AF remains the accepted gameplay base. S1.42AG remains **runtime rejected / partial fix / not accepted**.

Current successor safety authority:

`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`

Status:

**PASS FOR IMPLEMENTATION / SUCCESSOR NOT ARMED / NO BUILD YET**

### Proven S1.42AG partial fix

Exact LethalMin 1.1.108 source proves `MouthDogPikminEnemy.DoCheckInterval()` is the adapter-specific target/bite dispatcher.

S1.42AG's exact `Priority.First` prevention Prefix armed and executed. Runtime evidence proves it removed the prior `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab/death-timer signature and reduced `Work state with no task assigned!` from 707 in the S1.42AF exposure run to 0.

This guard remains part of the reviewed successor contract.

### Proven Vanilla V81 noise-position path

`MouthDogAI.DetectNoise(...)` consumes a world-space position. `noisePositionGuess` can drive pursuit/lunge behavior.

A carrying Pikmin can source recurring audible noise at its own transform when audible-noise suppression is disabled, as it is in accepted S1.42AF.

Therefore a Dog moving toward a Pikmin's current/recent position is not by itself proof of semantic Pikmin targeting. The successor must not patch `DetectNoise()` based on inferred source identity.

### Proven Vanilla V81 generic EnemyAI collision path

Vanilla declares:

`MouthDogAI.OnCollideWithEnemy(Collider other, EnemyAI collidedEnemy = null)`

For a different enemy type after cooldown it can lunge and call:

`collidedEnemy.HitEnemy(2, ...)`

Exact LethalMin source proves:

`PikminAI : EnemyAI`

So Pikmin can enter this native generic-enemy path solely through inheritance.

### Proven base contract

Exact V81 `EnemyAI.OnCollideWithEnemy()` is debug-only. It performs no gameplay, targeting, navigation, damage, grab, cleanup or lifecycle mutation.

This makes a Pikmin-only skip of the MouthDog override safe with respect to hidden base gameplay responsibilities.

## Reviewed successor architecture

The minimum exact successor is:

1. **retain** exact `Priority.First` Prefix on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`;
2. **add** exact `Priority.First` Prefix on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)`;
3. skip that Vanilla override only when the actual `collidedEnemy` is a validated runtime `LethalMin.PikminAI`.

Required fail-closed behavior:

- declared-only exact target resolution;
- exact declaring type;
- exact return/parameter contract;
- non-null method body;
- validate `LethalMin.PikminAI` derives from `EnemyAI`;
- no guessed target fallback.

Forbidden:

- name heuristics;
- global `EnemyAI` scanning;
- broad reflection patching;
- whole `MouthDogPikminEnemy` disable;
- manual Pikmin-state repair;
- patching `DetectNoise()`;
- patching `OnCollideWithPlayer()`;
- building from rejected S1.42AG.

## Lifecycle preservation

`MouthDogPikminEnemy` remains enabled so inherited `PikminEnemy` lifecycle remains active.

Native LethalMin continues to own:

- Pikmin -> MouthDog latch/attack;
- enemy death detection;
- trigger removal;
- unlatch/release;
- task completion;
- follow/idle restoration;
- dead-body/carry lifecycle.

MouthDog -> player remains a separate unpatched Vanilla path.

Non-Pikmin `EnemyAI` collisions pass through unchanged.

## One-variable successor rule

The successor must be a risky-patch delta against exact accepted S1.42AF.

Only the local compatibility DLL may change functionally, plus the necessary profile identity metadata. Packages and unrelated configs remain unchanged.

No candidate currently exists.

## Future runtime gates

A later candidate must deliberately verify:

- adapter-path Dog -> Pikmin protection;
- Vanilla-collision Dog -> Pikmin protection;
- native Pikmin -> Dog latch/attack/death/unlatch/task completion;
- Dog -> player;
- repeated protected collisions;
- non-Pikmin neighbor behavior;
- logs.

A passive follower is not a reverse-direction test. A noise-driven lunge toward an audible Pikmin position is not automatically a failure.

## Current lifecycle

- accepted: S1.42AF;
- latest built: S1.42AG, rejected partial fix;
- active candidate: none;
- successor armed: no;
- runtime test pending: no.

Exact next action is implementation/build preparation of the reviewed successor from S1.42AF in a later explicit project segment.

## CodeRebirth utility kills

The cumulative compatibility plugin also shields Pikmin/Puffmin from CodeRebirth utility kill RPCs, providing a direct failsafe for established utility-kill gaps.

## Diagnostic EnemyIsolation

EnemyIsolation was temporary test infrastructure only and defaults off. Do not restore continuous global EnemyAI scanning as normal gameplay behavior.

## Patch safety

Any future custom compatibility patch must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`. Compilation, main-menu load or disappearance of the directly targeted symptom is not sufficient for promotion.
