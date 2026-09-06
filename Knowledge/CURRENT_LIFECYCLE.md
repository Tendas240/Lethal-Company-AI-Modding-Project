# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
**Related:** `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Last-Validated:** 2026-09-06

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
- Candidate: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`
- Rejection: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`
- Runtime evidence: `RuntimeEvidence/S1.42AG/20260906T085500Z/`
- Runtime log SHA-256: `3e8ca4c8fe045bbd2c62576dbbd5aaba2a226990e6b4af4149481f2672c35dfe`

S1.42AG's exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` prevention guard armed and executed. It removed the prior LethalMin-specific bite/grab/death-timer signature and reduced `Work state with no task assigned!` from 707 in the exposure baseline to 0. It remains rejected because a Mouth Dog still visually pursued/attacked a scrap-carrying Purple Pikmin through a different path.

Reverse-direction Pikmin -> Mouth Dog combat was not deliberately tested and has no pass/fail result.

## Closed MouthDog source boundaries

The previously required pre-successor source extension is complete. Current analysis authority is `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`.

### Vanilla V81 MouthDog source

The provenance-safe MouthDog capture proves:

- `MouthDogAI.DetectNoise(...)` consumes a world-space position;
- `noisePositionGuess` drives native pursuit and can lead to `EnterLunge()`;
- `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` is an independent generic enemy-collision surface which can lunge and call `collidedEnemy.HitEnemy(2, ...)`;
- exact LethalMin source proves `PikminAI : EnemyAI`.

### Vanilla V81 EnemyAI base collision

The targeted `EnemyAI.OnCollideWithEnemy()` capture is complete and integrated under `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`.

Exact V81 behavior is debug-only: the method optionally emits a server debug log and performs no gameplay, navigation, targeting, damage, grab, cleanup or lifecycle mutation. This closes the previous concern that an exact future MouthDog collision Prefix might suppress hidden base gameplay responsibilities.

### LethalMin 1.1.108 carry/noise contract

Existing exact source evidence proves `PikminItem.CarryNumerator()` repeatedly calls `pikmin.PlayAudioOnLocalClient("ItemCarry", ...)` for each carrier. `PikminAI.PlayAudioOnLocalClient(...)` can call `RoundManager.PlayAudibleNoise(...)` at the Pikmin transform when audible-noise suppression is disabled, and the accepted config has `Dont Make Audible Noises = false`.

Therefore item carrying is source-proven to generate recurring audible noise through the carrying Pikmin at the carrier's world position. The stronger claim that Vanilla MouthDogAI semantically targets Purple Pikmin because they carry scrap, or that the GoldBar itself is the proved recurring carry-noise emitter, is unsupported/rejected. Exact runtime causality for the observed S1.42AG chase is still not proven.

No additional local source capture is currently required.

## Current controllers

- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_MOUTHDOG_SOURCE_BOUNDARIES_AWAITING_PATCH_SAFETY_REVIEW`.
- Guarded base remains accepted `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains runtime-evidence attribution only.
- No successor is armed.
- No runtime test is pending.

## Exact next project action

Perform the **successor-specific Patch Safety Review** under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

Before any successor is armed, the review must define:

- the exact smallest Harmony interception surface for remaining MouthDog -> Pikmin protection;
- exact declaring type, method, signature and Pikmin-identification boundary;
- inheritance/base behavior and secondary responsibilities;
- whether the proven S1.42AG `DoCheckInterval()` prevention guard remains part of the successor;
- preservation of MouthDog -> player behavior;
- preservation of native Pikmin -> MouthDog attack/latch/death/unlatch/task ownership;
- a one-variable delta against accepted S1.42AF;
- build-time target/signature/DLL/archive-diff diagnostics;
- runtime target, adjacent lifecycle, repetition, neighbor behavior and log checks;
- a deliberate reverse-direction Pikmin -> MouthDog test rather than passive follower observation.

Do **not** arm/build a successor or start a runtime test before this safety review is complete.

## Currently irrelevant actions

- Do not repeat `InspectMouthDogV81.ps1`.
- Do not repeat `InspectEnemyAICollisionV81.ps1` merely to recreate integrated evidence.
- Do not ask the user for `Assembly-CSharp.dll`, a full decompile, `-AssemblyPath`, a local repository clone, or manual .NET/ILSpy installation for the already closed source proofs.
- Do not repeat the S1.42AG gameplay run or request another S1.42AG log upload.

## Canonical Gale workflow

No runtime test is currently pending. When a later candidate reaches runtime testing, use the then-current canonical Gale workflow under `Knowledge/GALE_PROFILE_WORKFLOW.md` and include both the required replacement/import one-liner and the exact build-specific runtime-log uploader in the same response as the test instructions.
