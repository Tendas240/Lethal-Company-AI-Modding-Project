# C3F15 — exact V81 cross-type DunGen callee synthesis and first Count-3 lower bound

**Status:** CAPTURE VERIFIED / 1 OF 20 THREE-POSITIVE GENERATED LOWER BOUNDS PROVEN / GREENHOUSEFLOW STATIC COUNT-3 CAPACITY PROVEN / 19 REMAINING / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-22  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Capture commit:** `8b50743b86943a92fc06d6af98f0b0b20eb99ead`  
**Capture parent:** `d39b03326972787e6814f9fb6dd1125532cee220`  
**Capture directory:** `SourceEvidence/VanillaV81/DunGenGenerationCapacityCallees/20260922T204232Z-51dd0fae/`  
**Focused report SHA-256:** `da2132eddb988e3154c67e63eaade718fc9b631d930e02d8f1cafcd5ab264efd`

## Bounded objective

C3F15 ingests the exact installed-V81 cross-type DunGen callee capture requested by C3F14 and evaluates only the 20-flow C3F13 proof set.

The question remains the C3F12/C3F13 threshold:

> Does existing exact asset evidence plus exact installed DunGen implementation establish a static lower bound of at least three generated, eligible, positively weighted GlobalProp-ID-1231 candidates for any proof-set flow?

The answer changes from 0/20 to **1/20**. `GreenhouseFlow` now satisfies the strong static Count-3 capacity predicate.

This is not a B3 matrix promotion and is not full gameplay compatibility proof.

## Capture provenance

The new evidence commit is the direct child of the reviewed helper head and adds only the focused report plus `MANIFEST.json`.

The manifest binds:

