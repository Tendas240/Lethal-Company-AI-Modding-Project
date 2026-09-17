<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=none runtime_test_outstanding=false -->
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

**S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / RUNTIME NOT ARMED** is the latest built artifact.

Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`  
Candidate record: `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`  
Static evidence: `BuildSpecs/S1.42AJ_BUILD_EVIDENCE/STATIC_VERIFICATION.md`

The static gate proves the exact compatibility-first package delta: add LC Office 2.3.4, the V81 compatibility fix 2.0.0 and DestroyItemInSlotFix 1.0.0, transition DungeonGenerationPlus 1.5.0 -> 1.5.1, preserve every other package block byte-for-byte, preserve every non-export profile member byte-for-byte, retain `IAmBatby-LethalLevelLoader 1.7.12` as the sole LLL owner, keep `pacoito-LethalLevelLoaderUpdated` absent, and preserve the accepted Interior Weight Normalization DLL at SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest built artifact: **S1.42AJ**.
- Active runtime candidate: **none**.
- Runtime test outstanding: **no**.
- Selected successor scope: **LC Office V81 Integration — static validated / ready for runtime arming**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AJ_STATIC_VALIDATION_READY_FOR_RUNTIME_ARMING`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` remains runtime-evidence attribution only.
- No runtime test is armed and no gameplay run should start yet.

## Scope boundary

S1.42AJ remains compatibility-first. Do not combine universal LC Office moon availability, universal Interior viability, Wesley changes, CullFactory work, DunGenReferenceFixer evaluation or another deferred Interior scope into this candidate. The accepted post-viability normalization architecture remains unchanged.

## Exact next project action

Arm **S1.42AJ** as the sole runtime candidate in a separate lifecycle transition. Only that transition may set `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ` and `runtime_test_outstanding = true`. In the same user-facing response that arms the runtime test, provide both the canonical repository-driven Gale replacement/import PowerShell one-liner and the exact S1.42AJ-specific one-line runtime-log uploader.
