# 108 — Repository Handover Audit: S1.42AB Accepted / S1.42AC Rejected

**Date:** 2026-09-04  
**Status:** HANDOVER AUDIT / CANONICAL STATE CONSISTENCY CHECK

## Audit verdict

**PASS WITH INTENTIONAL HISTORICAL DRIFT PRESERVED.**

The canonical repository state now consistently identifies:

- accepted baseline: **S1.42AB — Interior Weight Normalization**;
- latest built candidate: **S1.42AC — BCMER EventType Equal Distribution**;
- S1.42AC outcome: **BUILD PASS / RUNTIME FAIL / REJECTED / NOT ACCEPTED**;
- no active runtime candidate;
- no pending gameplay test;
- no successor armed;
- exact next work: analyze the BCMER `1.71.0` final EventType-weight calculation before planning/building a successor.

## Verified accepted baseline

S1.42AB profile:

`Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`

SHA-256:

`3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance:

`Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`

Machine state:

`Current/Projektstatus_S1.42AB_ACCEPTED.json`

Runtime evidence:

`RuntimeEvidence/S1.42AB/20260904T174010Z/`

## Verified rejected latest build

S1.42AC profile:

`Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`

SHA-256:

`0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Build run:

`33903271224`

Automated build commit:

`a30b327580e28f42e55281e91abe03d32ae41363`

Runtime rejection:

`Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`

Machine state:

`Current/Projektstatus_S1.42AC_REJECTED.json`

Runtime evidence:

`RuntimeEvidence/S1.42AC/20260904T181854Z/`

Raw log SHA-256:

`8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0`

Primary runtime FAIL is unambiguous: five contexts emitted final BCMER EventType weights `6843 / 506 / 355 / 1368 / 1244 / 2737 / 27375 / 883`, not eight equal values.

## Canonical documents updated/verified

Current takeover/navigation documents now point to the rejection state:

- `README.md`;
- `START_HERE_ChatGPT_Masterprompt.txt`;
- `Current/00_CURRENT_STATE.md`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`;
- `Current/107_FINAL_HANDOVER_S1.42AB_ACCEPTED_S1.42AC_REJECTED_NEXT.md`;
- `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`;
- `Current/Projektstatus_S1.42AC_REJECTED.json`.

The old machine candidate file `Current/Projektstatus_S1.42AC_CANDIDATE.json` is retained but explicitly marked `HISTORICAL_CANDIDATE_SUPERSEDED_BY_RUNTIME_REJECTION` and points to the rejected machine state.

The old candidate record `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` is retained as historical build/test provenance, but its header and outcome now make the rejection explicit.

`BuildSpecs/S1.42AC_PLAN.md` is retained as a historical executed plan and explicitly records that its equal-scale semantic assumption was disproven.

## Controller verification

`BuildSpecs/current.json` verified:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AC_RUNTIME_REJECTION_ANALYSIS_REQUIRED`;
- base profile = accepted S1.42AB;
- base SHA-256 = `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- output = `Profiles/DO_NOT_BUILD.r2z`;
- no successor changes or patches armed.

`RuntimeInbox/ACTIVE_BUILD.txt` verified:

`S1.42AB`

`RuntimeInbox/Current/` verified clean except `.gitkeep` after successful S1.42AC runtime ingest.

## Runtime interpretation verification

S1.42AC runtime evidence was ingested before this handover. The canonical state no longer describes AC as untested/open.

The following conclusions are treated as confirmed:

1. AC's config-only change affected final BCMER EventType runtime weights relative to AB.
2. Equal configured EventType scale curves do not produce equal final effective EventType weights in BCMER `1.71.0`.
3. AC therefore fails its primary objective and is rejected.
4. The exact additional BCMER formula/calculation has **not yet been proven** and remains the next analysis target.
5. S1.42AB interior normalization remained healthy during AC runtime.
6. AC route/NavMesh/Pikmin error signatures are secondary evidence and are not automatically attributed to the BCMER config delta.

## Exact next-step verification

No gameplay/runtime test is pending. Therefore no log-upload PowerShell command is currently required.

Next technical step is analysis-only:

- inspect exact BCMER `1.71.0` final EventType-weight calculation;
- identify final pool owner and type-dependent inputs;
- choose a provable config-compensation design or a narrow fail-closed final-weight code normalization;
- follow the project-local patch safety policy if code is used;
- only then assign/arm/build a successor.

## Permanent invariants / restore state retained

Verified canonical current documents continue to preserve:

- exact BCMER `1.71.0` and no silent 2.x upgrade;
- BCMER rain-event disables;
- EnemyIsolation disabled;
- Compatibility Fixes `1.3.14`;
- BaboonBirdPikminEnemy enabled with narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy lifecycle;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C moon power/spawn restore baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- accepted Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning;
- accepted S1.42AB interior-normalization architecture;
- S1.42R whole-component disable approach remains prohibited.

Historical accepted/rejected/runtime evidence is retained; no evidence was deleted during this handover.

## Intentional historical drift retained

The following are not current authority and are intentionally preserved until the planned information-architecture overhaul:

- older chronology/current wording in portions of `Current/02_TECHNICAL_BASELINE.md`;
- historical/current checkpoint wording inside the large `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` (including older S1.42U/S1.42V checkpoints); newer canonical Current/rejection/acceptance documents override these checkpoints;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` that do not perfectly describe the newest accepted compatibility behavior;
- older handover/build-plan documents whose historical `current` statements describe the state at that time.

These files still contain diagnostic/provenance value and were not deleted. The planned repository overhaul explicitly includes authority classification/supersession and separation of live truth from chronology.

## Repository information-architecture overhaul continuity

The overhaul remains **planned, binding, not executed**.

Dedicated entry:

`OVERHAUL_START_HERE_ChatGPT.txt`

Plan:

`Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`

Execution playbook:

`Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`

Machine requirements:

`Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

When explicitly started later, the future chat must re-resolve the then-current repository state and create/verify a separate standalone pre-overhaul backup repository against the frozen pre-overhaul HEAD before the first structural migration change. A branch/tag in the primary repository alone is insufficient.

## Deletion audit

No file was identified as certain enough to delete during this handover.

Reason: rejected candidates, historical plans, old handovers, runtime evidence and diagnostic records still have provenance, regression or future reasoning value. The later information-architecture overhaul is the appropriate controlled stage for classification/redirects and any eventual conservative removal.
