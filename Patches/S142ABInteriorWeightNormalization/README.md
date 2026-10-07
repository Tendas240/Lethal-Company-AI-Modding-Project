# S1.42AB Interior Weight Normalization

Project-local, fail-closed LethalLevelLoader compatibility patch for the S1.42AB candidate.

## Goal

Preserve LethalLevelLoader's own viability/exclusion decision, then normalize only the positive rarity values of the dungeon flows that LethalLevelLoader has already returned as viable.

Target effective rule:

- not returned by LLL -> remains unavailable;
- returned with rarity 20/25/35/50/70/75/100/250/275/300/etc. -> becomes 100;
- no new flow is registered or appended;
- no flow is removed or deduplicated;
- no matching/config list is rewritten;
- no Enemy/Scrap/MapObject rarity system is touched.

## Exact runtime target

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

A Harmony Postfix runs after LLL has completed all native LevelMatchingProperties evaluation. It mutates only the `rarity` field of entries already present in the returned `List<ExtendedDungeonFlowWithRarity>`.

The built-in LLL debug report is emitted inside the original method before the Postfix executes, so it can still display the original author weights. S1.42AB therefore emits its own authoritative post-normalization marker:

`[InteriorWeightNormalization] Final effective viable pool ...`

That marker is the runtime acceptance evidence for the final selection weights.

## Fail-closed contract

The patch refuses to arm unless all of the following match the frozen S1.42Z baseline:

- BepInEx plugin GUID `imabatby.lethallevelloader` is loaded;
- LethalLevelLoader version is exactly `1.7.12`;
- the exact static two-parameter target exists;
- its return type is exactly `List<ExtendedDungeonFlowWithRarity>`;
- `ExtendedDungeonFlowWithRarity.rarity` is an `Int32` field;
- `ExtendedDungeonFlowWithRarity.extendedDungeonFlow` has the expected type;
- `ExtendedDungeonFlow.DungeonName` is a readable string property;
- the project-local Postfix is confirmed in Harmony's patch table after patching.

If a returned viable entry unexpectedly has a non-positive rarity, that entry is not promoted; it is preserved and an error marker blocks candidate acceptance pending investigation.

## Safety / scope

This patch does not skip the original method and does not replace LLL matching logic. It has no Prefix or Transpiler. It does not touch networking, generation, dungeon registration, config files, enemy pools, scrap pools, Pikmin, BCMER, CodeRebirth, Jetpack behavior, CullFactory, or map-specific NavMesh behavior.

The documented Shatteredrooms Experimentation/Embrion compatibility exclusion remains owned by the upstream viability decision. If LLL excludes Shatteredrooms on a level, S1.42AB never sees or adds it.

Rollback is the accepted S1.42Z profile.
