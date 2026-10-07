# C3E3E — Oxyde client-generation integration boundary

Status: bounded Dawn/LLL downstream generation chain resolved; installed-V81 false-flag callsite reachability remains unresolved.

## Scope and provenance

Parent PR #138 HEAD: `bc92bc6517d1c236d43b087dc53122bf72e38311`. Accepted baseline: S1.42AK. Inspection date: 2026-09-20.

C3E3D proved that the exact CodeRebirth 1.6.9 / DawnLib 0.9.25 owner path preserves Oxyde's packaged `SelectableLevel.spawnEnemiesAndScrap = false`; it found no direct owner write enabling that flag. C3E3E therefore asks one narrower question: **if the RoundManager dungeon-generation path is reached for this External level, do DawnLib 0.9.25 or LethalLevelLoader 1.7.12 stop generation because the flag is false?**

The exact Dawn package/DLL binding remains the C3E3D manifest: DawnLib 0.9.25 ZIP SHA-256 `c33c608869763f916f07e5ddf47224134f98bab15d044bd809a46ef2d3d538c3`, main DLL SHA-256 `9b4826a16eec1fa5091fb4246d010005bc9c3e04282034e8d067b499ab5c125b`. C3E3D's exact-binary `DungeonRegistrationHandler.Init` capture proves that this DLL installs the named GenerateNewFloor, RuntimeDungeon and deferred-generation hooks referenced below.

For method-body readability this checkpoint also pins TeamXiaolan/DawnLib commit `810613e556ecc357eac25e97c25a3bb90516f071`; its `Directory.Build.props` blob `b3741c4c59f235f19acde7bef81660de3e4801e5` declares version 0.9.25. The detailed Dawn method bodies are therefore **version-aligned upstream source**, not a new byte-for-byte source-to-DLL identity proof. LLL remains release-source-bound exactly as in C3B: `pacoito123/LC_LethalLevelLoader@f9998b91adf242cd8d735f4e697d55b32b94bfac` ("Release v1.7.12"), with no accepted-profile LLL DLL SHA-256 currently preserved.

Machine-readable source binding and conclusions are in `GENERATION_INTEGRATION_SOURCE.json`.

## LLL's false-flag branch does not terminate at the helper

LLL 1.7.12 `GenerateNewLevelClientRpc_Transpiler` searches for a `RoundManager.GenerateNewFloor` call and replaces that call with `InjectHostDungeonFlowSelection`.

The helper then makes a very specific split:

- when the current ExtendedLevel is loaded and `spawnEnemiesAndScrap` is true, it calls `DungeonLoader.SelectDungeon()`;
- otherwise, including the false-flag case, it calls `roundManager.GenerateNewFloor()`.

So **inside this LLL helper**, Oxyde's preserved false flag is not a "return without dungeon generation" condition. It delegates to GenerateNewFloor instead.

That statement has an important boundary: the transpiler tells us what happens **at the replaced callsite**. It does not tell us whether vanilla V81 reaches that callsite when the flag is false.

## Dawn takes over GenerateNewFloor's final Generate call

Dawn's version-aligned 0.9.25 source shows the interaction that C3E3D's exact binary `Init` hook list pointed toward:

1. `DeleteLLLTranspilerAndEnsureDelayedDungeon` removes LLL's `RoundManager.GenerateNewFloor` transpiler when LLL is present.
2. It then attaches Dawn's `DelayDungeonGeneration` IL patch.
3. `DelayDungeonGeneration` replaces GenerateNewFloor's direct `dungeonGenerator.Generate()` sequence with `StartCoroutine(LoadDungeonBundle)`.
4. `LoadDungeonBundle` waits for Dawn-owned bundle hotloading when necessary.
5. After that wait it either:
   - calls `LethalLevelLoaderCompat.LetLLLHandleGeneration()` for a flow that should remain LLL-controlled; or
   - applies Dawn's dungeon-size clamp and directly calls `RoundManager.Instance.dungeonGenerator.Generate()`.
6. The LLL delegate-back helper calls `InjectHostDungeonSizeSelection`; its network size path ends in `SetDungeonFlowSizeClientRpc`, which calls `RoundManager.dungeonGenerator.Generate()`.

No `SelectableLevel.spawnEnemiesAndScrap` test appears in this downstream Dawn delayed-generation decision chain. The decisions there are about selected dungeon ownership / skip semantics and bundle loading, not the moon generation flag.

**Bounded conclusion:** once `RoundManager.GenerateNewFloor` is actually entered, the inspected Dawn/LLL integration does not use Oxyde's false flag as a downstream stop gate. The previous uncertainty is now narrower: whether installed vanilla V81 reaches the LLL-transpiled GenerateNewFloor callsite for a false-flag level.

## Exact installed-V81 boundary is still missing

The repository's installed-V81 focused capture remains:

`SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T143200Z-a693b4b9/ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt`

It is SHA-256 `5317509a39e072db2c3df95de1cb9091dd9f7ff7e1a3bfe231045dea9cfc974f` and is attributed by its reviewed evidence to installed Assembly-CSharp SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`, Steam build 22825947.

As C3E3D already noted, this capture contains the useful `LoadNewLevelWait` and `FinishGeneratingNewLevelClientRpc` guards but **does not contain the bodies of `RoundManager.GenerateNewLevelClientRpc` or `RoundManager.GenerateNewFloor`**. Repository search found no second installed-V81 capture that supplies those bodies.

That missing method body matters. A Harmony transpiler can replace a call only where the original call exists; the source-level replacement does not prove whether an enclosing vanilla branch skips that call when `spawnEnemiesAndScrap == false`.

Therefore C3E3E does **not** claim that Oxyde definitely generates an ordinary dungeon at runtime, and it does not infer any main-entrance or fire-exit construction from the downstream chain.

## Preserved project state

The authoritative B3 matrix is unchanged. The existing **46 External selection-supported pairings** remain selection-only evidence. No matrix cell is promoted to generation/traversal proof.

No config, gameplay profile, controller or accepted architecture changes occur. In particular:

- S1.42AK remains accepted/latest and has no candidate or outstanding runtime test.
- `BuildSpecs/current.json` stays disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt` stays S1.42AK.
- S1.42AB InteriorWeightNormalization remains untouched.
- Black Mesa remains owner-registered and is not additionally registered through LLL.
- Shatteredrooms Experimentation/Embrion exclusions remain intact.
- no universal override, gameplay build or gameplay run is authorized.

## Next bounded segment

Next **C3E3F**: recover or definitively bound the exact installed-V81 method bodies for `RoundManager.GenerateNewLevelClientRpc` and `RoundManager.GenerateNewFloor`, using existing repository-native capture/provenance infrastructure first. The only question is callsite reachability/control flow around the generation call for `spawnEnemiesAndScrap = false`.

Do not request a gameplay run merely to fill this source gap. Do not start Oxyde entrance construction/topology until this upstream gate is resolved or explicitly proven unavailable. Black Mesa topology and the general entrance numbering/pairing semantics remain later C3 tasks.
