# C3F11 — exact installed DunGen GlobalProp Count semantics

**Status:** COUNT CONSUMPTION SEMANTICS PROVEN / GENERATED THREE-CANDIDATE CAPACITY UNRESOLVED / SPAWNSYNCEDOBJECT EXECUTION UNRESOLVED / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-22  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Capture parent head:** `0a5407d26a5614bf944756e7b43eca8461164eb3`  
**Capture commit:** `95c7ecd579fe6d74c53ee8feac7040a88011aaaf`

## Bounded objective

C3F11 resolves only the first dynamic Count-3 question left by C3F8/C3F9 for the
20 static-positive Black-Mesa-row flows:

- how exact installed V81 DunGen consumes a selected DungeonFlow GlobalProp count;
- what candidate set that count operates on;
- what happens when the generated dungeon contains fewer candidates than the
  requested count.

It does not infer `SpawnSyncedObject` execution behavior, generated-layout
capacity, or gameplay compatibility.

BackroomsFlow, CastleFlow and CircusFacilityFlow remain outside this 20-flow
proof set under the separate C3F10D restoration boundary.

## Exact installed evidence

The repository-native capture published:

- `SourceEvidence/VanillaV81/DunGenGlobalProp/20260922T171706Z-6231fcfa/DUNGEN_GLOBALPROP_FOCUSED_DECOMPILE.txt`;
- `SourceEvidence/VanillaV81/DunGenGlobalProp/20260922T171706Z-6231fcfa/MANIFEST.json`.

The capture is bound to:

