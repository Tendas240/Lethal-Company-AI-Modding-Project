# S1.42AK-BMDSFIX1-DIAG1PATH1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / IDENTITY-ONLY STATIC PASS / NOT INDEXED / NOT RUNTIME ARMED / DIAGNOSTIC SUPPORT ONLY / NEVER ACCEPT
**Date:** 2026-09-25
**Reviewed source/build head:** `8c6b5b60994985d15c087a72d52f8c178c15d697`
**Review workflow run:** `36063701766` (run `2`)
**Frozen Actions artifact:** `10835876163`
**Artifact ZIP SHA-256:** `b38036a3ae1e7d49c9890a8d9343252d8d0e19cfcde854b2410a91519968b90d`
**Published profile SHA-256:** `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`
**Short profile identity:** `LC V1 S1.42AK-D1P1`

The `.r2z` is copied byte-for-byte from frozen artifact `10835876163`. Relative to exact published DIAG1 (`31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`), the 338 archive members and their order are unchanged. Only `export.r2x` changes, exclusively by the single `profileName` identity after normalization. No package, config, mod-state or DLL bytes change and no DLL/profile rebuild occurs.

Protected DLL identities remain `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1` (DIAG1 selector), `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92` (BMDSFIX1) and `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06` (accepted normalizer). The readable `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/` snapshot is reconstructed from those exact bytes and its 338-row `FILE_INDEX.json` is data-identical to the reviewed index.

Publication intentionally leaves `BuildSpecs/current.json`, `Current/AUTO_BUILD_RESULT.*`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` unchanged. S1.42AK remains accepted; BMDSFIX1 remains the active gameplay candidate / not accepted with Black Mesa x `DeepSewersFlow` outstanding and unwaived. DIAG1 remains the preloader-blocked runtime/evidence pointer and must not be rerun. DIAG1PATH1 is not indexed, not armed, not a gameplay/acceptance candidate, and remains **DIAGNOSTIC SUPPORT ONLY / NEVER ACCEPT**. No Gale import or runtime execution is authorized. Greenhouse/BMGHDIAG remains out of scope.
