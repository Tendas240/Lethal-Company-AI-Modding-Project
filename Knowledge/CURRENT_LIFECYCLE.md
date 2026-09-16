<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=S1.42AI-DIAG1R3 runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`, `Current/Projektstatus_S1.42AI-DIAG1R3_CANDIDATE.json`, `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`, `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md`, `AnalysisEvidence/S1.42AI-DIAG1R3/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json`, `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** 2026-09-16

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Latest built artifact and active candidate

**S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`  
Candidate: `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`  
Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md`

R3 was built directly from exact full-normal S1.42AI. Canonical validation proves the exact runtime identity `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` with `StringComparison.Ordinal`, preserves the metadata-derived LethalMin owner repair and dependency-absent EndlessElevator `NOT_APPLICABLE` path, and proves decompiled C# plus normalized IL semantic equivalence to the repaired green gate.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R3**.
- Active candidate: **S1.42AI-DIAG1R3**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R3_BUILD_AWAITING_RUNTIME`; no successor build is armed during the runtime gate.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R3` controls attribution for the next uploaded runtime log and is not acceptance authority.
- `Current/AUTO_BUILD_RESULT.json.build_id = S1.42AI-DIAG1R3` identifies the exact built candidate.

## Canonical Gale workflow

Import/replace the active R3 profile only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` using canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The ready-to-test command is recorded in `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md` together with the exact R3 log uploader.

## Exact runtime gate

Run one R3 diagnostic profile. Require owner derivation, dependency-absent EndlessElevator `NOT_APPLICABLE`, and all guard layers to arm without DIAG1 invalidation/rollback; require the real exact ShyGuy identity to resolve without the R2 identity failure; no live non-ShyGuy isolation bypass or unexpected non-ShyGuy enemy may appear. ShyGuy must remain visibly observable, and exterior visibility is only considered exercised if an exterior ShyGuy is actually encountered.

Operator-visible confirmations for this run are: **(1)** no enemy other than ShyGuy spawns/appears while isolation is armed; **(2)** an exterior ShyGuy, when present, is visible rather than invisible. An interior ShyGuy not following the player outside is separately explained by inherited `Can Exit Facility = false` and is not this diagnostic's failure condition.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate remains mandatory and is **deferred, not waived**. R3 diagnostic success cannot replace it.

## Exact next project action

Perform one R3 diagnostic gameplay run, explicitly record the two operator-visible confirmations above, then upload the complete fresh R3 log for repository-native ingestion and decision. If no exterior ShyGuy is encountered, report exterior visibility as not exercised rather than passed.
