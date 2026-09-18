<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AK candidate=S1.42AK runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-18

## Accepted gameplay baseline: S1.42AI

Artifact: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

## Active runtime candidate: S1.42AK

Artifact: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Candidate: `Current/157_S1.42AK_BUILD_CANDIDATE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`  
Project status: `Current/Projektstatus_S1.42AK_CANDIDATE.json`  
Plan: `BuildSpecs/S1.42AK_PLAN.md`  
Static evidence: `BuildSpecs/S1.42AK_BUILD_EVIDENCE/STATIC_VERIFICATION.md`  
Readable snapshot: `ProfileSources/S1.42AK/`

S1.42AK is statically validated and is the active full-normal runtime candidate. It is not accepted. Fresh runtime evidence is outstanding.

## Balanced parent and diagnostic evidence

S1.42AJ remains the exact balanced parent for S1.42AK and is not accepted. S1.42AJ-DIAG1 and S1.42AJ-DIAG2 remain completed diagnostic-only evidence and are not gameplay bases.

## Pending / deferred unaccepted profiles

- **S1.42AK** — `ACTIVE_RUNTIME_CANDIDATE_PENDING`; fresh full-normal evidence required before an explicit decision.
- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.

## Completed diagnostic evidence: S1.42AI-DIAG1R3

R3 remains completed diagnostic-pass evidence only. It is not a gameplay baseline and does not replace the full-normal S1.42AI acceptance evidence.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
