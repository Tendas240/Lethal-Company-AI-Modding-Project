# C3F3 — exact BlackMesa.dll entrance-special-handling metadata and IL gate

**Status:** EXACT BLACKMESA.DLL STATIC IL + METADATA/HARMONY TARGET REVIEW COMPLETE / NO DIRECT DLL-LOCAL ENTRANCE REWRITE OR PAIRING PATH IDENTIFIED / C3F2 MOON-SIDE ID 2/3 ASYMMETRY NOT RECONCILED BY THIS DLL / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-20  
**Accepted baseline:** S1.42AK  
**Parent PR head:** `91e818c4297b64dd50632ad7ad307356e90e8d7d`  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded objective

C3F3 closes the exact-DLL question left open by C3F2:

**Does exact Black Mesa 3.4.4 `BlackMesa.dll` itself expose managed IL, bodyless external/native declarations, Harmony target metadata, reflection strings or module-internal abstract dispatch that creates/re-writes `EntranceTeleport` objects, changes entrance IDs/pairing, or otherwise explains the serialized Black Mesa moon-side IDs 2/3?**

This is a static exact-binary evidence checkpoint only. It does not change the authoritative B3 matrix and does not authorize a gameplay build or runtime test.

## Exact package and DLL identity

The inspection is bound to the same exact Black Mesa 3.4.4 package established by C3F2:

- package: `Plastered_Crab-Black_Mesa_Half_Life_Moon_Interior 3.4.4`;
- ZIP size: 228,214,268 bytes;
- ZIP SHA-256: `12921825bee51bfd46582989322a1f31183b65f59293c73654a102fb68d068b7`;
- DLL member: `BepInEx/plugins/BlackMesa.dll`;
- DLL size: 143,360 bytes;
- DLL SHA-256: `a90f157becdc68ab7fe6898eefc2feaee98352a0f04b2cda414741729a048eef`.

No mod assembly is loaded or executed. The helper uses pinned `dnfile 0.18.0` and `dncil 1.0.2`.

## Evidence chain

C3F3 consists of two complementary exact-DLL captures.

### Broad IL v2 capture

Successful workflow run:

- run ID: **35519633043**;
- run number: **2**;
- associated PR head: `348210d612438743fcf5ab9a118ed3fd789bf3a2`;
- artifact ID: **10607488800**;
- artifact name: `black-mesa-344-c3f3-602f408f131b9f9a0dcf8937ab93b98c351698de`;
- artifact digest: `sha256:9fc3d70fbff8bf33de861c1f5778e9e0a449c86f6dfed1612fc00960cd82f0d9`;
- report: `BLACK_MESA_344_DLL_ENTRANCE_IL.json`;
- report schema: `phase-c3f3-il-2`;
- report size: 550,163 bytes;
- report SHA-256: `fba034f97e67364374caa2a30e64d86a5a976c72b3db8c0baaacc6bd081e4638`.

The artifact-name suffix above is the historical workflow ref used by that older run; run binding is the provenance authority.

### Final metadata gate

Successful exact-HEAD workflow run:

- run ID: **35521903966**;
- run number: **6**;
- exact PR head: `91e818c4297b64dd50632ad7ad307356e90e8d7d`;
- artifact ID: **10608856431**;
- artifact name: `black-mesa-344-c3f3-metadata-91e818c4297b64dd50632ad7ad307356e90e8d7d`;
- artifact digest: `sha256:76a5b066e5d25d3f970ddad215b5dcda262497baa2254a89e2eb184c0301cb38`;
- report: `BLACK_MESA_344_METADATA_GATE.json`;
- report schema: `phase-c3f3-metadata-1`;
- report size: 103,783 bytes;
- report SHA-256: `fcf2a487f0af66d131c2967c57dc6b1eb5227900b6aa87847d9fa88554d06dbf`.

