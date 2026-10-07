# S1.42AK-BMGHDIAG2 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / STATIC PASS / NOT RUNTIME ARMED / NOT ACCEPTED
**Date:** 2026-09-24
**Review PR:** #142
**Reviewed head:** `e45c695a5f75dd8e304f0434cd21bce3e0a30da3`
**Review synthetic merge:** `569cbbb184a4f81085999a802c9a695ba3a9f3f2`
**Review workflow run:** `35990294162`
**Actions artifact ID:** `10803912824`
**Artifact name:** `S1.42AK-BMGHDIAG2-review-569cbbb184a4f81085999a802c9a695ba3a9f3f2`
**Artifact ZIP SHA-256:** `265ebfae87ad3c48a6dbb57d0b3dce81a4c4d1c2e4872357f970354974da7a62`

## Published exact identities

- exact accepted S1.42AK parent SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`;
- published profile SHA-256: `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2`;
- published `S142AKBMGHDiag2.dll` SHA-256: `51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

## Exact archive and readable snapshot contract

The published `.r2z` is copied byte-for-byte from the reviewed Actions artifact; no profile or DLL rebuild occurs. All 337 archive members were rechecked against the already reviewed 337-row `FILE_INDEX.json`. The only added member is `BepInEx/plugins/S142AKBMGHDiag2/S142AKBMGHDiag2.dll`; the only changed existing member is `export.r2x`, limited to profile identity metadata. There are zero package changes, zero config changes and no removed members.

`ProfileSources/S1.42AK-BMGHDIAG2/` was reconstructed from the exact reviewed `.r2z` with `BuildSystem/profile_builder.py` snapshot semantics rather than copied from the incomplete Actions upload. The reconstructed `FILE_INDEX.json` is data-identical to the reviewed 337-row index. `BepInEx/config/.LCMaxSoundsFix.cfg` is present at index 1 with size 621 and SHA-256 `0093bae709cec57fd3f4f3bc5af22231b16944a666768e7ecf879430693f73a2`.

Fresh LLL provenance from the review artifact is persisted as `LLL_PROVENANCE.json` and confirms LethalLevelLoader 1.7.12 byte identity, exact accepted-parent binding, byte-identical parent export metadata and absence of an alternate LLL owner.

## Lifecycle boundary

`Current/AUTO_BUILD_RESULT.*`, `BuildSpecs/current.json`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` are intentionally unchanged by publication. S1.42AK remains accepted/latest, `active_candidate = null`, `runtime_test_outstanding = false`, and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.

This publication exists only on the dedicated working branch until later PR/CI/merge handling. It does not authorize Gale import, gameplay, runtime arming or acceptance. Runtime activation remains a separate atomic lifecycle step.
