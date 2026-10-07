# S1.42AK-BMDSFIX1 main-integration checkpoint

**Status:** PASS / EXACT REVIEWED BYTES ON MAIN / NOT RUNTIME ARMED / NOT ACCEPTED
**Date:** 2026-09-24
**Integration PR:** #150
**Exact PR head:** `24713dfc93a24f5e65ae5f223d3ea9c164da785e`
**Main merge commit:** `21138185f1ab377660b61120f1d07733d4180672`

## Exact-head and main CI

- PR Knowledge Architecture: run `36023454162` — PASS;
- BMDSFIX1 source/pure-static gate: run `36023454260` — PASS;
- BMDSFIX1 publication-aware archive gate: run `36023454215` — PASS;
- permanent main Knowledge Architecture push gate: run `36024694126` — PASS.

The archive gate detected published-validation mode. It skipped both `profile_builder.py` and Actions artifact upload, then validated the already-published exact bytes and readable snapshot.

## Main-integrated identities

- profile SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- BMDSFIX1 DLL SHA-256: `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`;
- archive/index members: 337;
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- package/config drift: zero.

## Lifecycle boundary

This checkpoint integrates publication only. S1.42AK remains the accepted/latest normal baseline. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`, `active_candidate` remains null and `runtime_test_outstanding` remains false. BMDSFIX1 is not Gale-imported, not runtime-armed and not accepted.

The next permitted action is a separate atomic runtime-activation checkpoint for these exact main-integrated bytes. Black Mesa x Greenhouse successor-diagnostic repair remains separate.
