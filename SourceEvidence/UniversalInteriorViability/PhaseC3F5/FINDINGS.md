# C3F5 — exact installed-V81 entrance pairing semantics and Black Mesa conditional topology result

**Status:** EXACT V81 PAIRING PREDICATE + EXIT-ID NUMBERING PROVEN / BLACK MESA 0..3 DUNGEON-SIDE TOPOLOGY CONDITIONALLY EXPLAINED / GLOBALPROP 1231 PER-FLOW APPLICABILITY STILL OPEN / NO MATRIX OR GAMEPLAY CHANGE  
**Date:** 2026-09-20  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`

## Bounded objective

C3F5 ingests the focused exact-installed-V81 entrance-pairing capture requested by C3F4 and combines it only with the already established DawnLib 0.9.25 and LethalLevelLoader 1.7.12 fire-exit adaptation evidence.

The purpose is to resolve:

- the exact installed-V81 opposite-side pairing predicate;
- how and when `RoundManager.SetExitIDs` assigns generated inside fire-exit IDs;
- whether Black Mesa moon-side IDs 0..3 can correspond to dungeon-side IDs 0..3;
- the exact proof boundary imposed by DunGen GlobalProp ID `1231`.

This remains source/static integration evidence. It does not change the B3 matrix and does not authorize a gameplay build or runtime test.

## Exact installed-V81 capture provenance

The local fail-closed helper published one evidence commit directly on PR #138:

- evidence commit: `aaba1f7f183480134316e9cfefb5a718d4b4263e`;
- parent PR head: `da649b21e999b96dfac8357e3148cb1c919fe157`;
- exact main at capture: `56355ff518ae4301a38d370be9561251f6f963c1`;
- directory: `SourceEvidence/VanillaV81/EntrancePairing/20260920T201535Z-930a43a4/`;
- focused report: `ENTRANCE_PAIRING_FOCUSED_DECOMPILE.txt`;
- report SHA-256 recorded by the manifest: `5a44ffc7263989c475d18e53cd443e3a891682ee88ab49bdf7d6b36f87fbb0fe`.

The commit is exactly one commit ahead of the previously verified PR head and adds only the focused report plus `MANIFEST.json`.

The manifest binds:

- `Assembly-CSharp.dll` SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- `Lethal Company.exe` SHA-256 `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam App ID `1966720`;
- Steam build ID `22825947`;
- reviewed appmanifest SHA-256 `132fafc473ec39e9a0e3a0f84dba9966f7ccf3088389220fae63ae681c0ed58e`;
- `ilspycmd 11.0.0.9375`.

No game binary, full-type decompile, local path or username was published.

Exact-head CI for the evidence commit is green, including Knowledge Architecture and the V81 helper validation workflow.

## Exact V81 pairing predicate

`EntranceTeleport.FindExitPoint()` scans all `EntranceTeleport` instances and accepts a candidate only when both conditions hold:

1. the candidate is on the opposite side:
   `candidate.isEntranceToBuilding != this.isEntranceToBuilding`;
2. the candidate has the same ID:
   `candidate.entranceId == this.entranceId`.

No name, GameObject path, position, tag, owner, moon key, dungeon type or package identity participates in the predicate.

The method does not break after a match; a later matching candidate can replace an earlier `exitScript`. Therefore unique opposite-side IDs remain the safe expected topology.

`TeleportPlayer()` calls `FindExitPoint()`. If no pair is found, the local player receives the blocked-entrance tip and teleportation returns without moving the player.

Therefore exact installed V81 treats opposite-side equality of `entranceId` as the decisive traversal pairing rule.

## Exact V81 inside-side exit numbering

`RoundManager.SetExitIDs(Vector3 mainEntrancePosition)`:

1. collects all `EntranceTeleport` objects;
2. sorts them by squared distance to the inside main-entrance position;
3. starts a counter at 1;
4. rewrites only entries satisfying:
   - `entranceId == 1`;
   - `isEntranceToBuilding == false`;
5. assigns those qualifying inside entries sequential IDs `1, 2, 3, ...` in the sorted order.

It does not create additional `EntranceTeleport` objects. It only renumbers already-existing inside-side objects whose pre-numbering ID is exactly 1.

The inside main entrance, ID 0, is not rewritten by this method.

## When numbering occurs

`RoundManager.SetLevelObjectVariables()` starts `waitForMainEntranceTeleportToSpawn()`.

That coroutine:

- waits while `FindMainEntrancePosition() == Vector3.zero`, for at most 15 seconds;
- then resolves the main entrance position again;
- invokes `SetExitIDs(mainEntrancePosition)`.

With default arguments, `FindMainEntrancePosition()` searches active `EntranceTeleport` objects for:

- `entranceId == 0`;
- `isEntranceToBuilding == false`.

Thus the exact capture proves that exit numbering is deferred until the generated inside main entrance can be found, or until the 15-second wait expires. It is not a pre-generation serialized-ID rewrite.

The focused capture does not include the caller of `SetLevelObjectVariables()`, so C3F5 does not claim a more precise whole-generation phase ordering than this proven local sequence.

## Reconciliation with DawnLib 0.9.25

C3F4 already established from exact DawnLib binary hook evidence plus version-aligned 0.9.25 source that Dawn runs `AdjustFireExits` before the original `DunGen.RuntimeDungeon.Generate`.

For the active moon, Dawn:

- collects moon-side alternate `EntranceTeleport` objects with `entranceId != 0`;
- reassigns them sequentially as `1..N`;
- finds selected DungeonFlow GlobalProps whose ID is `1231`;
- sets that fire-exit GlobalProp count to exactly `N`.

C3F2 proves Black Mesa's exact moon scene contains four outside-side entrances:

- main ID 0;
- alternate IDs 1, 2 and 3.

