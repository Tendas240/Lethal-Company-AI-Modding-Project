# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `RuntimeEvidence/S1.42AF/20260905T223738Z/`  
**Code:** `Patches/S139CompatibilityFixes/Plugin.cs`  
**Related:** `Knowledge/ENEMY_SPAWN_BASELINE.md`  
**Last-Validated:** 2026-09-06

## Ownership principle

Native LethalMin owns normal Pikmin -> enemy combat, enemy death handling, latch removal, task completion, dead-body carry and Onion delivery. Project-local code blocks only proven Enemy -> Pikmin gaps and must preserve that native lifecycle.

Never repeat the S1.42R whole-component disable of `LethalMin.BaboonBirdPikminEnemy`. Disabling that component also suppressed inherited `PikminEnemy.Update()` death/unlatch cleanup.

## Baboon Hawk

Accepted asymmetric rule:

- Baboon Hawk -> Pikmin collision/bite/grab: blocked narrowly;
- Pikmin -> Baboon Hawk attack: allowed/native;
- `BaboonBirdPikminEnemy`: stays **enabled**;
- native death/unlatch lifecycle: preserved.

The compatibility source validates exact declared Hawk adapter entry points and uses the common `PikminAI.GrabPikmin(Transform,float,int)` prevention-only guard rather than manual follower-state reconstruction.

## Thumper / Crawler

The proven Enemy -> Pikmin broken grab path is blocked before it can mutate leader/grab/death-timer state.

Current accepted LethalMin configuration:

- `Thumper Bite Limit = 3`;
- `Crawler` is **not** in the Pikmin Attack Blacklist.

Do not revert to complete two-way noninteraction. Pikmin counterattack remains intended.

## Puffer / Spore Lizard

Puffer -> Pikmin smoke/effect interaction is protected by removing the LethalMin-injected Pikmin effect-trigger components from Puffer smoke. This is targeted protection, not a broad enemy disable.

## Mouth Dog / Eyeless Dog — current open gap

The accepted S1.42AF runtime run exposed a separate inherited Mouth Dog -> Pikmin compatibility gap. LethalMin logged `Biting 2 Pikmin`, both White Pikmin attaching to `EnemyAttackMouth`, and 2.5-second death timers. Pikmin invincibility prevented the final enemy-attack kill, but the grab/death-timer mutation had already happened and the two affected Pikmin subsequently generated 707 `Work state with no task assigned!` warnings.

The binding target is asymmetric:

- Mouth Dog / Eyeless Dog -> Pikmin targeting/bite/grab/kill: **must be blocked before Pikmin grab/death-timer state mutation**;
- Pikmin -> Mouth Dog attack: preserve native LethalMin behavior unless exact source evidence proves another requirement;
- relying on `Invinceable Pikmin = true` after the grab is insufficient;
- do not introduce delayed state repair or broad component disable without proving that no narrower prevention boundary exists.

`Patches/S139CompatibilityFixes/Plugin.cs` already patches exact declared `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` with a `Priority.First` prevention-only prefix for proven Crawler/Thumper and Baboon Hawk snap-position paths. It currently does not identify MouthDog/EyelessDog. That makes the existing prevention point a candidate for investigation, **not yet an authorized fix**.

Next work must first inspect the exact LethalMin MouthDog/EyelessDog owner, targeting/bite method, inheritance, native configuration surface and whether the harmful path reaches `GrabPikmin` before all mutation. See `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`. No successor is armed until that contract is proved.

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
