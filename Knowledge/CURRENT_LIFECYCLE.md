<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R1 candidate=S1.42AI-DIAG1R1 runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`, `Current/Projektstatus_S1.42AI-DIAG1R1_CANDIDATE.json`, `AnalysisEvidence/S1.42AI-DIAG1R1/MATERIALIZED_VALIDATION.md`, `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-14

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact and active candidate

**S1.42AI-DIAG1R1 — ShyGuy Isolation Diagnostic Owner Type Resolution Repair — ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1R1 ShyGuy Isolation Repair.r2z`  
SHA-256: `b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd`  
Candidate: `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`  
Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R1/MATERIALIZED_VALIDATION.md`

R1 repairs the predecessor's owner type-resolution failure without hardcoding a replacement namespace. The exact method metadata derives the real `List<T>` generic argument, and materialized evidence identifies it as `LethalMin.Pikmin.PikminType`. The canonical R1 profile passed the strengthened static and post-build semantic-equivalence gates.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R1**.
- Active candidate: **S1.42AI-DIAG1R1**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R1_BUILD_AWAITING_RUNTIME`; no successor build is armed during the runtime gate.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R1` controls attribution for the next uploaded runtime log.

## Exact runtime gate

Run the R1 diagnostic profile and require the metadata-derived owner path to arm without owner-target invalidation, DIAG1 invalidation, or Harmony rollback. All approved DIAG1 identity/config/owner/complex/transpiler markers must install; no live non-ShyGuy isolation bypass or unexpected non-ShyGuy enemy may appear while isolation is armed; exact Shy Guy must remain observable; exercised owner blocks must remain bounded without exception/retry flood.

Use `AnalysisEvidence/S1.42AI-DIAG1R1/MINIMAL_GUARD_CONTRACT.md` for the exact guard boundary and `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md` for the ready-to-test commands.


## Canonical Gale workflow

Import the active R1 candidate only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, using the canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The candidate record supplies the repository-driven one-line launcher together with the exact R1 runtime-log uploader; these commands are paired and must not be substituted by an older Gale helper.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**. R1 diagnostic success cannot replace it.

## Exact next project action

Perform one R1 diagnostic gameplay run, then upload the complete fresh R1 log for repository-native ingestion and decision. Do not rerun the failed predecessor DIAG1 profile.
