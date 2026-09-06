# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/Projektstatus_S1.42AF_ACCEPTED.json`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`, `Current/132_MOUTHDOG_PATCH_SAFETY_REVIEW.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/Projektstatus_S1.42AG_CANDIDATE.json`  
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

## Active candidate / runtime state

**S1.42AG — Mouth Dog Pikmin One-Way Protection — ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED.**

- Profile: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`
- SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`
- Compatibility DLL SHA-256: `976264a31b85bf3d913d3ad703fa770a666957664d0de5b848a5073b0883d064`
- Candidate: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`
- Project status: `Current/Projektstatus_S1.42AG_CANDIDATE.json`
- Runtime test outstanding: **yes**.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG`.
- `BuildSpecs/current.json` is disabled and guards the S1.42AG artifact while runtime validation is open.

The exact source contract is proved by `Current/130`, the authorized patch boundary by `Current/131`, and the pre-build safety review by `Current/132`. S1.42AG blocks exact declared `MouthDogPikminEnemy.DoCheckInterval()` with `Priority.First` before Pikmin target collection/bite/grab dispatch while keeping the adapter enabled.

The next action is the full-normal runtime gate described in `Current/133`, followed by the build-specific log uploader. S1.42AF remains accepted until that evidence passes.

## Current open compatibility finding

The S1.42AF acceptance run also exposed a separate inherited compatibility gap:

**Mouth Dog / Eyeless Dog -> Pikmin bite/grab/death-timer interaction is currently possible and must not be.**

The log records `Biting 2 Pikmin`, two White Pikmin attaching to `EnemyAttackMouth`, and two 2.5-second death timers. Pikmin invincibility prevented the final kill attempt, but the affected Pikmin then generated 707 `Work state with no task assigned!` warnings. This is tracked by `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`.

It is not classified as an S1.42AF regression: AF was built directly from S1.42AC and changed no LethalMin package/config state. The required asymmetric target is to prevent Mouth Dog / Eyeless Dog targeting, bite, grab and kill **before** Pikmin grab/death-timer state mutation while preserving native Pikmin -> Mouth Dog combat unless exact source evidence requires otherwise.

## Current controllers

- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG`.
- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AG_BUILD_AWAITING_RUNTIME_VALIDATION`.
- Guarded candidate: `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z` / `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`.
- No successor beyond S1.42AG is armed.

## Exact next project action

Import and runtime-test S1.42AG using `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`. Exercise repeated Mouth Dog lunges around Pikmin, prove the Dog -> Pikmin bite/grab/death-timer path is absent, prove Pikmin -> Dog attack/latch/death cleanup and Dog -> player attacks remain functional, confirm normal full-stack startup/generation and the accepted S1.42AF Microwave contract, then upload the complete fresh S1.42AG log. **Do not accept S1.42AG from build/startup success alone.**
