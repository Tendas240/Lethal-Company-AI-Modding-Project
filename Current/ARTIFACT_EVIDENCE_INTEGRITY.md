<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R1 candidate=S1.42AI-DIAG1R1 runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-14

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact / active runtime candidate: S1.42AI-DIAG1R1

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R1 ShyGuy Isolation Repair.r2z`  
SHA-256: `b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd`  
Candidate record: `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`  
Project status: `Current/Projektstatus_S1.42AI-DIAG1R1_CANDIDATE.json`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R1/`  
Plugin DLL SHA-256: `2d1b6e8a002eb55e0e6d935e36c0a619d1c875651b94afb9e748663af93c1de0`  
Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R1/MATERIALIZED_VALIDATION.md`  
Runtime evidence required now: **yes, pending upload after gameplay**.

The machine index records R1 as `ACTIVE_RUNTIME_CANDIDATE_PENDING` with `runtime_evidence_required=false` until a final runtime decision exists; this sentinel means runtime evidence is intentionally deferred at the artifact-integrity layer, not that gameplay evidence is unnecessary.

## Failed predecessor diagnostic

S1.42AI-DIAG1 remains preserved as completed failed diagnostic evidence under `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md` and `RuntimeEvidence/S1.42AI-DIAG1/20260913T202638Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the R1 diagnostic decision.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
