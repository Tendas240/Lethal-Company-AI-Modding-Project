# C3F10C — installed V81 NetworkConfig / EntranceTeleportB registry proof boundary

**Status:** OWNER RECOVERY UNRESOLVED / TARGET NOT EVALUATED / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-21  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Capture evidence head:** `036715943be0e964104a9d5546e5ca61a6eba607`  
**Capture parent / scanner source head:** `08729490c6853c3644e51221c73ab96e97aa7786`

## Bounded objective

C3F10C asks one narrow installed-V81 question:

> Is a prefab with the exact GameObject name `EntranceTeleportB` registered in the
> exact installed `Unity.Netcode.NetworkManager.NetworkConfig` prefab registry, and
> does that registered prefab carry the exact component surface
> `EntranceTeleport`, `InteractTrigger`, and `Unity.Netcode.NetworkObject`?

A GameObject name, similar prefab, runtime clone, package co-location, or component
identity inferred from a name is not sufficient. Positive proof requires the target
to be reached through the proven serialized NetworkManager -> NetworkConfig prefab
registry path.

## Evidence and provenance

Persistent installed-V81 evidence is published at:

`SourceEvidence/VanillaV81/NetworkConfigEntranceTeleportB/20260921T190943Z-c89cb708/`

The evidence commit has exactly one parent:
`08729490c6853c3644e51221c73ab96e97aa7786`.

The manifest binds the capture to:

- repository main at capture:
  `56355ff518ae4301a38d370be9561251f6f963c1`;
- exact `Assembly-CSharp.dll` SHA-256:
  `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- exact `Unity.Netcode.Runtime.dll` SHA-256:
  `dd5313b862c66f048139ff8e459d681bee2861c8b39c8dd50cc4d7851b4c32a2`;
- exact game executable SHA-256:
  `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam App ID `1966720`, Build ID `22825947`, reviewed appmanifest SHA-256
  `132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e`;
- scanner blob
  `07a565dace759e202871bf966e6f07dfa7ad8ffb`;
- capture schema `v81-networkconfig-entranceteleportb-9`.

The capture contains no game binary, Unity asset payload, full managed decompile,
absolute local path, or user name.

## Exact Netcode metadata facts

The exact installed `Unity.Netcode.Runtime.dll` parses without metadata/IL errors
for the focused evidence surface.

The capture confirms the exact managed identities needed by the scanner are present:

- `Unity.Netcode.NetworkManager`;
- `Unity.Netcode.NetworkConfig`;
- `Unity.Netcode.NetworkPrefab`;
- `Unity.Netcode.NetworkPrefabs`;
- `Unity.Netcode.NetworkPrefabsList`.

It also confirms the exact NetworkManager NetworkConfig field and the relevant
Netcode prefab-storage field surface are present.

These managed metadata facts establish the type/field model only. They do **not**
by themselves prove which serialized NetworkManager instance owns the installed
NetworkConfig or which prefab entries are registered in that instance.

## Serialized asset scan

The capture scans 41 installed serialized files containing 140,012 objects,
including 10,279 MonoBehaviours.

Normal serialized script resolution succeeds for 656 relevant MonoBehaviour
descriptors. Exactly 185 MonoBehaviours remain unresolved.

All 185 unresolved objects share the same fail-closed identity state:

- class ID 114;
- `script_type_index = -1`;
- serialized `script_id = ZERO`;
- serialized `old_type_hash = ZERO`;
- no embedded TypeTree;
- no raw structural NetworkConfig hit.

There are:

- zero raw structural NetworkConfig candidates;
- zero proven-owner structural NetworkConfig candidates;
- zero previously proven NetworkManager-owner candidates.

Therefore none of the normal serialized identity channels establishes the exact
NetworkManager owner.

## Exact generated NetworkManager TypeTree probe

The previous dependency-resolution failure is closed.

The scanner loaded the exact installed Managed DLL set as static TypeTree inputs
(167 DLLs, including `netstandard.dll`) and successfully generated the exact
`Unity.Netcode.NetworkManager` TypeTree:

- `generation_error = null`;
- generated assembly = `Unity.Netcode.Runtime.dll`;
- generated type = `Unity.Netcode.NetworkManager`.

That exact generated layout was then applied only to the 185 unresolved
null-script MonoBehaviours with UnityPy full-read checking enabled.

Result:

- candidate count: **0**;
- parse failures: **185**;
- failure type: **185 × EOFError**;
- successful full reads without an exact structured NetworkConfig: **0**.

No unresolved MonoBehaviour therefore qualifies as a structurally proven
NetworkManager owner under the capture contract.

## C3F10C result

The persistent capture intentionally reports:

- `analysis_status = OWNER_RECOVERY_UNRESOLVED`;
- `target_status = null`;
- `target_surface = null`.

This is a diagnostic proof boundary, not a negative registry result.

C3F10C therefore does **not** establish any of the following:

- that `EntranceTeleportB` is registered;
- that `EntranceTeleportB` is not registered;
- that an exact-name registered entry is unique or ambiguous;
- that the registered target has or lacks `EntranceTeleport`;
- that the registered target has or lacks `InteractTrigger`;
- that the registered target has or lacks `Unity.Netcode.NetworkObject`.

In particular, empty registry-output collections in this capture must not be
interpreted as `EXACT_NAME_NOT_REGISTERED`, because the owning NetworkConfig
instance was never proven.

## Static proof boundary

The currently established serialized-owner recovery channels have been exhausted
for this capture:

1. ordinary object `m_Script` resolution;
2. SerializedType `script_type_index`;
3. SerializedType `script_id`;
4. SerializedType `old_type_hash`;
5. embedded TypeTree recovery;
6. exact generated `Unity.Netcode.NetworkManager` TypeTree full-read probing.

The final failure mode is no longer missing TypeTree dependencies. The exact
NetworkManager TypeTree is generated successfully, but none of the 185 identityless
serialized MonoBehaviours can be read as that layout.

A future static attempt is justified only if it introduces an independent,
authoritative source for the actual installed NetworkConfig registry or owner
identity. Repeating the same null-script/script-ID/type-hash/TypeTree strategies
with cosmetic variations is not evidence progress.

## Relationship to C3F9 / C3F10 / C3F10B

C3F10C does not invalidate the earlier exact package/reference-restoration work.
It also does not upgrade that work into a registry proof.

BackroomsFlow, CastleFlow and CircusFacilityFlow therefore remain subject to the
previously identified reference-restoration and integration boundaries. Any final
static conclusion for those three flows must reconcile C3F9, C3F10,
C3F10B, the installed-V81 entrance-pairing evidence, and this C3F10C boundary
without inventing NetworkConfig registration or component identity.

## Lifecycle guard

No B3 matrix cell is changed.

The matrix remains:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`.

S1.42AB InteriorWeightNormalization remains unchanged. Black Mesa native/Dawn
registration remains single-owned. Shatteredrooms × Experimentation/Embrion
remain excluded. No gameplay build or runtime test is authorized.

## Next bounded segment

Reconcile only the already-established static evidence for the three remaining
reference-restoration flows:

- C3F9 package/template findings;
- C3F10 DunGenReferenceFixer evidence;
- C3F10B LLL restoration evidence;
- exact installed-V81 entrance-pairing evidence;
- this C3F10C NetworkConfig proof boundary.

Determine separately for BackroomsFlow, CastleFlow and CircusFacilityFlow whether
the combined static chain closes a valid entrance-template/restoration statement,
or whether each must remain at an explicit static proof boundary.

Do not promote B3, build a gameplay candidate, request a runtime test, or start
another local NetworkConfig capture solely from C3F10C.
