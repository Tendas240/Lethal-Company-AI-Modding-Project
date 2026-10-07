# C3F4 — integration-level entrance pairing precapture gate

Status: bounded integration semantics identified; exact installed-V81 pairing bodies still require focused capture.

## Scope and authority

Implementation parent PR #138 HEAD: `510672a1e2908b1fa5938d2997cc13e4ee605eab`. Accepted gameplay baseline remains S1.42AK. No gameplay build, runtime test, universal override or B3 matrix change is authorized by this checkpoint.

C3F2 established the exact Black Mesa 3.4.4 serialized topology: dungeon side IDs 0/1 with `isEntranceToBuilding=false`, moon side IDs 0/1/2/3 with `isEntranceToBuilding=true`. C3F3 then found no BlackMesa.dll-local managed-IL/Harmony path that rewrites or reconciles those IDs. C3F4 therefore moves one layer outward and asks how the shared V81/Dawn/LLL generation and pairing stack handles moon-side entrance counts.

## DawnLib 0.9.25 general fire-exit adaptation

Existing exact-binary evidence in `SourceEvidence/UniversalInteriorViability/PhaseC3E3D/OXYDE_OWNER_REGISTRATION_IL.json` proves that the SHA-256-bound DawnLib 0.9.25 assembly hooks `DunGen.RuntimeDungeon.Generate` and invokes `Dawn.DungeonRegistrationHandler::AdjustFireExits` before the original Generate call.

The already pinned version-aligned DawnLib 0.9.25 source commit `810613e556ecc357eac25e97c25a3bb90516f071` shows the bounded method semantics:

- find the object tagged `OutsideLevelNavMesh`;
- collect child `EntranceTeleport` components whose `entranceId != 0`;
- assign those moon-side alternate entrances sequential IDs `1..N`;
- find dungeon-flow GlobalProps with ID `1231` (`DawnDungeonInfo.FireExitGlobalPropID`);
- set that global-prop count to exactly `N`.

For Black Mesa's exact serialized moon surface, N is three. Therefore the static C3F2 absence of pre-serialized dungeon-side IDs 2/3 is not by itself the effective runtime entrance count.

## LethalLevelLoader 1.7.12 adaptation

The existing C3B/C3E3E release-source binding remains `f9998b91adf242cd8d735f4e697d55b32b94bfac` for LLL 1.7.12.

Its `DungeonLoader.PrepareDungeon` runs before `DungeonGenerator.Generate` for non-External selected dungeon flows. `PatchFireEscapes`:

- reads active moon-scene EntranceTeleports;
- moves the main entrance to the end of its working list;
- reassigns all scene entrance IDs to a contiguous sequence ending with main ID 0;
- sets dungeon-flow GlobalProp ID 1231 to exactly the number of non-main moon entrances.

LLL explicitly skips this PrepareDungeon path when the selected ExtendedDungeonFlow is `ContentType.External`. Dawn's observed RuntimeDungeon.Generate hook is a separate shared layer and is not gated by that LLL check.

## What this resolves

The absence of a BlackMesa.dll-local rewrite does **not** establish a missing shared reconciliation path. Both relevant shared integration layers contain explicit moon-entrance-count → fire-exit-generation adaptation.

This supports a narrower topology model: for ordinary generated interiors, the meaningful question is not how many EntranceTeleport objects were serialized in the source dungeon asset, but whether the selected flow exposes the standard fire-exit GlobalProp 1231 and how exact installed V81 assigns/matches the generated inside EntranceTeleport IDs against the moon-side IDs.

## Remaining exact-V81 gate

Existing repository V81 captures expose the `RoundManager.SetExitIDs` and `waitForMainEntranceTeleportToSpawn` declarations but not their bodies. Existing focused generation/spawning captures do not contain the required entrance-pairing bodies.

Historical/non-version-bound decompilation is insufficient for final classification, so this checkpoint does not elevate its familiar pairing behavior to exact V81 proof.

The new `AnalysisTools/InspectEntrancePairingV81.ps1` therefore captures only:

RoundManager:
- `SetExitIDs`
- `waitForMainEntranceTeleportToSpawn`
- `FindMainEntrancePosition`
- one-hop direct callers of those methods inside RoundManager

EntranceTeleport:
- `FindExitPoint`
- `TeleportPlayer`
- one-hop direct callers of those methods inside EntranceTeleport

The helper inherits the reviewed installed-V81 provenance contract from the prior RoundManager helper: exact Assembly-CSharp, executable, Steam App/Build, reviewed appmanifest hashes and pinned ilspycmd 11.0.0.9375. It rejects throw-null reference stubs, missing methods, oversized extraction and unreviewed provenance drift. Publication is limited to one focused text report plus one manifest.

Unlike the older source-evidence helper pattern, this helper is constrained to the existing PR #138 branch. It re-reads the PR and refuses publication if the PR is closed/merged, the head branch differs, the repository differs, or the head SHA moves during capture.

## Proof boundary

This checkpoint does not yet prove the exact installed-V81 pairing predicate or the final Black Mesa runtime topology. It also does not prove that every one of the 53 selectable interiors contains a usable GlobalProp 1231, that three fire exits always generate successfully, or that traversal/routing/NavMesh is safe.

Selection, generation, entrance topology and traversal remain separate evidence layers.

## Next bounded step

Validate the new helper/workflow on PR #138, then perform the focused installed-V81 capture. After publication, review the exact `SetExitIDs` / `FindExitPoint` bodies together with the already established Dawn/LLL adaptation before deciding whether Black Mesa's External row can be topologically classified further.

No gameplay run or matrix change is authorized.
