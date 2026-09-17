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

**S1.42AJ-DIAG1 — LC Office Diagnostic — STATIC PASS / NOT RUNTIME READY / NOT ARMED** is published strictly as diagnostic evidence derived from exact balanced S1.42AJ.

Profile: `Profiles/LC V1 S1.42AJ-DIAG1 LC Office Diagnostic.r2z`  
SHA-256: `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`  
Profile sources: `ProfileSources/S1.42AJ-DIAG1/`  
Build result: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json`  
Static verification: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json`  
Publication verification: `BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`

The diagnostic plugin SHA-256 is `9a477c18e5b8cf38922fa755b6bab101babc2f987e858567172b9be9c2c05fad`; the accepted normalizer remains byte-identical at `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`. The exact reviewed artifact came from PR #111 / reviewed head `d3155d86c89595cc9ab4b4cda5d8535ec138eae2`, review artifact ID `10513954928`, build/static gate run `35261773897`, and was published at commit `71ac6fad7eef3eb5e7d84b81e88a553d1032fbdf`.

This diagnostic is not an accepted build, does not replace balanced S1.42AJ, is not yet the runtime-active evidence target, and has no runtime evidence yet.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest balanced built artifact: **S1.42AJ**.
- Active runtime candidate/evidence target: **S1.42AJ**.
- Published diagnostic awaiting activation: **S1.42AJ-DIAG1**.
- Runtime test outstanding: **yes**.
- Selected successor scope: **LC Office V81 Integration — diagnostic artifact published, runtime activation still outstanding**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AJ_BUILD_AWAITING_RUNTIME_VALIDATION`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` controls runtime-evidence attribution only.

## Exact next project action

Perform the separate atomic runtime/lifecycle activation of the already published **S1.42AJ-DIAG1** diagnostic artifact without accepting or replacing balanced S1.42AJ. Update the canonical lifecycle/controllers and `RuntimeInbox/ACTIVE_BUILD.txt` consistently so the diagnostic runtime test is attributed to S1.42AJ-DIAG1, verify the resulting exact-head CI, then provide the repository-driven Gale replacement/import one-liner and the exact S1.42AJ-DIAG1 one-line runtime-log uploader in the same response as the test instructions.

The runtime test is only for the still-missing actual LC Office generation/traversal/elevator/power/enemy-navigation/scrap coverage on Offense after normal viability. Preserve the already ingested unforced S1.42AJ viability/weight proof.

## Scope boundary

S1.42AJ remains compatibility-first. S1.42AJ-DIAG1 is diagnostic-only and must not become acceptance authority. Do not combine universal LC Office moon availability, universal Interior viability, Wesley changes, CullFactory work, DunGenReferenceFixer evaluation or another deferred Interior scope into this diagnostic. The accepted post-viability normalization architecture remains unchanged.

## Canonical Gale runtime import helper

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at validated helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The currently armed runtime target remains S1.42AJ until the separate atomic S1.42AJ-DIAG1 activation is completed and verified.
