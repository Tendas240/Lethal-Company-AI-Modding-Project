# S1.42AI-DIAG1 Tier-A remaining spawn-owner exact review

**Status:** EXACT_TIER_A_REVIEW_COMPLETE / PATCH_SAFETY_PARTIAL / NOT_BUILD_READY  
**Canonical main reviewed:** `2915f2f04505581bec5056b3801130cc649aa1cf`  
**Successful exact-review run:** `34708556035`, run number `3`, head `1900cae19659a52ed30b400a143393bd1d109d7d`, SUCCESS  
**Artifact:** `10301933941`, `s142ai-tier-a-spawn-candidates-exact`, ZIP digest `sha256:8d1ebd346e83fd5f4334a6693036e5d068dc08d51457a6e94b642333bd23e79f`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope and provenance

This is the exact-review tranche selected from the six strongest still-unreviewed discovery positives in `SourceEvidence/NativeSpawnOwners/20260912T163027Z-RemainingEnabledDiscovery/VERIFICATION.json`:

- `ButteryStancakes-ButteRyBalance 0.7.0`;
- `malco-Lategame_Upgrades 3.14.1`;
- `Sparble-FacelessStalker 1.2.1`;
- `Snowlance-SnowyLib 1.13.1`;
- `IAmBatby-LethalLevelLoader 1.7.12`;
- `Bob123-Haunted_Harpist 1.3.24`.

The read-only Actions capture re-downloaded the exact Thunderstore package versions and required exact package ZIP SHA-256, DLL member path/SHA-256 and complete C# decompile SHA-256 to match discovery run `34705334804`. It then preserved complete C# and IL from pinned ILSpy 11.0.0.9375. Any mismatch failed closed.

Two earlier analysis-harness runs failed closed before this successful capture and are not source findings: run `34708438809` used shallow checkout, so the canonical-main ancestor guard could not see history; run `34708476341` exposed a manually transcribed SnowyLib expected-DLL-hash typo. The reported actual SnowyLib DLL hash exactly matched the original discovery authority; only the analysis literal was corrected. Run `34708556035` then passed all six ZIP/DLL/source-SHA gates.

## 1. ButteRyBalance 0.7.0 — confirmed stateful vent-scheduling spawn owner

Exact DLL: `ButteRyBalance.dll`, SHA-256 `d13c7996645c9cf34e2806acbd511972229aaf8874991524a56077390a63cf0e`.

The discovery hit is a real gameplay spawn-ownership family, not a generic `Instantiate` false positive. `RoundManagerPatches.RoundManager_Post_RefreshEnemiesList` runs `InfestationOverrides.CustomInfestation(...)` on the server when the infestation rework is active, an infestation is selected (or the configured Embrion special case selects one), and SpawnCycleFixes is installed. `CustomInfestation` takes ownership of infestation state before any actual vent spawn: it clears/replaces `enemyRushIndex`, selects an EnemyType from current-level interior enemies, sets that EnemyType's `PowerLevel` to zero, may alter `MaxCount`, and changes `currentMaxInsidePower` / `increasedInsideEnemySpawnRateIndex`. `EndInfestation` later owns restoration of those values.

`InfestationOverrides.SpawnInfestationWave()` is called from server-side RoundManager hooks around hourly plotting and exhausted outside spawning. For up to two enemies it selects an unoccupied `EnemyVent`, writes `enemyType`, `enemyTypeIndex`, `occupied` and `spawnTime`, may sync the vent time, increments the EnemyType's `numberSpawned`, sets `hasSpawnedAtLeastOne`, and increments `currentInsideEnemyDiversityLevel` before native vent execution later creates the enemy.

**Classification:** `CONFIRMED_STATEFUL_VENT_SCHEDULING_OWNER`.

**Patch-safety consequence:** a later denial at `SpawnEnemyGameObject` / shared network spawn does not undo the already-committed infestation EnemyType mutations, vent occupancy/timing, number-spawned or diversity bookkeeping. DIAG1 prevention for this path must occur at an owner decision point before those non-allowlisted commitments, or otherwise preserve/restore the complete reviewed transaction. Globally disabling ButteRyBalance or its RoundManager lifecycle is not justified.

## 2. Lategame Upgrades 3.14.1 — confirmed contract-driven explicit enemy spawn owner

Exact DLL: `BepInEx/plugins/MoreShipUpgrades/MoreShipUpgrades.dll`, SHA-256 `c3c6da8a2ad57930ec91db9df24223379a27bd0e0dcc60cf21fb1c9472f20465`.

`MoreShipUpgrades.Helpers.Tools.SpawnMob(string mob, Vector3 position, int numToSpawn)` scans `RoundManager.Instance.currentLevel.Enemies` by `enemyType.enemyName` and calls `RoundManager.Instance.SpawnEnemyOnServer(position, 0f, i)` once per requested spawn. This is a real enemy-spawn API owned by the package.

