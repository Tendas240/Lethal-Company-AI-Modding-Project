# S1.42AK universal interior viability — Phase C3C External owner/scene/topology source checkpoint

**Status:** PARTIAL C3 EVIDENCE / OXYDE OWNER+SCENE PROVEN / ENTRANCE-ID TOPOLOGY UNRESOLVED / NO GAMEPLAY BUILD OR RUNTIME AUTHORIZATION  
**Date:** 2026-09-19  
**Repository source commit:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent checkpoint:** `SourceEvidence/UniversalInteriorViability/PhaseC3B/FINDINGS.md`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Result

This checkpoint resolves the owner and scene-registration path for Oxyde far enough to rule out a second LLL registration path, and it establishes a hard proof boundary around entrance/fire-exit topology for both External target moons.

For **CodeRebirth 1.6.9 / Oxyde**, the exact accepted-package evidence already preserved in `SourceEvidence/NativeSpawnOwners/20260911T144505Z` SHA-256-binds the CodeRebirth package and DLL. The package's decompiled discovery report contains `MoonHandler`, `MoonHandler+OxydeAssets`, `CodeRebirthMoonKeys`, and repeated runtime lookups of `CodeRebirthMoonKeys.Oxyde` through Dawn's `LethalContent.Moons` registry.

The latest upstream source tree that still declares CodeRebirth **1.6.9** is commit `3aec94f6f737c86d5e1eb59a57396740317b210f`, the direct parent of the commit that bumps the project to 1.6.10. At that 1.6.9 tree, `MoonHandler` registers the `oxydeassets` bundle through CodeRebirth's Dusk/Dawn `ContentHandler` path. It does **not** manually construct or register an LLL `ExtendedLevel`. The namespaced key is `code_rebirth:oxyde`, and `OxydeMoonDefinition.asset` binds that key to `OxydeLevel.asset` and scene `Oxyde.unity`.

The Oxyde definition contains one explicit owner tag, `dawn_lib:has_buying_percent`. C3A remains the authority for automatic Dawn 0.9.25 `lethal_company:custom` and `lethal_company:all` tagging; C3B remains the authority for the Dawn-to-LLL bridge and its minimum LLL `Custom` + `All` result.

For **Black Mesa**, the accepted profile remains package-authoritative at **3.4.4** via `export.r2x`, while its generated config header identifies plugin version 3.4.1. The active owner config enables the dungeon and moon and sets the dungeon rule to `lethal_company:vanilla=+100,lethal_company:custom=+100`. C3A already established the Dawn registry key `black_mesa:black_mesa` and the automatic Dawn tag consequences.

A public `PlasteredCrab/BlackMesaLethalCompany` repository exists, but its newest commit is from 2024 and its `Plugin.cs` still declares version 0.9.0 and directly uses LethalLevelLoader. Thunderstore's current 3.4.x changelog states that 3.4.0 switched from LethalLevelLoader to DawnLib for v81. Therefore that public source is **historical only** and cannot be used as exact 3.4.4 registration or topology evidence.

## Oxyde owner registration and scene identity

Version-matched upstream source at CodeRebirth 1.6.9 establishes:

1. `MoonHandler : ContentHandler<MoonHandler>` owns an `OxydeAssets` asset-bundle loader and calls `RegisterContent("oxydeassets", out Oxyde)`.
2. `res/namespaced_keys.json` maps `CodeRebirthMoonKeys.Oxyde` to `code_rebirth:oxyde`.
3. `CodeRebirthContentContainer.asset` contains an `oxydeassets` bundle entry.
4. `OxydeMoonDefinition.asset` binds key `code_rebirth:oxyde` to the Oxyde `SelectableLevel` and to scene `Oxyde.unity` in bundle `oxydescene`.
5. `OxydeLevel.asset` identifies `sceneName: Oxyde`, `levelID: 745`, and `PlanetName: 745 Oxyde`; its serialized legacy `dungeonFlowTypes` list is empty.
6. The accepted runtime observation from C3A that LLL lists 745 Oxyde as `External` is consistent with this Dawn-owned registration followed by the C3B LLL bridge. No duplicate LLL owner registration is indicated.

The upstream source is version-matched, not asserted to be bit-identical to the accepted package DLL. Binary identity remains anchored only for the package/DLL and discovery report already preserved by the native-owner evidence manifest.

## Oxyde entrance/fire-exit source inspection

The committed 1.6.9 Oxyde scene `Oxyde.unity` contains a `DungeonGenerator` object, but its serialized YAML contains no textual `EntranceTeleport`, `entranceId`, `isEntranceToBuilding`, `entrancePoint`, `exitPoint`, `MainEntrance`, `FireExit`, or `DungeonEntrance` fields/names.