The final metadata report has `gate_status = METADATA_CAPTURE_COMPLETE_REVIEW_REQUIRED` and **zero blockers**. The green workflow is not used by itself as clearance; the report is reviewed together with the already-complete broad IL evidence below.

## Broad managed-IL coverage

The v2 IL report covers the complete RVA-bearing managed method surface of the exact DLL:

- TypeDefs: 91;
- MethodDefs with RVA scanned: **568**;
- methods without RVA: 8;
- IL instructions scanned: **14,095**;
- parse errors: **0**.

Directly identifiable entrance/pairing results:

- strong entrance-signal methods: **0**;
- direct entrance references: **0**;
- `entranceId` / `isEntranceToBuilding` / `entrancePoint` / `exitPoint` references: **0**;
- writes to those pairing fields: **0**;
- signal string literals: **1**.

The sole signal string is in `BlackMesa.Patches.PatchLungProp::DisconnectFromMachineryTranspiler`:

`Failed to patch DisconnectFromMachinery()`

It is not an entrance/fire-exit/pairing string.

The scan also records, rather than ignores, the DLL's dynamic-capable surface:

- 38 methods with component-creation and/or reflection calls;
- 51 creation/component references;
- 25 reflection references.

No directly identifiable captured target/string among those produces a strong entrance signal. This is bounded negative evidence, not a whole-program claim that arbitrary reflective behavior is impossible.

## Eight RVA-less MethodDefs

The metadata gate proves that the eight methods omitted from the RVA body scan are not hidden native/PInvoke/Runtime/InternalCall/ForwardRef bodies:

| Token | Declaration | Kind |
|---|---|---|
| `0x0600003f` | `BlackMesa.INightVisionCamera::get_Camera` | interface abstract declaration |
| `0x06000040` | `BlackMesa.INightVisionCamera::get_NightVisionLight` | interface abstract declaration |
| `0x060000a2` | `BlackMesa.Interfaces.IDumbEnemy::Stun` | interface abstract declaration |
| `0x060000a3` | `BlackMesa.Interfaces.IDumbEnemy::Kill` | interface abstract declaration |
| `0x06000202` | `BlackMesa.Components.StationBase::OnActivatedByPlayer` | abstract-class declaration |
| `0x06000206` | `BlackMesa.Components.StationBase::UpdateInteractabilityWithCapacity` | abstract-class declaration |
| `0x06000208` | `BlackMesa.Components.StationBase::DoActiveTick` | abstract-class declaration |
| `0x06000209` | `BlackMesa.Components.StationBase::OnActiveTickingEnded` | abstract-class declaration |

All eight have managed/IL implementation semantics, `abstract=true`, RVA 0, and no `ImplMap`. The exact DLL contains:

- **0** ImplMap rows;
- no PInvokeImpl on these declarations;
- no unmanaged/native/OPTIL classification;
- no Runtime/InternalCall;
- no ForwardRef;
- no UnmanagedExport.

The helper enumerates exact module-internal signature-compatible dispatch candidates for each declaration. Across the eight declarations there are **14 unique module-internal RVA body tokens**, and every one belongs to the already-complete 568-body v2 IL scan.

Therefore the eight no-RVA rows do not hide an unscanned implementation body inside `BlackMesa.dll`.

Implementations declared in other assemblies are explicitly **not** enumerated or claimed inspected. The conclusion is DLL-local only.

## HarmonyLib.MethodType blocker closure

The previous metadata attempt correctly failed closed on custom attribute token `0x0c0000ae` because external enum width/value semantics were not guessed.

The final helper pins the enum to version-matched HarmonyX evidence:

- assembly reference: `0Harmony, Version=2.7.0.0`;
- package: HarmonyX 2.7.0;
- release tag: `v2.7.0`;
- source commit: `253725768e59b0e1ea90105cdbcc4a0a477422c7`;
- source file: `Harmony/Public/Attributes.cs`;
- exact Git blob SHA-1: `636801ac53ff76eb3c9fc600e587569f2bf43910`;
- underlying type: `System.Int32`;
- permitted values: Normal=0, Getter=1, Setter=2, Constructor=3, StaticConstructor=4, Enumerator=5.

