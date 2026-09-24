# S1.42AK-BMGHDIAG2 exact-byte publication preparation

**Status:** PREPARATION PASS / EXACT REVIEW ARTIFACT REVERIFIED / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  
**Date:** 2026-09-24  
**Parent main:** `223cc097edd10f4eedba1efa23a2d78e7bc1a95a`  
**Lifecycle authority:** `Current/CURRENT_STATE.json`

## Purpose

Persist the completed pre-publication inspection for the already reviewed `S1.42AK-BMGHDIAG2` Actions artifact so a later publication checkpoint does not repeat discovery work or accidentally rebuild the diagnostic.

This record does not publish a profile and does not change any live build/runtime controller.

## Exact review artifact re-verification

The exact review artifact from the accepted inactive review-build checkpoint was re-queried and downloaded again from GitHub Actions:

- review workflow run: `35990294162`;
- reviewed branch head: `e45c695a5f75dd8e304f0434cd21bce3e0a30da3`;
- artifact ID: `10803912824`;
- artifact name: `S1.42AK-BMGHDIAG2-review-569cbbb184a4f81085999a802c9a695ba3a9f3f2`;
- artifact state: not expired at this checkpoint;
- artifact ZIP size: `1085339` bytes;
- artifact ZIP SHA-256: `265ebfae87ad3c48a6dbb57d0b3dce81a4c4d1c2e4872357f970354974da7a62`.

Independent inspection of the downloaded ZIP reconfirmed:

- reviewed profile SHA-256: `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2`;
- injected `BepInEx/plugins/S142AKBMGHDiag2/S142AKBMGHDiag2.dll` SHA-256: `51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775`;
- the reviewed `.r2z` contains exactly `337` archive members;
- the uploaded `ProfileSources/S1.42AK-BMGHDIAG2/FILE_INDEX.json` contains exactly `337` rows;
- every FILE_INDEX row matches the reviewed `.r2z` member at the same index by path, size and SHA-256.

These values agree with `REVIEW_BUILD_CHECKPOINT.md`. Publication must therefore materialize these exact reviewed bytes and must not substitute a later rebuild.

## Hidden ProfileSources omission found

The Actions review artifact contains `336` outer ZIP entries. Its uploaded readable `ProfileSources` subtree omits exactly the hidden text snapshot:

`BepInEx/config/.LCMaxSoundsFix.cfg`

This is an artifact-upload snapshot omission, not a reviewed-profile omission. The exact reviewed `.r2z` contains the file, and the already reviewed 337-row `FILE_INDEX.json` contains the corresponding row:

- index: `1`;
- path: `BepInEx/config/.LCMaxSoundsFix.cfg`;
- size: `621` bytes;
- SHA-256: `0093bae709cec57fd3f4f3bc5af22231b16944a666768e7ecf879430693f73a2`;
- `text_snapshot: true`.

The omission is consistent with the review workflow artifact upload using the default hidden-file exclusion. It does not alter the `.r2z`, its 337-member archive contract, or any gameplay/config bytes.

## Required publication materialization contract

The next publication checkpoint must remain exact-byte and fail closed:

1. download artifact `10803912824` from review run `35990294162`;
2. verify the artifact ZIP SHA-256, reviewed profile SHA-256 and diagnostic DLL SHA-256 above before writing repository output;
3. revalidate the exact 337-member archive delta and all 337 FILE_INDEX rows against the reviewed `.r2z`;
4. publish the reviewed `.r2z` byte-for-byte without rebuilding `S142AKBMGHDiag2.dll` or regenerating the profile;
5. reconstruct the readable `ProfileSources/S1.42AK-BMGHDIAG2/` snapshot from the exact reviewed `.r2z` using the repository snapshot semantics, rather than blindly copying the incomplete uploaded ProfileSources subtree;
6. require the reconstructed `FILE_INDEX.json` to agree exactly with the already reviewed 337-row index and require `.LCMaxSoundsFix.cfg` to be present with the exact size/hash above;
7. persist publication verification proving the exact profile/DLL/dependency/normalizer identities and zero package/config drift;
8. keep `BuildSpecs/current.json` disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, `active_candidate = null` and `runtime_test_outstanding = false` throughout publication.

Publication success still does **not** authorize Gale import or gameplay/runtime. Runtime activation remains a later separate atomic lifecycle step.

## Preserved boundaries

- S1.42AK remains the accepted/latest normal gameplay baseline.
- Accepted S1.42AB InteriorWeightNormalization remains unchanged.
- Black Mesa remains Dawn/native-owned; do not duplicate-register it through LLL.
- Greenhouse availability and the fixed B3 30×53 matrix remain unchanged.
- Black Mesa x Greenhouse remains `NOT_YET_PROVEN` until later runtime evidence.
- No Shatteredrooms Experimentation/Embrion scope expansion is authorized.
- Black Mesa/Pikmin routing remains a separate scope.
