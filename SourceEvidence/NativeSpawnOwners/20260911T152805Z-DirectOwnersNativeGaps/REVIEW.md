# S1.42AI-DIAG1 exact direct-owner review and native vent/nest blocker

**Status:** EXACT_MOD_OWNER_REVIEW_COMPLETE / INSTALLED_NATIVE_VENT_NEST_SOURCE_GAP_REMAINS / PATCH_SAFETY_OPEN / NOT_BUILT  
**Date:** 2026-09-11  
**Canonical plan:** `BuildSpecs/S1.42AI_PLAN.md`  
**Patch-safety authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Evidence boundary and provenance

Read-only Actions run `34616289395` on analysis head
`d5ba279b40b4fdecd34804b6a104ae9d1067681c` re-fetched the exact package versions
already anchored by `SourceEvidence/NativeSpawnOwners/20260911T144505Z/`, verified
package ZIP and DLL SHA-256 values, and reproduced all five prior complete-decompile
source hashes with pinned ILSpy `11.0.0.9375` before producing full C# and IL.
Artifact `10270990899` (`s142ai-direct-owner-exact`) has digest
`sha256:8386340124ea14e6f5bc41cec203b506e21cb4226d381f1379b0f12d4302e0e8`.
Full third-party decompiles remain in the Actions artifact; this repository retains
only hashes, bounded findings and provenance in `VERIFICATION.json`.

The same run restored the exact project V81 NuGet reference
`LethalCompany.GameLibs.Steam 81.0.5-ngd.0`. That reference is intentionally treated
as reference metadata only. `RoundManager.AssignRandomEnemyToVent(EnemyVent,float)`
is present but its body is `throw null`; the `RoundManager` type contains 186 such
stubs. `EnemyAINestSpawnObject` is only a 15-line reference type with fields and a
stub constructor, with no usable `Awake` lifecycle. This does not replace the prior
installed-game V81 capture and cannot close the remaining native gap.

## LethalMinNightly 1.1.108 direct EnemyAI creation

The exact LethalMin assembly confirms several owner-controlled creation paths that
bypass RoundManager enemy pools entirely.

### Pikmin -> Puffmin conversion

`LethalMin.PikminAI.TransformIntoPuffminServerRpc()` directly instantiates
`LethalMin.PuffminEnemyType.enemyPrefab`, network-spawns the resulting `PuffminAI`,
sends its Pikmin data and then despawns the original Pikmin. Blocking only
`Object.Instantiate`, `NetworkObject.Spawn` or a later shared network path is unsafe:
the method immediately dereferences the created component and destroys the source
entity as part of the same conversion transaction.

### PikminManager creation API and stateful callers

`LethalMin.PikminManager.SpawnPikminOnServer(...)` directly instantiates
`LethalMin.PikminEnemyType.enemyPrefab`, spawns it with normal or player ownership,
then runs type/onion synchronization. Its quantity overload directly creates and
network-spawns each Pikmin. A blanket denial at the instantiate/network layer is not
a safe contract for their callers.

Concrete caller-side state ownership makes a simple `return null` replacement of the
shared creation API insufficient:

- `Onion.SpawnPikmin(PikminData,ulong)` calls `RemovePikminDataClientRpc(data)` **before**
  `SpawnPikminOnServer`; denying only the callee can remove stored Onion data without
  producing the withdrawn Pikmin.
- `PuffminAI.TransformIntoPikminServerRpc()` calls `SpawnPikminOnServer` and then
  despawns the Puffmin; callee-only denial destroys the source without replacement.
- map/wild creation increments and reports its own spawn totals around calls to the
  manager; a low-level denial can leave bookkeeping/logs claiming creation that did
  not occur.
- EndlessElevator restoration iterates saved Pikmin through the same API and then
  clears the saved list; callee-only denial can discard persistence data.
- Sprout creation stores the returned Pikmin and may despawn the sprout afterward;
  the surrounding pluck lifecycle must be preserved deliberately rather than by a
  generic spawn hook.

Therefore DIAG1 must prevent these non-ShyGuy EnemyAI transactions at reviewed owner
entry points before destructive/persistence mutations, not by globally exempting the
Pikmin family and not by suppressing LethalMin managers/components wholesale.