The previously unresolved Black Mesa attribute now decodes completely:

- attribute token: `0x0c0000ae`;
- parent: `BlackMesa.Patches.PatchLungProp::DisconnectFromMachineryTranspiler`;
- target method name: `DisconnectFromMachinery`;
- method type: **Enumerator (5)**.

No payload-width guess remains.

## Harmony target binding

The final metadata capture inspects 274 CustomAttribute rows and records:

- Black Mesa patch types: 10;
- scoped attributes: 46;
- HarmonyPatch attributes in the assembly: 27;
- scoped HarmonyPatch attributes: 27;
- decoded HarmonyPatch attributes: **27/27**;
- resolved Harmony target declarations: **19/19**;
- dynamic target resolvers: **0**;
- blockers: **0**.

Class-level and method-level `HarmonyPatch` fragments are combined only when they are fully decoded and non-contradictory. Every resolved patch method also has an RVA body covered by the broad v2 scan.

The 19 resolved declared targets are:

| Patch | Declared external target |
|---|---|
| `PatchAnimator.SetTriggerStringPostfix` | `UnityEngine.Animator::SetTriggerString` |
| `PatchAnimator.SetTriggerIDPostfix` | `UnityEngine.Animator::SetTriggerID` |
| `PatchAnimator.SetBoolStringPostfix` | `UnityEngine.Animator::SetBoolString` |
| `PatchAnimator.SetBoolIDPostfix` | `UnityEngine.Animator::SetBoolID` |
| `PatchDeadBodyInfo.SetRagdollPositionSafelyPostfix` | `DeadBodyInfo::SetRagdollPositionSafely` |
| `PatchDungeonGenerator.GenerateNewFloorPrefix` | `DunGen.DungeonGenerator::ChangeStatus` |
| `PatchEnemyAI.StartPostfix` | `EnemyAI::Start` |
| `PatchEnemyAI.OnDestroyPostfix` | `EnemyAI::OnDestroy` |
| `PatchLungProp.DisconnectFromMachineryTranspiler` | `LungProp::DisconnectFromMachinery` Enumerator |
| `PatchMenuManager.StartPostfix` | `MenuManager::Start` |
| `PatchNetworkManager.InitializePrefabsPostfix` | `Unity.Netcode.NetworkConfig::InitializePrefabs` |
| `PatchPlayerControllerB.LateUpdatePrefix` | `PlayerControllerB::LateUpdate` |
| `PatchPlayerControllerB.SpawnDeadBodyPostfix` | `PlayerControllerB::SpawnDeadBody` |
| `PatchPlayerControllerB.TeleportPlayerPostfix` | `PlayerControllerB::TeleportPlayer` |
| `PatchRoundManager.SetLevelObjectVariablesPostfix` | `RoundManager::SetLevelObjectVariables` |
| `PatchRoundManager.SpawnSyncedPropsPostfix` | `RoundManager::SpawnSyncedProps` |
| `PatchStartOfRound.AwakePostfix` | `StartOfRound::Awake` |
| `PatchStartOfRound.ShipLeavePostFix` | `StartOfRound::ShipLeave` |
| `PatchStartOfRound.ShipHasLeftPostFix` | `StartOfRound::ShipHasLeft` |

None declares `EntranceTeleport`, an entrance-ID field, fire-exit matching, shortcut pairing or an entrance-pair resolver as its target.

All 19 corresponding Black Mesa patch bodies occur in the broad IL report as signal methods because their owner namespace contains `Patches`; all 19 have `strong_entrance_signal=false`.

## Combined C3F3 result

The two evidence layers close the exact-DLL gate together:

