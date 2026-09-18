<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`, `Current/154_S1.42AJ_DIAG1_LC_OFFICE_RUNTIME_PERFORMANCE_FINDING.md`, `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `RuntimeEvidence/S1.42AJ/20260917T171109Z/`, `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json`, `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json`, `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`, `RuntimeEvidence/S1.42AJ-DIAG1/20260917T204918Z/`
**Last-Validated:** 2026-09-18

## Accepted gameplay baseline

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

## Latest built artifact

**S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** remains the balanced lifecycle candidate.

Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`  
Candidate record: `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`  
Static evidence: `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`

The static gate proves the exact compatibility-first package delta, sole modern IAmBatby LLL ownership, absence of the deprecated fork, no unrelated package drift, and byte-identical accepted Interior Weight Normalization.

The first full-normal S1.42AJ runtime evidence is ingested at `RuntimeEvidence/S1.42AJ/20260917T171109Z/` (`LogOutput.log` SHA-256 `b5267cd62a222929c117bae52371229d4fe0dcf510248ee80d1f4c1a51e67c12`). On Offense, LLL returned `LC Office (65)` and the accepted post-viability normalizer produced final `LC Office(100)`, proving default viability plus equal effective weighting. That run selected `Facility`, so actual LC Office generation/traversal/elevator/power/enemy-navigation coverage is still outstanding.

## Published diagnostic artifact

**S1.42AJ-DIAG1 — LC Office Diagnostic — STATIC PASS / RUNTIME EVIDENCE INGESTED / PERFORMANCE REGRESSION UNDER INVESTIGATION / NOT ACCEPTED** remains strictly diagnostic evidence derived from exact balanced S1.42AJ.

Profile: `Profiles/LC V1 S1.42AJ-DIAG1 LC Office Diagnostic.r2z`  
SHA-256: `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`  
Profile sources: `ProfileSources/S1.42AJ-DIAG1/`  
Build result: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json`  
Static verification: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json`  
Publication verification: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`

The diagnostic plugin SHA-256 is `9a477c18e5b8cf38922fa755b6bab101babc2f987e858567172b9be9c2c05fad`; the accepted normalizer remains byte-identical at `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`. The exact reviewed artifact came from PR #111 / reviewed head `d3155d86c89595cc9ab4b4cda5d8535ec138eae2`, review artifact ID `10513954928`, build/static gate run `35261773897`, and was published at commit `71ac6fad7eef3eb5e7d84b81e88a553d1032fbdf`.

This diagnostic is not an accepted build and does not replace balanced S1.42AJ. Its completed Offense run is ingested at `RuntimeEvidence/S1.42AJ-DIAG1/20260917T204918Z/` (`LogOutput.log` SHA-256 `bb81a91f2cabcb1a3b010dd988335cc9c9cb0b5bcc9bd646ee2ac18ccbb15a26`). The run obtained actual LC Office generation coverage, but the user reported frequent later-day stutter at roughly 3-4 hitches per second. The first NavMesh-error hypothesis was downgraded after comparison with accepted S1.42AI, which already contained much larger repeated NavMesh-agent warning volume plus some RuntimeNavMeshBuilder readability noise. The current narrow working hypothesis is LC Office's periodic `Camera.Render()` path; this is not yet proven causal. See `Current/154_S1.42AJ_DIAG1_LC_OFFICE_RUNTIME_PERFORMANCE_FINDING.md`.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest balanced built artifact: **S1.42AJ**.
- Active balanced lifecycle candidate: **S1.42AJ**.
- Runtime-active evidence-attribution pointer: **S1.42AJ-DIAG1** until a successor diagnostic is actually published/armed.
- Runtime test outstanding: **yes**, but DIAG1 itself is complete; the outstanding work is the isolated DIAG2 performance A/B test after DIAG2 is built.
- Selected successor scope: **LC Office V81 Integration — DIAG1 evidence ingested; performance diagnosis required before acceptance**.
- `BuildSpecs/current.json` remains disabled at `IDLE_AFTER_S1.42AJ_BUILD_AWAITING_RUNTIME_VALIDATION`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ-DIAG1` controls diagnostic runtime-evidence attribution only.

## Exact next project action

Prepare and build a strictly one-variable **S1.42AJ-DIAG2** from exact S1.42AJ-DIAG1. Preserve DIAG1 force-selection and every package/DLL/config except set `BepInEx/config/Piggy.LCOffice.cfg` -> `[General] Camera Frame Speed = 0`. Statically prove that exact delta, publish/arm DIAG2, then perform an Offense A/B runtime test focused on whether the previously observed frequent later-day stutter disappears or materially decreases while Office generation/traversal/elevator/scrap/enemy behavior remains healthy.

Do not alter balanced S1.42AJ and do not treat the camera hypothesis as proven before the A/B result. If confirmed, a balanced successor must be derived from exact S1.42AJ rather than from a diagnostic profile.

## Scope boundary

S1.42AJ remains compatibility-first. S1.42AJ-DIAG1 and the planned S1.42AJ-DIAG2 are diagnostic-only and must not become acceptance authority. DIAG2 must be a one-variable camera-render A/B test only; do not combine universal LC Office moon availability, universal Interior viability, Wesley changes, CullFactory work, DunGenReferenceFixer evaluation or another deferred Interior scope into it. The accepted post-viability normalization architecture remains unchanged.

## Canonical Gale runtime import helper

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-17-import-uia-v2.4.1-diagnostic-build-result-url-delimiting`. The wrapper preserves the previously user-validated v2.2 UI/import path and resolves the runtime-active S1.42AJ-DIAG1 target only through the explicit fail-closed `CURRENT_STATE.selected_scope.diagnostic_revision` + build-result binding. The first real DIAG1 import attempt exposed a pre-import PowerShell expandable-string defect in the dynamic build-result URL: `?` was consumed as part of the variable name, yielding a Raw GitHub 404 before any profile download or local replacement occurred. v2.4.1 explicitly delimits the path variable before `?cb`, segment-escapes the repository path, and makes the diagnostic build-result fetch terminating/fail-closed. The corrected v2.4.1 import path was successfully used for the completed DIAG1 runtime run. `RuntimeInbox/ACTIVE_BUILD.txt` remains DIAG1 only until a later diagnostic artifact is actually published and armed; this pointer does not promote or replace balanced S1.42AJ.
