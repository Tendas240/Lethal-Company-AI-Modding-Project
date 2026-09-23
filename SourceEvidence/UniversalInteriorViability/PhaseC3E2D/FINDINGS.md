# S1.42AK universal interior viability — Phase C3E2D nested-source resolution

**Status:** PARTIAL TOPOLOGY SOURCE CHECKPOINT / FIVE TARGETED CHILD PATHS RESOLVED / ENTRANCE IDS STILL OPEN  
**Date:** 2026-09-19  
**Accepted baseline:** S1.42AK  
**Main authority commit:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent PR checkpoint:** `25401b9ccaff1f5bffd4cffbd7938f678e58715e`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded result

The five unbound nested source references identified in C3E2C are now matched by exact GUID to CodeRebirth 1.6.9 metadata at `3aec94f6f737c86d5e1eb59a57396740317b210f`.

| Child | Source GUID | Inspected evidence | Also one of the 192 terrain source groups? |
|---|---|---|---|
| HachimansNote | `7f34442d5c326764a9ad80d9f24d350f` | Complete prefab YAML | No |
| CraneSideLadder | `bdba9a2c03100664886827b6c039008d` | ModelImporter metadata + FBX LFS pointer | No |
| Cranecreteblock | `e9c8a995ff29cd34f9d4e98d646d9cb6` | ModelImporter metadata + FBX LFS pointer | No |
| WaterTowerCollider | `ff93510026b26594e8bd9d737599bde3` | ModelImporter metadata + FBX LFS pointer | No |
| Light | `7c4c76117c6eed74f95157783f0c3862` | Complete prefab YAML | Yes |

The evidence JSON preserves the complete metadata and asset Git blob texts, exact paths, Git blob identities, LFS pointer identities, component class counts and parent-child attribution. All ten read blobs independently reproduce their exact Git SHA-1 (19,889 UTF-8 bytes in total).

## What the two prefab texts establish

`HachimansNote.prefab` has two GameObjects, two Transforms and one MonoBehaviour. The MonoBehaviour on `Decal` serializes material, decal sizing/fading and UV fields. Its script GUID is recorded, but script implementation identity/semantics are not resolved in this segment.

`Light.prefab` has two GameObjects, two Transforms, a MeshFilter, a MeshRenderer, a native Light and one MonoBehaviour with light/shadow configuration fields. Its script GUID and mesh/material references remain distinct from prefab-instantiation references.

Both complete YAML texts contain zero occurrences of `EntranceTeleport`, `entranceId`, `isEntranceToBuilding`, `MainEntrance`, `FireExit`, `DungeonEntrance`, `entrancePoint` and `exitPoint`. Both contain zero `m_SourcePrefab` references and no serialized class-1001 PrefabInstance document. This closes further serialized prefab-instance branching for these two source texts, not all script behavior, external resource semantics or runtime additions.

## What the three model sources do not establish

`CraneSideLadder.fbx`, `Cranecreteblock.fbx` and `WaterTowerCollider.fbx` are Git LFS pointers. Their adjacent metadata declares ModelImporter and matches the exact targeted GUIDs. The model payloads were not downloaded or inspected. The recorded SHA-256 values identify expected LFS objects, not independently verified payload bytes. No zero-hit or no-entrance conclusion is assigned to unread model payloads.

## Exact coverage accounting

All nine child paths from C3E2C's recorded parent-to-child edges are now source-path-resolved: four were resolved before this segment and the remaining five here. That does not close recursive model/script semantics.

Only `Light` also belongs to the 192 terrain source-GUID groups. The other four are nested children, so they do not add four more terrain completions. The new coverage snapshot therefore records **27/192 source paths resolved, 165 unresolved**. Exactly one row changes from C3E2C's ledger; previous evidence remains intact.

## Proof boundaries and next segment

Oxyde entrance count, entrance IDs, outside/inside pairing and topology safety remain `NOT_YET_PROVEN`. Black Mesa 3.4.4 topology and the Dawn/LLL/vanilla pairing comparison remain outstanding. No topology clearance is added to the 46 selection-layer pairings.

No authoritative B3 matrix, gameplay/config, registration, Shatteredrooms exclusion, S1.42AB normalization or controller change is made. S1.42AK remains accepted; no candidate or runtime test is armed.

The targeted nested-source branch is resolved without exposing entrance fields. The next evidence surface is now prioritized as exact package composition rather than first exhausting 165 additional name-selected source paths. The incomplete source-map coverage remains explicit.

**Next bounded segment — C3E3A:** establish exact CodeRebirth 1.6.9 package provenance from the canonical native-owner manifest, locate the Oxyde scene bundle and determine the available static extraction path. Limit that segment to package/bundle evidence preparation; do not start Unity, author a candidate or request a runtime test.
