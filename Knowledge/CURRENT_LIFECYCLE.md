<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`, `RuntimeEvidence/S1.42AH/20260908T162411Z/`  
**Related:** `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-08

## Accepted baseline

**S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`

S1.42AF remains the only accepted gameplay base.

## Latest built artifact / active candidate

**S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / PARTIAL RUNTIME PASS / TARGETED REMAINDER OUTSTANDING / NOT ACCEPTED**

- Parent: exact accepted S1.42AF, not rejected S1.42AG.
- Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
- Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- Candidate authority: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`
- Partial runtime decision: `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`
- Runtime evidence: `RuntimeEvidence/S1.42AH/20260908T162411Z/`
- Runtime log SHA-256: `1778ad5b572349cda261b3b848e0a697dfdb527a1e4be4ab72624a88f9c51ef3`
- Build workflow run: `34141360051`
- Exact archive delta: `export.r2x` plus `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll` only.

Runtime test outstanding: **yes**. S1.42AH is **neither accepted nor rejected**.

## Patch contract already implemented

S1.42AH implements `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`:

- retain the exact `Priority.First` prevention prefix on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`;
- add the exact `Priority.First` prefix on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)`;
- skip the Vanilla override only for a validated runtime `LethalMin.PikminAI` collision;
- do not patch `DetectNoise`, `OnCollideWithPlayer`, base `EnemyAI.OnCollideWithEnemy`, or native Pikmin attack/task/latch lifecycle.

## First S1.42AH runtime run — proven

The ingested first run closes several parts of the original runtime gate:

- adapter-side `EatPikmin` / `HandleEnemyBite` patch-installation markers appear;
- the project-local Vanilla `MouthDogAI.OnCollideWithEnemy` prefix installs;
- live Vanilla MouthDog -> Pikmin collision handling is repeatedly blocked by `MouthDogVanillaCollisionGuard`;
- MouthDog -> player behavior remains functional in the exercised interval, including a real player death with cause `Mauling`.

These observations are recorded in `Current/140`. They are positive partial-runtime evidence, not a promotion decision.

## Remaining S1.42AH runtime gate

Run only the targeted remainder:

1. Explicitly command/throw Pikmin onto a MouthDog and prove native Pikmin -> MouthDog latch/attack/damage.
2. Prove MouthDog death through the Pikmin attack path plus death-triggered unlatch/release, attack-task finish and follow/idle cleanup.
3. Exercise the adapter-side MouthDog bite-protection path itself and prove Paw/Pikmin bite/grab/death-timer mutation is prevented.
4. Preserve Paw-initiated `BiteKillEnemyAI` behavior.
5. Re-check non-Pikmin neighboring `EnemyAI` behavior, combat/UI membership invariants and known regression markers around the targeted reverse-direction/death-cleanup sequence.
6. Preserve ordinary audible-noise response; position-based pursuit toward a Pikmin world position alone is not failure evidence.

Passive follower non-aggression is not a reverse-direction test. The first run's `Invalid Enemy States` / `Not hitting MouthDog` messages neither satisfy this gate nor by themselves prove a candidate defect because the required explicit reverse-direction attack conditions were not established.

## Current controllers

- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`.
- Guarded artifact: S1.42AH / `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`.
- No successor beyond S1.42AH is armed.

## Exact next project action

Run the targeted remainder documented in `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`. Do not rebuild S1.42AH and do not repeat already-proven startup/patch-install, Vanilla MouthDog -> Pikmin collision-block, or player-maul coverage merely to obtain the missing reverse-direction evidence.

If every remaining required check passes, record an explicit S1.42AH acceptance. If a targeted required check fails, record an explicit S1.42AH rejection and return to an S1.42AF-derived follow-up.

## Currently irrelevant actions

- Do not repeat the completed MouthDog/EnemyAI source captures merely to reproduce integrated evidence.
- Do not repeat the S1.42AG gameplay run or request another S1.42AG log upload.
- Do not repeat the Patch Safety Review unless new source/target evidence invalidates its contract.
- Do not rebuild S1.42AH or arm a successor beyond it before the S1.42AH runtime decision.
- Do not repeat already-proven S1.42AH collision/player coverage solely because the remaining reverse-direction gate is still open.

## Canonical Gale workflow

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`, as governed by `Knowledge/GALE_PROFILE_WORKFLOW.md`. When handing off the remaining runtime test, include both the Gale replacement/import one-liner and the exact S1.42AH build-specific uploader in the same response.
