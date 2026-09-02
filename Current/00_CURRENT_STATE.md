# 00 — Current State

**Canonical project state:** S1.41  
**Date:** 2026-09-02  
**Current gameplay profile:** `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
**Current profile SHA-256:** `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`  
**Latest runtime-tested profile:** `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
**Latest runtime result:** S1.41 accepted  
**Game:** Lethal Company V81

## S1.41 runtime acceptance

The complete S1.41 evidence was ingested online under:

`RuntimeEvidence/S1.41/20260902T215804Z/`

The ingestion workflow completed successfully and preserved:
- `LogOutput.log`
- `CodeRebirth.cfg`
- full `BrutalCompanyMinusExtraReborn/` config ZIP, including extracted configs.

BCMER runtime:
- exact `BrutalCompanyMinusExtraReborn 1.71.0` loaded and finished patching;
- ordinary BCMER events executed: Arachnophobia + ScarceOutsideScrap, with LeaflessTrees as an additional event;
- observed event MapMultipliers did not show a permanent baseline takeover in this run;
- no severe BCMER startup/landing/event-selection regression was observed.

Post-run BCMER config retained:
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

Post-run BCMER rain-event routes remained disabled:
- `Raining`
- `HeavyRain`
- `AllWeather`
- `Hurricane`

S1.40B CodeRebirth regression guard also survived:
- `Clean Unusued Configs = false`
- Coin/Bill/Wallet editing gates true
- Coin/Bill/Wallet inside moon/interior weights blank
- Flash Turret editing gate true
- `Flash Turret | Is Inside Hazard = false`
- Flash Turret inside weights blank

No natural Currency/Flash-Turret regression was identified in the S1.41 test.

**S1.41 is accepted.**

## New non-blocking issue — Mineshaft elevator + large Pikmin group

During the accepted S1.41 run, the user clipped through the Mineshaft elevator floor while descending with many Pikmin and died from fall damage.

The log shows:
- many `Failed to create agent because it is not close enough to the NavMesh` warnings around the elevator period;
- Coroner recorded gravity/fall damage;
- the elevator completed its movement shortly around the death window.

This does **not** currently prove that Pikmin physically pushed the player through the floor, and there is no evidence that BCMER caused it.

Track as a separate regression surface:
**Mineshaft elevator + large Pikmin group / NavMesh crowding**.

Do not block S1.42A solely on this one occurrence, but test elevators carefully in later interior work.

## Repository-first automation

Repository-first migration is complete. Future builds use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`

No local repository clone or local PowerShell build chain is required.

## Binding next stage

**S1.42A Interior Config Seed**

Add the eight binding interior packages without speculative deep tuning, generate their real runtime configs/IDs, upload complete config/log evidence, then tune S1.42.

See `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.
