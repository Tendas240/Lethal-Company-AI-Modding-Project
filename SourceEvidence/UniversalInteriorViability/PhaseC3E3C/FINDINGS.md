# C3E3C — Exact Oxyde level and Dusk moon definition

Status: complete bounded asset inspection; packaged ordinary-generation flag disabled; effective owner/runtime behavior unresolved.

## Provenance and scope

- Inspection date: 2026-09-20; accepted baseline S1.42AK.
- Parent PR #138 HEAD: `f5e9a2fd71f885d59f645a43f49a0eb3b646d60d`; main independently verified at `56355ff518ae4301a38d370be9561251f6f963c1`.
- Exact CodeRebirth 1.6.9 ZIP freshly downloaded: 263,010,364 bytes, SHA-256 `a44a47d3f9eb049ccea83f8483c257f4faa2bf927a6df7e0bb70ff1504b2a5d6`.
- Inspected member: `plugins/CodeRebirth/Assets/oxydeassets`, 398,696 bytes, SHA-256 `86d2ef29d428bcb3b96cb5ec99283a362324f8261c4a8e26737e3bd04fe24fe4`.
- Both hashes match C3E3A's manifest/inventory. DLL inspection and the C3E3B scene scan are not repeated.
- UnityPy 1.25.3 reads embedded type trees statically. No managed mod code or game executes.

The bundle has 48 objects in one serialized file, `CAB-34cea74cab018d261344242e7acd380f`, Unity 2022.3.62f2, with no external serialized-file references. All seven MonoScripts and fourteen MonoBehaviours are parsed for identity without errors. Only the level/moon definitions and their direct references plus route predicate/fail-node context are investigated. This is not recursive prefab/component closure.

## Identity and reference chain

The AssetBundle container exposes `assets/lethalcompany/mods/plugins/coderebirth/moons/oxyde/oxydemoondefinition.asset` at pathID `-3975445595720329216`.

| Record | pathID | Resolved script |
| --- | --- | --- |
| OxydeMoonDefinition | -3975445595720329216 | Dusk.DuskMoonDefinition, com.github.teamxiaolan.dawnlib.dusk.dll |
| OxydeLevel | -4793931200078666718 | SelectableLevel, Assembly-CSharp |
| OxydeProgressivePredicate | 5630240687614732369 | Dusk.ProgressivePredicate, com.github.teamxiaolan.dawnlib.dusk.dll |
| OxydeFailTerminalNode | 7283538759813322484 | TerminalNode, Assembly-CSharp |

Moon key is `code_rebirth:oxyde`. Its `<Level>k__BackingField` points directly to OxydeLevel. The explicit tag list contains `dawn_lib:has_buying_percent`; `_configEntries` is empty. The script references are serialized identities, not proof of the running implementation's behavior.

All 22 pointer occurrences in the two definition trees are accounted for: 18 non-null pointers resolve locally; four are null (two ScriptableObject m_GameObject pointers, specialEnemyRarity.overrideEnemy and PricingStrategy). The report preserves field paths and target identities, including planet prefab, video, ambience, nine outside enemy assets, both scene animations and route predicate.

## Serialized scene registration

The moon contains exactly one `_scenes` entry:

- key: `code_rebirth:oxyde`;
- scene asset GUID: `4f389119bf25893428e69532bbd78797`;
- scene path: `Assets/LethalCompany/Mods/plugins/CodeRebirth/Moons/Oxyde/Scene/Oxyde.unity`;
- bundle name: `oxydescene`;
- BaseWeight: 100; WeatherSpawnWeightsConfig: empty;
- GenerateWeightsConfig: 1;
- landing/takeoff animation pointers both resolve locally.

SelectableLevel independently has `sceneName = Oxyde`, `levelID = 745`, and `PlanetName = 745 Oxyde`. These are consistent serialized registration inputs. This asset inspection does not itself prove that a runtime registration or scene-load call executes. `GenerateWeightsConfig` belongs to the scene-weight definition; its presence is not evidence that ordinary interior generation is enabled.

## Generation-participation observations

