<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AK candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-18

## Accepted gameplay baseline: S1.42AI

Artifact: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

## Latest built artifact: S1.42AK

Artifact: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Plan: `BuildSpecs/S1.42AK_PLAN.md`  
Static evidence: `BuildSpecs/S1.42AK_BUILD_EVIDENCE/STATIC_VERIFICATION.md`  
Readable snapshot: `ProfileSources/S1.42AK/`

S1.42AK is statically validated but not accepted and not yet runtime-active. There is currently no active runtime candidate and no runtime test outstanding.

## Balanced parent and diagnostic evidence

S1.42AJ remains the exact balanced parent for S1.42AK and is not accepted. S1.42AJ-DIAG1 and S1.42AJ-DIAG2 remain diagnostic-only evidence; they are not gameplay bases.

## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained balanced parent, not active.
- **S1.42AK** — deferred full-normal gate until the explicit runtime-activation segment, not active yet.

## Completed diagnostic evidence: S1.42AI-DIAG1R3

R3 remains completed diagnostic-pass evidence only. It is not a gameplay baseline and does not replace the full-normal S1.42AI acceptance evidence.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
