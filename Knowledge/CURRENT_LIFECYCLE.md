<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
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

**S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**

- Parent: exact accepted S1.42AF, not rejected S1.42AG.
- Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
- Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- Candidate authority: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`
- Build workflow run: `34141360051`
- Exact archive delta: `export.r2x` plus `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll` only.

Runtime test outstanding: **yes**.

## Patch contract already implemented

S1.42AH implements `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`:

- retain the exact `Priority.First` prevention prefix on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`;
- add the exact `Priority.First` prefix on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)`;
- skip the Vanilla override only for a validated runtime `LethalMin.PikminAI` collision;
- do not patch `DetectNoise`, `OnCollideWithPlayer`, base `EnemyAI.OnCollideWithEnemy`, or native Pikmin attack/task/latch lifecycle.

## Current controllers

- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`.
- Guarded artifact: S1.42AH / `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`.
- No successor beyond S1.42AH is armed.

## Exact next project action

Import and runtime-test S1.42AH using `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`.

The test must deliberately cover:

- MouthDog -> Pikmin adapter protection;
- MouthDog -> Pikmin Vanilla collision protection;
- Pikmin -> MouthDog attack/latch/death/unlatch/task cleanup by explicit command/throw;
- MouthDog -> player behavior;
- non-Pikmin neighboring `EnemyAI` behavior;
- repeated protected collision opportunities;
- complete fresh `LogOutput.log` evidence.

Passive follower non-aggression is not a reverse-direction test. Position-based movement/lunge toward audible Pikmin world position is not by itself failure. Do not accept S1.42AH from build/startup success alone.

## Currently irrelevant actions

- Do not repeat the completed MouthDog/EnemyAI source captures merely to reproduce integrated evidence.
- Do not repeat the S1.42AG gameplay run or request another S1.42AG log upload.
- Do not repeat the Patch Safety Review unless new source/target evidence invalidates its contract.
- Do not rebuild S1.42AH or arm a successor beyond it before the S1.42AH runtime decision.

## Canonical Gale workflow

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` as governed by `Knowledge/GALE_PROFILE_WORKFLOW.md`. When handing off the runtime test, include both the Gale replacement/import one-liner and the exact S1.42AH build-specific uploader in the same response.
