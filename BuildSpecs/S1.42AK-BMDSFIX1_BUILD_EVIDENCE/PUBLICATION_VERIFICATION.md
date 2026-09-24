# S1.42AK-BMDSFIX1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / STATIC PASS / NOT RUNTIME ARMED / NOT ACCEPTED
**Date:** 2026-09-24
**Review PR:** #149
**Reviewed head:** `79922a13b3543552dac67bff3d49384c129d4260`
**Review synthetic merge:** `7dbe71ba9ec504a387c5750f4f4c479dceffa95c`
**Review workflow run:** `36014932493`
**Actions artifact ID:** `10813908176`
**Artifact name:** `S1.42AK-BMDSFIX1-review-7dbe71ba9ec504a387c5750f4f4c479dceffa95c`
**Artifact ZIP SHA-256:** `b22e14b07455f722202cfaaf915ee362786c1a05c090aff0939f5a61b9de5db1`

## Published exact identities

- exact accepted S1.42AK parent SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`;
- published profile SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- published `S142AKBMDSFix1.dll` SHA-256: `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

## Exact archive and readable snapshot contract

The published `.r2z` is copied byte-for-byte from the reviewed Actions artifact; no profile or DLL rebuild occurs. All 337 archive members were rechecked against the already reviewed 337-row `FILE_INDEX.json`. The only added member is `BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll`; the only changed existing member is `export.r2x`, limited to profile identity metadata. There are zero package changes, zero config changes and no removed members.

`ProfileSources/S1.42AK-BMDSFIX1/` was reconstructed from the exact reviewed `.r2z` with `BuildSystem/profile_builder.py` snapshot semantics rather than copied from the incomplete Actions upload. The reconstructed `FILE_INDEX.json` is data-identical to the reviewed 337-row index. `BepInEx/config/.LCMaxSoundsFix.cfg` is present at index 1 with size 621 and SHA-256 `0093bae709cec57fd3f4f3bc5af22231b16944a666768e7ecf879430693f73a2`.

Fresh LLL provenance from the review artifact is persisted as `LLL_PROVENANCE.json` and confirms LethalLevelLoader 1.7.12 byte identity, exact accepted-parent binding, byte-identical parent export metadata and absence of an alternate LLL owner.

## Lifecycle boundary

`Current/AUTO_BUILD_RESULT.*`, `BuildSpecs/current.json`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` are intentionally unchanged by publication. S1.42AK remains accepted/latest, `active_candidate = null`, `runtime_test_outstanding = false`, and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.

This publication exists only on the dedicated working branch until later lifecycle/PR/CI/merge handling. It does not authorize Gale import, gameplay, runtime arming or acceptance. Runtime activation remains a separate atomic lifecycle step. Black Mesa x Greenhouse successor-diagnostic repair remains separate.
