<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md`, `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`, `Current/Projektstatus_S1.42AI-DIAG1R3_RUNTIME_PASS.json`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/Projektstatus_S1.42AI_CANDIDATE.json`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** 2026-09-16

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Completed diagnostic evidence

**S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — DIAGNOSTIC RUNTIME PASS / NOT GAMEPLAY ACCEPTED.**

R3 runtime evidence proves clean owner derivation, dependency-absent EndlessElevator `NOT_APPLICABLE`, guard-layer installation, exact `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` ordinal identity resolution and ShyGuy-only pool/spawn behavior without DIAG1 invalidation, rollback, identity failure or isolation bypass. The operator again saw a visible interior ShyGuy and no non-ShyGuy enemy. No exterior ShyGuy occurred, so exterior visibility remains **NOT_EXERCISED**, not passed or failed. The ship-terminal `enemies` command was not repeated and is not required by the R3 gate.

Decision: `Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md`. Runtime: `RuntimeEvidence/S1.42AI-DIAG1R3/20260916T161243Z/`.

## Active candidate

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACTIVE FULL-NORMAL RUNTIME CANDIDATE / NOT ACCEPTED**  
Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Candidate authority: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`

R3 diagnostic success only clears the temporary diagnostic question; it does not substitute for this independent full-normal gate.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Completed diagnostic evidence: **S1.42AI-DIAG1R3**.
- Latest built artifact and active runtime candidate: **S1.42AI**.
- Runtime test outstanding: **yes — full-normal S1.42AI**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION`; no successor build is armed.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` controls the next runtime-evidence attribution and is not acceptance authority.
- `Current/AUTO_BUILD_RESULT.json.build_id = S1.42AI` identifies the exact artifact to import/test.

## Canonical Gale workflow

Import/replace the active S1.42AI profile only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` using canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The exact ready-to-test replacement/import command and the exact S1.42AI runtime-log uploader are recorded in `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`.

## Exact full-normal gate

Run `S1.42AI` under the full normal stack according to `Current/143...`: positively obtain or force the BCMER `ShyGuy` event; confirm intended interior ShyGuy availability; verify BCMER does not add ShyGuy to the exterior list/path and no `ShyGuy(Clone) spawned outside; Switching to exterior AI` marker is produced by that event; preserve exact BCMER 1.71.0/EventType values, ordinary Scopophobia `SpawnOutside=false`, inherited S1.42AH contracts and absence of new project regression markers.

## Exact next project action

Import S1.42AI with the canonical Gale v2.4 replacement helper and run the full-normal BCMER ShyGuy runtime gate from Current/143. Positively obtain or force the BCMER ShyGuy event, confirm ShyGuy remains available through the intended interior event path, verify that BCMER adds no ShyGuy to the exterior path and that no 'ShyGuy(Clone) spawned outside; Switching to exterior AI' marker occurs from that event, then upload the complete fresh S1.42AI LogOutput.log with the build-specific uploader in Current/143. Do not accept S1.42AI from diagnostic success alone.
