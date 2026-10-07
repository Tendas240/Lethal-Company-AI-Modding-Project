# S1.42AK-DRDIAG1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES MATERIALIZED ON PUBLICATION BRANCH / MAIN INTEGRATION PENDING / NOT CANONICALLY INDEXED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Date:** 2026-10-05  
**Authorization:** `Current/270_S1.42AK_DRDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`  
**Reviewed build head:** `5e10e1084425ee7152761d919a0b0ccc57282ff5`  
**Review workflow run:** `37273709334` / #1  
**Frozen Actions artifact:** `11329346796`  
**Artifact name:** `S1.42AK-DRDIAG1-review-5e10e1084425ee7152761d919a0b0ccc57282ff5`  
**Artifact size:** `536836` bytes  
**Artifact ZIP SHA-256:** `6a6ec13a36f9c3f655f025b73ec477e02394caac4831cee3fe395fe2ec24bf63`  
**Published profile SHA-256:** `15587975580ea9de38f995ff2e2a64586977c4c1a32f2c87534011375394c3d4`  
**DRDIAG1 DLL SHA-256:** `512b3085619852ba723163522860cf64f4ace53a6ae09356ae0ad943a59adf3b`  
**Profile identity:** `LC V1 S1.42AK-DRD1`  
**Publication PR:** `#278`  
**Successful publication transport run:** `37277020495` / #1 — **success**  
**Transport-definition commit:** `3777f051b41dc1b788a81afb5ee314ecb730938d`  
**Exact materialization commit:** `57235c9240e4e2237e655e8495b1d44b02442927`  
**Transport-removal commit:** `56f7fb9352b59be909878884dcc89038e8247cd4`

The exact profile at `Profiles/LC V1 S1.42AK-DRD1.r2z` has been materialized on the dedicated publication branch from frozen Actions artifact `11329346796`. No profile or DLL was rebuilt, reconstructed, recompiled, relinked, regenerated, repacked from source or substituted during publication.

## Immediate pre-materialization revalidation

Immediately before the publication transport was triggered, the assistant independently re-downloaded artifact `11329346796` through the GitHub connector into a separate workspace and rehashed its actual bytes:

- Actions metadata: `expired=false`, size **536836** bytes, digest `sha256:6a6ec13a36f9c3f655f025b73ec477e02394caac4831cee3fe395fe2ec24bf63`;
- downloaded ZIP SHA-256: `6a6ec13a36f9c3f655f025b73ec477e02394caac4831cee3fe395fe2ec24bf63`;
- profile member: **576350** bytes, SHA-256 `15587975580ea9de38f995ff2e2a64586977c4c1a32f2c87534011375394c3d4`;
- DLL member: **18432** bytes, SHA-256 `512b3085619852ba723163522860cf64f4ace53a6ae09356ae0ad943a59adf3b`;
- artifact ZIP CRC: **PASS**;
- profile ZIP CRC: **PASS**;
- artifact file count: **4**;
- review profile member count: **338**.

The one-shot publication transport then independently re-downloaded the same artifact by exact numeric ID and verified the same ZIP/profile/DLL hashes before materialization.

## Exact archive/delta verification

The publication transport validated the exact reviewed archive against the canonical indexed S1.42AK-BMDSFIX1 parent snapshot:

- parent profile: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z`;
- parent SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- parent member count: **337**;
- publication member count: **338**;
- first 337 member paths remain in exact parent archive order;
- sole added member: `BepInEx/plugins/S142AKDRDiag1/S142AKDRDiag1.dll`;
- every parent member except `export.r2x` matches the indexed parent SHA-256 byte-for-byte;
- `export.r2x` differs only by the one exact raw identity replacement to `LC V1 S1.42AK-DRD1`;
- embedded DRDIAG1 DLL equals the separately frozen DLL byte-for-byte;
- removed members: **0**;
- package changes: **0**;
- config changes: **0**;
- inherited BMDSFIX1 DLL remains SHA-256 `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- accepted S1.42AB InteriorWeightNormalization remains SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- Gale projected maximum remains **217 / 255 PASS**.

## Readable publication snapshot

A deterministic readable snapshot was derived from the already-frozen profile bytes. This did not reconstruct or rewrite the profile.

`ProfileSources/S1.42AK-DRDIAG1/FILE_INDEX.json` contains:

- **338** archive rows in exact archive order;
- **331** readable text snapshots;
- final row index **337**: `BepInEx/plugins/S142AKDRDiag1/S142AKDRDiag1.dll`, size **18432**, SHA-256 `512b3085619852ba723163522860cf64f4ace53a6ae09356ae0ad943a59adf3b`.

No `ProfileSources/S1.42AK-DRDIAG1/PROFILE_INDEX_RESULT.json` exists at this gate. `Profiles/EXPECTED_HASHES.json` remains unchanged. Therefore this is publication evidence only, **not canonical profile indexing**.

## Protected lifecycle/controller surfaces

Post-materialization branch verification confirms exact Git blob identity to current `main` for:

- `BuildSpecs/current.json`;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- `Current/AUTO_BUILD_RESULT.json`;
- `Current/AUTO_BUILD_RESULT.md`;
- `Profiles/EXPECTED_HASHES.json`.

Therefore S1.42AK remains accepted; S1.42AK-BMDSFIX1 remains active / **NOT ACCEPTED**; its selector-free Black Mesa x `DeepSewersFlow` gate remains passive, outstanding and unwaived; DRDIAG1 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**, not canonically indexed, not Gale-imported and not runtime-armed. Phase-C residual remains **29** and no gameplay run is authorized.

## Transport lifecycle

The temporary `.github/workflows/one-shot-drdiag1-publication.yml` existed only to transport the exact frozen bytes and has already been removed from the publication branch at commit `56f7fb9352b59be909878884dcc89038e8247cd4`. It must remain absent from the final integration head.

Final PR-head validation after the human-authored publication evidence/state commits remains required before merge.
