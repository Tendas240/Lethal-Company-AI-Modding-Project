<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`, `RuntimeEvidence/S1.42AH/20260908T174352Z/`, `RuntimeEvidence/S1.42AH/20260908T202138Z/`, `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`  
**Last-Validated:** 2026-09-09

## Current position

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact / active candidate: **S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / EXTENDED PARTIAL RUNTIME PASS / FINAL NON-PIKMIN NEIGHBOR REMAINDER OUTSTANDING / NOT ACCEPTED**, SHA-256 `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.

Runtime test outstanding: **yes**. `BuildSpecs/current.json` remains disabled (`IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`); `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`; no successor is armed.

## Completed S1.42AH runtime milestones

`Current/140` proves patch installation, repeated live Vanilla MouthDog -> Pikmin collision blocking and MouthDog -> player preservation. `Current/141` additionally proves explicit native Pikmin -> MouthDog latch/attack/damage, MouthDog death, native task-removal/unlatch cleanup, corpse carry, live adapter prevention, preserved noise response and clean known project regression markers.

Later S1.42AH evidence `RuntimeEvidence/S1.42AH/20260908T202138Z/` additionally exposes an independent BCMER/Scopophobia configuration defect: BCMER event `ShyGuy` can force an exterior ShyGuy despite Scopophobia retaining ordinary `SpawnOutside = false`. This finding does **not** close or replace the outstanding MouthDog non-Pikmin-neighbor gate and does not authorize mutation/rebuild of S1.42AH. Its deferred correction is `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`.

S1.42AG remains rejected historical evidence only.

## Exact next gameplay scope

Run only the **final non-Pikmin neighbor remainder** from `Current/141`:

- deliberately exercise MouthDog/Paw -> **non-Pikmin `EnemyAI`**;
- prove native Paw-initiated `BiteKillEnemyAI` / generic non-Pikmin collision behavior remains functional;
- prove the Pikmin-only prefix does not filter that path;
- upload the complete fresh S1.42AH log.

Do not repeat already-proven Pikmin -> MouthDog combat/death/cleanup, adapter protection, startup, Pikmin collision block or player-maul coverage merely for this final gate. If it passes, explicitly accept S1.42AH; if it fails, explicitly reject S1.42AH and return to an S1.42AF-derived follow-up.

## Remaining deferred independent scopes

- BCMER ShyGuy event interior-only correction under `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`: confirmed S1.42AH exterior-event spawn conflict; do not mutate S1.42AH. Apply in the first eligible independent BCMER/config successor after the current gate closes. If S1.42AH is rejected, the canonical S1.42AF-derived MouthDog recovery takes precedence and this correction stays pending unless a later lifecycle explicitly arms a combined scope.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`; do not arm while S1.42AH validation is open.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation; treat inside -> outside transition compatibility separately and do not enable ordinary Scopophobia `SpawnOutside` merely to emulate escape behavior.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible user-facing evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.

## Repository-integrity boundary

Handover/governance repair must preserve gameplay artifacts/controllers and pass the permanent Knowledge Architecture gates before final handover. Historical planning files do not override this live roadmap.
