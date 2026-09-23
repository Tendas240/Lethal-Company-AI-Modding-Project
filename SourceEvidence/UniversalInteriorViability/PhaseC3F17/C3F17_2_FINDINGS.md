# C3F17.2 — exact Black Mesa x Greenhouse diagnostic-candidate contract

**Status:** CANDIDATE CONTRACT AUTHORED AND STATICALLY RECONCILED / SOURCE NOT YET IMPLEMENTED / NO BUILD OR RUNTIME AUTHORIZATION  
**Date:** 2026-09-23  
**Accepted baseline:** S1.42AK  
**Working PR:** #138 / `scope/universal-interior-phase-c3a-dawn-tags`  
**Parent head:** `b2cb00f033d6b267ad8d29baa78a227d11c53ee4`

## Bounded objective

C3F17.2 converts C3F17.1's selected DIAG1-style mechanism into an exact implementation contract for a future diagnostic candidate. It does not implement the plugin source, build a profile, arm the runtime controller, change the B3 matrix or request gameplay.

The human contract is `BuildSpecs/S1.42AK-BMGHDIAG1_PLAN.md`. The machine mirror is `CANDIDATE_CONTRACT.json` in this directory.

## Fresh repository/lifecycle gate

At segment start:

- `main` remains `56355ff518ae4301a38d370be9561251f6f963c1`;
- PR #138 remains open, draft, unmerged and mergeable;
- PR head is `b2cb00f033d6b267ad8d29baa78a227d11c53ee4`;
- all 15 visible PR workflow runs on that head are completed/success;
- S1.42AK remains accepted/latest;
- `active_candidate=null`;
- `runtime_test_outstanding=false`;
- build controller remains disabled.

The current lifecycle therefore authorizes design/static contract work only.

## Exact candidate identity

Proposed diagnostic-only ID:

`S1.42AK-BMGHDIAG1`

Parent is exact accepted S1.42AK:

- profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`;
- SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

The candidate is not a balanced successor and must never become a parent for balanced gameplay work.

## Selection implementation contract

C3F17.1's DIAG1-style singleton mechanism is retained without broadening.

The only gameplay-mutating Harmony target is the exact static declared LLL query:

`DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

The future implementation must:

1. let LLL construct the full fresh viable pool;
2. let accepted S1.42AB normalization complete unchanged;
3. run as a postfix after the normalizer with `Priority.Last`;
4. require the exact server selection caller and `debugResults=true`;
5. exclude terminal simulation and all non-selection callers;
6. require exact Black Mesa `ExtendedLevel` runtime type plus `NumberlessPlanetName == "Black Mesa"`;
7. require exactly one viable `DungeonName == "Greenhouse"` entry whose asset is exactly `GreenhouseFlow` and whose already-normalized rarity is exactly 100;
8. only then clear the fresh result list and re-add that same wrapper object.

No new flow/wrapper, registration, config, package, RNG, RPC or network-owner change is permitted.

## Dependency and provenance result

### Accepted normalizer

The current normalizer contract is exact and sufficient:

- GUID `tendas.lethalcompany.s142abinteriorweightnormalization`;
- version `1.0.0`;
- accepted DLL SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`.

Its source confirms the same exact LLL query target and positive-rarity-to-100 behavior. The diagnostic therefore has a precise ordering anchor and must refuse unless exactly one normalizer postfix is already installed.

### LethalLevelLoader

The required package remains `IAmBatby-LethalLevelLoader 1.7.12`. S1.42AJ-DIAG1's proven implementation contract expected DLL SHA-256:

`b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`

S1.42AK's authorized delta from S1.42AJ contains no package addition/removal/version transition, so C3F17 expects that same binary. However C3B explicitly recorded that its accepted-profile LLL package binary was not independently SHA-bound in that checkpoint. The contract therefore does not overclaim current AK binary identity: the later implementation/build gate must freshly materialize the S1.42AK graph and independently re-confirm the exact LLL DLL hash before arming. Hash mismatch is a refusal, not permission to retarget silently.

## Black Mesa identity decision

The implementation will deliberately guard on the exact passed LLL `ExtendedLevel` type plus readable `NumberlessPlanetName == "Black Mesa"`, combined with the exact server-selection caller.

A broader reflection path to recover Dawn's namespaced key from the LLL bridge is not added merely to obtain a second string check. The repository already independently proves the underlying package identity as:

- Dawn/Dusk key `black_mesa:black_mesa`;
- planet `Black Mesa`;
- scene `BlackMesaScene`.

The diagnostic keeps Dawn/native ownership intact and requires the user to route to Black Mesa normally.

## Greenhouse identity decision

The exact Greenhouse guard is:

- display name `Greenhouse`;
- flow asset name `GreenhouseFlow`;
- exactly one matching viable wrapper;
- final rarity exactly `100`.

This is stronger than forcing by name alone and guarantees that the diagnostic only selects a flow already admitted by normal LLL viability and already processed by the accepted normalizer.

## Minimum observation gap and solution

C3F16's future runtime contract requires direct practical use of the main plus three Black Mesa alternate pairs. Existing LLL/DunGen/PathfindingLib logs can establish selection, generation and routing signals, but they do not unambiguously prove which `EntranceTeleport` IDs the local player actually traversed.

The minimum justified extra observation surface is therefore one **read-only postfix** on exact installed-V81:

`EntranceTeleport.TeleportPlayer()`

C3F5's exact installed-V81 evidence binds `Assembly-CSharp.dll` SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731` / Steam build `22825947`, and proves `TeleportPlayer()` performs native `FindExitPoint()` pairing before moving the local player.

