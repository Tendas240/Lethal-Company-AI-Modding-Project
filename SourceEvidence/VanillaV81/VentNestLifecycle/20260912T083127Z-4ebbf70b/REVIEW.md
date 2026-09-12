# S1.42AI-DIAG1: installed V81 vent/nest lifecycle review

**Status:** CAPTURE_VERIFIED / NATIVE_VENT_NEST_SOURCE_BLOCKER_CLOSED / PATCH_SAFETY_STILL_PARTIAL / NOT_BUILD_READY  
**Reviewed:** 2026-09-12  
**Canonical plan:** `BuildSpecs/S1.42AI_PLAN.md`  
**Patch-safety authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Evidence boundary and provenance

Original user capture commit: `ff9a15b96ef62953503cec2ba4b25fbeb7d208ce`.
Its single parent is repository main at capture:
`bfbd7eb79395ad6baff6ab2ea19209877267f5c5`.
The capture commit adds exactly two files in this directory:
`MANIFEST.json` and `V81_VENT_NEST_LIFECYCLE_FOCUSED_IL.txt`.
No existing repository file, profile, build/runtime controller, game binary or full type
decompile was modified or uploaded by the capture.

The manifest pins the same installed V81 identity as the already reviewed RoundManager
capture: Assembly-CSharp SHA-256
`5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`,
Lethal Company executable SHA-256
`24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`,
Steam app ID `1966720`, build ID `22825947`, reviewed appmanifest SHA-256
`b431704ad9cf0e44cba506274f6059d021e35f434af6ef27f3abd44c5d1e6ae3`,
and ILSpy `11.0.0.9375` in IL mode.

Exact Git blob SHA-1 values are:

| File | Git blob SHA-1 |
| --- | --- |
| `MANIFEST.json` | `11fff50283c4891d9dc5868c9007e0549ddda7d5` |
| `V81_VENT_NEST_LIFECYCLE_FOCUSED_IL.txt` | `30ef4b9aa6b6d397b1c979dbf7d7a8dbaed0d048` |

The manifest records report SHA-256
`91c870dc48cffe5789d3e6a90ead6cfda4798cef37b41ee3926b6afcbd8ce6e7`.
That value was computed by the capture helper from the report text immediately before
publishing the same report string. The repository-side review verifies the exact Git
blob identity and the capture's hash/provenance chain; it does not claim an independent
server-side SHA-256 recomputation of the full uploaded report bytes.

## Native vent assignment findings

`RoundManager.AssignRandomEnemyToVent(EnemyVent,float)` is a stateful native owner,
not a safe blanket-denial surface. It builds indoor spawn probabilities, invokes
`InsideEnemyCannotBeSpawned`, handles `specialEnemyRarity`, chooses the resulting
EnemyType index, and then performs the assignment transaction.

A successful assignment updates at least:

- `currentEnemyPower` and `currentEnemyPowerNoDeaths`;
- `EnemyVent.enemyType`, `enemyTypeIndex`, `occupied` and `spawnTime`;
- vent spawn-time client synchronization;
- inside diversity state;
- `EnemyType.numberSpawned` and `hasSpawnedAtLeastOne`.

Therefore DIAG1 must not skip the complete method merely to prevent a non-ShyGuy
identity. That would suppress required native scheduling, accounting and client state.
The exact body also closes the previously open `specialEnemyRarity` uncertainty: the
special override is handled inside the same assignment transaction and is not a
separate safe bypass target.

This conclusion composes with the exact installed mod review. DawnLib 0.9.25 detours
this method, temporarily owns selected `spawningDisabled` flags during rush assignment
and restores them after calling the original. SpawnCycleFixes 1.2.2 also transpiles,
prefixes and postfixes this exact target; its postfix may fan one successful assignment
out across additional vents while reserving additional power/count state. DIAG1 must
therefore neither permanently own `spawningDisabled` nor add a competing broad/default-
priority skip contract on `AssignRandomEnemyToVent`.

## EnemyAINestSpawnObject lifecycle finding

Installed V81 contains **zero declared `EnemyAINestSpawnObject.Awake` methods**. The
capture preserves this as evidence rather than treating it as an extraction failure.
It also finds no configured declared lifecycle seeds on the type.

The actual installed base chain is:

`EnemyAINestSpawnObject -> UnityEngine.MonoBehaviour -> UnityEngine.Behaviour -> UnityEngine.Component -> UnityEngine.Object -> System.Object`.

