# S1.42AI-DIAG1 Tier-G exact spawn-owner review

**Status:** EXACT REVIEW COMPLETE / DISCOVERY-POSITIVE INVENTORY EXHAUSTED / PATCH SAFETY PARTIAL / NOT BUILD READY  
**Scope:** all seven remaining discovery-positive packages after canonical Tier-F; eight managed DLLs because CullFactory contains a second managed assembly  
**Canonical main used for review:** `a3844ed8f708b0c5834ba1792ac331b3bc3c8d84`  
**Discovery authority:** `SourceEvidence/NativeSpawnOwners/20260912T163027Z-RemainingEnabledDiscovery/VERIFICATION.json`  
**Exact-review run:** `34714900794`  
**Exact-review head:** `cc00992cf7db111d0ee8e6d605903867f3d826c1`  
**Artifact:** `10304018023` / `s142ai-tier-g-spawn-candidates-exact`  
**Artifact digest:** `sha256:179f35e60d4020ad6033320bab93c8e6d6f440e248e19c06984ca49ff8f49d65`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Purpose and selection

After Tier-F, exactly seven discovery-positive packages remained. All seven were in the same weakest configured discovery class, `enemy_context_instantiate`; there was no stronger remaining signature class that justified another priority split. Tier-G therefore reviews the entire bounded remainder as one final discovery-positive tranche:

- `XuXiaolan-ImmersiveScrap 1.4.2`;
- `FlipMods-TooManyEmotes 2.3.17`;
- `BunyaPineTree-ModelReplacementAPI 2.4.20`;
- `mattymatty-LobbyControl 2.5.12`;
- `darmuh-darmuhsTerminalStuff 3.10.2`;
- `Beaniebe-Beanie_Lib 1.0.9`;
- `fumiko-CullFactory 2.0.7`.

CullFactory ships two managed DLLs. `CullFactory.dll` was the discovery-positive assembly; `CullFactoryBurstPlugin.dll` was additionally reviewed so the package boundary is complete rather than silently treating its second managed assembly as irrelevant.

## Provenance and method

The repository-native workflow re-downloaded the exact package versions and required the exact package ZIP and DLL SHA-256 values. For all seven discovery-positive DLLs it also reproduced both the discovery IL SHA and the prior complete-source SHA with pinned ILSpy. CullFactory's secondary managed DLL was exact ZIP/DLL/IL gated and then fully decompiled to C# and IL.

Successful Actions run `34714900794` produced artifact `10304018023`, whose GitHub artifact digest is `sha256:179f35e60d4020ad6033320bab93c8e6d6f440e248e19c06984ca49ff8f49d65`. The artifact ZIP was independently downloaded and recomputed to the same SHA-256. Every preserved C# and IL file recomputed to the SHA values recorded by the run.

Across all eight reviewed assemblies:

- `EnemyType` occurrences: **0**;
- `enemyPrefab` occurrences: **0**;
- `SpawnEnemyOnServer` occurrences: **0**;
- `SpawnEnemyGameObject` occurrences: **0**;
- confirmed direct `NetworkObject.Spawn` enemy-creation routes: **0**;
- confirmed direct EnemyAI-instance creation sites: **0**.

## Package findings

### XuXiaolan-ImmersiveScrap 1.4.2

Classification: `DOWNSTREAM_EXISTING_ENEMY_TELEPORT_HIT_AND_EXPLOSION_EFFECT_NOT_CREATOR`

`TeleportEnemy(EnemyAI, Vector3)` mutates position/serverPosition on an already-existing enemy. Enemy-hit handling resolves an existing `EnemyAICollisionDetect` and calls `HitEnemyOnLocalClient`. The sole exact `Object.Instantiate` site creates `StartOfRound.Instance.explosionPrefab`. No enemy definition, registration or creation primitive exists in this assembly.

### FlipMods-TooManyEmotes 2.3.17

Classification: `DOWNSTREAM_MASKED_EMOTE_RPC_VISUAL_AND_UI_INFRASTRUCTURE_NOT_CREATOR`

The assembly patches `MaskedPlayerEnemy.Start`/`Update` and existing EnemyAI mesh behavior, attaching `EmoteControllerMaskedEnemy` to already-created masked enemies and synchronizing emote state through named network messages. Its thirteen `Instantiate` sites create skeleton, preview-player/boombox, radial-menu/UI/loadout and emote-prop objects. None creates an EnemyAI instance.

Patch-safety implication: Masked lifecycle/network surfaces have active downstream responsibilities and are not valid blanket DIAG1 suppression points.

### BunyaPineTree-ModelReplacementAPI 2.4.20

Classification: `DOWNSTREAM_PLAYER_MASKED_MODEL_REPLACEMENT_AND_ENEMY_HIT_OBSERVER_NOT_CREATOR`