### Enemy revival

`PikUtils.ReviveEnemy(EnemyAI,Vector3)` first despawns the existing EnemyAI, then
instantiates `ai.enemyType.enemyPrefab`, network-spawns it, registers it in
`RoundManager.SpawnedEnemies` and returns the new EnemyAI. Its reviewed caller
`Onion.SetEnemyToBeRevived(EnemyGrabbableObject)` immediately dereferences the return
for `MaskedPlayerPikminEnemy` handling. A denial inside `ReviveEnemy` would either
lose the original enemy or violate the caller's non-null contract. If DIAG1 must deny
a non-ShyGuy revival, prevention has to occur before this revival transaction.

## CodeRebirth 1.6.9 explicit EnemyType consumers

The exact main assembly has fourteen calls to `RoundManager.SpawnEnemyGameObject`
across nine owner methods:

- `EnemyLevelSpawner.SpawnRandomEnemy()`;
- `TornadoWeather.SpawnTornado(Vector3)`;
- `FakeSnailCat.Update()`;
- `GuardPhone.SpawnWithDelay(Vector3)`;
- `Xui.OnNetworkDespawn()` (two Masked branches);
- `BoxChute.SpawnEnemy()`;
- `CutieFlyAI.HandleSpawningMonarch()`;
- `Monarch.OnNetworkSpawn()`;
- `Puppeteer.SwitchToStateAfterDelay(...)` (five calls across four branches plus the
  unconditional Masked call).

These consumers do not share one safe return contract:

- `EnemyLevelSpawner.SpawnRandomEnemy()` increments per-type and pipe counters **before**
  the call, converts the returned `NetworkObjectReference` to a `GameObject`, adds an
  `EnemySpawnerTracker`, reads its `EnemyAI`, and may add outside power. A central
  denied/invalid return corrupts bookkeeping and is immediately dereferenced.
- `TornadoWeather.SpawnTornado()` immediately converts the returned reference, reads
  `Tornados`, and stores it. An invalid return is not tolerated.
- `FakeSnailCat.Update()` sets its `destroyed` flag before spawning, immediately reads
  the returned `SnailCatAI`, copies state into it and then despawns the fake item.
  Central denial is destructive and invalidates the caller contract.
- `Xui.OnNetworkDespawn()` mixes Masked spawning with the distinct responsibility of
  reviving a dead player. Suppressing the whole method to stop Masked creation would
  also remove unrelated item behavior.
- `Monarch.OnNetworkSpawn()` performs normal Monarch network/lifecycle initialization
  before optionally spawning Cutie Flies; the whole lifecycle cannot be skipped.
- `Puppeteer.SwitchToStateAfterDelay()` performs the spawn branch first and then, after
  the delay, stops search state, changes animator/speed state and switches behavior.
  Suppressing the coroutine would remove required Puppeteer state transitions.
- GuardPhone, BoxChute and CutieFly owner paths ignore the spawn return, but this does
  not make a broad central denial safe because the other consumers above require a
  valid result or own adjacent state.

The result is fail-closed: `RoundManager.SpawnEnemyGameObject` is not an approved
blanket ShyGuy-only denial surface. CodeRebirth requires exact owner-level prevention
for disallowed explicit EnemyTypes while retaining each owner's non-spawn duties.

## CodeRebirth Dusk companion and DawnLib/Dusk replacement ownership

The CodeRebirth companion DLL contains fifteen typed
`DuskEnemyReplacementDefinition<T>` subclasses for CodeRebirth EnemyAI types. The
exact companion contains no `SpawnEnemyGameObject` call and no enemy-prefab creation
path found in this review. It defines replacement behavior; it is not a second enemy
spawn owner by itself.

DawnLib.Dusk confirms the replacement model:

- `DuskEnemyReplacementDefinition<T>.Apply(EnemyAI)` assigns replacement state to the
  already-created EnemyAI, applies hierarchy/addon changes and calls typed replacement
  logic on that same EnemyAI instance.
- replacement addons may instantiate/network-spawn auxiliary GameObjects. Those are
  replacement infrastructure, not evidence of a new EnemyAI; global
  `NetworkObject.Spawn` suppression would therefore break unrelated Dusk behavior.