For the captured Unity base types, the reviewed lifecycle set contains no declared
`Awake` responsibility either. Consequently there is no native declared or inherited
`Awake` body on this Installed-V81 path that a project-local patch must preserve,
replace or suppress.

This resolves the older DawnLib/Dusk review's source gap. DawnLib core and Dusk 0.9.25
contain hook code written against a declared `EnemyAINestSpawnObject.Awake`, but that
method is absent from the exact installed V81 assembly. This review does **not** infer
or claim the runtime behavior of MonoMod/HookGen when that foreign target is absent;
that behavior was not captured and is not needed to design DIAG1. The safe project
contract is simply: do not add an `EnemyAINestSpawnObject.Awake` patch or fabricate a
replacement lifecycle for a method that Installed V81 does not declare.

## Nest consumption and EnemyAI state ownership

`EnemyAI.UseNestSpawnObject(EnemyAINestSpawnObject)` has concrete required state
responsibilities. It temporarily disables the NavMeshAgent, moves/rotates the EnemyAI
to the nest transform, re-enables navigation, removes the nest from
`RoundManager.enemyNestSpawnObjects`, stores the nest GameObject in `EnemyAI.nestObject`
and, when `useMinEnemyThresholdForNest` is false, destroys the consumed nest object.

The bounded caller context proves that `EnemyAI.Start` owns the matching transaction:
for outside enemies with a nest prefab it scans `enemyNestSpawnObjects`, removes null
entries, matches `EnemyAINestSpawnObject.enemyType` to the EnemyAI's `enemyType`, and
calls `UseNestSpawnObject`. If no matching nest exists while
`requireNestObjectsToSpawn` is true, the startup path marks the enemy dead/in special
animation and destroys it server-side (or follows the client visibility path), while
`Start` also owns broader normal enemy initialization and network state.

Dusk 0.9.25 detours `EnemyAI.Start` and `EnemyAI.UseNestSpawnObject` for replacement
behavior and still invokes the original nest consumer after applying its replacement.
Therefore DIAG1 must preserve these native/foreign responsibilities. Nest suppression
is not an acceptable generic substitute for enemy-spawn prevention.

NestFix 1.3.0 and SpawnCycleFixes 1.2.2 already own parts of nest prediction/creation.
`SpawnNestObjectForOutsideEnemy` must remain infrastructure rather than being treated
as a generic EnemyAI spawn gate.

## Patch-safety decision

The previously explicit Installed-V81 vent/nest source blocker is **closed** by this
capture and review. No further Installed-V81 vent/nest recapture is required for
S1.42AI-DIAG1.

Approved negative constraints carried into implementation design:

- do not skip `RoundManager.AssignRandomEnemyToVent` wholesale;
- do not permanently own DawnLib's temporary `spawningDisabled` state;
- do not add a guessed `EnemyAINestSpawnObject.Awake` hook;
- do not suppress `EnemyAI.Start` or `EnemyAI.UseNestSpawnObject` wholesale;
- do not suppress `SpawnNestObjectForOutsideEnemy` or shared `NetworkObject.Spawn` to
  obtain an empty diagnostic round;
- do not use post-spawn cleanup to conceal a prevention gap;
- preserve unexpected exterior Shy Guy so the correction can fail visibly.

## Remaining patch-safety work

S1.42AI-DIAG1 is still **PARTIAL / NOT_BUILD_READY**. Closing this source blocker does
not close the broader isolation design. Before implementation/build, complete the
remaining bounded work already required by the canonical plan:

1. finish the remaining enabled-package EnemyAI spawn-owner inventory beyond the exact
   LethalMin/CodeRebirth/DawnLib/NestFix/SpawnCycleFixes batches already reviewed;
2. close the exact BCMER forced-event, forced-side-event, additional-event and runtime/
   custom-registration execution gate so every non-ShyGuy event is prevented without
   replacing BCMER's full selection/execution lifecycle;
3. preserve/verify the exact Shy Guy runtime identity and project source-to-DLL
   provenance needed by the final narrow interception design;
4. select and statically validate the smallest prevention-only interception points,
   retaining host/client, repeated-round and restoration requirements.

No build trigger, controller transition, Gale import, gameplay run or acceptance
change is authorized by this review. Existing S1.42AI remains the active unaccepted
candidate, and S1.42AI-DIAG1 remains planned but not built.
