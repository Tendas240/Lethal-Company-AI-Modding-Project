# S1.42AK-TSDIAG1 Patch Safety Review

**Scope:** Source / Pure Static only; DIAGNOSTIC ONLY / NEVER ACCEPT  
**Authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and `Current/360_S1.42AK_PHASE_C_TOY_STORE_TSDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`

## One exact Harmony surface

Exactly one Harmony surface exists: a `Priority.Last` postfix on the exact declared static `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`, with explicit `after` accepted S1.42AB normalizer. The postfix does not patch the RPC directly, alter LLL availability or normalizer rarity, or intercept generation. LLL remains owner of dungeon registration/viability, and the normalizer remains owner of positive-weight normalization.

## Exact caller, downstream ownership and adjacent effects

LLL's real `LethalLevelLoaderNetworkManager.GetRandomExtendedDungeonFlowServerRpc()` consumes the returned viable list. `TerminalManager.GetSimulationResultsText(ExtendedLevel)` uses a non-gameplay simulation path; other moons and non-debug calls may also use the same exact method. Non-Offense, non-debug and simulations must be inert. An unknown Offense debug caller must refuse, not select. No network ownership, lifecycle state, cleanup, player movement, enemy/scrap spawning, teleport, DunGen, CullFactory, PathfindingLib or NavMesh hook is authorized. These native responsibilities remain with their owning systems.

## Fail-closed constraints

Startup must validate LLL GUID/version/SHA, accepted normalizer GUID/version/SHA, declared target method/body/return type, every reflected member and exact caller signatures, one prior normalizer postfix, and one own postfix with `Priority.Last` after the normalizer. On failure: `[TSDIAG1] REFUSED TO ARM`; unpatch **only TSDIAG1**. Before selection, validate the entire fresh concrete writable viable list, no null entries, repeated wrappers or name/Unity-asset aliases, strictly positive rarities, and exactly one already viable exact `DungeonName == "Toy Store"` and Unity `DungeonFlow.name == "ToystoreFlow"` at effective rarity `100`. On refusal: `[TSDIAG1] REFUSED selection`, leave original list identity/order unchanged. On success only: preserve the **same original wrapper** by reducing fresh selection list N->1. No new wrapper, weight repair, global mutation or fallback.

## Prohibited broader alternatives and regression boundary

No `PatchAll`, prefix/transpiler, alternate RPC/RNG hooks, new owner rules, package/config edits, floor-size/topology changes, observer patch, component disable or startup suppression. The nine-U+200B LLL Toy Store config section and existing `Vanilla:100,Custom:100` stay unchanged. Source-only CI may compile code but does not authorize constructing/releasing/importing a profile.

Only a later, separately authorized frozen review build may derive from BMDSFIX1 parent SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0` with at most one new TSDIAG1 DLL plus required short Gale metadata. Subsequent separate runtime validation must prove exact ARM/SELECTED marker, real Toy Store floor completion, target CullFactory/equivalent materialization, observed actual directed entrances and no persistent target-correlated errors. A single diagnostic-generated proof is not natural frequency, player traversal, full gameplay acceptance or BMDSFIX1 acceptance; the passive selector-free Black Mesa DeepSewersFlow proof remains independent.
