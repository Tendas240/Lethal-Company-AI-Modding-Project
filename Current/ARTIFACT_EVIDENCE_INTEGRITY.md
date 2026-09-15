<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact: S1.42AI-DIAG1R2 — runtime failed diagnostic

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z`
SHA-256: `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`
Candidate record: `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`
Runtime failure: `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/`
Runtime log SHA-256: `6d913ac6788c72b7c2afb5092297a9070f5efb44bc33053d1ff6869a72019232`
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R2/`
Plugin DLL SHA-256: `099a54571dc0595638fbd2f338c67137f42734b8aedf80478005dff314a0a3b3`

R2 is now a completed `RUNTIME_FAILED_DIAGNOSTIC_REPAIR_REQUIRED` entry. Its owner/applicability repairs armed, but its exact identity classifier used `enemyName = Shy Guy` while runtime proves `Shy guy`; the resulting ShyGuy bypass markers are false-positive diagnostic classification.

## Prepared successor — no artifact yet

`S1.42AI-DIAG1R3` is determined by `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`. The source/static-gate identity repair is prepared, but no R3 profile, DLL SHA, runtime candidate or runtime test exists yet. `BuildSpecs/current.json` remains disabled.

## Earlier failed diagnostics

S1.42AI-DIAG1, S1.42AI-DIAG1R1 and S1.42AI-DIAG1R2 remain preserved as completed failed diagnostic evidence and must not be rerun unchanged.

## Deferred full-normal S1.42AI gate

S1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic repair path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
