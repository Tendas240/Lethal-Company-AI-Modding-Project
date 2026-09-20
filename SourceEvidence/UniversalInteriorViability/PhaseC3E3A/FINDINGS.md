# S1.42AK universal interior viability — Phase C3E3A exact Oxyde package/bundle preparation

**Status:** EXACT PACKAGE VERIFIED / SCENE BUNDLE LOCATED / STATIC READER READY / ENTRANCE EXTRACTION STILL OPEN  
**Date:** 2026-09-20  
**Accepted baseline:** S1.42AK  
**Main authority commit:** `56355ff518ae4301a38d370be9561251f6f963c1`  
**Parent PR checkpoint:** `d5f42a9ac79e4b084f67f5443b2e16b80218b61c`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded result

The exact CodeRebirth 1.6.9 Thunderstore ZIP has been downloaded and independently verified against the repository's native-owner manifest. Its Oxyde scene bundle is present and can be parsed statically with UnityPy 1.25.3. This resolves the package acquisition and static-reader preparation step. It does not extract or classify entrance IDs yet.

## Accepted-version and byte provenance

`ProfileSources/S1.42AK/export.r2x` (Git blob `669cf2bf096544de84be9475de8f3f9eb594ce14`) records `XuXiaolan-CodeRebirth` 1.6.9 as enabled.

Package provenance comes from `SourceEvidence/NativeSpawnOwners/20260911T144505Z/MANIFEST.json` (Git blob `77e77022d3cbdd742d57013f66812c0e8a336c64`). That snapshot was originally collected under S1.42AI; its package identity is reused here only after matching the accepted S1.42AK package version and rechecking the actual downloaded package bytes.

- URL: https://gcdn.thunderstore.io/live/repository/packages/XuXiaolan-CodeRebirth-1.6.9.zip
- ZIP bytes: **263,010,364**.
- ZIP SHA-256: `a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6` — independently matched.
- Both recorded DLL members independently match their existing SHA-256 values. Their code was not executed.

This is exact downloaded package evidence, distinct from the version-matched public Unity-project source used by C3C–C3E2D. It does not assert that all source-project assets are identical to this package.

## Package members found

| ZIP member under plugins/CodeRebirth/Assets/ | Bytes | SHA-256 |
|---|---:|---|
| oxydeassets | 398696 | `86d2ef29d428bcb3b96cb5ec99283a362324f8261c4a8e26737e3bd04fe24fe4` |
| oxydecrashshipassets | 2193570 | `e672f616fc0a415bf4ad586b78ff4b45a8bfe2b96826b5bb4369e9b167f4f685` |
| oxydeloreassets | 6662746 | `f9aff6191e86421b240b4ead69b9e4620f9fd9d4f1d8840866c31ec259b0d606` |
| oxydescene | 55038216 | `6b6dc42c2bef7d858e7e2efa2573df3e1c2bc8507cc7c3840483f0f6c1b0e883` |

All four members have UnityFS format version 8 and Unity revision `2022.3.62f2`; header-declared byte counts match the decompressed ZIP member sizes. Hashes above are computed from the actual uncompressed member bytes, not LFS pointers or source-path guesses.

## Static-reader readiness

`oxydeassets` parses as one serialized file with **48 objects**, including **14 MonoBehaviours**. Its type tree is enabled and one MonoBehaviour typetree probe succeeds.

`oxydescene` parses into:

| Serialized file | Objects | Embedded type tree |
|---|---:|---|
| BuildPlayer-Oxyde.sharedAssets | 973 | enabled |
| BuildPlayer-Oxyde | 19,588 | enabled |

The combined scene-bundle inventory contains **20,561 objects**, including **4,424 GameObjects**, **965 MonoBehaviours**, and **52 MonoScripts**. This object inventory supplies a concrete next extraction surface without requiring a Unity/game runtime.

The scene-bundle sample MonoBehaviour probe succeeds in `BuildPlayer-Oxyde.sharedAssets`, at path ID 963. It is a parser-readiness sample with sky-related fields, not an EntranceTeleport probe and not proof that every scene object or external reference can be resolved. The main scene references its sharedAssets file and Unity default resources. Those dependencies are recorded; comprehensive dependency resolution is not claimed.

`oxydecrashshipassets` and `oxydeloreassets` receive byte/hash/header inventory only in this segment; their object graphs are not parsed.

## Reproducer and validation

`AnalysisTools/inspect_universal_interior_c3e3a.py` takes an existing exact ZIP, verifies its fixed size/hash and both DLL hashes, inventories the four bundles, and statically parses only `oxydeassets` and `oxydescene`. It requires UnityPy 1.25.3. It does not download packages, crawl an extracted directory, start Unity, import a gameplay profile, execute managed assemblies, or extract entrance IDs.

Example from a repository checkout with the pinned Python dependency installed:

```sh
python AnalysisTools/inspect_universal_interior_c3e3a.py --zip /path/to/XuXiaolan-CodeRebirth-1.6.9.zip --out /path/to/inspection-output
```

The actual output is `OXYDE_PACKAGE_BUNDLE_INVENTORY.json`; `TOOLCHAIN.json` records the Python and installed dependency versions. A second run after adding explicit probe-file attribution completed successfully. Exact package/DLL hashes, bundle sizes/headers and object-count totals agree. Raw package/bundle binaries are not added to Git; the exact retrieval URL, expected package hash, member paths, member hashes and reproducer are persisted.

## Preserved proof boundaries and next segment

No EntranceTeleport IDs, outside/inside pairing, entrance counts, generation, traversal or topology safety are proven in C3E3A. The 46 selection-layer pairings gain no topology clearance. The prior source-GUID ledger remains **27/192 resolved, 165 unresolved** and is not presented as complete.

S1.42AK, the authoritative B3 matrix, S1.42AB normalization, Shatteredrooms exclusions, ownership/registration and build/runtime controllers remain unchanged. No candidate or runtime test is armed.

**Next bounded segment — C3E3B:** inspect the exact `oxydescene` MonoScript identities and the MonoBehaviour records that reference EntranceTeleport. Extract their serialized entrance IDs, side flags, GameObject/Transform identity and pointer targets where available. Preserve main-scene versus sharedAssets file identity when resolving references. This remains static evidence; the subsequent Dawn/LLL/vanilla pairing-semantics comparison and Black Mesa 3.4.4 topology remain separate work.
