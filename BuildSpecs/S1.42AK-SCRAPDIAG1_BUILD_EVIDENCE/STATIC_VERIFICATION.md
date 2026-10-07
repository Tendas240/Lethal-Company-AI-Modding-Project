# S1.42AK-SCRAPDIAG1 Static Verification

**Status:** STATIC PASS / NOT ARMED  
**Validation run:** GitHub Actions `S1.42AK SCRAPDIAG1 build and static gate` run `35383680389`  
**Validated PR head:** `758816b6ce09a3406f256b1a9376ccb66d996afa`

## Exact parent

- Base profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`
- Base SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`

## Build result

- Output review artifact profile: `Profiles/LC V1 S1.42AK-SCRAPDIAG1 LC Office Scrap Placement Diagnostic.r2z`
- Output SHA-256: `233bcc058a3fa95d63e0577c4ff74b5a0dc137db49757b50376e447dd082d3b1`
- Existing archive members changed: **none**
- Existing archive members removed: **none**
- Added archive members: exactly:
  - `BepInEx/plugins/S142AJDiag1OfficeSelection/S142AJDiag1OfficeSelection.dll`
  - `BepInEx/plugins/S142AKDiagScrapPlacement/S142AKDiagScrapPlacement.dll`

## Diagnostic DLL hashes

- `S142AJDiag1OfficeSelection.dll`: `51d8927838f003f8ea00d69942d21dda3937d46c0cff5b220e99651c3a61a191`
- `S142AKDiagScrapPlacement.dll`: `f1c0b7450d60b8c0400c342779abcae8dfb11c34d9112d2e945a02349610df7b`

## Preserved accepted DLL hashes

- `S139CompatibilityFixes.dll`: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- `S142ABInteriorWeightNormalization.dll`: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

## Static gates

- Reviewed AJDIAG1 selector source unchanged in this PR: **PASS**
- AJDIAG1 selection-boundary tests: **PASS**
- AJDIAG1 selector compile: **PASS**
- Scrap placement logger compile: **PASS**
- Exact source/archive gate: **PASS**
- `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Current/CURRENT_STATE.json`, and `Current/AUTO_BUILD_RESULT.*` unchanged: **PASS**
- `Knowledge Architecture #523`: **PASS**

The first static-gate attempt exposed a logger string-escaping compile error before any profile build occurred. Commit `758816b6ce09a3406f256b1a9376ccb66d996afa` fixed only that syntax defect; the complete second gate passed.

## Review artifact

GitHub Actions artifact `S1.42AK-SCRAPDIAG1-review`, artifact ID `10563033130`, SHA-256 `08c676c2a0f9c7a3df3a0cd58854dbcc0b53ba21dd514a7c7d661cfcfe231bc3`.

## Qualification

This proves build/source/archive safety only. **Runtime is not armed.** Startup Harmony ordering, deterministic LC Office selection, stable two-snapshot collection, anchor/item markers and actual placement observations remain runtime-unproven.
