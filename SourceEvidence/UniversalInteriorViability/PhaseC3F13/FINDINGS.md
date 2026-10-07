# C3F13 — repository-held generated-capacity feasibility ledger

**Status:** FEASIBILITY PASS COMPLETE / 0 OF 20 THREE-POSITIVE GENERATED LOWER BOUNDS PROVEN / NEXT EXACT DUNGEN GENERATION SURFACE IDENTIFIED / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-22  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Parent head:** `8bbd450d2b643a791770a7335d4428f730945224`

## Bounded objective

C3F13 performs the repository-held feasibility pass required by C3F12 before
creating another local capture.

It asks one question for the exact 20-flow C3F9/C3F12 proof set:

> Do the already captured flow graph, TileSet, candidate-source and serialized
> weight records establish a static lower bound of at least three **generated,
> eligible, positively weighted** ID-1231 candidates under Black-Mesa-sized
> generation?

The answer is **no for all 20 flows**. This is a proof-boundary result, not a
negative compatibility result.

`BackroomsFlow`, `CastleFlow` and `CircusFacilityFlow` remain outside this
set under C3F10D.

## Evidence revalidation

C3F13 re-read the committed C3F8 and C3F9 machine summaries and rehydrated only
the already existing GitHub Actions artifacts needed for this pass:

- C3F7 run `35537995994` / #4;
- C3F9 run `35569902534` / #2.

The seven C3F7 ZIP SHA-256 values used by the 17 direct flows matched the
artifact digests already recorded by C3F8. The Generic/Wesley/Storage C3F9 ZIPs
needed by `SHFlow`, `SpookyManorFlow` and `StorageComplex` likewise matched
the C3F9 committed digests.

The extracted `CAPTURE.json` and `GAP_CAPTURE.json` SHA-256 values matched the
hashes in the committed C3F8/C3F9 summaries. No package/game binary was added to
the repository.

Machine ledger:
`SourceEvidence/UniversalInteriorViability/PhaseC3F13/GENERATED_CAPACITY_FEASIBILITY_LEDGER.json`.

## Per-flow feasibility ledger

