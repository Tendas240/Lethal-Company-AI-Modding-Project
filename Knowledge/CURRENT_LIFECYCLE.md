<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`, `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `RuntimeEvidence/S1.42AJ/20260917T171109Z/`, `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json`, `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json`, `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`
**Last-Validated:** 2026-09-17

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

**S1.42AJ-DIAG1 — LC Office Diagnostic — STATIC PASS / RUNTIME-ACTIVE EVIDENCE TARGET / ARMED / NOT ACCEPTED** is published strictly as diagnostic evidence derived from exact balanced S1.42AJ.

Profile: `Profiles/LC V1 S1.42AJ-DIAG1 LC Office Diagnostic.r2z`  
SHA-256: `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`  
Profile sources: `ProfileSources/S1.42AJ-DIAG1/`  
Build result: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json`  
Static verification: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json`  
Publication verification: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`

The diagnostic plugin SHA-256 is `9a477c18e5b8cf38922fa755b6bab101babc2f987e858567172b9be9c2c05fad`; the accepted normalizer remains byte-identical at `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`. The exact reviewed artifact came from PR #111 / reviewed head `d3155d86c89595cc9ab4b4cda5d8535ec138eae2`, review artifact ID `10513954928`, build/static gate run `35261773897`, and was published at commit `71ac6fad7eef3eb5e7d84b81e88a553d1032fbdf`.

This diagnostic is not an accepted build and does not replace balanced S1.42AJ. It is now the runtime-active evidence target only so its diagnostic run is attributed separately; no diagnostic runtime evidence exists yet.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest balanced built artifact: **S1.42AJ**.
- Active balanced lifecycle candidate: **S1.42AJ**.
- Runtime-active diagnostic evidence target: **S1.42AJ-DIAG1**.
- Runtime test outstanding: **yes**.
- Selected successor scope: **LC Office V81 Integration — diagnostic artifact active for missing generation coverage**.
- `BuildSpecs/current.json` remains disabled at `IDLE_AFTER_S1.42AJ_BUILD_AWAITING_RUNTIME_VALIDATION`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ-DIAG1` controls diagnostic runtime-evidence attribution only.

## Exact next project action

Runtime-test the activated **S1.42AJ-DIAG1** diagnostic artifact on Offense for only the still-missing LC Office generation coverage: confirm LC Office actually generates after normal viability, validate traversal/entrance/exit, elevator and breaker/power where available, enemy navigation, scrap generation, and absence of a new critical regression/error flood. Preserve the already ingested unforced S1.42AJ viability/weight proof and do not treat diagnostic force-selection as balanced selection semantics.

Runtime evidence must be uploaded under `S1.42AJ-DIAG1` through `RuntimeInbox/ACTIVE_BUILD.txt`. Balanced S1.42AJ remains unchanged, not accepted, and remains the lifecycle candidate.

## Scope boundary

S1.42AJ remains compatibility-first. S1.42AJ-DIAG1 is diagnostic-only and must not become acceptance authority. Do not combine universal LC Office moon availability, universal Interior viability, Wesley changes, CullFactory work, DunGenReferenceFixer evaluation or another deferred Interior scope into this diagnostic. The accepted post-viability normalization architecture remains unchanged.

## Canonical Gale runtime import helper

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at validated helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The armed runtime target is now S1.42AJ-DIAG1; this does not promote or replace balanced S1.42AJ.