| SelectableLevel field | Exact serialized value |
| --- | --- |
| spawnEnemiesAndScrap | 0 (false) |
| dungeonFlowTypes | empty |
| spawnableScrap | empty |
| minScrap / maxScrap | 0 / 0 |
| minTotalScrapValue / maxTotalScrapValue | 0 / 0 |
| Enemies / DaytimeEnemies | empty / empty |
| spawnableMapObjects / indoorMapHazards / spawnableOutsideObjects | empty / empty / empty |
| planetHasTime | 0 |
| riskLevel | Safe |
| factorySizeMultiplier | 1.600000023841858 |

Nine OutsideEnemies entries and nonzero enemy-power limits are also serialized. They are preserved in the report and prevent treating every spawn-related field as empty. Such values, or the nonzero factory-size multiplier, do not override the observed false flag by themselves. Their effective use requires implementation evidence.

The Dusk moon has GenerateEnemyPowerCountConfigs = 1, while GenerateEnemySpawnCurveConfigs, GenerateEnemySpawnProbabilityRangeConfigs, GenerateMinMaxScrapConfig and GenerateTimeConfig are 0. Cost is 0; GenerateCostConfig and GenerateDisableUnlockConfig are 1. The linked progressive predicate starts with `_isHidden = 1`, `_isLocked = 1`, `_lockedName = ???` and a fail node containing `Coordinates not found.` These are packaged defaults, not a claim that the accepted profile cannot unlock or visit Oxyde.

**Bounded conclusion:** the exact packaged Oxyde level is not configured with the ordinary enemies/scrap generation flag enabled and supplies no dungeon-flow entries of its own. It cannot be assumed to be an ordinary dungeon destination merely because Dawn/LLL registers it as an External level or selection rules can match its tags. Whether owner registration, configuration or runtime code changes the flag, supplies flows or implements another generation/construction route is still unexamined here.

This explains why the next investigation must establish generation participation before expecting ordinary interior entrances. It does not prove zero runtime entrances, an intentional permanent non-dungeon design, a gameplay defect or technical incompatibility. The C3E3B absence of directly readable EntranceTeleport records remains a separate, scoped observation.

## Reproduction and validation

Install UnityPy 1.25.3 (this run's dependencies are recorded in TOOLCHAIN.json), then run:

```sh
python AnalysisTools/inspect_universal_interior_c3e3c.py --package /path/to/XuXiaolan-CodeRebirth-1.6.9.zip --out /path/to/output
# Or use the already extracted, hash-verified bundle:
python AnalysisTools/inspect_universal_interior_c3e3c.py --bundle /path/to/oxydeassets --out /path/to/output
```

The inspector rejects wrong input size/hash, wrong UnityPy version, unexpected serialized-file layout, ambiguous level/moon identity and unresolved non-null definition pointers. It records full definition type trees, local pointer resolution and selected raw-object SHA-256 values. Non-finite curve floats use explicit tagged objects so the report remains strict JSON without losing Infinity/NaN distinctions.

Both package and extracted-bundle paths produced byte-identical reports. Targeted checks confirmed the container-to-moon-to-level chain, scene identity, false generation flag, empty dungeon list and complete 18 resolved / 4 null pointer accounting. A modified bundle was rejected before parsing.

## Preserved state and next bounded segment

No authoritative B3 matrix change or target-universe reclassification follows from these assets alone. The 46 supported External selection pairings remain selection-only. Source-GUID coverage remains 27/192 resolved, 165 open; no broad source-GUID search was resumed.

Black Mesa ownership, Shatteredrooms exclusions and S1.42AB normalization are untouched. S1.42AK remains accepted/latest, with no candidate or outstanding runtime test. BuildSpecs/current.json remains disabled at IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS and RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK.

Next bounded segment **C3E3D**: trace only the version-bound owner registration/consumption of this Oxyde DuskMoonDefinition and SelectableLevel, including writes to spawnEnemiesAndScrap/dungeonFlowTypes and the effective normal-generation gate. Establish whether the packaged false flag survives owner setup, and identify any narrowly evidenced alternative construction path before pursuing entrance creation. Use existing repository manifests to bind the exact CodeRebirth 1.6.9 and Dawn/Dusk owner evidence; qualify source-versus-binary claims. Do not perform scene-wide topology or broad runtime analysis in that segment.

Black Mesa 3.4.4 scene topology and DawnLib/LLL/vanilla numbering/pairing semantics remain later obligations. No build, runtime test or universal override is authorized.
