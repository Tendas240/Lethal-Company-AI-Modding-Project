# S1.42AI-DIAG1 Minimal Guard Contract

**Status:** ANALYSIS-ONLY / GUARD-REDUCTION COMPLETE / IMPLEMENTATION CONTRACT READY / BUILD NOT AUTHORIZED  
**Canonical base:** `main@f058f8ff40d05bbcab691321b27b2164971b8b70`  
**Input coverage:** `analysis/s142ai-diag1-callsite-coverage` decisive run `34744968924`, 70 semantic spawn/queue transactions, 0 unclassified  
**Plan:** `BuildSpecs/S1.42AI_PLAN.md`  
**Patch-safety authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Decision

The 70-row exact callsite inventory is a completeness boundary, not a 70-patch design. The safe DIAG1 implementation is a temporary, default-off diagnostic plugin plus a small diagnostic config overlay. It must preserve package versions, the S1.42AI correction, existing S139CompatibilityFixes bytes, and all build/runtime controllers until a later atomic build transition.

The final design uses four layers:

1. exact Shy Guy identity resolution;
2. native pool/vent quarantine with deterministic Harmony ordering;
3. narrow config gates for owners that already expose an exact pre-spawn switch;
4. exact package-owner guards only where config/pool/parent prevention cannot close the route.

No blanket patch of `RoundManager.SpawnEnemyGameObject`, `RoundManager.SpawnEnemyOnServer`, `RoundManager.SpawnEnemyServerRpc`, `NetworkObject.Spawn`, `EnemyAI.Start`, `EnemyAI.UseNestSpawnObject`, or a whole foreign component is authorized.

## Exact allowed identity

DIAG1 must resolve one and only one `EnemyType` for which all three facts agree:

- Unity asset/object identity: `ShyGuyDef`;
- `EnemyType.enemyName == "Shy Guy"`;
- prefab contains component full type `ShyGuy.AI.ShyGuyAI`.

The resolver is one-shot / lifecycle-bound, not a per-frame global scan. Missing, ambiguous, or contradictory identity is `FAIL_CLOSED`: no non-verified enemy identity is permitted and the run must emit an explicit diagnostic-invalid marker. Location is never part of the allow decision. An exterior Shy Guy remains allowed and observable so the correction can fail visibly.

## Diagnostic config overlay

These are temporary DIAG1-only changes. They are not acceptance-state changes and must be absent from the later full-normal candidate.

### Existing BCMER plan

Keep the already-reviewed S1.42AI-DIAG1 BCMER overlay from `BuildSpecs/S1.42AI_PLAN.md`: only event `[ShyGuy]` enabled; custom events disabled; one normal event draw; no bonus draw; forced/forced-side/additional/runtime-custom execution remains constrained by the already-closed exact execution/consumer reviews. No broad BCMER Harmony patch is added.

### Additional exact owner gates

- `BepInEx/config/ArcadiaMoonPlugin.cfg`
  - `ForceSpawnFlowerman = false`
  - `ForceSpawnBaboon = false`
  - `ForceSpawnRadMech = false`
  - This disables the three deterministic host owner routes before temporary nest destruction/spawn work.

- `BepInEx/config/butterystancakes.lethalcompany.butterybalance.cfg`
  - `[Infestations] Rework Mechanics = false`
  - This removes ButteRyBalance's stateful custom infestation scheduler before it reserves vent/power/count state. SpawnCycleFixes remains installed and otherwise unchanged.

- `BepInEx/config/me.biodiversity.junk_radar.cfg`
  - `[_General] Enabled = false`
  - Exact Biodiversity source checks this value both before Junk Radar/buried-scrap generation and before the Masked Mug kill-to-Masked transaction. This closes `BuriedScrapObject.TryManageBuriedEnemy` and `MaskedMugItem.SpawnMaskedEnemyServerRpc` without patching player death or buried-item lifecycle.

- `BepInEx/config/me.biodiversity.ogopogo.cfg`
  - assert existing `EnableVermin = false`
  - assert existing `OgopogoEnabled = false`
  - no new change is needed; the build gate must fail if either is no longer false.

- `BepInEx/config/sparble.slendermanmod.cfg`
  - `[PageItem.Values] Page Spawning =` empty
  - assert `[Slenderman] Natural Spawn Chances = 0`
  - Exact parser behavior turns an empty page string into empty vanilla/custom rarity dictionaries. A runtime owner guard below still covers a page that survived from prior save state.

