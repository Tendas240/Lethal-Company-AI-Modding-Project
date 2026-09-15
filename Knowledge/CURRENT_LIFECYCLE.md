<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`, `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md`, `AnalysisEvidence/S1.42AI-DIAG1R3/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json`, `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`  
Build request: `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`  
Build workflow run: `35021307391` (`workflow_dispatch`, success)  
Build commit: `19914cff25cb768cffe22694e93df150e45bdd2f`  
Canonical post-build validation: `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md` / run `35023265624` (`push`, success)

R3 was built directly from exact full-normal S1.42AI, not from failed R2 bytes. The persisted validation proves the exact runtime identity `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` with `StringComparison.Ordinal`, preserves metadata-derived LethalMin owner resolution and dependency-absent EndlessElevator `NOT_APPLICABLE` handling, and proves decompiled C# plus normalized IL semantic equivalence to the repaired SDK8 green gate.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R3**, verified but not accepted.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R3_MATERIALIZED_VALIDATION_AWAITING_RUNTIME_CANDIDATE_ACTIVATION` and guards accepted S1.42AH.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R2` remains evidence attribution for the last completed failed R2 run; it is not acceptance authority and does not authorize gameplay.

## Canonical Gale workflow

Whenever R3 or any later runtime candidate is actually armed, import/replace it only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` using canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. There is no active runtime candidate now, so this routing rule does not authorize a gameplay run by itself.

## R2 history and R3 repair

R2 remains a completed failed diagnostic under `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md` / `RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/`. It proved the metadata-derived owner and EndlessElevator applicability repairs at runtime, then rejected the real ShyGuy only because its exact ordinal `enemyName` literal was `Shy Guy` instead of runtime `Shy guy`. R3 repairs only that literal and preserves the exact fail-closed identity triple and all predecessor guards.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate remains mandatory and is **deferred, not waived**. Diagnostic success cannot accept the full-normal candidate.

## Exact next project action

Perform a **separate coordinated R3 runtime-candidate activation transition**. Re-verify exact R3 profile/evidence and no-candidate state, then atomically move the disabled BuildSpecs guard to R3, update `RuntimeInbox/ACTIVE_BUILD.txt` to R3, create/update the R3 candidate/project-state and artifact-integrity authorities, set `active_candidate = S1.42AI-DIAG1R3`, and only then set `runtime_test_outstanding = true`. Do not import R3 into Gale or request gameplay before that transition is merged and Exact-HEAD validated.
