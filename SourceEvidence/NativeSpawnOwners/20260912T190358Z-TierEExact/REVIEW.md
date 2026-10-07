# S1.42AI-DIAG1 Tier-E exact spawn-owner review

**Status:** EXACT REVIEW COMPLETE / PATCH SAFETY PARTIAL / NOT BUILD READY  
**Scope:** next six prioritized discovery-positive packages after canonical Tier-D  
**Canonical main used for review:** `fce6d19de0a8810fe457b0436a44f948c51701cf`  
**Discovery authority:** `SourceEvidence/NativeSpawnOwners/20260912T163027Z-RemainingEnabledDiscovery/VERIFICATION.json`  
**Exact-review run:** `34713018420`  
**Exact-review head:** `c80173f8718869117f3ab4309347bb14f69cd055`  
**Artifact:** `10304290416` / `s142ai-tier-e-spawn-candidates-exact`  
**Artifact digest:** `sha256:a4c61ef958aba55a2573c296f0ab16904693d1f4e96b156ba6d48802fae0348a`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Purpose and selection

After Tier-D, 19 discovery-positive packages remained. The next bounded tranche was selected by signature strength and actual enemy context without re-reviewing Direct/Tier-A/Tier-B/Tier-C/Tier-D packages.

The three strongest remaining signature classes were:

- `DiFFoZ-LethalPerformance` — `enemy_spawn_lifecycle_patch_or_detour`;
- `Scoops-LethalSponge` — `enemy_spawn_lifecycle_patch_or_detour`;
- `ButteryStancakes-BarberFixes` — `enemy_context_spawn_named_surface`.

The additional three candidates were the most enemy-relevant remaining `enemy_context_instantiate` hits:

- `Wexop-RandomEnemiesSize`;
- `TheFluff-FairAI`;
- `ButteryStancakes-MaskFixes`.

For `LethalPerformance`, all three managed DLLs in the exact package were reviewed, including the preloader/patcher and Unity support assembly, so its lifecycle patch behavior is not classified from the plugin DLL alone.

## Provenance and method

The repository-native workflow re-downloaded the exact Thunderstore package versions, required the exact package ZIP and DLL SHA-256 values from discovery, reproduced the discovery IL SHA-256 with pinned ILSpy, then preserved complete C# and IL for all eight reviewed assemblies.

The review inspected complete creation sites and the relevant enemy lifecycle / pool / bookkeeping contexts. In all eight reviewed assemblies:

- `SpawnEnemyOnServer` occurrences: **0**;
- `SpawnEnemyGameObject` occurrences: **0**;
- direct `enemyPrefab` occurrences: **0**.

No reviewed Tier-E assembly contains a direct enemy-instance creation primitive.

## Package findings

### DiFFoZ-LethalPerformance 1.2.6

Reviewed assemblies:

- `BepInEx/patchers/LethalPerformance/LethalPerformance.Patcher.dll`
- `BepInEx/plugins/LethalPerformance/LethalPerformance.dll`
- `BepInEx/plugins/LethalPerformance/LethalPerformance.Unity.dll`

Classification:

`PERFORMANCE_CACHING_AND_SHARED_LIFECYCLE_TRANSPILER_INFRASTRUCTURE_NOT_CREATOR`

The patcher and Unity support assemblies do not create enemies. The main plugin performs broad object/reference caching and transpiler work. Its target inventory includes `EnemyVent.Start`, and its caching layer rewrites object-find behavior for networked gameplay types. It also contains an EnemyAI lookup optimization that replaces a `FindObjectsOfType<EnemyAI>` access with `RoundManager.Instance.SpawnedEnemies`-backed access.

Patch-safety implication: `EnemyVent.Start`, object-lookup helpers and `RoundManager.SpawnedEnemies` are shared lifecycle/bookkeeping surfaces with active performance consumers. They are not valid blanket DIAG1 suppression points.

### Scoops-LethalSponge 1.4.3

Reviewed assembly:

- `LethalSponge/LethalSponge.dll`

Classification:

`PERFORMANCE_CLEANUP_AND_AUDIO_DEDUP_INFRASTRUCTURE_NOT_CREATOR`

The exact assembly iterates existing `EnemyVent` and `EnemyType` assets as part of global audio deduplication/cleanup. The apparent `Instantiate` substring from the static occurrence scan is not an enemy creation call; it is contained in a configuration/property-name string (`GetInstantiatedLightProbesForScene`). No direct enemy creation path exists.

Patch-safety implication: discovery hits around EnemyVent/EnemyType here are downstream asset/performance infrastructure, not spawn ownership.

### ButteryStancakes-BarberFixes 1.3.1

Reviewed assembly:

- `BarberFixes.dll`

Classification:

