# S1.42AK universal interior viability — Phase C3E2B structural GUID resolution

**Status:** PARTIAL TOPOLOGY SOURCE CHECKPOINT / THREE STRUCTURAL GUIDS RESOLVED / ENTRANCE IDS STILL OPEN  
**Date:** 2026-09-19  
**Accepted baseline:** S1.42AK  
**Main authority commit:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent PR checkpoint:** `413a3ed412153ae22896e81d39ff94d19e40a611`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded result

This segment resolves exactly the three structural GUIDs left open by C3E2A. It does not repeat C3A-C3D and does not claim completion of the 192-GUID map.

The exact version-matched CodeRebirth 1.6.9 source at `3aec94f6f737c86d5e1eb59a57396740317b210f` contains matching **FBX model sources**. Each adjacent `.fbx.meta` declares `ModelImporter` and exactly the GUID recorded in C3E2A:

| Terrain GUID | Source asset | Meta Git blob |
|---|---|---|
| `4b9261bf2703779478397283d2a5a9e2` | CabinSupport.fbx | `9d1ae294c4a72ca8a39cb813d837e5c288169c19` |
| `f354eba67c9ac1c4faa7ce98cb6ee920` | SallyStairsCollider.fbx | `cc353a62fb0809d971574cfda832ddcc7b78ec06` |
| `e73a244d8e33195448df7390ea94caef` | SallyStairs.fbx | `25cfdce4d8564a43d56a0c2242368488e9d1d801` |

Full paths, exact meta content and exact Git LFS pointer content are preserved in `OXYDE_STRUCTURAL_MODEL_GUID_RESOLUTION.json`.

C3E2A's observation that no same-named **prefab** path exists remains true but did not establish a missing source asset. The terrain's `m_SourcePrefab` references are not limited to standalone `.prefab` files: these three GUIDs resolve to model-import sources. Future GUID resolution must include model metadata as well as prefab metadata; root-name filtering alone is insufficient.

## Payload/proof boundary

All three `.fbx` Git blobs contain **Git LFS pointers**, not model payloads. This checkpoint reads those pointers and the complete importer metadata; it does not download or inspect the LFS payloads. Recorded LFS SHA-256 values identify expected payloads and are not reported as independently verified downloaded hashes.

Neither importer metadata nor an LFS pointer establishes the final runtime component hierarchy. This result does not prove absence of dynamically added or instance-added entrance behavior. It supplies no `EntranceTeleport.entranceId`, entrance count or outside/inside pairing proof.

The source remains version-matched public source, not a claim of byte identity with accepted CodeRebirth package 1.6.9.

## Coverage and unchanged boundaries

- Three previously unresolved structural source paths are now resolved.
- Combined with C3E2A's eleven resolved prefab candidates, all fourteen structural candidate source paths are accounted for.
- The other 178 terrain GUID groups are not completed by these two checkpoints; the complete 192-GUID map remains unfinished.
- Oxyde entrance count, IDs, pairing and topology safety remain `NOT_YET_PROVEN`.
- Black Mesa 3.4.4 topology remains open.
- The 46 supported selection-layer pairings gain no topology clearance.
- No B3 matrix, gameplay/config, S1.42AB normalization, Shatteredrooms exclusion, registration or controller change is made. No candidate or runtime test is authorized.

## Next bounded action

C3E2C: resolve a bounded batch of remaining Oxyde terrain GUIDs using both prefab and model metadata, prioritizing nontrivial component-bearing compositions and recording exact coverage. Do not repeat the eleven C3E2A prefab searches or these three model resolutions. If source composition still does not expose entrance components, move to exact packaged Oxyde scene-bundle evidence. The later comparison with Dawn/LLL/vanilla pairing semantics remains outstanding.
