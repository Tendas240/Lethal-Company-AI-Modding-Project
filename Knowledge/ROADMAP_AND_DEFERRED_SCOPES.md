<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `RuntimeEvidence/S1.42AH/20260908T162411Z/`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`  
**Last-Validated:** 2026-09-08

## Current position

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**. Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact / active runtime candidate: **S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / PARTIAL RUNTIME PASS / TARGETED REMAINDER OUTSTANDING / NOT ACCEPTED**. Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.

Runtime test outstanding: **yes**. S1.42AH is neither accepted nor rejected. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`. No successor beyond S1.42AH is armed.

## Completed MouthDog implementation and first-runtime milestone

The source boundaries and successor Patch Safety Review are closed, and S1.42AH implements the reviewed dual-prevention delta from exact accepted S1.42AF:

1. retain the exact `Priority.First` prevention prefix on declared `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`;
2. add the exact `Priority.First` prefix on declared `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)`;
3. skip that Vanilla override only when the supplied `collidedEnemy` is a validated runtime `LethalMin.PikminAI`.

The first ingested S1.42AH runtime run is recorded in `Current/140` and `RuntimeEvidence/S1.42AH/20260908T162411Z/`. It positively proves patch installation, repeated live Vanilla MouthDog -> Pikmin collision blocking, and exercised MouthDog -> player maul/kill preservation. Those checks are no longer the open gate by themselves.

S1.42AG remains historical rejected evidence only. Do not rebuild from it and do not repeat its runtime test.

## Exact next gameplay scope

Run only the **targeted S1.42AH runtime remainder** from `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`.

The remaining gate must deliberately prove:

- native Pikmin -> MouthDog latch/attack/damage by explicit command/throw;
- MouthDog death through that attack path plus death-triggered unlatch/release/task cleanup;
- adapter-side MouthDog bite protection as runtime behavior, not installation only;
- preservation of Paw-initiated `BiteKillEnemyAI` behavior;
- non-Pikmin neighboring `EnemyAI` behavior remains unfiltered;
- combat/UI membership invariants and known regression markers remain clean around the reverse-direction/death-cleanup sequence;
- ordinary audible-noise response remains available.

Passive follower non-aggression is not a reverse-direction test. Position-based pursuit/lunge toward an audible Pikmin world position is not by itself failure. The first run's `Invalid Enemy States` / `Not hitting MouthDog` messages do not substitute for the explicit reverse-direction test and do not independently prove a defect.

If the remaining required checks all pass, explicitly accept S1.42AH. If a targeted required check fails, explicitly reject S1.42AH and return to an S1.42AF-derived follow-up. Do not rebuild S1.42AH or repeat already-proven startup/Vanilla-collision/player-maul coverage merely to obtain the missing evidence.

## Remaining deferred independent gameplay/compatibility scopes

- **LC Office V81 integration** under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`; do not arm while S1.42AH runtime validation is open.
- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible user-facing evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence beyond the selected MouthDog interaction.

## BCMER and interior boundaries

S1.42AC remains the accepted historical BCMER 1.71.0 static EventType-probability implementation inherited by S1.42AF/S1.42AH. Exact long-run executed EventType frequency after runtime eligibility filters is a separate unarmed algorithm-design scope.

The inherited S1.42AB implementation already equalizes effective rarity for LLL-viable interiors after viability filtering. S1.42AH does not alter this path. LC Office, CullFactory compatibility, Mausoleum fog and route/NavMesh recovery remain separate deferred scopes.

## Repository-integrity boundary

Repository architecture/handover repairs are governance work, not gameplay changes. They must preserve S1.42AF/S1.42AH artifact bytes and pass the permanent Knowledge Architecture gates before handover. Future automatic profile-index commits must also receive normal CI validation instead of bypassing it.

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` remains historical planning evidence only and does not override this live roadmap.
