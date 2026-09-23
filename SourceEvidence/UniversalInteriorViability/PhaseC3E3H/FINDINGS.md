# C3E3H — Oxyde External-row applicability and alternate-topology boundary

Status: bounded source/owner applicability decision complete; ordinary interior generation is not reachable through the current inspected Oxyde path, and no independent entrance/dungeon-construction path is established. No matrix, gameplay build or runtime-test change is authorized.

## Scope and authority

Parent PR #138 HEAD at checkpoint start: `de87857889579b5c47f0bf69c02e33e6f3c17acf`. Verified main remains `56355ff518ae4301a38d370be9561251f6f963c1`. Accepted gameplay baseline remains S1.42AK.

C3E3G closed the upstream installed-V81 gate: when `currentLevel.spawnEnemiesAndScrap == false`, exact V81 `RoundManager.GenerateNewLevelClientRpc` returns before the `RuntimeDungeon` lookup and before the ordinary `GenerateNewFloor` callsite. C3E3H asks the remaining bounded question for Oxyde only:

**Does the exact package/owner evidence establish an independent static or owner/runtime path that supplies dungeon generation or entrance-pairing semantics despite that skipped ordinary generation path?**

This checkpoint does not inspect Black Mesa 3.4.4 topology and does not generalize entrance semantics to other moons.

## Exact Oxyde asset state

C3E3C remains the exact package authority for the Oxyde moon/level definition from CodeRebirth 1.6.9:

- key `code_rebirth:oxyde`;
- level 745 / scene `Oxyde`;
- exact packaged `spawnEnemiesAndScrap = false`;
- packaged `dungeonFlowTypes` empty;
- packaged indoor enemies, daytime enemies, scrap, map objects and indoor hazards empty;
- `planetHasTime = false`, risk `Safe`;
- nine outside-enemy entries remain present;
- the Dusk moon definition registers exactly one Oxyde scene from bundle `oxydescene`.

C3E3D's exact six-assembly owner scan covered 10,024 available method bodies with zero parse errors. All 14 instructions targeting `SelectableLevel.spawnEnemiesAndScrap` are reads; no direct write or address-take enables the flag. Dawn's sole direct `dungeonFlowTypes` write can populate selectable dungeon metadata independently, but does not enable ordinary level generation.

Dawn's Company auto-tagger predicate returns `!moon.Level.spawnEnemiesAndScrap`; therefore the preserved Oxyde false flag satisfies that implementation predicate. This is a tag/implementation result, not a claim that Oxyde is semantically identical to Gordion or that its complete design intent is known.

## Static scene entrance surface

C3E3B statically parsed the exact 55,038,216-byte Oxyde scene bundle from CodeRebirth 1.6.9:

- 20,561 serialized objects;
- all 52 MonoScripts;
- all 965 MonoBehaviours, with zero parse errors;
- all 4,424 GameObjects, with zero parse errors;
- all 963 non-null MonoBehaviour script references resolved;
- two null-script MonoBehaviours retained on the `DungeonGenerator` GameObject.

The complete parsed component surface contains:

- zero MonoScript classes named `EntranceTeleport`;
- zero recursive field matches for `entranceId`, `isEntranceToBuilding`, `entrancePoint` or `exitPoint`;
- no entrance/fire-exit/teleport-named GameObject; the only related name hit is `DungeonGenerator`.

The two null-script records do not contain serialized entrance IDs or pairing fields. This remains negative static evidence only: it does **not** prove that runtime Oxyde contains zero entrance objects.

Earlier source-prefab checkpoints similarly found no direct Oxyde scene/prefab entrance serialization, while explicitly preserving incomplete recursive source-GUID coverage. Exact package composition therefore remains the stronger bounded static surface.

## CodeRebirth entrance handling is observational, not constructive

The version-matched CodeRebirth 1.6.9 source tree is commit `3aec94f6f737c86d5e1eb59a57396740317b210f`. It is version-matched source, not asserted byte-identical to the accepted package DLL; exact binary identity remains anchored by the native-owner evidence.

The narrowly relevant source blobs are:

- `Plugin/CodeRebirth/src/Patches/EntranceTeleportPatch.cs` — Git blob `91238eaa4ddde5428cd88246a30418c33b34f3dc`;
- `Plugin/CodeRebirth/src/Content/Maps/OxydeCrane.cs` — Git blob `b4d34145843a64511c117c727190e021721ec1c1`;
- `Plugin/CodeRebirth/src/MiscScripts/ShipAnimator.cs` — Git blob `7bc2b69f2b254110a77238201e627a41d335000d`;
- `Plugin/CodeRebirth/src/Patches/EnemyAIPatch.cs` — Git blob `d52af2414f5f70d8e8fd8e1dd21c00be3cc35727`;
- `Plugin/CodeRebirth/src/Util/CodeRebirthUtils.cs` — Git blob `d6e83983b62a25026b2f468a8f7d00f434636c72`.

`EntranceTeleportPatch` hooks `EntranceTeleport.Awake` and `OnDestroy` only to add/remove already-existing instances from `CodeRebirthUtils.EntrancePoints`. It does not instantiate an `EntranceTeleport`, assign `entranceId`, set `isEntranceToBuilding`, create inside/outside targets or rewrite pairing.