- `BepInEx/config/NoteBoxz.LethalMin.cfg`
  - `[Spawning] Indoor Pikmin Spawn Chance = 0`
  - `[Spawning] Outdoor Pikmin Spawn Chance = 0`
  - `[Spawning] Onion Spawn Chance = 0`
  - `[Glow Pikmin] Spawn Chance = 0`
  - These disable autonomous map/onion/glow creation but do not disable LethalMin itself. Persistence/item/manual owner routes are guarded below.

## Native pool and vent guard set

All hooks install only while the DIAG1 diagnostic flag is true. Exact target resolution is declared-only/signature-checked and must fail closed if the V81 contract differs.

### `RoundManager.PredictAllOutsideEnemies`

- patch: Prefix, `Priority.First`;
- action: quarantine `currentLevel.Enemies`, `currentLevel.OutsideEnemies`, `currentLevel.DaytimeEnemies`, and `RoundManager.WeedEnemies` to exact Shy Guy only;
- reason: this deterministically runs before SpawnCycleFixes' default-priority replacement predictor;
- forbidden alternative: skip prediction or suppress nest creation.

### `RoundManager.BeginEnemySpawning`

- patch: Prefix, `Priority.First`;
- action: reassert all four pools before SpawnCycleFixes' prefix immediately runs daytime/outside/weed batches;
- forbidden alternative: skip `BeginEnemySpawning`.

### `RoundManager.PlotOutEnemiesForNextHour`

- patch: Prefix, `Priority.First`;
- action: reassert the indoor pool before vent selection/scheduling;
- reason: prevents late pool repopulation from entering native scheduling while preserving plotting and SpawnCycleFixes' schedule rebuild;
- forbidden alternative: skip plotting.

### `RoundManager.FinishGeneratingNewLevelClientRpc`

- patch: Postfix, `Priority.Last`;
- action: late re-resolve/reassert identity and all four pools after generation/prediction hooks complete;
- forbidden alternative: use this as retroactive cleanup of already-created enemies.

### `RoundManager.AssignRandomEnemyToVent(EnemyVent,float)`

- patch pair: Prefix `Priority.First` + Postfix `Priority.Last` (with fail-safe restoration/finalizer if implementation requires it);
- prefix action: reassert the indoor pool; snapshot `currentLevel.specialEnemyRarity`; if that special override is absent or non-ShyGuy, temporarily neutralize only that override for the duration of the assignment transaction;
- postfix/finalizer action: restore the exact prior special-override reference;
- reason: exact V81 source proves special override participates inside the same stateful assignment transaction. This preserves native power/vent/diversity/count bookkeeping and permits SpawnCycleFixes' group-spawn postfix to fan out only an already-allowed identity;
- ordering: project Prefix must precede SpawnCycleFixes default-priority Harmony prefix; restoration must occur after SpawnCycleFixes postfix. DawnLib's temporary `spawningDisabled` ownership is not taken over or persisted by DIAG1;
- forbidden alternative: return false/skip the full method, permanently mutate `spawningDisabled`, or reorder occupied vent state after assignment.

## Exact package-owner guard set

The implementation should use reflection/Harmony only after validating exact declaring type, declared method, parameter types and return type. Transpilers must assert the exact expected callsite count and fail closed if it differs.

### FacelessStalker 1.2.1

- target: `SlendermanMod.Behaviours.SpawnSlendermanEnemyItem.SpawnSlenderman()`;
- patch: Prefix `Priority.First`, skip while DIAG1 active;
- rationale: preserves `PhysicsProp.EquipItem()` and the page item lifecycle while preventing the page's exact spawn request before its ServerRpc. The caller may mark the page used, but no EnemyAI/network object is created.

### Football 1.1.14

- target: `Kittenji.FootballEntity.TrainProp.ForceSpawnEnemy()`;
- patch: Prefix `Priority.First`, skip;
- rationale: dedicated enemy transaction; prevents the one-per-round `wasSpawnedThisRound` mutation from being committed for a denied enemy while leaving normal item grab/base behavior outside this helper intact.

### Herobrine 1.3.9

- target: `Kittenji.HerobrineMod.RedstoneTorchProp.ForceSpawnEnemy()`;
- patch: Prefix `Priority.First`, skip;
- target: `Kittenji.HerobrineMod.Networking.HerobrineNetworking.cmd_Spawn(string)`;
- patch: Prefix `Priority.First`, skip;
- rationale: first target closes the gameplay torch route before its round flag; second closes the separate developer command without touching unrelated Herobrine lifecycle.

