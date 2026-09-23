# S1.42AK universal interior viability — Phase C3E2a Oxyde structural-prefab topology triage

**Status:** PARTIAL TOPOLOGY SOURCE CHECKPOINT / STRUCTURAL PREFABS TRIAGED / ENTRANCE IDS STILL OPEN  
**Date:** 2026-09-19  
**Accepted baseline:** `S1.42AK`  
**Main authority commit at checkpoint start:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent PR checkpoint:** `62e0bbdd86dc46ae32859b0959bd982cfd6f9312`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded objective

C3E2a narrows C3E1's 192 nested Oxyde terrain-prefab source GUIDs by using the exact serialized PrefabInstance root-name overrides from the version-matched CodeRebirth 1.6.9 terrain prefab, then directly inspects the structurally plausible resolved prefab sources for moon-side `EntranceTeleport` fields.

This checkpoint does not claim that the complete 192-GUID map is resolved and does not inspect Black Mesa.

## Exact source binding

- CodeRebirth source tree: `XuuXiaolan/CodeRebirth@3aec94f6f737c86d5e1eb59a57396740317b210f`;
- Oxyde terrain prefab Git blob: `23bf23b3fb5782b5a268b89ec7783e3c5004f323`;
- the terrain contains 192 distinct nested `m_SourcePrefab` GUID groups.

All 192 GUID groups expose at least one serialized `m_Name` override in the terrain. None of those root names contains an explicit main-entrance/fire-exit/teleport label. A deliberately broad structural-name filter isolated 14 candidates.

## Structural candidates

Eleven of the fourteen candidates were resolved to exact source prefabs and inspected directly:

- `Door` — GUID `018ee60ec7481dd478e0ec3c84a6ca7c`, blob `7c2216f504940640edacf4e7d4dac1102e50e95d`;
- `Outhouse` — GUID `4bc8473a5c03c9b419944511ea4d0d5d`, blob `fd9d818d0adc99d8eec50bf3240bd036f9447004`;
- `JimothyCabinTiled` — GUID `d0b0d663356a6bc4d8123e75472774ed`, blob `7be6426fd138c25b7daf46bd33237df692e1064c`;
- `Minecart` — GUID `dd344d9c110af2f49a4802768ca63ad2`, blob `bef7396a45a382b7abcae463e1baa0a781e69d13`;
- `Sarcophagus` — GUID `2b0b26be9ebf7894c8a4339985cc435a`, blob `febe19caa1ab13405952c624e3ca0889f058d128`;
- `SarcophagusClosed` — GUID `8bd1f1fe7df5f26498b39b31f7785b52`, blob `5954bcd7f98f72a3023c07a89490a480c8308695`;
- `VetChallengesShip` — GUID `af0fe2d3a5f2eef4ab4770e94384b090`, blob `b93ff7d68fad45e229143c2b1af5b8f70a7fb3b0`;
- `Ladder1.5x (2) Tall` — GUID `7fc3884af2ad97b49ad6e8c07a374cfd`, blob `2dbd3dd0a95c4b3c65d693e58504b3b23faddd29`;
- `MansionEnemyEntrySpawn 1` — GUID `9d55255ec6eafdd4cbfac8cbbe01525a`, blob `07a425a854dd909c5750bf16265f3b7a975992c8`;
- `NatureEnemyEntrySpawn 1` — GUID `368ca36696e2da942baeb83aaee28b35`, blob `8f435319c75984fd16c89da5aba7e34ea43204cc`;
- `WorkforceEnemyEntrySpawn` — GUID `8d9d3c3fbc98cc44cb8b80c04ecf2af8`, blob `7737f55e86d24ec05e44a86d6c180b065f237ed8`.

Every one of those exact prefab blobs has zero literal hits for `EntranceTeleport`, `entranceId`, `isEntranceToBuilding`, `MainEntrance`, `FireExit`, `DungeonEntrance`, `entrancePoint`, and `exitPoint`.

The three remaining structurally named GUIDs are:

- `4b9261bf2703779478397283d2a5a9e2` — observed name `CabinSupport`;
- `f354eba67c9ac1c4faa7ce98cb6ee920` — observed name `SallyStairsCollider`;
- `e73a244d8e33195448df7390ea94caef` — observed name `SallyStairs`.

No same-named prefab path exists in the exact 1.6.9 tree, and repository code search does not resolve those GUID strings. Their source paths therefore remain unresolved in this checkpoint.

## Result and proof boundary

This materially reduces the plausible local-source surface: the obvious composite/door/ship/cabin candidates do not carry serialized entrance IDs or pairing flags.

It still does **not** prove Oxyde topology safety or zero entrances. An entrance can remain hidden in a source prefab whose root name is not entrance-like, in an unresolved dependency/base-game prefab, or in packaged scene-bundle composition.

Therefore:

- Oxyde entrance count remains `NOT_YET_PROVEN`;
- Oxyde `entranceId` values remain `NOT_YET_PROVEN`;
- outside/inside entrance pairing remains `NOT_YET_PROVEN`;
- the 46 C3B/C3D selection-layer pairings do not gain topology proof;
- the authoritative B3 matrix, build/runtime controllers, S1.42AB normalizer, Black Mesa registration and Shatteredrooms exclusions remain unchanged.

## Next bounded action

C3E2b should complete the exact GUID-to-asset resolution for the remaining terrain source GUIDs in small connector-safe batches, with special attention to the three unresolved structural GUIDs and any source prefab whose internal composition is non-trivial. If no serialized `EntranceTeleport` fields emerge, move to exact packaged Oxyde scene-bundle evidence rather than inferring safety from source naming.
