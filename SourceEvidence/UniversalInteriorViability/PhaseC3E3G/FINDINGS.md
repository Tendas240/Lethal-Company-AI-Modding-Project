# C3E3G — exact installed V81 false-flag generation-callsite reachability

Status: exact installed-V81 upstream gate resolved; `spawnEnemiesAndScrap = false` skips the normal `GenerateNewFloor` callsite. No gameplay build/run or matrix change is authorized by this checkpoint.

## Scope and provenance

Parent PR #138 HEAD before this checkpoint: `a50916d8ebafba2c91e53f1494adadd14a0177e4`. Accepted gameplay baseline remains S1.42AK. Verified main remains `56355ff518ae4301a38d370be9561251f6f963c1`.

The focused helper published:

- evidence branch: `source-evidence/roundmanager-generation-v81-20260920t095502z-fa6b63a6`;
- evidence commit: `9cc0525087eb109c0f04d6dcfcf5a942200135fa`;
- evidence commit parent: exact main `56355ff518ae4301a38d370be9561251f6f963c1`;
- directory: `SourceEvidence/VanillaV81/RoundManagerGeneration/20260920T095502Z-fa6b63a6/`;
- report Git blob: `c30e58659a1e5ae218f47b908fb193ad3d54b7bd`;
- manifest Git blob: `a54617350d73cedabc403802e485e74c2384446e`.

The capture manifest binds the same exact installed identity already reviewed for C3E3F:

- Assembly-CSharp SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- Lethal Company.exe SHA-256 `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam App ID `1966720`;
- Steam build ID `22825947`;
- reviewed appmanifest SHA-256 `132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e`;
- ilspycmd `11.0.0.9375`;
- manifest-bound focused-report SHA-256 `7905f5d56846db1b019a046ff45608598adfd25e6ed151c2081fa523fa052b0a`.

Only the focused report and manifest are ingested here; no game binary or full RoundManager decompile is added.

## Captured surface

The helper selected exactly four method blocks:

1. `RoundManager.GenerateNewFloor()`;
2. direct caller `RoundManager.LoadNewLevelWait(int randomSeed)`;
3. `RoundManager.GenerateNewLevelClientRpc(...)`;
4. direct RPC caller `RoundManager.__rpc_handler_3073943002(...)`.

This satisfies the C3E3F bounded extraction contract.

## Exact callsite decision

The installed V81 `GenerateNewLevelClientRpc` body performs normal setup, assigns `currentLevel`, initializes random state and map containers, then contains this control-flow guard **before** the dungeon generator lookup and before the `GenerateNewFloor()` call:

`if (!currentLevel.spawnEnemiesAndScrap) return;`

Only after that guard does the method:

- resolve `RuntimeDungeon` with `FindObjectOfType<RuntimeDungeon>(includeInactive: false)`;
- configure asynchronous generation;
- call `GenerateNewFloor()`;
- wait for or finish generation depending on generator status.

Therefore the exact result is:

**When `currentLevel.spawnEnemiesAndScrap == false`, installed V81 returns from `GenerateNewLevelClientRpc` before the `GenerateNewFloor` callsite. The callsite is not reached.**

The selected direct callers do not bypass this result:

- `LoadNewLevelWait` invokes `GenerateNewLevelClientRpc` and later uses additional `spawnEnemiesAndScrap` guards for generation waiting/post-processing, but it does not directly call `GenerateNewFloor`;
- the generated RPC handler only enters `GenerateNewLevelClientRpc`; it does not call `GenerateNewFloor` independently.

`GenerateNewFloor` itself contains no `spawnEnemiesAndScrap` guard and ends in `dungeonGenerator.Generate()`, which is consistent with C3E3E's bounded conclusion that once this method is entered the inspected downstream Dawn/LLL chain does not stop on the flag.

## Reconciliation with C3E3E

C3E3E established that LLL's `GenerateNewLevelClientRpc_Transpiler` replaces the existing `GenerateNewFloor` callsite with `InjectHostDungeonFlowSelection`, whose false-flag branch would delegate to `GenerateNewFloor`.

C3E3G now closes the missing upstream condition: the vanilla false-flag guard executes before that original callsite. Replacing the call instruction does not make a skipped callsite reachable.

Dawn's delayed generation integration is likewise downstream of actual `GenerateNewFloor` entry. It does not alter this newly proven upstream skip in the inspected chain.

Combined with C3E3C/C3E3D — exact packaged Oxyde `spawnEnemiesAndScrap = false` and no direct owner write/address-take changing it in the six inspected owner assemblies — the ordinary inspected `GenerateNewLevelClientRpc -> GenerateNewFloor` dungeon-generation path is blocked for that preserved false flag.

## Proof boundary

This checkpoint proves a **negative callsite-reachability result**, not a broader Oxyde topology claim.

It does **not** prove:

- that Oxyde has zero runtime entrances;
- that Oxyde must use ordinary generated-dungeon entrances;
- that no independent/static owner path can create or use entrance topology;
- successful or failed Oxyde gameplay traversal;
- any Black Mesa 3.4.4 topology property;
- general DawnLib/LLL/vanilla entrance-ID or pairing semantics.

Accordingly, Oxyde runtime dungeon generation and runtime entrance construction remain unproven as gameplay facts. The result is source/control-flow evidence only.

## Preserved project state

Nothing in gameplay/configuration changes:

- authoritative B3 matrix remains unchanged;
- the 46 External selection-supported pairings remain selection-layer evidence only;
- no External cell is promoted or reclassified from source evidence alone;
- Black Mesa is not duplicate-registered through LLL;
- Shatteredrooms Experimentation/Embrion exclusions remain intact;
- S1.42AB InteriorWeightNormalization remains unchanged;
- S1.42AK remains accepted/latest with no candidate and no outstanding runtime test;
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

## Next bounded segment

Next **C3E3H**: resolve the Oxyde External-row applicability/topology boundary now that the vanilla generation gate is closed. Using existing exact Oxyde package/scene/owner evidence first, determine whether any independent/static owner path supplies entrance or dungeon-pairing semantics despite the skipped ordinary `GenerateNewFloor` path, without assuming that Oxyde must possess normal generated-interior entrances and without changing the B3 matrix from source evidence alone.

Black Mesa 3.4.4 topology and general DawnLib/LLL/vanilla entrance-ID/pairing semantics remain later C3 work.
