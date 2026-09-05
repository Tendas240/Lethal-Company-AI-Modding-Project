# CodeRebirth and DawnLib Tuning

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted CodeRebirth ownership/tuning rules plus active S1.42AD implementation boundary  
**Canonical-For:** `coderebirth`  
**Evidence:** `Current/03_PROJECT_CHRONOLOGY.md`, `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`, S1.42Z/S1.42AD ProfileSources  
**Related:** `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Package architecture

Modern project stack uses CodeRebirth with DawnLib. **Do not reinstall CodeRebirthLib**; it is a historical removed/forbidden dependency in this project architecture.

For the active S1.42AD line, the frozen exact owner versions are:

- CodeRebirth `1.6.9`;
- DawnLib `0.9.25`;
- DawnLib.Dusk `0.9.25`.

## Natural Currency / Flash Turret control

S1.40 and S1.40A proved that project-local object filters or sparse config overrides were insufficient because DawnLib/CodeRebirth could regenerate author defaults.

S1.40B established the accepted native-owner solution:

- `Clean Unusued Configs = false`;
- Coin `Allow Editing Config = true`;
- Crisp Dollar Bill `Allow Editing Config = true`;
- Wallet `Allow Editing Config = true`;
- Currency inside moon/interior weights blank;
- Flash Turret `Allow Editing Config = true`;
- Flash Turret `Is Inside Hazard = false`;
- Flash Turret inside moon/interior weights blank.

Do not blank `Money | Enemy Drop Rates` as collateral damage. The target is unwanted natural dungeon generation, not dedicated CodeRebirth money-drop systems.

## CodeRebirth -> Pikmin utility protection

The cumulative compatibility plugin contains a direct utility-kill shield for Pikmin/Puffmin. This is retained because configuration toggles alone did not cover every Autonomous Crane kill path.

## Accepted aerial-defense tuning

S1.42Z accepted project-local transactional scaling of exactly two DawnLib map-object providers:

- `code_rebirth:air_control_unit`: all 18 Moon/tag curves × `0.5`;
- `code_rebirth:gunslinger_greg`: all 18 Moon/tag curves × `0.5`.

No other map-object provider is modified. The operation scales curve amplitude/spawn weight; a short gameplay sample is not guaranteed to show mathematically exact half-counts.

Aerial-defense DLL SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

Accepted runtime evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

## S1.42AD Functional Microwave active candidate

S1.42AD applies the same narrow owner principle to the Functional Microwave, but on its **InsideInfo** path.

Candidate:

- Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`
- Profile SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- DLL: `BepInEx/plugins/S142ADCodeRebirthMicrowaveSpawnTuning/S142ADCodeRebirthMicrowaveSpawnTuning.dll`
- DLL SHA-256: `45f22f9b27e3ab7c853fe742bb7c2ce9bc94abc5a0856bb278c747076a2f99c7`
- Build run: `33959742235` — SUCCESS
- Candidate record: `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`
- Status: **BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

### Exact target and owner surface

The user explicitly authorized Functional Microwaves to be encountered half as often, implemented as:

`SpawnScale = 0.5f`

The plugin resolves exactly:

`code_rebirth:functional_microwave`

through:

`DawnMapObjectInfo.InsideInfo.SpawnWeights -> ProviderTable -> Dusk.MapObjectSpawnMechanics`

### Corrected shipped provider contract

Independent source/provenance review corrected the interrupted draft's earlier 19-curve assumption.

The relevant `coderebirthasset` bundle was rebuilt at CodeRebirth commit:

`c4020f20f5a05f1aee6519a2eb1554903890e08f` — 2026-04-06

The later source edit:

`eb4d5148047c625076b4735784a7ca2477ef17b6` — 2026-04-09

added Interior curves after that relevant bundle rebuild. CodeRebirth's .NET packaging copies existing Unity bundles rather than rebuilding them, so the later Unity-source-only state must not be treated as the shipped 1.6.9 runtime asset contract.

The expected shipped/runtime contract is therefore:

- `PrioritiseMoons = true`;
- exactly 18 `CurvesByMoonOrTagName` entries;
- exactly 0 `CurvesByInteriorOrTagName` entries;
- no `code_rebirth:functional_microwave_ultra_high` in the expected Moon/tag key set.

The exact 18 keys are frozen in `Patches/S142ADCodeRebirthMicrowaveSpawnTuning/README.md`.

### Fail-closed runtime behavior

Before any mutation, S1.42AD requires:

1. exact dependency versions;
2. MapObjects registry frozen;
3. exact Functional Microwave key with InsideInfo;
4. expected ProviderTable `_providers` structure;
5. exactly one `MapObjectSpawnMechanics` provider;
6. Moon priority enabled;
7. zero Interior curves;
8. exact 18-key Moon/tag set;
9. all expected curves non-null/non-empty.

Only then are each keyframe's value, incoming tangent and outgoing tangent multiplied by `0.5`. No other provider is touched.

Any drift causes a logged refusal and **no curve mutation**. Do not weaken this into global Inside-Hazard scaling, fuzzy key matching, alternate-provider fallback, or a global DawnLib selection patch.

### Runtime markers required for acceptance

The fresh runtime log must show:

- exact dependency validation;
- intended registry-lifecycle armed marker;
- `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=0`;
- final application marker confirming all 18 Microwave Moon/tag curves × `0.5`;
- no S1.42AD contract-refusal/error;
- normal startup/generation/gameplay without new fatal project regression.

S1.42AC remains the accepted baseline until this gate is evaluated.
