# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/135_MOUTHDOG_V81_SOURCE_CAPTURE_TOOL_WINDOWS_HARDENING_STATE.md`, `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MOUTHDOGAI_FOCUSED_DECOMPILE.txt`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
**Related:** `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-06

## Accepted baseline

**S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Injected DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`
- Runtime log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`

S1.42AF remains the only accepted gameplay base. S1.42AC remains its accepted predecessor/provenance point.

## Latest built artifact

**S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**

- Profile: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`
- SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`
- Compatibility DLL SHA-256: `976264a31b85bf3d913d3ad703fa770a666957664d0de5b848a5073b0883d064`
- Candidate: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`
- Rejection: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`
- Runtime evidence: `RuntimeEvidence/S1.42AG/20260906T085500Z/`
- Runtime log SHA-256: `3e8ca4c8fe045bbd2c62576dbbd5aaba2a226990e6b4af4149481f2672c35dfe`
- Runtime test outstanding: **no**
- Active candidate: **none**

S1.42AG's `Priority.First` guard on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` armed and executed. It successfully prevented the LethalMin-specific Pikmin bite/grab/death-timer mutation path: the prior `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab signature disappeared and `Work state with no task assigned!` fell from 707 in the S1.42AF exposure evidence to 0.

S1.42AG remains rejected because the broader one-way contract still failed visually: a Mouth Dog pursued/attacked a scrap-carrying Purple Pikmin through a path outside the blocked LethalMin dispatcher. Reverse-direction Pikmin -> Mouth Dog combat was not deliberately exercised and has no pass/fail result yet.

## Vanilla V81 MouthDogAI source capture — completed

The previously prepared Windows capture is now complete and provenance-verified. `Current/135_MOUTHDOG_V81_SOURCE_CAPTURE_TOOL_WINDOWS_HARDENING_STATE.md` is resolved history; current analysis authority is `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`.

Authoritative capture:

- evidence branch: `source-evidence/mouthdog-v81-20260906t121738z`;
- evidence commit: `a618b19bfc30234ca556c924d681d43b2c13d1d9`;
- capture base: `main = 3049b0fa52af79db39efb075d94684d229eed3c6`;
- assembly SHA-256: `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- Steam buildid: `22825947`;
- manifest: `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json`;
- focused report: `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MOUTHDOGAI_FOCUSED_DECOMPILE.txt`.

Do not re-run the capture merely to recreate evidence that already exists.

## What the captured native source proves

Vanilla `MouthDogAI.DetectNoise(Vector3 noisePosition, ...)` is position-based. Native chase logic stores/uses `noisePositionGuess` and can enter a lunge once the dog is within less than 4 units of that world-space position.

Vanilla `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` is a separate generic enemy-collision attack surface. It calls `base.OnCollideWithEnemy(...)`; for a different enemy type after its cooldown it can face the collided enemy, enter a lunge in chase state, and call `collidedEnemy.HitEnemy(2, ...)`.

Exact LethalMin 1.1.108 evidence proves `PikminAI : EnemyAI`, so Pikmin can enter that generic Vanilla path without any Pikmin-specific selector in `MouthDogAI`.

Exact LethalMin evidence also proves Pikmin audio can call `RoundManager.PlayAudibleNoise(...)` at the Pikmin position. The accepted configuration has `Dont Make Audible Noises = false`, so a Pikmin itself is a proved possible audible-noise emitter.

The runtime evidence confirms a Purple Pikmin carried `GoldBar(Clone)`, but current source/runtime evidence does **not** prove that the carried GoldBar itself caused the Dog's noise pursuit. That narrower carried-scrap/noise causality remains unresolved.

## Current controllers

- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_MOUTHDOG_V81_CAPTURE_AWAITING_TARGETED_SOURCE_EXTENSION`.
- Guarded base remains accepted `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains runtime-evidence attribution only.
- No successor is armed.
- No runtime test is pending.

## Exact next project action

Perform a **targeted source-evidence extension**, not a build and not another gameplay run.

Prove exactly two remaining contracts:

1. Vanilla V81 `EnemyAI.OnCollideWithEnemy()` base behavior/side effects, because `MouthDogAI.OnCollideWithEnemy()` calls it before its own generic `EnemyAI` lunge/damage logic.
2. Exact LethalMin 1.1.108 `PikminItem.CarryNumerator()` plus carry-item audio / `PlayAudibleNoise` callsites, so the narrower carried-GoldBar/noise hypothesis is proved or rejected rather than inferred.

Only after those two source boundaries are proved may a successor-specific safety review be performed under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

Do **not** build or arm a successor, start a runtime test, disable `MouthDogPikminEnemy`, add broad `EnemyAI` scanning, guess a Harmony boundary, alter Mouth Dog -> player behavior, or suppress native Pikmin -> Mouth Dog combat/latch/death-unlatch ownership before that proof is complete.

## Historical Microwave boundary

S1.42AD remains runtime-rejected historical provider-contract evidence. S1.42AE remains superseded for path-length-safe packaging, not gameplay-rejected. S1.42AF proved the corrected provider source under a safe profile path and remains accepted.
