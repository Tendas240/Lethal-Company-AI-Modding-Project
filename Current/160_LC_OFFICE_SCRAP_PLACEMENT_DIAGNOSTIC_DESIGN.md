# LC Office Scrap Placement Diagnostic Design

**Date:** 2026-09-18  
**Status:** DESIGN COMPLETE / NOT IMPLEMENTED / NOT BUILT / NOT ARMED  
**Accepted parent:** S1.42AK — `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
**Accepted parent SHA-256:** `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
**Selected scope:** LC Office Scrap Quantity/Distribution Investigation  
**Count finding:** `Current/159_LC_OFFICE_SCRAP_EXISTING_EVIDENCE_FINDING.md`  
**Patch-safety authority:** `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Purpose

The existing evidence shows no LC Office-specific low generated-count regression. The remaining question is whether the 14-15 generated objects are spatially clustered, concentrated on one floor, placed in low-traffic rooms or otherwise difficult to discover.

This design collects placement evidence only. It must not alter scrap quantity, rarity, value, spawn points, object transforms, dungeon generation, player state or network state.

## Exact diagnostic parent and deterministic selection

The diagnostic must be derived directly from exact accepted **S1.42AK**, never from S1.42AJ-DIAG1 or DIAG2 profile bytes.

To avoid waiting for a natural LC Office roll, rebuild and add the already reviewed source project:

`Patches/S142AJDiag1OfficeSelection/S142AJDiag1OfficeSelection.csproj`

That plugin remains diagnostic-only. Its exact contract is already documented in `BuildSpecs/S1.42AJ-DIAG1_PLAN.md`: Offense only, post-LLL viability/post-normalization, exact LC Office / `OfficeDungeonFlow` identity, native downstream selection retained, no registration/RNG/RPC/config changes. S1.42AK still contains the accepted normalizer DLL at SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

Reusing this reviewed selection source is narrower than creating a second force-selection implementation. The new placement logger must hard-depend on the selection diagnostic and on `tendas.s139.compatibilityfixes`.

## New diagnostic logger

Proposed project:

`Patches/S142AKDiagScrapPlacement/S142AKDiagScrapPlacement.csproj`

Proposed plugin GUID:

`tendas.lethalcompany.s142akdiagscrapplacement`

The logger has exactly one Harmony target:

`RoundManager.SpawnScrapInLevel()`

### Why this target

The accepted S1.42AK stack already patches this exact method in `S139CompatibilityFixes.NaturalScrapFilterPatches`. That patch temporarily filters natural scrap candidates in a prefix and restores the list in its postfix. This establishes `SpawnScrapInLevel` as the project-owned exact natural-scrap generation surface already used by the accepted stack.

The alternative `RoundManager.FinishGeneratingNewLevelClientRpc` is deliberately rejected. V81 source evidence in `SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T143200Z-a693b4b9/` shows that method also owns loading UI, door sequence, level variables, enemy reset/prediction and other lifecycle work. It is broader than necessary.

No RPC method is patched. No prefix or transpiler is introduced. No foreign component is disabled.

### Arming validation

Before installing the postfix, the plugin must validate the exact declared method contract:

- declaring type is exactly `RoundManager`;
- method name is exactly `SpawnScrapInLevel`;
- declared-only lookup;
- instance method;
- zero parameters;
- return type `void`;
- non-null method body.

The installed Harmony patch must be verified by owner GUID after patching. Its postfix must declare ordering after `tendas.s139.compatibilityfixes` so the accepted S139 temporary pool restoration remains complete before the diagnostic schedules any observation.

If any contract is missing or ambiguous, unpatch/refuse with one explicit `[ScrapPlacementDiag] REFUSED` marker. No fallback target is allowed.

## Read-only sampling contract

The Harmony postfix performs no object scan itself. It only schedules one diagnostic coroutine for the generated round.

The coroutine performs at most two scene scans:

1. snapshot A after approximately 16 seconds;
2. snapshot B approximately four seconds later.

The 16-20 second window is chosen from repository runtime evidence: the targeted Office diagnostics took roughly 14.5 seconds between the initial `Number of scrap to spawn` line and final scrap-value replication; accepted S1.42AK Spooky Manor took roughly 12.2 seconds. The extra margin avoids inspecting the early incomplete set.

This is bounded diagnostic sampling, not per-frame polling.

Snapshot stability is based on the set of Unity instance IDs for objects satisfying:

- `GrabbableObject`;
- non-null `itemProperties`;
- `itemProperties.isScrap == true`.

If the two ID sets differ, emit `[ScrapPlacementDiag] INCONCLUSIVE unstable spawned set` and do not emit a final placement-complete marker. Do not modify or freeze any object to make the sets agree.

## Per-object evidence

For every final scrap object in stable snapshot B, log one structured `[ScrapPlacementDiag][ITEM]` line containing:

- Unity instance ID;
- item name;
- GameObject name;
- scrap value where available from the normal public game contract;
- world position `x,y,z`;
- current transform-parent hierarchy path;
- nearest `EntranceTeleport` by absolute Y difference, with teleport name/path/position and delta-Y;
- support-surface collider name and hierarchy path from a short downward read-only physics query.

The support query must ignore colliders belonging to the scrap object's own transform hierarchy. It must not move the object or change collision/layers.

## Floor and room context

Enumerate `EntranceTeleport` objects once in snapshot B and log each as `[ScrapPlacementDiag][ANCHOR]` with GameObject name, full transform hierarchy path and world position.

LC Office runtime evidence already shows distinct floor anchors with large vertical separation. Nearest-anchor-by-Y is therefore a diagnostic correlation, not a gameplay mutation or authoritative floor rewrite.

The support-surface collider path supplies a second independent room/tile clue. No attempt is made to alter or label dungeon tiles at runtime.

## Required summary markers

A valid run must contain:

- `[AJDIAG1] ARMED`;
- `[AJDIAG1] SELECTED Offense LC Office / OfficeDungeonFlow`;
- `[ScrapPlacementDiag] ARMED exact RoundManager.SpawnScrapInLevel read-only postfix`;
- snapshot A count;
- snapshot B count;
- stable ID-set confirmation;
- one `[ITEM]` line per stable scrap object;
- one or more `[ANCHOR]` lines;
- `[ScrapPlacementDiag] COMPLETE stable=<count>`.

A `REFUSED`, `INCONCLUSIVE`, selection refusal or non-Office selection invalidates placement conclusions.

## Patch Safety Review

**Exact method/component:** declared `RoundManager.SpawnScrapInLevel()`, postfix only.

**Smallest safe surface:** the accepted project already uses the same exact method for natural-scrap filtering. The new postfix does not alter arguments, result, fields or spawned objects; it only schedules bounded delayed observation.

**Inherited/base lifecycle:** not applicable to disabling or replacing a MonoBehaviour lifecycle; the original method always completes normally before the diagnostic postfix.

**Known secondary responsibilities:** S139 temporarily edits/restores `currentLevel.spawnableScrap` around this same call. Harmony ordering must leave that restoration untouched before observation scheduling.

**Adjacent behavior that must remain working:** normal S139 ScrapFilter markers; normal reported `Number of scrap to spawn`; final `clientRPC scrap values length`; item pickup; LC Office traversal/elevator; no new exception/log flood.

**Forbidden broader alternatives:** `FinishGeneratingNewLevelClientRpc` suppression/replacement, RPC interception, per-frame scene scans, transform mutation, spawn-list mutation, amount/value/rarity changes, component disabling, guessed reflection fallbacks.

## Static implementation gate

Before any runtime arming:

1. compile the new project cleanly against the repository's V81 GameLibs package;
2. compile the existing AJDIAG1 selection source cleanly;
3. verify exact accepted S1.42AK parent SHA;
4. build a separately named diagnostic artifact from S1.42AK with only the two diagnostic DLL additions;
5. verify no existing archive member changes or removals;
6. verify S139 and accepted normalizer bytes remain identical to S1.42AK;
7. verify new logger source contains no mutation of `spawnableScrap`, `scrapValue`, object transforms, network ownership or RPC state;
8. verify only the exact `SpawnScrapInLevel` postfix is installed by the new logger;
9. record both diagnostic DLL hashes;
10. keep `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, active-candidate state and runtime-test state unchanged until a separate explicit arming step.

## Runtime interpretation

The first goal is distribution diagnosis, not acceptance of a gameplay change.

After a valid run, analyze:

- total stable items;
- count per nearest floor anchor;
- X/Z spread within each floor;
- repeated/near-identical positions;
- support collider/room paths;
- whether the player's discoverability impression aligns with a strong floor/room concentration.

Only after that evidence may the project decide whether there is a placement defect, a discoverability issue inherent to the interior layout, or no reproducible LC Office-specific problem.

No quantity increase is authorized by this diagnostic design.