Two gameplay caller families are present:

- the Exorcism failure coroutine explodes first, then on the host calls `SpawnMob("Girl", ...)`, falling back to `SpawnMob("Crawler", ...)` when the Girl lookup returns false; its configured default failure count is 3;
- `ContractObject.Start()` is server-gated, positions the contract object, and for `contractType == "Exterminator"` calls `SpawnMob("Hoarding bug", ...)`; its configured default count is 20.

The package separately has many `Instantiate + NetworkObject.Spawn` paths for store, scrap and contract infrastructure; those are not EnemyAI evidence and must not be conflated with `SpawnMob`.

**Classification:** `CONFIRMED_CONTRACT_DRIVEN_EXPLICIT_ENEMY_SPAWN_OWNER`.

**Patch-safety consequence:** `SpawnMob` itself has meaningful boolean return semantics: Exorcism treats `false` as permission to try the Crawler fallback. A diagnostic interception cannot blindly return failure for a blocked enemy without changing the caller's branch. The Exorcism caller also performs explosion/audio/placed/collider state before the enemy spawn request, while the Exterminator caller may reposition its contract object first. Preserve those unrelated contract responsibilities and block only the non-allowlisted enemy creation decision.

## 3. FacelessStalker 1.2.1 — confirmed page-item direct network spawn owner

Exact DLL: `FacelessStalker/SlendermanMod.dll`, SHA-256 `0957f55e0aa69f83167d4f1e7e6b261c174d1412b1d06fcf4df0e708e83dbce8`.

The plugin registers `SlendermanEnemy.enemyPrefab` normally, but its collectible page items add a second direct owner path. `SpawnSlendermanEnemyItem.EquipItem()` checks that the round can spawn enemies, that no Slenderman is currently tracked and that the item has not already been used. It calls `SpawnSlenderman()`, which computes a position near the local player and calls `SpawnSlendermanServerRpc(position)`; the item then sets its local `isSpawned = true`.

The ServerRpc is `RequireOwnership = false`, executes only on server/host, re-checks `isSpawned`, and directly performs `Object.Instantiate(slendermanEnemy.enemyPrefab, ...)` followed by the prefab's `NetworkObject.Spawn(true)`. It does not route through `RoundManager.SpawnEnemyGameObject`. The spawned `SlendermanEnemyAI.Start()` is server-gated and then initializes AI state, chooses a target, syncs `numSlendermanEnemiesInLevel`, teleports/animates and may play spawn SFX; `OnDestroy()` owns tracker cleanup.

**Classification:** `CONFIRMED_PAGE_ITEM_DIRECT_NETWORK_SPAWN_OWNER`.

**Patch-safety consequence:** native pool filtering does not cover the page path. Shared `NetworkObject.Spawn` suppression is too late and too broad; the exact page/RPC owner decision must be considered so no local instantiated EnemyAI or half-started Slenderman lifecycle is left behind, while page/item behavior unrelated to the blocked spawn remains intact.

## 4. SnowyLib 1.13.1 — generic spawn API infrastructure, not an autonomous normal-stack owner in this assembly

Exact DLL: `Snowlance.SnowyLib.dll`, SHA-256 `cdbb80c8b0afa3e65acae83e25bd00fb704cefbeb2e14ccc561f1d959b0c3c95`.

SnowyLib exposes real generic enemy-creation surfaces:

- `NetworkHandler.SpawnEnemyRpc(...)` executes on the server, resolves a `DawnEnemyInfo`, directly instantiates its `EnemyType.enemyPrefab`, network-spawns the EnemyAI and appends it to `RoundManager.SpawnedEnemies`;
- `Utils.SpawnEnemy(key, position, ...)` is server/host gated and performs the same direct instantiate/network-spawn/list-add transaction;
- `Utils.SpawnEnemy(key, EnemyVent, spawnDelay)` is server/host gated and writes the vent EnemyType/index/occupied/spawnTime, then either calls native `SpawnEnemyFromVent` immediately or syncs the delayed vent.

Within this exact SnowyLib assembly, no normal gameplay caller of `SpawnEnemyRpc` or the direct position overload was found beyond the generated RPC handler. The vent overload is called by SnowyLib's `/spawnenemy` chat command, and `Utils.ChatCommand` returns immediately unless `Debugging / Testing` is true; that config defaults false. The library's normal startup only creates its own NetworkHandler infrastructure.

**Classification:** `GENERIC_SPAWN_API_INFRASTRUCTURE_NO_AUTONOMOUS_NORMAL_CALLER_FOUND`.

