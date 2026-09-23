# C3F17.1 — targeted Black Mesa x Greenhouse deterministic-selection mechanism review

**Status:** SAFE MINIMAL SELECTION MECHANISM IDENTIFIED / CANDIDATE NOT YET AUTHORED / NO BUILD, CONTROLLER OR GAMEPLAY CHANGE  
**Date:** 2026-09-23  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Parent head:** `31bb5c7ad32004966e40f3f62ac90c8459dcc605`

## Bounded objective

This first C3F17 segment identifies the smallest repository-native mechanism capable of deterministically exercising the exact pair:

- moon: Black Mesa;
- interior: `GreenhouseFlow`.

It does not author/build/arm a diagnostic candidate and does not start gameplay.

## Fresh lifecycle and provenance gate

At segment start:

- `main` is `56355ff518ae4301a38d370be9561251f6f963c1`;
- main Knowledge Architecture run #556 / run ID `35429763835` is completed/success and permanent job `validate-knowledge-architecture` is success;
- PR #138 is open, draft, unmerged and mergeable with base `main@56355ff518ae4301a38d370be9561251f6f963c1` and head `31bb5c7ad32004966e40f3f62ac90c8459dcc605`;
- the 15 PR workflow runs visible for that head are all completed/success;
- `CURRENT_STATE.json` still has accepted/latest S1.42AK, `active_candidate=null`, `runtime_test_outstanding=false` and disabled build controller state.

The current lifecycle therefore permits static candidate-design work only. No runtime test is authorized.

## Existing selection mechanisms relevant to the exact pair

### 1. Black Mesa moon ownership remains Dawn/native

Black Mesa remains Dawn/native-owned. The diagnostic must not create an LLL moon registration and must not change Black Mesa's owner weights merely to obtain this test.

The target moon itself does not require a gameplay patch: it can be selected through its normal owner-supported route/terminal path. The diagnostic selection hook should activate only after the current LLL `ExtendedLevel` identity has been validated as Black Mesa. Other moons must remain normal.

This keeps moon ownership unchanged and makes the diagnostic responsibility narrow: force the dungeon choice only when the player has deliberately routed to Black Mesa.

### 2. Greenhouse is already legitimately viable on Black Mesa

Phase B2 classifies Greenhouse / `GreenhouseFlow` as `DIRECT_LLL_UNIVERSAL_TAG_OVERRIDE`, with the active LLL setting:

`Dungeon Injection Settings - Dynamic Level Tags List = Vanilla:100,Custom:100`

C3B proves that the Dawn -> LLL bridge represents Black Mesa as an LLL `External` level while seeding/copying at least LLL `Custom` + `All` tags. Consequently the existing Greenhouse rule already matches Black Mesa at selection rarity 100 through LLL's normal viability path.

C3F16 therefore correctly treats Black Mesa selection-layer support for Greenhouse as already established. C3F17 does not need to invent availability or bypass an owner hard block.

### 3. S1.42AB normalization must remain upstream and unchanged

The accepted `S1.42ABInteriorWeightNormalization` architecture leaves viability ownership to LLL and changes only positive returned rarities to exactly 100.

For the diagnostic, this is useful as a fail-closed identity condition: the Greenhouse wrapper must already be present in the normal viable result and already have final rarity 100 before any diagnostic singleton mutation occurs.

The diagnostic must not modify, replace, disable or bypass the accepted normalizer.

### 4. Existing repository precedent: S1.42AJ-DIAG1 singleton postfilter

`BuildSpecs/S1.42AJ-DIAG1_PLAN.md` already defines a bounded deterministic interior-selection pattern against LLL 1.7.12:

- exact sole Harmony target: static `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`;
- postfix only; no prefix/transpiler/RPC patch;
- let LLL build its complete fresh viable pool first;
- act only for the exact server selection caller `LethalLevelLoaderNetworkManager.GetRandomExtendedDungeonFlowServerRpc()` and the intended `true` selection invocation;
- exclude terminal simulation and false/day-history calls;
- validate target moon, exactly one target flow, exact flow asset identity and already-normalized rarity 100 before mutation;
- then clear only that freshly allocated return list and re-add the same existing weighted wrapper;
- create no flow/wrapper and change no global registration/config/list;
- fail closed on unknown caller, missing/duplicate target, wrong asset or wrong rarity;
- preserve downstream native RPC ownership, synchronization and generation.

