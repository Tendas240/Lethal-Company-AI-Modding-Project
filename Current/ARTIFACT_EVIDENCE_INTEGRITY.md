<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-24

## Accepted gameplay baseline: S1.42AK

Artifact: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Acceptance: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`  
Runtime evidence: `RuntimeEvidence/S1.42AK/20260918T172838Z/`  
Runtime log SHA-256: `cc0f0a7a6c6a76ad44266aded11ff9cb2aca21f2623f5fb895d371ad778526b9`  
Readable snapshot: `ProfileSources/S1.42AK/`

S1.42AI remains the accepted predecessor/rollback provenance baseline.

## Completed diagnostic evidence: S1.42AK-SCRAPDIAG1

Profile: `Profiles/LC V1 S1.42AK-SCRAPDIAG1 LC Office Scrap Placement Diagnostic.r2z`  
SHA-256: `233bcc058a3fa95d63e0577c4ff74b5a0dc137db49757b50376e447dd082d3b1`  
Readable snapshot: `ProfileSources/S1.42AK-SCRAPDIAG1/`  
Runtime evidence: `RuntimeEvidence/S1.42AK-SCRAPDIAG1/20260918T200602Z/`  
Runtime log SHA-256: `e32e7d9b858fd78c046d5206c519a7709b3dcd5b2b8c432500233f51c6f13348`  
Decision: `Current/163_S1.42AK_SCRAPDIAG1_RUNTIME_PLACEMENT_FINDING.md`

The diagnostic passed its placement-capture contract and closed the LC Office scrap investigation with no gameplay delta. It remains diagnostic evidence only and is not a gameplay baseline.

## Completed failed diagnostic evidence: S1.42AK-BMGHDIAG1

Profile: `Profiles/LC V1 S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic.r2z`  
SHA-256: `7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90`  
Readable snapshot: `ProfileSources/S1.42AK-BMGHDIAG1/`  
Runtime evidence: `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`  
Runtime log SHA-256: `4f3dae931364cefc4b297c8c316502e96d32b27431467a5607ce69ed6d6e69ef`  
Decision: `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`

The diagnostic refused before arming because the loaded `Assembly-CSharp.dll` could not be hashed. Normal Black Mesa LLL evidence still proves Greenhouse viable at effective rarity 100, but actual selection was Decrepit store; Black Mesa x Greenhouse therefore remains unqualified and the diagnostic requires repair analysis. It is not runtime-active and is never a gameplay base.

## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.
- **S1.42AK-BMGHDIAG2** — active diagnostic runtime target over accepted S1.42AK; exact profile SHA-256 `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2`; runtime evidence outstanding; not accepted and not a gameplay base.

## Completed diagnostic evidence: S1.42AI-DIAG1R3

R3 remains completed diagnostic-pass evidence only. It is not a gameplay baseline and does not replace the full-normal S1.42AI acceptance evidence.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
