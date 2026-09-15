<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

## Latest built artifact: S1.42AI-DIAG1R2

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z`  
SHA-256: `9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15`  
Build request: `BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R2/`  
FILE_INDEX: `ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json`  
Build workflow run: `34958254886`  
Build commit: `854e4435676ef32648407dae9ba1e2e704a420d1`  
Canonical materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md` / `AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.json`  
Materialized EndlessElevator applicability: `AnalysisEvidence/S1.42AI-DIAG1R2/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json`  
Validation workflow run: `34990530260`

R2 is built and verified but has **no runtime decision yet** and is **not an active candidate yet**. The machine index continues to classify runtime-decided profiles and runtime-pending candidates; R2 enters the pending-candidate section only in the later coordinated activation transition. Exact R2 artifact/snapshot/materialized evidence is already repository-readable.

## Completed failed diagnostic predecessor: S1.42AI-DIAG1R1

R1 remains preserved as completed failed diagnostic evidence under `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `ProfileSources/S1.42AI-DIAG1R1/`, and `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`.

## Failed predecessor diagnostic

S1.42AI-DIAG1 remains preserved under `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md` and `RuntimeEvidence/S1.42AI-DIAG1/20260913T202638Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
