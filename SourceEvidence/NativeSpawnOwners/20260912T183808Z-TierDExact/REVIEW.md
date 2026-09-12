# S1.42AI-DIAG1 Tier-D exact spawn-owner review

**Status:** EXACT REVIEW COMPLETE / PATCH SAFETY PARTIAL / NOT BUILD READY  
**Canonical base reviewed:** `ae1a4693d23e41fce6674380f6ff83631b0a1eb3`  
**Analysis branch:** `analysis/s142ai-tier-d-exact`  
**Exact-review head:** `68d8bcef1653cf5087a6826b7e68070bca13f1ed`  
**Actions run:** `34711742173` — SUCCESS  
**Artifact:** `10303775401` / `s142ai-tier-d-spawn-candidates-exact`  
**Artifact digest:** `sha256:e2255ba78b8605fdc96df4b480dbdae0a79bf015ccea1cfe52f9336a8c94134c`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope and selection

This is the next bounded escalation from the 25 discovery-positive packages remaining after Tier-C. The six packages selected here were the only remaining packages with two configured discovery signals; the other 19 remaining candidates had one signal each. The review therefore covers:

- `ButteryStancakes-ButteryFixes` 1.17.16;
- `Evaisa-LethalLib` 1.2.0;
- `TestAccount666-ShipWindows` 2.11.1;
- `WhiteSpike-Interactive_Terminal_API` 1.3.3;
- `Zehs-SellMyScrap` 1.15.3, including both discovery-positive DLLs;
- `mr_hat-MisideItems` 0.3.9.

The workflow re-downloaded the exact Thunderstore package versions, required the discovery ZIP/DLL/complete-source SHA values to match, decompiled complete C# and IL with pinned ILSpy, and retained those complete third-party decompiles only in the Actions artifact. `VERIFICATION.json` records the byte/hash provenance used by this review.

## Exact classifications

### ButteryStancakes-ButteryFixes 1.17.16

**Classification:** `DOWNSTREAM_ENEMY_ASSET_LIFECYCLE_FIX_AND_POOL_STATE_MUTATOR_NOT_DIRECT_CREATOR`

The exact assembly contains extensive enemy-facing Harmony fixes and references to `EnemyType` / `enemyPrefab`, but no `SpawnEnemyOnServer`, no `SpawnEnemyGameObject`, and no reviewed `Instantiate` site creates an enemy instance. Examples of required secondary behavior include:

- Butler radar registration receives an already-existing `ButlerEnemyAI`; its `Object.Instantiate` creates the radar icon, not the Butler.
- enemy prefab/type metadata are inspected or modified as part of compatibility/fix behavior;
- `RoundManager_Post_PredictAllOutsideEnemies` resets `numberSpawned` and `hasSpawnedAtLeastOne` on cached existing enemy types.

This package is therefore relevant to enemy lifecycle/state bookkeeping but is not a direct enemy creation owner in the exact reviewed DLL. Broad suppression of its enemy lifecycle hooks would discard unrelated fixes and state maintenance.

### Evaisa-LethalLib 1.2.0

**Classification:** `ENEMY_REGISTRY_AND_LEVEL_POOL_OWNER_NOT_DIRECT_INSTANCE_CREATOR`

`LethalLib.Modules.Enemies.RegisterEnemy` accepts `EnemyType` definitions and records registration metadata. `AddEnemyToLevel` materializes `SpawnableEnemyWithRarity` records into `SelectableLevel.Enemies`, `DaytimeEnemies`, or `OutsideEnemies` according to the registered spawn type and rarity. The exact DLL has no `SpawnEnemyOnServer` or `SpawnEnemyGameObject` call. Its four `Object.Instantiate` sites clone scan nodes, a generic prefab, or a ScriptableObject; none directly instantiate an enemy instance.

This is a real registry/pool owner, not a direct runtime enemy-instance creator. Removing or globally suppressing LethalLib registration is not an approved DIAG1 strategy because it would alter package registration responsibilities rather than intercept the smallest exact runtime creation surfaces.

### TestAccount666-ShipWindows 2.11.1

**Classification:** `DOWNSTREAM_ENEMY_VISUAL_COLLISION_PATCH_AND_SHIP_NETWORK_INFRASTRUCTURE_NOT_CREATOR`

The exact assembly patches `EnemyAI.Start` / `MaskedPlayerEnemy.Start` to restore enemy mesh visibility and patches enemy collision behavior. Its reviewed `Object.Instantiate` sites create ship/window/skybox objects and the ShipWindows network manager. `SpawnNetworkManager` is host-gated and network-spawns that manager, not an enemy. The assembly has zero `EnemyType`, zero `enemyPrefab`, zero `SpawnEnemyOnServer`, and zero `SpawnEnemyGameObject` occurrences.

