# S1.42AI-DIAG1 BCMER exact event-execution review

**Status:** EXACT BCMER EXECUTION + INSTALLED-SET CONSUMER REVIEW COMPLETE / FORCED-FORCED-SIDE-ADDITIONAL-RUNTIME-CUSTOM EXECUTION GATE CLOSED / NO BCMER EXECUTION PATCH REQUIRED / PATCH SAFETY PARTIAL / NOT BUILD READY  
**Canonical main reviewed:** `15cd35a62a995b1895634d40a661a880aa6f087d`  
**Exact S1.42AI profile SHA-256:** `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
**Analysis branch:** `analysis/s142ai-bcmer-execution-exact`  
**Final analysis head:** `11959ac47e056394710b62070dd80e228c9eb3f5`  
**Decompiler:** `ilspycmd 11.0.0.9375`

## Scope

This review closes the remaining BCMER event-execution uncertainty for the planned `S1.42AI-DIAG1` ShyGuy-only diagnostic. It answers whether the exact installed S1.42AI stack contains an internal or external execution route that would require a dedicated BCMER Harmony interception patch after the diagnostic configuration disables every non-ShyGuy event, disables custom-event loading and heat forcing, clears ShyGuy `Events To Spawn With`, and requests exactly one normal event draw with no bonus draws.

It does **not** authorize DIAG1 implementation or build. Enemy-spawn interception safety, exact Shy Guy runtime identity/source-to-DLL provenance, and final host/client-safe interception selection remain separate open gates.

## Exact BCMER full-assembly capture

Successful Actions run `34716488701` on analysis head `49521b08e1c1a268aedc2153b4ab01e6fa93c132` re-fetched the exact package and produced artifact `10304724235` / `s142ai-bcmer-execution-exact`.

Artifact digest / independently re-downloaded ZIP SHA-256:

`35ca8ec171fc40f8d9b0c9d2a9f1af3ad062f54c56c63a22e1424012c20cc116`

Exact package identity:

- package: `SoftDiamond-BrutalCompanyMinusExtraReborn` 1.71.0;
- package ZIP SHA-256: `fa3d7727eef5ff023291caa7b0a306194b3a3826b8361af5bc42c7a6b58b1534`;
- assembly: `BrutalCompanyMinus.dll`;
- assembly SHA-256: `c344d3fdddd1f4ac32c80d3ec24eee54810c4cfd91a13594d88579fa23bbf148`;
- complete C# SHA-256: `ea8f0415d25cf5a468e6ba276ead7b4586819e531eaa6ed7b5ab6bafca6d3fb4`;
- complete IL SHA-256: `4a7d6e9059ef7344c00f0e419d42a2d238e8bed669a4963ab814907686169ace`;
- complete C#: 38,858 lines;
- complete IL: 164,206 lines.

The artifact preserves complete C#, complete IL, focused execution contexts and its own `VERIFICATION.json`. The repository stores the compact review and verification metadata only; the complete third-party decompile remains in the immutable Actions artifact.

## Exact `MEvent.Execute()` execution topology

The complete IL contains exactly three direct calls to `BrutalCompanyMinus.Minus.MEvent::Execute()`:

1. `EventManager.ApplyEvents(...)` — normal chosen events and normal additional/side events are executed through this helper. `ModifyLevel(...)` calls `ApplyEvents(list)` and `ApplyEvents(additionalEvents)`.
2. `EventManager.ModifyLevel(...)` — every entry already present in `forcedEvents` is executed directly with `forcedEvent.Execute()`.
3. `EventManager.ModifyLevel(...)` — each forced event's `EventsToSpawnWith` member is resolved with `MEvent.GetEvent(name)` and immediately executed.

The exact direct IL call lines in the captured full assembly are `44153`, `46848`, and `46865`. No fourth direct `MEvent.Execute()` call site exists in the complete captured IL.

This distinction matters: broad suppression of `MEvent.Execute()` or all of `ModifyLevel()` would be wider than the actual diagnostic requirement. `ModifyLevel()` also owns unrelated difficulty, power, scrap, weather/UI and synchronization-related work, so skipping it wholesale remains prohibited by the project patch-safety policy.

## Active-event-list gate

Configuration initialization first registers vanilla/modded events and conditionally custom events, then applies each event's `Event Enabled?` value. Disabled events are copied to `EventManager.disabledEvents`; only enabled events are retained when `EventManager.events` is replaced with the filtered list.

All reviewed force/name entry points relevant to DIAG1 then resolve through that active list:

- public `API.ForceEvents(string[])` adds only `EventManager.GetEventsByName(eventNames)` results to `forcedEvents`;
- heat forcing parses configured names and adds only `GetEventsByName(names)` results;
- internal `EventManager.GetEventsByName(params string[])` filters only `EventManager.events`;
- public API `GetEventsByName(string)` searches only `EventManager.events`;
- `MEvent.GetEvent(string)` searches only `EventManager.events` and otherwise returns `Nothing`;
- terminal command `MEVENT` iterates only `EventManager.events` before adding a forced event.

Therefore a non-ShyGuy event disabled by the DIAG1 overlay is not name-resolvable through these reviewed force surfaces after initialization.

## Normal additional / side events

`ChooseEvents(...)` begins its candidate pool from `EventManager.events`. For a normally chosen event, names in `EventsToSpawnWith` are converted into an additional-event list. Before returning, entries present in `disabledEvents` are removed from that normal additional-event list. `ModifyLevel(...)` then executes both the selected list and `additionalEvents` through `ApplyEvents(...)`.

For DIAG1, `[ShyGuy] Events To Spawn With` is required to be empty. This closes both the normal side-event expansion and the separate forced-side direct-execution path without patching BCMER's lifecycle.

## Heat forcing

Heat forcing occurs inside `ChooseEvents(...)` only when `Scale by Heat?` is enabled, the current heat equals the configured maximum and `Force event at max heat?` is enabled. Even then, configured names are resolved through active-list-only `GetEventsByName(...)`.

DIAG1 additionally requires `Scale by Heat? = false`, `Force event at max heat? = false`, and an empty heat force list. That configuration removes the heat-force trigger itself and leaves the active-list restriction as defense in depth.

## Runtime/custom-event loading

Custom JSON events are loaded only during configuration initialization under `if (Enable Custom Events?.Value)`. The complete BCMER assembly contains exactly one `Directory.GetFiles(customEventsFolder)` occurrence and zero `FileSystemWatcher` occurrences. No later file-watcher or second runtime JSON load/reload path was found in the complete captured C# assembly.

DIAG1 requires `Enable Custom Events? = false`, so those JSON events are not added to `EventManager.customEvents` or the active `EventManager.events` list during initialization.

This is a static exact-assembly conclusion. It is not a mathematical proof against a method name/string assembled wholly at runtime by arbitrary external reflection; that qualification is addressed by the installed-set consumer scan below.

## Exact installed-set external consumer scan

Successful Actions run `34716828573` on final analysis head `11959ac47e056394710b62070dd80e228c9eb3f5` scanned the exact installed S1.42AI package/DLL inventory and produced aggregate artifact `10303989823` / `s142ai-bcmer-external-event-consumers`.

Artifact digest / independently re-downloaded ZIP SHA-256:

`74303c27f635690df1178e30be7430c0146510cd3187ce42465b15f101fe4b3d`

Coverage:

- enabled packages scanned: **183**;
- embedded project DLLs scanned: **5**;
- managed DLLs scanned: **224**;
- raw candidate assemblies: **1**;
- external candidate assemblies: **0**.

The sole raw candidate is BCMER itself and reproduces the same exact DLL, C# and IL hashes as the full-assembly capture. Across every external installed managed assembly the scan found:

- callers of `API.ForceEvents`: **0**;
- callers of `API.RegenerateEvents`: **0**;
- callers of `MEvent.Execute`: **0**;
- callers of `MEvent.GetEvent`: **0**;
- constructions of `GeneralCustomEvent`: **0**;
- static reflection-like BCMER execution candidates: **0**.

The scan is complete for the exact static S1.42AI installed assembly set. Arbitrary strings or reflection targets generated entirely at runtime are outside static proof; no static indicator of such a route was found.

## Gate decision for S1.42AI-DIAG1

With the planned diagnostic configuration simultaneously enforcing:

- every non-ShyGuy BCMER event disabled;
- `[ShyGuy]` enabled;
- `[ShyGuy] Events To Spawn With` empty;
- `Enable Custom Events? = false`;
- heat scaling/heat forcing disabled and the heat force list empty;
- exactly one normal event draw and no bonus draws;

the **forced / forced-side / additional / runtime-custom BCMER execution gate is CLOSED for the exact static S1.42AI stack**.

**No dedicated BCMER event-execution Harmony patch is required for S1.42AI-DIAG1.** In particular, do not patch or broadly skip `MEvent.Execute()`, `EventManager.ModifyLevel()`, or the whole BCMER selection/execution lifecycle. Such intervention would add regression surface without a remaining evidenced execution bypass.

This closure is profile/version bounded. Any BCMER version change, package-set change, profile change affecting the event configuration, or new static external consumer evidence must reopen the conclusion.

## Patch-safety consequence and remaining gates

This review closes one bounded gate only. Overall patch safety remains **PARTIAL / NOT_BUILD_READY**.

Remaining work is:

1. preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design;
2. select and statically validate the smallest host/client-safe enemy-spawn interception points across the already reviewed native and mod owner paths;
3. only after those gates reach `BUILD_READY`, implement and repository-natively build `S1.42AI-DIAG1`.

The broad prohibitions in `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` remain fully in force. This review does not authorize blanket `EnemyAI` lifecycle suppression, global `NetworkObject.Spawn` suppression, global per-frame scans, post-spawn cleanup as proof of prevention, or broad BCMER execution skipping.

No build-controller transition, runtime-controller transition, Gale import or gameplay test is authorized by this checkpoint. Existing S1.42AI and its full-normal runtime gate remain unchanged.