| Flow | Candidate path | Flow Length | Existing candidate source | Strongest existing asset-level capacity signal | Generated 3-positive lower bound |
|---|---|---:|---|---|---|
| `BunkerFlow` | direct tile descendant | 16..16 | 9 candidate-bearing tile roots / 17 memberships | 2 IsRequired=1 main-path injections; BunkerCheckpointSet is 2/2 candidate-bearing at normalized path-depth windows 0.35..0.40 and 0.65..0.70 | NOT PROVEN |
| `DrainsFlow` | direct tile descendant | 16..16 | 5 candidate-bearing tile roots / 13 memberships | candidate-bearing TileSets are mixed; no required injection and no candidate-only node/line surface | NOT PROVEN |
| `SubstationFlow` | direct tile descendant | 16..16 | 3 candidate-bearing tile roots / 10 memberships | SubstationFacilityTileset is mixed 3/10; no required injection | NOT PROVEN |
| `TowerFlow` | direct tile descendant | 4..4 | 3 candidate-bearing tile roots / 8 memberships | TowerRoomset is mixed 3/16; no required injection | NOT PROVEN |
| `AquaticDungeonFlow` | direct tile descendant | 6..8 | 7 candidate-bearing tile roots / 25 memberships | AquaticTempleSet 5/12 and AquaticCavesSet 3/15 are mixed | NOT PROVEN |
| `DeepSewersFlow` | direct tile descendant | 18..20 | 3 candidate-bearing tile roots / 5 memberships | candidate-bearing SewerCap/SewerStructure/SewerTunnelsSet are all mixed | NOT PROVEN |
| `FracturedComplexFlow` | direct tile descendant | 10..10 | 8 candidate-bearing tile roots / 41 memberships | MazeSet 1/5 and ComplexSet 7/12 are mixed | NOT PROVEN |
| `GreenhouseFlow` | direct tile descendant | 12..12 | 5 candidate-bearing tile roots / 19 memberships | Line 0 and line 2 use candidate-only CornSet 3/3; Goal uses candidate-only CornEnd 1/1 | NOT PROVEN |
| `MuseumInteriorFlow` | direct tile descendant | 6..6 | 3 candidate-bearing tile roots / 8 memberships | MuseumSet 2/9 and DMMuseumSet 3/7 are mixed | NOT PROVEN |
| `StoreFlow` | direct tile descendant | 12..17 | 11 candidate-bearing tile roots / 40 memberships | Goal uses candidate-only EndSet 1/1; all line TileSets remain mixed | NOT PROVEN |
| `ExpandedFacility` | direct tile descendant | 11..13 | 1 candidate-bearing tile root / 1 membership | only one source candidate root; all reachable candidate-bearing TileSets are mixed; depth curve includes a negative serialized key value | NOT PROVEN |
| `Level3ButCoolFlow` | direct tile descendant | 18..20 | 7 candidate-bearing tile roots / 17 memberships | Level3TunnelTiles is mixed 7/11; cave segment has 0 direct candidates | NOT PROVEN |
| `GrandArmoryFlow` | direct tile descendant | 9..9 | 21 candidate-bearing tile roots / 52 memberships | high candidate ratios but ArmoryHallSet, SmokeHallsSet and AcidHallsSet are all mixed | NOT PROVEN |
| `RubberRoomsFlow` | direct tile descendant | 12..13 | 6 candidate-bearing tile roots / 10 memberships | AsylumSet is mixed 6/29; RubberRoomSet has 0 direct candidates | NOT PROVEN |
| `ToystoreFlow` | direct tile descendant | 10..11 | 12 candidate-bearing tile roots / 51 memberships | StoreSet/StoreSet 2/BackroomsSet are all mixed despite many candidate memberships | NOT PROVEN |
| `SlaughterhouseFlow` | direct tile descendant | 5..6 | 15 candidate-bearing tile roots / 44 memberships | Goal uses candidate-only GrinderRoomSet 1/1; one IsRequired=1 injection uses candidate-only ProcessingRoomSet 1/1 at normalized path depth 0.30..0.60 | NOT PROVEN |
| `Black Mesa` | direct tile descendant | 25..25 | 102 candidate-bearing tile roots / 102 memberships | very high candidate ratios; Office Cap Test 5/5 and Lab Cap Test 7/7 are candidate-only branch-cap sets, but line archetype choice and branch/cap placement semantics remain unproven | NOT PROVEN |
| `SHFlow` | Doorway blocker indirection | 11..11 | 2 target-flow indirect candidate assets / 74 positive-weight exact Doorway blocker links | blocker links have positive serialized weight 1, but candidate materialization is conditional on Doorway blocker selection | NOT PROVEN |
| `SpookyManorFlow` | Doorway blocker indirection | 8..11 | 3 target-flow indirect candidate assets / 36 positive-weight exact Doorway blocker links | three candidate assets exist and all blocker links have positive weight 1, but actual selected blocker count is not proven | NOT PROVEN |
| `StorageComplex` | Doorway blocker indirection | 10..10 | 1 target-flow indirect candidate asset / 43 positive-weight exact Doorway blocker links | one candidate asset is referenced with positive blocker weights 0.2,0.3,0.4,3,5,10,20,100; repeated materialization is not guaranteed | NOT PROVEN |

## Why the existing data stops here

The captures establish far more than simple prefab counts:

- exact `DungeonFlow.Length`, `BranchCount`, Nodes and Lines;
- exact DungeonArchetype → TileSet relations;
- exact TileSet tile entries and their serialized main/branch tile weights;
- exact direct ID-1231 tile membership for 17 flows;
- exact positive-weight DunGen Doorway blocker links for the other three flows;
- exact ID-1231 `MainPathWeight`, `BranchPathWeight` and
  `DepthWeightScale` inputs.

But they do **not** capture the exact installed DunGen rules that turn those
asset declarations into a concrete generated tile sequence.

That prevents a rigorous lower-bound proof in several distinct ways:

1. a source TileSet containing candidate tiles does not prove any such tile is
   selected in a concrete layout;
2. `DungeonFlow.Length` plus non-zero Line lengths do not by themselves prove
   the exact integer number of placements allocated to each Line;
3. `IsRequired=1` is a strong serialized declaration, but the exact injection
   placement/failure behavior has not yet been captured;
4. branch counts and candidate-only branch-cap sets do not prove which
   archetypes/branches/caps are actually instantiated;
5. tile repeat/reuse restrictions are not present in the C3F7/C3F9 evidence;
6. C3F11 proves `ProcessGlobalProps` evaluates
   `Tile.Placement.NormalizedDepth`, but the exact `NormalizedDepth`
   derivation used for main versus branch tiles is not captured;
