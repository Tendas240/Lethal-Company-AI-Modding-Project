# S1.42AK-AGDIAG1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES MATERIALIZED ON PUBLICATION BRANCH / MAIN INTEGRATION PENDING / NOT CANONICALLY INDEXED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Date:** 2026-10-04  
**Authorization:** `Current/258_S1.42AK_AGDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`  
**Reviewed build head:** `46a5924ae142b0c00ff9fbbc6fecec5e2a4badae`  
**Review workflow run:** `37199874193` / #4  
**Frozen Actions artifact:** `11302468045`  
**Artifact name:** `S1.42AK-AGDIAG1-review-46a5924ae142b0c00ff9fbbc6fecec5e2a4badae`  
**Artifact size:** `536850` bytes  
**Artifact ZIP SHA-256:** `4602fa4d7567b10a497830a9b8213ad10f14fc7dee459e02e08fb1a7cdecfdbd`  
**Published profile SHA-256:** `e62e3c41f4f78105f1dc9ac789d71fd54e8d7f796aa7b46f5fd5615a68f91081`  
**AGDIAG1 DLL SHA-256:** `23a90b8b2bffd1f08a1391319b0e48215e3ef231b43a68ebdbf637128bfbb131`  
**Profile identity:** `LC V1 S1.42AK-AGD1`  
**Publication PR:** `#262`  
**Successful publication transport run:** `37201389603` / #1 — **success**  
**Transport-definition commit:** `0438cbd3047de5699a26e018c4e661774ed6d534`  
**Exact materialization commit:** `70325423a8431a8ba3ea07aa540152babd430c4a`

The exact profile at `Profiles/LC V1 S1.42AK-AGD1.r2z` has been materialized on the dedicated publication branch from frozen Actions artifact `11302468045`. No profile or DLL was rebuilt, reconstructed, recompiled, relinked, regenerated, repacked from source or substituted during publication.

## Immediate pre-materialization revalidation

The one-shot publication transport re-downloaded artifact `11302468045` by **exact numeric ID** immediately before repository materialization and verified:

- Actions ZIP SHA-256 `4602fa4d7567b10a497830a9b8213ad10f14fc7dee459e02e08fb1a7cdecfdbd`;
- exact profile SHA-256 `e62e3c41f4f78105f1dc9ac789d71fd54e8d7f796aa7b46f5fd5615a68f91081`;
- exact standalone `S142AKAGDiag1.dll` SHA-256 `23a90b8b2bffd1f08a1391319b0e48215e3ef231b43a68ebdbf637128bfbb131`;
- exact artifact file set and every member hash from `REVIEW_BUILD_CHECKPOINT.json`;
- profile ZIP CRC;
- permanent Gale path guard against `BuildSpecs/S1.42AK-AGDIAG1.json`.

The materialization step copied the already-reviewed profile member byte-for-byte and re-ran the profile SHA-256 check **after** the copy and before the commit.

Independently of the workflow, the assistant re-downloaded the same authoritative Actions artifact through the GitHub connector immediately before publication and rehashed its actual bytes in a separate workspace:

- ZIP: **536850 bytes**, SHA-256 `4602fa4d7567b10a497830a9b8213ad10f14fc7dee459e02e08fb1a7cdecfdbd`;
- profile member: **576357 bytes**, SHA-256 `e62e3c41f4f78105f1dc9ac789d71fd54e8d7f796aa7b46f5fd5615a68f91081`;
- DLL member: **18432 bytes**, SHA-256 `23a90b8b2bffd1f08a1391319b0e48215e3ef231b43a68ebdbf637128bfbb131`;
- artifact ZIP CRC: **PASS**;
- artifact contained exactly the four files preserved by the frozen review checkpoint.

Artifact `11302835640` was not used and remains **SUPERSEDED / NON-AUTHORITATIVE / DO NOT PUBLISH / DO NOT IMPORT / DO NOT ARM**.

## Exact archive/delta verification

The publication transport validated the exact reviewed archive against the canonical indexed S1.42AK-BMDSFIX1 parent snapshot:

- parent profile: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z`;
- parent SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- parent member count: **337**;
- publication member count: **338**;
- the first 337 member paths remain in exact parent archive order;
- sole added member: `BepInEx/plugins/S142AKAGDiag1/S142AKAGDiag1.dll`;
- every parent member except `export.r2x` matches the indexed parent SHA-256 byte-for-byte;
- `export.r2x` differs only by the one exact raw identity replacement from `LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix` to `LC V1 S1.42AK-AGD1`;
- embedded AGDIAG1 DLL equals the separately frozen DLL byte-for-byte;
- removed members: **0**;
- package changes: **0**;
- config changes: **0**;
- inherited BMDSFIX1 DLL remains SHA-256 `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- accepted S1.42AB InteriorWeightNormalization remains SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- Gale projected maximum remains **217 / 255 PASS**.

## Readable publication snapshot

A deterministic readable snapshot was derived from the already-frozen profile bytes. This process did not reconstruct or rewrite the profile.

`ProfileSources/S1.42AK-AGDIAG1/FILE_INDEX.json` contains:

- **338** archive rows in exact archive order;
- **331** readable text snapshots;
- final row index **337**: `BepInEx/plugins/S142AKAGDiag1/S142AKAGDiag1.dll`, size **18432**, SHA-256 `23a90b8b2bffd1f08a1391319b0e48215e3ef231b43a68ebdbf637128bfbb131`.

No `ProfileSources/S1.42AK-AGDIAG1/PROFILE_INDEX_RESULT.json` exists at this gate. `Profiles/EXPECTED_HASHES.json` remains unchanged. Therefore this is publication evidence only, **not canonical profile indexing**.

## Protected lifecycle/controller surfaces

The publication transport and post-materialization branch verification confirm byte-identical Git blob identity to current `main` for:

- `BuildSpecs/current.json`;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- `Current/AUTO_BUILD_RESULT.json`;
- `Current/AUTO_BUILD_RESULT.md`;
- `Profiles/EXPECTED_HASHES.json`.

Therefore:

- S1.42AK remains the accepted gameplay baseline;
- S1.42AK-BMDSFIX1 remains active / **NOT ACCEPTED**;
- its regular Black Mesa x `DeepSewersFlow` gate remains passive, outstanding and unwaived;
- AGDIAG1 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**;
- AGDIAG1 remains not canonically indexed, not Gale-imported and not runtime-armed;
- no gameplay run is authorized.

## Automation note

The exact byte-materialization commit was created by `github-actions[bot]` using the publication workflow's `GITHUB_TOKEN`. Subsequent PR workflow records at that bot-generated synchronize head may appear as `action_required` without executing jobs; they are not publication-byte validation authority. Final PR-head validation must be obtained again after human-authored evidence/finalization commits and removal of the temporary one-shot workflow.

The temporary `.github/workflows/one-shot-agdiag1-publication.yml` is transport-only infrastructure and must be absent from the final integration head.
