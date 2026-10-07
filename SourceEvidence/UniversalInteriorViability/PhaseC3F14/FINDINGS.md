# C3F14 — installed DunGen generation-capacity implementation synthesis

**Status:** CAPTURE VERIFIED / CORE GENERATOR SEMANTICS RESOLVED / 0 OF 20 THREE-POSITIVE LOWER BOUNDS PROVEN / CROSS-TYPE CALLEE GAP NARROWED / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-22  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Capture commit:** `73a9552df7af0b51842ed2cf95f03145cc5928b9`  
**Capture manifest:** `SourceEvidence/VanillaV81/DunGenGenerationCapacity/20260922T193336Z-5d63c0ca/MANIFEST.json`  
**Focused report:** `SourceEvidence/VanillaV81/DunGenGenerationCapacity/20260922T193336Z-5d63c0ca/DUNGEN_GENERATION_CAPACITY_FOCUSED_DECOMPILE.txt`

## Bounded objective

C3F14 evaluates the exact installed-V81 DunGen generation-capacity capture requested by C3F13 against the existing 20-flow C3F13 feasibility ledger.

It does not reopen C3F10D, change the B3 matrix, author a universal override, create a gameplay build or authorize runtime testing.

## Capture provenance

The capture is bound to:

- `Assembly-CSharp.dll` SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- `DunGen.dll` SHA-256 `d62bbc63eae39ef388797194796ed9cf5a3e7c857fe31f7e5b7310ed78262db6`;
- `Lethal Company.exe` SHA-256 `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam app `1966720`, buildid `22825947`;
- ilspycmd `11.0.0.9375`;
- repository main `56355ff518ae4301a38d370be9561251f6f963c1`;
- PR #138 capture parent `911338ae00b584245125857a5f7262ed90e43eef`;
- C3F13 ledger text SHA-256 `6ae725f5982da848a0cd11c52d03bd3657df3b01b5ff9723df5674503dac48b3`.

The helper published only the focused report and manifest. No game binary, DunGen binary or full type decompile was committed.

## Exact semantics now proven

### Main-path construction

`DungeonGenerator.InnerGenerate` computes:

`targetLength = Max(RoundToInt(DungeonFlow.Length.GetRandom(RandomStream) * LengthMultiplier), 2)`.

`GenerateMainPath` then samples graph depth as `num / (targetLength - 1)`, asks `DungeonFlow.GetLineAtDepth(depth)`, changes archetype through `GraphLine.GetRandomArchetype(...)`, and substitutes the first not-yet-consumed graph node whose `Position <= depth`. Slot construction stops when the last graph node is consumed.

Concrete placement passes `j / (placementSlots.Count - 1)` into `AddTile`.

This resolves the generator-side discretization mechanism that C3F13 lacked. It does **not** yet resolve the implementations of `DungeonFlow.GetLineAtDepth` or `GraphLine.GetRandomArchetype`.

### Required injections

`GatherTilesToInject` materializes each eligible `TileInjectionRule` as an `InjectedTile`. Main-only rules are deterministically marked main-path.

`AddTile` checks pending injections through `InjectedTile.ShouldInjectTileAtPoint(...)`. On a successful injected placement it records `InjectionData`, removes that exact pending injection, and increments `targetLength` for main-path injection placement.

After branch generation, `InnerGenerate` scans remaining pending injections. Any remaining `IsRequired` injection forces a full generation retry. Therefore a generation that reaches `Complete` cannot still contain an unplaced required injection.

This closes C3F13's required-injection **completion/failure** ambiguity. The exact depth predicate remains external in `InjectedTile.ShouldInjectTileAtPoint`, so positive ID-1231 weight at the injection's final depth is not yet independently proven from this capture alone.

### Branch and cap construction

`GenerateBranchPaths` obtains per-main-tile branch counts from `BranchCountHelper.ComputeBranchCounts`.

For every generated branch, its length comes from `Archetype.BranchingDepth.GetRandom`. First and last branch positions use BranchStart/BranchCap TileSets according to `BranchStartType` / `BranchCapType`; intermediate positions use the archetype's ordinary TileSets. Branch normalized depth is `1` for branch depth <= 1, otherwise `j / (branchDepth - 1)`.

This proves how a selected branch reaches a candidate-only cap such as Black Mesa's `Office Cap Test` or `Lab Cap Test`. It does not prove that a qualifying branch exists, because `BranchCountHelper.ComputeBranchCounts` remains outside the focused report.

### Tile choice and repeat restrictions

`AddTile` flattens the selected TileSets' `TileWeights.Weights` into a `DoorwayPairFinder`, supplies the current normalized depth, and enforces:

- `TileRepeatMode.Allow` -> allowed;
- `DisallowImmediate` -> previous tile prefab may not repeat immediately;
- `Disallow` -> prefab may not already exist anywhere in the generated proxy dungeon.

The actual weighted/socket-compatible ordering and filtering inside `DoorwayPairFinder.GetDoorwayPairs` is not present in the capture. A mixed candidate-bearing TileSet therefore still does not establish that an ID-1231-bearing tile must be selected.

### Final normalized depth

`TryPlaceTile` assigns integer `PathDepth` / `BranchDepth`. During `PostProcess`, every concrete tile receives:

`NormalizedPathDepth = PathDepth / (MainPathTiles.Count - 1)`.

`TilePlacementData.NormalizedDepth` returns `NormalizedPathDepth` for main-path tiles and `NormalizedBranchDepth` for branch tiles.

This closes C3F13's generator-side `Tile.Placement.NormalizedDepth` ambiguity.

### Doorway blocker materialization

For an unused `DunGen.Doorway`, `ProcessDoorwayObjects` checks `BlockerPrefabWeights.HasAnyViableEntries()` and, if true, instantiates exactly one prefab returned by `BlockerPrefabWeights.GetRandom(randomStream)`.

This proves the materialization path for `SHFlow`, `SpookyManorFlow` and `StorageComplex`. Positive target weight remains possibility evidence, not a target-selection lower bound, unless a generated doorway's viable blocker table can itself be proven target-only.

## C3F13 threshold result after the new capture

The exact C3F13 question remains:

> Is a static lower bound of at least three generated, eligible, positively weighted ID-1231 candidates proven for any of the 20 proof-set flows?

**Result: no. The count remains 0/20.**

The reason is now substantially narrower:

- `BunkerFlow`: completed generation now proves both required injections cannot remain pending, and both source from candidate-only `BunkerCheckpointSet`; however the exact `ShouldInjectTileAtPoint` depth predicate is still needed before both can be promoted to positive-weight candidates at their intended depth windows, and current evidence still lacks a guaranteed third.
- `GreenhouseFlow`: Goal remains candidate-only, and Line 0 / Line 2 use candidate-only `CornSet`; the remaining blocker is exact `DungeonFlow.GetLineAtDepth` / archetype resolution against the serialized graph, not generic target-length uncertainty.
- `SlaughterhouseFlow`: completed generation closes the required-injection failure semantics and Goal is candidate-only, but the exact injection-depth predicate remains missing and no third guaranteed positive candidate follows.
- `Black Mesa`: branch-cap materialization semantics are now known, but `BranchCountHelper.ComputeBranchCounts` and exact line/archetype selection still prevent a guaranteed candidate-only cap from being instantiated.
- the remaining direct flows still rely on mixed TileSets, so `DoorwayPairFinder.GetDoorwayPairs` is the unresolved selection boundary.
- the three Doorway-blocker flows now have exact blocker materialization semantics, but no target blocker is guaranteed merely from positive weight.

This remains a **proof boundary**, not a compatibility failure.

## Smallest remaining exact DunGen surface

Do not recapture `DungeonGenerator.ProcessGlobalProps`, `GameObjectChanceTable.GetRandom`, `RoundManager.SpawnSyncedProps`, the already captured `DungeonGenerator` cluster, `TilePlacementData.NormalizedDepth`, or `Doorway.ProcessDoorwayObjects`.

The next focused installed-DunGen evidence should contain only the cross-type callees that still block the proof:

1. `DunGen.DungeonFlow.GetLineAtDepth`;
2. `DunGen.GraphLine.GetRandomArchetype` and only directly required same-type helpers;
3. `DunGen.InjectedTile.ShouldInjectTileAtPoint` and only directly required constructor/range helpers;
4. `DunGen.BranchCountHelper.ComputeBranchCounts` and only directly required same-type helpers;
5. `DunGen.DoorwayPairFinder.GetDoorwayPairs` and only directly required same-type helpers that evaluate/filter/order candidate tile pairs.

The capture must remain fail-closed and publish focused source evidence plus manifest only.

## Lifecycle consequence

- B3 matrix unchanged.
- S1.42AB InteriorWeightNormalization unchanged.
- Black Mesa remains native/Dawn-owned and must not be duplicate-registered through LLL.
- Shatteredrooms x Experimentation / Embrion remain excluded.
- No gameplay candidate exists.
- No runtime test is authorized.
- C3F10D restoration gaps are not reopened.

## Next bounded segment

Create and CI-validate the minimal cross-type DunGen callee helper above on PR #138. Stop after exact-head helper CI is green; do not request another local capture in that same segment.
