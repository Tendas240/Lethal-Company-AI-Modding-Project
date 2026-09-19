# S1.42AK universal interior viability — Phase C3E2C composite-source batch

**Status:** PARTIAL TOPOLOGY SOURCE CHECKPOINT / 12 MORE TERRAIN GUIDS RESOLVED / ENTRANCE IDS STILL OPEN  
**Date:** 2026-09-19  
**Accepted baseline:** S1.42AK  
**Main authority commit:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent PR checkpoint:** `a6c84e6e89d8b269d177071258c7489a3ac3326a`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded result

Twelve additional terrain source GUIDs are bound to exact CodeRebirth 1.6.9 source assets at `3aec94f6f737c86d5e1eb59a57396740317b210f`. The batch prioritizes composite structures, interaction/NPC objects and navigation helpers; names are only a search heuristic, never proof of identity or safety.

| Source | GUID | Evidence kind |
|---|---|---|
| OffMeshLink.prefab | `62251f173dbdf2c4eb66b14199b28043` | Prefab YAML inspected |
| GiftForGuardsman.prefab | `4fbfa31359a2b8c4e9e15ca705546b74` | Prefab YAML inspected |
| Jimothybabyboy.prefab | `bf118ce4bee444c48b81119847abdd6c` | Prefab YAML inspected |
| CratesSpawn.prefab | `c48d3516e654cef4da603caa740245f0` | Prefab YAML inspected |
| SafeBridge.prefab | `837869c64a267234a88e34027dcfbf56` | Prefab YAML inspected |
| Crane.prefab | `a80308eb2adefe149ad85a16a562dcb2` | Prefab YAML inspected |
| RadioTower.prefab | `302f922156e6fcc4f9df8fea106ad936` | Prefab YAML inspected |
| WaterTower.prefab | `bda9c03d997b3a84ab50549257a92bad` | Prefab YAML inspected |
| OxydeBobby.prefab | `df462f0ae7396094fb23763c4521c40f` | Prefab YAML inspected |
| DoomsdayClock.prefab | `d80fcfb0e89ef0a4ea6ce83c79e06803` | Prefab YAML inspected |
| MerchantBase.fbx | `f469f9dc199594a41b1caff572c8f462` | FBX LFS pointer only |
| SellingSally.prefab | `e4efbd87b159f874696f209f5debefa2` | Prefab YAML inspected |

All eleven prefab YAML texts contain zero literal occurrences of `EntranceTeleport`, `entranceId`, `isEntranceToBuilding`, `MainEntrance`, `FireExit`, `DungeonEntrance`, `entrancePoint` and `exitPoint`. These are direct serialization results, not a proof that the final compositions contain no entrances.

`MerchantBase.fbx` is a Git LFS pointer. Its model payload was not read, and no zero-hit conclusion is assigned to that unread payload.

## Exact identity and verification

The exact terrain blob was read and its class-1001 PrefabInstance documents grouped by `m_SourcePrefab` GUID, reproducing 192 groups. Serialized `m_Name` overrides were retained as observed names; an override can name a descendant rather than the instance root.

Twenty-three prefab/model metadata candidates were read. Twelve match terrain source GUIDs. The duplicate `Crane` candidates demonstrate why filename matching is insufficient: the autonomous crane add-on uses different GUIDs; the terrain uses the Oxyde Structures/Crane prefab.

All 35 fetched candidate metadata and selected source-asset texts (295,692 UTF-8 bytes) were independently checked against their Git blob SHA-1 using Git's blob header and exact content. All matched. The evidence JSON preserves all candidate metadata texts and the selected asset blob identities. Version alignment is not a claim of byte identity with the accepted Thunderstore package.

## Nested composition remains open

The inspected prefabs contain nine distinct parent-to-child source-GUID edges. Three child model paths are resolved by this batch's metadata, and the ladder child was already source-inspected in C3E2A. Five child paths remain unbound:

| Parent | Observed child name | Child GUID |
|---|---|---|
| GiftForGuardsman.prefab | HachimansNote | `7f34442d5c326764a9ad80d9f24d350f` |
| Crane.prefab | Cranecreteblock | `e9c8a995ff29cd34f9d4e98d646d9cb6` |
| Crane.prefab | CraneSideLadder | `bdba9a2c03100664886827b6c039008d` |
| Crane.prefab | Light | `7c4c76117c6eed74f95157783f0c3862` |
| WaterTower.prefab | WaterTowerCollider | `ff93510026b26594e8bd9d737599bde3` |

Script GUIDs are recorded per inspected prefab but their implementation semantics are not resolved here. Runtime-added components, prefab inheritance/instance additions and packaged scene composition remain potential evidence surfaces. No recursive closure or topology safety is asserted.

## Coverage ledger

`OXYDE_TERRAIN_GUID_COVERAGE.csv` materializes all 192 source-GUID groups with observed names, instance counts, exact resolved paths/blobs where known and checkpoint attribution:

- 14 source paths carried from C3E2A/C3E2B;
- 12 newly resolved source paths;
- **26/192 source paths resolved; 166 still unresolved**;
- source-path resolution is explicitly separate from component inspection and topology proof.

Nested child GUIDs do not automatically increase the 192-group resolution count. For example, the nested `Light` GUID is also an unresolved terrain source group; it must only be counted once when resolved.

## Preserved boundaries and next segment

Oxyde entrance count, entrance IDs, outside/inside pairing and topology safety remain `NOT_YET_PROVEN`. Black Mesa 3.4.4 topology and the later Dawn/LLL/vanilla pairing comparison remain outstanding. The 46 selection-layer pairings gain no topology clearance.

No authoritative B3 matrix, gameplay/config, registration, Shatteredrooms exclusion, S1.42AB normalization or controller change is made. S1.42AK remains accepted, with no candidate or runtime test armed.

**C3E2D:** resolve only the five unbound nested references listed above and inspect their available serialized composition. Keep nested-child coverage distinct from terrain-group coverage. If committed source cannot expose entrance components, proceed in a later bounded segment to exact packaged Oxyde scene-bundle evidence.
