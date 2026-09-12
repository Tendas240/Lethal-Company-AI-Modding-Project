# S1.42AI-DIAG1 direct SpawnEnemyGameObject candidate exact review

**Status:** EXACT_DIRECT_CANDIDATE_REVIEW_COMPLETE / DISCOVERY_SCOPE_STILL_OPEN / PATCH_SAFETY_PARTIAL / NOT_BUILD_READY  
**Canonical main reviewed:** `a9e508aabb2111f511ddf2790c0a4929092bdb15`  
**Remaining-package discovery:** run `34705334804`, head `45d22c3fa1abb3bbd95dd137cd3903eb053f87c7`  
**Exact-review run:** `34705834727`, head `72f00e1b3ab7aa6109d82087b1a0ecf337739f94`, SUCCESS  
**Exact-review artifact:** `10301920176`, `s142ai-direct-spawn-candidates-exact`, artifact ZIP digest `sha256:83c17bdb05d520fcdf9425e38d01ec10125914e2b5311161f80306e67fb04b6e`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope and evidence contract

This review closes only the first exact-review tranche selected from the successful remaining-package discovery: the ten enabled S1.42AI packages whose discovery IL contained a direct `RoundManager.SpawnEnemyGameObject` call. The exact-review workflow re-downloaded the same Thunderstore package versions, failed closed against the discovery ZIP SHA-256, DLL SHA-256 and complete decompiled-source SHA-256, and then captured full C# plus IL for method/caller/state review.

