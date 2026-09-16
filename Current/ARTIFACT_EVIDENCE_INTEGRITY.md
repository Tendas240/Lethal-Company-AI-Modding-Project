<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-16

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

## Completed diagnostic evidence: S1.42AI-DIAG1R3

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`  
Decision: `Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R3/20260916T161243Z/`  
Raw runtime log SHA-256: `37493170b9f6368bc4700161b8f0759ffaaff57925aed9784bec9a9a65c68084`

R3 is completed diagnostic-pass evidence, not a gameplay base. It proves exact ShyGuy identity resolution and ShyGuy-only isolation. Interior visibility was positively observed. Exterior visibility is **NOT_EXERCISED_NO_EXTERIOR_SHYGUY_OBSERVED**.

## Latest built artifact / active full-normal runtime candidate: S1.42AI

Artifact: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Candidate: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Readable snapshot: `ProfileSources/S1.42AI/`

The machine index records S1.42AI as `ACTIVE_RUNTIME_CANDIDATE_PENDING` with `runtime_evidence_required=false` until a final full-normal runtime decision exists. That sentinel does not make the gameplay gate optional.

## Completed failed diagnostic predecessors

DIAG1, DIAG1R1 and DIAG1R2 remain preserved as explicit failed diagnostic evidence. R3 supersedes their repair questions; they must not be rerun unchanged.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
