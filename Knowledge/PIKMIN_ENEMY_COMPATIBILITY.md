# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `RuntimeEvidence/S1.42AF/20260905T223738Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
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

## Mouth Dog / Eyeless Dog — S1.42AH active candidate

S1.42AF remains accepted. S1.42AG remains rejected partial-fix evidence. **S1.42AH is now the built active runtime candidate and is not accepted.**

S1.42AH implements the exact reviewed dual prevention architecture from `Current/138`: retain `Priority.First` prevention on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` and add `Priority.First` prevention on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` only when the supplied object is validated runtime `LethalMin.PikminAI`.

The complete target/signature/method-body/inheritance contract fails closed with no guessed fallback. The adapter stays enabled. `DetectNoise`, MouthDog -> player, non-Pikmin EnemyAI collision behavior and native Pikmin attack/latch/death/unlatch/task ownership remain unchanged.

Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`  
Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`

The archive was built directly from S1.42AF. Only `export.r2x` and the cumulative compatibility DLL differ; all unrelated members are byte-identical.

Runtime acceptance must deliberately prove the protected collision marker, absence of adapter/grab/HitEnemy mutation, explicit reverse-direction Pikmin command/throw latch/attack/death cleanup, MouthDog -> player, non-Pikmin neighbor behavior, repetition and clean logs. Noise-position pursuit alone is not failure evidence.

## Current lifecycle

- accepted: S1.42AF;
- latest built: S1.42AH, build pass / active candidate / not accepted;
- active candidate: S1.42AH;
- runtime test pending: yes;
- successor beyond S1.42AH: not armed.

## CodeRebirth utility kills

The cumulative compatibility plugin also shields Pikmin/Puffmin from CodeRebirth utility kill RPCs, providing a direct failsafe for established utility-kill gaps.

## Diagnostic EnemyIsolation

EnemyIsolation was temporary test infrastructure only and defaults off. Do not restore continuous global EnemyAI scanning as normal gameplay behavior.

## Patch safety

Any future custom compatibility patch must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`. Compilation, main-menu load or disappearance of the directly targeted symptom is not sufficient for promotion.
