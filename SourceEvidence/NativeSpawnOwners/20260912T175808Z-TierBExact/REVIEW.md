# S1.42AI-DIAG1 Tier-B remaining spawn-owner exact review

**Status:** EXACT_TIER_B_REVIEW_COMPLETE / PATCH_SAFETY_PARTIAL / NOT_BUILD_READY  
**Canonical main reviewed:** `a7a6958d9e82ee657aea65a72011eb7e0d44b86b`  
**Successful exact-review run:** `34709775849`, run number `1`, head `70e3cbac7c6255beb6d5dd447448979b8ee90e3c`, SUCCESS  
**Artifact:** `10303095900`, `s142ai-tier-b-spawn-candidates-exact`, ZIP digest `sha256:a5a33c57fec7c9f81d6b97fc335d5c4d6f6c697c175aa778d5d2200ed9014b7c`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope and provenance

This is the next bounded exact-review tranche selected from the still-unreviewed discovery positives in `SourceEvidence/NativeSpawnOwners/20260912T163027Z-RemainingEnabledDiscovery/VERIFICATION.json` after the Tier-A review. The tranche prioritizes the four remaining packages carrying three configured spawn-signature reasons, followed by two packages whose signatures include enemy-spawn lifecycle/detour surfaces:

- `Flowprojects-Mirage_v81 1.29.1`;
- `Alice-DungeonGenerationPlus 1.5.0`;
- `KawaiiBone-Remnants 1.4.4`;
- `LethalMatt-Bozoros 2.9.3`;
- `AntlerShed-EnemySkinRegistry 1.5.1`;
- `ButteryStancakes-EnemySoundFixes 1.9.14`.

The read-only Actions capture re-downloaded the exact Thunderstore versions and failed closed unless each package ZIP SHA-256, selected DLL SHA-256 and complete C# decompile SHA-256 matched the prior discovery evidence. It preserved complete C# and IL from pinned ILSpy `11.0.0.9375`. `VERIFICATION.json` records the exact hashes. Full third-party decompiles remain in the Actions artifact rather than being copied into the repository.

## 1. Mirage_v81 1.29.1 — conditional Masked spawn-pool mutator, not a direct EnemyAI creator

Exact DLL: `Mirage.dll`, SHA-256 `271a4a8a77c1c4317ae146e524bcd91089917a2a0d3720feb92dc42dca5b1e80`.

The source contains a host-side `TimeOfDay.Start` hook in the Masked integration. When `EnableSpawnControl` is true, it clones the Masked `EnemyType`, removes existing Masked entries from every `SelectableLevel.Enemies` list, computes replacement weights and appends the cloned type with the configured `MaxCount`. This is real spawn-pool ownership, but it does not instantiate or network-spawn an EnemyAI itself.

The exact S1.42AI config `BepInEx/config/Mirage.General.cfg` has `Enable spawn control (masked enemies) = false`. The hook therefore returns after the original `TimeOfDay.Start` on the current profile and does not perform that pool rewrite. Other Mirage `Instantiate`/network references in this assembly are not direct enemy creation evidence.

**Classification:** `CONDITIONAL_MASKED_POOL_MUTATOR_DISABLED_BY_EXACT_PROFILE_CONFIG`.

**Patch-safety consequence:** do not patch Mirage lifecycle globally. For the current diagnostic, the relevant spawn-control owner branch is already disabled by exact config; preserve Mirage's unrelated voice, Masked visual/item and networking responsibilities. Re-evaluate this route only if the exact profile config changes.

## 2. DungeonGenerationPlus 1.5.0 — discovery false positive for enemy ownership

Exact DLL: `DunGenPlus.dll`, SHA-256 `9d488d7bb98c87bbdb3967d7f9c6c5cb8ab9b82284467fe1c2dddefed1bc1765`.

The complete decompile has zero `EnemyAI` and zero `EnemyType` occurrences. Its `Instantiate`, `NetworkObject` and Harmony hits belong to dungeon generation, scrap/prop, bounds/debug and networking infrastructure rather than enemy creation or enemy spawn scheduling.

**Classification:** `NOT_ENEMY_SPAWN_OWNER_DISCOVERY_CONTEXT_FALSE_POSITIVE`.

**Patch-safety consequence:** no DIAG1 enemy interception is justified in this package from the reviewed evidence. Preserve its dungeon-generation responsibilities unchanged.

## 3. Remnants 1.4.4 — networked remnant/body/scrap owner, not EnemyAI creator

Exact DLL: `Remnants.dll`, SHA-256 `49d8e65a2bd6d451a552c12ec62d87d112b5cb7930859a8c72b8021e203f7ad5`.

The complete decompile likewise has zero `EnemyAI` and zero `EnemyType` occurrences. Its enemy-context discovery hits come from remnant/body mappings and networked remnant or scrap object handling. The reviewed `Instantiate`/`NetworkObject` paths create those non-EnemyAI objects rather than living enemy prefabs.

**Classification:** `NETWORKED_REMNANT_INFRASTRUCTURE_NOT_ENEMY_SPAWN_OWNER`.

**Patch-safety consequence:** shared `NetworkObject.Spawn` suppression would incorrectly damage this package while providing no justified enemy-isolation benefit. No package-specific enemy interception is indicated.

## 4. Bozoros 2.9.3 — conditional direct enemy-prefab network owner plus ordinary pool configuration

