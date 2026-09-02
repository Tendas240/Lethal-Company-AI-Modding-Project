# 00 — Current State

**Canonical project state:** S1.41  
**Date:** 2026-09-02  
**Current gameplay/test profile:** `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
**Current profile SHA-256:** `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`  
**Latest runtime-tested profile:** `Profiles/LC V1 S1.40B CodeRebirth Editing Gate Fix.r2z`  
**Latest runtime result:** S1.40B accepted  
**Game:** Lethal Company V81

## S1.40B acceptance

S1.40B resolved the CodeRebirth/DawnLib editing gate that defeated the S1.40/S1.40A suppression values.

Post-run evidence showed:
- `Clean Unusued Configs = false` survived runtime;
- Coin / Crisp Dollar Bill / Wallet retained `Allow Editing Config = true`;
- their inside moon/interior spawn-weight fields remained blank;
- Flash Turret retained `Allow Editing Config = true`;
- `Flash Turret | Is Inside Hazard = false` remained in the post-run config;
- the user did not observe natural Currency or Flash Turret;
- the evaluated runtime log did not show the prior natural Currency clone signatures.

S1.40B is therefore the latest accepted runtime baseline.

## S1.41 purpose

S1.41 reactivates the exact existing:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

BCMER 2.0.0 is explicitly not used.

Manifest state:
- 179 total Thunderstore entries;
- 174 enabled;
- 5 disabled.

Disabled packages remain:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8

## S1.41 BCMER ownership guard

`CoreProperties.cfg` is configured so BCMER can own its event effects without permanently taking over the established spawn architecture outside events:

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

BCMER rain-event routes are disabled:
- `[Raining] Event Enabled? = false`
- `[HeavyRain] Event Enabled? = false`
- `[AllWeather] Event Enabled? = false`
- `[Hurricane] Event Enabled? = false`

Natural vanilla Rainy weather remains allowed.

## Immediate next task — S1.41 runtime acceptance

Import S1.41 with Gale:

**Advanced options -> Import all files**

Then verify:
1. `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0` loads.
2. BCMER 2.0.0 is not present.
3. `S1.39 Compatibility Fixes loaded.` is still present.
4. BCMER can run normal non-rain events without startup/severe runtime regression.
5. BCMER does not permanently overwrite established spawn/power ownership outside events.
6. Raining / HeavyRain / AllWeather / Hurricane remain disabled in post-run BCMER configs.
7. S1.40B Currency/Flash-Turret suppression does not regress.

Runtime evidence should be uploaded to `RuntimeInbox/Current/`; `RuntimeInbox/ACTIVE_BUILD.txt` is set to `S1.41`.

## Repository-first automation

The repository migration is complete.

Exact S1.40B and S1.41 binaries are now online and were hash-verified/indexed by GitHub Actions. Future profile builds should be executed through:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`

Readable profile contents are available under:
- `ProfileSources/S1.40B/`
- `ProfileSources/S1.41/`

No local repository clone or local PowerShell build chain is required for future profile generation.

## Binding next stage

Only after S1.41 runtime acceptance:

**S1.42A Interior Config Seed -> runtime config generation -> collect full config + LogOutput -> analyze/tune -> S1.42 final interior build.**

See `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.