This is not a DIAG1 implementation approval. It does not classify the other discovery-positive packages as safe and does not change `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, any profile, or the accepted/active lifecycle. The existing project prohibition on a blanket `RoundManager.SpawnEnemyGameObject` deny remains in force and is strengthened by the concrete owner-state evidence below.

## Exact findings

### Zigzag-PremiumScraps 2.5.0

Assembly: `plugins/PremiumScraps.dll` (`380ffa37ff53576f561c27a9d06c30ecd35d9195606e142122647a0df583bf96`).

Confirmed central owner path: `PremiumScraps.Utils.Effects.SpawnMaskedOfPlayer(ulong playerId, Vector3 position)` calls `RoundManager.SpawnEnemyGameObject(..., PremiumScraps.Utils.GetEnemies.Masked.enemyType)`. The returned network object is required immediately afterward to set suit, assign `mimickingPlayer`, set inside/outside state and invoke `CreateMimicClientRpc`. A caller in the special-SFX coroutine reaches this path only on server/host and only for the inside-factory branch.

Separate confirmed non-central owner path in the same `Effects` type: `Spawn(SpawnableEnemyWithRarity enemy, Vector3 position, float yRot)` directly `Instantiate`s `enemy.enemyType.enemyPrefab`, calls `NetworkObject.Spawn(true)`, adds the resulting `EnemyAI` to `RoundManager.SpawnedEnemies`, and returns its `NetworkObjectReference`. The same special-SFX coroutine uses this path for Bunker Spider or Baboon Hawk spawns. Therefore filtering only `SpawnEnemyGameObject` would not isolate this package.

Classification: **CONFIRMED ACTIVE OWNER FAMILY; central Masked path plus separate direct Instantiate/network-spawn path.**

### Zigzag-ChillaxScraps 1.6.6

Assembly: `ChillaxScraps/ChillaxScraps.dll` (`1a448aaf93af58da00f16e7e7acf0c7e69b1bb564f084dc64020d06101bbb7d0`).

Confirmed central owner path: `ChillaxScraps.Utils.Effects.SpawnMaskedOfPlayer(ulong playerId, Vector3 position)` calls `SpawnEnemyGameObject(..., ChillaxScraps.Utils.GetEnemies.Masked.enemyType)` and then uses the returned network object to configure the Masked enemy's suit, mimicked player, inside/outside state and mimic ClientRpc.

Separate confirmed non-central owner path: `Effects.Spawn(SpawnableEnemyWithRarity enemy, Vector3 position, float yRot)` directly instantiates the enemy prefab, network-spawns it and appends its `EnemyAI` to `RoundManager.SpawnedEnemies`. A server RPC dispatch uses this helper for multiple caller-selected enemies, including Eyeless Dog, Redwood Titan/Redwood Giant/Forest Keeper, Baboon Hawk and optional special enemies, while ID 2 selects the central Masked path.

Classification: **CONFIRMED ACTIVE OWNER FAMILY; central Masked path plus separate direct Instantiate/network-spawn path.**

### rectorado-KenjiLib 0.7.0

Assembly: `KenjiLib.dll` (`3425ef267033ade207e7fb75bd9274ef4433a907e507a981c85b4050f550cccd`).

Confirmed owner: `KLightsEvent` has two direct Old Bird/rad-mech spawn paths. `PermanentPowerOffRoutine()` flickers lights, waits, switches power off and sets `RoundManager.powerOffPermanently = true` before optionally enumerating matching Old Bird nests and calling `SpawnEnemyGameObject`. It can then invoke JLL apparatus/event triggers. `TriggerAppyEventRoutine()` may raise `minEnemiesToSpawn`, flickers lights, permanently cuts power, shows the radiation warning, and only afterward spawns matching rad-mech enemies and optionally invokes JLL events. Public trigger methods start these coroutines, and `OnEnable()` may select them when configured.

Classification: **CONFIRMED STATEFUL EVENT OWNER.** A central spawn denial would occur after unrelated power/event state has already changed and cannot be used as the package-level prevention point.

### pacoito-itolib 0.9.3

Assembly: `BepInEx/plugins/itolib.dll` (`f454dcb67041914124f0f3ee415282b078409bb413ef51e3e9639a9d8dcb07d6`).

Confirmed owners: `EventfulApparatus.HandleDisconnect()` and `TwinApparatus.HandleDisconnect()` both contain direct Old Bird/rad-mech `SpawnEnemyGameObject` calls after substantial apparatus lifecycle work. Before the spawn gate these routines can stop/play apparatus audio, invoke disconnect events, mutate `minEnemiesToSpawn`, flicker lights, switch power, set `powerOffPermanently`, show radiation UI and invoke additional lifecycle events. `TwinApparatus.EquipItem()` also changes dock/power state, computes `bothPulled`, starts the disconnect coroutine and can invoke LLL dungeon/level apparatus events.

Classification: **CONFIRMED STATEFUL APPARATUS OWNER.** Blocking the shared central spawn after these mutations would not roll back apparatus state and is therefore not an acceptable isolation mechanism.

### notnotnotswipez-MoreCompany 1.14.0

Assembly: `BepInEx/plugins/MoreCompany.dll` (`d1947db8908fdf5b2d20a3e40c571099c656f6880434594e6997b20ec57b7fd7`).

Confirmed code path: `DebugCommandRegistry.HandleCommand(string[] args)` has a `spawnenemy` command that resolves an arbitrary `EnemyType` by name and calls `SpawnEnemyGameObject` near the local player. The caller is a Harmony prefix on `HUDManager.AddTextToChatOnServer`; it intercepts `/mc` chat only when `DebugCommandRegistry.commandEnabled` is true and the local instance is host.

The complete decompile contains the public static `commandEnabled` field and reads it in both the prefix and `HandleCommand`, but contains no assignment to that field. Consequently the route is **internally dormant by default in this assembly**, while still externally callable/enablable because the field is public static. It is not evidence of an autonomous normal-round owner.

Classification: **CONFIRMED DIRECT DEBUG/COMMAND ROUTE; internally dormant unless another actor enables it.**

### lethal_coder-31Arcadia_UPDATED 1.0.2

Assembly: `ArcadiaMoonPlugin.dll` (`c71866c7a2e4a0e1f2af1eb392aa41a428e584753f263ddc50efa8d7e75af4a0`).

Confirmed owner: `ArcadiaMoonPlugin.EnemySpawner`. `Start()` is host-only, resolves the configured `enemyName`, checks the package spawn toggle and, for enemies with a nest prefab, creates and network-spawns temporary nest objects. `Update()` waits for the configured time, destroys each stored temporary nest and then calls `SpawnEnemyAtPosition`; without a nest prefab it spawns at child transforms. `SpawnEnemyAtPosition` validates `enemyType.enemyPrefab` and calls `SpawnEnemyGameObject(..., enemyType)`. `Update()` then disables the spawner component. Package defaults bind deterministic force-spawn toggles for Flowerman, Baboon Hawk and RadMech to true, although actual scene/config activation remains a caller/config fact rather than an assumption from the default.

Classification: **CONFIRMED DETERMINISTIC HOST OWNER.** A central deny after the temporary nest has been destroyed would lose owner state; the exact owner-level enemy decision must be intercepted earlier if this path needs diagnostic filtering.

### Kittenji-Herobrine 1.3.9

Assembly: `BepInEx/plugins/HerobrineMod.dll` (`d4d7f4fa19ef1a9ceb0b1ef5b7108f39001e834deefc2247feb5af458211524e`).

Confirmed gameplay owner: `RedstoneTorchProp.ForceSpawnEnemy()`, called on the first server-side `GrabItem()` and also from `OnDestroy()` on Company Building. Before the spawn call it sets static `wasSpawnedThisRound = true`; after spawning `Plugin.EnemyDef` it may assign `HerobrineAI.PlayerSpawnedBy`, opens occupied Herobrine vents, and explicitly increments `Plugin.EnemyDef.numberSpawned`. A ship-leave patch resets `wasSpawnedThisRound`; other Herobrine lifecycle code can also set it true.

Confirmed separate developer route: `[DevCommand("spawn", true)] HerobrineNetworking.cmd_Spawn(string args)` host-spawns the same `Plugin.EnemyDef`, explicitly increments `numberSpawned`, and may assign `PlayerSpawnedBy`.

Classification: **CONFIRMED STATEFUL GAMEPLAY OWNER PLUS SEPARATE DEV-COMMAND OWNER.** A shared central deny after `wasSpawnedThisRound` has been set would suppress future owner attempts while not undoing that state.

### Kittenji-Football 1.1.14

Assembly: `BepInEx/plugins/FootballEntity.dll` (`7add08cb69f0d1d0ea83c229f23a44e1918d4753281b0117c768955beda02044`).

Confirmed owner: `TrainProp.ForceSpawnEnemy()`, called on first server-side `GrabItem()`. It checks round/ship/server state, sets static `wasSpawnedThisRound = true` before spawning `Plugin.EnemyDef`, chooses an outside AI node/fallback player position, and uses the returned network object to set `FootballAI.PlayerSpawnedBy`. A ship-leave patch resets the static round flag.

Classification: **CONFIRMED STATEFUL GAMEPLAY OWNER.** A central deny after the flag mutation would leave the Football owner believing its one-per-round spawn already occurred.

### JacobG5-JLL 1.10.1

Assembly: `BepInEx/plugins/JLL/JLL.dll` (`bbe20f86805f8cb90cf8c88893b27b664d39ea79107edc826e1089f0ac473f5a`).

Confirmed generic owner: `JLL.Components.EnemySpawner`. `Awake()` resolves configured enemy identities through JLL's registry. `OnEnable()` can call `SpawnEnemy()` when `spawnOnEnable` is set. Overloads delegate to `SpawnEnemy(Vector3 pos)`, which is host/server gated, selects either a fixed EnemyType or weighted random pool, optionally enforces enemy and power caps, validates prefab/navmesh, and can create/synchronize a missing outside nest before calling `SpawnEnemyGameObject`. If the returned object has `EnemyAI`, it invokes `SpawnedEvent` with that exact enemy.

Classification: **CONFIRMED GENERIC CONFIGURABLE OWNER WITH PRE-SPAWN NEST SIDE EFFECT AND POST-SPAWN EVENT CONTRACT.** Blanket central denial is not an owner-safe replacement for an identity check before nest/spawn work.

### super_fucking_cool_and_badass_team-Biodiversity 0.2.9

Assembly: `BepInEx/plugins/Biodiversity/com.github.biodiversitylc.Biodiversity.dll` (`6853a6430674721ffbc6ab13de0e85b2f921f05339bf33f167e8f391debf9f28`).

Confirmed owner: `Biodiversity.Items.JunkRadar.MaskedMugItem.SpawnMaskedEnemyServerRpc(ulong playerId, Vector3 position)`. The package resolves `enemyToSpawn` specifically from an EnemyType whose `enemyName == "Masked"`. A Harmony postfix on `PlayerControllerB.KillPlayer` invokes the ServerRpc when the Junk Radar feature is enabled and the retained Masked Mug owner is server-side. The RPC resolves an inside/outside navmesh position, spawns `enemyToSpawn.enemyType`, then unconditionally invokes `SyncMaskedEnemyClientRpc` with the returned reference.

The client-side sync coroutine is lifecycle-significant: it waits for network object/body availability, deactivates the dead player's body, then if the spawned object exists configures `MaskedPlayerEnemy.mimickingPlayer`, suit, inside/outside state and visibility, redirects the player to the enemy, and doubles enemy HP. Therefore denying only the central spawn while allowing the subsequent ClientRpc path to continue could still alter corpse/player state even if no enemy object was produced.

Classification: **CONFIRMED NETWORKED MASKED OWNER WITH REQUIRED POST-SPAWN CLIENT STATE.** Any diagnostic prevention must occur before this owner commits to the spawn/sync transaction, not at a shared central spawn method.

## Cross-package conclusions for DIAG1

1. All ten discovery candidates are real source-level `SpawnEnemyGameObject` call paths; none of the ten was a symbol-only false positive.
2. MoreCompany is the one materially different case: the path is a host debug command and no internal assignment enabling `commandEnabled` exists in the reviewed assembly. Keep it inventoried, but do not equate it with an autonomous gameplay owner.
3. PremiumScraps and ChillaxScraps each prove an additional, separate enemy creation path that bypasses `RoundManager.SpawnEnemyGameObject` entirely via direct prefab instantiation + `NetworkObject.Spawn(true)` + `RoundManager.SpawnedEnemies.Add(...)`. DIAG1 coverage cannot be defined around the central RoundManager method alone.
4. Football, Herobrine, KenjiLib, itolib, Arcadia, JLL and Biodiversity demonstrate concrete state/lifecycle contracts surrounding the central call. Suppressing the central method after owner-side state changes would leave stale one-per-round flags, destroyed/replaced nests, power/apparatus transitions, missing post-spawn events, or corpse/player synchronization effects.
5. This evidence therefore **confirms the existing prohibition on a blanket `RoundManager.SpawnEnemyGameObject` deny**. The future diagnostic must filter at the smallest reviewed owner decision before destructive/stateful side effects, or use another interception whose full contract is separately proven safe.
6. The exact remaining-package discovery is not yet fully patch-safe: the other 43 positive candidate packages still require bounded triage/exact escalation according to their signature strength. BCMER forced/side/additional/runtime-custom execution coverage and exact Shy Guy project source-to-DLL provenance also remain separate open gates.

## Build/runtime gate

`S1.42AI-DIAG1` remains **PLANNED_NOT_BUILT**. This review does not authorize a build, Gale import, gameplay test, controller transition, global `NetworkObject.Spawn` interception, broad EnemyAI lifecycle suppression, post-spawn cleanup, or removal of unexpected exterior Shy Guys.
