# CodeRebirth and DawnLib Tuning

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted CodeRebirth ownership/tuning rules plus current Functional Microwave correction boundary  
**Canonical-For:** `coderebirth`  
**Evidence:** `Current/03_PROJECT_CHRONOLOGY.md`, `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`  
**Related:** `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Package architecture

Modern project stack uses CodeRebirth with DawnLib. **Do not reinstall CodeRebirthLib**; it is a historical removed/forbidden dependency in this project architecture.

The current exact owner versions remain:

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

## Functional Microwave rarity — corrected S1.42AE candidate

The user's authorized balance target remains that Functional Microwaves should be encountered **half as often**:

`SpawnScale = 0.5f`

Target owner path:

`code_rebirth:functional_microwave`

via:

`DawnMapObjectInfo.InsideInfo.SpawnWeights -> ProviderTable -> Dusk.MapObjectSpawnMechanics`

### Rejected S1.42AD lesson

S1.42AD is historical rejection evidence. It expected 18 Moon curves and zero Interior curves. Runtime proved the provider instead exposed 18 Interior curves and the patch correctly failed closed before mutation.

Do not rewrite that historical record or use S1.42AD as a gameplay/build base.

### Corrected provenance

The prior inference that the shipped CodeRebirth 1.6.9 provider had no Interior table is no longer authoritative.

CodeRebirth commit `eb4d5148047c625076b4735784a7ca2477ef17b6` dated 2026-04-09 added exactly 18 `InsideInteriorCurveSpawnWeights` entries to the Functional Microwave asset. CodeRebirth later rebuilt bundles before the installed 1.6.9 state, and the S1.42AD runtime observation independently matches that 18-Interior structure.

The exact corrected runtime/provider contract used by S1.42AE is:

- exactly one `MapObjectSpawnMechanics` provider;
- `PrioritiseMoons = true`;
- exactly 18 Moon/tag curves;
- exactly 18 Interior/tag curves.

Moon table specifics:

- includes `code_rebirth:oxyde`;
- includes Microwave presets `none`, `low`, `medium`, `high`;
- does **not** include `functional_microwave_ultra_high`.

Interior table specifics:

- does **not** include `code_rebirth:oxyde`;
- includes Microwave presets `none`, `low`, `medium`, `high`, `ultra_high`;
- includes the same Vanilla moon-like keys and `lethal_company:vanilla/custom` entries documented in `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`.

### Dusk 0.9.25 effective selection semantics

With `PrioritiseMoons = true`, Dusk evaluates:

1. exact Moon key;
2. exact Interior key fallback;
3. matching Moon-tag curves;
4. otherwise zero.

Moon and Interior curves are not combined. Interior entries are not used as an extra tag-fallback set in this mode.

Therefore the smallest verified mutation is:

- validate both exact 18-key dictionaries;
- validate every curve in both dictionaries;
- log both dictionaries before mutation;
- scale only the 18 `CurvesByMoonOrTagName` curves by `0.5`, including values and in/out tangents;
- leave all 18 `CurvesByInteriorOrTagName` curves unmodified.

This covers exact-Moon and Moon-tag evaluation while preserving relative distribution. Scaling each participating Moon/tag curve by 0.5 also leaves any average of matching Moon-tag curves at exactly 0.5 of its previous amplitude.

### Current S1.42AE candidate

- Profile: `Profiles/LC V1 S1.42AE Functional Microwave Provider Contract Correction.r2z`
- Profile SHA-256: `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`
- DLL SHA-256: `f42b25f32dc338617176d6d1d8c76ec3583ab29c7c4a1231c9e5ca4078378357`
- Build run: `33968217356` — SUCCESS
- Build commit: `85e6caade0edd94ac5d7f409b9dd734fc8613f3f`
- Candidate record: `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`
- Status: **BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**

Archive diff vs accepted S1.42AC is isolated to Gale `export.r2x` metadata plus the new S1.42AE DLL. No mod-state or config change is part of the build.

### Runtime acceptance boundary

Required S1.42AE evidence:

- dependency versions validate;
- armed lifecycle marker appears;
- provider marker reports `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`;
- both exact keysets are logged;
- final marker reports all 18 Moon/tag curves scaled by `0.5` and 18 Interior curves validation-only;
- no S1.42AE refusal/error marker;
- ordinary startup/round generation/gameplay remains healthy;
- no new fatal/project-critical regression marker.

S1.42AC remains the accepted rollback/full-normal-stack baseline until S1.42AE passes this runtime gate.
