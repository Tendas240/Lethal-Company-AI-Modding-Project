# S1.42AK-FXDIAG1 — Frozen exact-byte publication verification

**Status:** FROZEN REVIEWED BYTES MATERIALIZED ON PR #362 BRANCH; MAIN INTEGRATION PENDING; NOT CANONICALLY INDEXED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED; DIAGNOSTIC ONLY / NEVER ACCEPT
**Date:** 2026-10-08
**Authority:** `Current/333_S1.42AK_FXDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md`, `Current/334_S1.42AK_FXDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_POST_MERGE_RECONCILIATION.md`
**Original review run:** `37801213085/#1`; build head `1c2e9d100f6f34a2946489a555d07da39a841c83`
**Exclusive original Actions artifact ID:** `11561251337`
**Artifact ZIP (537017 bytes) SHA-256:** `2805967a866ad8d88c4d80221c5bbd354a1a59adeaf1d7decfaa634d725c4b89`
**Published exact reviewed profile:** `Profiles/LC V1 S1.42AK-FXD1.r2z` (576445 bytes); SHA-256 `b2491e10811310661de76b71e7bf42cf259065e4b363e36d18abfa8457a14435`
**Embedded/frozen FXDIAG1 DLL (18944 bytes) SHA-256:** `322774f531f87dc9b253e712e63d69ed39fb998017af75b6545cdc904d0b7705`
**Immutable parent BMDSFIX1 SHA-256:** `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`
**Publication PR:** [#362](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/pull/362)
**Publication transport run:** [37821754670/#2](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/actions/runs/37821754670) — `completed/success`.
**Transport definition:** `7942a502dc1a41602e6293f3ff4ccdd5bbe52a84`; exact materialization commit `766391cb3224a5e22dbb12ee18c146ed947e5e79`; temporary workflow removal `74a54a7ba47a4838da148bf87177b1439106f350`.

## Independently retrieved original frozen bytes

The assistant used the connected GitHub artifact download operation with **numeric ID 11561251337**. Independently recomputed SHA-256 values matched the frozen ZIP, profile and DLL; four unique outer ZIP members and **338 unique profile ZIP members** passed their respective CRC tests. Original `DLL/S142AKFXDiag1.dll` bytes matched the embedded `BepInEx/plugins/S142AKFXDiag1/S142AKFXDiag1.dll`. The nested `export.r2x` had exactly one `profileName: LC V1 S1.42AK-FXD1`.

The published profile was copied unchanged by the one-shot transport following a **second GitHub API download by the exact numeric artifact ID** and successful `sha256sum --check --strict` for ZIP, profile and DLL. No compilation/reconstruction or profile/ZIP re-packaging ran. The first transport attempt `37821606794/#1` failed before any materialization due solely to an incorrect DRDIAG1 DLL filename in the temporary workflow. Its path-only correction `cce484a36cce1a99af508a72647f36dc1dbee6e5` allowed successful transport. No replacement build or new source bytes were produced.

## Parent-delta and materialization guard

The successful transport validated the exact 337-member indexed BMDSFIX1 parent state versus 338 reviewed FXDIAG1 members. The first 337 member paths were identical and in exact parent order; each inherited member except `export.r2x` rehashed byte-identically to the indexed parent. The only added member was `BepInEx/plugins/S142AKFXDiag1/S142AKFXDiag1.dll`. The only changed existing member was `export.r2x`, exactly the single short-profile identity replacement. **Zero** removed, package or config changes. The profile DLL matched the separately frozen DLL.

- Inherited BMDSFIX1 DLL: `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92` — PASS.
- Inherited S1.42AB normalizer DLL: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06` — PASS.
- Permanent Gale path-length guard: **217/255 PASS**.
- Full parent-to-profile comparison was originally proven by the pinned review-build CI; during publication the independent transport compared archived contents to pinned indexed parent-member hashes and the original exact export snapshot, rather than a separately downloaded full parent. Do not conflate these two proof methods.

## Deterministic readable snapshot

`ProfileSources/S1.42AK-FXDIAG1/FILE_INDEX.json` lists all **338** nested archive members, their sizes and SHA-256 digests in archive order; **331** UTF-8-readable text/config/metadata members are snapshotted in the same directory. Final member is the 18944-byte FXDIAG1 DLL with exact frozen hash. Readable snapshots are **not** replacement profile bytes.

`ProfileSources/S1.42AK-FXDIAG1/PROFILE_INDEX_RESULT.json` is absent and `Profiles/EXPECTED_HASHES.json` has **not** been altered. Canonical profile indexing is a separate future decision/step, not part of this transport.

## Preserved main and controller boundary

The one-shot transport checked that `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, `Current/AUTO_BUILD_RESULT.json`, `Current/AUTO_BUILD_RESULT.md`, and `Profiles/EXPECTED_HASHES.json` were identical to current main. `S1.42AK` is accepted; `S1.42AK-BMDSFIX1` remains active **NOT ACCEPTED**, with the passive selector-free Black Mesa x DeepSewersFlow gate unwaived. Phase-C residual **24** stays unchanged. `FXDIAG1` remains **DIAGNOSTIC ONLY / NEVER ACCEPT**, with no actual Fractured Complex materialization proof, Gale import, activation or runtime authorization.

**Next strictly separate gate:** final exact-PR-head CI verification and main integration/reconciliation of publication PR **#362** after removal of its temporary one-shot workflow. The publication segment itself must not merge the PR.
