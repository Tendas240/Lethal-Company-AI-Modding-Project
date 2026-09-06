# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `RuntimeEvidence/S1.42AF/20260905T223738Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
**Code:** `Patches/S139CompatibilityFixes/Plugin.cs`  
**Related:** `Knowledge/ENEMY_SPAWN_BASELINE.md`, `Knowledge/CURRENT_LIFECYCLE.md`  
**Last-Validated:** 2026-09-06

## Ownership principle

Native LethalMin owns normal Pikmin -> enemy combat, enemy death handling, latch removal, task completion, dead-body carry and Onion delivery. Project-local code blocks only proven Enemy -> Pikmin gaps and must preserve that native lifecycle.

Prefer prevention before mutation. Never disable an entire foreign component merely to suppress one interaction unless its complete lifecycle is proven safe to lose.

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

### Proven S1.42AG partial fix

Exact LethalMin 1.1.108 source proved `MouthDogPikminEnemy.DoCheckInterval()` is the adapter-specific target/bite dispatcher and the bite path mutates `GrabbedPikmin` before calling `PikminAI.GrabPikmin(...)`.

S1.42AG's exact `Priority.First` prevention Prefix armed and executed. Runtime evidence proves it removed the prior `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab/death-timer signature and reduced `Work state with no task assigned!` from 707 in the S1.42AF exposure run to 0.

Keep this prevention-before-mutation result as useful proven evidence. It is not the complete one-way solution.

### Proven Vanilla V81 noise-position path

The provenance-safe MouthDog capture proves `MouthDogAI.DetectNoise(...)` consumes a world-space position. Native pursuit stores and follows `noisePositionGuess` and can enter a lunge near that position.

Therefore `targetPos` / `lastheardnoisePosition` diagnostics prove a position-pursuit mechanism, not a Pikmin-specific target handle.

### Proven Vanilla V81 generic EnemyAI collision path

Vanilla `MouthDogAI.OnCollideWithEnemy(Collider other, EnemyAI collidedEnemy = null)` is a separate attack surface. For a different enemy type after its cooldown it can rotate toward the collided enemy, enter a lunge in chase state and call `collidedEnemy.HitEnemy(2, ...)`.

Exact LethalMin 1.1.108 evidence proves `PikminAI : EnemyAI`. Pikmin can therefore enter this generic native collision path without the Dog knowing they are Pikmin.

### Proven Vanilla V81 base collision contract

The targeted source capture under `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/` proves exact `EnemyAI.OnCollideWithEnemy()` is debug-only. It conditionally logs the collision on the server when `debugEnemyAI` is enabled and performs no gameplay, targeting, navigation, damage, grab, cleanup or lifecycle mutation.

This closes the prior safety uncertainty around bypassing the MouthDog override for an exactly identified Pikmin collision: no hidden base gameplay responsibility would be lost. The only base effect is optional debug logging.

### Proven LethalMin carry/noise contract

Existing exact LethalMin source proves `PikminItem.GrabPikminItemOnLocalClient()` starts `CarryNumerator()`, parents the item to the primary Pikmin's hold position, marks it held by an enemy and disables normal physics.

`PikminItem.CarryNumerator()` repeatedly calls:

`pikmin.PlayAudioOnLocalClient("ItemCarry", PlayOnVoice: true, vol);`

for each carrier. Exact `PikminAI.PlayAudioOnLocalClient(...)` evidence proves that when audible-noise suppression is off, it can call `RoundManager.PlayAudibleNoise(...)` at the Pikmin transform. The accepted config has `Dont Make Audible Noises = false`.

Therefore carrying an item is source-proven to generate recurring audible noise through the carrying Pikmin at the carrier's world position.

The stronger claim that Vanilla MouthDogAI semantically selects a Purple Pikmin because it carries `GoldBar(Clone)`, or that the GoldBar itself is the proved recurring carry-noise emitter, is unsupported/rejected. Exact causality for the observed S1.42AG chase remains unproved; the source proves capability and attack surfaces, not which single audible event triggered that runtime observation.

## Current MouthDog successor boundary

All source proofs required before successor design are now closed. Current analysis authority is `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`.

The next action is **not** another source capture, build or gameplay test. It is the successor-specific safety review under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

That review must determine the smallest exact patch surface and explicitly preserve:

- MouthDog -> player behavior;
- native Pikmin -> MouthDog attack/latch/death/unlatch/task lifecycle;
- enabled native LethalMin ownership;
- the proven S1.42AG prevention-before-mutation guard where still required;
- passive follower non-aggression as normal behavior.

Forbidden broader alternatives remain:

- broad `EnemyAI` scanning or fallback Harmony targeting;
- whole `MouthDogPikminEnemy` disable;
- manual Pikmin state reconstruction;
- guessed method/signature interception;
- building from rejected S1.42AG as gameplay base.

A future successor must be a one-variable risky-patch delta against accepted S1.42AF and must deliberately test both directions: MouthDog -> Pikmin protection and Pikmin -> MouthDog attack/latch/death-unlatch behavior. Passive follower observation does not satisfy the reverse-direction gate.

No successor is currently armed and no runtime test is pending.

## CodeRebirth utility kills

The cumulative compatibility plugin also shields Pikmin/Puffmin from CodeRebirth utility kill RPCs, providing a direct failsafe for established utility-kill gaps.

## Diagnostic EnemyIsolation

EnemyIsolation was temporary test infrastructure only and defaults off. Do not restore continuous global EnemyAI scanning as normal gameplay behavior.

## Patch safety

Any future custom compatibility patch must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`. Compilation, main-menu load or disappearance of the directly targeted symptom is not sufficient for promotion.
