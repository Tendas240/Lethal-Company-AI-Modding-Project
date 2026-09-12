# S1.42AI-DIAG1 remaining enabled-package spawn-owner discovery

**Status:** DISCOVERY_COMPLETE / DIRECT_CANDIDATE_TRANCHE_EXACT_REVIEWED / PATCH_SAFETY_PARTIAL / NOT_BUILD_READY  
**Canonical main reviewed:** `a9e508aabb2111f511ddf2790c0a4929092bdb15`  
**Discovery run:** `34705334804`, head `45d22c3fa1abb3bbd95dd137cd3903eb053f87c7`, SUCCESS  
**Discovery aggregate artifact:** `10301363891`, `s142ai-remaining-spawn-owner-discovery`, artifact ZIP digest `sha256:de218a23690b4d1b1453f7428e8245d84b347cdf1181fe235c63964a4d9eea96`  
**Aggregate payload SHA-256:** `2c96e4a1e05599f90249270b402eed638a4d9bcab6160d238c46f4b1b131728f`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope and evidence contract

The guarded S1.42AI export contains 183 enabled packages. Seven packages already covered by the earlier native-owner batch and two packages routed to separate exact authorities were excluded from repeat screening, leaving exactly 174 enabled packages for this second pass. These exclusions are evidence routing only; they are not declarations that the excluded packages are safe.

The read-only workflow re-downloaded the exact enabled Thunderstore package versions, hashed package ZIPs and every DLL member, detected managed PE assemblies from CLI metadata rather than package/file-name guesses, and screened managed IL for EnemyAI/EnemyType/prefab, `RoundManager.SpawnEnemyGameObject`, enemy-context `Instantiate` / `NetworkObject.Spawn`, enemy/nest/vent/batch surfaces and Harmony/MonoMod detour indicators. Only positive DLLs were decompiled to bounded source excerpts. The aggregate job failed closed unless every one of the 174 remaining packages was covered exactly once.

The first run stopped correctly when one managed assembly exceeded the original 128 MiB DLL bound. The only repair raised that bounded analysis allowance to 512 MiB for the scan; no package was skipped and no negative result was converted into an approval. Run `34705334804` then completed with all twelve shards plus the aggregate job successful.

## Aggregate result

- enabled S1.42AI packages: **183**;
- routed exclusions: **9** (`7` prior-batch + `2` separate-authority);
- remaining exact packages scanned: **174**;
- managed DLLs inspected: **206**;
- positive candidate packages: **53**;
- positive candidate DLLs: **55**;
- registration-only packages: **3**;
- packages with no configured positive signature: **118**.

A registration-only or no-positive-signature result is **not** a patch-safety approval. It means only that this exact-byte static signature pass did not identify a direct owner candidate under the configured discovery rules. The scanner is source-location discovery, not a complete call graph or proof that every possible dynamic/reflection/runtime spawn path is absent.

The three registration-only packages are `TestAccount666-TestAccountCore 1.18.0`, `Fneaky-ImmortalSnailFork 0.1.1`, and `YaBoiDucki-men_stalker 3.1.2`.

## Direct SpawnEnemyGameObject escalation

Ten of the 53 positive packages contained a direct `RoundManager.SpawnEnemyGameObject` signature and were escalated first into exact full-source/IL review:

- `Kittenji-Herobrine 1.3.9`;
- `Kittenji-Football 1.1.14`;
- `pacoito-itolib 0.9.3`;
- `lethal_coder-31Arcadia_UPDATED 1.0.2`;
- `notnotnotswipez-MoreCompany 1.14.0`;
- `Zigzag-PremiumScraps 2.5.0`;
- `rectorado-KenjiLib 0.7.0`;
- `JacobG5-JLL 1.10.1`;
- `Zigzag-ChillaxScraps 1.6.6`;
- `super_fucking_cool_and_badass_team-Biodiversity 0.2.9`.

Their exact review is canonicalized alongside this discovery at `SourceEvidence/NativeSpawnOwners/20260912T163927Z-DirectSpawnCandidatesExact/REVIEW.md` and `VERIFICATION.json`. All ten are real source-level call paths. PremiumScraps and ChillaxScraps additionally contain direct enemy-prefab `Instantiate` + `NetworkObject.Spawn(true)` paths that bypass `SpawnEnemyGameObject`; MoreCompany's direct route is an internally dormant host debug command unless another actor enables its public static flag. The remaining stateful owners further confirm that a blanket central `SpawnEnemyGameObject` denial is unsafe because owner state, power/apparatus state, nests or post-spawn synchronization may already be committed around the shared call.

## Remaining patch-safety scope

This second-pass discovery closes the previous unknown inventory size, but it does **not** close patch safety. After the ten direct candidates, **43 positive packages remain** for bounded triage and exact escalation according to signature strength and relevance. The separate exact BCMER forced/forced-side/additional/runtime-custom execution gate and the Shy Guy runtime identity / project source-to-DLL provenance gate also remain open before final interception design.

`S1.42AI-DIAG1` remains **PLANNED_NOT_BUILT / NOT_BUILD_READY**. This evidence does not authorize a build, controller transition, Gale import, gameplay test, global `NetworkObject.Spawn` suppression, blanket `SpawnEnemyGameObject` denial, broad EnemyAI lifecycle suppression, post-spawn cleanup, or removal of unexpected exterior Shy Guys.
