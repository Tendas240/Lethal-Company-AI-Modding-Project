# C3F9 — unresolved fire-exit template gap attribution

**Status:** 20/23 STATIC STANDARD TEMPLATE SURFACES PROVEN / 3 REFERENCE-RESTORATION GAPS REMAIN / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-21  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Source probe head:** `caec94a2acdb0b1d6094788f449fd7ab3e23513a`

## Bounded objective

C3F9 follows only the six unresolved C3F8 flows. It reuses the exact C3F7
package lock/acquisition path and performs two fail-closed checks:

1. whether a same-bundle ID-1231 GlobalProp omitted by direct
   flow -> TileSet -> tile hierarchy traversal is nevertheless linked to a
   **target-flow-owned exact `DunGen.Doorway`** through a positive-weight
   serialized `BlockerPrefabWeights[n].GameObject` reference; and
2. whether Backrooms' two null-script components can be rebound from serialized
   type metadata/raw layout to known same-package game component layouts.

Names and package co-location are never enough for a positive result.

## Exact-head validation

`Capture C3F9A unresolved template-gap evidence` run
`35569902534` / #2 completed **SUCCESS** on source head
`caec94a2acdb0b1d6094788f449fd7ab3e23513a`: the helper self-test and all five exact-package matrix jobs
succeeded. The source head's Knowledge Architecture, C3F7, Black Mesa topology,
Black Mesa DLL, V81 generation, V81 spawning and V81 entrance-pairing workflows
also completed successfully.

Artifact IDs, GitHub digests and the SHA-256 of each derived `GAP_CAPTURE.json`
are preserved in `STATIC_GAP_SUMMARY.json`.

## Three C3F8 gaps are statically closed

### SHFlow

The package contains 17 same-bundle ID-1231 candidates not found by C3F8's direct
tile-descendant walk. Fifteen belong directly to Backrooms and are not borrowed.
Exactly **two** candidates are instead linked from SHFlow's own tile hierarchy by
positive-weight exact `DunGen.Doorway.BlockerPrefabWeights[n].GameObject`
references.

Both candidate GlobalProps spawn the same serialized `EntranceTeleportB`
template. Its exact component surface includes `InteractTrigger`,
`EntranceTeleport` and `NetworkObject`; the captured EntranceTeleport is
inside-side with pre-numbering ID 1. Both templates therefore satisfy the narrow
standard-template predicate.

### SpookyManorFlow

All **three** same-bundle candidates are linked from Spooky Manor's exact tile
hierarchy through positive-weight exact DunGen Doorway blocker entries. All three
resolve to a complete serialized `EntranceTeleportB` surface with one
inside-side pre-numbering ID-1 `EntranceTeleport`.

### StorageComplex

The single same-bundle candidate is linked from StorageComplex tile Doorways
through **43** positive-weight serialized blocker references. The weights vary,
but every accepted edge is positive. The linked GlobalProp resolves to a complete
`EntranceTeleportB` surface with one inside-side pre-numbering ID-1
`EntranceTeleport`.

These three flows join the 17 C3F8 direct positives. The current narrow static
template-proof set is therefore **20/23** selection-supported Black-Mesa-row
flows.

## Three static gaps remain

### BackroomsFlow — serialized component identity unavailable

All 15 flow-reachable ID-1231 props still lead through `spawnPrefab` to the
serialized root named `EntranceTeleportB`. The root has two null-script
MonoBehaviour objects. Both are only 32 bytes and serialize:

- MonoBehaviour class ID 114;
- `script_type_index = -1`;
- all-zero 16-byte script ID;
- all-zero 16-byte old type hash;
- no serialized script-type binding.

The same package contains eight exact known `EntranceTeleport` controls and 413
exact known `InteractTrigger` controls. Neither null component matches those
known classes by script-ID/type-hash fingerprint. Re-reading each null component
with known same-package EntranceTeleport and InteractTrigger typetrees fails
closed because the 32-byte payload is too short for either layout.

Therefore the GameObject name does not recover class identity, `entranceId` or
side. Backrooms remains unresolved pending an authoritative loader/reference
restoration mechanism.

### CastleFlow — membership proven, entrance surface absent

Both same-bundle ID-1231 candidates are now exactly attributed to CastleFlow
through target-flow `DunGen.Doorway` blocker entries with positive weight 1.
Their `SpawnSyncedObject.spawnPrefab` references point to a GameObject named
`EntranceTeleportB`, but that exact serialized spawned root contains **only a
Transform**. No EntranceTeleport/InteractTrigger/NetworkObject component surface
exists in the captured package object.

### CircusFacilityFlow — membership proven, entrance surface absent

Both same-bundle ID-1231 candidates are likewise exactly attributed to the Circus
flow through target-flow exact DunGen Doorway blocker entries with positive
weight 1. Their shared serialized `EntranceTeleportB` spawned root also
contains **only a Transform**.

The Castle and Circus findings are not interpreted as broken fire exits. They
narrow the remaining question to a loader/reference-restoration boundary: the
flow membership is proven, but the exact package asset does not itself serialize
the component surface required for the standard-template proof.

## Consequence for count-three proof

C3F9 changes no gameplay classification. The B3 matrix remains
662 / 14 / 0 / 0 / 914.

For the **20** static-positive flows, the common next obligation remains the
runtime DunGen Count-3 semantics identified by C3F8: prove how an effective
GlobalProp-1231 count of three selects/executes instances and whether a generated
layout can supply three usable fire-exit templates before V81 `SetExitIDs`
numbers them 1..3.

The **three** unresolved flows have one earlier gate. Before they enter that
common proof set, inspect the exact accepted reference-restoration/loader path
that could reconstruct missing component references. The accepted stack contains
`Zaggy1024-DunGenReferenceFixer 0.0.1`, but C3F9 makes **no claim** about its
implementation merely from its name or installation.

## Lifecycle guard

S1.42AK remains accepted/latest. No matrix cell is promoted, no universal
availability rule is implemented, no gameplay build is created and no runtime
test is requested. S1.42AB normalization and the Black Mesa native registration
remain untouched.

## Next bounded segment

Acquire and inspect the exact accepted `Zaggy1024-DunGenReferenceFixer 0.0.1`
package/binary and the relevant LLL/DunGen loading integration only as needed to
answer the three remaining restoration questions:

- can Backrooms' null-script `EntranceTeleportB` components be authoritatively
  reconstructed;
- is Castle's Transform-only `EntranceTeleportB` placeholder repaired into the
  expected game prefab/component surface;
- is Circus' equivalent Transform-only placeholder repaired likewise.

Fail closed if the exact restoration identity cannot be established. Do not move
to the Count-3 generation gate for those three flows unless this earlier static
restoration gate closes.
