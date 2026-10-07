# C3F8 — C3F7 exact-head capture ingestion and Black Mesa count-3 static boundary

**Status:** 23/23 GLOBALPROP-1231 PRESENT / 17 STANDARD TEMPLATE SURFACES PROVEN / 6 STATIC TEMPLATE GAPS REMAIN / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-21  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Source capture head:** `1155f76a67fccf63cc3bd7fc510bbdb0d4175381`

## Bounded objective

C3F8 ingests the seven successful C3F7 derived artifacts and answers only the
static asset questions left by C3F6/C3F7:

- which of the 23 selection-supported Black Mesa-row flows actually serialize
  DungeonFlow GlobalProp ID `1231`;
- which of those flows expose a flow-reachable standard fire-exit template with
  an inside-side `EntranceTeleport` whose serialized pre-numbering ID is `1`;
- which exact static gaps remain before a three-fire-exit Black Mesa topology can
  be considered further.

This checkpoint does not perform gameplay compatibility analysis and does not
promote the B3 matrix.

## Exact-head artifact provenance

The ingested workflow is `Capture C3F7 GlobalProp asset evidence`, run
`35537995994` / #4 / attempt 1, conclusion **SUCCESS**, on exact PR head
`1155f76a67fccf63cc3bd7fc510bbdb0d4175381`.

All seven artifact ZIP SHA-256 values independently match the GitHub artifact
digests. Every `CI_PROVENANCE.json` binds the same repository, run and exact
head. The durable compact machine ingest is
`SourceEvidence/UniversalInteriorViability/PhaseC3F8/CAPTURE_INGEST_SUMMARY.json`.

No package, bundle or game binary is committed by this ingest.

## GlobalProp 1231 result

All **23/23** target DungeonFlows contain exactly one readable GlobalProp-table row
with ID `1231`.

There are:

- **17** `PROP_AND_TEMPLATE_PROVEN`;
- **6** `PROP_PRESENT_TEMPLATE_UNRESOLVED`;
- **0** `PROP_1231_ABSENT`;
- **0** `CAPTURE_UNRESOLVED`;
- **0** fatal capture ambiguities.

The 22 direct-LLL flows serialize ID-1231 Count `Min=1, Max=1`. Native Black
Mesa serializes `Min=4, Max=4`. C3F4/C3F5 already establish that Dawn rewrites
the selected flow's ID-1231 count to the active moon's alternate-entrance count;
for Black Mesa that target count is three. The packaged Black Mesa `4..4` value
therefore is not treated as a hard static prohibition, but this checkpoint also
does **not** infer that count-three generation is guaranteed.

## Seventeen standard template surfaces proven

The following flows have flow-reachable ID-1231 GlobalProp components whose every
captured template resolves through an explicit
`SpawnSyncedObject.spawnPrefab` reference to exactly one serialized
inside-side `EntranceTeleport` with pre-numbering `entranceId=1`:

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

This proves the narrow static template predicate required by C3F5. It does not
prove how many eligible instances exist in a particular generated layout or that
three are actually spawned.

One important example is `ExpandedFacility`: its source graph exposes one
flow-reachable ID-1231 template, but generated tiles can repeat. Conversely,
counting source templates greater than three does not prove that any specific
runtime layout contains three eligible instances. Source-template cardinality is
therefore not used as count-three capacity evidence.

## Six unresolved static template surfaces

