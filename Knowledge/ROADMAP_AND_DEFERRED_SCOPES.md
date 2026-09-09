<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AH candidate=none runtime_test_outstanding=false -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`, `RuntimeEvidence/S1.42AH/20260909T162513Z/`, `RuntimeEvidence/S1.42AH/20260908T202138Z/`, `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`  
**Last-Validated:** 2026-09-09

## Current position

Accepted gameplay baseline and latest built artifact: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**, SHA-256 `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.

Active candidate: **none**. Runtime test outstanding: **no**. `BuildSpecs/current.json` is disabled (`IDLE_AFTER_S1.42AH_ACCEPTANCE_PREP_SHYGUY_CONFIG_SUCCESSOR`); `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`; no successor has yet been built or armed.

S1.42AF remains the accepted predecessor/rollback point. S1.42AG remains rejected historical evidence only.

## Completed S1.42AH MouthDog scope

`Current/140` proves patch installation, repeated live Vanilla MouthDog -> Pikmin collision blocking and MouthDog -> player preservation. `Current/141` additionally proves explicit native Pikmin -> MouthDog latch/attack/damage, MouthDog death, native task-removal/unlatch cleanup, corpse carry, live adapter prevention, preserved noise response and clean known project regression markers.

The final deliberate neighbor test in `RuntimeEvidence/S1.42AH/20260909T162513Z/`, analyzed under `Current/142`, closes non-Pikmin `EnemyAI` pass-through. In the decisive last gameplay run MouthDogs and a Redwood Titan are present and the Redwood Titan reaches the normal enemy-death path. The user reported observing what appeared to be a Mouth Dog killing it. The raw death line does not encode attacker identity, so current authority relies on that deliberate observation together with the exact S1.42AH type gate and Vanilla V81 `MouthDogAI.OnCollideWithEnemy` -> `HitEnemy(2)` source contract rather than inventing an attacker field.

S1.42AH is therefore explicitly accepted and its runtime gate is closed.

## Selected next independent scope — BCMER ShyGuy interior-only correction

The next project action is the already documented correction under `BuildSpecs/DEFERRED_BCMER_SHYGUY_INTERIOR_ONLY_PLAN.md`.

Prepare a single-variable BCMER/config successor from accepted S1.42AH that:

- keeps `[ShyGuy] Event Enabled? = true`;
- keeps its EventType and all three interior values unchanged;
- sets `ShyGuyDef OutsideEnemyRarity = 0, 0, 0, 0`;
- sets `ShyGuyDef MinOutsideEnemy = 0, 0, 0, 0`;
- sets `ShyGuyDef MaxOutsideEnemy = 0, 0, 0, 0`;
- keeps ordinary Scopophobia `SpawnOutside = false`;
- changes no unrelated package/config/gameplay scope.

This correction is now eligible because the S1.42AH lifecycle gate is closed, but no successor is armed by the acceptance itself. Static archive-delta validation comes before any new runtime test.

The user-observed exterior ShyGuy invisibility remains a symptom with an unproven exact renderer/material mechanism. The proven defect is the BCMER event forcing an exterior ShyGuy despite the ordinary Scopophobia location contract.

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