`CONDITIONAL_SERVER_SIDE_CLAYSURGEON_SPAWN_PARAMETER_MUTATOR_NOT_INSTANCE_CREATOR`

`PreAdvanceHourAndSpawnNewBatchOfEnemies` is a Harmony prefix on `RoundManager.AdvanceHourAndSpawnNewBatchOfEnemies`. It runs only on the server and only when `configApplySpawningSettings` is enabled. The code-level configuration default is `false`. When active, it resolves the `ClaySurgeon` `EnemyType` from current level pools and mutates `spawnInGroupsOf` and `MaxCount`; the native RoundManager path subsequently owns instance creation.

BarberFixes also patches existing `ClaySurgeonAI` lifecycle behavior, but contains no direct enemy creation primitive.

Patch-safety implication: `AdvanceHourAndSpawnNewBatchOfEnemies` is a native spawn transaction with legitimate pre-spawn configuration consumers. A blanket denial there would suppress required native behavior and unrelated mods.

### Wexop-RandomEnemiesSize 1.1.20

Reviewed assembly:

- `RandomEnemiesSize.dll`

Classification:

`DOWNSTREAM_ENEMY_START_SCALE_AND_RPC_SYNC_NOT_CREATOR`

The package postfixes `EnemyAI.Start` and `MaskedPlayerEnemy.Start`. It operates on an already-created enemy, applies randomized scale and related gameplay adjustments, and synchronizes those values through RPC/network-object identity.

Its two real `Object.Instantiate<Item>` sites clone item metadata for Giant Kiwi egg and Red Locust Bee hive support. They do not instantiate enemy prefabs.

Patch-safety implication: `EnemyAI.Start` is again proven to carry legitimate downstream responsibilities and cannot be globally skipped.

### TheFluff-FairAI 1.6.1

Reviewed assembly:

- `FairAI.dll`

Classification:

`DOWNSTREAM_ENEMY_COMBAT_AND_HAZARD_COMPATIBILITY_NOT_CREATOR`

FairAI enumerates and patches existing enemy/hazard behavior so enemies can interact with turrets, landmines and other combat systems. Its sole `Object.Instantiate<GameObject>` site creates `StartOfRound.Instance.explosionPrefab` as an effect during downstream combat handling. It does not instantiate an EnemyAI or call a native direct spawn primitive.

Patch-safety implication: enemy hit/kill/hazard surfaces here are downstream compatibility logic, not spawn ownership.

### ButteryStancakes-MaskFixes 1.6.2

Reviewed assembly:

- `MaskFixes.dll`

Classification:

`DOWNSTREAM_MASKED_START_STATE_VISUAL_AND_SPAWNEDENEMIES_REPAIR_NOT_CREATOR`

Its `MaskedPlayerEnemy.Start` postfix operates on an already-existing masked enemy. If that instance is absent from `RoundManager.Instance.SpawnedEnemies`, the patch adds the same existing instance to the list, then repairs tags, scan-node/appearance state and other masked behavior.

The two `Object.Instantiate<GameObject>` sites create suit/costume visual objects (`headCostumeObject` / `lowerTorsoCostumeObject`), not enemy instances.

Patch-safety implication: `MaskedPlayerEnemy.Start` and `RoundManager.SpawnedEnemies` are active downstream state-repair surfaces and must not be mistaken for direct creation ownership.

## Tier-E patch-safety conclusion

This tranche contains no direct enemy-instance creator.

It nevertheless strengthens the negative safety evidence against broad interception:

- do not globally suppress `EnemyAI.Start`;
- do not globally suppress `MaskedPlayerEnemy.Start`;
- do not suppress `EnemyVent.Start`;
- do not clear or block `RoundManager.SpawnedEnemies`;
- do not blanket-deny `RoundManager.AdvanceHourAndSpawnNewBatchOfEnemies`;
- do not treat shared object/network lookup infrastructure as an enemy-only surface.

The smallest exact owner/interception rule from `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` remains mandatory.

## Remaining coverage

Canonicalizing this tranche reduces the still-unreviewed discovery-positive inventory from **19 to 13**.

Still open independently:

1. exact-review the remaining 13 discovery-positive packages;
2. trace SnowyLib cross-assembly consumers;
3. trace `InteractiveTerminalAPI.Tools.SpawnMob` cross-assembly consumers;
4. close BCMER forced / forced-side / additional / runtime-custom event execution coverage;
5. preserve/verify exact Shy Guy runtime identity and project source-to-DLL provenance;
6. select and statically validate the smallest host/client-safe interception points.

`S1.42AI-DIAG1` remains **NOT_BUILT / NOT_BUILD_READY**. No profile, build controller, runtime controller, candidate identity, Gale state or gameplay authorization changes are made by this review.