### Lategame Upgrades 3.14.1

- target: `MoreShipUpgrades.Misc.Util.Tools.SpawnMob(string,Vector3,int)` returning `bool`;
- patch: Prefix `Priority.First`;
- behavior: resolve the requested `mob` against the exact current indoor enemy table. Allow original only if it resolves to the exact Shy Guy identity. For a denied/non-resolved identity set `__result = true` and skip original;
- reason: `false` has semantic meaning to the Exorcism caller (it triggers Crawler fallback), so a blocked request must not report `false`.

### JLL 1.10.1

- target: `JLL.Components.EnemySpawner.SpawnEnemy(Vector3)`;
- patch: exact transpiler/branch guard;
- insertion point: after the method resolves local `EnemyType enemyType` from fixed/random configuration and before cap/power/nest/spawn work;
- behavior: return from this `void` method when `enemyType` is not exact Shy Guy;
- reason: this is the earliest point with exact identity and it precedes missing-nest creation, power/cap work and `SpawnedEvent` postconditions;
- validation: transpiler must match exactly one resolved-enemy decision region and one downstream `SpawnEnemyGameObject` call.

### KenjiLib 0.7.0

- targets:
  - `KenjiLib.Scripts.KLightsEvent.PermanentPowerOffRoutine()`;
  - `KenjiLib.Scripts.KLightsEvent.TriggerAppyEventRoutine()`;
- patch: exact transpilers replacing only their single ignored-result `RoundManager.SpawnEnemyGameObject` call with the DIAG1 allowed-identity helper;
- expected matches: exactly one call in each method;
- reason: both methods own unrelated light/power/JLL-event state before/after the spawn. Their whole coroutine must not be suppressed.

### itolib 0.9.3

- targets:
  - `itolib.Behaviours.Grabbables.EventfulApparatus.HandleDisconnect()`;
  - `itolib.PlayZone.TwinApparatus.HandleDisconnect()`;
- patch: exact transpilers replacing only the ignored-result Old Bird `SpawnEnemyGameObject` call;
- expected matches: exactly one call per method;
- reason: apparatus audio, disconnect events, power, dungeon/level events and radiation state must remain intact.

### PremiumScraps 2.5.0

- target: `PremiumScraps.Utils.Effects.Spawn(SpawnableEnemyWithRarity,Vector3,float)` returning `NetworkObjectReference`;
- patch: Prefix `Priority.First`; if the requested `enemy.enemyType` is not exact Shy Guy, set default result and skip original;
- exact-callsite condition: the reviewed PremiumScraps assembly's enemy callers ignore this helper's return value. Implementation/static gate must re-prove that invariant in the exact DLL/source before enabling this prefix;
- target: `PremiumScraps.Utils.Effects.SpawnMaskedOfPlayer(ulong,Vector3)`;
- patch: Prefix `Priority.First`, skip because its fixed Masked identity cannot be Shy Guy;
- target: `PremiumScraps.CustomEffects.HarryDoll.SpawnEnemyServerRpc(Vector3,bool,bool)`;
- patch: Prefix `Priority.First`, skip the dedicated enemy RPC transaction;
- reason: this closes both direct-prefab and central-Masked families without patching common network spawn or unrelated scrap/item helpers.

### ChillaxScraps 1.6.6

- target: `ChillaxScraps.Utils.Effects.Spawn(SpawnableEnemyWithRarity,Vector3,float)` returning `NetworkObjectReference`;
- patch: Prefix `Priority.First`; denied non-ShyGuy requests return default. Static validation must prove every non-Ocarina enemy caller that can reach this helper ignores the result;
- target: `ChillaxScraps.CustomEffects.Ocarina.SpawnSpecialEnemyServerRpc(int,Vector3,ulong)`;
- patch: Prefix `Priority.First`, skip the whole dedicated enemy-dispatch RPC while DIAG1 is active;
- reason: Ocarina branches consume returned references for client synchronization, so they are stopped at the owner RPC rather than receiving a fabricated/invalid enemy reference. Other helper callers may use the safe ignored-return guard. `SpawnMaskedOfPlayer` is covered by the Ocarina owner route in the exact reviewed source.

### CodeRebirth 1.6.9

