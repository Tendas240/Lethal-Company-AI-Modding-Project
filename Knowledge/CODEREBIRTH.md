# CodeRebirth and DawnLib Tuning

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted CodeRebirth ownership/tuning rules plus selected S1.42AD implementation boundary  
**Canonical-For:** `coderebirth`  
**Evidence:** `Current/03_PROJECT_CHRONOLOGY.md`, `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`, S1.40B/S1.42Z ProfileSources  
**Related:** `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Package architecture

Modern project stack uses CodeRebirth with DawnLib. **Do not reinstall CodeRebirthLib**; it is a historical removed/forbidden dependency in this project architecture.

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

Do not blank `Money | Enemy Drop Rates` as collateral damage. The project target is unwanted **natural dungeon generation**, not dedicated CodeRebirth money-drop systems.

## CodeRebirth -> Pikmin utility protection

The cumulative compatibility plugin contains a direct utility-kill shield for Pikmin/Puffmin. This is retained because configuration toggles alone did not cover every Autonomous Crane kill path.

## Accepted aerial-defense tuning

S1.42Z accepted project-local transactional scaling of exactly two DawnLib map-object providers:

- `code_rebirth:air_control_unit`: all 18 moon/tag curves × `0.5`;
- `code_rebirth:gunslinger_greg`: all 18 moon/tag curves × `0.5`.

No other map-object provider is modified. The operation scales the curve amplitude/spawn weight; DawnLib subsequently evaluates/rounds the result, so a short sample is not guaranteed to show mathematically exact half-counts.

Aerial-defense DLL SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

Accepted runtime evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

## Selected S1.42AD Functional Microwave scope

The Functional Microwave spawn-rarity reduction is now the explicitly selected next scope after accepted S1.42AC.

An interrupted ChatGPT session committed an **unbuilt source draft** at:

`Patches/S142ADCodeRebirthMicrowaveSpawnTuning/`

Recovery/status authority:

`Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`

The draft intentionally mirrors the accepted S1.42Z DawnLib provider-scaling architecture and currently attempts to:

- validate CodeRebirth `1.6.9`, DawnLib `0.9.25`, Dusk `0.9.25`;
- resolve exactly `code_rebirth:functional_microwave`;
- use `InsideInfo` rather than the aerial-defense `OutsideInfo` path;
- require exactly one `Dusk.MapObjectSpawnMechanics` provider;
- require an exact 19-curve Microwave key set;
- scale only those curves and fail closed on drift.

This is a plausible narrow ownership approach because it follows an already accepted project pattern, but it is **not yet independently source-proven, compiled, built or runtime-tested for the Microwave target**.

The draft hard-codes `SpawnScale = 0.5f`. Do not treat that value as accepted merely because the aerial-defense tuner also uses `0.5`: current Microwave authority only requires the object to become rarer and does not yet define an exact percentage.

Before S1.42AD is armed, independently verify the owner/19-curve contract, complete the mandatory Patch Safety Review, resolve the exact target magnitude and create the explicit build plan.
