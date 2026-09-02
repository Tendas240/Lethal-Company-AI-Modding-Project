# 01 — Handover Core

## Binding state

- Canonical candidate: **S1.41**
- Profile: `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`
- SHA-256: `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`
- Latest runtime-tested state: **S1.41**
- S1.40B status: **accepted**
- S1.41 status: **accepted**
- Game: Lethal Company V81

## Critical recent lineage

### S1.39
The cumulative local compatibility DLL loaded correctly, but late `RoundManager/SelectableLevel` Currency filtering did not catch the actual DawnLib natural spawn path.

### S1.40
Moved Currency/Flash Turret suppression into `CodeRebirth.cfg`. Runtime failed because CodeRebirth/DawnLib restored defaults.

### S1.40A
Set `Clean Unusued Configs = false`. Runtime still failed: the individual relevant content definitions had `Allow Editing Config = false`, so DawnLib continued enforcing author defaults.

### S1.40B
Opened the relevant DawnLib editing gates:
- Coin `Allow Editing Config = true`
- Crisp Dollar Bill `Allow Editing Config = true`
- Wallet `Allow Editing Config = true`
- Flash Turret `Allow Editing Config = true`

Currency inside weights remained blank and Flash Turret remained `Is Inside Hazard = false`.

Post-run values survived and the evaluated test did not show the previous natural Currency/Flash-Turret behavior. **S1.40B accepted.**

### S1.41
Reactivates exact BCMER 1.71.0 without changing the accepted S1.40B CodeRebirth solution.

Manifest:
- 179 total
- 174 enabled
- 5 disabled

BCMER 2.0.0 is not used.

## S1.41 BCMER configuration

```ini
[Events Features]
Disable all events? = false

[Mod Compatibility]
Experimental Dont Handle Power? = true
Experimental Dont Handle Spawn Chance? = true
Let Brutal handle properties outside of events? = false

[Randomizer]
Enable Randomizer? = false
```

Disabled BCMER event routes:

```ini
[Raining]
Event Enabled? = false

[HeavyRain]
Event Enabled? = false

[AllWeather]
Event Enabled? = false

[Hurricane]
Event Enabled? = false
```

GeneralImprovements `SpeakerPlaysIntroVoice = true` is compatible with the BCMER reactivation requirement and was already present, so it did not require a build delta.

## Required local compatibility plugin

Source:
`Patches/S139CompatibilityFixes/`

Embedded DLL:
`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

Expected marker:
`S1.39 Compatibility Fixes loaded.`

Gale profile imports that depend on the local DLL must use:

**Advanced options -> Import all files**

## Persistent project rules

- S1.29D is diagnostic only.
- Malfunctions stays disabled until explicit user request.
- SCP999 stays disabled.
- Observer stays disabled.
- Don't Touch Me stays disabled.
- AJB ship-door mod stays disabled while the local failsafe exists.
- BCMER reactivation is pinned to exact 1.71.0; do not upgrade to 2.0.0 as part of S1.41.
- CodeRebirthLib must not return.
- LethalModDataLib is not a hard ban; reintroduce only if DULL requires it, in the isolated interior stage.
- Unknown Enemy PowerLevels are never guessed.
- Prefer one positive spawn owner per enemy.
- Leaf Boy stays in the LethalMin Attack Blacklist.
- Natural vanilla Rainy weather is allowed; the four disabled rain routes are BCMER events only.

## Repository-first workflow

GitHub is the canonical build workspace.

Do not ask the user to run local profile-build PowerShell scripts or maintain a local repository clone when the base profile is already online.

Use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/<build_id>/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`

Binding policy: `Current/09_REPOSITORY_FIRST_AUTOMATION.md`.

## Binding roadmap

**S1.41 accepted -> S1.42A interior config seed -> runtime config generation -> config/log collection -> S1.42 tuned interior candidate.**

See `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.

## S1.41 acceptance result

Accepted. Runtime evidence is persisted under `RuntimeEvidence/S1.41/20260902T215804Z/`.

Confirmed:
- exact BCMER 1.71.0 loaded and ran events;
- four BCMER rain routes remained disabled post-run;
- ownership-guard values survived post-run;
- S1.40B CodeRebirth Currency/Flash-Turret suppression survived;
- no severe BCMER regression was observed.

New separate issue: Mineshaft elevator + large Pikmin group may trigger NavMesh/collision instability and a player fall-through. Track independently; do not attribute to BCMER without evidence.
