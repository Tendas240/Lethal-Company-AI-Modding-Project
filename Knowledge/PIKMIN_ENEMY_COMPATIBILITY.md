# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/128_S1.42AF_RUNTIME_GATE_PASS_ACCEPTANCE_DEFERRED_MOUTH_DOG_BASELINE_GAP.md`, `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md`  
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

## Mouth Dog / Eyeless Dog — open baseline gap

The S1.42AF normal runtime run exposed a previously unhandled Mouth Dog / Eyeless Dog -> Pikmin bite/grab interaction. The user directly observed the interaction and the same run later contained a large `Work state with no task assigned!` burst.

This is currently classified as a **baseline compatibility gap**, not an S1.42AF Microwave regression:

- S1.42AF's isolated archive delta changed only `export.r2x` and added the Microwave tuning DLL;
- the cumulative compatibility DLL is byte-identical in accepted S1.42AC and S1.42AF: SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- current `LethalMinEnemyGrabPrevention` source blocks Crawler/Thumper and Baboon Hawk snap-position families, but contains no Mouth-Dog branch.

Desired asymmetric contract is fixed:

- Mouth Dog / Eyeless Dog -> Pikmin bite/grab: **must not begin at all**;
- Pikmin -> Mouth Dog attack: **allowed/native**;
- native LethalMin enemy death/unlatch/task lifecycle: **preserved**.

The exact implementation owner is **not yet proven**. The next analysis must inspect LethalMin `1.1.108` config first, then exact adapter/collision/bite/grab methods if configuration cannot express the contract. A common `PikminAI.GrabPikmin(Transform,float,int)` snap-position guard is only acceptable if source/runtime analysis proves the dog uses that exact path and can be classified unambiguously. If a separate Mouth-Dog adapter bite/collision entry point exists, a narrow prevention prefix may also be required.

Do not disable an entire adapter, add delayed follower-state repair, or install a guessed reflection fallback. Authority: `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md`.

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
