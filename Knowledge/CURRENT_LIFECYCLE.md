<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action
**Evidence:** `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`
**Last-Validated:** 2026-09-10

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`
Final decisive runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

S1.42AH remains the sole accepted gameplay base. Its MouthDog/Pikmin scope is closed and inherited unchanged by the new config-only candidate.

## Latest built artifact / active candidate

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`
Profile SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`
Parent: `S1.42AH`
Candidate: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`
Project status: `Current/Projektstatus_S1.42AI_CANDIDATE.json`
Static evidence: `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`

Static verification proves exactly two changed existing archive members: `export.r2x` and `BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`. The semantic config delta is exactly the three ShyGuy exterior values changed to `0, 0, 0, 0`. All interior ShyGuy event values, EventType, event enable state, package state and every unrelated archive member are preserved; `Scopophobia.cfg` is byte-identical to S1.42AH.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI**.
- Active candidate: **S1.42AI**.
- Runtime test outstanding: **yes**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION` and guards the exact S1.42AI profile/SHA.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` is the runtime/evidence-attribution pointer.
- S1.42AI is not accepted until an explicit runtime decision closes the gate.

## Diagnostic preparation priority

The user requested a temporary ShyGuy-only enemy and BCMER event isolation revision before the next gameplay run. The current preparation authority is `BuildSpecs/S1.42AI_PLAN.md` (planned `S1.42AI-DIAG1`, not built). The existing S1.42AI artifact and its full-normal runtime gate remain intact and unaccepted; diagnostic success cannot replace full-normal acceptance.

The existing S1.42AI import/upload pair below belongs to the existing full-normal artifact. Do not present it as an isolation build. Keep both controllers unchanged during plan preparation and preserve upload access for already-completed S1.42AI tests.

## Canonical Gale workflow

Use the repository-driven **v2.4** Gale replacement path in `Knowledge/GALE_PROFILE_WORKFLOW.md`, implemented by `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. For this candidate, pair it with the exact S1.42AI runtime-log uploader recorded in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, as required by `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md`.

## Exact next project action

Prepare the temporary S1.42AI-DIAG1 ShyGuy-only enemy and BCMER event isolation described in BuildSpecs/S1.42AI_PLAN.md before requesting another gameplay run. Preserve the existing S1.42AI artifact and its still-open full-normal runtime gate. Complete the exact spawn/forced-event interception safety review, then implement and build the separately identified diagnostic revision through repository-native infrastructure. Do not import the existing S1.42AI profile as if it already contained isolation. Keep build and runtime controllers unchanged until an atomic validated candidate transition; ingest any already-completed S1.42AI test without requiring a repeat.
