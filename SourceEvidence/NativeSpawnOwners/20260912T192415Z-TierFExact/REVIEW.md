# S1.42AI-DIAG1 Tier-F exact spawn-owner review

**Status:** EXACT REVIEW COMPLETE / PATCH SAFETY PARTIAL / NOT BUILD READY  
**Scope:** next six prioritized discovery-positive packages after canonical Tier-E  
**Canonical main used for review:** `2eac9f13eeadeb37989f397afa0e07d7c03a01fe`  
**Discovery authority:** `SourceEvidence/NativeSpawnOwners/20260912T163027Z-RemainingEnabledDiscovery/VERIFICATION.json`  
**Exact-review run:** `34714066827`  
**Exact-review head:** `acc5d96b1a1b4b2a31d720a2cbce57d7785f0d69`  
**Artifact:** `10304281875` / `s142ai-tier-f-spawn-candidates-exact`  
**Artifact digest:** `sha256:69c00cbbb6b543a6396e96d1a268801203b1ebd3182742260ebf0494de909858`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Purpose and selection

After canonical Tier-E, exactly 13 discovery-positive packages remained unreviewed. All 13 carried only the weaker discovery class `enemy_context_instantiate`, so raw signature count no longer separated the tranche reliably. Selection therefore used the already hash-anchored discovery source context to prioritize actual enemy-definition, EnemyAI-subclass and downstream enemy-lifecycle relevance.

The six selected packages were:

- `zealsprince-Locker 1.6.3` — EnemyAI subclass plus exact EnemyType/enemyPrefab/LethalLib registration ownership;
- `Cabinet_crew-TheCabinet 1.12.1` — EnemyAI subclass plus exact EnemyType/enemyPrefab/LethalLib registration ownership;
- `Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior 3.4.4` — custom `DummyEnemyAI` adapter plus EnemyAI lifecycle tracking;
- `NotezyTeam-EnemyHealthBars 1.4.0` — direct `EnemyAI.Start` downstream UI consumer;
- `DiggC-CruiserImproved 1.6.3` — direct enemy collision/damage compatibility around vehicle logic;
- `Zaggy1024-OpenBodyCams 3.0.12` — direct `EnemyAI.Start`/`OnDestroy` downstream tracking plus networked ship/camera infrastructure.

The remaining seven discovery-positive packages are `XuXiaolan-ImmersiveScrap 1.4.2`, `FlipMods-TooManyEmotes 2.3.17`, `BunyaPineTree-ModelReplacementAPI 2.4.20`, `mattymatty-LobbyControl 2.5.12`, `darmuh-darmuhsTerminalStuff 3.10.2`, `Beaniebe-Beanie_Lib 1.0.9` and `fumiko-CullFactory 2.0.7`.

## Provenance and method

The repository-native workflow re-downloaded the exact Thunderstore package versions and failed closed unless all prior discovery anchors matched. For each reviewed assembly it required:

- exact package ZIP SHA-256;
- exact DLL member path and DLL SHA-256;
- exact discovery IL SHA-256;
- exact complete-source SHA-256 from the prior discovery capture;
- a fresh complete C# and IL decompile with pinned `ilspycmd 11.0.0.9375`.

All six packages and six managed DLLs passed those gates. Complete C#/IL are preserved in the Actions artifact rather than copied into the repository.

Across all six exact-reviewed assemblies:

- `SpawnEnemyOnServer` occurrences: **0**;
- `SpawnEnemyGameObject` occurrences: **0**;
- direct `NetworkObject.Spawn` / `SpawnWithOwnership` / `SpawnAsPlayerObject` call sites: **0**;
- no exact reviewed `Instantiate` site directly creates an EnemyAI prefab instance.

The absence of a direct instance-creation primitive does not make EnemyType registration or downstream lifecycle surfaces safe to suppress. The package-specific responsibility map below remains the patch-safety authority for this tranche.

## Package findings

### zealsprince-Locker 1.6.3

Reviewed assembly:

- `Locker.dll`

Classification:

`ENEMY_DEFINITION_AND_LETHALLIB_REGISTRATION_OWNER_NO_DIRECT_INSTANCE_SPAWN`

