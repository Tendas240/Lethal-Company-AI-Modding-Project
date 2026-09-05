# CodeRebirth and DawnLib Tuning

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted CodeRebirth ownership/tuning rules plus current Functional Microwave correction boundary  
**Canonical-For:** `coderebirth`  
**Evidence:** `Current/03_PROJECT_CHRONOLOGY.md`, `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, S1.42Z/S1.42AD ProfileSources and runtime evidence  
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

## Functional Microwave rarity — S1.42AD rejected implementation

The user's authorized balance target remains that Functional Microwaves should be encountered **half as often**, represented by:

`SpawnScale = 0.5f`

S1.42AD attempted to apply that target through:

`code_rebirth:functional_microwave`

via:

`DawnMapObjectInfo.InsideInfo.SpawnWeights -> ProviderTable -> Dusk.MapObjectSpawnMechanics`

Candidate artifact:

- Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`
- Profile SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- DLL SHA-256: `45f22f9b27e3ab7c853fe742bb7c2ce9bc94abc5a0856bb278c747076a2f99c7`
- Build run: `33959742235` — SUCCESS
- Runtime: `RuntimeEvidence/S1.42AD/20260905T103333Z/`
- Decision: `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`
- Status: **RUNTIME REJECTED / NOT ACCEPTED**

### What runtime proved

The plugin loaded and validated CodeRebirth `1.6.9`, DawnLib `0.9.25` and Dusk `0.9.25`, then armed for the moon-registry freeze.

At the callback it failed closed because the runtime provider exposed **18 Interior/tag curves**, while the S1.42AD contract expected zero. The actual Interior key set included `code_rebirth:functional_microwave_ultra_high`.

No final S1.42AD application marker exists. The `0.5` mutation therefore did not execute.

### Corrected authority after S1.42AD

The pre-build provenance inference that shipped CodeRebirth `1.6.9` should expose 18 Moon curves and **0 Interior curves** for this provider is no longer authoritative. Direct runtime evidence supersedes that inference.

However, this run does **not** establish the complete replacement contract because S1.42AD returned immediately after the Interior-count mismatch, before validating/logging the Moon dictionary.

Therefore the current known facts are:

- exact Functional Microwave provider key resolution succeeds;
- exact dependency versions succeed;
- at least one `MapObjectSpawnMechanics` provider is reached;
- the runtime provider has 18 Interior/tag curves, not zero;
- `code_rebirth:functional_microwave_ultra_high` exists in that Interior set;
- the exact runtime Moon-curve count/key set still requires explicit resolution;
- the exact DawnLib selection/evaluation semantics with `PrioritiseMoons = true` still require proof.

### Successor safety contract

Before a corrected successor is armed:

1. inspect/log both Moon and Interior dictionaries before any refusal/mutation;
2. prove `MapObjectSpawnMechanics` selection/evaluation behavior under `PrioritiseMoons = true`;
3. determine which table or tables actually contribute to Functional Microwave effective rarity in the project's target moon/interior contexts;
4. freeze exact key sets only after that proof;
5. scale only the verified effective path needed for the user-authorized `0.5` target;
6. preserve fail-closed behavior on dependency/provider/key-set drift.

Do **not** solve S1.42AD by merely removing the Interior check, by blindly scaling both dictionaries, by fuzzy key matching, by alternate-provider fallback, or by a global DawnLib selection patch.

S1.42AC remains the accepted gameplay baseline while this correction is unresolved.
