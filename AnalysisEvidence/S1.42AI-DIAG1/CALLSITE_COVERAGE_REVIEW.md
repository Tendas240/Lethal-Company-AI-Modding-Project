# S1.42AI-DIAG1 Exact Spawn Callsite Coverage Review

**Status:** ANALYSIS-ONLY / EXACT-SOURCE COVERAGE PASS / NO IMPLEMENTATION / NO BUILD AUTHORIZATION  
**Canonical base:** `main@f058f8ff40d05bbcab691321b27b2164971b8b70`  
**Analysis branch:** `analysis/s142ai-diag1-callsite-coverage`  
**Decisive workflow run:** `34744968924` / run number `4` / `SUCCESS`  
**Decisive analysis head:** `e3c0a64b7e93dfebb3e181d7a4bbb93817d272ee`  
**Artifact:** `10314105406` — `s142ai-diag1-exact-callsite-coverage`  
**Artifact digest:** `sha256:1101dfd4d50b658342d47342e51b715e8a59524e7bb87e4213b9a0336f707139`  
**Matrix SHA-256:** `03e6c6ae6431df22ba8eeade75aa576f2b7a9c011294f1dc306a1d8bd5992af5`  
**Rendered matrix SHA-256:** `f571af592e7580613e8ff787c4dd4f5f01528720a45e33a6e82a21cc67761dd3`  
**Source inventory SHA-256:** `f92bb99d56c4f3516c82e4e92b40e281a62bec6f3d4e7fe5fa2e4b1c6818e24c`

## Evidence boundary

This review does not fetch new package versions and does not infer new runtime behavior. The workflow consumes the already exact-reviewed source artifacts from runs `34529045495`, `34614454120`, `34616289395`, `34705834727`, `34708556035`, `34709775849`, `34710724733`, `34711742173`, `34713018420`, `34714066827`, `34714900794` and `34716488701`, plus the preserved Installed-V81 RoundManager and vent/nest source captures in the repository.

The workflow inventories 148 exact source files and analyzes 73 primary source files after intentionally preferring C# over duplicate C#/IL copies. Installed-V81 vent assignment remains IL-backed because that is the exact preserved evidence form. The generated matrix contains **70 semantically relevant spawn/queue callsites and 0 unclassified rows**.

The installed-set conclusions that SnowyLib and `InteractiveTerminalAPI.Tools.SpawnMob` have no external static consumers remain anchored by the separate exact installed-set review run `34715820639`; the BCMER external execution-consumer conclusion remains anchored by run `34716828573`. This matrix uses those already-closed gates as classifications rather than pretending its narrower source set re-proved them.

An earlier successful matrix run deliberately exposed over-conservative duplicate/registration hits. The final analyzer removes C#/IL duplicate inflation, supports generic `Instantiate<T>(enemyPrefab)` forms, excludes generated RPC handlers and reference stubs, and rejects C# field initializers as method headers. That final correction removed the false `WeatherRegistryCompat.ContainsKey` row and simultaneously exposed the real `CodeRebirth.EnemyLevelSpawner.SpawnRandomEnemy()` callsite, leaving the final semantic count at 70.

## Coverage categories

- `ALLOW_EXACT_SHYGUY_OWNER`: 3
- `BCMER_EVENT_CONFIG_CONSTRAINED`: 1
- `NATIVE_QUEUE_CONSUMER_COVERED`: 1
- `NATIVE_SELECTOR_GUARD_REQUIRED`: 1
- `NO_ACTIVE_CONSUMER_STATIC_SET`: 3
- `OWNER_GUARD_REQUIRED`: 46
- `PARENT_PREVENTION_CANDIDATE`: 4
- `POOL_QUARANTINE_COVERED`: 3
- `RUNTIME_GATED_ASSERTION`: 3
- `SHARED_SINK_FORBIDDEN`: 3
- `STATEFUL_SCHEDULER_GUARD_REQUIRED`: 2

These counts are a coverage inventory, not a proposed count of Harmony patches. Multiple rows can collapse under one earlier owner decision after exact reachability/side-effect review. Conversely, a row may require a narrowly targeted caller branch rather than a whole-method prefix.

## Exact callsite matrix