`Plugin.Awake()` loads the exact Locker `EnemyType`, registers `val.enemyPrefab` with LethalLib `NetworkPrefabs.RegisterNetworkPrefab`, applies `PowerLevel` and `MaxCount`, and registers the EnemyType into LethalLib level pools through `Enemies.RegisterEnemy`. The assembly also defines `LockerAI : EnemyAI`.

`Assets.SpawnPrefab(string, Vector3)` is a generic helper that can `Object.Instantiate` an entry from the package's internal prefab dictionary, but the complete exact assembly contains no internal caller of that helper. Its other real instantiate site creates `StartOfRound.Instance.explosionPrefab` as an effect.

Patch-safety implication: Locker is a genuine enemy-definition/registration owner even though instance creation is delegated downstream to the registered level/native framework path. Suppressing LethalLib registration wholesale or treating every prefab registration as a spawn call would break legitimate package ownership. The uncalled generic helper is not promoted into an active normal-stack spawn path.

### Cabinet_crew-TheCabinet 1.12.1

Reviewed assembly:

- `plugins/TheCabinet/VectorV.TheCabinet.dll`

Classification:

`ENEMY_DEFINITION_AND_LETHALLIB_REGISTRATION_OWNER_NO_DIRECT_INSTANCE_SPAWN`

`Plugin.Awake()` loads the `TheCabinet` `EnemyType`, registers its `enemyPrefab` as a network prefab and passes the EnemyType plus configured moon rarity maps to `Enemies.RegisterEnemy`. The package defines `TheCabinetAI : EnemyAI`.

The assembly's only `Object.Instantiate<GameObject>` site creates a blood decal effect. It contains no direct EnemyAI instance creation or native explicit enemy-spawn primitive.

Patch-safety implication: like Locker, TheCabinet owns enemy definition and pool registration while later framework/native code owns instance creation. DIAG1 cannot globally disable LethalLib enemy registration as a substitute for narrow spawn prevention.

### Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior 3.4.4

Reviewed assembly:

- `BepInEx/plugins/BlackMesa.dll`

Classification:

`INTERIOR_HAZARD_ENEMYAI_ADAPTER_AND_DOWNSTREAM_LIFECYCLE_TRACKING_NOT_DIRECT_CREATOR`

The assembly declares `DummyEnemyAI : EnemyAI` as an adapter around Black Mesa `IDumbEnemy` hazards. Its `Awake()` initializes only the minimal inherited/network fields required by that adapter and disables the behaviour; `Start()` is empty; damage/stun/kill calls are delegated to the wrapped hazard; `OnDestroy()` removes the adapter from `RoundManager.Instance.SpawnedEnemies`.

Separately, a Harmony postfix on `EnemyAI.Start` adds already-created EnemyAI instances to `PatchEnemyAI.AllEnemies`, and `EnemyAI.OnDestroy` removes them. The two real `Object.Instantiate` sites create the vanilla explosion prefab and `BlackMesaInterior.GenerationRulesPrefab`, not enemy instances.

`PatchNetworkManager.AddNetworkPrefab(GameObject)` can register a supplied prefab with the NetworkManager, but the complete exact assembly contains no internal caller of this helper.

Patch-safety implication: `EnemyAI.Start`, `EnemyAI.OnDestroy` and `RoundManager.SpawnedEnemies` again carry legitimate downstream/interior compatibility responsibilities. Black Mesa's adapter must not be mistaken for an autonomous enemy spawn owner, and a guessed global EnemyAI lifecycle block would damage its hazard compatibility.

### NotezyTeam-EnemyHealthBars 1.4.0

Reviewed assembly:

- `NoteBoxz.EnemyHealthBars.dll`

Classification:

`DOWNSTREAM_ENEMY_START_UI_ATTACHMENT_NOT_CREATOR`

A Harmony postfix on `EnemyAI.Start` receives an already-existing EnemyAI instance. If it is not blacklisted, the patch instantiates `HPBarPrefab` as a child of that existing enemy and stores the EnemyAI reference in the HealthBar component.

There is no EnemyType registration, enemy prefab creation or explicit enemy-spawn primitive in the exact assembly.

Patch-safety implication: `EnemyAI.Start` has a concrete UI responsibility for existing enemies. A blanket DIAG1 prefix that skips `EnemyAI.Start` would silently suppress this package and similar downstream behavior.

