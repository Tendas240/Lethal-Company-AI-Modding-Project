# S1.42AK-BMAFDIAG1 Inactive Review-Build Infrastructure

**Date:** 2026-09-30  
**Status:** INFRASTRUCTURE IMPLEMENTED ON WORKING BRANCH / REVIEW CI NOT YET RECONCILED / NO REVIEWED BYTES PUBLISHED / NOT RUNTIME-ARMED

## Implemented scope

This checkpoint prepares repository-native review-build infrastructure only:

- immutable separate recipe `BuildSpecs/S1.42AK-BMAFDIAG1.json`;
- executable policy-test harness `AnalysisTools/S142AKBMAFDiag1PolicyTests/` outside the integrated patch source directory;
- exact archive/config/lifecycle validator `AnalysisTools/validate_s142ak_bmafdiag1_build.py`;
- review workflow `.github/workflows/s142ak-bmafdiag1-build-static.yml`;
- checkpoint plan `BuildSpecs/S1.42AK-BMAFDIAG1_REVIEW_BUILD_PLAN.md`.

## Preserved source/static boundary

`Patches/S142AKBMAFDiag1/` is not modified and receives no `Tests/` subdirectory. The already integrated PR #198 source bytes remain the source under review.

The harness links the integrated pure policy files at build time. It checks exact Foundry targeting and fail-closed selection behavior together with retained provenance, runtime identity, traversal and topology policies. It does not write LLL configuration or create availability.

## Review construction contract

The workflow derives the review profile directly from exact accepted S1.42AK SHA-256:

`b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`

Expected archive delta:

- add exactly `BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll`;
- remove nothing;
- change existing `export.r2x` only for profile identity;
- change existing `BepInEx/config/LethalLevelLoader.cfg` only by appending one canonical Abandoned Foundry section;
- preserve all other archive members byte-for-byte;
- preserve accepted `S142ABInteriorWeightNormalization.dll` bytes exactly;
- freshly re-verify exact LethalLevelLoader 1.7.12 provenance.

The Foundry section is anchored to the repository-native owner-default section at `RuntimeEvidence/S1.42A/20260902T224318Z/extracted/config/config/LethalLevelLoader.cfg`. Its key set and every owner value remain unchanged except the two authorized semantic deltas:

1. `Enable Content Configuration = true`;
2. append exactly `Black Mesa:100` to the existing owner `Dungeon Injection Settings - Manual Level Names List`.

No `External:100`, no size-rule delta, no additional tag/mod/route-price mapping and no duplicate Foundry section or registration is permitted.

The output is an Actions review artifact only. This infrastructure does not publish or runtime-arm it.

## Preserved live controllers

The build validator requires the current live state to remain unchanged:

- accepted baseline: `S1.42AK`;
- active gameplay candidate: `S1.42AK-BMDSFIX1`;
- BMDSFIX1 target qualification: outstanding/passive/unwaived;
- `BuildSpecs/current.json`: disabled / `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt`: `S1.42AK-BMDSFIX1`;
- BMAFDIAG1: inactive review only.

## Not claimed yet

This file does not claim a successful compile, successful policy test, successful archive/config-delta validation, stable review profile SHA-256, DLL SHA-256, workflow run ID, Actions artifact ID, publication, Gale import, runtime arming, gameplay evidence, or Black Mesa x Abandoned Foundry qualification.

Those facts may be recorded only after the repository-native review gate actually completes and is separately reconciled.
