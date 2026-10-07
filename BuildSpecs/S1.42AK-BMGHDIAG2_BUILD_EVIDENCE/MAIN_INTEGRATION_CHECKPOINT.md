# S1.42AK-BMGHDIAG2 main-integration checkpoint

**Status:** PASS / EXACT REVIEWED BYTES ON MAIN / NOT RUNTIME ARMED / NOT ACCEPTED
**Date:** 2026-09-24
**Integration PR:** #144
**Exact PR head:** `984feb61d9a23296ec111f377639c090cf4f952b`
**Main merge commit:** `1dc18d5a37b5560d282174e11460672b508382ba`

## Exact-head CI

- Knowledge Architecture: run `35996531577` — PASS;
- BMGHDIAG2 source/pure-static gate: run `35996531589` — PASS;
- BMGHDIAG2 publication-aware archive gate: run `35996531593` — PASS.

The archive gate detected published-validation mode. It skipped both `profile_builder.py` and Actions artifact upload, then validated the already-published exact bytes and readable snapshot.

## Main-integrated identities

- profile SHA-256: `56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2`;
- diagnostic DLL SHA-256: `51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775`;
- archive/index members: 337;
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- package/config drift: zero.

## Lifecycle boundary

This checkpoint integrates publication only. S1.42AK remains the accepted/latest normal baseline. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`, `active_candidate` remains null and `runtime_test_outstanding` remains false. BMGHDIAG2 is not Gale-imported, not runtime-armed and not accepted.

The next permitted action is a separate atomic runtime-activation checkpoint for these exact main-integrated bytes.
