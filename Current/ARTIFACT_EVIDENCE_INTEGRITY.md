<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-17

## Accepted gameplay baseline: S1.42AI

Artifact: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`  
Raw runtime log SHA-256: `1765a2b65cfa31da049ba415938119f9eb3690d09618a2f85a32209bfad6d9b5`

S1.42AI is now a completed accepted profile in the machine index. S1.42AH remains its accepted predecessor/rollback provenance baseline.

## Latest built artifact: S1.42AJ — static validated / runtime not armed

Artifact: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`  
Profile sources: `ProfileSources/S1.42AJ/`  
Static evidence: `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`

S1.42AJ has no runtime evidence yet and is not an active runtime candidate. It is therefore not listed under `pending_profiles` until a later explicit runtime-arming transition. S1.42AI remains the accepted completed gameplay profile.

## Completed diagnostic evidence: S1.42AI-DIAG1R3

Artifact: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`  
Decision: `Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI-DIAG1R3/20260916T161243Z/`  
Raw runtime log SHA-256: `37493170b9f6368bc4700161b8f0759ffaaff57925aed9784bec9a9a65c68084`

R3 remains completed diagnostic-pass evidence only. It proves exact ShyGuy identity resolution and ShyGuy-only isolation; it is not a gameplay baseline and does not replace the full-normal S1.42AI acceptance evidence.

## Completed failed diagnostic predecessors

DIAG1, DIAG1R1 and DIAG1R2 remain preserved as explicit failed diagnostic evidence. R3 supersedes their repair questions; they must not be rerun unchanged.

## Pending runtime candidates

None. `pending_profiles` is empty. No new runtime test is outstanding.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
