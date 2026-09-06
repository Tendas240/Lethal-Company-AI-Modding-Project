# Deferred LC Office V81 Integration Plan

**Status:** DEFERRED / PLANNED / NOT ARMED  
**Date:** 2026-09-06  
**Prerequisite:** close the active S1.42AG runtime gate before selecting or arming this scope  
**Topic authority:** `Knowledge/INTERIORS_AND_LLL.md`

## Objective

Add LC Office as a normal Interior Dungeon under the project's existing LethalLevelLoader ownership and equal-effective-weight architecture, without introducing the deprecated `pacoito-LethalLevelLoaderUpdated` fork and without changing Wesley's Interiors or unrelated interior balance.

This document is a deferred integration contract only. It does not authorize a build and must not change `BuildSpecs/current.json` or `RuntimeInbox/ACTIVE_BUILD.txt` while S1.42AG remains the active runtime candidate.

## External package contract researched 2026-09-06

Target package set:

- `Piggy-LC_Office` `2.3.4`;
- `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix` `2.0.0`;
- `JacobG5-DestroyItemInSlotFix` `1.0.0`;
- `Alice-DungeonGenerationPlus` transition from current `1.5.0` to `1.5.1`.

The V81 compatibility fix declares the modern `IAmBatby-LethalLevelLoader` path and explicitly advises removing/disabling `LethalLevelLoaderUpdated`. It also declares LC Office 2.3.4, FixPluginTypesSerialization, LethalModDataLib, DungeonGenerationPlus 1.5.1, SmartEnemyPathfinding, PathfindingLib, JLL and DestroyItemInSlotFix as its compatibility stack.

The current S1.42AG profile already contains compatible/newer versions of the following required infrastructure:

- `BepInEx-BepInExPack` `5.4.2305`;
- `Evaisa-FixPluginTypesSerialization` `1.1.4`;
- `IAmBatby-LethalLevelLoader` `1.7.12`;
- `MaxWasUnavailable-LethalModDataLib` `1.2.2`;
- `JacobG5-JLL` `1.10.1`;
- `Zaggy1024-SmartEnemyPathfinding` `0.0.4`;
- `Zaggy1024-PathfindingLib` `2.4.1`.

`Alice-DungeonGenerationPlus` `1.5.1` is a narrow follow-up to the installed V81-compatible `1.5.0`; its published changelog states that 1.5.1 fixes the first main path not using the main room's doorway groups.

## Hard ownership / packaging guards

The eventual build must preserve all of the following:

1. `IAmBatby-LethalLevelLoader` `1.7.12` remains the sole LethalLevelLoader owner in the profile.
2. `pacoito-LethalLevelLoaderUpdated` must be absent from the final Gale export and must not load at runtime.
3. If Thunderstore dependency resolution for `Piggy-LC_Office 2.3.4` attempts to add the deprecated fork, the build operation must explicitly remove/refuse it before candidate publication.
4. Do not replace IAmBatby's LLL with the deprecated fork.
5. Do not change the accepted S1.42AB Interior Weight Normalization plugin or its post-viability normalization contract.
6. Do not alter Wesley's Interiors, Art Gallery, Rubber Rooms, Shatteredrooms, Junkrooms, Black Mesa, Mausoleum or other unrelated interior configs as part of this scope.
7. Do not combine the optional DunGenReferenceFixer replacement/fork evaluation with LC Office integration.

## Intended exact package delta

Relative to whichever profile is the accepted full-normal-stack baseline when this scope is actually selected:

### Add

- `Piggy-LC_Office` `2.3.4`;
- `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix` `2.0.0`;
- `JacobG5-DestroyItemInSlotFix` `1.0.0`.

### Version transition

- remove/disable `Alice-DungeonGenerationPlus` `1.5.0`;
- add/enable `Alice-DungeonGenerationPlus` `1.5.1`;
- final export must contain only the intended active DungeonGenerationPlus version.

### Explicitly forbidden

- `pacoito-LethalLevelLoaderUpdated` in any enabled or packaged state;
- any second LethalLevelLoader owner;
- unrelated package upgrades;
- Wesley compatibility/weight changes;
- forced LC Office universal moon availability in the initial integration candidate.

## Initial configuration policy

The first LC Office candidate should preserve the package/modern-LLL viability contract rather than immediately overriding it with a universal manual moon list.

The accepted project rule remains:

- LLL decides whether LC Office is viable on the current moon;
- if LLL returns LC Office with a positive rarity, the S1.42AB-derived project-local postfix normalizes its final effective rarity to exactly `100`;
- no new registration, deduplication or membership-forcing logic is added by the normalization plugin.

If later evidence shows that LC Office has overly narrow author matching and the user wants universal availability, that is a separate balance/configuration scope after compatibility is proven.

## Required pre-build assertions when armed

Before publishing a candidate, the build workflow/spec must prove:

- exact guarded accepted base SHA-256;
- target package versions above are present/enabled as intended;
- `IAmBatby-LethalLevelLoader 1.7.12` remains present/enabled;
- `pacoito-LethalLevelLoaderUpdated` is absent from final export text/package state;
- no unintended package-version cascade occurred;
- no existing interior configuration changed unless explicitly documented by the selected build spec;
- the S1.42AB Interior Weight Normalization plugin remains present unchanged unless a later accepted baseline legitimately changes its binary through another scope.

## Runtime acceptance gate

A future LC Office candidate is not accepted from startup or registration alone. Runtime validation must prove all of the following under the full normal stack:

1. normal BepInEx -> main menu -> lobby startup with no duplicate LLL owner and no `LethalLevelLoaderUpdated` load;
2. LC Office registers exactly once with modern IAmBatby LLL;
3. LLL reports LC Office as viable on at least one tested moon under the candidate's unforced/default matching contract;
4. the project-local final effective viable-pool marker shows LC Office at exactly `100` whenever it is returned viable;
5. an actual LC Office dungeon is selected and generation completes without softlock/fatal error;
6. the player can enter and traverse the generated office;
7. LC Office elevator functionality is exercised successfully;
8. breaker/power interaction is exercised successfully where available;
9. ordinary enemy spawning/navigation inside the office is healthy, including door/elevator pathing where practical to exercise;
10. ordinary scrap/interior generation remains healthy;
11. inherited accepted gameplay contracts remain healthy, including the current accepted Interior Weight Normalization and whichever Mouth Dog/Pikmin state has been accepted before this scope is armed;
12. no new project-critical regression or persistent error flood appears.

Because a normal equal-weight pool may contain 40+ viable interiors, a dedicated diagnostic force-selection mechanism may be used to obtain LC Office runtime coverage if necessary. Such diagnostic forcing must be isolated from the final candidate and must never be promoted as the accepted balanced profile.

## Wesley evidence boundary

This scope is not a repair for Wesley's Interiors. Current runtime evidence already proves both `Art Gallery (MuseumInteriorFlow)` and `Rubber Rooms (RubberRoomsFlow)` register, are viable on Offense, and reach the project-local final pool at effective rarity `100`. Their lack of observed user rolls is therefore not evidence of an incorrect configured spawn weight.

## Arming rule

Do not assign a successor build ID yet. The eventual build must be based on the then-current **accepted** full-normal-stack artifact, not automatically on an unaccepted candidate. If S1.42AG is accepted, it may become that base; if it is rejected, this LC Office plan must wait for the lifecycle to resolve the accepted base first.
