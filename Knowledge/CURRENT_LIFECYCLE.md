<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AK candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`, `Current/154_S1.42AJ_DIAG1_LC_OFFICE_RUNTIME_PERFORMANCE_FINDING.md`, `Current/155_S1.42AJ_DIAG2_LC_OFFICE_CAMERA_RENDER_PARTIAL_FINDING.md`, `Current/156_S1.42AJ_DIAG2_LC_OFFICE_CAMERA_RENDER_CONFIRMATION_AND_S1.42AK_SUCCESSOR_DECISION.md`, `RuntimeEvidence/S1.42AJ-DIAG2/20260918T153753Z/`, `BuildSpecs/S1.42AK_PLAN.md`  
**Last-Validated:** 2026-09-18

## Accepted gameplay baseline

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`

## Balanced lifecycle candidate

**S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / NOT ACCEPTED BALANCED PARENT** remains the exact balanced parent used for S1.42AK. It is not the active runtime candidate.

Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`

The first full-normal Offense evidence at `RuntimeEvidence/S1.42AJ/20260917T171109Z/` proves ordinary LC Office viability at author rarity `65` and final normalized effective rarity `100`. That run selected Facility, so actual Office generation was obtained later through DIAG1.

## Diagnostic parent evidence

**S1.42AJ-DIAG1 — LC Office force-selection diagnostic — RUNTIME EVIDENCE INGESTED / NOT ACCEPTED** is now the explicit diagnostic parent for DIAG2.

Profile SHA-256: `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`  
Runtime evidence: `RuntimeEvidence/S1.42AJ-DIAG1/20260917T204918Z/`  
Log SHA-256: `bb81a91f2cabcb1a3b010dd988335cc9c9cb0b5bcc9bd646ee2ac18ccbb15a26`

DIAG1 successfully generated LC Office on Offense. During that run the user observed later-day stutter at roughly 3–4 hitches per second. Comparison with accepted S1.42AI downgraded the initial NavMesh-error hypothesis. The remaining narrow A/B hypothesis is LC Office's periodic camera-render path.

## Diagnostic runtime conclusion

**S1.42AJ-DIAG2 — LC Office Camera Render Diagnostic — CONFIRMATION RUNTIME EVIDENCE INGESTED / POSITIVE A/B COMPLETE / NOT ACCEPTED** is complete as diagnostic evidence.

Confirmation runtime evidence: `RuntimeEvidence/S1.42AJ-DIAG2/20260918T153753Z/`  
Confirmation log SHA-256: `f347b1ca20ddc82d0fe93a5ca8c536fd7c116061a9080f4711f6bf2ac924329b`  
Canonical confirmation/decision: `Current/156_S1.42AJ_DIAG2_LC_OFFICE_CAMERA_RENDER_CONFIRMATION_AND_S1.42AK_SUCCESSOR_DECISION.md`

The longer confirmation run covered roughly twelve minutes after LC Office generation, exceeded the DIAG1 comparison window, and the user again reported that the characteristic repeated DIAG1 stutter was absent. Men-stalker and Aloe both spawned from interior vents, repeated elevator operation occurred, and the log planned 15 scrap objects. The user separately reported isolated frame drops near Men-stalker and continued to perceive scrap as sparse or poorly distributed.

The combined A/B is sufficient for this project to carry `Camera Frame Speed = 0` into the next balanced successor, without claiming universal causal proof.

## Built balanced successor

**S1.42AK — LC Office Camera Enemy Balance — BUILT / STATIC VALIDATED / NOT ACCEPTED / NOT YET RUNTIME-ACTIVE** was built directly from exact S1.42AJ, never from DIAG1 or DIAG2.

Profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Plan: `BuildSpecs/S1.42AK_PLAN.md`  
Static verification: `BuildSpecs/S1.42AK_BUILD_EVIDENCE/STATIC_VERIFICATION.md`  
Successful build run: `35366580975`.

Authorized delta only:
- LC Office `[General] Camera Frame Speed = 0`;
- disable exact `YaBoiDucki-men_stalker 3.1.2`;
- Biodiversity Aloe `[SpawnSettings] PowerLevel = 0`;
- preserve RandomEnemiesSize and all unrelated settings unchanged.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest built balanced artifact: **S1.42AK** — static validated, not accepted, not yet runtime-active.
- Balanced parent: **S1.42AJ** — not accepted; retained as exact S1.42AK lineage parent.
- Diagnostic evidence target: **S1.42AJ-DIAG2** — confirmation complete, diagnostic-only, not accepted.
- Active runtime candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled and guards the accepted S1.42AI baseline between atomic build operations.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` remains only an idle evidence-attribution pointer; no runtime test is pending.

## Exact next project action

Activate **S1.42AK** as the explicit full-normal runtime candidate in one repository-native lifecycle update. Do not call it accepted before runtime evidence. The response that releases that test must include the repository-driven Gale replacement/import one-liner and the exact S1.42AK autonomous PowerShell log uploader.

## Scope boundary

Universal-moon availability, general Interior viability work, Wesley, CullFactory, DunGenReferenceFixer and unrelated Interior changes remain out of scope for this A/B.

## Canonical Gale runtime import helper

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. The resolver remains fail-closed: a normal target must match `AUTO_BUILD_RESULT`; a direct diagnostic must bind exactly to that balanced result; and a second-generation diagnostic is permitted only when `CURRENT_STATE.selected_scope.diagnostic_parent_revision` identifies one exact published parent whose own base binds directly to `AUTO_BUILD_RESULT`. `AUTO_BUILD_RESULT` now identifies S1.42AK, so the earlier DIAG2 chain is retained as completed historical diagnostic evidence rather than a current runtime target. The helper does not allow an arbitrary diagnostic chain.
