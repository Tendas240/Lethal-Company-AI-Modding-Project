# S1.42AI-DIAG1 Tier-C remaining spawn-owner exact review

**Status:** EXACT_TIER_C_REVIEW_COMPLETE / PATCH_SAFETY_PARTIAL / NOT_BUILD_READY  
**Canonical main reviewed:** `94be00f2ca31cb2caa4d0125e2bebb7573d22a50`  
**Remaining-package discovery:** run `34705334804`, head `45d22c3fa1abb3bbd95dd137cd3903eb053f87c7`  
**Exact-review run:** `34710724733`, head `1e75d80af54bf80daf11ef37f0ef8327fde7d301`, SUCCESS  
**Exact-review artifact:** `10303047183`, `s142ai-tier-c-spawn-candidates-exact`, artifact ZIP digest `sha256:369f15e556017cde234b312c00728ab434c0e286271ed7813d767f3ddeab464e`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope and evidence contract

This review closes the next bounded six-package tranche selected from the 31 discovery-positive packages still unreviewed after Tier-B. Selection prioritized the strongest remaining combined `Instantiate` + network-spawn signature class, then favored packages whose discovery excerpts placed those primitives next to enemy lifecycle, EnemyAI subclasses, or enemy-adjacent infrastructure.

The exact-review workflow re-downloaded the same Thunderstore package versions, failed closed against the prior discovery ZIP SHA-256, DLL SHA-256 and complete-source SHA-256, and preserved complete C# plus IL. The full third-party decompiles remain in the GitHub Actions artifact; this repository stores only hashes, classifications and review conclusions.

