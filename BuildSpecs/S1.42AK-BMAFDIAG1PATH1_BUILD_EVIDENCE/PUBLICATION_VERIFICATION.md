# S1.42AK-BMAFDIAG1PATH1 exact reviewed-artifact publication verification

**Status:** EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / IDENTITY-ONLY STATIC PASS / NOT INDEXED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Date:** 2026-10-01  
**Reviewed source/build head:** `9191dcf3d71853ff4f8cb62d85b3b2c577680846`  
**Review workflow run:** `36898174164` (run `1`)  
**Frozen Actions artifact:** `11180586234`  
**Artifact ZIP SHA-256:** `98b9285a48cba4d78b48140289d7b8b4eaaad65778d9a59ee06826f5add88fae`  
**Published profile SHA-256:** `423e2e5185c85c1a3ce7a100583717d3503cf7308a12a182f5f7f65dc501ff91`  
**Short profile identity:** `LC V1 S1.42AK-BMAFD1P1`  
**Publication transport run:** `36899684349` (run `1`) — success  
**Exact publication commit:** `baf97cc8f4a17c35493b42b8a6326155c5e0a0c4`

The `.r2z` is copied byte-for-byte from frozen Actions artifact `11180586234`; no profile or DLL rebuild occurs during publication. Before materialization, the one-shot transport re-downloaded the artifact and revalidated the exact artifact ZIP digest, exact profile digest, exact protected BMAFDIAG1 DLL digest, exact frozen Foundry `LethalLevelLoader.cfg` digest, exact accepted S1.42AB normalizer digest, archive member count/uniqueness, snapshot index order and permanent Gale path budget.

Relative to exact published long-name BMAFDIAG1 SHA-256 `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2`:

- archive members remain exactly `337`;
- member ordering remains unchanged;
- added members: `0`;
- removed members: `0`;
- changed existing members: exactly `export.r2x`;
- semantic export delta: exactly the single `profileName` identity to `LC V1 S1.42AK-BMAFD1P1`;
- package changes: `0`;
- config changes: `0`;
- mod-state changes: `0`;
- local plugin builds: `0`;
- DLL rebuilds: `0`.

Protected identities remain byte-identical:

- `BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll` SHA-256 `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`;
- `BepInEx/config/LethalLevelLoader.cfg` SHA-256 `c9f03e7839c70ce21fae37ff597085175de35a9c176b97aed40798401ce66c0e`;
- `BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll` SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

The permanent Gale path guard still projects the two critical runtime paths at `219 / 221` characters under the project budget of `255`.

`ProfileSources/S1.42AK-BMAFDIAG1PATH1/` is materialized from the exact review artifact snapshot. Its `FILE_INDEX.json` has `337` rows in the same archive order and matched the review profile during publication validation. No `PROFILE_INDEX_RESULT.json` is created here; profile-index reconciliation is intentionally a later gate.

Publication intentionally leaves `BuildSpecs/current.json`, `Current/AUTO_BUILD_RESULT.*`, `Current/CURRENT_STATE.json` and `RuntimeInbox/ACTIVE_BUILD.txt` unchanged. S1.42AK remains accepted. S1.42AK-BMDSFIX1 remains the active gameplay candidate / not accepted with its regular Black Mesa x `DeepSewersFlow` qualification passive, outstanding and unwaived. The long-name BMAFDIAG1 remains preloader-blocked / **DO NOT RERUN**. BMAFDIAG1PATH1 is not indexed, not Gale-imported, not runtime-armed, not a gameplay/acceptance candidate, and remains **DIAGNOSTIC ONLY / NEVER ACCEPT**. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`; no gameplay run is authorized by this publication checkpoint.
