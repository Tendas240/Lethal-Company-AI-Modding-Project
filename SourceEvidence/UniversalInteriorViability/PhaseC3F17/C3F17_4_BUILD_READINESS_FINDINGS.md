# C3F17.4 — S1.42AK-BMGHDIAG1 Inactive Build / Archive-Delta Findings

**Status:** STATIC BUILD-READINESS SUB-GATE COMPLETE / CLEAN / NOT RUNTIME-ARMED  
**Scope:** second bounded C3F17.4 segment only. This checkpoint authors and validates the separate inactive diagnostic build request and exact archive-delta gate. It does not publish/arm a runtime candidate, change the live build/runtime controllers, request gameplay, import/replace a Gale profile, change B3, or roll out universal availability.

## Exact implementation state

- Pull request: `#138`
- Branch: `scope/universal-interior-phase-c3a-dawn-tags`
- Build-gate implementation head: `9badf106a488c97606baf5c7b08800671c23d397`
- Implementation tree: `db342124ad7fed32d5566b5c900fd624f9c6e713`
- PR synthetic merge SHA used by the successful build-gate checkout: `2580945dbce53d4a35f41f5e90e4644e31c3cf7c`
- The synthetic merge commit resolves to the same tree `db342124ad7fed32d5566b5c900fd624f9c6e713`; therefore the repository bytes exercised by the gate are identical to the implementation head.

## Separate inactive build request

Added:

- `BuildSpecs/S1.42AK-BMGHDIAG1.json`

The request is intentionally `enabled: true` only so the repository builder can consume it when explicitly passed as a separate review spec. It is **not** the live build controller and is never copied into `BuildSpecs/current.json` by this checkpoint.

Exact request contract:

- build ID: `S1.42AK-BMGHDIAG1`
- parent: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`
- parent SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`
- output review profile: `Profiles/LC V1 S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic.r2z`
- package state changes: none
- package additions/removals: none
- config patches: none
- file injections: none
- local plugin builds: exactly one, `Patches/S142AKBMGHDiag1/S142AKBMGHDiag1.csproj`
- injected archive member: `BepInEx/plugins/S142AKBMGHDiag1/S142AKBMGHDiag1.dll`

`BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`. `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

## Static build / archive-delta gate

Added:

- `AnalysisTools/validate_s142ak_bmghdiag1_build.py`
- `.github/workflows/s142ak-bmghdiag1-build-static.yml`

The source-only C3F17 gate was minimally transitioned so that the now-authorized separate build request may exist while it still requires the live build controller to remain disabled/idle and the runtime pointer to remain `S1.42AK`. The source-only workflow itself still never invokes the profile builder.

The build gate executes, in order:

1. pure selection/observation policy tests;
2. source fail-closed contract verification;
3. fresh S1.42AK / LethalLevelLoader 1.7.12 provenance verification;
4. explicit repository-builder invocation using only the separate BMGHDIAG1 request;
5. exact archive-delta and inactive-lifecycle validation;
6. upload of an unarmed review artifact only after every prior gate succeeds.

## Exact successful CI

Build/archive-delta workflow:

- workflow: `S1.42AK BMGHDIAG1 build and archive-delta gate`
- run: `#1`
- run ID: `35849257773`
- result: `completed / success`
- tested branch head: `9badf106a488c97606baf5c7b08800671c23d397`
- artifact ID: `10744791628`
- artifact digest: `sha256:5e74b0fe1cb73afb928c98ff1a166d97f89a975dd4bdb76708721c8d4fe030f7`

Related exact-head gates also passed on the implementation head:

- `S1.42AK BMGHDIAG1 source and pure static gate` run `#6` / ID `35849257663`: `completed / success`
- `S1.42AK BMGHDIAG1 LLL provenance gate` run `#3` / ID `35849257642`: `completed / success`
- `Knowledge Architecture` run `#656` / ID `35849257719`: `completed / success`

## Review-build result

The CI review artifact records:

- output profile SHA-256: `8e0cd11c818f228cfacd612ef14bbc450c629ef5db695df418752d17cb9855f3`
- diagnostic DLL SHA-256: `61e02d193ceb43a457e9241040aa2995696b5d61a11ff8400c9925c2fff78e78`
- freshly re-confirmed LLL DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`
- accepted normalizer DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`
- output archive members: `337`
- parent archive members: `336`

Exact archive delta:

- added members: exactly `BepInEx/plugins/S142AKBMGHDiag1/S142AKBMGHDiag1.dll`
- changed existing members: exactly `export.r2x`
- removed members: none
- package changes: `0`
- config changes: `0`

The validator normalizes only the single `profileName:` field when comparing parent/output `export.r2x`. All other export content must remain identical, so the successful result proves there was no dependency/package-state drift hidden behind the allowed profile-identity change.

The accepted `S142ABInteriorWeightNormalization.dll` is present in both parent and review output, retains exact SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`, and is byte-identical across the delta. The injected BMGHDIAG1 DLL is byte-identical to the DLL compiled by the repository builder, and its `ProfileSources/S1.42AK-BMGHDIAG1/FILE_INDEX.json` entry records the same DLL hash.

## Provenance retained inside the build gate

The successful build workflow freshly materialized LethalLevelLoader again rather than trusting only the previous C3F17.4 sub-gate:

- dependency: `IAmBatby-LethalLevelLoader 1.7.12`
- enabled / Thunderstore
- `LethalLevelLoaderUpdated`: absent
- package SHA-256: `e01eadec8b1df3a1bc331e98b29d94baffa572cb7379953f1fa4e46df0aa6451`
- DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`
- both hashes match the required identities.

## Lifecycle boundary

This successful gate is **build/static evidence only**.

- The generated `.r2z`, ProfileSources snapshot and build-evidence files currently exist only in the GitHub Actions review artifact from this checkpoint; this segment does not publish them as the live runtime candidate.
- `Current/CURRENT_STATE.json` still has `active_candidate = null` and `runtime_test_outstanding = false`.
- `BuildSpecs/current.json` remains disabled/idle.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.
- No Gale replacement/import is requested.
- No gameplay run or runtime-log upload is requested.
- Black Mesa x Greenhouse remains `NOT_YET_PROVEN` until the later runtime evidence contract is actually executed and satisfied.
- S1.42AK remains the accepted baseline; S1.42AB normalization, Black Mesa Dawn/native ownership, Greenhouse availability configuration, B3, Shatteredrooms exclusions and the separate Black-Mesa/Pikmin routing scope remain unchanged.

## C3F17.4 conclusion

The provenance prerequisite, separate inactive build request, compile/build path and exact archive-delta gate are now all clean. The candidate is deliberately **not runtime-armed** by C3F17.4.

Any publication or lifecycle/controller transition that makes `S1.42AK-BMGHDIAG1` the runtime-active diagnostic must be a later separate atomic checkpoint after freshly re-reading the lifecycle authorities. Static success alone does not authorize that transition.
