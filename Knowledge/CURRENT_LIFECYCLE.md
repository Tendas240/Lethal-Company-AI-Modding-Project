<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`, `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `RuntimeEvidence/S1.42AJ/20260917T171109Z/`
**Last-Validated:** 2026-09-17

## Accepted gameplay baseline

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

## Latest built artifact

**S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** is the latest built artifact.

Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`  
Candidate record: `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`  
Static evidence: `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`

The static gate proves the exact compatibility-first package delta, sole modern IAmBatby LLL ownership, absence of the deprecated fork, no unrelated package drift, and byte-identical accepted Interior Weight Normalization.

The first full-normal S1.42AJ runtime evidence is ingested at `RuntimeEvidence/S1.42AJ/20260917T171109Z/` (`LogOutput.log` SHA-256 `b5267cd62a222929c117bae52371229d4fe0dcf510248ee80d1f4c1a51e67c12`). On Offense, LLL returned `LC Office (65)` and the accepted post-viability normalizer produced final `LC Office(100)`, proving default viability plus equal effective weighting. That run selected `Facility`, so actual LC Office generation/traversal/elevator/power/enemy-navigation coverage is still outstanding.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest built artifact: **S1.42AJ**.
- Active runtime candidate: **S1.42AJ**.
- Runtime test outstanding: **yes**.
- Selected successor scope: **LC Office V81 Integration — active runtime candidate**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AJ_BUILD_AWAITING_RUNTIME_VALIDATION`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` controls runtime-evidence attribution only.

## Exact next project action

Prepare a strictly diagnostic **S1.42AJ-DIAG1** from exact S1.42AJ that force-selects LC Office on Offense only after normal LLL viability determination. Build/static-validate that diagnostic, then use it only to obtain the still-missing actual LC Office generation/traversal/elevator/power/enemy-navigation/scrap coverage. Preserve the ingested unforced S1.42AJ viability/weight proof, keep balanced S1.42AJ unchanged, and do not accept it until the complete runtime gate is satisfied.

## Scope boundary

S1.42AJ remains compatibility-first. Do not combine universal LC Office moon availability, universal Interior viability, Wesley changes, CullFactory work, DunGenReferenceFixer evaluation or another deferred Interior scope into this candidate. The accepted post-viability normalization architecture remains unchanged.

## Canonical Gale runtime import helper

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at validated helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof` for the currently armed S1.42AJ runtime import/materialization workflow.