**Patch-safety consequence:** SnowyLib cannot be marked globally irrelevant: another installed assembly can call these public APIs. Cross-assembly consumer coverage remains required. Patching these generic library sinks without enumerating consumers would repeat the same broad-callee problem already forbidden for vanilla/network shared methods. The internal testing command alone is not a normal-stack owner.

## 5. LethalLevelLoader 1.7.12 — spawn observer/downstream contract, not an EnemyAI creation owner in this evidence

Exact DLL: `LethalLevelLoader.dll`, SHA-256 `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`.

The sole `SpawnEnemyGameObject` occurrence is a Harmony target declaration, not a call. `EventPatches.RoundManagerSpawnEventFromVent_Prefix(EnemyVent vent)` caches the selected vent before native `RoundManager.SpawnEnemyFromVent`. A postfix on native `RoundManager.SpawnEnemyGameObject` then assumes the spawn completed, reads the last entry of `RoundManager.SpawnedEnemies`, and emits both dungeon-local and global `onEnemySpawnedFromVent` events before clearing the cached vent.

The assembly's `Object.Instantiate`/`NetworkObject.Spawn` pairs create LethalLevelLoader networking-manager infrastructure, not EnemyAI. Other instantiate uses are weather-prefab overrides. EnemyType/enemyPrefab-heavy code primarily validates, registers, extracts and restores content references and level enemy pools.

**Classification:** `SPAWN_OBSERVER_DOWNSTREAM_CONTRACT_NOT_ENEMY_CREATION_OWNER`.

**Patch-safety consequence:** this is still highly relevant to interception design. A blanket denial of native `SpawnEnemyGameObject` can leave LethalLevelLoader's postfix running with a cached vent but no newly appended enemy; it may observe the wrong previous `SpawnedEnemies` element or fail when the list is empty. Therefore the existing central-denial prohibition is strengthened even though LethalLevelLoader itself is not a creation owner.

## 6. Haunted Harpist 1.3.24 — confirmed server-side escort direct network spawn owner

Exact DLL: `BepInEx/plugins/HauntedHarpist/LethalCompanyHarpGhost.dll`, SHA-256 `d8d35767d74e3226c6adf8728fc4269a2fac4e05e11da2842f22858fc23c2ac0`.

The plugin registers its Harp, Bagpipes and Enforcer enemy types normally. In addition, `BagpipesGhostAIServer.Start()` calls base EnemyAI startup, returns on non-server peers, initializes its server AI/netcode/config and instrument state, then starts `SpawnEscorts(...)` when the Enforcer enemy prefab exists.

After a delay, `SpawnEscorts` loops `numberOfEscorts` (configured through the synchronized Bagpipes Ghost escort-count setting). Each iteration directly instantiates `HarpGhostPlugin.EnforcerGhostEnemyType.enemyPrefab`, network-spawns it, increments `RoundManager.currentEnemyPower` by the Enforcer PowerLevel, finds the Enforcer entry in the current indoor enemy list, increments its `numberSpawned`, configures the resulting `EnforcerGhostAIServer`, adds it to the Bagpipes Ghost's escort collection, and spaces successive spawns by one second.

**Classification:** `CONFIRMED_SERVER_SIDE_ESCORT_DIRECT_NETWORK_SPAWN_OWNER`.

**Patch-safety consequence:** pool filtering cannot cover these escort spawns. A shared network-spawn denial would occur after local `Instantiate` and before the package's subsequent power/count/escort transaction, leaving inconsistent object/lifecycle state. Prevention needs to act at the reviewed escort owner decision before non-allowlisted instantiation while preserving the Bagpipes Ghost's own initialization, instrument and network responsibilities.

## Cross-package result

The six-package Tier-A escalation resolves as:

1. ButteRyBalance — confirmed stateful vent-scheduling owner;
2. Lategame Upgrades — confirmed contract-driven explicit enemy owner;
3. FacelessStalker — confirmed direct page/RPC enemy owner;
4. SnowyLib — generic spawn infrastructure with no autonomous normal caller found inside this assembly; external consumers remain to be traced;
5. LethalLevelLoader — observer/downstream spawn-event contract, not an enemy creation owner;
6. Haunted Harpist — confirmed direct server-side escort enemy owner.

Thus **four of six are confirmed gameplay spawn owners**, while the other two remain important for coverage/design for different reasons. The unreviewed discovery-positive package count is reduced from 43 to **37**, but patch safety is not closed: SnowyLib cross-assembly consumers must still be accounted for, the remaining 37 positives require bounded escalation, BCMER forced/forced-side/additional/runtime-custom execution remains separate, and the exact Shy Guy/project-DLL provenance and final host/client-safe interception design remain open.

No DIAG1 implementation, profile build, controller transition, Gale import or gameplay test is authorized by this review. `S1.42AI-DIAG1` remains **PLANNED_NOT_BUILT / NOT_BUILD_READY**.
