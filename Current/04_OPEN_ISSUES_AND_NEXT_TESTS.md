# 04 — Open Issues and Next Tests

## Highest priority — S1.41 runtime acceptance

### 1. Valid import

Import:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Use Gale:

**Advanced options -> Import all files**

Confirm:
- `S1.39 Compatibility Fixes loaded.`
- BCMER exact version 1.71.0 loads.

### 2. BCMER version and event operation

Expected:
- `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0` active;
- BCMER 2.0.0 absent;
- ordinary BCMER events may occur;
- no severe startup, landing, lever-pull, event-selection or networking regression.

### 3. Spawn/power ownership

Post-run `CoreProperties.cfg` must retain:

```ini
Experimental Dont Handle Power? = true
Experimental Dont Handle Spawn Chance? = true
Let Brutal handle properties outside of events? = false
Enable Randomizer? = false
```

BCMER may modify gameplay as part of an event. It must not silently become the permanent owner of established spawn/power architecture outside events.

### 4. Rain-event suppression

The following BCMER event sections must remain disabled after runtime:
- `Raining`
- `HeavyRain`
- `AllWeather`
- `Hurricane`

This does not disable vanilla Rainy weather.

### 5. S1.40B regression guard

Continue checking:
- no natural Coin / Crisp Dollar Bill / Wallet in the dungeon;
- no natural Flash Turret;
- CodeRebirth post-run editing-gate/suppression values remain intact.

### 6. Runtime evidence upload

After the S1.41 test, upload runtime evidence through GitHub:

`RuntimeInbox/Current/`

Preferred:
- full `LogOutput.log`;
- complete `BepInEx/config/BrutalCompanyMinusExtraReborn/` as ZIP;
- `CodeRebirth.cfg` if a Currency/Flash-Turret regression is suspected;
- screenshots only when they document a meaningful runtime observation.

The ingestion workflow will hash, preserve and extract the evidence under `RuntimeEvidence/S1.41/<timestamp>/`.

## Other carry-forward checks

When naturally encountered:
- Ogopogo absent.
- Vermin absent.
- Autonomous Crane cannot kill Pikmin/Puffmin through CodeRebirth utility-kill path.
- GeneralImprovements recharge station performs desired full heal.
- Old Bird Resonance replacement set works in a real encounter.
- Mirage `neverDeleteRecordings=true` remains active after import.

## Do not do yet

Until S1.41 passes:
- do not start the interior expansion;
- do not upgrade BCMER to 2.0.0;
- do not fabricate interior config IDs/sections in advance.

## After S1.41 acceptance

Follow exactly:

**S1.42A Interior Config Seed -> run/host/land/generate -> collect config + log -> tune -> S1.42.**

Details: `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.
