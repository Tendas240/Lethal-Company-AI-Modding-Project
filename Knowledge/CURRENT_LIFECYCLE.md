# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/Projektstatus_S1.42AF_ACCEPTED.json`  
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

There is **no active build candidate** and **no runtime test outstanding**.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF` remains the runtime-evidence attribution pointer; it is not a separate acceptance authority. The completed S1.42AF log is already ingested, so no upload or repeat run is pending.

## Current open compatibility finding

The S1.42AF acceptance run also exposed a separate inherited compatibility gap:

**Mouth Dog / Eyeless Dog -> Pikmin bite/grab/death-timer interaction is currently possible and must not be.**

The log records `Biting 2 Pikmin`, two White Pikmin attaching to `EnemyAttackMouth`, and two 2.5-second death timers. Pikmin invincibility prevented the final kill attempt, but the affected Pikmin then generated 707 `Work state with no task assigned!` warnings. This is tracked by `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`.

It is not classified as an S1.42AF regression: AF was built directly from S1.42AC and changed no LethalMin package/config state. The required asymmetric target is to prevent Mouth Dog / Eyeless Dog targeting, bite, grab and kill **before** Pikmin grab/death-timer state mutation while preserving native Pikmin -> Mouth Dog combat unless exact source evidence requires otherwise.

## Current controllers

- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`.
- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AF_ACCEPTANCE_MOUTHDOG_ANALYSIS`.
- Guarded base: `Profiles/LC V1 S1.42AF Microwave Fix.r2z` / `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.
- No successor is armed.

## Exact next project action

Perform focused source/contract analysis of the confirmed MouthDog/EyelessDog -> Pikmin path under:

- `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`;
- `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`;
- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`;
- `Patches/S139CompatibilityFixes/Plugin.cs`.

Determine the exact LethalMin owner/method/inheritance/config contract for Mouth Dog targeting/bite/grab and whether native configuration can enforce the desired one-way noninteraction. If not, prove whether the existing exact `PikminAI.GrabPikmin(Transform,float,int)` prevention-only boundary can safely cover MouthDog/EyelessDog before harmful state mutation. Preserve native Pikmin -> Mouth Dog behavior. **Do not arm or build a successor until that contract is proved.**