This evidence is not a DIAG1 implementation approval. It does not classify the other discovery-positive packages as safe and does not change `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, any profile, candidate identity, or acceptance state.

A shared negative fact across this tranche is significant: all six exact decompiles have zero `EnemyType`, zero `SpawnEnemyOnServer`, zero `SpawnEnemyGameObject`, and their complete object-creation sites were reviewed. Two packages define their own `EnemyAI` subclasses, but neither assembly contains a direct enemy-instance creation primitive. This does not prove that their registered enemy definitions can never be instantiated by native/framework pool logic; it only closes direct spawn ownership inside the reviewed assembly.

## Exact findings

### coderCleric-Poltergeist 1.2.12

Assembly: `BepInEx/plugins/Poltergeist.dll` (`18d5f6c9251972b130decbac01141e467dc3259bc8754b660f6f0180c255e98f`).

`Patches.AddInteractorForEnemies(EnemyAI)` is a postfix on `EnemyAI.Start`/`MaskedPlayerEnemy.Start`. On host/server it instantiates `Poltergeist.enemyInteractibleObject`, attaches it to the already-existing enemy, sets `NetworkedInteractible.intendedParent`, and network-spawns that interactor. Other creation sites produce prop interactors, ghost-head spectator infrastructure, UI/trigger objects and cloned materials.

No source site instantiates an enemy prefab or calls a game/mod enemy spawn API. The enemy reference is an input to downstream interaction infrastructure, not a created object.

Classification: **DOWNSTREAM_ENEMY_LIFECYCLE_INTERACTOR_INFRASTRUCTURE_NOT_CREATOR.** A broad `EnemyAI.Start` skip would remove required Poltergeist setup from allowed enemies and is therefore not an acceptable DIAG1 interception surface.

### Entity378-SellBodiesFixed 1.14.0

Assembly: `BepInEx/plugins/SellBodies/SellBodies.dll` (`3c3e43d8c27e55f9b4289b7f2d047aa1b1624c084c16c22a7f3a172345ad13c0`).

The package patches `EnemyAI.KillEnemy`/`KillEnemyServerRpc`. Its network-spawn creation paths are post/death replacement infrastructure: configured sellable body prefabs, replacement shotgun/mask items, generic modded body prefabs selected by the dead enemy's power level, and cartridge/scrap items. Some branches despawn the original dead enemy network object after replacement body creation.

No reviewed creation site creates a live `EnemyAI`; `EnemyAI` is the already-dying source object whose state determines which body/item is produced.

Classification: **ENEMY_DEATH_BODY_AND_SCRAP_REPLACEMENT_INFRASTRUCTURE_NOT_CREATOR.** Shared `NetworkObject.Spawn` suppression would break corpse/body sale behavior and item replacement while doing nothing owner-specific for enemy isolation.

### 347956-JPOGRaptor 1.0.6

Assembly: `plugins/JPOGRaptor.dll` (`ae2b8c752e229aa5a76083e1c4c641156f3a8294802a7edbebac325b4793b983`).

The assembly defines `JPOGRaptorAI : EnemyAI` and owns the enemy's AI lifecycle after an instance exists. Its sole object-instantiation site is `JPOGRaptorAI.DropLoot()`: it instantiates a selected item's `spawnPrefab`, obtains `GrabbableObject`, network-spawns it and assigns scrap value.

There is no `EnemyType`, `SpawnEnemyGameObject`, `SpawnEnemyOnServer`, or enemy-prefab instantiation in the exact assembly. Therefore this DLL is an enemy implementation/behavior owner but not a direct enemy-instance spawn owner at the reviewed code level. Its enemy definition may still enter game/framework spawn pools outside this direct-creation scope; this review does not claim otherwise.

Classification: **CUSTOM_ENEMY_IMPLEMENTATION_WITH_SCRAP_DROP_NO_DIRECT_ENEMY_CREATION_PRIMITIVE.** DIAG1 must preserve the allowed enemy's normal `EnemyAI` lifecycle rather than suppressing it globally.

### ScienceBird-ScienceBird_Tweaks 4.7.5

Assembly: `ScienceBird.ScienceBirdTweaks.dll` (`ab9d87a037b090b3f80afbbaebd409254a024b81442d0280a9164a7811324059`).

The full assembly contains many Harmony patches around existing enemies plus numerous object-creation sites. Exact review resolves those sites as gameplay/support infrastructure: a network handler; big-door/player-death effects; mask and shell scrap; item replacement; furniture/panel/teleport/late-client-sync/cassette interaction helpers; quicksand/effect/render duplicates and related support objects. Network-spawned helper prefabs are not live enemy prefabs.

No reviewed creation site uses `EnemyType` or a direct enemy spawn API. Enemy classes are patched/observed, not instantiated by this assembly.

Classification: **DOWNSTREAM_ENEMY_PATCH_AND_NETWORKED_GAMEPLAY_INFRASTRUCTURE_NOT_CREATOR.** The volume of legitimate networked helpers is additional evidence against global `NetworkObject.Spawn` suppression.

### ShaosilGaming-GeneralImprovements 1.5.5

Assembly: `GeneralImprovements.dll` (`5b7199e2b92b2880e2bf12f5198a4905a63b0a4633f1ad16c1ed43dd981f86c4`).

`EnemyAIPatch` observes `EnemyAI.Start` and `SubtractFromPowerLevel` to maintain aggregate danger/power display state. Object creation is ship/UI/support infrastructure: monitor clones, placeable Med Station and Charge Station network objects, HUD/radar icons and teleport particles. Its reflection lookup for `Object.Instantiate<GameObject>` belongs to a `StartOfRound.LoadShipGrabbableItems` transpiler that preserves saved item rotations; it is not an arbitrary enemy creator.

No exact source path creates a live enemy or consumes `EnemyType` for creation.

Classification: **DOWNSTREAM_ENEMY_POWER_OBSERVER_AND_SHIP_INFRASTRUCTURE_NOT_CREATOR.** Broad `EnemyAI.Start` suppression would corrupt its danger-level bookkeeping for allowed enemies.

### HQ_Team-LethalThingsReloaded 0.11.7

Assembly: `plugins/LethalThings.dll` (`1f1923b2f104fc5b90774ef4369fa7c46f70c13159110096550fa61bf56dec62`).

The assembly defines custom enemies including `FishFriend : EnemyAI` and `RoombaAI : EnemyAI`, but its complete `Instantiate` sites create explosion/effect particles, darts/projectiles, dart items, dropped crystal-core scrap, ping/UI markers and missiles. Network ownership/spawn operations belong to those projectiles/items/support objects.

There is no `EnemyType`, `SpawnEnemyGameObject`, `SpawnEnemyOnServer`, or enemy-prefab instantiation in this exact assembly. As with JPOGRaptor, this proves only that the reviewed DLL is not a direct enemy-instance creation owner; it does not deny that its enemy definitions can be registered and instantiated by native/framework spawn systems.

Classification: **CUSTOM_ENEMY_IMPLEMENTATIONS_WITH_ITEM_PROJECTILE_INFRASTRUCTURE_NO_DIRECT_ENEMY_CREATION_PRIMITIVE.** Global lifecycle/network suppression would damage unrelated LethalThings gameplay systems.

## Cross-package conclusions for DIAG1

1. None of the six assemblies is a direct enemy-instance spawn owner in its exact complete source. The discovery signatures were caused by downstream enemy lifecycle or non-enemy networked object creation.
2. `JPOGRaptor` and `LethalThingsReloaded` remain relevant because they define custom `EnemyAI` implementations; their instances can still be introduced through external/native/framework pool ownership even though these DLLs contain no direct creation primitive.
3. `Poltergeist` and `GeneralImprovements` concretely depend on `EnemyAI.Start`-time behavior after an enemy already exists. Suppressing that shared lifecycle would break downstream responsibilities for any allowed Shy Guy or other unavoidable infrastructure.
4. `SellBodiesFixed`, `ScienceBird_Tweaks`, `GeneralImprovements`, `Poltergeist` and `LethalThingsReloaded` all demonstrate legitimate non-enemy uses of `NetworkObject.Spawn`/ownership. A global network-spawn deny is therefore architecturally invalid for DIAG1.
5. The future isolation design must continue to distinguish direct creator/owner decisions from downstream observers and non-enemy network infrastructure, consistent with `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

## Remaining scope and build/runtime gate

This exact tranche reduces the still-unreviewed discovery-positive inventory from 31 to **25**. SnowyLib cross-assembly consumers remain an explicit separate gate. Exact BCMER forced/forced-side/additional/runtime-custom execution coverage, Shy Guy runtime/source-to-DLL provenance, and final narrow host/client-safe interception selection remain open.

`S1.42AI-DIAG1` remains **PLANNED_NOT_BUILT / NOT_BUILD_READY**. This review does not authorize a build, controller transition, Gale import, gameplay test, global `NetworkObject.Spawn` interception, broad `EnemyAI` lifecycle suppression, or post-spawn cleanup.