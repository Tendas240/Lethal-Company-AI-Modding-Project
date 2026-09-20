# C3E3F — exact installed V81 generation-body recovery gate

Status: repository-held proof boundary closed; exact local source capture helper prepared; no gameplay run/build authorized.

## Scope

Parent PR #138 HEAD at start: `bbf81f13b68882de04122c36bde20fc6c70ac8b1`. Accepted gameplay baseline remains S1.42AK.

C3E3E narrowed the Oxyde uncertainty to one upstream question: when `SelectableLevel.spawnEnemiesAndScrap = false`, does installed Lethal Company V81 actually reach the `RoundManager.GenerateNewFloor` callsite inside `RoundManager.GenerateNewLevelClientRpc`?

This checkpoint does not inspect Oxyde entrances, Black Mesa topology, general entrance numbering or any gameplay behavior.

## Repository-native recovery result

The existing authoritative installed-V81 capture at:

`SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T143200Z-a693b4b9/`

is provenance-bound to:

- Assembly-CSharp SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- Lethal Company executable SHA-256 `24f39cbf2060834e8b648833c0c31ed82506ea633a9e8e5609e01102c7d6e8f1`;
- Steam app 1966720 / build 22825947;
- ilspycmd 11.0.0.9375.

Its focused report intentionally contains only the previously selected spawn/despawn surface and one-hop callers. It includes `LoadNewLevelWait` and `FinishGeneratingNewLevelClientRpc`, but not the bodies of `GenerateNewLevelClientRpc` or `GenerateNewFloor`.

The original helper records the SHA-256 of the complete locally decompiled RoundManager type but intentionally excludes that full source and all game binaries from publication. Therefore the missing method bodies cannot be reconstructed from the committed report/hash alone.

No second repository capture contains these two non-stub installed-game method bodies. The repository therefore has a real byte-availability boundary rather than an unresolved search task.

## Narrow exact-capture helper

A new repository-native helper is added:

`AnalysisTools/InspectRoundManagerGenerationV81.ps1`

It deliberately reuses the established fail-closed installed-game provenance contract instead of weakening it. It accepts only the same reviewed V81 assembly/executable/app/build identity and uses pinned ilspycmd 11.0.0.9375.

Its required declared methods are exactly:

- `GenerateNewLevelClientRpc`
- `GenerateNewFloor`

The generic focused extractor also includes their one-hop direct callers inside RoundManager. That should capture the enclosing callsite/control-flow context required by C3E3E without uploading the whole type or any binary.

Publication is restricted to exactly two text files on a new evidence branch under:

`SourceEvidence/VanillaV81/RoundManagerGeneration/<timestamp>-<suffix>/`

- `ROUNDMANAGER_GENERATION_FOCUSED_DECOMPILE.txt`
- `MANIFEST.json`

No DLL, EXE, complete decompile, local path or username is published. The helper performs no game launch, gameplay run, profile build or mod execution.

A dedicated Windows PowerShell 5.1 CI workflow, `.github/workflows/roundmanager-generation-evidence-helper.yml`, validates the extractor/provenance self-test and isolated .NET/ILSpy bootstrap path.

## Why a local installed-byte capture is now necessary

The repository cannot manufacture exact installed method bodies from hashes. GitHub-hosted CI also has no authenticated/owned Lethal Company installation corresponding to the pinned local Steam provenance.

Accordingly, the remaining source step requires one execution of the repository helper on a machine that already has the pinned V81 Steam build installed. This is a **source capture only**, not a gameplay test and not a build request. It requires no repository clone: the script can be fetched directly from the PR branch and self-publishes only the focused evidence branch after validating the local bytes.

If the local installed files have drifted from the pinned V81 contract, the helper fails closed and uploads nothing.

## Preserved state

Nothing in gameplay/configuration changes:

- authoritative B3 matrix remains unchanged;
- the 46 External selection-supported pairings remain selection-only;
- Oxyde runtime dungeon generation remains unproven;
- Oxyde runtime entrance construction remains unproven;
- Black Mesa is not duplicate-registered;
- Shatteredrooms Experimentation/Embrion exclusions remain preserved;
- S1.42AB InteriorWeightNormalization remains unchanged;
- S1.42AK remains accepted/latest with no candidate and no outstanding runtime test;
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`;
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`.

## Next bounded segment

Next **C3E3G** starts only after the focused source-capture branch exists. Ingest and verify that capture, inspect only the two required method bodies plus their selected callers, and decide the exact `spawnEnemiesAndScrap = false` callsite reachability.

Do not launch the game for this source capture. Do not begin Oxyde entrance/topology analysis before the upstream gate is resolved. No gameplay candidate/runtime test is authorized.
