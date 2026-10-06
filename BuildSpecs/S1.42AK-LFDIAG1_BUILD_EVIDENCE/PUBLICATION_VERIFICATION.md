# S1.42AK-LFDIAG1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES MATERIALIZED ON PUBLICATION BRANCH / MAIN INTEGRATION PENDING / NOT CANONICALLY INDEXED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Date:** 2026-10-06  
**Authorization:** `Current/282_S1.42AK_LFDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`  
**Reviewed build head:** `1a57702777eb63e7f1fd4571a67f09e705457c6f`  
**Review workflow run:** `37435859117` / #1  
**Frozen Actions artifact:** `11399366599`  
**Artifact name:** `S1.42AK-LFDIAG1-review-1a57702777eb63e7f1fd4571a67f09e705457c6f`  
**Artifact size:** `536867` bytes  
**Artifact ZIP SHA-256:** `ca1922b3b59666cfd5f8a6105dec9e1dfddf367874be4d3a324bfd8dfacf0b93`  
**Published profile SHA-256:** `ce6835944f90e1972caebf52dc344bdf660283c9a074ac07899486ce0b4564f4`  
**LFDIAG1 DLL SHA-256:** `13fd01cba6d30a0c9044d43df813b17adf352139f723c9444f8db14403a0a474`  
**Profile identity:** `LC V1 S1.42AK-LFD1`  
**Publication PR:** `#294`  
**Successful publication transport run:** `37444290626` / #1 — **success**  
**Transport-definition commit:** `129e456da9df4fa223d3899a6c9a4ed141dd61cc`  
**Exact materialization commit:** `8ba511c9d3a7ddd3d1fe859a021553b0c34edeb6`  
**Transport-removal commit:** `129a5d5b2c303df068ea257265e353db0e862f72`

The exact profile at `Profiles/LC V1 S1.42AK-LFD1.r2z` has been materialized on the dedicated publication branch from frozen Actions artifact `11399366599`. No profile or DLL was rebuilt, reconstructed, recompiled, relinked, regenerated, repacked from source or substituted during publication.

## Immediate pre-materialization revalidation

Immediately before the publication transport was triggered, the assistant independently re-downloaded artifact `11399366599` through the GitHub connector into a separate workspace and rehashed its actual bytes:

- exact numeric artifact ID downloaded: **11399366599**, actual ZIP size **536867** bytes;
- downloaded ZIP SHA-256: `ca1922b3b59666cfd5f8a6105dec9e1dfddf367874be4d3a324bfd8dfacf0b93`;
- profile member: **576368** bytes, SHA-256 `ce6835944f90e1972caebf52dc344bdf660283c9a074ac07899486ce0b4564f4`;
- DLL member: **18432** bytes, SHA-256 `13fd01cba6d30a0c9044d43df813b17adf352139f723c9444f8db14403a0a474`;
- artifact ZIP CRC: **PASS**;
- profile ZIP CRC: **PASS**;
- artifact file count: **4**;
- review profile member count: **338**.

The one-shot publication transport then independently re-downloaded the same artifact by exact numeric ID and verified the same ZIP/profile/DLL hashes before materialization.


## Superseded artifact exclusion

