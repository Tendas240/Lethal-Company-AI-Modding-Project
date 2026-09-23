# C3F17.3 — Black Mesa x Greenhouse diagnostic source and pure static tests

**Status:** SOURCE IMPLEMENTED / PURE STATIC TESTS + PLUGIN COMPILE + SOURCE CONTRACT CI PASS / NO GALE BUILD OR RUNTIME AUTHORIZATION  
**Date:** 2026-09-23  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Parent head:** `e211255aae2ead7a5730524183ec20e89c24a78e`  
**Validated implementation head:** `65bab16f3b3a73d3fc281c59a5725e635b34c286`

## Bounded objective

C3F17.3 implements the source-only diagnostic defined by `BuildSpecs/S1.42AK-BMGHDIAG1_PLAN.md` and `CANDIDATE_CONTRACT.json`.

This checkpoint intentionally stops before a Gale candidate build, archive delta validation, lifecycle arming or gameplay. `BuildSpecs/S1.42AK-BMGHDIAG1.json` is intentionally absent and the new source-only workflow is forbidden from invoking `BuildSystem/profile_builder.py`.

## Implemented source surface

New project directory:

`Patches/S142AKBMGHDiag1/`

The plugin contains exactly two Harmony postfix surfaces.

### 1. LLL selection postfix — sole deliberate gameplay mutation

Exact reflected target:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

The implementation preserves the C3F17.2 contract:

- exact LLL `1.7.12` dependency and expected DLL SHA-256 gate;
- exact accepted S1.42AB normalizer GUID/version/SHA-256 gate;
- exact declared target, weighted fields, readable moon/name/asset properties and method-body checks;
- exact `GetRandomExtendedDungeonFlowServerRpc()` selection caller;
- exact `TerminalManager.GetSimulationResultsText(ExtendedLevel)` simulation exclusion;
- exact runtime `ExtendedLevel` type plus `NumberlessPlanetName == "Black Mesa"`;
- exactly one existing `Greenhouse` wrapper;
- exact asset `GreenhouseFlow`;
- already-normalized rarity `100`;
- `HarmonyAfter` the accepted normalizer plus `Priority.Last`;
- all validation before the final fresh-list singleton mutation;
- one-way runtime refusal on an unknown/mismatched Black Mesa selection contract.

No flow/wrapper is created. No registration, config, package, RNG, RPC or global LLL state is changed.

### 2. installed-V81 TeleportPlayer postfix — observation only

Exact reflected target:

`EntranceTeleport.TeleportPlayer()`

The implementation:

- resolves exact global `EntranceTeleport` from `Assembly-CSharp`;
- hashes the loaded declaring assembly and requires SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- requires exact public parameterless `void` `TeleportPlayer()` with a method body;
- validates declared `entranceId`, `isEntranceToBuilding` and `exitScript` field contracts;
- remains inert until the exact Black Mesa x Greenhouse selection has succeeded;
- reads native post-call source/target ID, side, object name and coordinates;
- records success only for same-ID opposite-side native `exitScript` pairs for required IDs 0..3;
- tracks both traversal directions in diagnostic-only coverage bits;
- performs one typed active-`EntranceTeleport` snapshot after the first valid targeted traversal;
- emits `TOPOLOGY_OK` only when IDs 0..3 each have exactly one outside-side and one inside-side active entry;
- emits `TOPOLOGY_INCONCLUSIVE` on missing/duplicate required sides and never repairs topology.

The observer contains no reflection field write, no `FindExitPoint` invocation, no player teleport, no RPC and no entrance-ID rewrite.

## Pure policy layer

`SelectionPolicy.cs` contains only the deterministic selection decision and performs no list mutation.

`ObservationPolicy.cs` contains only:

- traversal post-state classification;
- required-ID topology counting;
- diagnostic traversal coverage bits.

The pure test executable covers the C3F17.2 required cases:

### Selection