Use six exact owner targets. Do not patch the three EnemyAI child-owner paths (`CutieFlyAI.HandleSpawningMonarch`, `Monarch.OnNetworkSpawn`, `Puppeteer.SwitchToStateAfterDelay`) because they are reachable only after a non-ShyGuy parent EnemyAI already exists; parent prevention plus generic explicit-owner guards make them unreachable in a valid DIAG1 round.

1. `CodeRebirth.src.MiscScripts.EnemyLevelSpawner.SpawnRandomEnemy()` returning `EnemyAI`
   - exact transpiler guard after weighted `EnemyType val` selection and before `entitiesSpawned`, pipe counters, spawn and returned-object dereference;
   - if non-ShyGuy: return `null` before any counters mutate.

2. `CodeRebirth.src.Content.Weathers.TornadoWeather.SpawnTornado(Vector3)`
   - Prefix `Priority.First`, skip; fixed Tornado identity and dedicated spawn helper.

3. `CodeRebirth.src.Content.Items.FakeSnailCat.Update()`
   - exact transpiler guard inside only the server conversion branch, before `destroyed = true`;
   - if the fixed RealEnemySnailCat identity is non-ShyGuy, branch around the conversion block while preserving `GrabbableObject.Update()` and the rest of the item lifecycle.

4. `CodeRebirth.src.Content.Items.GuardPhone.SpawnWithDelay(Vector3)`
   - Prefix returning an empty iterator / equivalent exact wrapper skip; this iterator's reviewed responsibility is delayed fixed Guardsman creation. Do not patch a generated `MoveNext` by guessed name.

5. `CodeRebirth.src.Content.Items.Xui.OnNetworkDespawn()`
   - exact transpiler replaces only its two ignored-result fixed Masked `SpawnEnemyGameObject` calls with the allowed-identity helper;
   - preserve the separate dead-player revival/teleport responsibilities of `OnNetworkDespawn`.

6. `CodeRebirth.src.Content.Enemies.BoxChute.SpawnEnemy()`
   - Prefix `Priority.First`, skip; dedicated fixed DebtCollector creation method.

### LethalMinNightly 1.1.108

Do not patch shared `PikminManager.SpawnPikminOnServer`, global Pikmin/EnemyAI lifecycle, or `NetworkObject.Spawn`. Autonomous generation is zeroed by config. The exact source/callsite inventory shows no external installed-set caller of the shared Pikmin creation API; remaining persistence/item/manual routes are closed before destructive state.

1. `LethalMin.Onion.WithdrawPikminFromOnion(List<PikminType>,int[],Leader)`
   - Prefix replaces returned iterator with an empty iterator;
   - prevents reaching `SpawnPikmin(PikminData,...)`, which otherwise removes stored Onion data before creating the field Pikmin;
   - depositing Pikmin into the Onion is a separate path and remains untouched.

2. `LethalMin.Onion.SetEnemyToBeRevived(EnemyGrabbableObject)`
   - Prefix `Priority.First`, skip;
   - prevents the revival transaction before `PikUtils.ReviveEnemy` despawns the original enemy and before the caller dereferences the replacement.

3. `LethalMin.GlowSeed.SpawnGlowPikminServerRpc(ulong)`
   - Prefix `Priority.First`, skip;
   - stops before the ClientRpc performs seed visual/consumption/despawn state and calls Pikmin creation.

4. `LethalMin.Lumiknull.DepositeItem(float,Leader)`
   - Prefix `Priority.First`, skip only its `DoGlowSpawn` launch.

5. `LethalMin.Triknull.DepositeItem(float,Leader)`
   - Prefix `Priority.First`, skip only its `DoGlowSpawn` launch.

6. `LethalMin.Sprout.PluckAndDespawnServerRpc(ulong)`
   - Prefix `Priority.First`, skip;
   - exact body otherwise creates Pikmin and immediately starts the client despawn routine.

7. `LethalMin.Sprout.OnInteractEarlyOnOtherClients(PlayerControllerB)`
   - Prefix `Priority.First`, skip;
   - prevents the alternate animated `PluckRoutine` from starting; that routine otherwise creates Pikmin and then despawns the Sprout. Do not patch compiler-generated coroutine `MoveNext`.

8. `LethalMin.Compats.EndlessElevatorPatch.WaitRespawnPikmin(EndlessElevator)`
   - Prefix replaces returned iterator with an empty iterator;
   - preserves saved Pikmin data instead of iterating it through `SpawnPikminOnServer` and then clearing `PikminSaved`.

