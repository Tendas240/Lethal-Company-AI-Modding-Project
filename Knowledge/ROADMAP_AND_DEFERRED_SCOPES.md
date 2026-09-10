<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC
**Authority:** live selected/deferred-scope list only
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`, `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`
**Last-Validated:** 2026-09-10

## Current position

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**, SHA-256 `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.

Latest built artifact and active runtime candidate: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction**, SHA-256 `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`. Runtime validation is outstanding; S1.42AI is not yet accepted.

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION`; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI`.

## Active independent scope — S1.42AI BCMER ShyGuy interior-only correction

S1.42AI implements the previously selected config-only correction directly from accepted S1.42AH. Static verification proves the only semantic gameplay/config change is the `[ShyGuy]` exterior triplet becoming zero while Event Enabled, EventType, all three interior values and ordinary Scopophobia `SpawnOutside = false` remain unchanged. Every unrelated archive member is byte-identical to S1.42AH.

The user requested a temporary ShyGuy-only enemy and BCMER event isolation revision before the next gameplay run. The current preparation authority is `BuildSpecs/S1.42AI_PLAN.md` (planned `S1.42AI-DIAG1`, not built). The existing S1.42AI artifact and its full-normal runtime gate remain intact and unaccepted; diagnostic success cannot replace full-normal acceptance.

After the diagnostic stage, the retained normal-stack gate must positively exercise ShyGuy and prove its interior availability and absence of the exterior defect. Exact acceptance authority remains `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`.

The earlier user-observed invisible exterior ShyGuy remains a symptom whose exact renderer/material mechanism was not proven; S1.42AI claims only to correct the proven BCMER exterior-spawn configuration defect.

## Remaining deferred independent scopes

- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation; treat inside -> outside transition compatibility separately and do not enable ordinary Scopophobia `SpawnOutside` merely to emulate escape behavior.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible user-facing evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.

## Repository-integrity boundary

Handover/governance repair must preserve gameplay artifacts/controllers and pass the permanent Knowledge Architecture gates before final handover. Historical planning files do not override this live roadmap.
