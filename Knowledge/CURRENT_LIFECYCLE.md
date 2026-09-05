# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Topics:** `accepted_baseline`, `active_candidate_and_next_test`  
**Evidence:** `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/Projektstatus_S1.42AC_ACCEPTED.json`  
**Related:** `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Knowledge/BCMER.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
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

## Active candidate

**NONE.**

There is no successor build armed by the S1.42AC acceptance.

## Current controllers

`RuntimeInbox/ACTIVE_BUILD.txt` contains:

`S1.42AC`

This is consistent with both the installed/tested runtime profile and the current accepted baseline.

`BuildSpecs/current.json` remains disabled:

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42AC_ACCEPTANCE_NO_SUCCESSOR_ARMED`
- guarded base = accepted S1.42AC profile/SHA
- output = `Profiles/DO_NOT_BUILD.r2z`

## Pending runtime test

**NONE.**

Permanent UX rule: whenever a future build is designated ready for runtime testing, the same response must provide both the repository-driven Gale replacement/import PowerShell one-liner when required and the exact build-specific self-contained runtime-log upload PowerShell one-liner. If a user has already completed a run but evidence upload is still pending, provide the uploader for `RuntimeInbox/ACTIVE_BUILD.txt` without requiring another run. See `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Knowledge/GALE_PROFILE_WORKFLOW.md`.

## Exact next gameplay decision

No next gameplay build is implicitly selected. Route the user's next explicit scope choice through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`.

The repository information-architecture overhaul remains complete and is not the active maintenance scope. There is currently no active gameplay candidate, runtime gate, or automatically implied successor.

Do not build inverse BCMER compensation merely to make the eight logged per-event weights numerically equal. Exact post-filter long-run `12.5%` executed EventType frequency, if ever required, is a separate algorithm-design scope rather than a correction to accepted S1.42AC.
