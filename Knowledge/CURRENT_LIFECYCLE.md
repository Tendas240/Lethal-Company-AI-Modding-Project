<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AJ candidate=S1.42AJ runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`, `Current/154_S1.42AJ_DIAG1_LC_OFFICE_RUNTIME_PERFORMANCE_FINDING.md`, `BuildSpecs/S1.42AJ-DIAG2_BUILD_EVIDENCE/BUILD_RESULT.json`, `BuildSpecs/S1.42AJ-DIAG2_BUILD_EVIDENCE/STATIC_VERIFICATION.json`, `BuildSpecs/S1.42AJ-DIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`  
**Last-Validated:** 2026-09-18

## Accepted gameplay baseline

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`

## Balanced lifecycle candidate

**S1.42AJ — LC Office V81 Integration — STATIC VALIDATED / ACTIVE BALANCED CANDIDATE / NOT ACCEPTED** remains unchanged.

Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`

The first full-normal Offense evidence at `RuntimeEvidence/S1.42AJ/20260917T171109Z/` proves ordinary LC Office viability at author rarity `65` and final normalized effective rarity `100`. That run selected Facility, so actual Office generation was obtained later through DIAG1.

## Diagnostic parent evidence

**S1.42AJ-DIAG1 — LC Office force-selection diagnostic — RUNTIME EVIDENCE INGESTED / NOT ACCEPTED** is now the explicit diagnostic parent for DIAG2.

Profile SHA-256: `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`  
Runtime evidence: `RuntimeEvidence/S1.42AJ-DIAG1/20260917T204918Z/`  
Log SHA-256: `bb81a91f2cabcb1a3b010dd988335cc9c9cb0b5bcc9bd646ee2ac18ccbb15a26`

DIAG1 successfully generated LC Office on Offense. During that run the user observed later-day stutter at roughly 3–4 hitches per second. Comparison with accepted S1.42AI downgraded the initial NavMesh-error hypothesis. The remaining narrow A/B hypothesis is LC Office's periodic camera-render path.

## Active diagnostic runtime target

**S1.42AJ-DIAG2 — LC Office Camera Render Diagnostic — PUBLISHED / ARMED FOR A/B / NOT ACCEPTED** is the current runtime evidence-attribution target.

Profile: `Profiles/LC V1 S1.42AJ-DIAG2 LC Office Camera Render Diagnostic.r2z`  
SHA-256: `1a17b532ebe5cfa598348ae15dea21af906ac7b33ec00c9c428d2684cc9f69cb`  
Exact parent: `S1.42AJ-DIAG1` / SHA-256 `4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832`  
Publication evidence: `BuildSpecs/S1.42AJ-DIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`

The reviewed artifact proves zero changed existing archive members, zero removed members and exactly one added member: `BepInEx/config/Piggy.LCOffice.cfg`, containing only `[General] Camera Frame Speed = 0`. DIAG1 force-selection and all existing package/DLL/config bytes are preserved. This isolates the camera-render variable but does **not** establish causality.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Balanced lifecycle candidate: **S1.42AJ**.
- Runtime-active evidence-attribution pointer: **S1.42AJ-DIAG2**.
- Runtime test outstanding: **yes — DIAG2 Offense A/B**.
- `BuildSpecs/current.json` remains disabled; no balanced successor is being built.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ-DIAG2` is evidence attribution only and does not promote DIAG2.

## Exact next project action

Run exact published **S1.42AJ-DIAG2** on Offense. Confirm LC Office generation, traversal, elevator, scrap and observable enemy behavior remain healthy, and specifically compare the previously observed later-day ~3–4 hitches-per-second stutter against DIAG1 with `Camera Frame Speed = 0`. Upload the resulting `LogOutput.log` as DIAG2 evidence.

Do not promote or reject balanced S1.42AJ from this diagnostic alone. If the camera hypothesis is confirmed, any balanced successor must be derived from exact S1.42AJ, never from DIAG1 or DIAG2.

## Scope boundary

Universal-moon availability, general Interior viability work, Wesley, CullFactory, DunGenReferenceFixer and unrelated Interior changes remain out of scope for this A/B.

## Canonical Gale runtime import helper

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. The resolver remains fail-closed: a normal target must match `AUTO_BUILD_RESULT`; a direct diagnostic must bind exactly to that balanced result; and a second-generation diagnostic is permitted only when `CURRENT_STATE.selected_scope.diagnostic_parent_revision` identifies one exact published parent whose own base binds directly to `AUTO_BUILD_RESULT`. DIAG2 is the currently authorized one-hop case. The helper does not allow an arbitrary diagnostic chain.
