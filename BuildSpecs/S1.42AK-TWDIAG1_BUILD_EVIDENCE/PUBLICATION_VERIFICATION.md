# S1.42AK-TWDIAG1 Publication Verification

**Date:** 2026-10-07  
**Status:** PASS — EXACT FROZEN REVIEW BYTES MATERIALIZED / MAIN INTEGRATION PENDING  
**Classification:** DIAGNOSTIC ONLY / NEVER ACCEPT

Authority: `Current/306_S1.42AK_TWDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`.

## Exact byte authority

- Actions artifact ID: `11471277979`
- artifact ZIP SHA-256: `36e1466c1891f74d06a1195084a8c939b531dbd19b33a7abd29fd9463e568da0`
- profile SHA-256: `a5561b26ae5efe17b53239a0fc8a81020eec64ea59b5e3a7cca3481e6b3d7857`
- DLL SHA-256: `80c8f7615e6eeba59333160db5b7f3d40c6a97f2aafeaa01953cb4ce19e40499`
- parent S1.42AK-BMDSFIX1 SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`

Immediately before publication the assistant re-downloaded exact artifact `11471277979` through the authenticated GitHub connector. Artifact ZIP, profile and DLL hashes matched exactly; artifact and profile CRC checks passed. No rebuild or reconstruction occurred.

## Transport

Publication PR: **#325** on `publish/s142ak-twdiag1-exact`.

- initial transport definition: `5571f12b1faab1751ad20ec0b15075827b2cab08`;
- run `37618475651` / #1 — **failed closed before materialization** because a precedent-derived assertion referenced a field absent from the TWDIAG1 checkpoint; materialization/commit steps were skipped;
- corrected successful transport definition: `eec60ec8d17ad2e7ec2259e0882b68d95f953322`;
- exact-byte transport run: `37618575865` / #2 — **success**;
- byte-materialization commit: `1461cfdd93adfc28ac3aca6d8f0d7b74467adff9`;
- recursive bot-triggered runs on that commit were `action_required` and did not execute;
- explicit revalidation head: `dacb584703b61acdb14893375233551fe3a5db60`;
- revalidation run: `37618817992` / #4 — **success**;
- revalidation Knowledge Architecture: `37618817908` / #1299 — **success**;
- revalidation commit step: **Exact publication bytes already materialized; no commit required.**
- temporary workflow removal: `05f8c19540b67d45a2327b8da6bc7691aa93adb9`.

The temporary publication workflow is absent from the final publication diff.

## Materialized result

`Profiles/LC V1 S1.42AK-TWD1.r2z` is exactly **576351 bytes** with SHA-256 `a5561b26ae5efe17b53239a0fc8a81020eec64ea59b5e3a7cca3481e6b3d7857`.

The profile has exactly **338** unique members. Final member `BepInEx/plugins/S142AKTWDiag1/S142AKTWDiag1.dll` is **18432 bytes** with SHA-256 `80c8f7615e6eeba59333160db5b7f3d40c6a97f2aafeaa01953cb4ce19e40499`.

`ProfileSources/S1.42AK-TWDIAG1/FILE_INDEX.json` has **338** rows and **331** readable text snapshots. `PROFILE_INDEX_RESULT.json` is absent.

The transport verified exact indexed-parent member order, byte-identical protected parent members, exact `export.r2x` profile-name-only replacement, exact embedded/separate DLL equality, the four-file artifact member set, and the **217/255** Gale path budget.

## Boundary

Before lifecycle metadata writes PR #325 contained exactly one published profile plus **332** TWDIAG1 snapshot files: **333 changed files**.

Unchanged protected surfaces:

- `BuildSpecs/current.json`
- `RuntimeInbox/ACTIVE_BUILD.txt`
- `Current/AUTO_BUILD_RESULT.json`
- `Current/AUTO_BUILD_RESULT.md`
- `Profiles/EXPECTED_HASHES.json`

Canonical indexing, Gale import, runtime activation, gameplay and acceptance remain unauthorized.