### DiggC-CruiserImproved 1.6.3

Reviewed assembly:

- `BepInEx/plugins/CruiserImproved/DiggC.CruiserImproved.dll`

Classification:

`DOWNSTREAM_VEHICLE_ENEMY_COLLISION_AND_DAMAGE_COMPATIBILITY_NOT_CREATOR`

CruiserImproved reads existing `EnemyAICollisionDetect.mainScript`, `EnemyAI.isEnemyDead` and enemy hit methods as part of vehicle collision/damage compatibility. Its two `Object.Instantiate` sites create a replacement cruiser exhaust particle system and a copied cabin-light control transform.

The many `NetworkObject` references belong to synchronization of existing vehicle/network state; there is no `NetworkObject.Spawn` call and no enemy-instance creation path in the exact assembly.

Patch-safety implication: enemy collision/hit surfaces have legitimate neighboring vehicle behavior and are not spawn-only interception points.

### Zaggy1024-OpenBodyCams 3.0.12

Reviewed assembly:

- `OpenBodyCams.dll`

Classification:

`DOWNSTREAM_ENEMY_TRACKING_CAMERA_AND_SHIP_NETWORK_INFRASTRUCTURE_NOT_CREATOR`

OpenBodyCams postfixes `EnemyAI.Start` to add body-camera target trackers to an already-created enemy's NetworkObject transform. Its `EnemyAI.OnDestroy` prefix performs FlowerSnake/Centipede attachment cleanup. Other enemy-specific patches track existing Masked, Centipede and FlowerSnake state.

All exact instantiate sites create camera/night-vision, weather-effect, UI/overlay or related visual objects. Its `NetworkPrefabs.RegisterNetworkPrefab` call registers the optional BodyCam ship-upgrade antenna prefab, not an enemy. There is no direct network spawn call in the exact assembly.

Patch-safety implication: `EnemyAI.Start` and `OnDestroy` are again proven shared downstream lifecycle surfaces, while network-prefab registration also services non-enemy ship infrastructure. Neither surface is valid for blanket enemy isolation.

## Tier-F patch-safety conclusion

This tranche contains **no direct EnemyAI instance creator**. It resolves two packages as genuine enemy-definition/LethalLib-registration owners, one as an EnemyAI adapter plus lifecycle observer, and three as downstream enemy/UI/vehicle/camera consumers.

The tranche therefore strengthens the existing narrow-interception requirements:

- do not globally suppress `EnemyAI.Start` or `EnemyAI.OnDestroy`;
- do not manipulate `RoundManager.SpawnedEnemies` as a generic isolation mechanism;
- do not suppress all LethalLib `Enemies.RegisterEnemy` or `NetworkPrefabs.RegisterNetworkPrefab` calls;
- do not treat generic prefab registration or `Instantiate` presence as proof of active enemy creation;
- preserve non-enemy network, vehicle, UI, camera and interior-hazard responsibilities.

The smallest exact owner/interception rule from `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` remains mandatory.

## Remaining coverage

Canonicalizing this tranche reduces the still-unreviewed discovery-positive inventory from **13 to 7**.

The remaining seven are:

1. `XuXiaolan-ImmersiveScrap 1.4.2`;
2. `FlipMods-TooManyEmotes 2.3.17`;
3. `BunyaPineTree-ModelReplacementAPI 2.4.20`;
4. `mattymatty-LobbyControl 2.5.12`;
5. `darmuh-darmuhsTerminalStuff 3.10.2`;
6. `Beaniebe-Beanie_Lib 1.0.9`;
7. `fumiko-CullFactory 2.0.7`.

Still open independently:

1. exact-review those remaining seven discovery-positive packages;
2. trace SnowyLib cross-assembly consumers;
3. trace `InteractiveTerminalAPI.Tools.SpawnMob` cross-assembly consumers;
4. close BCMER forced / forced-side / additional / runtime-custom event execution coverage;
5. preserve/verify exact Shy Guy runtime identity and project source-to-DLL provenance;
6. select and statically validate the smallest host/client-safe interception points.

`S1.42AI-DIAG1` remains **NOT_BUILT / NOT_BUILD_READY**. No profile, build controller, runtime controller, candidate identity, Gale state or gameplay authorization changes are made by this review.