- installed V81 `Assembly-CSharp.dll` SHA-256
  `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- installed `DunGen.dll` SHA-256
  `d62bbc63eae39ef388797194796ed9cf5a3e7c857fe31f7e5b7310ed78262db6`;
- Steam app `1966720`, buildid `22825947`;
- pinned `ilspycmd 11.0.0.9375`;
- repository main `56355ff518ae4301a38d370be9561251f6f963c1`;
- PR #138 head `0a5407d26a5614bf944756e7b43eca8461164eb3` at capture time.

Only the focused report and manifest were published. No game/DunGen binary,
full type decompile, local path or gameplay run was uploaded.

## Exact generation-stage ordering

`DunGen.DungeonGenerator.PostProcess()` calls, in order relevant here:

1. `CurrentDungeon.PostGenerateDungeon(this)`;
2. `ProcessLocalProps()`;
3. `ProcessGlobalProps()`;
4. later built-in post-processing including key/lock placement.

Therefore the captured GlobalProp selection happens against the already generated
`CurrentDungeon` tile set during DunGen post-processing.

## What ProcessGlobalProps actually does

The exact installed `ProcessGlobalProps()` body establishes this algorithm.

### 1. Candidate discovery is from the concrete generated dungeon

DunGen enumerates every tile in `CurrentDungeon.AllTiles`.

For each generated tile it calls
`GetComponentsInChildren<GlobalProp>(includeInactive: true)`.

Each discovered `GlobalProp` is grouped by its `PropGroupID`.

This is decisive for the earlier proof boundary: the Count does not operate on
the number of source templates in an asset bundle. It operates on GlobalProp
instances that exist in the concrete generated dungeon tile hierarchy.

### 2. Each candidate receives a generation weight

For each candidate DunGen selects either:

- `MainPathWeight` when the owning generated tile is on the main path; or
- `BranchPathWeight` otherwise.

That weight is multiplied by
`DepthWeightScale.Evaluate(allTile.Placement.NormalizedDepth)`.

The resulting GameObject/weight entry is added to the chance table for that
`PropGroupID`.

### 3. All collected candidates are initially disabled

Before selecting winners, DunGen iterates every collected chance-table entry and
calls:

`weight.Value.SetActive(false)`.

The later selection stage therefore activates selected existing candidate
GameObjects. This method does not instantiate or duplicate extra GlobalProp
candidates to satisfy a requested Count.

### 4. The requested Count is read from the matching DungeonFlow setting

For a generated candidate group, DunGen finds the first
`DungeonFlow.GlobalProps` entry whose `ID` equals that generated
`PropGroupID`.

It then evaluates:

`globalPropSettings.Count.GetRandom(RandomStream)`.

C3F4 already proves that Dawn rewrites GlobalProp ID 1231 to the active moon's
alternate-entrance count before DunGen generation. For Black Mesa, that effective
requested count is three.

### 5. The Count is clamped to the number of generated candidates

The exact implementation performs:

`random = Mathf.Clamp(random, 0, gameObjectChanceTable.Weights.Count)`.

Therefore an effective ID-1231 Count of three cannot cause DunGen to synthesize
three candidates when fewer than three ID-1231 GlobalProp instances exist in the
generated dungeon.

If the concrete generated layout exposes only N candidates where N < 3, the
selection-loop count is clamped to N.

This closes the C3F8 question about the explicit fewer-than-requested-candidates
behavior.

### 6. Selection uses the generated weighted table

DunGen loops the clamped number of times and calls
`GameObjectChanceTable.GetRandom(... allowImmediateRepeats: true,
removeFromTable: true)`.

When the returned entry and GameObject are non-null, DunGen activates that
candidate with `SetActive(true)`.

The current capture proves those call arguments but does not include the
implementation of `GameObjectChanceTable.GetRandom`. Therefore C3F11 does not
over-claim the exact removal/repeat behavior beyond the fact that
`removeFromTable: true` is requested by `ProcessGlobalProps`.

## Count-3 consequence for the 20 static-positive flows

The common static model is now narrower and stronger:

1. Dawn requests ID-1231 Count 3 for Black Mesa.
2. DunGen generates the dungeon tiles.
3. `ProcessGlobalProps` discovers ID-1231 GlobalProp instances actually present
   on those generated tiles.
4. DunGen clamps the requested 3 to the number of discovered generated
   candidates.
5. It performs that many weighted selection attempts and activates successful
   returned candidates.
6. DunGen does not create additional GlobalProp candidates when the generated
   layout provides fewer than three.

Therefore a source asset containing one, two, three or many fire-exit templates
does not by itself prove Count-3 capacity.

For Black Mesa's three moon-side alternate entrances, the remaining structural
requirement is now explicit: the generated interior must expose enough usable
ID-1231 GlobalProp candidates for three successful selections before the
inside-side teleports can be numbered.

## Relationship to installed V81 entrance numbering

The existing exact installed-V81 pairing evidence remains unchanged.

`RoundManager.SetExitIDs` numbers active inside-side
`EntranceTeleport` instances whose pre-numbering state is:

- `entranceId == 1`;
- `isEntranceToBuilding == false`.

Those instances are assigned sequential IDs beginning at 1.

`EntranceTeleport.FindExitPoint` then requires:

- opposite `isEntranceToBuilding` side; and
- equal `entranceId`.

Thus, if three valid inside-side pre-ID-1 EntranceTeleports exist by that stage,
the proven V81 numbering path can assign them IDs 1, 2 and 3 and the corresponding
Black Mesa outside IDs can pair by ID/opposite side.

C3F11 does not prove that all three inside teleports exist. If fewer usable
inside exits are produced, the missing outside-side ID(s) would have no proven
inside counterpart under `FindExitPoint`.

## What remains unproven

C3F11 closes the Count-consumption/fewer-candidate semantics only.

The following obligations remain for the 20 static-positive flows:

1. exact `GameObjectChanceTable.GetRandom` behavior for
   `removeFromTable: true`, including whether repeated selection of the same
   candidate is impossible in this path;
2. exact installed `SpawnSyncedObject` lifecycle/implementation establishing
   whether activation of one selected ID-1231 GlobalProp causes its captured
   `spawnPrefab` to execute exactly once at the relevant generation stage;
3. whether concrete generated layouts for each target flow can actually expose
   at least three usable ID-1231 candidates under Black-Mesa-sized generation,
   rather than merely having source templates that can appear;
4. later compatibility evidence for generation success, traversal, accessible
   geometry, routing and NavMesh safety before any universal promotion.

## Lifecycle consequence

No B3 cell changes.

The matrix remains:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`.

S1.42AB InteriorWeightNormalization remains unchanged.

Black Mesa remains native/Dawn-owned; no duplicate LLL registration is added.

Shatteredrooms × Experimentation and Shatteredrooms × Embrion remain excluded.

S1.42AK remains accepted/latest. No gameplay build or runtime test is authorized
by this checkpoint.

## Next bounded segment

Capture the two implementation links immediately downstream of
`ProcessGlobalProps` that are still required for the Count-3 proof:

1. exact installed DunGen `GameObjectChanceTable.GetRandom` behavior relevant to
   `removeFromTable: true`;
2. exact installed V81 `SpawnSyncedObject` behavior relevant to an activated
   GlobalProp's `spawnPrefab`.

Use the existing SHA-bound V81/DunGen provenance and focused-decompile
infrastructure. Publish only focused source evidence and manifests.

Do not start gameplay generation-capacity testing, change B3, author a universal
override, or build a gameplay candidate from C3F11 alone.