Therefore Dawn observes `N = 3` for Black Mesa and normalizes its moon-side alternate exits to IDs `1,2,3`.

## Reconciliation with LethalLevelLoader 1.7.12

C3F4 also established that LLL `DungeonLoader.PrepareDungeon` / `PatchFireEscapes` runs for non-External selected dungeon flows before `DungeonGenerator.Generate`.

That path:

- normalizes active moon-scene entrance IDs to a contiguous sequence with the main entrance as ID 0;
- sets GlobalProp `1231` to the number of non-main moon entrances.

LLL skips this own PrepareDungeon path when the **selected ExtendedDungeonFlow** is `ContentType.External`.

Dawn's later `RuntimeDungeon.Generate` hook is independent of that LLL skip.

Accordingly:

- non-External replacement flows can receive both the LLL preparation layer and Dawn's generation-time adaptation;
- the External Black Mesa flow skips LLL's own preparation path but is still subject to Dawn's shared adjustment.

## Conditional Black Mesa 0..3 topology result

The combined exact behavior now supports the following conditional sequence for a selected flow using the standard fire-exit mechanism:

1. Black Mesa supplies one main outside entrance plus three alternate outside entrances.
2. Dawn normalizes the alternate moon-side IDs to `1,2,3` and requests three fire exits by setting GlobalProp `1231` count to 3.
3. DunGen generates three corresponding inside-side fire-exit `EntranceTeleport` objects from that standard fire-exit GlobalProp/template.
4. Those generated inside-side fire exits enter `SetExitIDs` with pre-numbering `entranceId == 1`.
5. Exact V81 `SetExitIDs` renumbers them to `1,2,3`.
6. The inside main entrance remains ID 0.
7. Exact V81 `FindExitPoint` then pairs each moon-side ID 0..3 with the opposite-side dungeon ID 0..3 purely by equal ID and opposite `isEntranceToBuilding`.

Under those conditions, the earlier C3F2 static 0/1 versus 0/1/2/3 serialization asymmetry is fully compatible with a runtime 0..3 paired topology.

This is the first exact-V81 evidence explaining how additional dungeon-side IDs can arise without any BlackMesa.dll-specific rewrite.

## Critical GlobalProp 1231 proof boundary

The result above is **conditional**, not universal clearance.

Neither `RoundManager.SetExitIDs` nor `EntranceTeleport.FindExitPoint` creates missing fire exits.

Dawn's count adjustment can produce extra standard fire exits only if the selected DungeonFlow exposes a usable GlobalProp with ID `1231` whose generated fire-exit objects provide the expected inside-side `EntranceTeleport` template semantics.

In particular, C3F5 does not yet prove for every selectable flow that:

- GlobalProp `1231` exists;
- the prop is reachable/active in the effective selected DungeonFlow;
- count 3 is supported without generation failure;
- each generated instance produces one inside-side `EntranceTeleport`;
- those teleports enter V81 numbering with initial `entranceId == 1`;
- no duplicate opposite-side IDs remain after generation;
- the resulting exits are geometrically accessible and traversable.

C3F2's exact Black Mesa package scan proves one serialized inside ID 0 and one serialized inside ID 1, but it did not inventory the Black Mesa DungeonFlow's GlobalProp table. Therefore this checkpoint does not upgrade that observation into proof that the exact Black Mesa flow itself necessarily produces IDs 2/3 at runtime.

The same limitation applies more broadly to arbitrary replacement interiors.

## What C3F5 resolves

C3F5 closes the previously missing exact installed-V81 semantics:

- opposite-side pairing predicate is exact;
- inside fire-exit numbering rule is exact;
- numbering timing relative to inside-main-entrance discovery is exact within the captured sequence;
- Black Mesa's three moon-side alternate entrances are compatible with a standard generated three-fire-exit topology;
- the serialized absence of dungeon-side IDs 2/3 is no longer evidence of a missing vanilla/shared numbering mechanism.

Therefore it remains incorrect to classify Black Mesa moon IDs 2/3 as inherently broken or stranded from the static package shape alone.

## What remains unresolved

C3F5 does not prove:

- that Black Mesa IDs 2/3 always receive dungeon-side partners for every selected interior;
- that the Black Mesa packaged flow itself contains and successfully uses GlobalProp `1231`;
- that all 53 selectable interiors contain a usable standard fire-exit GlobalProp `1231`;
- that all 53 flows' generated fire exits use initial inside ID 1;
- successful three-fire-exit generation for every flow;
- geometry, traversal, routing or NavMesh safety on Black Mesa;
- universal Black Mesa-row compatibility.

Selection, generation, entrance topology and traversal remain separate proof layers.

## Matrix and lifecycle consequence

No authoritative B3 matrix cell changes from C3F5 alone.

Preserved state:

- B3 remains 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, 914 `NOT_YET_PROVEN`;
- the separately recorded External selection-supported pairings remain selection-only evidence;
- Black Mesa remains single-registered through its native owner path;
- no duplicate LLL registration is introduced;
- Shatteredrooms Experimentation/Embrion exclusions remain unchanged;
- S1.42AB InteriorWeightNormalization remains unchanged;
- S1.42AK remains accepted/latest;
- no gameplay candidate or runtime test is armed;
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

## Next bounded segment

Next C3 work should resolve the GlobalProp `1231` applicability boundary for the Black Mesa row before any topology promotion.

Start with repository-held exact flow/package evidence and determine, in a bounded inventory, which selectable DungeonFlows expose the standard fire-exit GlobalProp/template semantics required by the now-proven V81 numbering and pairing mechanism.

Do not infer all 53 flows from convention. Do not change the B3 matrix, start a gameplay build/run, duplicate-register Black Mesa, modify S1.42AB normalization, or relax unrelated owner hard blocks.
