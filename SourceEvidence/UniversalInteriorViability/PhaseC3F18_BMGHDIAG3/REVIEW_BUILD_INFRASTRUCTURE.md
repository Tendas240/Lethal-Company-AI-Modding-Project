# S1.42AK-BMGHDIAG3 Inactive Review-Build Infrastructure

**Date:** 2026-09-27  
**Status:** INFRASTRUCTURE IMPLEMENTED ON WORKING BRANCH / REVIEW CI NOT YET RECONCILED / NO REVIEWED BYTES PUBLISHED / NOT RUNTIME-ARMED

## Implemented scope

This checkpoint prepares repository-native review-build infrastructure only:

- immutable separate recipe `BuildSpecs/S1.42AK-BMGHDIAG3.json`;
- executable policy-test harness `AnalysisTools/S142AKBMGHDiag3PolicyTests/` outside the integrated patch source directory;
- exact archive/lifecycle validator `AnalysisTools/validate_s142ak_bmghdiag3_build.py`;
- review workflow `.github/workflows/s142ak-bmghdiag3-build-static.yml`;
- checkpoint plan `BuildSpecs/S1.42AK-BMGHDIAG3_REVIEW_BUILD_PLAN.md`.

## Preserved source/static boundary

`Patches/S142AKBMGHDiag3/` is not modified and receives no `Tests/` subdirectory. The already integrated source bytes remain the source under review.

The harness links the integrated pure policy files at build time. It retains provenance, runtime type/assembly/method, selection, traversal and topology regression coverage while deliberately omitting the disproven BMGHDIAG2 "wrong manifest module" refusal case.

## Review artifact contract

The workflow will derive the review profile directly from exact accepted S1.42AK SHA-256:

`b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`

Expected archive delta:

- add exactly `BepInEx/plugins/S142AKBMGHDiag3/S142AKBMGHDiag3.dll`;
- remove nothing;
- preserve every existing member byte-for-byte except `export.r2x`;
- allow `export.r2x` to differ only in profile identity;
- preserve accepted `S142ABInteriorWeightNormalization.dll` bytes exactly;
- freshly re-verify exact LethalLevelLoader 1.7.12 provenance.

The output is an Actions review artifact only. This infrastructure does not publish the profile into repository `Profiles/`.

## Preserved live controllers

The build validator requires the current live state to remain unchanged:

- accepted baseline: `S1.42AK`;
- active gameplay candidate: `S1.42AK-BMDSFIX1`;
- BMDSFIX1 target qualification: outstanding and passive;
- `BuildSpecs/current.json`: disabled / `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt`: `S1.42AK-BMDSFIX1`;
- BMGHDIAG3: inactive review only.

## Not claimed yet

This file does not claim a successful compile, successful policy test, successful archive-delta validation, stable review profile SHA-256, DLL SHA-256, workflow run ID, Actions artifact ID, publication, Gale import, runtime arming, gameplay evidence, or Black Mesa x Greenhouse qualification.

Those facts may be recorded only after the corresponding repository-native gate has actually completed and been reconciled.