Artifact `11398652708` (run `37436398066` / #2; ZIP SHA-256 `73c4278ff5da3b3dc27b697deed84da83cba676c3639ccb3431f5c996ea11535`) remains **SUPERSEDED / NON-AUTHORITATIVE / DO NOT PUBLISH / DO NOT IMPORT / DO NOT ARM**. The transport explicitly checked the checkpoint's authoritative numeric ID and excluded the superseded artifact. No recency, name-prefix or later-run selection was used.

## Exact archive/delta verification

The publication transport validated the exact reviewed archive against the canonical indexed S1.42AK-BMDSFIX1 parent snapshot:

- parent profile: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z`;
- parent SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- parent member count: **337**;
- publication member count: **338**;
- first 337 member paths remain in exact parent archive order;
- sole added member: `BepInEx/plugins/S142AKLFDiag1/S142AKLFDiag1.dll`;
- every parent member except `export.r2x` matches the indexed parent SHA-256 byte-for-byte;
- `export.r2x` differs only by the one exact raw identity replacement to `LC V1 S1.42AK-LFD1`;
- embedded LFDIAG1 DLL equals the separately frozen DLL byte-for-byte;
- removed members: **0**;
- package changes: **0**;
- config changes: **0**;
- inherited BMDSFIX1 DLL remains SHA-256 `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- accepted S1.42AB InteriorWeightNormalization remains SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- Gale projected maximum remains **217 / 255 PASS**.

## Readable publication snapshot

A deterministic readable snapshot was derived from the already-frozen profile bytes. This did not reconstruct or rewrite the profile.

`ProfileSources/S1.42AK-LFDIAG1/FILE_INDEX.json` contains:

- **338** archive rows in exact archive order;
- **331** readable text snapshots;
- final row index **337**: `BepInEx/plugins/S142AKLFDiag1/S142AKLFDiag1.dll`, size **18432**, SHA-256 `13fd01cba6d30a0c9044d43df813b17adf352139f723c9444f8db14403a0a474`.

No `ProfileSources/S1.42AK-LFDIAG1/PROFILE_INDEX_RESULT.json` exists at this gate. `Profiles/EXPECTED_HASHES.json` remains unchanged. Therefore this is publication evidence only, **not canonical profile indexing**.

## Independent post-materialization byte verification

After the transport and its removal, the assistant fetched the published repository profile as base64 from exact commit `129a5d5b2c303df068ea257265e353db0e862f72` and rehashed the decoded bytes. Profile SHA-256 and embedded LFDIAG1 DLL SHA-256 exactly matched the frozen authority; profile ZIP CRC passed. All 338 committed FILE_INDEX rows were independently compared against the actual published archive for order, path, size and SHA-256, with exactly 331 text-snapshot flags.

## Protected lifecycle/controller surfaces

Post-materialization branch verification confirms exact Git blob identity to current `main` for:

- `BuildSpecs/current.json`;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- `Current/AUTO_BUILD_RESULT.json`;
- `Current/AUTO_BUILD_RESULT.md`;
- `Profiles/EXPECTED_HASHES.json`.

Therefore S1.42AK remains accepted; S1.42AK-BMDSFIX1 remains active / **NOT ACCEPTED**; its selector-free Black Mesa x `DeepSewersFlow` gate remains passive, outstanding and unwaived; LFDIAG1 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**, not canonically indexed, not Gale-imported and not runtime-armed. Phase-C residual remains **28** and no gameplay run is authorized.

## Transport lifecycle

The temporary `.github/workflows/one-shot-lfdiag1-publication.yml` existed only to transport the exact frozen bytes and has already been removed from the publication branch at commit `129a5d5b2c303df068ea257265e353db0e862f72`. It must remain absent from the final integration head.

Final PR-head validation after the human-authored publication evidence/state commits remains required before merge.


## Publication integration blocker — source-stage lifecycle assertion

Exact evidence head `c9dbc906ef273276a46ceaec38c868f8b1402f60` passed Knowledge Architecture `37444638422` / #1197, frozen inactive-review guard `37444638393` / #8, DRDIAG1 source gate `37444638466` / #37 and AGDIAG1 source gate `37444638519` / #47. LFDIAG1 source gate `37444638509` / #11 failed only in `AnalysisTools/validate_s142ak_lfdiag1_source.py` at the historical assertion `liminal_facility_lfdiag1_built is False` (`RuntimeError: LFDIAG1 must remain unbuilt`), after pure selector tests and source compilation had passed.

The publication state correctly records the existing built/published artifact; reverting that fact would misstate lifecycle reality. The source-stage assertion is incompatible with the authorized later publication stage. No source validator or gameplay code was changed or bypassed in this publication checkpoint. Publication transport/hash/archive checks remain PASS, but this PR is **not integration-ready** until a separately bounded integration/reconciliation checkpoint resolves that stage-bound assertion against the frozen publication authority and obtains all required exact-final-head gates. Do not merge on Knowledge Architecture alone. Any later metadata-only head still requires its own exact-head CI; the run IDs above certify only the named evidence head.
