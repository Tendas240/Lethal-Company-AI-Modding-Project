# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`, `Current/132_MOUTHDOG_PATCH_SAFETY_REVIEW.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/Projektstatus_S1.42AF_ACCEPTED.json`, `Current/Projektstatus_S1.42AG_REJECTED.json`, `RuntimeEvidence/S1.42AG/20260906T085500Z/`  
**Related:** `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/CODEREBIRTH.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-06

## Accepted baseline

**S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Injected DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`
- Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Fresh acceptance runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`
- Runtime log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`

S1.42AF passed the path-length-safe packaging gate and the corrected Functional Microwave provider contract. The imported nested SoundAPI LC binding was present and non-empty at 40960 bytes on a 226-character full path; BepInEx then reached normal preloader/chainloader/game runtime. Runtime validated CodeRebirth `1.6.9`, DawnLib/Dusk `0.9.25`, `PrioritiseMoons=true`, exactly 18 Moon/tag and 18 Interior/tag curves, and the final mutation marker: 18 Moon/tag curves scaled by `0.5`, 18 Interior curves validation-only and not mutated.

S1.42AC remains the accepted predecessor and historical rollback/provenance point.

## Historical rejected/superseded Microwave steps

**S1.42AD — Functional Microwave Spawn Rarity Reduction — RUNTIME REJECTED / NOT ACCEPTED.**

S1.42AD failed closed because it expected `InteriorCurves=0`, while runtime exposed 18 Interior/tag curves. No `0.5` mutation executed. Rejection authority: `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`.

**S1.42AE — Functional Microwave Provider Contract Correction — SUPERSEDED FOR PATH-LENGTH-SAFE PACKAGING / NOT GAMEPLAY-REJECTED.**

The corrected provider code was never reached during AE's failing launches. v2.4 and direct filesystem checks proved the nested SoundAPI binding remained physically present and non-empty at 40960 bytes, but the full path measured 262 characters and BepInEx/Mono failed before chainloader startup. S1.42AF isolated the same functional source on a short profile identity and succeeded, confirming the path-length compatibility classification. Decision history: `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`.

## Latest built artifact / runtime decision

**S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`
- SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`
- Compatibility DLL SHA-256: `976264a31b85bf3d913d3ad703fa770a666957664d0de5b848a5073b0883d064`
- Candidate: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`
- Rejection: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`
- Project status: `Current/Projektstatus_S1.42AG_REJECTED.json`
- Runtime evidence: `RuntimeEvidence/S1.42AG/20260906T085500Z/`
- Runtime log SHA-256: `3e8ca4c8fe045bbd2c62576dbbd5aaba2a226990e6b4af4149481f2672c35dfe`
- Runtime test outstanding: **no**.
- Active candidate: **none**.

The exact S1.42AG `Priority.First` guard on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` did arm and execute. Runtime proves it successfully blocks the LethalMin Pikmin target/bite/grab/death-timer mutation path before `GrabbedPikmin` bookkeeping or `PikminAI.GrabPikmin(...)`. The accepted S1.42AF run had produced `Biting 2 Pikmin`, `EnemyAttackMouth` attachments, 2.5-second death timers and then 707 `Work state with no task assigned!` warnings. In S1.42AG that warning count is `0`, and the harmful bite/grab signature is absent.

However, the runtime contract was broader than state-mutation prevention. During the S1.42AG test a Mouth Dog visibly targeted and attacked a scrap-carrying Purple Pikmin. The same encounter contains repeated native Mouth Dog noise-targeting diagnostics (`Heard noise!`, `targetPos`, `lastheardnoisePosition`). Those diagnostics are consistent with, but do not by themselves prove, a remaining target/attack path outside the blocked LethalMin dispatcher. The intended reverse direction — Pikmin attacking/latching the Mouth Dog with native death/unlatch/task cleanup — was also not positively proven in that run.

Therefore S1.42AG is rejected as a partial fix and is **not** a safe gameplay base.

The inherited S1.42AF Functional Microwave gate remained healthy in S1.42AG: `PrioritiseMoons=true`, 18 Moon/tag curves, 18 Interior/tag curves, 18 Moon/tag curves scaled by `0.5`, Interior curves validation-only. The SoundAPI `RoundManagerPatch::Reporting()` `TypeLoadException` also existed in the accepted S1.42AF evidence and is not classified as an S1.42AG regression.

## Current controllers

- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains the last runtime-evidence attribution target; it is not acceptance authority.
- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AG_RUNTIME_REJECTION_AWAITING_TARGETED_ANALYSIS`.
- Guarded build base: accepted `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.
- No successor beyond S1.42AG is armed.

## Exact next project action

Perform **targeted repository-native analysis of the remaining Mouth Dog targeting/attack path** exposed by the S1.42AG rejection. Use exact current source and runtime evidence to determine why a scrap-carrying Purple Pikmin can still be selected/attacked despite the successful `MouthDogPikminEnemy.DoCheckInterval()` prevention guard, and determine whether the intended Pikmin -> Mouth Dog attack/latch path remains functional.

Do **not** guess a fallback, do **not** disable the `MouthDogPikminEnemy` adapter, and do **not** build or arm a successor until the exact owner/method boundary is proved under the project-local patch safety policy.