- `EntityReplacementRegistrationPatch` detours `EnemyAI.Start` and
  `EnemyAI.UseNestSpawnObject` under `DetourContext(int.MaxValue)`.
  `ReplaceEnemyEntityUsingNest` applies any selected nest replacement and then still
  invokes the original `UseNestSpawnObject` method.
- Dusk also hooks the exact declared `EnemyAINestSpawnObject.Awake`. Its
  `OnNestSpawnAwake` selects a replacement and normally invokes the original Awake;
  however, if the replacement-weight sum is absent (`!num.HasValue`), the exact body
  returns without calling `orig`. This existing mod behavior is another reason not to
  add an unreviewed lifecycle suppression on the same target.

DawnLib core independently hooks the same nest `Awake` through
`FixNestBlankReferences`, which may normalize a vanilla EnemyType reference and then
calls `orig`. The installed execution surface therefore already has multiple foreign
owners on nest Awake even before any project-local DIAG1 hook.

## DawnLib vent/special-override interaction

DawnLib core directly detours `RoundManager.AssignRandomEnemyToVent` via
`CheckIfEnemyCanSpawn`. When `enemyRushIndex == -1`, it returns the original result.
For an active rush index it temporarily sets `spawningDisabled = true` on certain
Dawn-managed inside enemies whose current inside weight is not positive, calls the
original method, restores those flags, and then returns `true`. DawnLib also installs
its `StopDawnEnemyResetting` IL manipulator on the same method.

This means the live vent contract already has temporary state mutation and altered
return semantics. A DIAG1 patch must not skip the entire method, permanently own
`spawningDisabled`, or infer that the returned bool alone tells whether a particular
EnemyType was safely assigned.

The exact DawnLib `FixDawnMoonEnemies()` body also reads
`SelectableLevel.specialEnemyRarity?.overrideEnemy` into a local variable. On a
matching registered enemy it logs a replacement and assigns the local variable, but
the reproduced C# **and IL** contain no write back to
`specialEnemyRarity.overrideEnemy`. Therefore this code is not evidence that the
special override asset itself has been normalized to the registered EnemyType. The
native special-override/vent behavior remains an explicit coverage requirement.

## Remaining native installed-source blocker

The previously accepted installed V81 RoundManager capture already proves the caller
side: `PlotOutEnemiesForNextHour()` contains the special-enemy override condition and
calls `AssignRandomEnemyToVent`; `SpawnNestObjectForOutsideEnemy()` creates and
registers nests. It intentionally did not include the missing vent assignment body or
`EnemyAINestSpawnObject`/`EnemyAI.UseNestSpawnObject` downstream lifecycle.

The exact NuGet probe in this review cannot fill that gap because it contains only
reference stubs. Before selecting DIAG1 interception targets, a **narrow supplemental
installed-V81 source capture** is still required for only the missing surfaces:

1. `RoundManager.AssignRandomEnemyToVent(EnemyVent,float)`;
2. the declared `EnemyAINestSpawnObject` lifecycle, including its actual `Awake` body;
3. `EnemyAI.UseNestSpawnObject(EnemyAINestSpawnObject)` and the smallest useful direct
   caller/downstream context needed to establish state ownership.

This is not a request to repeat the completed 27-method RoundManager capture. Reuse
its exact installed-game/Steam/binary provenance gates and add only these previously
uncaptured surfaces. Do not weaken the source requirement or infer method bodies from
NuGet stubs.

## Patch-safety result

The LethalMin, CodeRebirth and Dusk direct-creation/replacement/return-value gaps from
batch 1 are now materially closed at exact-package source level. They rule out the
old Pikmin-family exemption, blanket central `SpawnEnemyGameObject` denial, shared
`NetworkObject.Spawn` suppression, whole-component disabling and post-spawn cleanup.

Overall S1.42AI-DIAG1 remains **PARTIAL / NOT_BUILD_READY** because the exact installed
native vent/nest downstream bodies above are still missing, followed by the remaining
enabled spawn-owner inventory and the already-required BCMER forced/side-event gate.
No build trigger, controller transition, Gale import, gameplay run or acceptance
change is authorized by this checkpoint.