Parent/prevention closure: with autonomous spawning zeroed and the eight owner entries above blocked, `PikminAI.TransformIntoPuffminServerRpc`, `PuffminAI.TransformIntoPikminServerRpc`, shared manager spawn overloads, Sprout's lower spawn RPC/helper and other child conversions are unreachable in a valid fresh DIAG1 round. A startup/round assertion below detects any pre-existing non-ShyGuy EnemyAI instead of silently deleting it.

## Rows intentionally requiring no hook

- Scopophobia Shy Guy painting: exact Shy Guy owner, allowed by identity; its appearance is not positive BCMER-event proof.
- BCMER non-ShyGuy event owners: config/execution-consumer gate, not Harmony suppression.
- `SpawnRandomOutsideEnemy`, `SpawnRandomDaytimeEnemy`, `SpawnRandomWeedEnemy`: covered by pool quarantine.
- `SpawnEnemyFromVent`: covered by allowed-only vent queue; native completion remains intact.
- Haunted Harpist escort, CodeRebirth CutieFly/Monarch/Puppeteer child spawns, Biodiversity MicBird/Ogopogo/Vermin child spawns and LethalMin Pikmin/Puffmin child conversions: parent/prevention closure; do not duplicate child guards.
- SnowyLib spawn APIs and InteractiveTerminalAPI `Tools.SpawnMob`: exact installed-set review found no external consumers; keep as static build assertions.
- MoreCompany debug spawn: exact assembly has no internal `commandEnabled` assignment; assert false at runtime/startup.
- Bozoros Puffer/Butler EmergencyDice routes: provider GUID was not present in the exact installed package set; assert provider absence at startup. If present, DIAG1 is invalid rather than silently widening patches.
- Mirage spawn control: exact S1.42AI config has its Masked spawn-control owner disabled; assert it remains false.

## Runtime observability / fail-closed assertions

DIAG1 must emit stable startup markers for:

- diagnostic mode enabled;
- exact Shy Guy identity triple resolved;
- each config overlay verified;
- every exact Harmony target/signature installed;
- every transpiler expected match count satisfied;
- MoreCompany command disabled;
- SnowyLib Testing disabled/no-consumer evidence version anchored;
- InteractiveTerminal no-consumer evidence version anchored;
- EmergencyDice provider absent;
- old S139 diagnostic isolation disabled / no legacy Thumper-Puffer-Baboon-Pikmin allowlist active.

At round setup, perform one bounded assertion over already-live `EnemyAI` instances. If any live non-ShyGuy EnemyAI exists, log `DIAG1_ISOLATION_BYPASS` with exact type/EnemyType and mark the diagnostic failed. Do not despawn, kill, hide, relocate, or otherwise repair the enemy. Repeat the assertion at a small number of lifecycle checkpoints only; no per-frame global scan is allowed.

Every prevented owner should log a rate-limited owner-specific marker so the runtime log proves which prevention layer actually fired. Shy Guy spawns must never be suppressed solely for being exterior.

## Static implementation gate

Before a DIAG1 build is authorized, repository-native validation must prove:

1. every target above resolves as an exact declared method with expected signature/return type;
2. every transpiler matches the exact expected callsite count and no fallback target is installed;
3. PremiumScraps ignored-return invariant and Chillax non-Ocarina ignored-return invariant remain true for the exact profile DLLs;
4. all config overlay deltas are exactly the documented diagnostic keys plus the existing BCMER DIAG1 keys;
5. S139CompatibilityFixes embedded DLL remains byte-identical to S1.42AI;
6. no package version changes;
7. no broad shared sink or lifecycle patch exists in the diagnostic plugin;
8. the plugin is default-off outside the DIAG1 profile;
9. generated profile contains the exact new diagnostic DLL and recorded SHA-256;
10. archive diff against S1.42AI contains only diagnostic identity metadata, the approved config overlay and the new diagnostic plugin artifacts;
11. startup markers above are present in the source/static contract and old forbidden diagnostic markers are absent.

Passing this gate authorizes only a runtime diagnostic build, not S1.42AI acceptance.

## Result

The callsite-completeness problem and guard-reduction problem are both closed for the exact S1.42AI static stack. The next bounded project action may implement this contract on a clean work branch and run static/build validation. No gameplay test, controller transition or candidate acceptance is authorized by this analysis record itself.
