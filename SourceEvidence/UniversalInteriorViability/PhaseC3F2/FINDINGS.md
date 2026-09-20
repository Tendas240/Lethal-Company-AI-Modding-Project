# C3F2 — exact Black Mesa 3.4.4 package capture and static entrance surface

**Status:** EXACT 3.4.4 PACKAGE CAPTURED / PACKAGE+DLL+BUNDLES HASH-BOUND / MOON+SCENE DEFINITION RESOLVED / SIX SERIALIZED ENTRANCE TELEPORTS RESOLVED / RUNTIME PAIRING LOGIC STILL OPEN  
**Date:** 2026-09-20  
**Accepted baseline:** S1.42AK  
**Parent PR head:** `6a308c0b39236985a843236e843aeca28dfed884`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded objective

C3F2 implements and validates the fail-closed repository-native acquisition path required by C3F1. It obtains exactly `Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior 3.4.4`, binds its package bytes, inventories the implementation and UnityFS surface, resolves the Dusk moon/scene definition and records directly serialized `EntranceTeleport` fields.

This remains source/static evidence. It does not change the B3 matrix and does not authorize a gameplay build or runtime test.

## Reproducible capture

The repository now contains:

- `AnalysisTools/inspect_universal_interior_c3f2.py`;
- `.github/workflows/black-mesa-344-topology-evidence.yml`.

After the first successful discovery capture, the helper was hardened to require the measured exact package size and SHA-256 plus the exact manifest name/version/website. The canonical repeated capture is workflow run **35518348054 / #2**, executed for PR head `6a308c0b39236985a843236e843aeca28dfed884`, and completed successfully with no fatal parser/layout ambiguity.

The workflow artifact is ID **10607691761**, digest `sha256:8139301f0e4605d84266ab5edfdeaf3ef4884fe04e76b5b8460b400b475369ea`. Its compact raw derived report is 873,634 bytes with SHA-256 `0b4e3a2bad887da6631e9c8f79cdd74ce8a42294fb62fa0d387a5458d1d9e6fd`. Raw package/DLL/bundle bytes are not committed.

## Exact package identity and bytes

Exact package:

- namespace: `Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior`;
- manifest name: `Black_Mesa_Half_Life_Moon_Interior`;
- version: **3.4.4**;
- archive size: **228,214,268 bytes**;
- archive SHA-256: `12921825bee51bfd46582989322a1f31183b65f59293c73654a102fb68d068b7`.

There is one implementation DLL:

- `BepInEx/plugins/BlackMesa.dll`;
- 143,360 bytes;
- SHA-256 `a90f157becdc68ab7fe6898eefc2feaee98352a0f04b2cda414741729a048eef`.

Seven UnityFS members are present and individually hash-bound in `BLACK_MESA_344_STATIC_TOPOLOGY.json`. The two topology-critical bundles are:

- `blackmesamoon` — 33,612,583 bytes, SHA-256 `b67a127bb9954c32244e019ba2b6118e72f75d9e37d3e92f060def50f303e062`;
- `blackmesadungeon` — 178,159,643 bytes, SHA-256 `6c93ec27a34ac60e1a19f2f13c245392c0474a7e0e32b0b8eae1379385deec70`.

## Exact Dusk moon and dungeon definitions

The current package's moon definition is directly serialized as:

- class: `DuskMoonDefinition`;
- name: `BlackMesaMoonDefinition`;
- key: `black_mesa:black_mesa`;
- level: `BlackMesaLevel`;
- planet: `Black Mesa`;
- level ID: 1;
- scene name: `BlackMesaScene`;
- `spawnEnemiesAndScrap = true`;
- factory-size multiplier: 3.25.

Its exact scene registration is:

- scene path: `Assets/LethalCompany/Mods/BlackMesaMoon/Scenes/BlackMesaScene.unity`;
- scene key: `black_mesa:blackmesascene`;
- bundle: `blackmesamoon`.

The current package's interior definition is directly serialized as:

- class: `DuskDungeonDefinition`;
- name: `BlackMesaDungeonDefinition`;
- key: `black_mesa:black_mesa`;
- flow asset: `Black Mesa`;
- flow bundle: `blackmesadungeon`.

The packaged definition also contains a Black-Mesa-moon weight entry with numeric weight 300. That is package asset state; accepted editable config/owner behavior remains governed by the already-established C3D evidence and is not reclassified here.

## Exact serialized EntranceTeleport surface

The complete static UnityFS scan found **six** directly readable `EntranceTeleport` MonoBehaviours with no relevant parser failure.

Dungeon bundle:

| GameObject | entranceId | isEntranceToBuilding |
|---|---:|---:|
| `EntranceTeleportA` | 0 | false |
| `EntranceTeleportB` | 1 | false |

Black Mesa moon scene:

| GameObject | entranceId | isEntranceToBuilding |
|---|---:|---:|
| `EntranceTeleportA` | 0 | true |
| `EntranceTeleportB` | 1 | true |
| `EntranceTeleportC` | 2 | true |
| `EntranceTeleportD` | 3 | true |

Thus the exact static package contains opposite-side serialized IDs 0 and 1, while moon-side IDs 2 and 3 have no directly serialized dungeon-side `EntranceTeleport` counterpart in the scanned package bundles.

That asymmetry is a **static serialization fact**, not yet a runtime failure finding.

## Proof boundary

C3F2 does **not** yet establish what happens to moon-side IDs 2 and 3 at runtime. In particular, the exact `BlackMesa.dll` has not yet been inspected for:

- creation or cloning of additional `EntranceTeleport` objects;
- rewriting of `entranceId` or `isEntranceToBuilding`;
- custom shortcut/fire-exit pairing;
- patches around vanilla/Dawn/LLL entrance matching;
- special handling of `EntranceTeleportC/D`.

Therefore C3F2 does not claim that C/D are stranded, broken, incompatible or ordinary fire exits. It also does not yet prove that arbitrary registered interiors can safely replace the Black Mesa interior on the Black Mesa moon.

The package's `spawnEnemiesAndScrap=true` does distinguish Black Mesa from the already-closed Oxyde false-generation gate, but generation eligibility alone does not satisfy the entrance/topology compatibility contract.

## C3F2 decision

C3F2's acquisition/capture gate is complete:

- exact 3.4.4 package bytes are reproducibly bound;
- exact current implementation DLL is bound;
- all seven UnityFS bundles are inventoried and bound;
- Dawn/Dusk moon and scene identity are exact;
- the package's static moon/dungeon entrance-ID surface is exact;
- no B3 matrix cell changes;
- no gameplay build or runtime test is authorized.

Black Mesa moon topology is now **partially resolved**, with one sharply bounded remaining question: whether exact `BlackMesa.dll` or its integration layer supplies runtime semantics that reconcile moon-side entrance IDs 2/3 with the generated dungeon.

## Next bounded segment

**C3F3:** inspect the exact SHA-256-bound `BlackMesa.dll` for `EntranceTeleport` creation/rewrite/matching, ID 2/3 handling, shortcut/fire-exit behavior and relevant Harmony/Dawn hooks. Use exact-binary evidence and fail closed on unavailable method bodies or ambiguous decompilation.

Do not change the B3 matrix, do not duplicate-register Black Mesa, and do not request a gameplay run.
