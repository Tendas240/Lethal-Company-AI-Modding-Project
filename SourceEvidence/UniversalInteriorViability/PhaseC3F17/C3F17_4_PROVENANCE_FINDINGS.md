# C3F17.4 — S1.42AK / LethalLevelLoader 1.7.12 Provenance Findings

**Status:** PROVENANCE SUB-GATE COMPLETE / CLEAN  
**Scope:** first bounded C3F17.4 segment only; no candidate build request, profile build, runtime arming, gameplay run, Gale import/replacement, B3 change, or universal-availability rollout is authorized by this file.

## Exact repository state verified

- Pull request: `#138`
- Branch: `scope/universal-interior-phase-c3a-dawn-tags`
- Provenance implementation head: `01ed1747ab96f1990932edf9a3e29bb3b6849c68`
- Tree: `9ba7269470ac45f074f44d6a626180d85b4cef25`
- PR synthetic merge SHA used by `pull_request` checkout: `0a5445ce41af126cf1b257bc363002e411170d28`
- The synthetic merge commit and the branch-head commit resolve to the same tree `9ba7269470ac45f074f44d6a626180d85b4cef25`; therefore the checked repository bytes are identical.

## Repository-native verification

Added fail-closed verifier:

- `AnalysisTools/verify_s142ak_lll_1712_provenance.py`

Added read-only PR gate:

- `.github/workflows/s142ak-bmghdiag1-lll-provenance.yml`
- Workflow: `S1.42AK BMGHDIAG1 LLL provenance gate`
- Run: `#1`
- Run ID: `35848358428`
- Result: `completed / success`
- Workflow branch head SHA: `01ed1747ab96f1990932edf9a3e29bb3b6849c68`
- Artifact ID: `10744346181`
- Artifact digest: `sha256:ce3e3ffc6428585b0379c9cb58bde65aa2c1d8d38e58c7ff54239aa28c28b39c`

The gate freshly materializes the exact pinned Thunderstore package selected by exact S1.42AK dependency metadata. It fails closed on profile drift, export drift, dependency version/source/enablement drift, alternate LLL owner presence, package hash drift, manifest drift, DLL multiplicity, or DLL hash drift.

## Freshly re-confirmed identity

Exact accepted parent profile:

- path: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`
- SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`

Exact dependency metadata:

- dependency: `IAmBatby-LethalLevelLoader`
- version: `1.7.12`
- enabled: `true`
- source: `Thunderstore`
- alternate/deprecated `LethalLevelLoaderUpdated`: absent
- the `export.r2x` embedded in the exact S1.42AK profile is byte-identical to `ProfileSources/S1.42AK/export.r2x`
- `ProfileSources/S1.42AK/export.r2x` SHA-256: `19935c1afc98de1562fda8b299d7d23d09c3555eac88f9de7992eb3d6e2b46b8`

Freshly downloaded package:

- URL: `https://gcdn.thunderstore.io/live/repository/packages/IAmBatby-LethalLevelLoader-1.7.12.zip`
- manifest name: `LethalLevelLoader`
- manifest version: `1.7.12`
- package SHA-256: `e01eadec8b1df3a1bc331e98b29d94baffa572cb7379953f1fa4e46df0aa6451`
- expected package SHA-256: `e01eadec8b1df3a1bc331e98b29d94baffa572cb7379953f1fa4e46df0aa6451`
- package hash match: `true`

Freshly extracted binary:

- member: `LethalLevelLoader.dll`
- exactly one matching DLL member exists in the package
- DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`
- expected DLL SHA-256 from the prior S1.42AJ-DIAG1 capture: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`
- DLL hash match: `true`

## Conclusion

The C3F17 diagnostic contract's S1.42AK / LethalLevelLoader 1.7.12 binary-provenance prerequisite is independently re-confirmed by a fresh repository-native materialization. The prior AJ observation is no longer being reused merely by assertion: the exact S1.42AK dependency graph selects the same pinned package, and fresh package/DLL bytes match the expected identities.

This closes only the first bounded C3F17.4 provenance sub-gate.

## Preserved boundaries

- `BuildSpecs/current.json` remains the disabled idle controller.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.
- No `BuildSpecs/S1.42AK-BMGHDIAG1.json` candidate request is created by this checkpoint.
- No candidate is active or runtime-armed by this checkpoint.
- No runtime test is requested or authorized by this checkpoint.
- Black Mesa x Greenhouse remains `NOT_YET_PROVEN` pending later runtime evidence.
- S1.42AK remains the accepted baseline; S1.42AB normalization, Black Mesa Dawn/native ownership, Greenhouse availability config, B3, Shatteredrooms exclusions, and separate Black-Mesa/Pikmin routing remain unchanged.

## Next bounded C3F17.4 segment

Using this clean provenance only, author/authorize the separate **inactive** `S1.42AK-BMGHDIAG1` candidate build request and the static archive-delta/build gate. The candidate must remain not runtime-armed unless the freshly re-read lifecycle explicitly authorizes a later separate transition.
