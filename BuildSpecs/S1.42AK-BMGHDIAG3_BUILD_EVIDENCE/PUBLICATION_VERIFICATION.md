# S1.42AK-BMGHDIAG3 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / NOT INDEXED / NOT RUNTIME ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT
**Date:** 2026-09-27
**Reviewed source/build head:** `4462ced77519b34f6d55181fc33692b298434833`
**Review workflow run:** `36311706288` (run `1`)
**Frozen Actions artifact:** `10929208327`
**Artifact ZIP SHA-256:** `20f616e85585e10631c31e09844a27bb6bb7649843a98655ed70e37b89152198`
**Published profile SHA-256:** `7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace`
**Diagnostic DLL SHA-256:** `d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352`
**Profile identity:** `LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic`

The `.r2z` is copied byte-for-byte from frozen Actions artifact `10929208327`; no profile or DLL rebuild occurs during publication. The artifact ZIP digest, exact profile digest and exact embedded `S142AKBMGHDiag3.dll` digest were revalidated before materialization.

Relative to exact accepted S1.42AK (`b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`), the published diagnostic profile has 337 members, adds only `BepInEx/plugins/S142AKBMGHDiag3/S142AKBMGHDiag3.dll`, removes none, and changes existing bytes only at `export.r2x` for profile identity after stable normalization. Package changes remain `0`, config changes remain `0`, accepted normalizer SHA-256 remains `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`, and reviewed LLL 1.7.12 provenance remains `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`.

`ProfileSources/S1.42AK-BMGHDIAG3/` is reconstructed from those exact reviewed profile bytes with repository snapshot semantics, and its `FILE_INDEX.json` is data-identical to the reviewed artifact index. No `PROFILE_INDEX_RESULT.json` exists yet; indexing is intentionally a later gate.

Publication intentionally leaves `BuildSpecs/current.json`, `Current/AUTO_BUILD_RESULT.*`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` unchanged. S1.42AK remains accepted. S1.42AK-BMDSFIX1 remains active gameplay candidate / not accepted with its regular Black Mesa x `DeepSewersFlow` qualification outstanding/passive. `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`. BMGHDIAG3 is not Gale-imported, not runtime-armed, not a gameplay/acceptance candidate, and remains **DIAGNOSTIC ONLY / NEVER ACCEPT**. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`; no gameplay run is authorized by this publication checkpoint.
