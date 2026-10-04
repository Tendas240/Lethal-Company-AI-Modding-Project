# S1.42AK-DRDIAG1 Source / Pure-Static Findings

**Date:** 2026-10-04  
**Status:** SOURCE / PURE-STATIC STAGED / PR VALIDATION PENDING / DIAGNOSTIC ONLY / NOT BUILT / NOT ARMED / NEVER ACCEPT  
**Authority:** `Current/266_S1.42AK_PHASE_C_DRAINS_DRDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`  
**Implementation base:** `77e9696931f412879886fb2396a84be73fb49d26`

## Implemented source contract

The isolated source root is `Patches/S142AKDRDiag1/`.

The implementation reuses the validated AGDIAG1 selector-only architecture with the separately frozen DRDIAG1 identity:

- build: `S1.42AK-DRDIAG1`;
- assembly/project: `S142AKDRDiag1`;
- GUID: `tendas.lethalcompany.s142akdrdiag1`;
- version: `1.0.0`;
- marker: `[DRDIAG1]`;
- classification: `DIAGNOSTIC ONLY / NEVER ACCEPT`.

Exactly one intended Harmony patch call exists. It targets LLL `DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` as a postfix, ordered after the accepted S1.42AB normalizer at `Priority.Last`.

On the validated real Offense selection path the selector may retain only one already-returned viable `Drains` wrapper whose exact asset is `DrainsFlow` and whose final normalized rarity is `100`. The same existing wrapper is retained; the policy never constructs a replacement and never creates eligibility.

## Fail-closed pure policy coverage

The pure test program covers:

- positive exact Offense Drains / DrainsFlow / rarity-100 index selection;
- retained-wrapper object identity;
- `debugResults=false` inert behavior;
- non-Offense inert behavior;
- terminal-simulation exclusion;
- unknown selection caller refusal;
- null/empty pool refusal;
- missing accessor refusal for each accessor;
- null wrapper refusal;
- missing Drains refusal;
- duplicate Drains refusal;
- asset mismatch refusal;
- rarity 65/0 refusal;
- repeated independent pools without mutation.

Refusal tests snapshot the pool and prove count plus wrapper identity/order remain unchanged.

## Static safety surface

`Patches/S142AKDRDiag1/PATCH_SAFETY_REVIEW.md` records the mandatory project-local Patch Safety Review.

The intended sole mutation remains the fresh already-viable/normalized return list after every guard passes. No availability, registration, global rarity, RNG, RPC, generation, entrance, NavMesh, PathfindingLib, enemy/scrap, BCMER, BMDSFIX1 or accepted-normalizer mutation is part of DRDIAG1.

The deterministic repository validator is `AnalysisTools/validate_s142ak_drdiag1_source.py`; the dedicated exact-PR-head workflow is `.github/workflows/s142ak-drdiag1-source-static.yml`.

## Controller and lifecycle preservation

This source/static checkpoint constructs no profile and arms no runtime:

- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- parent remains exact S1.42AK-BMDSFIX1 profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`;
- S1.42AK remains accepted;
- S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED;
- its regular selector-free Black Mesa x DeepSewersFlow gate remains outstanding and unwaived;
- Phase-C residual remains 29 pending actual Drains runtime evidence.

The semantic router remains `interiors_and_lll`; no router-map mutation is required.

## Validation status

PR validation pending. No source/static PASS is claimed until both the dedicated DRDIAG1 gate and Knowledge Architecture succeed on the exact same PR head.

No review profile, publication, Gale import, activation or runtime is authorized by this source checkpoint.