The scene instantiates a large terrain prefab, `NewTerrainXuStillABitch.prefab`. Its exact 7,355,812-byte Git blob was also inspected. It likewise contains none of those serialized entrance/fire-exit names or fields. Nested prefab-instance names expose ordinary structural `Door` objects, not evidence of Lethal Company's `EntranceTeleport` IDs.

CodeRebirth's version-matched `EntranceTeleportPatch.cs` hooks `EntranceTeleport.Awake` and `OnDestroy` only to maintain `CodeRebirthUtils.EntrancePoints`. It does not rewrite `entranceId`, `isEntranceToBuilding`, or pairing semantics.

These negative source searches are a proof boundary, **not proof that Oxyde has zero entrances or fire exits**. The final runtime scene can include objects from asset-bundle composition, base-game prefabs, Dawn setup, or other serialized references that are not recoverable as literal field names in the inspected committed YAML. Therefore Oxyde entrance IDs/pairing remain `NOT_YET_PROVEN`.

## Black Mesa 3.4.4 evidence boundary

The exact S1.42AK profile config proves the active settings and generated owner surface, but not the 3.4.4 implementation body. In particular:

- `BlackMesaDungeon Options / Enabled = true`;
- `Black Mesa | Allow Editing Config = true`;
- `Black Mesa | Preset Moon Weights = lethal_company:vanilla=+100,lethal_company:custom=+100`;
- `BlackMesaMoon Options / Enabled = true`;
- `BlackMesaScene | Allow Editing Config = false`.

Thunderstore identifies 3.4.4 as the current package and documents a v81 DawnLib migration beginning in 3.4.0. Its README describes a custom exterior with fire exits, a secret fire-exit shortcut, and a main entrance. Those are useful author-level topology descriptions, but they do not expose the exact `EntranceTeleport` IDs or prove pairing in the accepted 3.4.4 bytes.

The repository does not currently preserve a Black Mesa 3.4.4 package ZIP/DLL decompilation equivalent to the CodeRebirth native-owner snapshot. The available public GitHub source predates the Dawn migration by roughly two years. Accordingly, this checkpoint does not infer 3.4.4 owner implementation or entrance IDs from that obsolete source.

## Matrix and selection consequence

No authoritative B3 matrix cell changes in C3C.

The **44** C3B direct-LLL selection pairings remain supported by the C3B proposed delta, but C3C adds no new selection promotions. It also does not retract those 44 availability results: the new source work concerns owner identity and topology evidence boundaries.

The Black Mesa dungeon's active Dawn-native `vanilla/custom=100` rule is intentionally left for the next bounded selection-rules segment. Its config text alone is not promoted into two new matrix cells until the exact Dawn 0.9.25 matching/guard path is applied end-to-end.

## Proof boundary

This checkpoint proves or strengthens:

- CodeRebirth 1.6.9 owns Oxyde through the Dusk/Dawn content-registration path;
- Oxyde's key, SelectableLevel identity, scene identity and explicit owner tag;
- absence of a CodeRebirth-side entrance-ID rewrite in the inspected version-matched patch;
- the current lack of exact serialized entrance/fire-exit ID evidence in the inspected Oxyde source assets;
- that the public Black Mesa GitHub source is too old to stand in for package 3.4.4.

It does **not** prove:

- exact Black Mesa 3.4.4 implementation bytes or scene serialization;
- main-entrance/fire-exit IDs or pairing for Black Mesa or Oxyde;
- actual dungeon generation, traversal, geometry, elevators/ladders, routing or NavMesh;
- Black Mesa's Dawn-native dungeon selection result on Black Mesa or Oxyde;
- any additional owner/asset-matched or vanilla-native interior viability cells.

## Required next bounded analysis

Continue C3 by tracing the exact DawnLib 0.9.25 native dungeon-weight application for Black Mesa's active `lethal_company:vanilla=+100,lethal_company:custom=+100` rule against the two External target moons. Use the SHA-256-bound C3A method evidence and the now-established target tag/owner facts; determine whether the Black Mesa dungeon itself gains selection-layer `VIABLE_EQUAL_100` support on Black Mesa and Oxyde.

Keep entrance/fire-exit topology as a separate unresolved proof obligation. Do not duplicate-register Black Mesa, do not alter Shatteredrooms exclusions, and do not convert selection availability into generation/traversal proof.

## Checkpoint decision

Phase C3 remains open. No gameplay/config/controller bytes are changed. S1.42AK remains accepted, no Candidate or runtime test is created, and S1.42AB normalization remains unchanged.
