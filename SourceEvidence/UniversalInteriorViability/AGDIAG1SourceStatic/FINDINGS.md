# S1.42AK-AGDIAG1 Source / Pure-Static Findings

**Date:** 2026-10-04  
**Status:** SOURCE / PURE-STATIC PASS / DIAGNOSTIC ONLY / NOT BUILT / NOT ARMED / NEVER ACCEPT  
**Authority:** `Current/254_S1.42AK_PHASE_C_ART_GALLERY_AGDIAG1_SOURCE_STATIC_IMPLEMENTATION_AUTHORIZATION.md`  
**Implementation base:** `17ef86a6895371d3187e4d01ae78ff15c6e16e55`

## Implemented source contract

The isolated source root is `Patches/S142AKAGDiag1/`.

The implementation follows the approved selector-only BMDSFIX1-DIAG1 architecture with the frozen AGDIAG1 identity:

- build: `S1.42AK-AGDIAG1`;
- assembly/project: `S142AKAGDiag1`;
- GUID: `tendas.lethalcompany.s142akagdiag1`;
- version: `1.0.0`;
- marker: `[AGDIAG1]`;
- classification: `DIAGNOSTIC ONLY / NEVER ACCEPT`.

Exactly one Harmony patch call exists. It targets LLL `DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` as a postfix, ordered after the accepted S1.42AB normalizer at `Priority.Last`.

The selector is Offense-specific and may retain only one already-returned viable `Art Gallery` wrapper whose exact asset is `MuseumInteriorFlow` and whose final normalized rarity is `100`. The same existing wrapper is retained; the policy does not construct a replacement.

## Fail-closed pure policy coverage

The pure test program covers:

- positive Offense Art Gallery / MuseumInteriorFlow / rarity-100 index selection;
- proof that the returned index identifies the same existing wrapper;
- `debugResults=false` inert behavior;
- non-Offense inert behavior;
- terminal-simulation exclusion;
- unknown selection caller refusal;
- null/empty pool refusal;
- missing accessor refusal for each accessor;
- null wrapper refusal;
- missing Art Gallery refusal;
- duplicate Art Gallery refusal;
- asset mismatch refusal;
- rarity 65/0 refusal;
- repeated independent pools without mutation.

Refusal tests snapshot the pool and prove count plus wrapper identity/order remain unchanged.

## Static safety surface

`Patches/S142AKAGDiag1/PATCH_SAFETY_REVIEW.md` records the project-local safety analysis.

The intended sole mutation remains the fresh already-viable/normalized return list after every guard has passed. No availability, registration, global rarity, RNG, RPC, generation, entrance, NavMesh, PathfindingLib, enemy/scrap, BCMER, BMDSFIX1 or accepted-normalizer mutation is part of AGDIAG1.

The deterministic repository validator is `AnalysisTools/validate_s142ak_agdiag1_source.py`; the dedicated PR workflow is `.github/workflows/s142ak-agdiag1-source-static.yml`.

## Controller and lifecycle preservation

This checkpoint does not create a review profile or DLL publication and does not arm runtime:

- `BuildSpecs/current.json` stays disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- base remains exact S1.42AK-BMDSFIX1 profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`;
- S1.42AK remains accepted;
- S1.42AK-BMDSFIX1 remains active / NOT ACCEPTED;
- its regular selector-free Black Mesa x DeepSewersFlow gate remains outstanding and unwaived.

The semantic router remains `interiors_and_lll`; no router-map mutation is required because no new semantic topic was introduced.

## Exact PR validation PASS

The repaired implementation was validated on exact PR head `84ea816a132b39861134b2eca1fb71847324e6f2`.

- `S1.42AK AGDIAG1 source and pure static gate`: run `37197799601`, run number 2, **success**.
  - pure Art Gallery fail-closed policy tests: success;
  - plugin source compile: success;
  - deterministic source/controller validator: success.
- `Knowledge Architecture`: run `37197799585`, run number 1063, **success**.

This proves the source/pure-static checkpoint only. No review profile, publication, Gale import, activation or runtime is authorized here.


## First PR-gate repair history

The first dedicated AGDIAG1 source/static run on PR #257 was run `37197526404` against PR head `6c1055b596a42bd82e0b7d5d5f033877fe329b27`.

Its pure Art Gallery policy-test step passed. The compile step then failed during package restore because the new project depended on runner-global NuGet configuration and therefore saw only `nuget.org`; `BepInEx.Core` and the required UnityEngine package version were unavailable from that source. The source/static validator was skipped because compilation stopped the job.

On the same PR head, Knowledge Architecture run `37197526593` passed.

The bounded repair changes no selector/gameplay code. It makes the project restore contract explicit with exactly:

- `https://api.nuget.org/v3/index.json`;
- `https://nuget.bepinex.dev/v3/index.json`.

The validator now fails if those project-local feeds drift, and the dedicated workflow explicitly checks out `${{ github.event.pull_request.head.sha }}` so subsequent source/static validation executes against the exact PR head rather than relying on the synthetic PR merge checkout.


## Source/static completion boundary

AGDIAG1 is now source/pure-static complete and remains `DIAGNOSTIC ONLY / NEVER ACCEPT`.

The exact next lifecycle decision is a separately bounded inactive review-build authorization/recipe decision. That decision must preserve the exact S1.42AK-BMDSFIX1 parent profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`, keep the future short Gale identity `LC V1 S1.42AK-AGD1`, and prove that any future review artifact would add only the AGDIAG1 DLL plus allowed profile-identity metadata.

This source/static PASS itself does not authorize constructing, publishing, importing, activating or running that profile.
