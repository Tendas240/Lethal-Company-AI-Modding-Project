# S1.42AK Static Verification

**Build:** S1.42AK — LC Office Camera Enemy Balance  
**Parent:** S1.42AJ — `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
**Parent SHA-256:** `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`  
**Output:** `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
**Output SHA-256:** `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
**Successful build workflow run:** `35366580975`  
**Automated build commit:** `395f8298230d343b523eeda3afbfc9253a281931`  
**Status:** STATIC VERIFIED / NOT ACCEPTED / NOT YET RUNTIME-ACTIVE

## Exact authorized delta

- `export.r2x`: profile name changed to S1.42AK and exact package `YaBoiDucki-men_stalker 3.1.2` changed from enabled to disabled.
- `BepInEx/config/me.biodiversity.aloe.cfg`: only `[SpawnSettings] PowerLevel` changed from `1` to `0`.
- `BepInEx/config/Piggy.LCOffice.cfg`: added with `[General] Camera Frame Speed = 0`.
- No LC Office scrap tuning was added.
- `BepInEx/config/wexop.random_enemies_size.cfg` is byte-identical to S1.42AJ.

## Archive verification

Parent snapshot entries: **335**.  
S1.42AK snapshot entries: **336**.

Changed existing members, exactly:
- `BepInEx/config/me.biodiversity.aloe.cfg`
- `export.r2x`

Added members, exactly:
- `BepInEx/config/Piggy.LCOffice.cfg`

Removed members: **none**.

The RandomEnemiesSize config has identical archive SHA-256 in parent and output:
`166158f2544f15daa7e06770db829046d611a056d5c4cb3fdd98adff96c8726f`.

The readable snapshot content was checked so the new export equals the parent export with only the profile-name and Men-stalker enabled-state edits, and the new Aloe config equals the parent Aloe config with only `PowerLevel = 1` -> `PowerLevel = 0`.

## Build-run provenance

The first trigger run `35366478552` failed before profile publication because its `export.r2x` text assertion was too strict about CRLF line endings. No S1.42AK profile commit was produced by that failed run. The assertion was corrected without changing the requested profile delta. Run `35366580975` then completed build, verification, repository commit and artifact upload successfully.

## Lifecycle boundary

This record proves static/build correctness only. S1.42AK is **not accepted** and is **not yet the active runtime candidate**. Runtime activation and the corresponding user test instructions belong to the next bounded lifecycle segment.
