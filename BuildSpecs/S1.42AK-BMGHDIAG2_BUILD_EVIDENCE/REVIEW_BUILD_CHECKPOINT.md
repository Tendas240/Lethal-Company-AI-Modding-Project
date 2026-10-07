# S1.42AK-BMGHDIAG2 inactive review-build checkpoint

**Status:** PASS / REVIEW ARTIFACT ONLY / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  
**Date:** 2026-09-24  
**Review PR:** #142  
**Reviewed head:** `e45c695a5f75dd8e304f0434cd21bce3e0a30da3`  
**PR merge ref used by Actions:** `569cbbb184a4f81085999a802c9a695ba3a9f3f2`  
**Review workflow run:** `35990294162`  
**Actions artifact ID:** `10803912824`  
**Artifact name:** `S1.42AK-BMGHDIAG2-review-569cbbb184a4f81085999a802c9a695ba3a9f3f2`  
**Artifact ZIP SHA-256:** `265ebfae87ad3c48a6dbb57d0b3dce81a4c4d1c2e4872357f970354974da7a62`

## Exact reviewed bytes

- exact parent S1.42AK SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`;
- review profile SHA-256: `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2`;
- compiled/injected `S142AKBMGHDiag2.dll` SHA-256: `51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

The build compiled with zero warnings and zero errors. The injected diagnostic DLL was byte-identical to the compiled DLL.

## Exact archive delta

All 337 archive members were checked against the generated `FILE_INDEX.json`.

- added: `BepInEx/plugins/S142AKBMGHDiag2/S142AKBMGHDiag2.dll` only;
- changed existing: `export.r2x` only, and only permitted profile identity metadata differs after normalization;
- removed: none;
- package changes: 0;
- config changes: 0;
- accepted normalizer: byte-identical.

## Lifecycle boundary

This checkpoint records only an ephemeral Actions review artifact. No BMGHDIAG2 `.r2z` or `ProfileSources/S1.42AK-BMGHDIAG2/` has been published to `main`. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`, `active_candidate` remains null and `runtime_test_outstanding` remains false.

The next permitted bounded action is a separate publication checkpoint that materializes **these exact reviewed bytes** and revalidates their identity without arming runtime. Gale import/gameplay remains forbidden until a later explicit activation step.
