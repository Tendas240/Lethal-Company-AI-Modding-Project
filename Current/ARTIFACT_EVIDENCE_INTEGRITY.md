<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=S1.42AI-DIAG1R2 runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact / active runtime candidate: S1.42AI-DIAG1R2

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z`  
SHA-256: `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`  
Candidate record: `Current/148_S1.42AI-DIAG1R2_BUILD_CANDIDATE_ENDLESS_ELEVATOR_APPLICABILITY_REPAIR.md`  
Project status: `Current/Projektstatus_S1.42AI-DIAG1R2_CANDIDATE.json`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R2/`  
Plugin DLL SHA-256: `099a54571dc0595638fbd2f338c67137f42734b8aedf80478005dff314a0a3b3`  
Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md`  
Runtime evidence required now: **yes, pending upload after gameplay**.

The machine index records R2 as `ACTIVE_RUNTIME_CANDIDATE_PENDING` with `runtime_evidence_required=false` until a final runtime decision exists; this sentinel means runtime evidence is intentionally deferred at the artifact-integrity layer, not that gameplay evidence is unnecessary.

## Failed predecessor diagnostics

S1.42AI-DIAG1 and S1.42AI-DIAG1R1 remain preserved as completed failed diagnostic evidence. R1 failure authority is `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md` with runtime evidence under `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the R2 diagnostic decision.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
