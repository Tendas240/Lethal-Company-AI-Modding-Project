# S1.42AI-DIAG1 exact NestFix / SpawnCycleFixes patch-safety review

**Status:** EXACT_TWO_PACKAGE_REVIEW_COMPLETE / PATCH_SAFETY_STILL_OPEN / NOT_BUILT  
**Date:** 2026-09-11  
**Canonical plan:** `BuildSpecs/S1.42AI_PLAN.md`  
**Patch-safety authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Evidence and provenance

Actions run `34614454120` captured complete C# decompiles and IL for the exact already-reviewed package bytes:

- PureFPSZac-NestFix 1.3.0, package ZIP SHA-256 `a9cf704b463fab1cc988f6872ba4faa641ac9eb6dae52372fa13d61b80a28a4c`, `NestFix.dll` SHA-256 `0a4072618c2a089283933b8aeebe4962c4e45d465518760c90b4c18eb2b70f20`;
- ButteryStancakes-SpawnCycleFixes 1.2.2, package ZIP SHA-256 `ccc66892f996890c9a24dbe430d394262911ad576d2dd797d5535daf196e1c2f`, `SpawnCycleFixes.dll` SHA-256 `aa41f4bb8a8e2dedd75f7987d85c0e0a6792d92bd1fecbffa278f5f4dc9c52a0`.

ILSpy is pinned to 11.0.0.9375. Both complete C# hashes exactly reproduce the hashes recorded by the prior merged discovery, proving that this review is against the same DLLs rather than newer package bytes. Artifact `10269567481` ZIP SHA-256 is `875a6860f73d9ec785ea8fd0f848e0a9afb25bbeade1e4961c077e76dfcd51ba`. `VERIFICATION.json` records the complete hash set. The full third-party decompiles remain in the Actions artifact; this repository retains the bounded review and provenance rather than duplicating the whole decompile.

The active S1.42AI SpawnCycleFixes config is also exact and relevant: `Consistent Spawn Times = true`, `Limit Old Birds = true`, `Mask Hornets Power = false`, `Cadaver Growths Subtract = true`.

## NestFix 1.3.0 complete patch behavior

The DLL installs exactly one Harmony target from `NestFix.Plugin`: a prefix on `RoundManager.SpawnNestObjectForOutsideEnemy(EnemyType,System.Random)`. It has no explicit Harmony priority or before/after constraint.

For every enemy type except Unity object name `BaboonHawk`, the prefix returns `true`; the installed V81 method therefore executes unchanged. For `BaboonHawk`, the prefix replaces the original completely. It repeatedly searches `OutsideAINode` positions, applies its own position/physics/NavMesh validation, instantiates `enemyType.nestSpawnPrefab`, network-spawns its child `NetworkObject`, registers the `EnemyAINestSpawnObject` in `RoundManager.enemyNestSpawnObjects`, increments `enemyType.nestsSpawned`, then returns `false` so vanilla does not run. Failure to find a position also returns `false` without creating the nest.

The package version is 1.3.0 while the embedded BepInPlugin/version constants decompile as 1.2.0. The exact package/DLL hashes above are therefore the provenance authority; the embedded version string is not used to identify the reviewed bytes.

### Isolation consequence

`SpawnNestObjectForOutsideEnemy` is infrastructure creation plus bookkeeping, not a generic EnemyAI spawn. A DIAG1 patch must not globally suppress it merely to obtain an empty non-Shy-Guy round. Competing with NestFix on the same method using another default-priority prefix would also leave prefix ordering dependent on Harmony installation order. Prefer to preserve this method and intercept actual non-allowlisted enemy creation at reviewed owner paths. The still-unreviewed `EnemyAINestSpawnObject` downstream lifecycle remains a separate gap because a nest may later own enemy creation.

## SpawnCycleFixes 1.2.2 complete patch behavior

The exact `SpawnCycleFixes.Patches` type contains 15 Harmony patch methods. Except for `EnemyAI.SubtractFromPowerLevel`, the relevant RoundManager patches have no explicit Harmony priority/before/after constraint.

