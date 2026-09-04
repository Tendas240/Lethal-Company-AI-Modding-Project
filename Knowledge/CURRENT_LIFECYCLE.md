# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`, `Current/Projektstatus_S1.42AC_REJECTED.json`  
**Related:** `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/BCMER.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-04

## Accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`
- SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
- Machine state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`
- Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

S1.42AB preserves LethalLevelLoader ownership of interior viability/exclusion membership and normalizes every positive rarity in LLL's returned viable list to `100`. The accepted Offense run retained all 40 viable entries, kept Black Mesa single-registered, generated `Expanded facility`, and had the project-critical Work/no-task, Leader-null, Compatibility Fixes Error and Fatal regressions at zero.

## Active candidate

**NONE.**

S1.42AC exists as a built artifact but is **formally rejected / not promoted / not armed**. Its original rejection criterion was later shown to be semantically wrong for BCMER's per-event weighting model, but that analysis did not silently accept the artifact.

- S1.42AC profile SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Historical rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Corrected source-path analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`

## Current controllers

`RuntimeInbox/ACTIVE_BUILD.txt` contains:

`S1.42AB`

`BuildSpecs/current.json` is disabled:

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42AC_WEIGHT_PATH_ANALYSIS_COMPLETE_NO_SUCCESSOR_ARMED`
- guarded base = accepted S1.42AB profile/SHA
- output = `Profiles/DO_NOT_BUILD.r2z`

## Pending runtime test

**NONE.**

No runtime-log uploader is currently required.

Permanent UX rule: whenever a future build is designated ready for runtime testing, the same response must provide both the repository-driven Gale replacement PowerShell one-liner and the exact build-specific self-contained runtime-log upload PowerShell one-liner. See `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Knowledge/GALE_PROFILE_WORKFLOW.md`.

## Exact next gameplay decision

The repository overhaul is the active maintenance scope and must not alter gameplay state.

If gameplay work resumes after the overhaul, no successor is implied automatically. The outstanding S1.42AC artifact may first be reconsidered under the corrected BCMER acceptance model in `Knowledge/BCMER.md`; alternatively a different deferred scope may be selected explicitly from `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`.

Do not build inverse BCMER compensation merely to make the eight logged per-event weights numerically equal.
