# S1.42AK-TSDIAG1 exact frozen original-byte publication verification

**Status:** MATERIALIZED ON OPEN DRAFT PR #399 ONLY / FINAL EXACT-HEAD CI PENDING / MAIN MERGE SEPARATE / DIAGNOSTIC ONLY — NEVER ACCEPT  
**Date:** 2026-10-09  
**Authorizations:** `Current/365_S1.42AK_TSDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`, main-integrated and effective under `Current/366_S1.42AK_TSDIAG1_PUBLICATION_AUTHORIZATION_POST_MERGE_RECONCILIATION.md`.  
**Frozen source:** `Current/363_S1.42AK_TSDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md` and immutable `BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`.  
**Publication checkpoint:** `Current/367_S1.42AK_TSDIAG1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md`.

## Original review artifact, independently acquired by exact numeric ID

- Sole Actions original **artifact ID 11615262607**, original producing run **37929246619/#2**, exact producer head `24105017a0d98ccc05b878c809f84f93f4e87e37`, artifact size **537308**, `expired=false`, expiry `2027-01-07T12:19:15Z`. No latest/by-name/failed-run substitution.
- Newly re-downloaded outer ZIP SHA-256 **`010b84c1ffaea1d5cda2e14cdb9580c049da2cd1790e929491e44d13e2c4f39f`**, **4 unique outer members** with CRC PASS.
- Exact original profile `Profiles/LC V1 S1.42AK-TS1.r2z` SHA-256 **`d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e`**, size **576574**, **338 distinct nested members** with CRC PASS, name `LC V1 S1.42AK-TS1`.
- Standalone `DLL/S142AKTSDiag1.dll` and nested `BepInEx/plugins/S142AKTSDiag1/S142AKTSDiag1.dll` identical, size **18944**, SHA-256 **`fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201`**.
- Original independently computed profile Git blob SHA-1 `ba6c086f74187e10f31d57ac429512424572cf45` exactly matches `Profiles/LC V1 S1.42AK-TS1.r2z` Git tree entry on PR materialization commit `27b23c71da7415b921e9ab4daa75bfac372c2c98`. Hence byte equality is checked independently of the transport job's post-copy hash.

## Separate successful exact-original-byte transport

- Branch `publish/s142ak-tsdiag1-exact-20261009`, open [draft PR #399](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/pull/399).
- Temporary one-shot definition commit `1777941124b06391f8168b98f643762ef5f9f6dd`; [transport Actions run 37942238752/#1](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/actions/runs/37942238752), `pull_request`, `completed/success`; exact materialization commit `27b23c71da7415b921e9ab4daa75bfac372c2c98`.
- Transport independently downloaded the sole artifact by ID and checked GitHub original artifact metadata, run/head, digest and size. It checked full ZIP/DLL/profile hashes, CRC, uniqueness, DLL/GUID/version/marker and dependency signatures.
- **Actual checked-out immutable BMDSFIX1 parent** SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`; 337 unique CRC-clean parent members; all parent members tested byte-for-byte against new profile. Exactly one DLL appended, only `export.r2x` changed by one exact profileName replacement, zero inherited drift, removals, package/config change. Parent `ProfileSources/S1.42AK-BMDSFIX1/FILE_INDEX.json`, parent profile index and parent export snapshot independently cross-checked.
- Inherited BMDSFIX1 DLL `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`, inherited normalizer `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`. No LLL fork injected.
- Permanent Windows/Gale path guard against unchanged spec passed with maximal projected **216/255** at reference root. Future user-local profile root remains a separate activation-specific check.
- Exact reviewed nested original copied directly without rebuilding or repacking; post-copy SHA-256 success. Deterministic `ProfileSources/S1.42AK-TSDIAG1/FILE_INDEX.json`: **338 entries**, **331 readable UTF-8 snapshots**.
- Final PR must **delete** temporary `.github/workflows/one-shot-tsdiag1-publication.yml` before exact-PR-head CI. Frozen source/review workflow and validator are unchanged. No second build/re-upload/transport authorized.

## Prohibited scopes and next independent gate

No `Profiles/EXPECTED_HASHES.json` edit, no canonical `PROFILE_INDEX_RESULT.json`, no canonical hash-map/profile index, Gale import, controller mutation, runtime arm/test, gameplay qualification or acceptance. Live accepted S1.42AK, active BMDSFIX1 NOT ACCEPTED with its separate unwaived selector-free Black Mesa x DeepSewersFlow obligation, residual 22 (10 viable / 12 owner-hard-block), Toy Store still without trusted real generation/materialization/entrance/traversal proof.

**Current:** Original-byte materialization on unmerged PR #399 only. **Next:** final exact PR-head applicable CI, then **another user-gated segment** for pinned-head PR integration and exact-main-head permanent Knowledge Architecture `push`. Do not merge here.