The assembly patches `EnemyAI.HitEnemy` and `MaskedPlayerEnemy.Start`, attaches `MaskedReplacementBase` to an already-created masked enemy and builds replacement-model/avatar state. Its nine `Instantiate` sites clone replacement models, meshes, view/ragdoll/avatar-support objects. There is no enemy creation primitive.

### mattymatty-LobbyControl 2.5.12

Classification: `LOBBY_NETWORK_CONTROL_AND_DEAD_ENEMY_AI_GUARD_NOT_CREATOR`

LobbyControl patches `EnemyAI.SetDestinationToPosition` and `DoAIInterval` under its log-spam/path guard so dead existing enemies stop unnecessary path work. Its NetworkObject references belong to lobby/network ownership and cleanup infrastructure. The sole `Instantiate` site creates a menu popup.

Patch-safety implication: EnemyAI movement/interval methods carry downstream compatibility responsibilities and must not be treated as spawn-only surfaces.

### darmuh-darmuhsTerminalStuff 3.10.2

Classification: `DOWNSTREAM_BIOSCAN_AND_TERMINAL_UI_OVER_EXISTING_SPAWNEDENEMIES_NOT_CREATOR`

The bioscan reads `RoundManager.Instance.SpawnedEnemies` and filters existing living EnemyAI instances. Its sole `Instantiate` site clones a terminal `RawImage` for miniscreen/camera UI. No enemy creation path exists.

Patch-safety implication: `RoundManager.SpawnedEnemies` is again confirmed as shared downstream bookkeeping/consumer state rather than a safe blanket denial surface.

### Beaniebe-Beanie_Lib 1.0.9

Classification: `GENERIC_UNCALLED_GAMEOBJECT_LAUNCH_HELPER_PLUS_DOWNSTREAM_ENEMY_INTERACTION_NOT_CONFIRMED_CREATOR`

`RigidbodyLauncher.LaunchObject(GameObject LaunchPrefab)` generically calls `Object.Instantiate<GameObject>(LaunchPrefab)`. The complete exact assembly contains only the method declaration and **no internal caller**. Its enemy-related code handles already-existing EnemyAI item-grab/collision/shotgun interaction state. There is no `EnemyType`, `enemyPrefab`, `NetworkObject.Spawn`, `SpawnEnemyOnServer` or `SpawnEnemyGameObject` evidence connecting this generic helper to enemy creation.

This is deliberately classified as **not a confirmed creator**, not as proof that no external consumer could ever pass an enemy prefab to a public/generic API. The present discovery-positive obligation is nevertheless exhausted because the exact assembly itself provides no enemy-specific ownership path.

### fumiko-CullFactory 2.0.7

Reviewed assemblies:

- `CullFactory.dll`;
- `CullFactoryBurstPlugin.dll`.

Classification: `DOWNSTREAM_DYNAMIC_CULLING_ENEMY_TELEPORT_ITEM_TRACKING_AND_BURST_GEOMETRY_NOT_CREATOR`

`CullFactory.dll` postfixes `EnemyAI.SetEnemyOutside` and updates dynamic culling state for already-existing enemies and items held by enemies. Its two `Instantiate` sites create portal and tile-bounds visualizers. `CullFactoryBurstPlugin.dll` is Burst/geometry infrastructure and has zero EnemyAI, EnemyType, Instantiate or NetworkObject occurrences. Neither assembly creates enemies.

## Tier-G patch-safety conclusion

Tier-G contains no confirmed direct enemy-instance creator. It closes the final seven-package remainder of the canonical 53-package discovery-positive inventory. After this tranche, the number of still-unreviewed discovery-positive packages is **0**.

This does **not** make DIAG1 build-ready. It narrows the remaining work to previously identified non-inventory gates:

1. trace SnowyLib cross-assembly consumers of its generic spawn APIs;
2. trace cross-assembly consumers of `InteractiveTerminalAPI.Tools.SpawnMob`;
3. close BCMER forced / forced-side / additional / runtime-custom event execution coverage;
4. preserve/verify Shy Guy runtime identity and project source-to-DLL provenance required by the final design;
5. select and statically validate the smallest host/client-safe interception points.

The accumulated exact reviews also continue to prohibit broad suppression of `EnemyAI.Start`, Masked lifecycle, EnemyAI movement/interval methods, `RoundManager.SpawnedEnemies`, shared `NetworkObject.Spawn`, generic `Object.Instantiate`, or other shared lifecycle/bookkeeping surfaces.

`S1.42AI-DIAG1` remains **NOT_BUILT / NOT_BUILD_READY**. No profile, controller, runtime attribution, Gale state or gameplay authorization changes are made by this review.