7. for `SHFlow`, `SpookyManorFlow` and `StorageComplex`, a candidate is
   reached through positive-weight `DunGen.Doorway.BlockerPrefabWeights`.
   Positive weight proves possibility, not that the blocker prefab is actually
   selected/materialized on enough generated doorways.

## Strongest current asset constraints

The pass does expose useful high-value cases for the next exact implementation
capture.

### BunkerFlow

Two separate `IsRequired=1` main-path injection rules both use
`BunkerCheckpointSet`, and that TileSet is 2/2 direct ID-1231 candidate-bearing
tiles. Their path-depth windows are 0.35..0.40 and 0.65..0.70.

If exact installed DunGen proves one successful placement per required injection,
this would establish two generated candidate-bearing tiles before considering the
ordinary line/goal selections. It still does not establish the required third
candidate from current evidence.

### GreenhouseFlow

Line 0 and Line 2 each use `CornArchetype` whose `CornSet` is 3/3
candidate-bearing. The Goal uses candidate-only `CornEnd` 1/1.

This is the strongest apparent three-surface asset pattern, but the missing rule
is precisely how `Length=12` is discretized across Lines and how Nodes are
placed. C3F13 therefore does not silently convert the serialized graph into three
runtime placements.

### SlaughterhouseFlow

The Goal uses candidate-only `GrinderRoomSet` 1/1 and one
`IsRequired=1` injection uses candidate-only `ProcessingRoomSet` 1/1 at
normalized path depth 0.30..0.60.

As with Bunker, exact Node and required-injection placement semantics are still
needed; the remaining ordinary line sets are mixed.

### Black Mesa

Black Mesa has 102 direct candidate-bearing tile roots and very high candidate
ratios in several main TileSets. `Office Cap Test` is 5/5 candidate-bearing and
`Lab Cap Test` is 7/7 candidate-bearing.

Those counts make capacity plausible, but they do not produce a lower bound
because the exact line-archetype and branch/cap selection path is still missing.

## Weight boundary

All 20 flows have positive serialized main/branch base weights on the proven
candidate surfaces, but the depth multiplier remains relevant.

Most captured profiles have a `DepthWeightScale` key at depth 0 with value 0.
`ExpandedFacility` is especially important because its serialized depth curve
contains an intermediate key value of approximately `-0.002704`.

C3F11 therefore cannot treat "candidate GameObject exists" as equivalent to
"candidate has positive effective selection weight". The exact generated
`NormalizedDepth` value is part of the remaining proof.

## Smallest next exact installed-DunGen surface

A new full DunGen decompile is unnecessary.

For the 17 direct flows, the smallest common capture surface is:

1. the `DunGen.DungeonGenerator` method cluster that consumes
   `DungeonFlow.Length`, `Lines`, `Nodes`, DungeonArchetypes and TileSets to
   create the concrete main path;
2. the immediate tile-choice/placement helper(s) that consume
   `TileSet.TileWeights` and enforce repeat/reuse restrictions;
3. the `TileInjectionRules` / `IsRequired` placement path;
4. the branch-generation/cap path where branch candidates can contribute;
5. the exact type/property implementing `Tile.Placement.NormalizedDepth`.

For the three C3F9 indirect-positive flows, add only:

6. the `DunGen.Doorway` method(s) that consume
   `BlockerPrefabWeights` and select/materialize blocker prefabs.

The next helper should locate those roots by the exact member signals above and
include only one-hop same-type callers/callees needed to make their control flow
self-contained. It should not re-capture `ProcessGlobalProps`,
`GameObjectChanceTable.GetRandom`, or `RoundManager.SpawnSyncedProps`; those
are already closed by C3F11/C3F12.

## Lifecycle consequence

No B3 cell changes.

The matrix remains 662 `VIABLE_EQUAL_100`, 14
`AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0
`KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`.

S1.42AB InteriorWeightNormalization remains unchanged. Black Mesa remains
Dawn/native-owned. Shatteredrooms × Experimentation and × Embrion remain
excluded.

No gameplay build or runtime test is authorized.

## Next bounded segment

Implement and CI-validate one fail-closed focused helper for the exact installed
DunGen generation-capacity surface identified above.

The helper must remain source-evidence-only and must publish no binary or full
type decompile. Do not ask the user for another local capture until that helper's
Windows PowerShell 5.1 self-test/bootstrap CI is green on an exact PR head.
