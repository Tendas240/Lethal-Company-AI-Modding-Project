# S1.42AK-BMDSFIX1-DIAG1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / STATIC PASS / NOT RUNTIME ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT
**Date:** 2026-09-24
**Review PR:** #154
**Reviewed source/build head:** `87154ea28b0167a6d4e435f04620978926565e85`
**Review synthetic merge:** `476e69887030005d455b50a7c85ea8a6f11d5da6`
**Review workflow run:** `36051334448`
**Review run number:** `3`
**Actions artifact ID:** `10830821692`
**Artifact ZIP SHA-256:** `53787c9e943a297996f5cb0f81d6a9e783ad23abc4a7d642ab45b449ed6419d7`

## Published exact identities

- exact BMDSFIX1 parent profile SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- published DIAG1 profile SHA-256: `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`;
- published `S142AKBMDSFix1Diag1.dll` SHA-256: `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`;
- inherited `S142AKBMDSFix1.dll` SHA-256: `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

## Exact archive and readable snapshot contract

The published `.r2z` is copied byte-for-byte from the final reviewed Actions artifact; no profile or DLL rebuild occurs. All 338 archive members are rechecked against the reviewed 338-row `FILE_INDEX.json`. Relative to the exact BMDSFIX1 parent, the only added member is `BepInEx/plugins/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.dll`; the only changed existing member is `export.r2x`, limited to profile identity metadata. There are zero package changes, zero config changes and no removed members.

`ProfileSources/S1.42AK-BMDSFIX1-DIAG1/` is reconstructed from the exact reviewed `.r2z` with `BuildSystem/profile_builder.py` snapshot semantics rather than copied blindly from the Actions upload. The reconstructed `FILE_INDEX.json` is data-identical to the reviewed 338-row index, including hidden-file metadata.

The preliminary artifact from workflow run `36050896488` is superseded and is not used by this publication. The sole byte source is artifact `10830821692` from final successful review run `36051334448`.

## Lifecycle boundary

`Current/AUTO_BUILD_RESULT.*`, `BuildSpecs/current.json`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` are intentionally unchanged by publication. S1.42AK remains the accepted baseline. S1.42AK-BMDSFIX1 remains the active gameplay candidate / not accepted with its exact original profile bytes and `runtime_test_outstanding=true`.

DIAG1 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**. This publication exists only on the dedicated working branch until later lifecycle/PR/CI integration. It does not authorize Gale import, gameplay, runtime arming, BMDSFIX1 acceptance, or any reinterpretation of DIAG1 evidence as regular exact-byte BMDSFIX1 qualification.
