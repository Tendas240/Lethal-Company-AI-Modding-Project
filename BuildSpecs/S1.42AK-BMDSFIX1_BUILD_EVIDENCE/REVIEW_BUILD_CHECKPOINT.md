# S1.42AK-BMDSFIX1 inactive review-build checkpoint

**Status:** PASS / REVIEW ARTIFACT ONLY / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  
**Date:** 2026-09-24  
**Review PR:** #149  
**Reviewed head:** `79922a13b3543552dac67bff3d49384c129d4260`  
**PR merge ref used by Actions:** `7dbe71ba9ec504a387c5750f4f4c479dceffa95c`  
**Review workflow run:** `36014932493`  
**Actions artifact ID:** `10813908176`  
**Artifact name:** `S1.42AK-BMDSFIX1-review-7dbe71ba9ec504a387c5750f4f4c479dceffa95c`  
**Artifact ZIP SHA-256:** `b22e14b07455f722202cfaaf915ee362786c1a05c090aff0939f5a61b9de5db1`

## Exact reviewed bytes

- exact parent S1.42AK SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`;
- review profile SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- compiled/injected `S142AKBMDSFix1.dll` SHA-256: `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

The build compiled with zero warnings and zero errors. The injected BMDSFIX1 DLL was byte-identical to the compiled DLL.

## Exact archive delta

All 337 archive members were checked against the generated `FILE_INDEX.json`.

- added: `BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll` only;
- changed existing: `export.r2x` only, and only permitted profile identity metadata differs after normalization;
- removed: none;
- package changes: 0;
- config changes: 0;
- accepted normalizer: byte-identical.

## Lifecycle boundary

This checkpoint records only an ephemeral Actions review artifact. No BMDSFIX1 `.r2z` or `ProfileSources/S1.42AK-BMDSFIX1/` has been published to `main`. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`, `active_candidate` remains null and `runtime_test_outstanding` remains false.

The next permitted bounded action is a separate exact-byte publication checkpoint that materializes **these exact reviewed bytes** and revalidates their identity without arming runtime. Gale import/gameplay remains forbidden until a later explicit activation step.
