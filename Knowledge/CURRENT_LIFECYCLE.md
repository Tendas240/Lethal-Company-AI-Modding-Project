<!-- LIVE_STATE: accepted=S1.42AI latest=S1.42AI candidate=none runtime_test_outstanding=false -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed decisions remain in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `RuntimeEvidence/S1.42AI/20260916T180452Z/RUNTIME_ACCEPTANCE_DECISION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `Current/151_S1.42AI-DIAG1R3_RUNTIME_DIAGNOSTIC_PASS.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** 2026-09-16

## Accepted gameplay baseline

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK** is the sole current accepted gameplay baseline.

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

S1.42AH remains the accepted predecessor and rollback provenance baseline, but it is no longer the current gameplay baseline.

## Acceptance result

The independent full-normal S1.42AI gate passed after the completed DIAG1/R1/R2/R3 diagnostic chain. The real BCMER `ShyGuy` event path was exercised; interior ShyGuy availability remained functional; `ShyGuyDef` stayed at zero exterior weight/spawn contribution; and no `ShyGuy(Clone) spawned outside; Switching to exterior AI` marker attributable to the event occurred.

Static evidence proves the semantic delta remains exactly the three `[ShyGuy]` exterior BCMER values while the event, EventType, interior values, package state and ordinary Scopophobia `SpawnOutside=false` contract are preserved.

The observed ShyGuy `InvalidOperationException` and disconnect/teardown AdditionalNetworking fatal are retained as real evidence. Attribution review found neither is caused by the S1.42AI three-value exterior-config delta, so neither fails the build-specific acceptance gate.

## Completed diagnostic evidence

**S1.42AI-DIAG1R3** remains diagnostic runtime-pass evidence only. DIAG1, R1 and R2 remain failed diagnostic predecessors. None of these diagnostic artifacts is a gameplay baseline or active candidate.

## Live execution state

- Accepted baseline: **S1.42AI**.
- Latest built artifact: **S1.42AI**.
- Active runtime candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_ACCEPTANCE_AWAITING_NEXT_SCOPE`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI` remains the runtime-evidence attribution build and does not arm a successor.
- No successor build is armed.

## Permanent Gale profile replacement/import route

For any future runtime candidate that is explicitly armed, the canonical Gale profile replacement/import workflow remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, with the permanent fail-closed helper revision contract `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The detailed workflow authority is `Knowledge/GALE_PROFILE_WORKFLOW.md`.

The current S1.42AI acceptance state has no runtime test outstanding, so this permanent route does not itself instruct an import, arm a candidate, or require another gameplay run. It becomes operational only after exactly one future candidate is explicitly selected and armed by the repository lifecycle.

## Exact next project action

Select exactly one remaining deferred independent scope from `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md` before preparing or arming any successor. Do not mix unrelated deferred scopes.
