<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md`, `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`, `AnalysisEvidence/S1.42AI-DIAG1R2/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z`  
SHA-256: `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`  
Build request: `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md`  
Build workflow run: `34958254886` (`workflow_dispatch`, success)  
Build commit: `854e4435676ef32648407dae9ba1e2e704a420d1`  
Canonical post-build validation: `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md` / run `34990530260` (`push`, success)

R2 is the newly compiled successor of failed R1 and remains directly derived from exact full-normal S1.42AI, never from R1 bytes. The persisted validation proves the DIAG1 static contract, the materialized `kite.ZelevatorCode` dependency-absent `NOT_APPLICABLE` behavior, and semantic DLL equivalence to the repaired green-gate build.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R2**, verified but not accepted.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R2_MATERIALIZED_VALIDATION_AWAITING_RUNTIME_CANDIDATE_ACTIVATION` and guards accepted S1.42AH.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R1` remains evidence attribution for the last completed failed R1 run; it is not acceptance authority and does not authorize gameplay.

## R1 history and R2 repair

R1 remains a completed failed diagnostic: it proved metadata-derived `LethalMin.Pikmin.PikminType`, then invalidated because it incorrectly required `ElevatorMod.Patches.EndlessElevator` when dependency GUID `kite.ZelevatorCode` was absent. The permanent source contract is now: dependency absent => only that compat target is `NOT_APPLICABLE`; dependency present => exact provider/type/owner/signature/install remains required and fail-closed. R2 contains and materializes that repaired contract.

## Canonical Gale workflow

Whenever R2 or any later runtime candidate is actually armed, import/replace it only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` using canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. There is no active runtime candidate now, so this routing rule does not authorize a gameplay run by itself.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate remains mandatory and is **deferred, not waived**. Diagnostic success cannot accept the full-normal candidate.

## Exact next project action

Perform a **separate coordinated R2 runtime-candidate activation transition**. Re-verify exact R2 profile/evidence and no-candidate state, then atomically move the disabled BuildSpecs guard to R2, update `RuntimeInbox/ACTIVE_BUILD.txt` to R2, create/update the R2 candidate/project-state and artifact-integrity authorities, set `active_candidate = S1.42AI-DIAG1R2`, and only then set `runtime_test_outstanding = true`. Do not import R2 into Gale or request gameplay before that transition is merged and Exact-HEAD validated.