The observer activates only after the exact target selection succeeds. It performs no field writes and no manual pairing/teleport/RPC call. After the original method returns, it records a successful traversal only when native `exitScript` is non-null, has the same `entranceId`, and lies on the opposite `isEntranceToBuilding` side.

On the first successful targeted traversal, it performs one read-only active-teleport snapshot. Runtime topology is strongly observed only if IDs 0,1,2,3 each have exactly one outside-side and one inside-side active teleport. Missing/duplicate pairing logs `TOPOLOGY_INCONCLUSIVE`; the observer never repairs it.

This additional hook exists for evidence only. The sole deliberate gameplay mutation remains the LLL returned-list singleton filter.

## Required runtime markers designed

Future implementation markers are fixed as:

- `[BMGHDIAG1] ARMED`;
- `[BMGHDIAG1] SELECTED Black Mesa Greenhouse / GreenhouseFlow; normalized rarity=100; pool=<N>->1`;
- `[BMGHDIAG1] TRAVERSED id=<id> ...`;
- `[BMGHDIAG1] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4`;
- `[BMGHDIAG1] REFUSED TO ARM`;
- `[BMGHDIAG1] REFUSED selection`;
- `[BMGHDIAG1] TOPOLOGY_INCONCLUSIVE ...`.

The future observer also tracks IDs 0..3 in both directions as diagnostic coverage bits without changing gameplay.

## Static contract review

The contract satisfies the permanent patch-safety rule:

- selection interception is the smallest proven query surface;
- original LLL responsibilities complete before mutation;
- accepted normalizer remains owner of equal effective weighting;
- native RPC/network selection remains owner after the filtered result is returned;
- Black Mesa remains Dawn/native-owned;
- Greenhouse must already be normally viable;
- the second hook is observation-only and runs after native teleport logic;
- no whole component/lifecycle is disabled;
- no state repair, ID rewrite, teleport retry or routing repair is introduced;
- unknown target/caller/hash/identity contracts fail closed.

The future source must expose pure policy helpers and test negative cases for moon/caller/list/identity/rarity selection gates plus observer/topology gates before any build is considered.

## Runtime proof contract preserved

A later separately armed session must still establish:

1. exact Black Mesa + Greenhouse identity;
2. successful DunGen generation;
3. unique opposite-side active pairs for IDs 0..3;
4. normal main entry and exit;
5. direct player use of alternate IDs 1,2,3, preferably both directions where practical;
6. no severe clipping/inaccessible required endpoint geometry, with user observation retained for visual geometry quality;
7. no new severe/persistent target-attributable routing/NavMesh failure, using existing routing signals without reopening Black-Mesa/Pikmin repair.

Static design success is not runtime clearance.

## Preserved boundaries

- S1.42AK remains accepted/latest and unchanged.
- `S1.42ABInteriorWeightNormalization` remains unchanged.
- Black Mesa remains Dawn/native-owned and single-registered.
- Greenhouse config remains unchanged.
- Shatteredrooms x Experimentation / Embrion remain untouched.
- B3 remains unchanged; Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.
- no `KNOWN_TECHNICAL_RESTRICTION` is inferred.
- C3F10D exhausted restoration paths remain closed.
- Black-Mesa/Pikmin routing recovery remains separate.
- no plugin source is implemented in this checkpoint.
- no candidate profile is built or armed.
- no runtime test is requested.

## Next bounded checkpoint

Perform **C3F17.3 — diagnostic source + pure static-test implementation**.

Implement one project-local plugin exactly to `BuildSpecs/S1.42AK-BMGHDIAG1_PLAN.md` and `CANDIDATE_CONTRACT.json`, including the selection policy and read-only traversal/topology observer policy. Compile/test infrastructure may be authored and CI-validated, but do not automatically build a Gale candidate, change `BuildSpecs/current.json`, arm runtime or request gameplay in the same segment.