- `Assembly-CSharp.dll` SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- `DunGen.dll` SHA-256 `d62bbc63eae39ef388797194796ed9cf5a3e7c857fe31f7e5b7310ed78262db6`;
- `Lethal Company.exe` SHA-256 `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam app `1966720`, buildid `22825947`;
- appmanifest SHA-256 `132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e`;
- ilspycmd `11.0.0.9375`;
- main `56355ff518ae4301a38d370be9561251f6f963c1`;
- capture parent PR head `d39b03326972787e6814f9fb6dd1125532cee220`;
- the exact C3F14 synthesis ledger and its five remaining callee roots.

No game/DunGen binary, full type decompile, local clone, build or gameplay evidence was published.

## Five cross-type callees

### 1. DungeonFlow.GetLineAtDepth

The method clamps depth to 0..1, returns the first line at depth 0 and the last line at depth 1, and otherwise returns the first line satisfying:

`normalizedDepth >= line.Position && normalizedDepth < line.Position + line.Length`.

This closes C3F14's exact line-boundary ambiguity.

### 2. GraphLine.GetRandomArchetype

The method filters `DungeonArchetypes` only by the `Unique` rule against already-used archetypes. If that filtered set is empty it falls back to the complete line archetype list. It then selects an index from that set through the generation RandomStream.

Consequences:

- a one-archetype line is deterministic;
- a non-unique archetype may be selected again on a later line;
- a multi-archetype line does not provide a deterministic candidate-only guarantee merely because one member has a candidate-only cap or TileSet.

### 3. InjectedTile.ShouldInjectTileAtPoint

The method requires the requested main/branch side to match. It rejects while `NormalizedPathDepth > pathDepth`. Once the sampled path threshold is reached, a main-path injection is immediately eligible; branch injections additionally require `NormalizedBranchDepth <= branchDepth`.

Together with C3F14's required-injection retry semantics this proves that a completed generation cannot omit a required main-path injection after its sampled threshold becomes reachable.

For the current proof set this strengthens:

- `BunkerFlow`: both required candidate-only `BunkerCheckpointSet` injections are generated in a completed layout, at positive normalized path depths. Static lower bound: at least **2** positive ID-1231 candidates.
- `SlaughterhouseFlow`: its required candidate-only `ProcessingRoomSet` injection plus candidate-only Goal establish at least **2** positive ID-1231 candidates.

Neither flow gains a guaranteed third candidate from existing evidence.

### 4. BranchCountHelper.ComputeBranchCounts

The exact helper dispatches by `BranchMode`:

- Local: sample each main tile's archetype `BranchCount`, capped by unused doorways;
- Section: sample once per graph line/archetype section and distribute by unused-doorway weights;
- Global: sample the flow-level `BranchCount` and distribute across eligible main tiles subject to archetype and doorway caps.

This closes C3F14's branch-count implementation gap but does not make Black Mesa's candidate-only Office/Lab caps guaranteed. Black Mesa has one graph line with six possible archetypes. `GetRandomArchetype` therefore retains a random archetype choice, and existing evidence does not prove that every possible chosen archetype exposes a candidate-only branch cap.

### 5. DoorwayPairFinder.GetDoorwayPairs

`CalculateOrderedListOfTiles` builds an ordering by repeatedly calling the already-proven `GameObjectChanceTable.GetRandom` over entries whose effective weight is positive, removing each selected entry from the temporary table. Potential doorway pairs are then generated only from members of that positive-weight ordering and filtered by repeat/placement predicates plus doorway/socket validity. `OrderDoorwayPairs` sorts the surviving pairs by the randomized tile-order rank, then doorway weight.

Therefore:

- candidate-only TileSets remain strong: any successfully placed tile from such a set is candidate-bearing;
- mixed TileSets remain non-deterministic: a positive candidate weight proves eligibility/possibility, not that the candidate must be the successfully placed tile;
- the three C3F9 indirect Doorway-blocker flows are not upgraded by this method, because their remaining uncertainty is the separate blocker-prefab choice rather than TileSet ordering.

## GreenhouseFlow — first strong Count-3 proof

The C3F7 artifact re-used by C3F13 is still digest-bound and reverified. For `GreenhouseFlow` it records:

- flow `Length = 12..12`;
- Start node at position 0;
- Goal node at position 1 using candidate-only `CornEnd` 1/1;
- Line 0: position 0, length 0.4, exactly one archetype: `CornArchetype`;
- Line 1: position 0.4, length 0.3, exactly one archetype: `GreenhouseArchetype`;
- Line 2: position 0.7, length 0.3, exactly one archetype: `CornArchetype`;
- `CornArchetype.Unique = 0`;
- `CornArchetype` uses `CornSet`;
- `CornSet` is 3/3 candidate-bearing and all three tile choices have positive tile-selection base weights.

C3F14 proves that `GenerateMainPath` constructs slots at `num / (targetLength - 1)`, substitutes the first not-yet-consumed node whose position has been reached, and otherwise uses the current line archetype.

For target length 12 the successful main path is therefore statically partitioned as:

- slot 0: Start node;
- slots 1..4, depths 1/11..4/11: Line 0 / `CornArchetype` / candidate-only `CornSet`;
- slots 5..7, depths 5/11..7/11: Line 1 / `GreenhouseArchetype`;
- slots 8..10, depths 8/11..10/11: Line 2 / `CornArchetype` / candidate-only `CornSet`;
- slot 11, depth 1: candidate-only Goal / `CornEnd`.

The new `GetRandomArchetype` body makes both Corn line selections deterministic because each line contains exactly one archetype, and `CornArchetype` is non-unique.

C3F13 already binds the relevant ID-1231 candidate weight profiles for Greenhouse to positive base weights with depth curves that are positive for every normalized depth greater than zero. C3F14 binds final main-path normalized depth to `PathDepth / (MainPathTiles.Count - 1)`.

Thus every successfully generated slot 1..4 and 8..10 contributes at least one eligible, positively weighted ID-1231 candidate, and the Goal contributes another at depth 1.

**Static generated positive-candidate lower bound for GreenhouseFlow: at least 8.**

This is stronger than the required Count-3 threshold. Combined with C3F11/C3F12, Dawn's Black Mesa request for three alternate exits has at least three distinct eligible generated candidates to select from for this flow.

## Updated 20-flow result

- **1/20 proven:** `GreenhouseFlow`, lower bound >= 8.
- **19/20 not proven at the >=3 threshold.**
- `BunkerFlow`: strengthened to lower bound >= 2.
- `SlaughterhouseFlow`: strengthened to lower bound >= 2.
- `Black Mesa`: branch implementation is resolved, but multi-archetype selection still blocks a guaranteed candidate-only cap.
- Other direct flows remain blocked by mixed TileSets or insufficient candidate-only forced surfaces.
- `SHFlow`, `SpookyManorFlow`, and `StorageComplex` remain blocked by non-guaranteed target blocker selection.

The new result is a proof-boundary improvement, not evidence that any remaining 19 flow is incompatible.

## Black Mesa x Greenhouse evidence consequence

C3F5 already proves the exact installed-V81 entrance numbering and opposite-side pairing predicate. C3F7/C3F8 prove Greenhouse's standard serialized inside-ID-1 fire-exit templates. C3F11/C3F12 prove the GlobalProp selection/removal and later SpawnSyncedProps consumption chain. C3F15 now supplies the missing strong generated Count-3 capacity condition.

Therefore **Black Mesa x GreenhouseFlow is statically cleared through the Count-3 entrance-topology layer**.

It is not yet fully cleared for the authoritative B3 viability matrix:

- C1 contains Greenhouse generation-only evidence on Offense with four entrance connections and no DunGen failure marker;
- C1 does not contain a recorded player entry/exit for Greenhouse;
- no repository-held evidence cited here proves Black Mesa x Greenhouse successful generation, player traversal, route accessibility or NavMesh behavior on the Black Mesa moon.

## Lifecycle consequence

- B3 matrix unchanged.
- S1.42AB InteriorWeightNormalization unchanged.
- Black Mesa remains Dawn/native-owned; no LLL duplicate registration.
- Shatteredrooms x Experimentation and x Embrion remain excluded.
- C3F10D restoration gaps remain closed to exhausted recovery techniques.
- No gameplay candidate is created.
- No build or runtime test is authorized in this checkpoint.
- Oxyde's separate false-generation boundary is unchanged.

## Next bounded checkpoint

Perform **C3F16 — Black Mesa x Greenhouse repository-held runtime-evidence sufficiency review**.

Search only existing authoritative runtime evidence for an actual Black Mesa-moon + `GreenhouseFlow` combination and evaluate whether it already proves successful generation, player traversal, entrance use, routing and NavMesh behavior. Do not perform a broad repository audit.

If that exact pair is not already covered, define the smallest remaining runtime proof obligation and candidate contract, but do not build or start gameplay in the same segment.
