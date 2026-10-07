# C3F10D — three-flow restoration synthesis and static proof boundary

**Status:** THREE-FLOW STATIC SYNTHESIS COMPLETE / RESTORATION CONDITION PROVEN / TARGET REGISTRY UNRESOLVED / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-21  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Parent PR head:** `7de6b7886a168585bf8b22f8c529b4eae2ef9ae9`

## Bounded objective

C3F10D performs no new package capture and no new NetworkConfig owner-recovery attempt.

It reconciles only the already-established static evidence for the three C3F9
reference-restoration gaps:

- `BackroomsFlow`;
- `CastleFlow`;
- `CircusFacilityFlow`.

The synthesis is bounded to:

1. C3F9 exact flow / GlobalProp / spawned-prefab membership;
2. exact accepted `Zaggy1024-DunGenReferenceFixer 0.0.1` managed-IL evidence from
   exact-head workflow run #24;
3. exact accepted `IAmBatby-LethalLevelLoader 1.7.12` restoration managed-IL
   evidence from exact-head workflow run #19;
4. installed-V81 `RoundManager.SetExitIDs` and
   `EntranceTeleport.FindExitPoint` semantics;
5. C3F10C's installed-V81 NetworkConfig / `EntranceTeleportB` proof boundary.

No component identity is inferred from a GameObject name. No NetworkConfig
registration is inferred from package co-location, a runtime clone, or a similarly
named prefab.

## Exact-head evidence binding

The synthesis uses parent PR head
`7de6b7886a168585bf8b22f8c529b4eae2ef9ae9`.

At that head:

- `Capture C3F10 DunGenReferenceFixer evidence` run #24 /
  run ID `35643993588` completed **SUCCESS**;
- its exact-head capture artifact is ID `10658864776`,
  digest `sha256:9d595ab15be57731d3537f89e2f0d898fb62c9448765f692eaf23d02d041eb18`;
- `Capture C3F10B LLL restoration evidence` run #19 /
  run ID `35643993159` completed **SUCCESS**;
- its exact-head capture artifact is ID `10659159201`,
  digest `sha256:fa31b174fa35f736adc165aa875546a06f23e418cfa20a777adc7b00c6b9a9d4`.

Both capture jobs explicitly checked out and bound
`7de6b7886a168585bf8b22f8c529b4eae2ef9ae9` before producing their derived JSON.

## What DunGenReferenceFixer actually proves

The exact accepted `DunGenReferenceFixer.dll` is a BepInEx patcher.

Its relevant managed path patches Unity's serialized managed-class resolution so
that stale DunGen component references which still point at `Assembly-CSharp`
can be redirected to the `DunGen` assembly when the serialized namespace is
`DunGen` or a DunGen subnamespace.

This establishes a narrow assembly-reference repair mechanism.

It does **not** establish a general prefab replacement mechanism and does not
prove that the patcher:

- creates `EntranceTeleport`;
- creates `InteractTrigger`;
- creates `NetworkObject`;
- assigns `entranceId`;
- assigns `isEntranceToBuilding`;
- replaces a `SpawnSyncedObject.spawnPrefab` by GameObject name;
- reconstructs identityless null-script MonoBehaviours into a named game component.

Therefore DunGenReferenceFixer does not by itself close any of the three C3F9
gaps.

## What LethalLevelLoader restoration actually proves

Exact accepted LethalLevelLoader 1.7.12 does contain a separate
`SpawnSyncedObject` prefab-restoration path.

During dungeon-content network registration it attempts to restore a
`SpawnSyncedObject.spawnPrefab`. The relevant restoration path searches the
active NetworkManager NetworkConfig prefab collection and compares prefab names
with an exact ordinal string comparison.

If an exact registered target is found, LLL can replace the stale/original
`spawnPrefab` reference with that registered network prefab.

This is a real generic prefab-restoration mechanism.

However, this mechanism is conditional. The LLL managed IL does **not** prove
that a specific `EntranceTeleportB` target is actually registered in the
installed active NetworkConfig, nor does it prove the target component surface.

If no suitable registered prefab is found, the evidence does not establish that
LLL synthesizes the missing `EntranceTeleport` / `InteractTrigger` surface.
The fallback network-registration behavior for the original prefab is not a
substitute for proving entrance functionality.

## Installed-V81 pairing semantics

The exact installed V81 evidence establishes the semantics that would apply
*after* a valid `EntranceTeleport` surface exists.

`RoundManager.SetExitIDs`:

- finds all `EntranceTeleport` objects;
- considers inside-side entries whose pre-numbering `entranceId == 1` and
  `isEntranceToBuilding == false`;
- orders the full entrance set by distance from the main entrance;
- assigns qualifying inside-side fire exits sequential IDs beginning at 1.

`EntranceTeleport.FindExitPoint` pairs an entrance only with an
`EntranceTeleport` that has:

- the opposite `isEntranceToBuilding` side; and
- the same `entranceId`.

