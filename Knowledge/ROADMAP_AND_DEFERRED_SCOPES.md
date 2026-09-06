# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MANIFEST.json`, `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/MOUTHDOGAI_FOCUSED_DECOMPILE.txt`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`  
**Last-Validated:** 2026-09-06

## Current position

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**. Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact: **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**. Profile SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`.

There is no active runtime candidate and no successor armed. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_MOUTHDOG_V81_CAPTURE_AWAITING_TARGETED_SOURCE_EXTENSION`. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains evidence-attribution only.

## Completed Mouth Dog analysis milestone

The provenance-safe Vanilla V81 MouthDogAI capture has succeeded. The prior `Current/135...AWAITING_RETRY` work state is resolved history; current analysis authority is `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`.

Authoritative capture:

- branch `source-evidence/mouthdog-v81-20260906t121738z`;
- commit `a618b19bfc30234ca556c924d681d43b2c13d1d9`;
- assembly SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- Steam buildid `22825947`;
- evidence under `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`.

The source now proves two native surfaces outside the LethalMin-specific `DoCheckInterval()` mutation dispatcher:

- position-based noise pursuit through `MouthDogAI.DetectNoise(...)`, `noisePositionGuess` and the native lunge transition;
- generic `EnemyAI` collision/lunge/damage through `MouthDogAI.OnCollideWithEnemy(...)`.

Exact LethalMin evidence proves `PikminAI : EnemyAI` and also proves Pikmin can emit `RoundManager.PlayAudibleNoise(...)` at their own position while the current config has `Dont Make Audible Noises = false`.

The runtime evidence proves a Purple Pikmin carried `GoldBar(Clone)`, but the carried GoldBar itself as the causal noise emitter remains unproved and unexcluded.

## Exact next scope

The selected work is now a **targeted source-evidence extension**, not another capture retry, not a new build and not a gameplay run.

Prove only these two remaining contracts:

1. exact Vanilla V81 `EnemyAI.OnCollideWithEnemy()` base behavior and side effects, because the MouthDog override calls the base method before its own generic `EnemyAI` lunge/damage logic;
2. exact LethalMin 1.1.108 `PikminItem.CarryNumerator()` and carry-item audio / `RoundManager.PlayAudibleNoise(...)` callsites, so the narrower carried-scrap/noise causality can be proved or rejected.

Then apply `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and perform a successor-specific safety review. Do not arm/build a successor until that review closes the boundary.

Preserve:

- S1.42AF as the guarded gameplay base;
- the useful S1.42AG prevention-before-mutation result on `MouthDogPikminEnemy.DoCheckInterval()` where applicable;
- enabled native LethalMin ownership for Pikmin -> Mouth Dog attack/latch/death/unlatch/task lifecycle;
- Mouth Dog -> player behavior;
- passive follower non-aggression as normal behavior.

Do not add guessed Harmony targets, broad `EnemyAI` scanning, whole-component disables or manual Pikmin state reconstruction.

## Remaining deferred independent gameplay/compatibility scopes

- **LC Office V81 integration** under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`: add `Piggy-LC_Office 2.3.4` with `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix 2.0.0`, `JacobG5-DestroyItemInSlotFix 1.0.0` and `Alice-DungeonGenerationPlus 1.5.1`; preserve `IAmBatby-LethalLevelLoader 1.7.12` as sole owner; explicitly forbid `pacoito-LethalLevelLoaderUpdated`; do not arm while the selected Mouth Dog compatibility scope remains open;
- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- broader LethalMin teardown/despawn repair only with stronger evidence beyond the selected Mouth Dog interaction.

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