The exact CodeRebirth binary discovery blob `31c4d1ceed2b9f5a7905a177b533f1d0e131b5a5` likewise exposes the patch/type surface and Oxyde-specific classes without an inspected `AddComponent<EntranceTeleport>`, `Instantiate<EntranceTeleport>`, `new EntranceTeleport` or equivalent creator signature. Other observed CodeRebirth entrance references consume already-existing teleports or entrance-use events. This is a bounded discovery-surface statement, not a whole-program proof against arbitrary reflection or an uninspected dependency.

## Oxyde-specific owner behavior does not supply a dungeon

The version-matched Oxyde-specific code inspected here is exterior/lifecycle-oriented:

- `EnemyAIPatch` marks enemies as outside on Oxyde and chooses a nearby outside AI node.
- `ShipAnimator` handles Oxyde-specific ship landing/leaving behavior and the death reroute.
- `OxydeCrane` waits for `dungeonCompletedGenerating` and a map-props container before calling `SpawnOutsideHazards()`; it does not invoke `GenerateNewFloor`, `RuntimeDungeon.Generate` or create entrance teleports.
- `OxydeCrane.Update()` continuously sets `RoundManager.Instance.currentDungeonType = -1`, which is consistent with an exterior/special-level treatment but is not independently elevated into an author-intent claim.

Waiting on `dungeonCompletedGenerating` is not evidence that Oxyde itself generated a dungeon: the coroutine observes a lifecycle state and then triggers outside hazards.

## DawnLib boundary

The exact DawnLib 0.9.25 binary discovery remains bound to main DLL SHA-256 `9b4826a16eec1fa5091fb4246d010005bc9c3e04282034e8d067b499ab5c125b`.

The narrowly relevant discovered generation operations are attached to the `RoundManager.GenerateNewFloor` / `RuntimeDungeon` integration already resolved by C3E3E. The inspected Dawn discovery surface does not establish a separate `EntranceTeleport` constructor/instantiator or an alternate false-flag dungeon-generation path.

C3E3G is therefore decisive for the ordinary supported path: Oxyde's preserved false flag returns before the callsite through which LLL/Dawn dungeon selection/generation integration would execute.

## External-row applicability result

The C3 selection work remains valid at its own layer:

- the 22 direct LLL `Vanilla:100,Custom:100` flows can match Oxyde's bridged `Custom` tag;
- the Dawn-native Black Mesa dungeon rule can also match Oxyde;
- together these account for **23 Oxyde selection-supported pairings** and, with the 23 Black Mesa-row pairings, the existing **46 External selection-supported pairings**.

C3E3H does not retract those metadata/selection results.

However, for Oxyde those positive selection matches are **not sufficient to establish an executable ordinary interior pairing**. Under the currently inspected exact architecture:

1. Oxyde preserves `spawnEnemiesAndScrap=false`;
2. exact V81 returns before the ordinary dungeon-selection/generation callsite;
3. the exact scene bundle supplies no directly identifiable serialized `EntranceTeleport` topology;
4. no inspected CodeRebirth/Dawn owner path establishes an independent dungeon or entrance-pair construction route.

**Bounded decision:** Oxyde is not currently proven to be an applicable ordinary interior-generation target through the supported inspected V81/LLL/Dawn/CodeRebirth path. A simple rarity/tag/selection override cannot establish universal interior availability on Oxyde. Making ordinary interiors actually generate there would require changing generation semantics or proving a different construction path, not merely equalizing availability metadata.

This is stronger than `selection-only uncertainty`, but it is deliberately **not** labeled a proven gameplay incompatibility or a claim that Oxyde has zero runtime entrances.

## Matrix and lifecycle consequence

The authoritative Phase-B3 matrix remains unchanged by this source checkpoint, per the C3 proof contract. No Oxyde cell is promoted, removed or reclassified solely from this source evidence.

Preserved state:

- B3 remains 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, 914 `NOT_YET_PROVEN`;
- all 46 External selection-supported pairings remain separately recorded as selection-layer evidence;
- Black Mesa is not duplicate-registered;
- Shatteredrooms × Experimentation/Embrion exclusions remain intact;
- S1.42AB InteriorWeightNormalization remains unchanged;
- S1.42AK remains accepted/latest;
- no candidate or runtime test is armed;
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains S1.42AK.

## Proof boundary

C3E3H does **not** prove:

- zero Oxyde runtime `EntranceTeleport` objects;
- zero possible reflection-/dependency-/runtime-created entrance objects;
- that Oxyde is broken;
- that Oxyde can never support generated interiors under a future deliberate semantic change;
- exact Black Mesa 3.4.4 entrance topology;
- general vanilla/LLL/Dawn entrance-ID assignment or inside/outside pairing rules.

It proves only that the current inspected Oxyde path does not provide the required ordinary interior generation/topology mechanism despite positive selection metadata.

## Next bounded segment

Next **C3F1**: acquire and inspect exact Black Mesa 3.4.4 package/scene topology evidence using repository-native provenance first. Establish the accepted package's actual Dawn-owned moon scene and entrance/fire-exit surface without using the obsolete public 0.9.0/direct-LLL source as current implementation evidence.

Do not duplicate-register Black Mesa, do not start a gameplay run, and do not modify the B3 matrix from source evidence alone. General DawnLib/LLL/vanilla entrance-ID and pairing semantics remain a later C3 obligation.