- exact Black Mesa + real selection + one Greenhouse/GreenhouseFlow/100;
- other moon;
- `debugResults=false`;
- terminal simulation;
- unknown caller refusal;
- null/empty pool;
- null wrapper;
- missing/duplicate Greenhouse;
- wrong asset;
- rarity 65 and 0;
- input preservation on refusal;
- independent repeated pools.

### Observation

- inactive before target selection;
- null native `exitScript`;
- same-side pair;
- different-ID pair;
- out-of-scope ID;
- valid opposite-side same-ID pair;
- idempotent and bidirectional coverage tracking;
- exact unique topology for IDs 0..3;
- missing side;
- duplicate same-side entry;
- missing required ID;
- topology input preservation.

## Source-only CI gate

New workflow:

`.github/workflows/s142ak-bmghdiag1-source-static.yml`

It performs exactly:

1. pure `net8.0` policy test execution;
2. isolated `netstandard2.1` plugin compilation using the established BepInEx/HarmonyX/V81 GameLibs dependency set;
3. `AnalysisTools/validate_s142ak_bmghdiag1_source.py` fail-closed source-contract validation.

The source validator additionally requires:

- exactly two Harmony patch calls;
- no prefix/transpiler/PatchAll path;
- no reflection `SetValue` write;
- no manual `FindExitPoint`/`TeleportPlayer` invocation;
- all exact hashes, caller/identity markers and runtime markers;
- absence of `BuildSpecs/S1.42AK-BMGHDIAG1.json`;
- absence of `profile_builder.py` from this workflow.

Therefore this CI can prove source/test/buildability only. It cannot create or publish a Gale profile and cannot arm runtime.

## Exact-head CI result

The source implementation was first committed as `b4e33729b6dece918bae461cdf113836bd7393ab`.

Source workflow run #1 reached the substantive gates successfully:

- pure selection/observation policy tests: **success**;
- diagnostic plugin compile: **success**, 0 warnings / 0 errors;
- source validator: **failed** only because its textual forbidden-call check matched the documentation/string literal `EntranceTeleport.TeleportPlayer()` rather than an executable method invocation.

No C# runtime/source behavior was changed in response. Commit `65bab16f3b3a73d3fc281c59a5725e635b34c286` hardened only `AnalysisTools/validate_s142ak_bmghdiag1_source.py` to strip C# comments and string/character literals before checking forbidden executable call/write patterns.

On exact implementation head `65bab16f3b3a73d3fc281c59a5725e635b34c286`:

- source workflow run **#2 / 35846489106** completed `success`;
- pure policy tests completed `success`;
- plugin compile completed `success`;
- fail-closed source-contract validator completed `success`;
- all **16/16** PR workflows visible for that exact head completed `success`, including Knowledge Architecture and all existing V81/Black-Mesa/DunGen evidence-helper validation workflows.

This closes the C3F17.3 source/static gate. It does not prove loaded runtime hashes, actual Harmony arming/order, Greenhouse generation on Black Mesa, entrance traversal, topology, geometry or routing behavior.

## Lifecycle and scope preservation

- S1.42AK remains accepted/latest.
- `active_candidate` remains null.
- `runtime_test_outstanding` remains false.
- `BuildSpecs/current.json` remains disabled.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains S1.42AK.
- no package/config/profile bytes are changed.
- S1.42AB normalization remains unchanged.
- Black Mesa remains Dawn/native-owned and single-registered.
- Greenhouse availability config remains unchanged.
- B3 remains unchanged; Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.
- Black-Mesa/Pikmin routing recovery remains separate.
- no runtime test is requested.

## Next checkpoint

C3F17.4 should perform the next bounded provenance/build-readiness gate: freshly re-confirm the exact S1.42AK LLL 1.7.12 binary identity required by the contract and author the separate inactive candidate build request/static archive-delta gate. Do not arm runtime in that same checkpoint.
