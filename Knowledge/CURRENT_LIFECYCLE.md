# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
**Related:** `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Last-Validated:** 2026-09-07

## Accepted baseline

**S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Injected DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`
- Runtime log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`

S1.42AF remains the only accepted gameplay base.

## Latest built artifact

**S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**

- Parent: accepted S1.42AF, not rejected S1.42AG.
- Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
- SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`
- Build workflow run: `34141360051`
- Build commit: `__BUILD_COMMIT__`
- Exact archive delta: `export.r2x` + compatibility DLL only; every unrelated member byte-identical to S1.42AF.

S1.42AF remains the only accepted gameplay base until S1.42AH passes runtime validation.

## MouthDog successor Patch Safety Review

`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md` is implemented by S1.42AH. The candidate retains exact `DoCheckInterval()` prevention and adds the exact Pikmin-only Vanilla `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` prevention. `DetectNoise`, MouthDog -> player, non-Pikmin EnemyAI collisions and native Pikmin lifecycle remain outside the patch.

## Current controllers

- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`.
- Guarded candidate: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z` / `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`.
- Runtime test outstanding: **yes**.
- No successor beyond S1.42AH is armed.

## Exact next project action

Import and runtime-test S1.42AH using `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`. Deliberately exercise both protected MouthDog -> Pikmin paths, explicitly command/throw Pikmin for the reverse-direction latch/attack/death/unlatch/task test, preserve MouthDog -> player/non-Pikmin/noise behavior, repeat the collision gate, and upload the complete fresh log using the build-specific uploader in the candidate record.

Do not accept S1.42AH from build/startup success alone.

## Future runtime acceptance

A future candidate must deliberately cover:

- MouthDog -> Pikmin adapter protection;
- MouthDog -> Pikmin Vanilla collision protection;
- Pikmin -> MouthDog attack/latch/death/unlatch/task lifecycle;
- MouthDog -> player;
- repetition;
- non-Pikmin neighbor behavior;
- logs.

Passive follower non-aggression is not a reverse-direction test. Position-based noise pursuit is not itself a failure.

## Currently irrelevant actions

- Do not repeat the successful MouthDog or EnemyAI source captures.
- Do not ask for `Assembly-CSharp.dll`, `-AssemblyPath`, a local clone or manual ILSpy setup for these closed proofs.
- Do not repeat the S1.42AG run or log upload.
- Do not repeat the safety review unless new evidence invalidates its exact contract.
- Do not start a runtime test before a later candidate is built.

## Canonical Gale workflow

The current repository-driven Gale replacement/import workflow remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`, as governed by `Knowledge/GALE_PROFILE_WORKFLOW.md`.

No runtime test is currently pending. Any future candidate requiring Gale replacement must continue to use this canonical v2.4 path unless a later validated workflow authority explicitly supersedes it. When a future candidate is ready, the same response that explains the test must include the Gale replacement/import one-liner when required and the exact build-specific self-contained PowerShell log uploader.