Exact DLL: `BepInEx/plugins/Bozoros.dll`, SHA-256 `87feb32c19c5c9e5fbc42f6af5211baa169239994c6dafed4236545ee3a47265`.

Two Emergency Dice compatibility effects are real direct EnemyAI creation paths:

- `PufferInfestationDiceEffect.SpawnPufferServerRpc` resolves the vanilla `Puffer` EnemyType, directly instantiates its `enemyPrefab`, obtains its `NetworkObject`, network-spawns it and then continues the effect's synchronization path;
- `SantaVisitDiceEffect.SpawnButlerServerRpc` resolves the vanilla `Butler` EnemyType and likewise directly instantiates/network-spawns the enemy before continuing the effect transaction.

These paths bypass `RoundManager.SpawnEnemyGameObject`. Their registration is not unconditional: `LoadPatch.MenuManagerStartPre` calls `EmergencyDiceCompatibility.RegisterDiceEffects()` only when `EmergencyDiceCompatibility.Enabled` and Bozoros' `BOZO_DICE_EFFECTS` setting are true. `EmergencyDiceCompatibility.Enabled` is specifically guarded by `Chainloader.PluginInfos.ContainsKey("Theronguard.EmergencyDice")`. The exact S1.42AI Bozoros config enables the compatibility flag, while the guarded export contains no package identity named for `Theronguard`/`EmergencyDice`; therefore no active provider is identified by the exact package inventory. Do not convert that package-name observation into a universal proof that the plugin GUID can never be supplied under another package identity.

Bozoros also performs ordinary level enemy-pool integration for its moon/content, which is a separate registration/configuration responsibility and not itself proof of direct creation.

**Classification:** `CONDITIONAL_DIRECT_ENEMY_PREFAB_NETWORK_OWNER_PROVIDER_NOT_IDENTIFIED_IN_EXACT_PACKAGE_INVENTORY`.

**Patch-safety consequence:** if the Emergency Dice provider is absent at runtime, these direct paths are dormant and should not be patched. If later evidence proves the provider GUID is loaded, prevention must occur before the direct prefab instantiate for non-allowlisted enemies while preserving the dice/network transaction; a shared network-spawn denial is too late and too broad.

## 5. EnemySkinRegistry 1.5.1 — downstream EnemyAI lifecycle/skin observer, not creator

Exact DLL: `plugins/EnemySkinRegistry/EnemySkinRegistry.dll`, SHA-256 `6b53db95bfc15b7d71539126c79e32861d3255e4aa73d6f06de7a65ce8edb733`.

The principal spawn-adjacent hook is a Harmony postfix on `EnemyAI.Start`. It records view state, chooses/applies the spawn skin and invokes registered `EnemyEventHandler.OnSpawn` callbacks. Separate hooks observe/stage nest use and many enemy lifecycle transitions. The exact source contains no `SpawnEnemyGameObject` call and no enemy-prefab direct network-spawn transaction.

**Classification:** `DOWNSTREAM_ENEMY_LIFECYCLE_SKIN_OBSERVER_NOT_CREATOR`.

**Patch-safety consequence:** suppressing `EnemyAI.Start` to implement DIAG1 would destroy this package's downstream contract in addition to native enemy startup. Isolation must happen before disallowed enemy creation, not by disabling this observer lifecycle.

## 6. EnemySoundFixes 1.9.14 — audio/lifecycle patch set, not enemy creator

Exact DLL: `EnemySoundFixes.dll`, SHA-256 `b295c812646df1ff8b102d2c1f95d66040beb4176b38f93cebaeadc24a017b65`.

The package contains many narrowly targeted enemy/audio Harmony patches. Its vent-related hit is a postfix on `EnemyVent.OpenVentClientRpc` that resets vent audio state. The complete source contains no `Instantiate` call and no `SpawnEnemyGameObject` call; its single `NetworkObject` occurrence is not an enemy creation transaction.

**Classification:** `ENEMY_AUDIO_LIFECYCLE_PATCH_SET_NOT_CREATOR`.

**Patch-safety consequence:** no DIAG1 enemy creation interception is justified here. Vent/lifecycle suppression would instead risk collateral audio or state behavior.

## Cross-package result

This six-package escalation resolves as:

1. Mirage_v81 — conditional Masked pool mutator, disabled by exact S1.42AI spawn-control config;
2. DungeonGenerationPlus — discovery context false positive, not an enemy owner;
3. Remnants — networked remnant/body/scrap infrastructure, not EnemyAI creation;
4. Bozoros — real conditional Puffer/Butler direct network owner behind Emergency Dice provider gating; provider not identified in the exact package inventory;
5. EnemySkinRegistry — downstream spawn/lifecycle observer, not creator;
6. EnemySoundFixes — enemy/audio lifecycle patches, not creator.

The previously unreviewed discovery-positive count is therefore reduced from **37 to 31**. This does not close patch safety. SnowyLib cross-assembly consumer coverage remains open; the remaining 31 discovery positives still require bounded triage/exact escalation; BCMER forced/forced-side/additional/runtime-custom execution remains a separate gate; and exact Shy Guy/project-DLL provenance plus the final host/client-safe narrow interception design remain open.

No DIAG1 implementation, profile build, build/runtime controller transition, Gale import or gameplay test is authorized by this review. `S1.42AI-DIAG1` remains **PLANNED_NOT_BUILT / NOT_BUILD_READY**.
