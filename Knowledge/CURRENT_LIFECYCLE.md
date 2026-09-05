# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`, `Current/128_S1.42AF_RUNTIME_GATE_PASS_ACCEPTANCE_DEFERRED_MOUTH_DOG_BASELINE_GAP.md`, `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md`, `Current/Projektstatus_S1.42AF_RUNTIME_PASS_ACCEPTANCE_DEFERRED.json`  
**Related:** `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`, `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Last-Validated:** 2026-09-06

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC remains the formal rollback/gameplay baseline until a later explicit lifecycle decision promotes a successor.

## Latest built artifact / active candidate

**S1.42AF — Path-Length-Safe Microwave Packaging — TARGETED RUNTIME GATE PASS / ACCEPTANCE DEFERRED / NOT REJECTED.**

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- Gale profile name: `LC V1 S1.42AF Microwave Fix`
- Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- Microwave DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`
- Build workflow run: `33993880634` — SUCCESS
- Automated build commit: `2cab9044579e74739669440699c763a32f0fe379`
- Candidate record: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Runtime decision: `Current/128_S1.42AF_RUNTIME_GATE_PASS_ACCEPTANCE_DEFERRED_MOUTH_DOG_BASELINE_GAP.md`
- Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`
- Raw-log SHA-256: `63df88a3acb0c455bab914fd844767cb50b7384ab4b1ede8bd7cbcb63537d956`
- Project status: `Current/Projektstatus_S1.42AF_RUNTIME_PASS_ACCEPTANCE_DEFERRED.json`

The S1.42AF runtime test is complete. No rerun is currently pending.

### S1.42AF targeted gate result

S1.42AF clears the S1.42AE path-length/preloader failure and reaches normal BepInEx startup, moon/interior generation and gameplay.

The preserved Microwave plugin then validates the exact runtime contract:

- CodeRebirth `1.6.9`;
- DawnLib/Dusk `0.9.25`;
- `PrioritiseMoons=true`;
- `MoonCurves=18`;
- `InteriorCurves=18`;
- both exact keysets present;
- all 18 Functional Microwave Moon/tag curves scaled by `0.5`;
- all 18 Interior/tag curves validation-only, not mutated;
- no other map-object provider modified.

Therefore the Microwave/provider/path-length scope is **PASS**. S1.42AF is not runtime-rejected.

## Why S1.42AF is not yet the accepted full-stack baseline

The same normal run exposed a separate Mouth Dog / Eyeless Dog -> Pikmin compatibility problem. The user directly observed the dog entering a bite/grab interaction with Pikmin, and the evidence contains `707` occurrences of `Work state with no task assigned!` later in the run.

This is not being dismissed as monitor-only. Formal full-stack acceptance is deferred until the compatibility gap is analyzed.

The issue is also not attributed to the isolated S1.42AF Microwave delta:

- S1.42AF changed only `export.r2x` and added the Microwave tuning DLL;
- there were no mod/config changes;
- `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll` is byte-identical in S1.42AC and S1.42AF: `57344` bytes, SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- current compatibility source protects Crawler/Thumper and Baboon Hawk at the common `GrabPikmin` prevention path, but has no Mouth-Dog branch.

Canonical classification: **pre-existing/baseline Enemy -> Pikmin compatibility gap exposed during S1.42AF, not an S1.42AF Microwave regression.**

## Current selected scope

**Mouth Dog / Eyeless Dog -> Pikmin baseline compatibility analysis.**

Authority: `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md`.

Required result:

- Mouth Dogs must not grab or bite Pikmin at all;
- Pikmin -> Mouth Dog combat stays native;
- native LethalMin enemy death/unlatch/task lifecycle stays intact.

Investigation order:

1. inspect LethalMin `1.1.108` configuration for an exact native one-way noninteraction option;
2. if config is insufficient, prove the exact Mouth-Dog adapter/collision/bite/grab ownership path;
3. choose the earliest prevention-before-mutation point;
4. only then prepare an isolated successor plan under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

No successor build ID is currently legitimate or armed.

## Current controllers

- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF` — retained for runtime-evidence attribution.
- `BuildSpecs/current.json` is disabled.
- Controller id: `IDLE_AFTER_S1.42AF_RUNTIME_GATE_PASS_MOUTH_DOG_ANALYSIS_SELECTED`.
- Guarded build base: accepted S1.42AC — `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z` / `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`.
- Successor armed: **no**.
- Runtime test outstanding: **no**.

## Exact next project action

Do **not** rerun S1.42AF merely to repeat its completed Microwave gate.

Open `Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md`, inspect LethalMin configuration and exact source/runtime ownership for Mouth Dog -> Pikmin bite/grab, and determine whether the required asymmetric noninteraction can be achieved natively or needs a narrow project-local prevention extension. Do not name or arm a successor until the exact contract and isolated build plan are proven.
