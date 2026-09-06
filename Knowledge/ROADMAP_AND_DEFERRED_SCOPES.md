# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`, `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`, `SourceEvidence/VanillaV81/EnemyAIOnCollideWithEnemy/20260906T204535Z/`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`  
**Last-Validated:** 2026-09-06

## Current position

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**. Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact: **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**. Profile SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`.

There is no active runtime candidate and no successor armed. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_MOUTHDOG_SOURCE_BOUNDARIES_AWAITING_PATCH_SAFETY_REVIEW`. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains evidence-attribution only.

## Completed MouthDog source-analysis milestone

All source boundaries required before successor design are now closed. Current analysis authority is `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`.

Proven boundaries:

- Vanilla `MouthDogAI.DetectNoise(...)` is position-based and can drive pursuit/lunge through `noisePositionGuess`.
- Vanilla `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` is an independent generic collision attack surface.
- Exact LethalMin 1.1.108 proves `PikminAI : EnemyAI`.
- Exact Vanilla V81 `EnemyAI.OnCollideWithEnemy()` is debug-only and has no gameplay/lifecycle mutation.
- Exact LethalMin `PikminItem.CarryNumerator()` repeatedly plays `ItemCarry` through the carrying Pikmin; with current audible-noise configuration, Pikmin sounds can emit `RoundManager.PlayAudibleNoise(...)` at the carrier position.

The stronger claim that Vanilla MouthDogAI semantically targets a Purple Pikmin because it carries `GoldBar(Clone)`, or that the GoldBar itself is the proved recurring carry-noise emitter, is unsupported/rejected. The exact audible event that caused the observed S1.42AG pursuit remains runtime-causally unproved.

No additional local source capture is currently required.

## Exact next scope

The selected work is now the **successor-specific MouthDog Patch Safety Review** under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

Before any successor is armed, the review must define the smallest exact Harmony boundary, its declaring type/signature/Pikmin identification, inheritance and secondary responsibilities, and the exact regression contract. It must preserve:

- S1.42AF as the guarded gameplay base;
- the useful S1.42AG prevention-before-mutation result on `MouthDogPikminEnemy.DoCheckInterval()` where still applicable;
- enabled native LethalMin ownership for Pikmin -> MouthDog attack/latch/death/unlatch/task lifecycle;
- MouthDog -> player behavior;
- passive follower non-aggression as normal behavior.

The future successor must remain a one-variable risky-patch delta and its runtime gate must deliberately test reverse-direction Pikmin -> MouthDog behavior.

Do not add guessed Harmony targets, broad `EnemyAI` scanning, whole-component disables or manual Pikmin state reconstruction. Do not arm/build a successor or start a gameplay test until the safety review closes.

## Remaining deferred independent gameplay/compatibility scopes

- **LC Office V81 integration** under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`: add `Piggy-LC_Office 2.3.4` with `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix 2.0.0`, `JacobG5-DestroyItemInSlotFix 1.0.0` and `Alice-DungeonGenerationPlus 1.5.1`; preserve `IAmBatby-LethalLevelLoader 1.7.12` as sole owner; explicitly forbid `pacoito-LethalLevelLoaderUpdated`; do not arm while the selected MouthDog compatibility scope remains open;
- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- broader LethalMin teardown/despawn repair only with stronger evidence beyond the selected MouthDog interaction.

## BCMER scope boundary

S1.42AC remains the accepted historical BCMER 1.71.0 static EventType-probability implementation inherited by S1.42AF. Exact long-run executed EventType frequency after runtime eligibility filters is a broader algorithm-design scope and is not armed.

## Interior scope boundary

The inherited S1.42AB implementation already equalizes effective rarity for LLL-viable interiors after viability filtering. S1.42AG did not alter that path.

Current full-normal-stack evidence proves `Art Gallery (MuseumInteriorFlow)` and `Rubber Rooms (RubberRoomsFlow)` register, are viable on Offense, and reach final effective rarity `100`. Their lack of observed natural rolls is not evidence of a weight defect.

LC Office remains separate/deferred. Author/technical viability restrictions, CullFactory compatibility, Mausoleum fog and route/NavMesh recovery remain separate.

## Repository-overhaul boundary

The overhaul is closed and validated. Future repository-architecture changes remain separate from gameplay changes and must continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves historical planning/package research only. This file plus `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md` are the live roadmap/lifecycle authorities.