| Category | Source | Class | Method | Primitives |
|---|---|---|---|---|
| `ALLOW_EXACT_SHYGUY_OWNER` | `theunknowncod3r-Scopophobia-Scopophobia.ShyGuyPaintingProp.txt` | `ShyGuyPaintingProp` | `SpawnEnemyOnServer` | enemy_type, spawn_game_object, spawn_on_server |
| `ALLOW_EXACT_SHYGUY_OWNER` | `theunknowncod3r-Scopophobia-Scopophobia.ShyGuyPaintingProp.txt` | `ShyGuyPaintingProp` | `SpawnEnemyServerRpc` | spawn_on_server, spawn_server_rpc |
| `ALLOW_EXACT_SHYGUY_OWNER` | `theunknowncod3r-Scopophobia-Scopophobia.ShyGuyPaintingProp.txt` | `ShyGuyPaintingProp` | `StartSpawnShyGuy` | spawn_on_server, spawn_server_rpc |
| `BCMER_EVENT_CONFIG_CONSTRAINED` | `BrutalCompanyMinus-1.71.0.cs` | `KiwiBird` | `Execute` | enemy_type, spawn_game_object |
| `NATIVE_QUEUE_CONSUMER_COVERED` | `ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt` | `<unknown>` | `SpawnEnemyFromVent` | spawn_on_server, vent_state |
| `NATIVE_SELECTOR_GUARD_REQUIRED` | `V81_VENT_NEST_LIFECYCLE_FOCUSED_IL.txt` | `<il>` | `AssignRandomEnemyToVent` | enemy_type, vent_state |
| `NO_ACTIVE_CONSUMER_STATIC_SET` | `InteractiveTerminalAPI-1.3.3.cs` | `Tools` | `SpawnMob` | enemy_type, spawn_on_server |
| `NO_ACTIVE_CONSUMER_STATIC_SET` | `SnowyLib-1.13.1.cs` | `NetworkHandler` | `SpawnEnemyRpc` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `NO_ACTIVE_CONSUMER_STATIC_SET` | `SnowyLib-1.13.1.cs` | `Utils` | `SpawnEnemy` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `ArcadiaMoonPlugin-1.0.2.cs` | `EnemySpawner` | `SpawnEnemyAtPosition` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `Biodiversity-0.2.9.cs` | `BuriedScrapObject` | `TryManageBuriedEnemy` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `Biodiversity-0.2.9.cs` | `MaskedMugItem` | `SpawnMaskedEnemyServerRpc` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `Biodiversity-0.2.9.cs` | `MicBirdAI` | `SpawnMicBird` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `Biodiversity-0.2.9.cs` | `OgopogoAI` | `SpawnVermin` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `Biodiversity-0.2.9.cs` | `VerminAI` | `SpawnVermin` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `ChillaxScraps-1.6.6.cs` | `Effects` | `Spawn` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `ChillaxScraps-1.6.6.cs` | `Effects` | `SpawnMaskedOfPlayer` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `CodeRebirth-1.6.9.cs` | `BoxChute` | `SpawnEnemy` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `CodeRebirth-1.6.9.cs` | `EnemyLevelSpawner` | `SpawnRandomEnemy` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `CodeRebirth-1.6.9.cs` | `FakeSnailCat` | `Update` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `CodeRebirth-1.6.9.cs` | `GuardPhone` | `SpawnWithDelay` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `CodeRebirth-1.6.9.cs` | `Puppeteer` | `SwitchToStateAfterDelay` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `CodeRebirth-1.6.9.cs` | `TornadoWeather` | `SpawnTornado` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `CodeRebirth-1.6.9.cs` | `Xui` | `OnNetworkDespawn` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `FacelessStalker-1.2.1.cs` | `SpawnSlendermanEnemyItem` | `SpawnSlendermanServerRpc` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `Football-1.1.14.cs` | `TrainProp` | `ForceSpawnEnemy` | spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `Herobrine-1.3.9.cs` | `HerobrineNetworking` | `cmd_Spawn` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `Herobrine-1.3.9.cs` | `RedstoneTorchProp` | `ForceSpawnEnemy` | enemy_type, spawn_game_object, vent_state |
| `OWNER_GUARD_REQUIRED` | `JLL-1.10.1.cs` | `EnemySpawner` | `SpawnEnemy` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `KenjiLib-0.7.0.cs` | `KLightsEvent` | `PermanentPowerOffRoutine` | enemy_type, spawn_game_object, vent_state |
| `OWNER_GUARD_REQUIRED` | `KenjiLib-0.7.0.cs` | `KLightsEvent` | `TriggerAppyEventRoutine` | enemy_type, spawn_game_object, vent_state |
| `OWNER_GUARD_REQUIRED` | `Lategame_Upgrades-3.14.1.cs` | `Tools` | `SpawnMob` | enemy_type, spawn_on_server |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `EndlessElevatorPatch` | `WaitRespawnPikmin` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `GlowSeed` | `SpawnGlowPikminClientRpc` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `Lumiknull` | `DoGlowSpawn` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `Onion` | `SetEnemyToBeRevived` | enemy_revival |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `Onion` | `SpawnPikmin` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PikUtils` | `ReviveEnemy` | enemy_prefab_instantiate, enemy_revival, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PikminManager` | `SpawnMapPikmin` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PikminManager` | `SpawnPikmin` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PikminManager` | `SpawnPikminIntervalled` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PikminManager` | `SpawnPikminOnServer` | enemy_prefab_instantiate, enemy_type, network_spawn, pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PikminManager` | `SpawnPikminOnServer` | enemy_prefab_instantiate, enemy_type, network_spawn, pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PikminManager` | `SpawnPikminServerRpc` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `PuffminAI` | `TransformIntoPikminServerRpc` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `Sprout` | `PluckAndDespawnServerRpc` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `Sprout` | `SpawnPikminOnServer` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `Sprout` | `SpawnPikminServerRpc` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `LethalMinNightly-1.1.108.cs` | `Triknull` | `DoGlowSpawn` | pikmin_spawn |
| `OWNER_GUARD_REQUIRED` | `PremiumScraps-2.5.0.cs` | `Effects` | `Spawn` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `OWNER_GUARD_REQUIRED` | `PremiumScraps-2.5.0.cs` | `Effects` | `SpawnMaskedOfPlayer` | enemy_type, spawn_game_object |
| `OWNER_GUARD_REQUIRED` | `PremiumScraps-2.5.0.cs` | `HarryDoll` | `DiscardItem` | spawn_server_rpc |
| `OWNER_GUARD_REQUIRED` | `PremiumScraps-2.5.0.cs` | `HarryDoll` | `SpawnEnemyServerRpc` | spawn_server_rpc |
| `OWNER_GUARD_REQUIRED` | `itolib-0.9.3.cs` | `EventfulApparatus` | `HandleDisconnect` | enemy_type, spawn_game_object, vent_state |
| `OWNER_GUARD_REQUIRED` | `itolib-0.9.3.cs` | `TwinApparatus` | `HandleDisconnect` | enemy_type, spawn_game_object, vent_state |
| `PARENT_PREVENTION_CANDIDATE` | `CodeRebirth-1.6.9.cs` | `CutieFlyAI` | `HandleSpawningMonarch` | enemy_type, spawn_game_object |
| `PARENT_PREVENTION_CANDIDATE` | `CodeRebirth-1.6.9.cs` | `Monarch` | `OnNetworkSpawn` | enemy_type, spawn_game_object, vent_state |
| `PARENT_PREVENTION_CANDIDATE` | `Haunted_Harpist-1.3.24.cs` | `BagpipesGhostAIServer` | `SpawnEscorts` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `PARENT_PREVENTION_CANDIDATE` | `LethalMinNightly-1.1.108.cs` | `PikminAI` | `TransformIntoPuffminServerRpc` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `POOL_QUARANTINE_COVERED` | `ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt` | `<unknown>` | `SpawnRandomDaytimeEnemy` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `POOL_QUARANTINE_COVERED` | `ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt` | `<unknown>` | `SpawnRandomOutsideEnemy` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `POOL_QUARANTINE_COVERED` | `ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt` | `<unknown>` | `SpawnRandomWeedEnemy` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `RUNTIME_GATED_ASSERTION` | `Bozoros-2.9.3.cs` | `PufferInfestationDiceEffect` | `SpawnPufferServerRpc` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `RUNTIME_GATED_ASSERTION` | `Bozoros-2.9.3.cs` | `SantaVisitDiceEffect` | `SpawnButlerServerRpc` | enemy_prefab_instantiate, enemy_type, network_spawn |
| `RUNTIME_GATED_ASSERTION` | `MoreCompany-1.14.0.cs` | `DebugCommandRegistry` | `HandleCommand` | enemy_type, network_spawn, spawn_game_object |
| `SHARED_SINK_FORBIDDEN` | `ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt` | `<unknown>` | `SpawnEnemyGameObject` | enemy_prefab_instantiate, enemy_type, network_spawn, spawn_game_object |
| `SHARED_SINK_FORBIDDEN` | `ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt` | `<unknown>` | `SpawnEnemyOnServer` | spawn_game_object, spawn_on_server, spawn_server_rpc |
| `SHARED_SINK_FORBIDDEN` | `ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt` | `<unknown>` | `SpawnEnemyServerRpc` | spawn_game_object, spawn_server_rpc |
| `STATEFUL_SCHEDULER_GUARD_REQUIRED` | `ButteRyBalance-0.7.0.cs` | `InfestationOverrides` | `SpawnInfestationWave` | enemy_type, vent_state |
| `STATEFUL_SCHEDULER_GUARD_REQUIRED` | `SpawnCycleFixes-1.2.2.cs` | `Patches` | `RoundManager_Post_AssignRandomEnemyToVent` | enemy_type, vent_state |

## Important new closure facts

The machine inventory confirms the full-source Biodiversity finding that motivated this review. The exact `Biodiversity-0.2.9.cs` source has five relevant rows: independent `BuriedScrapObject.TryManageBuriedEnemy`, Masked Mug spawn ownership, and MicBird/Ogopogo/Vermin direct child creation. They cannot be omitted merely because the earlier human summary emphasized the Masked Mug path.

The matrix also directly contains both PremiumScraps and ChillaxScraps central Masked routes plus their separate direct prefab/network-spawn helpers, the FacelessStalker page/RPC route, the Haunted Harpist escort path, the LethalMin creation/revival family, the CodeRebirth owner family, native outside/daytime/weed direct creation, vent assignment, and the stateful ButteRyBalance/SpawnCycleFixes scheduling paths.

The three native shared sinks remain explicitly `SHARED_SINK_FORBIDDEN`: the matrix is not permission to add a blanket `SpawnEnemyGameObject`, `SpawnEnemyOnServer`, `SpawnEnemyServerRpc`, `NetworkObject.Spawn`, `EnemyAI.Start` or post-spawn cleanup guard.

The exact Shy Guy painting path is intentionally allowed by identity and remains separate from BCMER evidence. A painting-spawned Shy Guy cannot satisfy the positive BCMER-event execution gate. Exterior Shy Guy remains allowed through identity filtering so an exterior defect remains observable rather than being hidden by the diagnostic.

## Remaining implementation gate

This review closes the **callsite discovery/completeness** subproblem for the exact previously reviewed S1.42AI static source set. It does **not** make DIAG1 build-ready by itself.

Before coding, reduce the 46 conservative `OWNER_GUARD_REQUIRED` rows and four `PARENT_PREVENTION_CANDIDATE` rows into the smallest exact guard set by proving caller reachability and the earliest side-effect-free decision point. In particular:

1. prove which child spawns become unreachable when their non-ShyGuy parent EnemyAI is prevented;
2. collapse LethalMin caller chains only at reviewed points before Onion/persistence/source-despawn mutation;
3. choose exact branch/owner guards for stateful CodeRebirth, item/event and apparatus routes rather than suppressing their whole lifecycle;
4. define the narrow native vent-assignment identity guard while preserving DawnLib/SpawnCycleFixes ordering and vent completion;
5. carry the static runtime-gated/no-consumer assertions into the final DIAG1 static build gate;
6. validate exact Harmony target signatures, host/server ownership, priority/order and default-off behavior for every chosen project-local hook.

Only after that guard-reduction/signature review passes may an implementation or repository-native diagnostic build be prepared. `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, S1.42AI acceptance state and all profile bytes remain untouched by this analysis.