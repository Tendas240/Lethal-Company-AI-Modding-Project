<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`, `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`  
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

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest built artifact: **S1.42AJ**.
- Active runtime candidate: **S1.42AJ**.
- Runtime test outstanding: **yes**.
- Selected successor scope: **LC Office V81 Integration — active runtime candidate**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AJ_BUILD_AWAITING_RUNTIME_VALIDATION`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` controls runtime-evidence attribution only.

## Exact next project action

Import S1.42AJ with the canonical Gale v2.4 replacement helper, execute the full-normal LC Office runtime acceptance gate from `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md` and `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`, then upload the complete fresh S1.42AJ `LogOutput.log`. Do not accept S1.42AJ from static/build success alone.

## Scope boundary

S1.42AJ remains compatibility-first. Do not combine universal LC Office moon availability, universal Interior viability, Wesley changes, CullFactory work, DunGenReferenceFixer evaluation or another deferred Interior scope into this candidate. The accepted post-viability normalization architecture remains unchanged.

## Canonical Gale runtime import helper

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at validated helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof` for the currently armed S1.42AJ runtime import/materialization workflow.
