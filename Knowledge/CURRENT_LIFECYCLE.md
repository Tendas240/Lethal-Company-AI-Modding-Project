# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
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

**S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**

- Profile: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`
- SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`
- Compatibility DLL SHA-256: `976264a31b85bf3d913d3ad703fa770a666957664d0de5b848a5073b0883d064`
- Rejection: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`
- Runtime evidence: `RuntimeEvidence/S1.42AG/20260906T085500Z/`
- Runtime log SHA-256: `3e8ca4c8fe045bbd2c62576dbbd5aaba2a226990e6b4af4149481f2672c35dfe`

S1.42AG remains rejected. Its `DoCheckInterval()` guard is retained as proven partial-fix evidence, not as a gameplay base.

## MouthDog successor Patch Safety Review

Current review authority:

`Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`

Status:

**PASS FOR IMPLEMENTATION / SUCCESSOR NOT ARMED / NO BUILD YET**

The reviewed minimum safe architecture is:

1. retain exact `Priority.First` prevention on `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`;
2. add exact `Priority.First` prevention on declared Vanilla `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` only when the actual `collidedEnemy` is a validated `LethalMin.PikminAI`.

Do not patch the position-only `DetectNoise()` path. A MouthDog may legitimately move toward an audible Pikmin world position without semantically selecting a Pikmin target.

Preserve unchanged:

- MouthDog -> player;
- MouthDog -> non-Pikmin EnemyAI;
- native Pikmin -> MouthDog attack/latch/death/unlatch/task lifecycle;
- enabled `MouthDogPikminEnemy` / `PikminEnemy` lifecycle;
- all unrelated S1.42AF packages/config.

## Current controllers

- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_MOUTHDOG_PATCH_SAFETY_REVIEW_AWAITING_SUCCESSOR_IMPLEMENTATION`.
- Guarded base remains accepted `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains runtime-evidence attribution only.
- No successor is armed.
- No runtime test is pending.

## Exact next project action

In the next explicit project segment, implement the reviewed dual prevention-only MouthDog successor in `Patches/S139CompatibilityFixes/Plugin.cs` and prepare/arm its build repository-native from exact accepted S1.42AF.

Before building, validate exact target types/signatures/method bodies, validate `LethalMin.PikminAI : EnemyAI`, install no guessed fallback, and keep package/config state unchanged. The eventual candidate must record DLL/profile SHA-256 and archive-diff diagnostics.

Do not start runtime testing until a successful candidate artifact exists.

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
