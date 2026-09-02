# 01 — Handover Core

## Binding state

- Canonical candidate: **S1.40A**
- Profile: `Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`
- SHA-256: `ab894ead158941d6f9d6c3463baab51c65486ebf6d40df8b2325fca626d966a5`
- Latest runtime-tested state: **S1.40**
- S1.40 status: **failed acceptance**
- S1.40A status: build/archive/config verified; runtime pending
- Game: Lethal Company V81

## Critical lineage

### S1.36
Accepted clean baseline for:
- ship-door anti-lockout behavior;
- complete EnemyScan output;
- CodeRebirth microwave/Pikmin protection.

### S1.37
Added normal-scrap Currency filtering. Later proved insufficient for CodeRebirth's separate DawnLib map-object path.

### S1.38
Added fixed 2560x1440 FixCameraResolution and Old-Bird-only Lethal Resonance. Mirage retention required manual setting after import.

### S1.39
Added broader late map-object Currency/Flash Turret filtering, Ogopogo/Vermin disablement, recharge-station config carry-forward and direct CodeRebirth utility-kill Pikmin/Puffmin shield. The local plugin loaded in runtime, but Currency still naturally spawned. Therefore late `RoundManager/SelectableLevel` filtering is a confirmed insufficient primary solution.

### S1.40
Moved Currency/Flash Turret suppression into `CodeRebirth.cfg`. Runtime testing still produced a Flash Turret and the post-run config proved CodeRebirth cleanup/default generation had restored the relevant values.

### S1.40A
Keeps S1.40 suppression values and additionally sets:

`Clean Unusued Configs = false`

This is intentionally a minimal isolation build. The local DLL is unchanged.

## Exact S1.40A CodeRebirth config intent

```ini
[General]

Clean Unusued Configs = false

[Merchant Options]

Coin | Inside Moon Spawn Weights =
Coin | Inside Interior Spawn Weights =
Crisp Dollar Bill | Inside Moon Spawn Weights =
Crisp Dollar Bill | Inside Interior Spawn Weights =
Wallet | Inside Moon Spawn Weights =
Wallet | Inside Interior Spawn Weights =

[FlashTurret Options]

Flash Turret | Is Inside Hazard = false
Flash Turret | Inside Moon Spawn Weights =
Flash Turret | Inside Interior Spawn Weights =
```

Do not alter `Money | Enemy Drop Rates` as part of this fix.

## Required local plugin

Source/package:

`Patches/S139CompatibilityFixes/`

Fallback ZIP:

`Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip`

Fallback ZIP SHA-256:

`ec02f79c56f2f3ce24c8f625be3b51cea68b5a71a2a24d3ac8b4996f02c055c1`

Embedded DLL:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

Expected marker:

`S1.39 Compatibility Fixes loaded.`

Gale must use **Advanced options -> Import all files**.

## Persistent project rules

- S1.29D is diagnostic only.
- Malfunctions stays disabled until explicit user request.
- SCP999 stays disabled.
- BCMER remains disabled until S1.40A passes.
- AJB ship-door mod stays disabled while the local failsafe exists.
- CodeRebirthLib must not return.
- LethalModDataLib is not a hard ban; reintroduce only if DULL requires it, in the isolated interior stage.
- Unknown Enemy PowerLevels are never guessed.
- Prefer one positive spawn owner per enemy.
- Rolling Giant, Shy Guy/Scopophobia and Siren Head remain native-owned unless new evidence says otherwise.
- Leaf Boy stays in LethalMin Attack Blacklist.
- Natural vanilla Rainy weather is allowed; later BCMER rain suppression applies only to BCMER event routes.

## Binding roadmap

**S1.40A test -> S1.41 BCMER 1.71.0 -> S1.41 test -> S1.42A interior config seed -> runtime config generation -> config/log collection -> S1.42 tuned interior candidate.**

See `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` before changing BCMER or interiors.

## Current acceptance gate

S1.40A is accepted only after:
- no natural Coin / Crisp Dollar Bill / Wallet;
- no natural Flash Turret;
- post-run CodeRebirth config retains the S1.40A values;
- full runtime log is preserved.
