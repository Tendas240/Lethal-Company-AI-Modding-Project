# S1.42AK-BMAFR1I1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES MATERIALIZED ON PUBLICATION BRANCH / MAIN INTEGRATION PENDING / NOT INDEXED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Date:** 2026-10-03  
**Authorization:** `Current/234_S1.42AK_BMAFR1I1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`  
**Reviewed build head:** `6efb8fd3ff4e5b5a31b3b85bd600abe5ac5c5da9`  
**Review workflow run:** `37140903801` / #2  
**Frozen Actions artifact:** `11280870468`  
**Artifact name:** `S1.42AK-BMAFR1I1-review-6efb8fd3ff4e5b5a31b3b85bd600abe5ac5c5da9`  
**Artifact size:** `598993` bytes  
**Artifact ZIP SHA-256:** `c16938786c6ffa8e0dc43e71a3fad206457433397cb9fd34c8676da1d2d4b60c`  
**Published profile SHA-256:** `734dbe491b4f4fb77704472a303e386058e976325e0595dc4795af1940d1cb07`  
**Instrumentation DLL SHA-256:** `d9e09b20a889260d5cc8b4970d023a76d5b7af77ad677077b9718dfa8a150b6a`  
**Profile identity:** `LC V1 S1.42AK-BMAFR1I1`  
**Publication PR:** `#238`  
**Successful publication transport run:** `37156810501` / #1 — success  
**Transport-definition commit:** `5fabe076e33a2e20a467773b6e0719467d81c21c`  
**Exact materialization commit:** `9e7b2ac042a6b7ed38b4942f9481b5d89e9dd8b1`

The exact profile at `Profiles/LC V1 S1.42AK-BMAFR1I1.r2z` has been materialized on the dedicated publication branch from frozen Actions artifact `11280870468`. No profile or DLL was rebuilt, reconstructed, relinked, regenerated or substituted during publication.

The successful one-shot transport independently re-downloaded the frozen review artifact immediately before materialization and verified the exact artifact ZIP, profile and DLL SHA-256 values above. The assistant also downloaded the same frozen artifact through the repository connector into an independent workspace and rehashed it again: the 598993-byte ZIP, 600268-byte profile member and 52736-byte DLL matched the same three frozen SHA-256 values. ZIP contents were exactly the 14 files recorded by `REVIEW_BUILD_CHECKPOINT.json`.

## Exact archive/delta verification

The publication transport validated the exact reviewed archive contract against the canonical indexed BMAFR1 parent snapshot:

- direct parent: `Profiles/LC V1 S1.42AK-BMAFR1.r2z`;
- parent SHA-256: `8607a022e83304b473e7327ce5644141212a697fb8dffa210c58e02e5caafba5`;
- parent member count: `337`;
- publication member count: `338`;
- the first 337 member paths remain in the exact parent order;
- the sole added member is `BepInEx/plugins/S142AKBMAFR1I1/S142AKBMAFR1I1.dll`;
- every parent member except `export.r2x` matches the parent `FILE_INDEX.json` SHA-256 exactly;
- `export.r2x` differs only by the single byte-exact identity replacement `profileName: LC V1 S1.42AK-BMAFR1` -> `profileName: LC V1 S1.42AK-BMAFR1I1`;
- the DLL embedded in the profile equals the separately frozen DLL byte-for-byte;
- removed members: none;
- package changes: `0`;
- config changes: `0`;
- exact repaired nine-U+200B Foundry binding is inherited byte-for-byte;
- exact existing BMAF diagnostic DLL is inherited byte-for-byte;
- accepted S1.42AB InteriorWeightNormalization is inherited byte-for-byte;
- permanent Gale path guard passed at `219 / 221 <= 255`.

The publication transport first compared the protected controller/registry surfaces against `origin/main` and kept them unchanged: `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Current/AUTO_BUILD_RESULT.json/.md` and `Profiles/EXPECTED_HASHES.json`.

## Readable publication snapshot

A readable publication snapshot was derived deterministically from the already frozen profile bytes using the repository's established snapshot semantics. This operation did not write or reconstruct a profile.

`ProfileSources/S1.42AK-BMAFR1I1/FILE_INDEX.json` contains:

- `338` archive rows in exact archive order;
- `331` text snapshots;
- final row index `337`: `BepInEx/plugins/S142AKBMAFR1I1/S142AKBMAFR1I1.dll`, size `52736`, SHA-256 `d9e09b20a889260d5cc8b4970d023a76d5b7af77ad677077b9718dfa8a150b6a`.

No `ProfileSources/S1.42AK-BMAFR1I1/PROFILE_INDEX_RESULT.json` exists at this gate. `Profiles/EXPECTED_HASHES.json` remains unchanged. Therefore this is publication evidence only, not canonical profile indexing.

The normal `profile-index.yml` is intentionally not used as authority for this checkpoint. After later publication integration to `main`, its existing fail-closed behavior must reject the unmapped current profile until a separately authorized profile-index mapping/reconciliation gate supplies canonical build-ID/hash mapping.

## Lifecycle boundary

Publication leaves the gameplay and runtime lifecycle unchanged:

- S1.42AK remains the sole accepted gameplay baseline.
- S1.42AK-BMDSFIX1 remains active / **NOT ACCEPTED**.
- Its Black Mesa x DeepSewersFlow gate remains passive, outstanding and unwaived.
- BMAFR1 remains inactive / **DIAGNOSTIC ONLY / NEVER ACCEPT** with its bounded Black Mesa x Abandoned Foundry pair PASS preserved.
- BMAFDIAG1 and BMAFDIAG1PATH1 remain **DO NOT RERUN**.
- BMAFR1I1 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**, not indexed, not Gale-imported and not runtime-armed.
- Princess selection, live Janitor zero-blendshape state, exact array emitter, native Unity ownership and root cause remain unproven; SpringMan remains an equal-scope contemporaneous alternative.
- No gameplay run is authorized by publication.

The temporary one-shot publication transport is transport-only infrastructure and must be removed from PR #238 before repository integration.