This is additional concrete evidence that neither `EnemyAI.Start` nor shared `NetworkObject.Spawn` is a safe blanket diagnostic-denial surface.

### WhiteSpike-Interactive_Terminal_API 1.3.3

**Classification:** `GENERIC_EXPLICIT_ENEMY_SPAWN_API_NO_INTERNAL_CALLER_EXTERNAL_CONSUMER_GATE_OPEN`

The exact assembly contains one direct explicit enemy-spawn entry point:

`InteractiveTerminalAPI.Tools.SpawnMob(string mob, Vector3 position, int numToSpawn)`

The method searches `RoundManager.Instance.currentLevel.Enemies` by `enemyType.enemyName`; for each requested spawn it calls:

`RoundManager.Instance.SpawnEnemyOnServer(position, 0f, i)`

The complete exact DLL contains only this one `SpawnMob(` occurrence and one `SpawnEnemyOnServer` occurrence, so no internal caller exists in this assembly. That does **not** prove the public API is unused by the installed profile. Cross-assembly consumers must therefore be searched before DIAG1 implementation. Until that gate is closed, this API remains a possible installed-mod enemy creation path.

### Zehs-SellMyScrap 1.15.3

**Classification:** `NETWORKED_SCRAP_EATER_HANDLER_AND_DOWNSTREAM_ENEMY_HIT_INFRASTRUCTURE_NOT_CREATOR`

Both discovery-positive DLLs were exact-reviewed. Neither contains `EnemyType`, `enemyPrefab`, `SpawnEnemyOnServer`, or `SpawnEnemyGameObject`. Their network creation includes `StartScrapEaterOnServer`, which instantiates/network-spawns the configured Scrap Eater prefab, and `SpawnNetworkHandler`, which creates the mod's network handler. Other `Instantiate` sites create flashbang/explosion effects. Enemy references belong to downstream hit/explosion handling (`EnemyAIHelper`) against already-existing enemies.

The two exact DLL variants therefore provide networked scrap/mod infrastructure, not direct enemy-instance creation.

### mr_hat-MisideItems 0.3.9

**Classification:** `ITEM_FURNITURE_UI_INFRASTRUCTURE_WITH_DOWNSTREAM_ENEMY_HIT_LOGIC_NOT_CREATOR`

The exact assembly has no `EnemyType`, no `enemyPrefab`, no `SpawnEnemyOnServer`, and no `SpawnEnemyGameObject`. Its `Instantiate` sites create the FarmAndCook stove, monitor screens/buttons and HUD overlay. Enemy references are downstream collision/hit checks through `EnemyAICollisionDetect` / existing `EnemyAI` instances. Network object references and RPCs service item/furniture state rather than enemy creation.

## Patch-safety consequences

Tier-D confirms three distinct categories that must not be conflated:

1. **direct explicit creation API:** `InteractiveTerminalAPI.Tools.SpawnMob` reaches `RoundManager.SpawnEnemyOnServer`;
2. **registry/pool ownership:** LethalLib controls how registered EnemyTypes enter level pools but does not itself instantiate them in the exact assembly;
3. **downstream/non-enemy infrastructure:** ButteryFixes, ShipWindows, SellMyScrap and MisideItems use enemy lifecycle or shared networking surfaces for required non-creation responsibilities.

Therefore broad `EnemyAI.Start`, global `NetworkObject.Spawn`, wholesale LethalLib registration suppression, or blanket central spawn denial remains unsafe. The project-local patch policy still requires the smallest exact prevention-only surface while preserving native/mod bookkeeping, observer and cleanup contracts.

## Remaining gates

This tranche reduces the still-unreviewed discovery-positive inventory from 25 to **19**, but does not authorize DIAG1 implementation or build. Remaining work includes:

- exact-review/triage of the remaining 19 discovery-positive packages;
- trace SnowyLib cross-assembly spawn-API consumers;
- trace cross-assembly consumers of `InteractiveTerminalAPI.Tools.SpawnMob`;
- close the BCMER forced / forced-side / additional / runtime-custom execution gate;
- preserve/verify exact Shy Guy runtime identity and project source-to-DLL provenance;
- then select and statically validate the smallest host/client-safe interception points.

No profile, build controller, runtime controller, Gale state, candidate identity or acceptance state is changed by this evidence review. `S1.42AI-DIAG1` remains `PLANNED_NOT_BUILT` / `NOT_BUILD_READY`.
