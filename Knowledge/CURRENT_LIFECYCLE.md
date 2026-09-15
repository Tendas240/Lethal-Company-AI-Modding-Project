<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=S1.42AI-DIAG1R2 runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`, `Current/Projektstatus_S1.42AI-DIAG1R2_CANDIDATE.json`, `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md`, `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact and active candidate

**S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z`  
SHA-256: `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`  
Candidate: `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`  
Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`

R2 preserves the metadata-derived owner repair and fixes the R1 complex-owner failure by making the exact `kite.ZelevatorCode` EndlessElevator target conditional on dependency applicability. Canonical materialized evidence proves this profile has the dependency absent and therefore records the exact target as `NOT_APPLICABLE_DEPENDENCY_ABSENT`; static/materialized semantic equivalence is green.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R2**.
- Active candidate: **S1.42AI-DIAG1R2**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R2_BUILD_AWAITING_RUNTIME`; no successor build is armed during the runtime gate.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R2` controls attribution for the next uploaded runtime log and is not acceptance authority.

Canonical Gale runtime replacement/import route: `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, pinned helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`.

## Exact runtime gate

Run one R2 diagnostic profile. Require `[DIAG1_OWNER_TYPE_DERIVED]` and the dependency-absent `[DIAG1_COMPLEX_TARGET_NOT_APPLICABLE]` path to arm without DIAG1 invalidation or rollback; all approved isolation layers must install; no live non-ShyGuy isolation bypass or unexpected non-ShyGuy enemy may appear; exact Shy Guy must remain visibly observable, including outside when an exterior Shy Guy is present; exercised guards must remain bounded without broad shared-spawn/network regression.

The inherited `Can Exit Facility = false` behavior explains why an interior Shy Guy may not follow a player outside and is not itself the current diagnostic failure condition.

Use `AnalysisEvidence/S1.42AI-DIAG1R1/MINIMAL_GUARD_CONTRACT.md` plus `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md` for the exact guard/applicability boundary and `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md` for ready-to-test commands.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**. R2 diagnostic success cannot replace it.

## Exact next project action

Perform one R2 diagnostic gameplay run, then upload the complete fresh R2 log for repository-native ingestion and decision. Do not rerun failed DIAG1 or R1 profiles.
