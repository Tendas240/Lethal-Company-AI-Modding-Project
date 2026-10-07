# S1.42AK universal interior viability — Phase C3E1 Oxyde scene/prefab indirection checkpoint

**Status:** TOPOLOGY SOURCE CHECKPOINT / OXYDE DIRECT SCENE LAYER RESOLVED / ENTRANCE IDS STILL OPEN  
**Date:** 2026-09-19  
**Accepted baseline:** `S1.42AK`  
**Main authority commit at checkpoint start:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent PR checkpoint:** `c7a9673a868f838a2435ed55c651a0e956a41541`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded objective

This checkpoint inspects only the version-matched CodeRebirth 1.6.9 Oxyde scene hierarchy far enough to determine whether moon-side `EntranceTeleport` IDs/pairings are serialized directly in the committed scene or its large terrain prefab.

It does not repeat C3A-C3D selection work and does not inspect Black Mesa 3.4.4 topology yet.

## Exact source binding

C3C already fixed the version-matched CodeRebirth source tree to:

- repository: `XuuXiaolan/CodeRebirth`;
- latest 1.6.9 tree: `3aec94f6f737c86d5e1eb59a57396740317b210f`;
- Oxyde scene blob: `f374dd1ffad448089157f29d58559310e9a7707e`;
- Oxyde terrain prefab blob: `23bf23b3fb5782b5a268b89ec7783e3c5004f323`.

The accepted CodeRebirth package/DLL remains separately SHA-256-bound by the existing native-owner evidence; this source tree is version-matched and is not asserted byte-identical to the accepted package bytes.

## Direct Oxyde scene result

The exact `Oxyde.unity` source contains 22,780 serialized lines and exactly 11 distinct `m_SourcePrefab` GUIDs at its direct prefab-instance layer.

Their observed instance-name overrides classify them as:

- item-spawn helpers;
- outside path nodes;
- NavMesh modifier/collider helpers;
- a workforce enemy-entry spawn;
- an item ship animation container;
- an editor sponge-shader helper;
- the `NewTerrainXuStillABitch` terrain prefab.

None of those direct scene prefab types is an entrance/fire-exit prefab. No direct scene instance exposes an entrance-like name override.

This strengthens C3C's earlier literal-search boundary: the unresolved Oxyde entrances are not hidden among the direct `Oxyde.unity` prefab-instance types.

## Terrain-prefab result

The exact terrain prefab blob is 7,355,812 characters / 201,136 serialized lines. It contains 192 distinct nested `m_SourcePrefab` GUIDs.

A direct search of the terrain serialization returns zero hits for:

- `EntranceTeleport`;
- `entranceId`;
- `isEntranceToBuilding`;
- `MainEntrance`;
- `FireExit`;
- `DungeonEntrance`;
- `entrancePoint`;
- `exitPoint`.

The exact 1.6.9 Git tree also contains no Oxyde asset path whose filename/path is entrance-, fire-exit-, exit- or teleport-named. The only repository path directly named for `EntranceTeleport` is the CodeRebirth patch already inspected in C3C; that patch tracks instances and does not rewrite IDs/pairing.

## Proof boundary

This does **not** prove that Oxyde has zero entrances or fire exits.

A nested prefab source can carry an `EntranceTeleport` component without repeating the component's serialized fields in the parent prefab instance. Base-game/dependency prefab references or asset-bundle composition can therefore still supply the runtime entrance objects.

Accordingly:

- Oxyde main-entrance/fire-exit count remains `NOT_YET_PROVEN`;
- Oxyde `entranceId` values remain `NOT_YET_PROVEN`;
- Oxyde outside/inside pairing remains `NOT_YET_PROVEN`;
- no topology-safety conclusion is drawn for any of the 46 selection-layer pairings.

## Next bounded topology action

Resolve the 192 terrain-prefab source GUIDs against the exact 1.6.9 Unity-project `.meta` GUID map and inspect only the resolved prefab sources that can plausibly carry entrance/exit behavior. If that still does not expose the moon-side `EntranceTeleport` components, the next evidence surface is the exact packaged Oxyde scene bundle rather than another broad source search.

Black Mesa 3.4.4 remains a separate subsequent topology segment.

No matrix, build, runtime controller, S1.42AB normalization rule, Black Mesa registration path or Shatteredrooms exclusion is changed by this checkpoint.
