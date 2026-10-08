# S1.42AK-SCDIAG1 exact original-byte publication verification

**Status:** REVIEWED ORIGINAL PROFILE BYTES MATERIALIZED ON DRAFT PUBLICATION PR #380 / MAIN INTEGRATION PENDING / NO CANONICAL INDEX / NO RUNTIME / DIAGNOSTIC ONLY — NEVER ACCEPT
**Date:** 2026-10-09
**Authorization:** `Current/348_S1.42AK_SCDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md` (integrated and permanent exact-main CI verified by `Current/349_S1.42AK_SCDIAG1_PUBLICATION_AUTHORIZATION_POST_MERGE_RECONCILIATION.md`)
**Frozen review:** `Current/346_S1.42AK_SCDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md`; `BuildSpecs/S1.42AK-SCDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`

## Exclusive original artifact and exact provenance

- Original Actions artifact ID: **11581745624**, not name/latest selected.
- Original producer head: `3e1680298b794d392a6938c9b734ecb649b2eea1`.
- Original dedicated review build: `37849046793/#2`.
- Artifact metadata at publication: `expired=false`, size **537332 bytes**, `expires_at=2027-01-06T21:46:01Z`; owner/run/head/name/digest pinned and checked by the transport.
- Original outer ZIP SHA-256: `9971c22f162ef61177b57f2e350bba5289f5fa09dd78cff65ccd82fcadb0d730`.
- Original nested `Profiles/LC V1 S1.42AK-SCD1.r2z` SHA-256: `6be6865a7fde205280439503680ac910401c20b997f757ffbedbddc963c704f4` (**576585 bytes**).
- Standalone and embedded `S142AKSCDiag1.dll` SHA-256: `2bd49852973c04c89dceea5b8dc9e75b051bc9a95c16850af08fb37dc3113131` (**18944 bytes**).

An independent assistant-side direct download of exactly artifact 11581745624 during this publication checkpoint rehashed the downloaded outer ZIP, nested profile, DLL and both ZIPs. Outer ZIP contains exactly four unique members; ZIP and profile CRC PASS; inner archive contains exactly **338 distinct** safe-path members. Embedded DLL is byte-identical to the standalone DLL. The `export.r2x` first line is exactly `profileName: LC V1 S1.42AK-SCD1`, without the forbidden LLL fork identity. Inherited BMDSFIX1 DLL = `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`; inherited InteriorWeightNormalization DLL = `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

## Exact-byte transport and strict full-parent comparison

Temporary fail-closed transport definition: `.github/workflows/one-shot-scdiag1-publication.yml` on branch `publish/s142ak-scdiag1-exact`; original definition commit `66bb2a5cc56ac322ccc33f489b2b66a989a151b3`. It was executed only by [Actions pull_request run 37855073698/#1](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/actions/runs/37855073698), job **113577179542**, `completed/success`. On checked-out publication branch the workflow:

1. Verified original artifact metadata against ID, producer head, producer run, non-expired status, ZIP digest and size; re-downloaded **only** exact ID 11581745624; SHA-256, unique archive members and CRC all PASS.
2. Independently SHA-256 checked the **actual checked-out** BMDSFIX1 parent profile bytes as `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`; parent ZIP CRC and exactly **337 unique members** PASS.
3. Compared each of all 337 parent members directly byte-for-byte to reviewed profile: same 337-member order, all inherited members identical except `export.r2x`; only new final member `BepInEx/plugins/S142AKSCDiag1/S142AKSCDiag1.dll`. Exact `export.r2x` replacement restricted to the one short profileName. Zero removals, no package/config drift. The parent full-member comparison is newly verified by this publication transport; the earlier assistant-side independent review download in record 346 **did not separately download the parent**. Do not conflate those evidence scopes.
4. Cross-checked canonical BMDSFIX1 `FILE_INDEX.json`, `PROFILE_INDEX_RESULT.json`, exact parent export bytes, inherited DLL SHA identities, plugin strings/marker/GUID/version, and the original frozen four-member manifest.
5. Ran the repository Windows/Gale profile-path guard against the immutable SCDIAG1 recipe: **215 and 217 /255** projected critical path lengths at the canonical reference root. This does not prove an unknown longer user-local Gale root will fit; that remains a later activation check.
6. Copied, **without reconstructing/repacking or rebuilding**, the existing frozen nested r2z bytes to `Profiles/LC V1 S1.42AK-SCD1.r2z` on the publication PR branch. Re-verified post-copy profile SHA-256. GitHub Actions bot exact-materialization commit: **`fad10ebec14c0ae4578776a75253c59fe6eb7d22`**.

The original producer's 8/8 negative validator cases remain frozen prior CI evidence, not newly repeated in the publication workflow. No replacement artifact was produced.

## Readable static snapshot, indexing boundary and controllers

The materialization generated `ProfileSources/S1.42AK-SCDIAG1/FILE_INDEX.json` with **338** unique in-order rows and **331** UTF-8-readable text snapshots, derived solely from the verified original profile bytes. Final row is the one added DLL with exact digest. No `ProfileSources/S1.42AK-SCDIAG1/PROFILE_INDEX_RESULT.json` has been generated and `Profiles/EXPECTED_HASHES.json` was not changed. This is **profile publication on an unmerged PR branch, not canonical profile indexing**.

The PR transport verified no modifications to `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Current/AUTO_BUILD_RESULT.json/.md` or `Profiles/EXPECTED_HASHES.json`. Gameplay accepted baseline remains **S1.42AK**, active **S1.42AK-BMDSFIX1 — NOT ACCEPTED**; its separate selector-free/passive Black Mesa × DeepSewersFlow proof remains outstanding/unwaived. SCDIAG1 is permanently **DIAGNOSTIC ONLY / NEVER ACCEPT**; Offense Storage Complex / `StorageComplex` generation, materialization and entrance-proof remain unproven. Phase C residual **23 = 11 viable/equal-100 + 12 owner-hard-block** unchanged. No Gale import, runtime activation/test, source/LLL/owner/normalizer/RNG change or gameplay acceptance.

## Exact-final-PR-head and integration boundary

**Before any main merge**, remove the *temporary* one-shot workflow; final PR #380 must contain only the exact frozen profile, readable snapshots and bounded publication documentation. Validate the final PR head with all required exact-head CI; bot-generated synchronize commits may be `action_required` rather than run jobs, so a later human-authored finalization commit is required for the genuine final-head tests. **Main integration, permanent exact-new-main-head Knowledge Architecture `push` CI, live-navigation reconciliation, later canonical EXPECTED_HASHES/index mapping, Gale import and runtime work are all separate gates.** Never merge or advance automatically.
