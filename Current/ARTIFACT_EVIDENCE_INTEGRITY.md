<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1 candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-14

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact / failed diagnostic: S1.42AI-DIAG1

Artifact: `Profiles/LC V1 S1.42AI-DIAG1 ShyGuy Isolation.r2z`  
SHA-256: `22e2132669a790756f2a1e2bd10b14fd05144b3ecdd55233d8d57f1d6dd9f3fd`  
Candidate record: `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`  
Runtime failure: `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1/20260913T202638Z/`  
Runtime log SHA-256: `0125f1ff1f16b99fa2531374bbfbc1a1294ec4918b22e67aed804ad1e41ebe49`  
Project status: `Current/Projektstatus_S1.42AI-DIAG1_CANDIDATE.json`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1/`  
Plugin DLL SHA-256: `bc8d51121451ecd1b1550e2aa6007991983c7a88ad93c86c38541ec0d358a2b3`

S1.42AI-DIAG1 now has an explicit failed diagnostic runtime decision and is indexed as completed failed evidence, not as `ACTIVE_RUNTIME_CANDIDATE_PENDING`.

## Deferred full-normal S1.42AI gate

S1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic repair path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
