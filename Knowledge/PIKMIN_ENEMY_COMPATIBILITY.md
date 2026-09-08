# Pikmin / Enemy Compatibility

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interaction ownership and permanent anti-regression rules  
**Canonical-For:** `pikmin_enemy_compatibility`  
**Evidence:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`, `RuntimeEvidence/S1.42AH/20260908T162411Z/`, `RuntimeEvidence/S1.42AH/20260908T174352Z/`  
**Code:** `Patches/S139CompatibilityFixes/Plugin.cs`  
**Last-Validated:** 2026-09-08

## Ownership principle

Native LethalMin owns normal Pikmin -> enemy combat, enemy death handling, latch removal, task completion, dead-body carry and Onion delivery. Project-local code blocks only proven Enemy -> Pikmin gaps and must preserve that native lifecycle. Prefer prevention before mutation.

## Accepted neighboring contracts

- Baboon Hawk -> Pikmin bite/grab is blocked narrowly while native reverse-direction lifecycle remains enabled.
- Thumper/Crawler retain their accepted compatibility behavior; Thumper Bite Limit remains 3 and Crawler remains available for Pikmin counterattack.
- Puffer protection remains targeted rather than a broad enemy disable.

## Mouth Dog / Eyeless Dog — S1.42AH active candidate

S1.42AF remains accepted. S1.42AG remains rejected partial-fix evidence. **S1.42AH is the built active runtime candidate; two ingested runs now form an extended positive partial pass, but S1.42AH is still neither accepted nor rejected.**

S1.42AH retains `Priority.First` prevention on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` and adds `Priority.First` prevention on exact `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` only when the supplied object is validated runtime `LethalMin.PikminAI`. The adapter stays enabled. `DetectNoise`, MouthDog -> player, non-Pikmin EnemyAI collisions and native Pikmin attack/latch/death/unlatch/task ownership remain outside the new patch boundary.

Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`  
Latest partial runtime decision: `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`  
Latest runtime evidence: `RuntimeEvidence/S1.42AH/20260908T174352Z/`  
Latest runtime log SHA-256: `6fca32623eb350c53b4f81c98ea3ef1218dee9a4256a4bb70a8950f1b3ab06a6`  
Prior partial decision/evidence: `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md` / `RuntimeEvidence/S1.42AH/20260908T162411Z/`  
Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`

### Runtime coverage now proven

Across the first and second S1.42AH runs:

- both intended patch boundaries install;
- repeated real Vanilla MouthDog -> Pikmin collision blocks occur;
- MouthDog -> player behavior remains functional;
- explicitly thrown Pikmin latch onto the MouthDog, enter `AttackEnemy`, and damage it;
- Pikmin combat kills the MouthDog;
- native death cleanup sets attackers idle, removes their attack task/leader and unlatches them;
- the dead MouthDog transitions into Pikmin corpse carrying;
- the adapter prevention executes live before bite/grab mutation with no known harmful adapter mutation signature in the targeted interval;
- ordinary MouthDog noise response remains available;
- known project-local regression markers remain clean.

### Final targeted remainder

Only one adjacent contract still needs deliberate proof: **MouthDog/Paw -> non-Pikmin `EnemyAI` pass-through**. Deliberately exercise that interaction and prove native Paw-initiated `BiteKillEnemyAI` / generic non-Pikmin collision behavior remains functional and is not filtered by the Pikmin-only prefix.

Do not repeat the already-proven Pikmin -> MouthDog attack/death/unlatch/task-cleanup or adapter-protection sequence solely to obtain that final neighboring evidence.

## Current lifecycle

- accepted: S1.42AF;
- latest built/active candidate: S1.42AH, extended partial runtime pass, final non-Pikmin neighbor remainder outstanding, not accepted;
- runtime test pending: yes;
- successor beyond S1.42AH: not armed.

## Patch safety

Any future custom compatibility patch must follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`. Compilation, main-menu load or disappearance of the directly targeted symptom is not sufficient for promotion.