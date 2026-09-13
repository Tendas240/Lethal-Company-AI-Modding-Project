<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1 candidate=S1.42AI-DIAG1 runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md`  
**Last-Validated:** 2026-09-13

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact / active candidate

**S1.42AI-DIAG1 — ShyGuy Isolation Diagnostic — ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1 ShyGuy Isolation.r2z`  
SHA-256: `22e2132669a790756f2a1e2bd10b14fd05144b3ecdd55233d8d57f1d6dd9f3fd`  
Parent: `S1.42AI`  
Candidate: `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`  
Canonical build run: `34777833867`  
Build commit: `1018ac909435a51f1b98ceb9dfdad0599dc4dcc4`

The canonical build, pre-build static gate, and materialized profile checks passed. Package state is unchanged; the reviewed diagnostic config overlay and exact narrow plugin are present.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1**.
- Active candidate: **S1.42AI-DIAG1**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1_BUILD_AWAITING_RUNTIME_VALIDATION` and guards the exact DIAG1 profile/SHA.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1` attributes the next evidence to DIAG1.

## Diagnostic runtime gate

Use `AnalysisEvidence/S1.42AI-DIAG1/MINIMAL_GUARD_CONTRACT.md` and `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`. Require successful startup/identity/config/guard markers, no `DIAG1_ISOLATION_BYPASS`, no unexpected non-ShyGuy live enemy, and preserved exact Shy Guy observability.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` is deferred until after DIAG1 and is **not waived**.

## Canonical Gale workflow

Use the repository-driven **v2.4** replacement/import path in `Knowledge/GALE_PROFILE_WORKFLOW.md`, implemented by `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The ready-to-test import and exact S1.42AI-DIAG1 log uploader are recorded in `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md` and must be supplied together.

## Exact next project action

Runtime-test S1.42AI-DIAG1 as the active temporary diagnostic candidate. Verify DIAG1 startup/identity/config/guard markers, exercise the ShyGuy-only round, fail on any DIAG1_ISOLATION_BYPASS or unexpected non-ShyGuy enemy, preserve ShyGuy observability, then upload the exact DIAG1 LogOutput.log. Diagnostic success does not accept S1.42AI; its full-normal BCMER ShyGuy gate remains required afterward.
