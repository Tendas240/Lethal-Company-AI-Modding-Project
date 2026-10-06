# S1.42AK-SHDIAG1 Publication Verification

**Date:** 2026-10-06  
**Status:** PASS — EXACT FROZEN REVIEW BYTES MATERIALIZED / MAIN INTEGRATION PENDING  
**Classification:** DIAGNOSTIC ONLY / NEVER ACCEPT

Authority: `Current/294_S1.42AK_SHDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`.

## Exact byte authority

- Actions artifact ID: `11416035651`
- artifact ZIP SHA-256: `e97eb01168ca0679f514d63ff8559cf06215949c644b64bc16c513384c552b44`
- profile SHA-256: `787a7baf441ec0ccc2af1295ccc3e94b70ca3bff17e026fb90985733efcb957e`
- DLL SHA-256: `e78e0eb6483d332e3b2a05be772173036c90e9fccd2c1fc9d52980a5d516d062`
- parent S1.42AK-BMDSFIX1 SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`

The exact artifact was independently re-downloaded immediately before publication. ZIP/profile/DLL hashes matched the frozen authority and ZIP CRC validation passed. No reconstruction or rebuild occurred.

## Transport

Publication PR: **#309** on `publish/s142ak-shdiag1-exact`.

- transport-definition commit: `61bd6342624f9a4b23669f6b5e51ee48a4cd3a74`
- publication transport run: `37479350216` / #1 — **success**
- materialization commit: `5f3fe6379bb05735b37c22b6243d156ce8f53c9f`
- cleanup/revalidation run: `37480229257` / #3 — **success**
- temporary transport removal commit: `ba3abb28fe1dbe204f004222ee719c3ff3efab6f`

The temporary publication workflow is absent from the final PR diff.

## Materialized result

`Profiles/LC V1 S1.42AK-SHD1.r2z` is exactly **576359 bytes** with SHA-256 `787a7baf441ec0ccc2af1295ccc3e94b70ca3bff17e026fb90985733efcb957e`.

The profile has exactly **338** members. The added final member is `BepInEx/plugins/S142AKSHDiag1/S142AKSHDiag1.dll`, **18432 bytes**, SHA-256 `e78e0eb6483d332e3b2a05be772173036c90e9fccd2c1fc9d52980a5d516d062`.

`ProfileSources/S1.42AK-SHDIAG1/FILE_INDEX.json` contains exactly **338** rows and the snapshot contains **331** readable text files. `PROFILE_INDEX_RESULT.json` is absent.

## Boundary

Before lifecycle metadata writes, PR #309 contained exactly the published profile plus 332 SHDIAG1 snapshot files. These protected surfaces were unchanged:

- `BuildSpecs/current.json`
- `RuntimeInbox/ACTIVE_BUILD.txt`
- `Current/AUTO_BUILD_RESULT.json`
- `Current/AUTO_BUILD_RESULT.md`
- `Profiles/EXPECTED_HASHES.json`

This is publication evidence only. Canonical indexing, Gale import, runtime activation, gameplay and acceptance remain unauthorized.
