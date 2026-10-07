# S1.42AK-BMDSFIX1-DIAG1 inactive review-build checkpoint

**Status:** PASS / REVIEW ARTIFACT ONLY / NOT PUBLISHED / NOT ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Date:** 2026-09-24  
**Review PR:** #154  
**Reviewed head:** `87154ea28b0167a6d4e435f04620978926565e85`  
**PR merge ref used by Actions:** `476e69887030005d455b50a7c85ea8a6f11d5da6`  
**Review workflow:** `S1.42AK BMDSFIX1-DIAG1 inactive review build gate`  
**Review workflow run:** `36051334448`  
**Run number:** `3`  
**Actions artifact ID:** `10830821692`  
**Artifact name:** `S1.42AK-BMDSFIX1-DIAG1-review-476e69887030005d455b50a7c85ea8a6f11d5da6`  
**Artifact ZIP SHA-256:** `53787c9e943a297996f5cb0f81d6a9e783ad23abc4a7d642ab45b449ed6419d7`

## Exact reviewed bytes

- exact parent `S1.42AK-BMDSFIX1` profile SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- review profile SHA-256: `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`;
- compiled/injected `S142AKBMDSFix1Diag1.dll` SHA-256: `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`;
- inherited `S142AKBMDSFix1.dll` SHA-256: `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

The downloaded Actions artifact ZIP independently hashed to the same SHA-256 recorded by GitHub Actions. The review profile and DIAG1 DLL hashes were independently recomputed from that artifact after the workflow completed.

## Exact archive delta

All `338` review-profile archive members were checked against the generated `FILE_INDEX.json`.

- added: `BepInEx/plugins/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.dll` only;
- changed existing: `export.r2x` only, limited to permitted profile identity metadata after normalization;
- removed: none;
- package changes: `0`;
- config changes: `0`;
- inherited BMDSFIX1 DLL: byte-identical;
- accepted S1.42AB normalizer: byte-identical.

## Validation gates on the reviewed head

- inactive review-build gate: run `36051334448`, run #3, `success`;
- source/pure-static gate: run `36051334458`, run #4, `success`;
- Knowledge Architecture: run `36051334438`, run #725, `success`.

A prior preliminary review artifact from run `36050896488` is **superseded and must not be published** because later plan/validator-only commits changed the Git source revision embedded by the .NET build. The exact reviewed bytes for any later publication are exclusively the run `36051334448` artifact identified above.

## Lifecycle boundary

This checkpoint records only an ephemeral GitHub Actions review artifact. The DIAG1 `.r2z` and `ProfileSources/S1.42AK-BMDSFIX1-DIAG1/` are not repository-published by this stage.

The live/build controllers remain on the unchanged BMDSFIX1 gameplay candidate:

- `BuildSpecs/current.json` remains disabled and pinned to the exact BMDSFIX1 parent profile;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`;
- S1.42AK remains the sole accepted baseline;
- S1.42AK-BMDSFIX1 remains active / not accepted;
- `runtime_test_outstanding=true` remains the regular BMDSFIX1 target gate;
- DIAG1 is not runtime-armed and is never an acceptance candidate.

## Next permitted bounded action

A separate exact-byte publication checkpoint may materialize **only the reviewed profile/DLL bytes from review run `36051334448`** and then revalidate their identity. No rebuild may be substituted for those reviewed bytes. Publication still does not itself authorize Gale activation or runtime execution; those remain later explicit lifecycle steps.