| Exact target | Patch | Installed responsibility / isolation consequence |
| --- | --- | --- |
| `LungProp.DisconnectFromMachinery` | transpiler | After its `RoundManager.SpawnEnemyGameObject` call, injects `Utilities.UpdateEnemySpawnVariables(radMechEnemyType)`. With active `Limit Old Birds = true`, a central DIAG1 denial inside `SpawnEnemyGameObject` would still be followed by SpawnCycleFixes power/count bookkeeping unless the caller contract is handled. Central spawn denial alone is therefore unsafe for this path. |
| `RoundManager.AssignRandomEnemyToVent` | transpiler | Replaces `currentHour` reads with `timeScript.hour` when consistent times are enabled. |
| `RoundManager.SpawnRandomOutsideEnemy` | transpiler | Injects probability post-processing. It can zero a nest-requiring enemy when no matching nest exists and natural outside power is already full. This changes the effective selection list before vanilla's direct outside creation. |
| `EnemyAI.SubtractFromPowerLevel` | prefix priority 800 + postfix priority 0 | Captures pre-subtraction power state and conditionally compensates Butler/Mask-Hornet power. Current `Mask Hornets Power = false`, so compensation is inactive, but the patch confirms that ordinary EnemyAI death/despawn power ownership must remain intact. |
| `RoundManager.BeginEnemySpawning` | prefix, `HarmonyWrapSafe` | With `Consistent Spawn Times = true`, server-side code advances the spawn timer, applies eclipse/challenge/streak state, then immediately calls `SpawnDaytimeEnemiesOutside`, `SpawnEnemiesOutside` and `SpawnWeedEnemies` before vanilla `BeginEnemySpawning` continues. DIAG1 must therefore be effective before this prefix runs. |
| `RoundManager.AssignRandomEnemyToVent` | prefix | If the supplied vent is already occupied, chooses another empty vent or cancels with `__result=false`; otherwise vanilla continues. |
| `RoundManager.AssignRandomEnemyToVent` | postfix | On a successful assignment, implements `spawnInGroupsOf`: directly occupies additional vents with the same `EnemyType`, copies `enemyTypeIndex`, reserves inside power, increments `numberSpawned`, adds/sorts spawn times and may sync vent time immediately. A single disallowed vent assignment can therefore fan out into multiple queued disallowed enemies. |
| `RoundManager.PlotOutEnemiesForNextHour` | postfix | Rebuilds `enemySpawnTimes` from occupied vents and resets `currentEnemySpawnIndex` when non-empty. Skipping the whole plotting lifecycle would lose required scheduling state. |
| `RoundManager.PredictAllOutsideEnemies` | prefix | With `Consistent Spawn Times = true`, server code completely replaces vanilla prediction and returns `false`; clients also return `false`. It clears/rebuilds nest state, resets/updates outside `EnemyType` counters, predicts weighted outside species, calls `SpawnNestObjectForOutsideEnemy`, then synchronizes nest order. |
| `RoundManager.PlotOutEnemiesForNextHour` | transpiler | Corrects time-of-day reads and switches two random sources to `IndoorEnemySpawnPlacementRandom`. |
| `RoundManager.SpawnEnemiesOutside` | transpiler | Corrects current-hour reads; the underlying V81 outside selection/creation remains the direct-spawn owner. |
| `RoundManager.SpawnDaytimeEnemiesOutside` | transpiler | Corrects current-hour reads; the underlying V81 daytime selection/creation remains the direct-spawn owner. |
| `RoundManager.SpawnWeedEnemies` | transpiler | Corrects current-hour reads; the independent weed pool remains active. |
| `CadaverGrowthAI.RemoveWeedFromTile` | postfix | With active `Cadaver Growths Subtract = true`, calls native `SubtractFromPowerLevel` once all growth tiles are eradicated. Broad EnemyAI/power lifecycle suppression would break this responsibility. |

## Exact installed ordering and interactions

### Generation / outside prediction

Installed V81 `FinishGeneratingNewLevelClientRpc` calls `PredictAllOutsideEnemies` before returning. The existing project diagnostic installs its `PredictAllOutsideEnemies` prefix at `Priority.First`; SpawnCycleFixes' predictor prefix has default priority. Therefore the project prefix executes first, then SpawnCycleFixes sees the resulting pools. With active consistent times, SpawnCycleFixes performs the prediction and returns `false`, so the vanilla predictor is skipped.