That DIAG1 mechanism successfully produced deterministic LC Office diagnostic coverage without becoming balanced gameplay state. It is the strongest repository-native precedent for C3F17.

## Mechanism comparison

### Config-only weight increase — rejected

Increasing Greenhouse rarity cannot deterministically select it because the accepted normalizer converts every positive viable rarity to 100. A larger pre-normalization Greenhouse number therefore does not survive as a selection advantage.

### Config-only exclusion of every competing flow — rejected

A pure config singleton would require suppressing the complete competing viable pool on Black Mesa. The current 53-flow universe spans direct LLL config, owner/asset matching, vanilla/native LLL matching and Dawn-native Black Mesa ownership. Broadly editing those unrelated owners/configs would be much larger than the diagnostic question and would violate the no-unrelated-change constraint.

### Duplicate LLL registration / Black Mesa ownership transfer — rejected

Black Mesa is already Dawn/native-owned and LLL bridges it as External. Duplicate registration is unnecessary and explicitly forbidden.

### RNG manipulation or network/RPC replacement — rejected

The existing DIAG1 pattern proves that deterministic selection can be obtained by postfiltering the fresh validated query result. RNG manipulation, RPC replacement or broader lifecycle patches would take ownership away from the existing stack without need.

## Smallest safe C3F17 candidate mechanism

The smallest safe candidate is therefore an S1.42AK-derived diagnostic-only adaptation of the DIAG1 singleton postfilter:

1. Player routes to Black Mesa through the normal owner-supported moon route.
2. LLL/Dawn perform their normal moon registration/tag matching and LLL constructs the full viable dungeon pool.
3. The accepted S1.42AB normalizer completes unchanged.
4. A diagnostic postfix on `DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` acts only when all static/runtime guard conditions identify:
   - Black Mesa as the target `ExtendedLevel`;
   - the real server random-dungeon selection caller;
   - the selection-mode `true` call;
   - exactly one existing Greenhouse entry;
   - exact flow asset `GreenhouseFlow`;
   - final rarity 100.
5. Only then, the postfix reduces that fresh return value to the same existing Greenhouse wrapper as a singleton.
6. LLL's existing RPC/network owner and Dawn/LLL downstream generation remain untouched.

This mechanism forces the interior without changing the moon owner, flow registration, Greenhouse availability rule, accepted normalizer, package graph or unrelated configuration.

## Candidate-design obligations still open

Before any diagnostic artifact can be authored/armed, the next bounded segment must turn this mechanism into an exact candidate contract and revalidate the current S1.42AK implementation boundary, including:

- exact accepted S1.42AK parent/profile identity;
- exact current loaded LLL dependency/version/hash and declared target/caller signatures;
- exact Black Mesa `ExtendedLevel` identity fields safe to guard on;
- exact Greenhouse display/asset identity fields;
- Harmony ordering relative to the accepted normalizer;
- fail-closed startup and selection markers;
- preservation of simulation, false/history calls, other moons and repeated upstream full-pool construction;
- whether existing runtime logging is sufficient for C3F16 proof items 1-7 or whether one minimal observation-only logger is necessary.

Static candidate validation must precede any build/runtime arming decision.

## Preserved boundaries

- S1.42AK remains accepted/latest.
- S1.42ABInteriorWeightNormalization remains unchanged.
- Black Mesa remains Dawn/native-owned.
- No duplicate LLL registration is introduced.
- Greenhouse's existing direct LLL availability rule remains unchanged.
- B3 matrix remains unchanged; Black Mesa x Greenhouse remains `NOT_YET_PROVEN` pending runtime qualification.
- No `KNOWN_TECHNICAL_RESTRICTION` is inferred.
- Shatteredrooms x Experimentation and x Embrion remain untouched.
- Black Mesa/Pikmin routing recovery remains a separate deferred scope.
- C3F10D exhausted restoration paths are not reopened.
- No BuildSpecs/current, runtime controller, package, config or gameplay bytes are changed in this segment.
- No runtime test is armed or requested.

## Next bounded checkpoint

Perform **C3F17.2 — exact diagnostic-candidate contract authoring**.

Adapt the proven DIAG1 singleton-postfilter design to exact S1.42AK + Black Mesa + `GreenhouseFlow`, bind all dependency/identity/order/fail-closed guards repository-native, and define the minimum observation surface needed for C3F16's runtime proof contract.

Do not build, arm or start gameplay in that same segment unless the lifecycle is explicitly advanced by a later bounded checkpoint.