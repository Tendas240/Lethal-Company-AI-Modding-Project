# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md`, `Current/130_LETHALMIN_1.1.108_MOUTHDOG_SOURCE_CONTRACT_DECOMPILE.txt`, `Current/131_MOUTHDOG_PIKMIN_PATCH_BOUNDARY_AND_SUCCESSOR_PLAN.md`, `Current/132_MOUTHDOG_PATCH_SAFETY_REVIEW.md`, `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-06

## Current position

Accepted gameplay baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**. Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. Runtime acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`.

Latest built artifact: **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**. Profile SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`. Rejection authority: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`. Runtime evidence: `RuntimeEvidence/S1.42AG/20260906T085500Z/`.

There is now **no active runtime candidate** and **no successor armed**. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AG_RUNTIME_REJECTION_AWAITING_TARGETED_ANALYSIS` and guards accepted S1.42AF. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains only the last runtime-evidence attribution target.

S1.42AD remains runtime-rejected historical provider-contract evidence. S1.42AE remains superseded for packaging after its physically present SoundAPI binding was blocked through a 262-character runtime path. S1.42AF reused the corrected source on a 226-character path and passed both normal startup and the exact 18 Moon / 18 Interior Functional Microwave runtime contract.

## Exact next scope

The selected work is now **targeted repository-native analysis of the remaining Mouth Dog targeting/attack path**, not a new build and not a repeat of the already-proven `DoCheckInterval()` source analysis.

S1.42AG proved a useful but incomplete boundary:

- its `Priority.First` prefix on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` armed and executed;
- the prior LethalMin `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab-death-timer mutation path was absent;
- the prior 707 `Work state with no task assigned!` warning aftermath fell to 0;
- the inherited S1.42AF Functional Microwave contract remained healthy.

However, the user directly observed a Mouth Dog visibly target and attack a scrap-carrying Purple Pikmin. The same encounter contains repeated native Mouth Dog `Heard noise!` / `targetPos` diagnostics. Those lines support investigation of a second/native path but do not yet prove its exact owner or whether the carried scrap was the trigger.

Reverse-direction Pikmin -> Mouth Dog combat was **not actively exercised** in this run. No Pikmin was deliberately thrown/assigned onto the Mouth Dog; nearby follower Pikmin remaining passive is expected normal behavior and is not evidence of a defect. Reverse-direction attack/latch/death-unlatch behavior therefore remains a future deliberate runtime validation gate, not part of the current failure finding.

The next analysis must therefore determine the exact current owner/method/path for the remaining Mouth Dog -> Pikmin target/attack behavior, including the carried-scrap/noise possibility, while preserving:

- the enabled `MouthDogPikminEnemy` adapter;
- native Pikmin -> Mouth Dog combat/latch/death cleanup;
- Mouth Dog -> player attacks;
- the proven S1.42AG prevention-before-mutation concept where it remains valid.

Do not add guessed fallbacks, broad EnemyAI scanning, or a whole-component disable. Do not arm/build a successor until the exact remaining Mouth Dog -> Pikmin boundary is proved under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

## Remaining deferred independent gameplay/compatibility scopes

- **LC Office V81 integration** under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`: add `Piggy-LC_Office 2.3.4` with `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix 2.0.0`, `JacobG5-DestroyItemInSlotFix 1.0.0` and `Alice-DungeonGenerationPlus 1.5.1`; preserve `IAmBatby-LethalLevelLoader 1.7.12` as sole owner; explicitly forbid `pacoito-LethalLevelLoaderUpdated`; do not arm while the selected Mouth Dog compatibility analysis remains open;
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

Current full-normal-stack evidence also proves `Art Gallery (MuseumInteriorFlow)` and `Rubber Rooms (RubberRoomsFlow)` register, are viable on Offense, and reach final effective rarity `100`. Their lack of observed natural rolls is therefore not evidence of a weight-configuration defect.

LC Office remains a separate deferred integration scope. Its first candidate must prove modern-LLL registration/viability and actual Office generation before any separate universal-moon availability tuning is considered.

Author/technical viability restrictions, CullFactory compatibility, Mausoleum fog and route/NavMesh recovery remain separate.

## Repository-overhaul boundary

The overhaul is closed and validated. Future repository-architecture changes remain separate from gameplay changes and must continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves historical planning/package research only. This file plus `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md` are the live roadmap/lifecycle authorities.
