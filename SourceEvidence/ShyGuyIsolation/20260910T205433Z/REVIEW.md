# S1.42AI-DIAG1 — exact-package inspection checkpoint

**Status:** PARTIAL_SOURCE_REVIEW / NOT_IMPLEMENTED / NOT_BUILD_READY
**Reviewed:** 2026-09-11
**Canonical plan:** `BuildSpecs/S1.42AI_PLAN.md`
**Accepted baseline and active artifact:** resolve from `Current/CURRENT_STATE.json`; this evidence is not lifecycle authority.

## Capture provenance

The read-only GitHub Actions inspection run [34529045495](https://github.com/Tendas240/Lethal-Company-AI-Modding-Project/actions/runs/34529045495) succeeded on analysis commit `0eb3080303eca3eec415e5ab9e653f8dc47cd65f`.
Its artifact `10172755960` has ZIP SHA-256 `ab4bb578bbb28b8ab8c4fc4284039eba5595d54b354460edb1d973a5e78bb123`.
The initial narrower capture was run `34528820510`, artifact `10172664148`; the expanded capture retained here is the registration-owner follow-up, not a runtime test.

`MANIFEST.json` and all 16 original captured files are preserved beside this review. The 11 declared mod report hashes were recomputed after downloading the artifact. `CAPTURE_INDEX.json` records hashes for every retained capture file. Reports contain numbered, bounded source windows; they are not necessarily complete methods. Missing-reference decompiler annotations are preserved and must not be mistaken for verified base-method behavior.

The workflow verified the existing S1.42AI profile SHA-256 and exact embedded export bytes against ProfileSources before deriving package versions. It downloaded exact Scopophobia 1.3.4 and BCMER 1.71.0 package releases and recorded package/DLL hashes. These are package bytes, not a claim that the user's current Gale install has been inspected.

## Confirmed identity and owner mapping

| Surface | Exact evidence | Consequence |
| --- | --- | --- |
| Shy Guy AI | `ShyGuy.AI.ShyGuyAI : EnemyAI` in Scopophobia 1.3.4 | Use exact type/prefab identity; do not allow enemies merely because their names contain a broad substring. |
| Scopophobia asset | `Scopophobia.ScopophobiaPlugin.Awake()` loads `ShyGuyDef.asset` into its `shyGuy` EnemyType field, registers its enemyPrefab, then registers that enemy with LethalLib | Resolve the actual loaded asset/prefab and validate its AI component at runtime. The bundle's serialized values have not been separately extracted here. |
| BCMER event | `BrutalCompanyMinus.Minus.Events.ShyGuy.Name()` returns `ShyGuy`; `AddEventIfOnly()` checks Scopophobia presence; `Execute()` calls `ExecuteAllMonsterEvents()` with the `ShyGuyDef` definition | Preserve this exact event as the only diagnostic BCMER event. |
| BCMER asset lookup | `Assets.EnemyList` is keyed by Unity object `name`; `Assets.GetEnemy(string)` returns that dictionary entry | `ShyGuyDef` is a registry/asset key, not the display-name string. Validate a non-null prefab: missing lookups can return an empty EnemyType. |
| Scopophobia display-name lookup | `ShyGuyPaintingProp.SpawnEnemyOnServer(int)` looks for `enemyType.enemyName.ToLower() == "shy guy"` | This is additional identity corroboration; exact live registration is still required. |

Supporting reports: the ScopophobiaPlugin, ShyGuyAI, ShyGuyPaintingProp, BCMER Assets and BCMER Events.ShyGuy files in this directory.

## Confirmed spawn and event bypasses

1. `MEvent.MonsterEvent.Execute()` adds inside/outside entries and queues explicit spawns through `Manager.Spawn.InsideEnemies` and `OutsideEnemies`.
2. `Manager.Spawn.DoSpawnInsideEnemies()` and `DoSpawnOutsideEnemies()` directly instantiate queued prefabs, spawn their NetworkObjects and register EnemyAI instances. Therefore a guard limited to vanilla `RoundManager.SpawnEnemyGameObject` or normal spawn-list selection cannot prove full isolation.
3. `ChooseEvents` handles normal selection and filters normal additional events against disabled events, but the separate forced-event loop directly calls event `Execute()` and forced side-event `Execute()`. These routes need an exact reviewed diagnostic boundary; disabling configs alone is insufficient.
4. `ShyGuyPaintingProp.SpawnEnemyOnServer(int)` calls `RoundManager.SpawnEnemyGameObject(Vector3,float,int,EnemyType)` and then uses the returned ShyGuyAI. A painting-triggered encounter is a separate owner path and cannot prove BCMER event execution. Do not silently alter the painting or fabricate event evidence.
5. The compatibility DLL actually embedded in S1.42AI has SHA-256 `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`. Its captured diagnostic class retains the old enemy targets and Pikmin-family allowance. Capturing the source and DLL hashes does not by itself prove reproducible source-to-DLL equivalence.

The exact package methods above are candidates for narrower review, not approved Harmony targets. This checkpoint introduces no interception code.

## V81 reference limitation — confirmed blocker for native patch review

The exact project reference package `LethalCompany.GameLibs.Steam 81.0.5-ngd.0` contains an Assembly-CSharp reference with SHA-256 `d8bedaba3ce700072fc231b1d4f4a41fb3c88a3cbf9dd0ee8c90dbe64272e2af`.

Its RoundManager decompile exposes signatures including:

- `void SpawnEnemyFromVent(EnemyVent)`;
- `void SpawnEnemyOnServer(Vector3,float,int)`;
- `void SpawnEnemyServerRpc(Vector3,float,int)`;
- `NetworkObjectReference SpawnEnemyGameObject(Vector3,float,int,EnemyType)`.

The inspected bodies are `throw null;` stubs. They cannot establish native spawn bookkeeping, return-value expectations, direct call chains, network stages or caller side effects. Do not implement a guessed early return from these methods based on this package alone.

The repository already has a provenance-checked installed-V81 evidence pattern in `AnalysisTools/InspectEnemyAICollisionV81.ps1` and its linked SourceEvidence. The next native capture should reuse that provenance discipline and collect only the needed RoundManager spawn methods and directly relevant callers. Existing collision evidence is not a substitute for those spawn bodies.

## Remaining gates and next bounded action

- Obtain focused nonstub native V81 spawn/caller evidence before reviewing any vanilla spawn interception.
- Inventory the other active native-mod enemy spawn owners, including EnemyAI-derived entities previously exempted as Pikmin family; prove coverage without blanket shared-NetworkObject suppression.
- Finish exact forced/side-event entry-point and adjacent lifecycle review; bounded source windows alone do not certify every responsibility.
- Validate loaded Shy Guy asset/prefab/type agreement and distinguish normal, BCMER and painting origins in diagnostic evidence.
- Verify the final source-to-DLL provenance and exact archive delta when code is implemented.

Next bounded action: prepare the focused installed-V81 source-evidence capture using the repository's existing verified helper pattern, and define the remaining native-mod source inventory. No new gameplay run or diagnostic import is ready. Build/runtime controllers and accepted state remain untouched.
