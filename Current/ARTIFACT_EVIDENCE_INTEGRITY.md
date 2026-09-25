<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-25

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

The diagnostic refused before arming because the loaded `Assembly-CSharp.dll` could not be hashed. Normal Black Mesa LLL evidence still proves Greenhouse viable at effective rarity 100, but actual selection was Decrepit store; Black Mesa x Greenhouse therefore remains unqualified. It is not runtime-active and is never a gameplay base.

## Completed failed diagnostic evidence: S1.42AK-BMGHDIAG2

Profile: `Profiles/LC V1 S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic.r2z`  
SHA-256: `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2`  
Readable snapshot: `ProfileSources/S1.42AK-BMGHDIAG2/`  
Runtime evidence: `RuntimeEvidence/S1.42AK-BMGHDIAG2/20260924T124542Z/`  
Runtime log SHA-256: `5c7931cbf68414c76ea4cc0950d23b592497a2daa2b0f4d8e49986cc13c863d9`  
Decision: `Current/173_S1.42AK_BMGHDIAG2_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL_AND_DEEP_SEWERS_INCIDENT.md`

BMGHDIAG2 loaded but refused before arming with `EntranceTeleport manifest module identity mismatch`; Black Mesa x Greenhouse therefore remains `NOT_YET_PROVEN`. The same normal-fallback session separately exposes the Black Mesa x Deep Sewers 4.875-size generation incident that motivates the source/static-only BMDSFIX1 repair. BMGHDIAG2 is not runtime-active and is never a gameplay base.

## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.
- **S1.42AK-BMDSFIX1** — active gameplay runtime candidate directly over accepted S1.42AK; profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`; BMDSFIX1 DLL SHA-256 `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`; runtime evidence outstanding; not accepted.
- **S1.42AK-BMDSFIX1-DIAG1** — preserved preloader-blocked diagnostic parent; profile SHA-256 `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`; DIAG1 DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; must not be rerun and is not the active runtime/evidence target.
- **S1.42AK-BMDSFIX1-DIAG1PATH1** — active diagnostic runtime/evidence target using short identity `LC V1 S1.42AK-D1P1`; profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; inherited DIAG1 selector DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; supporting deterministic Deep Sewers evidence only; never a gameplay base or acceptance candidate.

BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. `RuntimeInbox/ACTIVE_BUILD.txt` now points to exact DIAG1PATH1 solely for Gale target resolution and diagnostic evidence attribution; blocked long-name DIAG1 is retained only as the one-hop parent and must not be rerun. Activation changes only lifecycle/controller/evidence routing and regenerates no gameplay/config/package/profile/plugin bytes. DIAG1PATH1 may supply supporting deterministic Black Mesa x `DeepSewersFlow` evidence but cannot qualify or accept BMDSFIX1. Black Mesa x Greenhouse remains separate and unproven.

## Completed diagnostic evidence: S1.42AI-DIAG1R3

R3 remains completed diagnostic-pass evidence only. It is not a gameplay baseline and does not replace the full-normal S1.42AI acceptance evidence.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
