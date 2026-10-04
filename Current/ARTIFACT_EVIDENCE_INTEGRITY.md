<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-10-04

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

## Completed diagnostic evidence: S1.42AK-BMGHDIAG3

Profile: `Profiles/LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic.r2z`
SHA-256: `7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace`
Diagnostic DLL SHA-256: `d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352`
Readable snapshot: `ProfileSources/S1.42AK-BMGHDIAG3/`
Runtime evidence: `RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/`
Runtime log SHA-256: `e30858fcebce0fc51f092170b50bd439290cf4752bf0917ae28d66e29a37a9f8`
Decision: `Current/199_S1.42AK_BMGHDIAG3_RUNTIME_COMPATIBILITY_PASS.md`

The exact diagnostic passed the bounded Black Mesa x Greenhouse runtime-compatibility contract: exact selection at normalized rarity 100, completed generation, topology IDs 0..3, and direct bidirectional traversal of all four IDs in run 2. The user's manual observation additionally reported accessible required entrance geometry without severe clipping or persistent routing/NavMesh failure. RuntimeNavMeshBuilder Error-severity source-mesh messages remain documented as a non-blocking observation for this gate. BMGHDIAG3 is completed diagnostic evidence only / NEVER ACCEPT.

## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.
- **S1.42AK-BMDSFIX1** — active gameplay candidate directly over accepted S1.42AK; profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`; its regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding/unwaived; not accepted.
- **S1.42AK-BMDSFIX1-DIAG1** — preserved preloader-blocked diagnostic parent; profile SHA-256 `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`; must not be rerun and is not the active runtime/evidence target.
- **S1.42AK-BMDSFIX1-DIAG1PATH1** — completed supporting diagnostic evidence using short identity `LC V1 S1.42AK-D1P1`; profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; not runtime-active and never a gameplay base or acceptance candidate.
- **S1.42AK-BMAFDIAG1** — preserved preloader-blocked diagnostic parent; profile SHA-256 `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2`; exact 260/262-character critical-path block; **DO NOT RERUN / DIAGNOSTIC ONLY / NEVER ACCEPT**.
- **S1.42AK-BMAFDIAG1PATH1** — completed failed config-binding diagnostic provenance; profile SHA-256 `423e2e5185c85c1a3ce7a100583717d3503cf7308a12a182f5f7f65dc501ff91`; **DO NOT RERUN / DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**.
- **S1.42AK-BMAFR1** — completed Black Mesa x Abandoned Foundry runtime-compatibility diagnostic; profile SHA-256 `8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5`; repaired Foundry LLL config SHA-256 `d2a01df4829623ef3dcbacf8c09e98a9c6a72b0885f9302502da2bcb91b31b68`; reused diagnostic DLL SHA-256 `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`; supplemental runtime evidence `RuntimeEvidence/S1.42AK-BMAFR1/20261002T164741Z/` / raw log SHA-256 `ca2d83a56115f66623c3dfb38d2cdd47085b3c0a368efc3ace29321a323b4d90` reaches final bidirectional IDs 0..3 coverage. Separate 6696-array-index-error / degraded-frame-rate finding remains attribution-outstanding; **DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**.
- **S1.42AK-BMAFR1I1** — completed inconclusive performance-attribution diagnostic over completed BMAFR1; profile SHA-256 `734dbe491b4f4fb77704472a303e386058e976325e0595dc4795af1940d1cb07`; instrumentation DLL SHA-256 `d9e09b20a889260d5cc8b4970d023a76d5b7af77ad677077b9718dfa8a150b6a`; runtime evidence `RuntimeEvidence/S1.42AK-BMAFR1I1/20261003T232317Z/` / raw log SHA-256 `0f28ad24f0279cd18a039bc4e1de695e9590d1c70e98d2a6a2aa318b30674ce3`; instrumentation ARMED, exact array signature count 0, required Janitor/SpringMan target-instance comparison not observed; **DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**.

BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. The BMAFR1 entrance/topology diagnostic remains a pair-specific runtime-compatibility PASS / NEVER ACCEPT. The subsequent BMAFR1I1 attribution run is complete but inconclusive: the flood did not recur and the required Janitor/SpringMan comparison instances were not observed. Runtime/evidence routing is back on exact `S1.42AK-BMDSFIX1`; `BuildSpecs/current.json` remains disabled and `Current/AUTO_BUILD_RESULT.json` remains BMDSFIX1. The BMDSFIX1 Deep Sewers target gate remains passive/outstanding/unwaived.

## Completed diagnostic evidence: S1.42AI-DIAG1R3

R3 remains completed diagnostic-pass evidence only. It is not a gameplay baseline and does not replace the full-normal S1.42AI acceptance evidence.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
