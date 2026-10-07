# C3E3D — Oxyde owner registration and generation-field consumption

Status: bounded exact-owner analysis complete; direct generation-flag mutation absent in the inspected owners; full client generation gate remains unresolved.

## Scope and provenance

Parent PR #138 HEAD: `220a9087a4c574d5c7241ed1cae4021899f7942f`. Accepted baseline: S1.42AK. Inspection date: 2026-09-20.

This checkpoint follows C3E3C's exact OxydeMoonDefinition → OxydeLevel reference. It inspects only the CodeRebirth 1.6.9 / DawnLib 0.9.25 owner registration path and uses already captured installed-V81 source for narrowly relevant lifecycle guards. It does not repeat scene topology, search source GUIDs, or audit the full mod stack.

Both ZIP hashes and all six assembly hashes were independently checked against `SourceEvidence/NativeSpawnOwners/20260911T144505Z/MANIFEST.json` (Git blob `77e77022d3cbdd742d57013f66812c0e8a336c64`). The accepted S1.42AK export retains both enabled package versions. DLL inspection uses dnfile 0.18.0 and dncil 1.0.2; no game or managed mod code executes. These are exact-package IL observations, not inferred equivalence with upstream source.

## Registration chain

Thirty selected method bodies are preserved in `OXYDE_OWNER_REGISTRATION_IL.json`, with method tokens, signatures, nested declaring types and resolved IL operands.

| Owning stage | Exact observed behavior |
| --- | --- |
| CodeRebirth MoonHandler constructor, token 0x06000955 | Calls Dusk RegisterContent for `oxydeassets`, then installs a terminal text modifier if loading succeeded. |
| MoonHandler.OxydeAssets constructor, 0x06000956 | Delegates to Dusk AssetBundleLoader. |
| Dusk ContentHandler RegisterContent / TryLoadContentBundle / LoadAllContent | Checks bundle availability/content enablement, constructs the loader, then calls each content definition's Register, RegisterPost and RegisterConfigs. |
| Dusk AssetBundleLoader constructors | Load bundle content and order definitions, including DuskMoonDefinition. |
| DuskMoonDefinition.Register, 0x060003f5 | Creates moon config, then passes its TypedKey and existing Level object into DawnLib.DefineMoon with a builder callback. |
| DuskMoonDefinition callback, 0x060003fb | Adds the serialized scenes, bundle paths and animations; applies purchase/config providers and tags. |
| DawnLib.DefineMoon, 0x060000f3 | Builds DawnMoonInfo, attaches it to the same SelectableLevel and registers it in LethalContent.Moons. |
| DawnMoonInfo constructor, 0x060002c6 | Stores the supplied Level reference. |

C3E3C supplies the actual definition values: `code_rebirth:oxyde`, scene `Oxyde`, bundle `oxydescene`, and `spawnEnemiesAndScrap = false`. The scene callback forms the bundle path from the mod-relative `Assets` directory and serialized bundle name. This is a traced registration implementation, not a newly observed Oxyde gameplay run.

## Narrow field-use inventory

A token-resolved search covered every available method body in these six exact owner assemblies for just two fields: `SelectableLevel.spawnEnemiesAndScrap` and `SelectableLevel.dungeonFlowTypes`.

| Assembly | Bodies scanned | No-body declarations | Relevant field instructions |
| --- | ---: | ---: | ---: |
| CodeRebirth | 5,723 | 8 | 3 reads |
| CodeRebirth Dusk replacement entities | 46 | 0 | 0 |
| DawnLib | 2,485 | 78 | 8 reads, 1 write |
| DawnLib.Dusk | 1,741 | 57 | 10 reads |
| DawnLib compatibility | 21 | 0 | 0 |
| DawnLib interfaces | 8 | 27 | 0 |
| Total | 10,024 | 170 | 22 |

There are zero parse errors. All 14 references to `spawnEnemiesAndScrap` are reads. No direct write or address-taking instruction targets that flag in these owners. No exact field-name string literal for either searched field occurs. This does not exclude arbitrary reflection, other assemblies, patches, or externally supplied runtime mutations.

Dusk's ten flag reads belong to CreateMoonConfig. The flag gates time and enemy power/curve/range config creation together with the respective Generate* toggles; it is not an assignment enabling generation. Thus C3E3C's GenerateEnemyPowerCountConfigs = 1 does not independently enable normal generation or even guarantee those config entries are created while the flag is false. The empty `_configEntries` recorded in C3E3C also provides no serialized dynamic override for this flag.

**Bounded conclusion:** the inspected owner path carries the existing level object through registration, and no direct owner mutation enables its packaged false generation flag. This is substantially stronger than asset defaults alone, but is not a whole-stack final-value proof.

