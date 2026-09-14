<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R1 candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-14

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Latest built artifact / completed failed diagnostic: S1.42AI-DIAG1R1

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R1 ShyGuy Isolation Repair.r2z`  
SHA-256: `b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd`  
Candidate record: `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md`  
Runtime failure: `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`  
Project status: `Current/Projektstatus_S1.42AI-DIAG1R1_CANDIDATE.json`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R1/`  
Plugin DLL SHA-256: `2d1b6e8a002eb55e0e6d935e36c0a619d1c875651b94afb9e748663af93c1de0`  
Materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R1/MATERIALIZED_VALIDATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`  
Runtime log SHA-256: `173eefaea3a81f84e82f210066a2b034655220d951b5a66c7bb7614895737635`

R1 is completed failed diagnostic evidence, not an active runtime candidate. Runtime proved the metadata-derived LethalMin owner type repair works, then exposed the missing required complex-owner type `ElevatorMod.Patches.EndlessElevator`; DIAG1 invalidated and rolled back all owned Harmony hooks.

## Failed predecessor diagnostic

S1.42AI-DIAG1 remains preserved as completed failed diagnostic evidence under `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md` and `RuntimeEvidence/S1.42AI-DIAG1/20260913T202638Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains preserved as `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic repair path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
