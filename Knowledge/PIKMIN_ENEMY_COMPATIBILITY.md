# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `RuntimeEvidence/S1.42AH/20260909T162513Z/`  
**Code:** `Patches/S139CompatibilityFixes/Plugin.cs`  
**Last-Validated:** 2026-09-09

## Ownership principle

Native LethalMin owns normal Pikmin -> enemy combat, enemy death handling, latch removal, task completion, dead-body carry and Onion delivery. Project-local code blocks only proven Enemy -> Pikmin gaps and must preserve that native lifecycle. Prefer prevention before mutation.

## Accepted neighboring contracts

- Baboon Hawk -> Pikmin bite/grab is blocked narrowly while native reverse-direction lifecycle remains enabled.
- Thumper/Crawler retain their accepted compatibility behavior; Thumper Bite Limit remains 3 and Crawler remains available for Pikmin counterattack.
- Puffer protection remains targeted rather than a broad enemy disable.

## Mouth Dog / Eyeless Dog — S1.42AH accepted

**S1.42AH — Mouth Dog Pikmin Dual Prevention is ACCEPTED FULL NORMAL STACK.**

Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Final decisive runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`  
Final raw-log SHA-256: `ae57fb71a38952936e9056150240e2eaa70be9d89253b15644b3f5d35dd09729`

S1.42AF is the accepted predecessor/rollback point. S1.42AG remains rejected historical partial-fix evidence.

### Accepted patch boundary

S1.42AH retains `Priority.First` prevention on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` and adds `Priority.First` prevention on exact `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` only when the supplied object is validated runtime `LethalMin.PikminAI`.

The collision prefix contract is exact:

- `collidedEnemy == null` -> pass through;
- unresolved Pikmin type -> pass through/fail-safe rather than broad blocking;
- non-`LethalMin.PikminAI` `EnemyAI` -> pass through;
- validated `LethalMin.PikminAI` -> skip only the Dog override before its generic enemy lunge/cooldown/`HitEnemy(2)` mutation.

The adapter stays enabled. Do **not** patch or suppress:

- `MouthDogAI.DetectNoise(...)`;
- `MouthDogAI.OnCollideWithPlayer(...)`;
- base `EnemyAI.OnCollideWithEnemy(...)`;
- `LethalMin.PikminEnemy` lifecycle;
- native Pikmin attack/task/latch/death/carry lifecycle.

### Accepted runtime coverage

Across the targeted S1.42AH evidence:

1. both intended patch boundaries install;
2. repeated live Vanilla MouthDog -> Pikmin collision blocks occur;
3. MouthDog -> player behavior remains functional, including mauling/death coverage;
4. explicitly thrown Pikmin latch onto MouthDog, enter `AttackEnemy`, and repeatedly damage it;
5. Pikmin combat kills MouthDog;
6. native death cleanup sets attackers idle, removes attack task/leader and unlatches them;
7. dead MouthDog body becomes a Pikmin item and native corpse carrying begins;
8. adapter prevention executes before bite/grab mutation;
9. ordinary MouthDog audible-noise response remains present;
10. known project-local regression markers remain clean in the focused evidence;
11. the final deliberate non-Pikmin neighbor run includes MouthDogs and a Redwood Titan, followed by normal Redwood Titan death while the collision guard remains Pikmin-only.

The user directed the final decision to use only the last gameplay run of the final uploaded log. The user reported that a Mouth Dog appeared to kill the Redwood Titan; the log independently proves the relevant entities were present and the Redwood Titan reached the normal enemy-death path. The death line does not encode attacker identity, so do not misrepresent it as a per-hit attacker log.

### Exact native neighbor semantics

Exact Vanilla V81 source authority proves `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` calls:

`collidedEnemy.HitEnemy(2, null, playHitSFX: true)`

for the eligible non-same-type collision path, with lunge behavior when its state permits.

Earlier current-state text used `BiteKillEnemyAI` as shorthand for the final neighbor check. That is not the exact method name exposed by the focused V81 source evidence. Future reasoning should use the exact **`OnCollideWithEnemy` -> `HitEnemy(2)`** contract.

## Permanent MouthDog anti-regression rules

- Never restore S1.42AG as a gameplay base.
- Never disable the whole LethalMin MouthDog adapter merely to block MouthDog -> Pikmin behavior.
- Never broaden the S1.42AH collision prefix from runtime `LethalMin.PikminAI` to arbitrary `EnemyAI`.
- Preserve MouthDog -> player behavior and non-Pikmin `EnemyAI` pass-through.
- Preserve native Pikmin -> MouthDog combat/death/unlatch/task/carry ownership.
- A future change to either exact MouthDog hook requires a new patch-safety review and targeted regression evidence.

## Current lifecycle

- accepted baseline: **S1.42AH**;
- latest built artifact: **S1.42AH**;
- active candidate: none;
- runtime test pending: no;
- next independent scope: BCMER ShyGuy interior-only correction under `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`.

## Patch safety

Any future custom compatibility patch must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`. Compilation, main-menu load or disappearance of the directly targeted symptom is not sufficient for promotion.