<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `RuntimeEvidence/S1.42AK/20260918T172838Z/RUNTIME_ACCEPTANCE_DECISION.md`, `Current/157_S1.42AK_BUILD_CANDIDATE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`, `BuildSpecs/S1.42AK_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `Current/156_S1.42AJ_DIAG2_LC_OFFICE_CAMERA_RENDER_CONFIRMATION_AND_S1.42AK_SUCCESSOR_DECISION.md`, `BuildSpecs/LC_OFFICE_SCRAP_INVESTIGATION_PLAN.md`, `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md`, `Current/160_LC_OFFICE_SCRAP_PLACEMENT_DIAGNOSTIC_DESIGN.md`, `BuildSpecs/S1.42AK-SCRAPDIAG1_PLAN.md`, `Current/161_S1.42AK_SCRAPDIAG1_STATIC_VALIDATION_CLEARANCE.md`, `BuildSpecs/S1.42AK-SCRAPDIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `BuildSpecs/S1.42AK-SCRAPDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`, `Current/162_S1.42AK_SCRAPDIAG1_RUNTIME_ACTIVATION.md`  
**Last-Validated:** 2026-09-18

## Accepted gameplay baseline

**S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK** is the sole current accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Acceptance: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`  
Runtime evidence: `RuntimeEvidence/S1.42AK/20260918T172838Z/`

S1.42AI remains the accepted predecessor and rollback provenance baseline.

## Acceptance result

S1.42AK passed its full-normal Offense gate. The uploaded session contains two runs: the first was aborted shortly after landing before interior entry; the second naturally selected `Spooky manor` and was played inside for roughly three minutes until the user died.

The user saw no hostile indoor enemy during the played Spooky Manor window. This is a coverage limitation, not a proven spawn regression. The log still proves normal stack startup/gameplay flow, ordinary exterior enemy activity, normal Interior Weight Normalization, interior generation, scrap generation/interactions and zero project-critical markers named by the candidate gate.

Men-stalker produced no package/runtime/spawn signature, consistent with the verified disabled state. Aloe remained registered without a new runtime regression; an Aloe spawn was not required. LC Office was not naturally selected, which is explicitly valid under the candidate contract because the completed S1.42AJ-DIAG2 A/B already provides deterministic LC Office generation, repeated elevator operation and the camera-render comparison.

The one-shot LethalMin `PiggyMetalDetectorPatch` failure is retained as real compatibility evidence. The identical signature predates S1.42AK in the normal S1.42AJ run and both LC Office diagnostics; DIAG2 subsequently exercised LC Office for roughly twelve minutes. No current user-facing metal-detector/Pikmin regression is established.

## Accepted contract

S1.42AK was built directly from exact S1.42AJ and accepts only the statically verified balanced delta:

- LC Office `Camera Frame Speed = 0`;
- exact `YaBoiDucki-men_stalker 3.1.2` disabled;
- Biodiversity Aloe `PowerLevel = 0`;
- RandomEnemiesSize byte-identical to S1.42AJ;
- LC Office scrap tuning unchanged;
- no diagnostic force-selection artifacts.

## Parent and diagnostic evidence

**S1.42AJ — LC Office V81 Integration** remains the exact unaccepted parent of S1.42AK. It is not a gameplay baseline.

**S1.42AJ-DIAG1** and **S1.42AJ-DIAG2** remain diagnostic-only evidence. DIAG2's longer confirmation run retained `Camera Frame Speed = 0`, covered roughly twelve minutes after LC Office generation, included repeated elevator operation and did not reproduce the characteristic repeated DIAG1 stutter reported by the user.

## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK**.
- Active gameplay candidate: **none**.
- Active diagnostic runtime target: **S1.42AK-SCRAPDIAG1**.
- Runtime test outstanding: **yes**.
- Selected scope: **LC Office Scrap Quantity/Distribution Investigation — PUBLISHED / ARMED DIAGNOSTIC / RUNTIME PLACEMENT EVIDENCE OUTSTANDING**.
- Exact runtime profile: `Profiles/LC V1 S1.42AK-SCRAPDIAG1 LC Office Scrap Placement Diagnostic.r2z` / SHA-256 `233bcc058a3fa95d63e0577c4ff74b5a0dc137db49757b50376e447dd082d3b1`.
- S1.42AK remains both accepted gameplay baseline and latest normal built artifact; the diagnostic is not a gameplay successor.
- `BuildSpecs/current.json` remains disabled at `IDLE_AFTER_S1.42AK_ACCEPTANCE_INVESTIGATE_LC_OFFICE_SCRAP`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-SCRAPDIAG1` controls attribution for the pending diagnostic run.

## Selected investigation scope

LC Office scrap quantity/distribution is explicitly selected under `BuildSpecs/LC_OFFICE_SCRAP_INVESTIGATION_PLAN.md` and `Knowledge/INTERIORS_AND_LLL.md`. It changes no accepted gameplay tuning and assigns no gameplay successor build ID.

The existing-evidence count comparison is complete. LC Office produced a 14-object base target in DIAG1 and 15 in DIAG2; accepted S1.42AK Spooky Manor also began at 14 and finalized at 15. The normal S1.42AJ Facility run finalized much higher only because BCMER selected `PlentyOutsideScrap`, so that event-inflated result is not a normal comparator. No LC Office-specific low-count regression is established. Placement/discoverability remains unresolved.

The diagnostic defined by `Current/160_LC_OFFICE_SCRAP_PLACEMENT_DIAGNOSTIC_DESIGN.md` is implemented, statically validated and now repository-published from the exact pinned review artifact. Publication evidence is `BuildSpecs/S1.42AK-SCRAPDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`; activation authority is `Current/162_S1.42AK_SCRAPDIAG1_RUNTIME_ACTIVATION.md`. The pending Offense run must prove selector/logger arming, actual LC Office generation, stable snapshot A/B IDs, anchor/item placement markers and COMPLETE with no REFUSED/INCONCLUSIVE marker. Only the resulting placement evidence may resolve the distribution/discoverability question.

## Exact next project action

Run exact published S1.42AK-SCRAPDIAG1 on Offense, obtain a valid stable scrap-placement capture, then upload the resulting LogOutput.log under S1.42AK-SCRAPDIAG1 for repository ingestion and placement analysis.

## Permanent Gale workflow

Use the canonical repository-driven Gale replacement/import helper in `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. S1.42AK-SCRAPDIAG1 exercises its existing fail-closed **direct diagnostic** path: `ACTIVE_BUILD` and `CURRENT_STATE.diagnostic_revision` identify the published diagnostic, while its base build/profile/SHA must bind exactly to `AUTO_BUILD_RESULT` for accepted/latest S1.42AK. No diagnostic-parent hop is used.