| Flow | Exact C3F8 gap |
|---|---|
| `BackroomsFlow` | 15 flow-reachable ID-1231 components each point to an object named EntranceTeleportB; the spawned root exposes two null-script MonoBehaviours plus Unity.Netcode.NetworkObject, but no readable EntranceTeleport discriminator fields, so class/ID/side identity is not proven |
| `SHFlow` | GlobalProp table contains ID 1231, but current exact flow graph resolves zero flow-reachable ID-1231 components; 17 package-wide ID-1231 component(s) exist in the same bundle and cannot be borrowed without an exact ownership/path link |
| `CircusFacilityFlow` | GlobalProp table contains ID 1231, but current exact flow graph resolves zero flow-reachable ID-1231 components; 2 package-wide ID-1231 component(s) exist in the same bundle and cannot be borrowed without an exact ownership/path link |
| `SpookyManorFlow` | GlobalProp table contains ID 1231, but current exact flow graph resolves zero flow-reachable ID-1231 components; 3 package-wide ID-1231 component(s) exist in the same bundle and cannot be borrowed without an exact ownership/path link |
| `CastleFlow` | GlobalProp table contains ID 1231, but current exact flow graph resolves zero flow-reachable ID-1231 components; 2 package-wide ID-1231 component(s) exist in the same bundle and cannot be borrowed without an exact ownership/path link |
| `StorageComplex` | GlobalProp table contains ID 1231, but current exact flow graph resolves zero flow-reachable ID-1231 components; 1 package-wide ID-1231 component(s) exist in the same bundle and cannot be borrowed without an exact ownership/path link |

`BackroomsFlow` is especially narrow: all 15 flow-reachable ID-1231 components
do lead through `spawnPrefab` to the same serialized root named
`EntranceTeleportB`, but that root contains two MonoBehaviours whose
`m_Script` pointers are literally null plus a known Netcode `NetworkObject`.
The readable null-script type trees do not expose `entranceId`,
`isEntranceToBuilding` or another exact target discriminator. The object name
is suggestive but is not sufficient to convert it into an EntranceTeleport proof.

For `SHFlow`, `CircusFacilityFlow`, `SpookyManorFlow`, `CastleFlow` and
`StorageComplex`, the DungeonFlow table itself has ID 1231 but the exact current
flow -> archetype/TileSet -> tile hierarchy traversal reaches no ID-1231
GlobalProp component. Same-bundle package-wide candidates exist, but package
co-location is not an ownership link and is deliberately not used as proof.

## Remaining count-three proof obligations

For the 17 static-positive flows, C3F8 still does not establish the dynamic
count-three behavior required for Black Mesa. The next proof layer must establish
the exact DunGen/owner semantics that consume a runtime ID-1231 Count of three:

1. how the installed DunGen runtime selects GlobalProp instances for a Count of
   three, including behavior when the generated layout exposes fewer than three
   eligible instances;
2. whether one selected ID-1231 GlobalProp executes the captured
   `SpawnSyncedObject.spawnPrefab` path exactly once for this generation stage;
3. whether the generated Black Mesa-sized layout for a given flow can actually
   supply three eligible ID-1231 instances rather than merely containing one or
   more source templates;
4. that the resulting inside teleports exist in time for the already proven V81
   `SetExitIDs` numbering path and preserve unique opposite-side IDs 1..3;
5. later, before any universal compatibility promotion, actual generation,
   traversal, accessible geometry, routing and NavMesh safety.

The six unresolved flows have an earlier obligation: recover an exact serialized
or owner/runtime link for their fire-exit template before they can even enter the
same count-three proof set.

## Matrix and lifecycle consequence

No B3 cell changes from C3F8. The authoritative matrix remains:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`.

S1.42AK remains accepted/latest. No gameplay candidate or runtime test is armed.
`BuildSpecs/current.json` stays disabled at
`IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, and
`RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

## Next bounded segment

Resolve the six static-template gaps first, without a gameplay run:

- for Backrooms, determine whether the two null-script components on the exact
  `EntranceTeleportB` prefab can be authoritatively rebound to the expected
  game component identities through the installed owner/loader serialization
  path;
- for SHFlow, CircusFacilityFlow, SpookyManorFlow, CastleFlow and StorageComplex,
  trace the same-bundle ID-1231 candidates and any owner/loader indirection that
  can establish or reject exact flow membership.

Do not borrow package-wide props by name/proximity, do not promote matrix cells,
and do not start a gameplay build or runtime test from C3F8 alone.
