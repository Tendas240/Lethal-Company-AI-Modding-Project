# 11 — Runtime Evidence: S1.41 BCMER Reactivation

**Profile:** `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
**SHA-256:** `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`  
**Result:** accepted

## Persisted evidence

GitHub runtime ingestion:
`RuntimeEvidence/S1.41/20260902T215804Z/`

Ingested files:
- `LogOutput.log` — SHA-256 `f0184428806955d88935f437f4f106104c7b5d9a14f97dfa2763d5215f199a8d`
- `CodeRebirth.cfg` — SHA-256 `51e269a79824eb177b1726ee4442ce59f086f75103a2cdb4b6e7829bff08e084`
- `BrutalCompanyMinusExtraReborn.zip` — SHA-256 `f22e390ae17f2d117db5c69bcc16096bdc5432fb0cd3454e53da1d4d9bbf8fb5`

The BCMER ZIP was extracted online and contains all 11 runtime-generated BCMER config files.

## BCMER runtime

Exact `BrutalCompanyMinusExtraReborn 1.71.0` loaded and finished patching.

Observed event selection on Offense:
- Arachnophobia
- ScarceOutsideScrap
- additional event LeaflessTrees

Observed MapMultipliers:
- SpawnChanceMultiplier = 1
- SpawnCapMultiplier = 1
- InsidePower = 0
- OutsidePower = 0
- insideSpawnChanceAdditive = 0
- outsideSpawnChanceAdditive = 0

This run did not show BCMER permanently taking over the established baseline spawn/power architecture.

## Post-run BCMER guard

Confirmed exact retained values:

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

Confirmed disabled after runtime:
- `[Raining] Event Enabled? = false`
- `[HeavyRain] Event Enabled? = false`
- `[AllWeather] Event Enabled? = false`
- `[Hurricane] Event Enabled? = false`

## CodeRebirth regression guard

Post-run `CodeRebirth.cfg` retained:
- `Clean Unusued Configs = false`
- Coin/Bill/Wallet `Allow Editing Config = true`
- Coin/Bill/Wallet inside moon/interior weights blank
- Flash Turret `Allow Editing Config = true`
- `Flash Turret | Is Inside Hazard = false`
- Flash Turret inside moon/interior weights blank

No natural Currency/Flash-Turret regression was identified in this run.

## Mineshaft elevator incident

The user died while descending in the Mineshaft elevator with a large Pikmin group.

Runtime evidence shows:
- many `Failed to create agent because it is not close enough to the NavMesh` warnings around the elevator period;
- fall/gravity death;
- elevator movement completed around the same time window.

Interpretation:
- retain as an open non-blocking LethalMin/Mineshaft elevator regression surface;
- no proof that Pikmin physically pushed the player through the floor;
- no evidence that BCMER caused it.

## Acceptance decision

S1.41 passes its intended BCMER reactivation gate.

Proceed to S1.42A Interior Config Seed.
