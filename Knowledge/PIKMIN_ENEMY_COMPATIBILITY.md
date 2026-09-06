# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`, `Current/132_MOUTHDOG_PATCH_SAFETY_REVIEW.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `RuntimeEvidence/S1.42AF/20260905T223738Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
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

## Mouth Dog / Eyeless Dog — S1.42AG runtime-rejected partial fix

The S1.42AF acceptance run exposed the inherited Mouth Dog -> Pikmin gap recorded in `Current/129`. Exact LethalMin 1.1.108 decompile evidence in `Current/130` proved `MouthDogPikminEnemy.DoCheckInterval()` is an adapter-specific target/bite dispatcher and that `BiteNearbyPikmin` mutates `GrabbedPikmin` before calling `PikminAI.GrabPikmin(mouthGrip, 2.5f, 5)`. S1.42AG therefore added a fail-closed `Priority.First` prefix on exact declared `DoCheckInterval()` while keeping the adapter enabled.

Runtime evidence now proves that this narrow guard **does work for the LethalMin bite/grab/death-timer mutation path**:

- the guard armed and executed during the encounter;
- no Mouth Dog `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab-death-timer signature was observed;
- `Work state with no task assigned!` fell from 707 in the S1.42AF exposure run to 0 in S1.42AG;
- no compatibility-fix error or fatal marker was introduced.

But S1.42AG is **runtime rejected** because the full asymmetric interaction contract was not achieved. The user directly observed a Mouth Dog visibly target and attack a scrap-carrying Purple Pikmin even though the Pikmin was not harmed by the blocked LethalMin mutation path. The encounter also contains repeated native Mouth Dog noise-targeting diagnostics. These are evidence of a remaining behavior outside the proven `DoCheckInterval()` mutation boundary, but they are not yet sufficient to identify the exact root owner/method.

The same run did not positively prove the intended Pikmin -> Mouth Dog attack/latch path either. Do not infer that reverse-direction behavior is broken merely from a non-event, but treat it as an open validation question for the targeted analysis.

Current rule:

- **S1.42AF remains the accepted gameplay base.**
- **S1.42AG must not be used as a gameplay base.**
- Preserve the proven S1.42AG prevention concept as evidence: blocking `DoCheckInterval()` before LethalMin bite/grab mutation is useful and effective.
- Do not accept that guard as the complete solution because a separate Mouth Dog target/attack path remains unresolved.
- Do not disable `MouthDogPikminEnemy`; native reverse-direction lifecycle ownership must remain intact unless exact source evidence proves a different boundary is required.
- Do not add guessed fallbacks or broad EnemyAI scanning.
- Before any successor build, identify the exact current owner/method/path for the remaining target/attack behavior, including whether a carried scrap object's noise/threat behavior is the trigger.

Rejection authority: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`.

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
