<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=S1.42AI-DIAG1R3 runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-16

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact / active runtime candidate: S1.42AI-DIAG1R3

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`  
Candidate record: `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`  
Project status: `Current/Projektstatus_S1.42AI-DIAG1R3_CANDIDATE.json`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R3/`  
Plugin DLL SHA-256: `98b464e559120dc43e8041f163ceab038506e045f4b3cd4c71be8687e9c5da7a`  
Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md`  
Runtime evidence required now: **yes, pending upload after gameplay**.

The machine index records R3 as `ACTIVE_RUNTIME_CANDIDATE_PENDING` with `runtime_evidence_required=false` until a final runtime decision exists; this artifact-integrity sentinel means no completed runtime evidence is required yet, not that the gameplay gate is optional.

## Completed failed predecessor: S1.42AI-DIAG1R2

R2 remains preserved as completed failed diagnostic evidence under `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md` and `RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
