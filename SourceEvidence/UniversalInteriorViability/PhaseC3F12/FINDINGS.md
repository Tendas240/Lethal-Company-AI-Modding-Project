# C3F12 — exact installed DunGen unique-selection and V81 SpawnSyncedProps semantics

**Status:** GETRANDOM REMOVAL SEMANTICS PROVEN / ROUND MANAGER SPAWN CONSUMER PROVEN / GENERATED THREE-POSITIVE-CANDIDATE CAPACITY UNRESOLVED / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-22  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Capture parent head:** `09c0dda948c1b846dec0183987de99e7d0760ebf`  
**Capture commit:** `df2172ce884716e0ea9cf6992d647993017313c8`

## Bounded objective

C3F12 closes the two implementation links immediately downstream of C3F11's
`DunGen.DungeonGenerator.ProcessGlobalProps()` evidence for the 20 C3F9
static-positive Black-Mesa-row flows:

1. exact installed DunGen `GameObjectChanceTable.GetRandom` behavior when
   `removeFromTable=true`; and
2. exact installed V81 ownership of the later `SpawnSyncedObject.spawnPrefab`
   consumption path.

It does not prove that any concrete generated layout contains three selectable
ID-1231 candidates, that three spawns complete without an exception, or that
gameplay traversal/routing/NavMesh compatibility is safe.

`BackroomsFlow`, `CastleFlow` and `CircusFacilityFlow` remain outside this
20-flow proof set under the C3F10D reference-restoration boundary.

## Exact installed evidence

The repository-native local capture published exactly:

- `SourceEvidence/VanillaV81/DunGenChanceSpawnSynced/20260922T185024Z-e0d76674/DUNGEN_CHANCE_SPAWNSYNCED_FOCUSED_DECOMPILE.txt`;
- `SourceEvidence/VanillaV81/DunGenChanceSpawnSynced/20260922T185024Z-e0d76674/MANIFEST.json`.

The evidence commit is exactly one commit after the reviewed helper head and
contains only those two files.

The manifest binds the capture to:

- installed V81 `Assembly-CSharp.dll` SHA-256
  `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- installed `DunGen.dll` SHA-256
  `d62bbc63eae39ef388797194796ed9cf5a3e7c857fe31f7e5b7310ed78262db6`;
- installed `Lethal Company.exe` SHA-256
  `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam app `1966720`, buildid `22825947`;
- reviewed appmanifest SHA-256
  `132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e`;
- `ilspycmd 11.0.0.9375`;
- repository main
  `56355ff518ae4301a38d370be9561251f6f963c1`;
- reviewed helper PR head
  `09c0dda948c1b846dec0183987de99e7d0760ebf`;
- the existing C3F11 DunGen GlobalProp manifest.

The focused report SHA-256 recorded by the manifest is
`df64120b167705af8c5a6d66b890263bc41dfcb7a7056f2e0f026b985493d43c`.

## GameObjectChanceTable.GetRandom removal semantics

The exact installed `GameObjectChanceTable.GetRandom` body first sums the
effective weights of eligible entries. Eligibility excludes null table entries,
excludes null `Value` entries when `allowNullSelection=false`, and can exclude
`previouslyChosen` when immediate repeats are disallowed.

For the selected entry, the method performs:

`Weights.Remove(weight3)`

before returning that entry whenever `removeFromTable=true`.

C3F11 already proves that `ProcessGlobalProps` calls this method with:

- `allowImmediateRepeats=true`;
- `removeFromTable=true`.

Therefore a successfully selected chance-table entry is removed before the next
selection attempt and cannot be selected again from that same table entry during
the remaining C3F11 loop.

`allowImmediateRepeats=true` does not cancel this removal. It only disables the
separate `previouslyChosen` rejection rule.

### Important zero-weight boundary

Removal happens only after an entry actually wins the weighted selection.

If the remaining eligible entries have no positive effective selection weight,
`GetRandom` can return `null`; no entry is removed in that call.

Consequently, C3F11's clamped loop count of three does **not** by itself prove
three successful distinct selections merely because three ID-1231 entries exist.

For a strong Count-3 capacity proof, a concrete generated layout must expose at
least three ID-1231 entries that are actually eligible and positively weighted
under their generated main/branch-path and normalized-depth conditions.

## Exact V81 spawn consumer

The captured `SpawnSyncedObject` surface exposes the data member:

`public GameObject spawnPrefab;`

The exact installed V81 `RoundManager.SpawnSyncedProps()` body is the consumer.

It obtains:

`SpawnSyncedObject[] array = UnityEngine.Object.FindObjectsOfType<SpawnSyncedObject>();`

and then, for each returned array element, performs one direct:

`UnityEngine.Object.Instantiate(array[i].spawnPrefab, ...)`

at that element's transform position and rotation.

When the instantiated GameObject is non-null, the same loop then performs:

`gameObject2.GetComponent<NetworkObject>().Spawn(destroyWithScene: true);`

and records the spawned object in `spawnedSyncedObjects`.

The entire method is wrapped in one `try/catch`; an exception is logged as
`Unable to sync spawned objects on host`. C3F12 therefore does not turn the
static method body into a claim that every runtime item must complete
exception-free.

## Exact lifecycle ordering

