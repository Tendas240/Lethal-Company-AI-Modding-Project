# S1.42AK-CFDIAG1 Publication Verification

**Date:** 2026-10-07  
**Status:** PASS — EXACT FROZEN REVIEW BYTES MATERIALIZED / MAIN INTEGRATION PENDING  
**Classification:** DIAGNOSTIC ONLY / NEVER ACCEPT

Authority: `Current/319_S1.42AK_CFDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`.

## Exact byte authority

- Actions artifact ID: `11499680067`
- artifact name: `S1.42AK-CFDIAG1-review-61d71173b353c6aaea10ca9e983d944880fc05be`
- artifact ZIP size: **536888 bytes**
- artifact ZIP SHA-256: `287dc7aacb481b63d9381ce0f7b4be56134c5330c21eb8a506b71a21db879371`
- profile size: **576383 bytes**
- profile SHA-256: `a4ebbed30e530153e3f3dc92b97b676729eada94e602ccf29a4ca63a64f3ce4c`
- DLL size: **18432 bytes**
- DLL SHA-256: `00ea72dff35512779b5c24d64bb481db21be7f6d9365d1ec947245e5505c6776`
- parent S1.42AK-BMDSFIX1 SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`

Immediately before repository materialization, exact artifact `11499680067` was re-downloaded by numeric ID. The assistant-side independent download rehashed to the exact frozen ZIP digest above, outer ZIP CRC passed, and all four artifact members matched `REVIEW_BUILD_CHECKPOINT.json`. The publication workflow independently repeated the exact numeric-ID download, ZIP SHA-256 check and outer ZIP CRC check before any repository write.

No rebuild, reconstruction, recompilation, relinking, profile regeneration, source repack or byte substitution occurred.

## Transport

Publication PR: **#340** on `publish/s142ak-cfdiag1-exact`.

- transport-definition head: `dbb4e99847f60f6c023e8489b3643abc2554311b`
- exact-byte transport run: `37681154509` / #1 — **success**
- exact byte-materialization commit: `04b368c91de37cc024951e0cb0aab920403adb6c`
- recursive bot-triggered one-shot/Knowledge runs on the bot commit were `action_required` and did not execute
- explicit revalidation head: `70aef7d2158b7a0abca753431793798921d23d27`
- revalidation transport run: `37681283868` / #3 — **success**
- revalidation Knowledge Architecture: `37681283860` / #1346 — **success**
- revalidation produced no replacement byte commit; the branch head remained the explicit revalidation commit
- temporary workflow removal: `c25a0c36067ae890d7bd85b7165668a2c8f53df7`

The transport ran `RepositoryTools/gale_profile_path_length_guard.py --spec BuildSpecs/S1.42AK-CFDIAG1.json` before materialization and retained the reviewed **217/255 PASS** path budget.

## Materialized result

`Profiles/LC V1 S1.42AK-CFD1.r2z` is exactly **576383 bytes** with SHA-256 `a4ebbed30e530153e3f3dc92b97b676729eada94e602ccf29a4ca63a64f3ce4c`.

The profile has exactly **338** unique members. Final member `BepInEx/plugins/S142AKCFDiag1/S142AKCFDiag1.dll` is **18432 bytes** with SHA-256 `00ea72dff35512779b5c24d64bb481db21be7f6d9365d1ec947245e5505c6776`.

`ProfileSources/S1.42AK-CFDIAG1/FILE_INDEX.json` has **338** rows and **331** readable text snapshots. `PROFILE_INDEX_RESULT.json` is absent.

The transport verified the exact indexed-parent member order, byte-identical protected parent members, exact `export.r2x` profile-name-only replacement, exact embedded/separate DLL equality, exact four-file artifact member set, ZIP CRCs and Gale path budget.

## Boundary

After temporary workflow removal and before lifecycle metadata writes, PR #340 contained exactly one published profile plus **332** CFDIAG1 snapshot files: **333 changed files**.

Unchanged protected surfaces:

- `BuildSpecs/current.json`
- `RuntimeInbox/ACTIVE_BUILD.txt`
- `Current/AUTO_BUILD_RESULT.json`
- `Current/AUTO_BUILD_RESULT.md`
- `Profiles/EXPECTED_HASHES.json`

Canonical profile indexing, Gale import, runtime activation, gameplay and acceptance remain unauthorized.