## Dungeon-list population is independent

The sole direct write to `SelectableLevel.dungeonFlowTypes` is Dawn.DungeonRegistrationHandler.AddDawnDungeonsToMoons, token `0x0600010c`, offset 208.

Its implementation iterates registered moons, copies each existing list, appends eligible Dawn dungeon indexes with initial rarity 0, and stores the resulting array. It filters dungeon ownership with ShouldSkipIgnoreOverride but does not test the moon's spawnEnemiesAndScrap flag. Init attaches this routine to the moon registry's OnFreeze event. Later weight updates are separate.

Therefore Oxyde's empty packaged dungeon list can be populated by the owner infrastructure without changing its false generation flag. Neither that list nor the existing 46 selection-supported pairings proves that ordinary dungeon generation executes.

## Company tagging and generation-call boundary

Dawn.MoonRegistrationHandler.Init installs a Company auto-tagger whose exact callback (`0x060002a5`) returns `!moon.Level.spawnEnemiesAndScrap`. The Company key is `lethal_company:company`, as already captured in C3A's exact Tags initializer. With C3E3C's false flag preserved, Oxyde meets this predicate. This is a conditional implementation result, not a runtime tag dump or an assertion that Oxyde is identical to Gordion.

The inspected Dawn dungeon hooks show:

- GenerateNewFloor wrapper updates dungeon weights and calls the original delegate; this wrapper itself has no flag guard.
- RuntimeDungeon.Start wrapper sets GenerateOnStart to false before delegating.
- RuntimeDungeon.Generate wrapper adjusts fire exits / tile sets and delegates when invoked; it does not prove that Oxyde invokes it.

Existing installed-V81 evidence provides a limited native gate:

`SourceEvidence/VanillaV81/RoundManagerSpawning/20260911T143200Z-a693b4b9/ROUNDMANAGER_SPAWNING_FOCUSED_DECOMPILE.txt`

Its exact 43,505 bytes were rehashed to `5317509a39e072db2c3df95de1cb9091dd9f7ff7e1a3bfe231045dea9cfc974f`. The reviewed capture attributes the source to installed Assembly-CSharp SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`, Steam build 22825947. The game DLL itself is not present/rehashed here.

LoadNewLevelWait always dispatches GenerateNewLevelClientRpc on the captured route, but waits for dungeon/player generation and calls GeneratedFloorPostProcessing only when spawnEnemiesAndScrap is true. FinishGeneratingNewLevelClientRpc likewise gates SetLevelObjectVariables on this flag, while several remaining lifecycle operations are outside that conditional.

**Do not promote these guards into proof that the client never generates a dungeon.** This capture does not contain the actual GenerateNewLevelClientRpc / GenerateNewFloor bodies. The separate V81 reference-only report is not substituted for nonstub installed-game code. Dawn's deferred generation/hotloading and LLL's client-generation integration have not been closed by this segment. No alternative Oxyde entrance-construction path is established.

## Validation and reproduction

```sh
python AnalysisTools/inspect_universal_interior_c3e3d.py --coderebirth-package /path/to/XuXiaolan-CodeRebirth-1.6.9.zip --dawnlib-package /path/to/TeamXiaolan-DawnLib-0.9.25.zip --out /path/to/output
```

The inspector validates the existing manifest Git blob, both ZIP sizes/hashes, all six DLL hashes, exact parser versions and selected-method coverage. MANIFEST.json binds the generated report, inspector and cited repository inputs. Validation checks the 30 selected bodies, 10,024-body field coverage, fourteen flag reads/no writes, sole dungeon-list write and concrete registration/tag/hook instruction sequences.

## Preserved state and next bounded segment

Authoritative B3 matrix and target universe remain unchanged. The 46 External selection pairings remain selection-only. No owner registration, Shatteredrooms exclusion, accepted S1.42AB normalization, gameplay config or controller changes occur. S1.42AK remains accepted/latest, with no candidate or outstanding runtime test. BuildSpecs/current.json remains disabled at IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS; RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK.

Next **C3E3E**: close the remaining client-generation integration boundary, starting with exact DawnLib deferred-generation/hotload methods and version-bound LLL generation hooks. Determine what actually guards/delegates GenerateNewFloor for a false-flag External level, using existing repository-native inputs first. Explicitly retain any missing installed-V81 method-body proof; do not request a new gameplay run merely to fill a source gap. Only then decide whether an Oxyde entrance-construction investigation is warranted.

Black Mesa 3.4.4 topology and general DawnLib/LLL/vanilla entrance numbering/pairing remain later tasks. No matrix reclassification, universal override, gameplay build or runtime test is authorized.