1. every RVA-bearing managed body in exact `BlackMesa.dll` is scanned;
2. the eight no-RVA MethodDefs are proven managed abstract declarations with their module-internal dispatch bodies enumerated and already covered by that scan;
3. there are no ImplMap/native/forwarded exceptional methods;
4. all 27 HarmonyPatch attributes are decoded;
5. all 19 effective class+method Harmony target declarations are bound without conflict;
6. no bound Harmony target is an entrance/fire-exit/pairing target;
7. the broad IL scan exposes zero direct entrance references, zero pairing-field references/writes and zero strong entrance-signal methods.

**Bounded C3F3 decision:** exact Black Mesa 3.4.4 `BlackMesa.dll` does not expose an identified DLL-local managed-IL or declared-Harmony mechanism that creates/re-writes `EntranceTeleport` topology, changes IDs 2/3, rewrites inside/outside pairing fields, or otherwise reconciles C3F2's serialized moon-side 2/3 asymmetry.

This is stronger than the earlier incomplete "no direct reference found" result because the RVA-less metadata and the previously undecodable Harmony attribute are now closed.

It is still a bounded static conclusion, not a universal absence proof.

## Relationship to C3F2 topology

C3F2 remains authoritative for exact serialized topology:

Dungeon side:

- ID 0, `isEntranceToBuilding=false`;
- ID 1, `isEntranceToBuilding=false`.

Black Mesa moon side:

- IDs 0, 1, 2, 3, all `isEntranceToBuilding=true`.

C3F3 does **not** establish that IDs 2/3 are broken. It establishes only that the exact Black Mesa implementation DLL does not provide an identified reconciliation mechanism within the inspected managed IL/metadata/Harmony surface.

Therefore:

- the 0/1 versus 0/1/2/3 asymmetry remains a real static package fact;
- it remains insufficient to prove arbitrary replacement-interior topology safe;
- it is also insufficient to prove Black Mesa moon gameplay incompatibility;
- Black Mesa's positive selection-layer matches remain selection evidence, not traversal/topology clearance.

## Matrix and lifecycle consequence

No authoritative matrix cell changes from C3F3 alone.

Preserved state:

- B3 remains 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, 914 `NOT_YET_PROVEN`;
- the separately recorded 46 External selection-supported pairings remain selection-only evidence;
- Black Mesa remains single-registered through its native owner path;
- no duplicate LLL registration is introduced;
- Shatteredrooms × Experimentation/Embrion exclusions remain unchanged;
- S1.42AB InteriorWeightNormalization remains unchanged;
- S1.42AK remains accepted/latest;
- no candidate or runtime test is armed;
- build controller remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

## Proof boundary

C3F3 does **not** prove:

- that Black Mesa moon-side IDs 2/3 are broken or stranded;
- that IDs 2/3 are ordinary fire exits;
- that arbitrary replacement interiors are topology-compatible with Black Mesa;
- absence of entrance/pairing behavior in another assembly, Unity/game engine code, DawnLib, LethalLevelLoader, vanilla `Assembly-CSharp`, serialized runtime data or dynamically generated code;
- final Harmony runtime patch order or successful external overload resolution;
- actual traversal behavior;
- general gameplay compatibility of arbitrary interiors on Black Mesa.

The broad IL evidence records direct component/reflection callsites and identifiable string/metadata signals in this exact DLL. Unknown runtime targets that cannot be recovered from those static operands remain outside the proof.

## C3F3 decision

The C3F3 **exact BlackMesa.dll metadata/IL gate is complete**.

The previously open exact-DLL special-handling question is closed without finding a DLL-local reconciliation path for the extra moon-side entrance IDs.

C3F3 is therefore publication-complete as a static evidence checkpoint, while Black Mesa's full External-row topology applicability remains unresolved at the broader integration level. Any later clearance must come from separate evidence about the actual general entrance matching/pairing semantics and/or appropriately authorized runtime traversal evidence; it must not be inferred from the absence of a BlackMesa.dll-specific rewrite.

No gameplay build, runtime test, universal override or B3 matrix rewrite is authorized by this checkpoint.