These methods do not create missing entrance components and do not use the
GameObject name as pairing identity.

## Flow synthesis

### BackroomsFlow

C3F9 proves all 15 flow-reachable ID-1231 GlobalProps lead through
`SpawnSyncedObject.spawnPrefab` to a serialized root named
`EntranceTeleportB`.

That root contains two 32-byte null-script MonoBehaviour objects whose serialized
identity channels are unavailable:

- `script_type_index = -1`;
- all-zero script ID;
- all-zero old type hash;
- no usable serialized class binding.

The components cannot be promoted to `EntranceTeleport`,
`InteractTrigger`, or another specific type from the GameObject name.

DunGenReferenceFixer does not close this because no authoritative stale
`DunGen.*` class identity is established for those identityless components.

LLL provides a possible whole-prefab replacement route **if** an exact-name
`EntranceTeleportB` network prefab exists in the active NetworkConfig.

C3F10C could not prove the owning NetworkConfig and therefore intentionally
reports:

- `analysis_status = OWNER_RECOVERY_UNRESOLVED`;
- `target_status = null`;
- `target_surface = null`.

**BackroomsFlow result:** static chain **not closed**. The concrete remaining
boundary is the authoritative existence and component surface of the active
NetworkConfig `EntranceTeleportB` restoration target.

### CastleFlow

C3F9 proves both relevant same-bundle ID-1231 candidates are members of
CastleFlow through positive-weight exact `DunGen.Doorway` blocker references.

Their `SpawnSyncedObject.spawnPrefab` points to a serialized GameObject named
`EntranceTeleportB`, but the exact captured spawned root contains only a
`Transform`.

DunGenReferenceFixer cannot create an entrance surface from that Transform-only
root under the proven patch contract.

LLL can replace that whole prefab only if the exact corresponding network prefab
is already registered in the active NetworkConfig.

C3F10C does not prove that registration.

**CastleFlow result:** static chain **not closed**. Flow/GlobalProp membership is
proven; the remaining boundary is the active NetworkConfig restoration target
and its required entrance component surface.

### CircusFacilityFlow

C3F9 likewise proves both relevant ID-1231 candidates are members of
CircusFacilityFlow through positive-weight exact `DunGen.Doorway` blocker
references.

The shared serialized `EntranceTeleportB` spawned root is also Transform-only.

The same boundaries therefore apply:

- DunGenReferenceFixer does not synthesize the missing entrance surface;
- LLL has a conditional whole-prefab restoration mechanism;
- the required active NetworkConfig target is not proven by C3F10C.

**CircusFacilityFlow result:** static chain **not closed**. Membership is proven,
but successful entrance-prefab restoration remains unproven.

## Combined result

The three flows remain distinct from the 20 C3F9 static-positive
standard-template flows.

C3F10D proves a meaningful restoration **condition**:

> If the active installed NetworkConfig contains the exact-name registered
> network prefab needed by LLL, LLL has a managed path capable of replacing the
> stale/original `SpawnSyncedObject.spawnPrefab`.

It does not prove that the condition is satisfied for
`EntranceTeleportB`.

Therefore BackroomsFlow, CastleFlow and CircusFacilityFlow must not be promoted
into the 20-flow static-positive set from the current evidence.

A future positive registry proof would close only this earlier restoration
boundary. It would not by itself close the separate DunGen Count-3 generation
obligation.

## C3F10C stopping rule

Do **not** start another C3F10C-style trial-and-error capture using the already
exhausted owner-recovery ideas:

- ordinary `m_Script`;
- SerializedType `script_type_index`;
- script ID;
- old type hash;
- embedded TypeTree;
- generated NetworkManager TypeTree applied to the same identityless objects.

A new static registry attempt is justified only by an independent authoritative
source for the actual active NetworkConfig owner or registry contents.

## Lifecycle consequence

No matrix cell changes.

The authoritative B3 totals remain:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`.

S1.42AB InteriorWeightNormalization remains unchanged.

Black Mesa remains single-owned through its native/Dawn path. No duplicate LLL
registration is introduced.

Shatteredrooms × Experimentation and Shatteredrooms × Embrion remain excluded.

No gameplay build or runtime test is authorized.

## Next bounded segment

Proceed independently with the **20 C3F9 static-positive Black-Mesa-row flows**.

Resolve the common DunGen GlobalProp-1231 **Count-3 generation semantics**:
determine, from authoritative static implementation evidence first, how an
effective count of three selects/instantiates the qualifying fire-exit templates
and whether the generated layout can supply three inside-side pre-numbering
ID-1 `EntranceTeleport` instances before installed V81 `SetExitIDs` assigns
IDs 1..3.

Keep BackroomsFlow, CastleFlow and CircusFacilityFlow outside that 20-flow proof
set unless an independent authoritative NetworkConfig restoration source later
closes their earlier boundary.

Do not change B3, author a gameplay candidate, build, or request a runtime test
solely from this checkpoint.
