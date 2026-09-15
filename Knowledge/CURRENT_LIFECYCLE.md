<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action
**Evidence:** `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`, `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`, `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`, `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**. S1.42AH remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — RUNTIME DIAGNOSTIC FAILED / NOT ACCEPTED**
Profile: `Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z`
SHA-256: `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`
Failure: `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/`

R2 proved the repaired metadata-derived LethalMin owner path and the dependency-absent EndlessElevator `NOT_APPLICABLE` path arm without DIAG1 install rollback. It then failed exact ShyGuy identity resolution because the diagnostic required ordinal `enemyName = "Shy Guy"` while the real runtime object is `ShyGuyDef/Shy guy` with AI type `ShyGuy.AI.ShyGuyAI`. Every R2 isolation-bypass marker identifies that exact ShyGuy object, so this is a diagnostic identity-classification failure, not evidence that another enemy bypassed the allowlist.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R2**, failed diagnostic evidence.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI-DIAG1R2_RUNTIME_FAILURE_R3_PREPARED_NOT_ARMED`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R2` remains runtime/evidence attribution only and is not acceptance authority.
- Prepared successor: **S1.42AI-DIAG1R3**, not built and not a runtime candidate.

Canonical Gale runtime replacement/import route: `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, pinned helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`.

## R3 successor boundary

`BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md` binds the smallest exact repair: `ExpectedEnemyName = "Shy guy"` while preserving exact `ShyGuyDef`, `ShyGuy.AI.ShyGuyAI`, `StringComparison.Ordinal`, reference-equality allowlisting, all existing spawn-owner guards, the metadata-derived owner repair, and the EndlessElevator applicability contract. The static gate now rejects the known-bad `"Shy Guy"` capitalization. No broader case-insensitive/substring/alias identity is allowed.

There is **no gameplay test to run now**. R3 must first be built repository-native from exact full-normal S1.42AI, then pass compile/static/archive/materialized validation, and only a later coordinated lifecycle transition may activate it and set `runtime_test_outstanding=true`.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md` remains mandatory and is **deferred, not waived**. Diagnostic work cannot replace it.

## Exact next project action

Perform a separate coordinated R3 build-controller transition from exact S1.42AI using `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`. Do not run gameplay before a built and repository-natively verified R3 artifact is explicitly activated.
