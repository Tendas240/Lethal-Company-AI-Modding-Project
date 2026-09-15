<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

## Latest built artifact: S1.42AI-DIAG1R3

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`  
Build request: `BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R3/`  
FILE_INDEX: `ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json`  
Build workflow run: `35021307391`  
Build commit: `19914cff25cb768cffe22694e93df150e45bdd2f`  
Plugin DLL SHA-256: `98b464e559120dc43e8041f163ceab038506e045f4b3cd4c71be8687e9c5da7a`  
Canonical materialized validation: `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md` / `AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.json`  
Materialized EndlessElevator applicability: `AnalysisEvidence/S1.42AI-DIAG1R3/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json`  
Validation workflow run: `35023265624`

R3 is built and verified but has **no runtime decision yet** and is **not an active candidate yet**. The machine index continues to classify runtime-decided profiles and runtime-pending candidates; R3 enters `pending_profiles` only in the later coordinated activation transition. Exact R3 artifact/snapshot/materialized evidence is already repository-readable.

## Completed failed diagnostic predecessor: S1.42AI-DIAG1R2

R2 remains preserved as completed failed diagnostic evidence under `Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md`, `ProfileSources/S1.42AI-DIAG1R2/`, and `RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/`.

## Earlier failed diagnostics

S1.42AI-DIAG1 and S1.42AI-DIAG1R1 remain preserved as completed failed diagnostic evidence and must not be rerun unchanged.

## Deferred full-normal S1.42AI gate

S1.42AI remains `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
