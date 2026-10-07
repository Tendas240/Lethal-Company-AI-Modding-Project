# C3E3B — Exact Oxyde scene-bundle entrance-component scan

Status: complete bounded static scan; no directly identifiable EntranceTeleport component or entrance-field match; runtime entrance construction and topology unresolved.

## Scope and provenance

- Inspection date: 2026-09-20.
- Repository parent: `60240ddc8d104fda16dcc75453c5732b7c84fc8a` on draft PR #138.
- Verified main: `56355ff518ae4301a38d370be9561251f6f963c1`.
- Accepted baseline: S1.42AK; CodeRebirth 1.6.9.
- Input: `plugins/CodeRebirth/Assets/oxydescene` from the exact CodeRebirth 1.6.9 package verified in C3E3A.
- Bundle: 55,038,216 bytes; SHA-256 `6b6dc42c2bef7d858e7e2efa2573df3e1c2bc8507cc7c3840483f0f6c1b0e883`.
- Package SHA-256: `a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6`.
- C3E3A inventory Git blob: `4d343b00a9f29f854064affd393b0cabffad7ee3`.
- Parser: UnityPy 1.25.3; embedded type trees; no Unity player, game or managed mod code executed.

The input hash chain is recorded in `../PhaseC3E3A/OXYDE_PACKAGE_BUNDLE_INVENTORY.json`, its manifest and toolchain. The accepted package ZIP and both DLLs were independently hash-verified there. This checkpoint consumes that exact extracted scene bundle; it does not repeat C3A–C3D selection analysis.

## Complete serialized coverage

| Check | Result |
| --- | ---: |
| Serialized objects across two files | 20,561 |
| MonoScripts inspected | 52 |
| MonoBehaviours parsed | 965 / 965 |
| MonoBehaviour parse errors | 0 |
| Non-null script references resolved | 963 |
| Null script references | 2 |
| GameObjects parsed | 4,424 / 4,424 |
| GameObject parse errors | 0 |
| MonoScript class named EntranceTeleport | 0 |
| MonoBehaviours matching that class or searched entrance fields | 0 |

The files are `BuildPlayer-Oxyde` and `BuildPlayer-Oxyde.sharedAssets`. Reference resolution retains serialized-file identity: fileID 0 means the local serialized file; positive fileIDs index that file's external-reference table before resolving the pathID. Every non-null MonoBehaviour script reference resolves to an inspected MonoScript.

All parsed MonoBehaviour trees were recursively searched for the exact field names `entranceId`, `isEntranceToBuilding`, `entrancePoint` and `exitPoint`. None matched. All GameObject names were searched case-insensitively for `entrance|fire.?exit|teleport|dungeon`; the only match was `DungeonGenerator`.

These searches are explicitly scoped. They do not establish that every possible subclass, differently named owner mechanism or later runtime-created component has been excluded.

## The two null-script records

Both records belong to GameObject pathID 70, named `DungeonGenerator`, in `BuildPlayer-Oxyde`.

| MonoBehaviour pathID | m_Script | Raw bytes | Serialized fields |
| --- | --- | ---: | --- |
| 18691 | fileID 0 / pathID 0 | 32 | m_GameObject, m_Enabled, m_Script, m_Name |
| 18692 | fileID 0 / pathID 0 | 32 | m_GameObject, m_Enabled, m_Script, m_Name |

Both raw payloads are identical:

`0000000046000000000000000100000000000000000000000000000000000000`

Both reference GameObject 70, have m_Enabled 1 and an empty m_Name. Neither contains serialized entrance IDs or pairing fields. No managed class can be assigned from these null pointers.

The GameObject is active and has components Transform 4494, MonoBehaviour 18692 and MonoBehaviour 18691. Its serialized layer is 0 and tag value is 20013; no tag meaning is inferred. Transform 4494 has no children and references parent Transform 4476. Its local position is (229.60130310058594, -6.126550197601318, -17.99966049194336), local rotation is identity and local scale is (1, 1, 1). This is a local pose, not a computed world pose or an entrance anchor.

Null serialized script pointers are an observation about this asset. They are not by themselves a demonstrated gameplay failure, nor proof that this moon is supposed to run normal dungeon generation.

## Follow-up records and proof boundary

The JSON preserves the full MonoScript inventory, resolved MonoBehaviour class counts, both null-script records and GameObject/Transform context. It also retains 37 records from three observed classes: 16 Dawn.Utils ChanceScript, 20 Dawn.Utils SpawnSyncedDawnLibObject and one Dusk.Utils UnlockProgressiveObject. These are evidence for possible later routing only; this checkpoint does not claim they create entrances.

No moon-side main-entrance ID, fire-exit ID, side flag or entrance/exit transform target can be extracted from the directly identified components in this scene bundle. This is **not** a finding of zero runtime entrances. Other bundles, owner code, runtime additions and the level's actual generation participation are outside this scan.

Consequently no entrance-numbering comparison, pairing compatibility, generation viability, topology safety, traversal, geometry, elevators, routing or NavMesh conclusion is made. The 46 supported selection-layer pairings remain selection-only.

## Reproduction and validation

Install the exact parser dependencies recorded by C3E3A, then run:

```sh
python AnalysisTools/inspect_universal_interior_c3e3b.py --bundle /path/to/oxydescene --out /path/to/output
```

The script rejects a different bundle size/hash or UnityPy version. It statically parses all MonoBehaviours, resolves script pointers and records scan coverage without loading managed assemblies.

Validation confirmed that all 965 MonoBehaviours parsed, 963 resolved references plus two null references account for the entire set, resolved class counts sum to 963, both null records identify GameObject 70 in the main serialized file, and the sole name-search match is DungeonGenerator. The JSON contains the raw observations needed to audit these claims.

## Preserved state and next bounded segment

The source-GUID ledger remains 27 / 192 resolved and 165 unresolved. The authoritative B3 matrix is unchanged. Black Mesa is not registered again; Shatteredrooms exclusions and S1.42AB InteriorWeightNormalization remain unchanged.

Accepted S1.42AK remains active. There is no candidate and no outstanding runtime test. `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`; `RuntimeInbox/ACTIVE_BUILD.txt` remains S1.42AK.

Next: **C3E3C**, inspect the exact `oxydeassets` level definition and Dusk moon-definition records, especially generation participation and scene registration (including `spawnEnemiesAndScrap` if present). Establish whether Oxyde is configured for ordinary dungeon generation before selecting a bounded owner/runtime construction follow-up. Black Mesa 3.4.4 scene topology and DawnLib/LLL/vanilla numbering/pairing comparison remain open.
