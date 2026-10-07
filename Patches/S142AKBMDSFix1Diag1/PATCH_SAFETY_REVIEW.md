# S1.42AK-BMDSFIX1-DIAG1 Patch Safety Review

**Stage:** Source / Pure Static only  
**Disposition:** DIAGNOSTIC ONLY / NEVER ACCEPT  
**Authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Surface inventory

Exactly one Harmony surface exists:

- Postfix: `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`
- Ordering: after `tendas.lethalcompany.s142abinteriorweightnormalization`
- Priority: `Priority.Last`
- Mutation scope: only the fresh returned `List<ExtendedDungeonFlowWithRarity>` for the validated Black Mesa server-selection call
- Mutation shape: preserve the exact existing Deep Sewers wrapper and reduce local list `N -> 1`

There are no Harmony prefixes, transpilers, broad `PatchAll` calls, secondary observation patches, or lifecycle takeovers.

## Fail-closed guards

Arming requires exact LLL version/hash, exact accepted S1.42AB normalizer version/hash, exact reflected target signature/body, exact result type, exact relevant fields/properties/caller methods, and exactly one normalizer postfix already present on the same target.

Selection requires the real server-selection stack and explicitly excludes `TerminalManager.GetSimulationResultsText`. It further requires Black Mesa, exact result-list identity, a non-empty mutable concrete result list, no null wrapper anywhere, exactly one canonical `DungeonName == "Deep Sewers"` entry, exact `DungeonFlow.name == "DeepSewersFlow"`, and final normalized rarity `100`.

No local-list mutation occurs until every validation above has completed.

## Preserved ownership

This diagnostic does not:

- patch `DungeonLoader.GetClampedDungeonSize()` or emit `[BMDSFIX1] APPLIED`;
- copy or replace BMDSFIX1 size logic;
- patch `EntranceTeleport` or any teleport ID/state;
- touch NavMesh;
- hook global RNG;
- replace or patch the selection RPC;
- register dungeon flows;
- change Dawn/native Black Mesa ownership;
- recalculate rarity;
- mutate global LLL registries/lists;
- modify S1.42AB InteriorWeightNormalization.

The original S1.42AK-BMDSFIX1 DLL remains sole owner of the Black Mesa / `DeepSewersFlow` size clamp.

## One-variable test boundary

A future DIAG1 review profile may differ from the exact BMDSFIX1 candidate only by addition of this diagnostic DLL. The current Source/Pure-Static stage does not create that profile, arm it, or change `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, accepted baseline, active candidate, or runtime qualification state.

A DIAG1 runtime result can be supporting diagnostic evidence only and cannot silently satisfy the exact-byte BMDSFIX1 acceptance gate.
