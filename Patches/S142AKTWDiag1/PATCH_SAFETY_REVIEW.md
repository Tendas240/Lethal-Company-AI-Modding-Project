# S1.42AK-TWDIAG1 Patch Safety Review

**Stage:** Source / Pure Static only  
**Disposition:** DIAGNOSTIC ONLY / NEVER ACCEPT  
**Authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`  
**Implementation authority:** `Current/302_S1.42AK_PHASE_C_TOWER_TWDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`

## Surface inventory

Exactly one Harmony surface exists:

- Postfix: `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`
- Ordering: after `tendas.lethalcompany.s142abinteriorweightnormalization`
- Priority: `Priority.Last`
- Mutation scope: only the fresh returned `List<ExtendedDungeonFlowWithRarity>` for the validated Offense server-selection call
- Mutation shape: preserve the exact existing Tower wrapper and reduce only that local viable list from `N -> 1`

There are no Harmony prefixes, transpilers, broad `PatchAll` calls, secondary observer patches, RNG hooks, RPC patches or generation/teleport lifecycle takeovers.

## Fail-closed guards

Arming requires:

- exact LethalLevelLoader GUID/version/hash;
- exact accepted S1.42AB InteriorWeightNormalization GUID/version/hash;
- exact reflected target signature/body and exact concrete return type;
- exact relevant fields/properties/caller methods;
- exactly one accepted-normalizer postfix already present on the exact target;
- TWDIAG1 installed after that normalizer at `Priority.Last`.

Selection remains inert outside Offense or when `debugResults == false`. For an Offense selection attempt it additionally requires:

- the real managed `GetRandomExtendedDungeonFlowServerRpc()` call stack;
- explicit exclusion of `TerminalManager.GetSimulationResultsText(ExtendedLevel)`;
- exact result runtime type `List<ExtendedDungeonFlowWithRarity>`;
- non-empty mutable concrete result list;
- no null wrapper anywhere;
- exactly one canonical `DungeonName == "Tower"` entry;
- non-null existing `ExtendedDungeonFlow`;
- exact `DungeonFlow.name == "TowerFlow"`;
- final normalized rarity exactly `100`.

No local-list mutation occurs until every identity/caller/pool/target/asset/rarity guard has completed. A startup mismatch unpatches TWDIAG1; a selection mismatch logs `[TWDIAG1] REFUSED selection` and preserves the normal viable pool.

## Preserved ownership

TWDIAG1 does not:

- add an unavailable flow or bypass an owner hard block;
- modify LLL registration or viability calculation;
- recalculate rarity or change the accepted normalizer;
- patch `EntranceTeleport.TeleportPlayer()`;
- replace or patch any RPC;
- touch global RNG;
- patch DunGen generation or generation size;
- touch CullFactory, NavMesh or PathfindingLib;
- alter scrap/enemy spawning;
- alter BCMER;
- alter BMDSFIX1 or emit `[BMDSFIX1] APPLIED`;
- mutate global LLL registries/lists.

LLL remains owner of registration and viability, and the accepted S1.42AB normalizer remains owner of equal-effective-rarity normalization before this diagnostic's final local singleton reduction.

## Secondary lifecycle review

The intercepted method's returned list is consumed by LLL selection. TWDIAG1 changes only which already-viable wrapper survives in the fresh result of the validated real selection call. It does not intercept generation, CullFactory materialization, entrance pairing, teleport, floor completion, PathfindingLib, NavMesh, AI, scrap, cleanup or network ownership.

That boundary is intentional: record 289 already established sufficient normal-stack observability for generation/materialization, so adding an EntranceTeleport, DunGen, CullFactory, PathfindingLib or NavMesh observer would enlarge risk without improving the basic proof contract.

## One-variable and runtime boundary

This source/static stage creates no profile and changes no runtime controller.

A later separately authorized review profile must derive from exact `S1.42AK-BMDSFIX1` profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0` and differ only by the diagnostic addition plus profile identity metadata proven by a future build gate.

Any later runtime must verify, at minimum:

- `[TWDIAG1] ARMED` and exact target-selection marker;
- no unexpected `[BMDSFIX1] APPLIED` on Offense;
- `Players finished generating the new floor`;
- exact post-generation `TowerFlow` materialization via CullFactory or equivalent exact-flow evidence;
- complete concrete PathfindingLib entrance relationships for the generated topology;
- no new target-correlated persistent generation/exception flood.

That later runtime can establish diagnostic-generated Tower evidence only. TWDIAG1 itself is never acceptable gameplay content.

## Forbidden broader alternative

Do not make Tower globally available, change rarity/weights, re-register the flow, patch RNG/RPC/generation, force a dungeon through a different lifecycle, patch CullFactory/PathfindingLib/NavMesh, or add traversal observers merely to obtain the target. The smallest safe mechanism is the single post-normalizer local-result postfix implemented here.
