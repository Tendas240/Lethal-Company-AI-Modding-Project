# S1.42AK-BMAFDIAG1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / NOT INDEXED / NOT RUNTIME ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT
**Date:** 2026-09-30
**Reviewed source/build head:** `47f2beca815c4d726fec8b85f4e9aac129519486`
**Review workflow run:** `36735131025` (run `2`)
**Frozen Actions artifact:** `11106178288`
**Artifact ZIP SHA-256:** `e96b8de8084f051d74fcb06b05aa06ed3355419602c813b6021acb8a5b9f78b0`
**Published profile SHA-256:** `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2`
**Diagnostic DLL SHA-256:** `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`
**Profile identity:** `LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic`

The `.r2z` is copied byte-for-byte from frozen Actions artifact `11106178288`; no profile or DLL rebuild occurs during publication. The artifact ZIP digest, exact profile digest, exact embedded `S142AKBMAFDiag1.dll` digest, archive delta, owner-default Foundry configuration delta and controller boundary were revalidated before materialization.

Relative to exact accepted S1.42AK (`b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`), the published diagnostic profile has 337 members, adds only `BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll`, removes none, and changes existing bytes only at `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`. Package changes remain `0`, config changes remain `1`, accepted normalizer SHA-256 remains `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`, and reviewed LLL 1.7.12 provenance remains `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`.

The LLL delta materializes exactly one owner-default `Abandoned Foundry` section at file tail, changes only `Enable Content Configuration` from owner-default `false` to `true`, appends exactly `Black Mesa:100` once to the preserved owner Manual Level Names mapping, preserves all other owner values, and adds no `External:100`, foreign pairing or size-rule change.

`ProfileSources/S1.42AK-BMAFDIAG1/` is reconstructed from those exact reviewed profile bytes with repository snapshot semantics, and its `FILE_INDEX.json` is data-identical to the reviewed artifact index. No `PROFILE_INDEX_RESULT.json` exists yet; indexing is intentionally a later gate.

Publication intentionally leaves `BuildSpecs/current.json`, `Current/AUTO_BUILD_RESULT.*`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` unchanged. S1.42AK remains accepted. S1.42AK-BMDSFIX1 remains active gameplay candidate / not accepted with its regular Black Mesa x `DeepSewersFlow` qualification outstanding/passive. `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`. BMAFDIAG1 is not Gale-imported, not runtime-armed, not a gameplay/acceptance candidate, and remains **DIAGNOSTIC ONLY / NEVER ACCEPT**. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`; no gameplay run is authorized by this publication checkpoint.