The one-hop same-type caller captured with `SpawnSyncedProps` is
`RoundManager.LoadNewLevelWait(int randomSeed)`.

For levels whose `spawnEnemiesAndScrap` flag is true, the captured method waits
for dungeon generation completion and for connected players to finish generating
the floor. It then waits another 0.3 seconds and calls:

`SpawnSyncedProps();`

before `GeneratedFloorPostProcessing()`.

The call to `SpawnSyncedProps()` itself is outside the later
`if (currentLevel.spawnEnemiesAndScrap)` post-processing guard.

This establishes that the relevant prefab-spawn consumer is
`RoundManager.SpawnSyncedProps`, not a required `Start`/`Awake` or other
self-executing method on `SpawnSyncedObject`.

The earlier helper assumption that `SpawnSyncedObject` itself had to contain
the lifecycle method is therefore rejected by the exact installed V81 evidence.

## Combined C3F11 + C3F12 model

For the 20 C3F9 static-positive flows, the currently proven common chain is:

1. Dawn sets the selected flow's GlobalProp ID 1231 Count to Black Mesa's
   alternate-entrance count of three.
2. DunGen generates the concrete dungeon tiles.
3. `ProcessGlobalProps` discovers generated ID-1231 GlobalProp instances from
   `CurrentDungeon.AllTiles`.
4. DunGen computes their path/depth-dependent chance weights.
5. The requested count is clamped to the number of discovered generated
   candidates.
6. DunGen performs that many weighted `GetRandom` attempts.
7. Every successfully selected chance-table entry is removed from the table
   before it is returned.
8. Each successful returned candidate is activated with `SetActive(true)`.
9. Later, exact V81 `LoadNewLevelWait` invokes
   `RoundManager.SpawnSyncedProps()`.
10. `SpawnSyncedProps` consumes each `SpawnSyncedObject` returned by its
    `FindObjectsOfType` query by instantiating that object's `spawnPrefab`;
    successful instantiated objects are network-spawned.

This closes the two C3F11 downstream implementation questions without proving
the generated-layout cardinality/weight condition that precedes them.

## Current 20-flow proof set

The common C3F11/C3F12 proof set remains exactly:

- `BunkerFlow`
- `DrainsFlow`
- `SubstationFlow`
- `TowerFlow`
- `AquaticDungeonFlow`
- `DeepSewersFlow`
- `FracturedComplexFlow`
- `GreenhouseFlow`
- `MuseumInteriorFlow`
- `StoreFlow`
- `ExpandedFacility`
- `Level3ButCoolFlow`
- `GrandArmoryFlow`
- `RubberRoomsFlow`
- `ToystoreFlow`
- `SlaughterhouseFlow`
- `Black Mesa`
- `SHFlow`
- `SpookyManorFlow`
- `StorageComplex`

The three C3F10D restoration gaps remain separate:

- `BackroomsFlow`
- `CastleFlow`
- `CircusFacilityFlow`

No exhausted C3F10C owner-recovery technique is reopened.

## Remaining proof boundary

The dominant common structural obligation is now narrower:

For each of the 20 static-positive flows, determine whether a concrete
Black-Mesa-sized generated layout can supply at least three **eligible,
positively weighted** ID-1231 candidates before the installed V81
`SetExitIDs` numbering stage.

Source-template cardinality alone remains insufficient because:

- generated tiles can repeat;
- source candidates may never occur in a particular generated layout;
- a discovered candidate can have zero effective path/depth weight;
- the fixed selection-attempt count does not retry beyond its clamped loop merely
  because an attempt returns `null`.

Even a positive three-candidate capacity result would still not by itself prove
full gameplay compatibility, traversal, accessible geometry, routing or NavMesh
safety.

## Lifecycle consequence

No B3 cell changes.

The authoritative matrix remains:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`.

S1.42AB InteriorWeightNormalization remains unchanged.

Black Mesa remains native/Dawn-owned; no duplicate LLL registration is added.

Shatteredrooms × Experimentation and Shatteredrooms × Embrion remain excluded.

`BuildSpecs/current.json` remains disabled and
`RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

No gameplay build or runtime test is authorized by C3F12.

## Next bounded segment

Perform a repository-held **generated-capacity feasibility pass** before creating
another local capture or authorizing gameplay.

Use the existing C3F8/C3F9 machine evidence for the 20-flow proof set to build a
per-flow ledger of:

- how ID-1231 candidates enter the flow (direct tile descendant versus exact
  positive-weight Doorway blocker indirection);
- which TileSets/archetypes/tiles can carry those candidates;
- the serialized MainPathWeight, BranchPathWeight and DepthWeightScale inputs
  available for those candidates;
- whether the existing flow graph and length/repetition constraints establish a
  static lower bound of at least three eligible positive-weight candidates in a
  generated Black-Mesa-sized layout.

Do not infer a guaranteed runtime lower bound merely from three source templates
or package-wide counts.

If the existing repository-held asset/flow evidence cannot establish that lower
bound, stop at the precise missing DunGen generation rule and identify the
smallest exact installed-DunGen method surface needed for the next focused
capture.

Do not request a gameplay run, change B3, implement a universal override, modify
S1.42AB normalization, or revisit the three C3F10D restoration gaps in this
segment.