Within that SpawnCycleFixes predictor, nest creation calls `RoundManager.SpawnNestObjectForOutsideEnemy`. NestFix then intercepts only `BaboonHawk`; all other enemy types proceed into the installed V81 nest method. SpawnCycleFixes subsequently synchronizes the resulting `enemyNestSpawnObjects` order. This ordering makes a broad DIAG1 skip of prediction or nest creation unsafe.

The existing project's `FinishGeneratingNewLevelClientRpc` diagnostic hook is a `Priority.Last` postfix, so it runs only after the native method and its nested patched prediction have completed. It is useful for late pool reassertion but cannot retroactively prove prevention of prediction-time creation.

### BeginEnemySpawning

The existing project diagnostic uses a `Priority.First` prefix on `BeginEnemySpawning`. SpawnCycleFixes' prefix has default priority and therefore follows it. SpawnCycleFixes then immediately performs its early daytime, outside and weed batches before vanilla `BeginEnemySpawning` continues. Any retained DIAG1 lifecycle pre-filter must stay deterministically before SpawnCycleFixes, but that only constrains list-driven selection; it does not cover explicit/direct spawn owners.

### Vent scheduling

The effective vent path is:

1. SpawnCycleFixes transpiles `PlotOutEnemiesForNextHour`;
2. vanilla plotting computes the schedule and calls `AssignRandomEnemyToVent`;
3. SpawnCycleFixes' vent transpiler changes time reads;
4. SpawnCycleFixes' vent prefix may reassign an occupied vent or cancel;
5. vanilla `AssignRandomEnemyToVent` assigns the selected identity;
6. SpawnCycleFixes' postfix may multiply that identity across additional vents and reserve additional power;
7. after plotting, SpawnCycleFixes' `PlotOutEnemiesForNextHour` postfix rebuilds/sorts `enemySpawnTimes`.

The prior installed-V81 capture did not include the body of `AssignRandomEnemyToVent`, and its review already identified `specialEnemyRarity` as an unresolved override. Because SpawnCycleFixes has both pre- and post-responsibilities on that exact target, DIAG1 must not guess a skip contract there. Capture/review of the exact native assignment body is still required before choosing a vent interception.

### Explicit Old Bird spawn / return-value hazard

SpawnCycleFixes proves a concrete reason that `SpawnEnemyGameObject` cannot simply return a denied/empty result for every non-Shy-Guy caller. `LungProp.DisconnectFromMachinery` is transpiled so its explicit Old Bird spawn is followed by `UpdateEnemySpawnVariables` regardless of any central DIAG1 decision inside the called method. With the active config this updates spawn count and a power bucket. Denial must therefore be caller-aware or occur at a reviewed point where the caller does not subsequently reserve state for an enemy that never existed.

## Patch-safety decision

This segment closes the requested exact NestFix/SpawnCycleFixes body and ordering review. It does **not** make S1.42AI-DIAG1 build-ready.

Approved conclusions for later design:

- Preserve SpawnCycleFixes and NestFix packages and their non-isolation responsibilities.
- If a lifecycle pool-reassertion hook is retained, explicit `Priority.First` ordering before SpawnCycleFixes is required; relying on default Harmony order is not acceptable.
- Do not add a competing default-priority prefix on `SpawnNestObjectForOutsideEnemy` or `AssignRandomEnemyToVent`.
- Do not skip `PredictAllOutsideEnemies`, `BeginEnemySpawning`, `PlotOutEnemiesForNextHour`, or generic EnemyAI lifecycle methods wholesale.
- Do not treat a central `SpawnEnemyGameObject` denial as complete or state-safe without resolving its callers/return-value bookkeeping, specifically the SpawnCycleFixes Old Bird path.
- Preserve unexpected exterior Shy Guy. No location-based Shy Guy suppression or cleanup is justified by this review.

## Remaining exact gaps / next bounded work

Continue with the already-discovered LethalMin/CodeRebirth/Dusk direct-creation, replacement and return-value owners, while closing the specific native `AssignRandomEnemyToVent` / `specialEnemyRarity` body and `EnemyAINestSpawnObject` downstream lifecycle gaps. Preserve the BCMER forced/side-event execution gate. Those are prerequisites to selecting final DIAG1 interception points.

No diagnostic build, controller transition, new source capture from the user, Gale import or gameplay run is authorized by this checkpoint.
