# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`, `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `RuntimeEvidence/S1.42AF/20260905T223738Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`, `RuntimeEvidence/S1.42AH/20260908T162411Z/`  
**Code:** `Patches/S139CompatibilityFixes/Plugin.cs`  
**Related:** `Knowledge/ENEMY_SPAWN_BASELINE.md`, `Knowledge/CURRENT_LIFECYCLE.md`  
**Last-Validated:** 2026-09-08

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

S1.42AF remains accepted. S1.42AG remains rejected partial-fix evidence. **S1.42AH is the built active runtime candidate; its first run is a positive partial pass, but S1.42AH is still neither accepted nor rejected.**

S1.42AH implements the exact reviewed dual prevention architecture from `Current/138`: retain `Priority.First` prevention on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` and add `Priority.First` prevention on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` only when the supplied object is validated runtime `LethalMin.PikminAI`.

The complete target/signature/method-body/inheritance contract fails closed with no guessed fallback. The adapter stays enabled. `DetectNoise`, MouthDog -> player, non-Pikmin EnemyAI collision behavior and native Pikmin attack/latch/death/unlatch/task ownership remain outside the new patch boundary.

Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`  
Partial runtime decision: `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`  
Runtime evidence: `RuntimeEvidence/S1.42AH/20260908T162411Z/`  
Runtime log SHA-256: `1778ad5b572349cda261b3b848e0a697dfdb527a1e4be4ab72624a88f9c51ef3`  
Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`

The archive was built directly from S1.42AF. Only `export.r2x` and the cumulative compatibility DLL differ; all unrelated members are byte-identical.

### First runtime run — positively evidenced

The first ingested S1.42AH run establishes:

- adapter-side `EatPikmin` and `HandleEnemyBite` patch installation;
- installation of the project-local Vanilla `MouthDogAI.OnCollideWithEnemy` prefix;
- repeated real Vanilla MouthDog -> Pikmin collision-block markers during gameplay;
- exercised MouthDog -> player behavior remains functional, including a real player death with cause `Mauling`.

This is enough to close those exercised portions of the original gate, but not enough to promote the build.

### Targeted remainder before any acceptance/rejection decision

The remaining runtime validation must deliberately prove:

1. Explicit command/throw Pikmin -> MouthDog latch/attack/damage remains native and functional.
2. MouthDog death through the Pikmin attack path releases/unlatches Pikmin and completes the attack-task/follow-idle cleanup correctly.
3. The adapter-side bite-protection path itself prevents Paw/Pikmin bite/grab/death-timer mutation when exercised; installation alone is insufficient.
4. Paw-initiated `BiteKillEnemyAI` behavior remains functional.
5. Non-Pikmin neighboring `EnemyAI` behavior, combat/UI membership invariants and known regression markers remain sound around the targeted reverse-direction/death-cleanup sequence.
6. Ordinary audible-noise response remains available; position-based pursuit toward a Pikmin world position alone is not failure evidence.

The first run's `Enemy Not Hit By Pikmin. Reason: [Invalid Enemy States]` / `Not hitting MouthDog` messages neither satisfy the required reverse-direction test nor independently prove a candidate regression because the explicit attack conditions required by the gate were not established.

Do not rebuild S1.42AH and do not repeat already-proven startup/Vanilla-collision/player-maul coverage merely to obtain this missing evidence.

## Current lifecycle

- accepted: S1.42AF;
- latest built: S1.42AH, build pass / partial runtime pass / targeted remainder outstanding / not accepted;
- active candidate: S1.42AH;
- runtime test pending: yes;
- successor beyond S1.42AH: not armed.

## CodeRebirth utility kills

The cumulative compatibility plugin also shields Pikmin/Puffmin from CodeRebirth utility kill RPCs, providing a direct failsafe for established utility-kill gaps.

## Diagnostic EnemyIsolation

EnemyIsolation was temporary test infrastructure only and defaults off. Do not restore continuous global EnemyAI scanning as normal gameplay behavior.

## Patch safety

Any future custom compatibility patch must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`. Compilation, main-menu load or disappearance of the directly targeted symptom is not sufficient for promotion.
