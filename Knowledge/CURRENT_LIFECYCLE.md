# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/Projektstatus_S1.42AC_ACCEPTED.json`, `Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`  
**Related:** `BuildSpecs/current.json`, `BuildSpecs/S1.42AD_PLAN.md`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/BCMER.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`, `Knowledge/ITEM_TUNING.md`  
**Last-Validated:** 2026-09-05

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

- Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`
- SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
- Machine state: `Current/Projektstatus_S1.42AC_ACCEPTED.json`
- Fresh acceptance runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

S1.42AC inherits accepted S1.42AB unchanged outside the isolated BCMER EventType scale config and implements the intended equal static EventType probability model under exact BCMER `1.71.0`. All eight scales are constant `12.5`; BCMER's unequal logged per-event weights are the expected inverse-population normalization. Fresh runtime reproduced the expected weight/count formula, kept project-critical regression markers at zero, and the user reported no problematic gameplay behavior.

S1.42AB remains the previous accepted rollback/predecessor baseline.

## Historical S1.42AC rejection qualification

`Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` remains historical evidence of the first runtime decision. Its requirement that the eight logged `Set eventType weight ...` values be numerically equal was later shown to be technically invalid by `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`.

The artifact was **not** silently accepted by that analysis. It was explicitly promoted only by the later corrected acceptance decision in `Current/118...` after fresh S1.42AC runtime confirmation.

## Selected next scope

**S1.42AD — Functional Microwave Spawn Rarity Reduction — SOURCE DRAFT PRESENT / NOT BUILT.**

The user explicitly selected the next build after S1.42AC acceptance. The interrupted ChatGPT session then began the Functional Microwave scope and committed a source-only draft under:

`Patches/S142ADCodeRebirthMicrowaveSpawnTuning/`

Recovery/audit record:

`Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`

Blocked pre-build plan:

`BuildSpecs/S1.42AD_PLAN.md`

The draft uses `SpawnScale = 0.5f`, but current canonical project requirements only establish that the Functional Microwave should become rarer; no exact percentage is currently authorized. Therefore `0.5` is a proposal, not a current accepted target.

## Active candidate

**NONE.**

No S1.42AD profile has been built. Source files and a blocked pre-build plan are not a gameplay candidate.

## Current controllers

`RuntimeInbox/ACTIVE_BUILD.txt` contains:

`S1.42AC`

This is the runtime-active/evidence-attribution build and remains the accepted baseline because no S1.42AD profile exists yet.

`BuildSpecs/current.json` remains disabled:

- `enabled = false`
- `build_id = IDLE_S1.42AD_SCOPE_SELECTED_SOURCE_REVIEW_PENDING_NO_SUCCESSOR_ARMED`
- guarded base = accepted S1.42AC profile/SHA
- output = `Profiles/DO_NOT_BUILD.r2z`

## Pending runtime test

**NONE.**

There is no S1.42AD runtime test because no candidate exists.

Permanent UX rule: whenever a future build is designated ready for runtime testing, the same response must provide both the repository-driven Gale replacement/import PowerShell one-liner when required and the exact build-specific self-contained runtime-log upload PowerShell one-liner. If a user has already completed a run but evidence upload is still pending, provide the uploader for `RuntimeInbox/ACTIVE_BUILD.txt` without requiring another run. See `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Knowledge/GALE_PROFILE_WORKFLOW.md`.

## Exact next gameplay action

Before any S1.42AD build is armed:

1. resolve the exact desired Functional Microwave spawn reduction magnitude; the current `0.5` draft value is not yet an authorized target;
2. independently verify the exact CodeRebirth `1.6.9` / DawnLib `0.9.25` / Dusk `0.9.25` ownership and the exact 19-curve Microwave provider contract;
3. complete/finalize the blocked pre-build plan `BuildSpecs/S1.42AD_PLAN.md`, including the mandatory Patch Safety Review from `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`;
4. only then arm the repository build controller.

Do not treat the green Knowledge Architecture run on the source draft as a compile/build gate. Do not runtime-test source-only files.

The repository information-architecture overhaul remains complete and is not the active maintenance scope.
