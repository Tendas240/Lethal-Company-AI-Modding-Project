# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MOUTHDOGAI_FOCUSED_DECOMPILE.txt`, `RuntimeEvidence/S1.42AF/20260905T223738Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
**Code:** `Patches/S139CompatibilityFixes/Plugin.cs`  
**Related:** `Knowledge/ENEMY_SPAWN_BASELINE.md`, `Knowledge/CURRENT_LIFECYCLE.md`  
**Last-Validated:** 2026-09-06

## Ownership principle

Native LethalMin owns normal Pikmin -> enemy combat, enemy death handling, latch removal, task completion, dead-body carry and Onion delivery. Project-local code blocks only proven Enemy -> Pikmin gaps and must preserve that native lifecycle.

Never repeat the S1.42R whole-component disable of `LethalMin.BaboonBirdPikminEnemy`. Disabling that component also suppressed inherited `PikminEnemy.Update()` death/unlatch cleanup.

## Baboon Hawk

Accepted asymmetric rule:

- Baboon Hawk -> Pikmin collision/bite/grab: blocked narrowly;
- Pikmin -> Baboon Hawk attack: allowed/native;
- `BaboonBirdPikminEnemy`: stays enabled;
- native death/unlatch lifecycle: preserved.

## Thumper / Crawler

The proven Enemy -> Pikmin broken grab path is blocked before it can mutate leader/grab/death-timer state.

Current accepted LethalMin configuration:

- `Thumper Bite Limit = 3`;
- `Crawler` is not in the Pikmin Attack Blacklist.

Do not revert to complete two-way noninteraction. Pikmin counterattack remains intended.

## Puffer / Spore Lizard

Puffer -> Pikmin smoke/effect interaction is protected by removing the LethalMin-injected Pikmin effect-trigger components from Puffer smoke. This is targeted protection, not a broad enemy disable.

## Mouth Dog / Eyeless Dog — current boundary after S1.42AG and Vanilla V81 capture

S1.42AG remains **runtime rejected / partial fix / not accepted**. S1.42AF remains the gameplay base.

### Proven LethalMin-specific prevention result

Exact LethalMin 1.1.108 source evidence proved `MouthDogPikminEnemy.DoCheckInterval()` as the adapter-specific target/bite dispatcher and `BiteNearbyPikmin` as the path that mutates `GrabbedPikmin` before `PikminAI.GrabPikmin(mouthGrip, 2.5f, 5)`.

S1.42AG's `Priority.First` prefix on exact `DoCheckInterval()` armed and executed. Runtime proves that this guard prevents that harmful mutation path:

- the prior Mouth Dog `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab-death-timer signature was absent;
- `Work state with no task assigned!` fell from 707 in the S1.42AF exposure run to 0;
- no compatibility-fix fatal/error marker was introduced.

Keep this prevention-before-mutation result as proven evidence. It is not, by itself, the complete one-way solution.

### Proven Vanilla V81 noise-position path

The successful provenance-safe V81 capture is authoritative under `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md` and `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`.

Vanilla `MouthDogAI.DetectNoise(Vector3 noisePosition, ...)` receives a world position. `EnrageDogOnLocalClient(...)` stores a world-space `noisePositionGuess`, sends the Dog toward that position, and records `lastHeardNoisePosition`. In chase state the Dog can call `EnterLunge()` once it is within less than 4 units of `noisePositionGuess`.

Therefore native `targetPos`/`lastheardnoisePosition` diagnostics are a position-pursuit contract. They do not prove a Pikmin-specific target handle.

### Proven Vanilla V81 generic EnemyAI collision path

Vanilla V81 also declares:

`MouthDogAI.OnCollideWithEnemy(Collider other, EnemyAI collidedEnemy = null)`

That override calls `base.OnCollideWithEnemy(...)`. For a different enemy type after its other-enemy cooldown, it can rotate toward the collided enemy, enter a lunge while in chase state, and call `collidedEnemy.HitEnemy(2, ...)`.

Exact LethalMin 1.1.108 evidence proves `PikminAI : EnemyAI`. A Pikmin can therefore enter this generic Vanilla collision path without the Dog knowing it is a Pikmin.

This is an independent native interaction surface outside the S1.42AG `DoCheckInterval()` guard.

### Pikmin audible-noise evidence

Exact LethalMin 1.1.108 evidence proves `PikminAI.PlayAudioOnLocalClient(...)` calls `RoundManager.PlayAudibleNoise(...)` at the Pikmin's own transform when audible-noise generation is enabled. Singing uses the same mechanism.

The accepted configuration has:

`Dont Make Audible Noises = false`

A Pikmin itself is therefore a proved possible Mouth Dog noise source in the current stack.

### Carried scrap / GoldBar hypothesis

The S1.42AG runtime evidence proves Purple Pikmin carried `GoldBar(Clone)` during the relevant run.

What is **not** yet proved is whether that carried GoldBar itself emitted the audible-noise event that caused the observed pursuit. Current evidence neither establishes nor excludes that narrower causality.

Do not state that Vanilla `MouthDogAI` selected the Purple Pikmin because it carried scrap. The proved native model is world-position perception plus generic `EnemyAI` collision.

## Remaining Mouth Dog proof before any successor

Two targeted source contracts remain mandatory:

1. inspect exact Vanilla V81 `EnemyAI.OnCollideWithEnemy()` base behavior and side effects, because the MouthDog override calls it first; a prefix that blindly returns `false` could incorrectly skip base responsibilities;
2. inspect exact LethalMin 1.1.108 `PikminItem.CarryNumerator()` plus carry-item audio / `RoundManager.PlayAudibleNoise(...)` callsites to prove or reject carried-GoldBar noise causality.

Only after those contracts are proved may a successor-specific safety review determine the narrow patch boundary.

Current rules:

- S1.42AF remains the accepted gameplay base.
- S1.42AG must not be used as a gameplay base.
- `MouthDogPikminEnemy` stays enabled unless exact evidence later proves a different safe ownership boundary.
- Preserve the proven S1.42AG prevention-before-mutation concept where it remains part of the final solution.
- Do not add broad EnemyAI scans, guessed Harmony targets, whole-component disables or manual Pikmin state reconstruction.
- Preserve Mouth Dog -> player behavior.
- Preserve native Pikmin -> Mouth Dog combat/latch/death/unlatch/task lifecycle.
- Do not build/arm a successor or start another gameplay test before the two remaining source contracts and safety review are complete.

Reverse-direction Pikmin -> Mouth Dog combat was not deliberately tested in S1.42AG. Passive follower non-aggression is expected normal behavior and is not a failure signal. A future successor runtime gate must deliberately command/throw Pikmin onto the Mouth Dog and validate attack/latch/death-unlatch behavior.

## CodeRebirth utility kills

The cumulative compatibility plugin also shields Pikmin/Puffmin from CodeRebirth utility kill RPCs, providing a direct failsafe for gaps such as Autonomous Crane kills even when corresponding LethalMin toggles are already false.

## Diagnostic EnemyIsolation

EnemyIsolation was temporary test infrastructure only and defaults off. Do not treat the old isolated allowlist as normal gameplay state and do not restore continuous global EnemyAI scanning.

## Patch safety

Any future change to these interactions is high risk and must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`:

- inspect exact owner/method/inheritance/lifecycle first;
- prefer prevention before state mutation;
- isolate risky patch deltas;
- test target behavior, adjacent lifecycle, reverse direction, repetition and neighboring behavior;
- compile/startup success alone is not acceptance.
