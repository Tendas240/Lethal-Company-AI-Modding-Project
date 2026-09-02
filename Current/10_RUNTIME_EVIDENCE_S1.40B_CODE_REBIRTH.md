# 10 — Runtime Evidence: S1.40B CodeRebirth Editing Gate Fix

**Build:** S1.40B  
**Profile:** `Profiles/LC V1 S1.40B CodeRebirth Editing Gate Fix.r2z`  
**SHA-256:** `fd303f73f0f2223a6375fcf2b7ed209dae77e1934e3b4e8139932a89e7de7eb9`  
**Result:** accepted

## Test observation

The user reported that no Flash Turret, Coin or Wallet was found during the S1.40B test run.

Visual absence alone was not treated as decisive because the relevant objects can be missed during traversal.

## Log evaluation

The evaluated S1.40B runtime log did not show the prior natural Currency instance signatures that were present in failed runs:
- `NewCoinPrefab(Clone)`
- `DollaBill(Clone)`
- `Wallet(Clone)`

No corresponding runtime evidence of a naturally generated Flash Turret was found in the evaluated run.

Registration lines for CodeRebirth prefabs were not treated as spawn evidence; registration only proves the content exists and is available to the mod.

## Decisive post-run config retention

Unlike S1.40/S1.40A, the S1.40B post-run `CodeRebirth.cfg` retained the intended editing-gate values.

Confirmed intent:
- `Clean Unusued Configs = false`
- Coin `Allow Editing Config = true`
- Coin inside moon/interior weights blank
- Crisp Dollar Bill `Allow Editing Config = true`
- Crisp Dollar Bill inside moon/interior weights blank
- Wallet `Allow Editing Config = true`
- Wallet inside moon/interior weights blank
- Flash Turret `Allow Editing Config = true`
- Flash Turret `Is Inside Hazard = false`
- Flash Turret inside moon/interior weights blank

This identifies the relevant DawnLib `Allow Editing Config` gate as the missing piece in S1.40A.

## Acceptance interpretation

S1.40B is accepted because three independent observations aligned:
1. user did not encounter the unwanted natural spawns;
2. prior unwanted runtime clone signatures were absent from the evaluated log;
3. the suppression/editing values survived runtime instead of reverting to mod defaults.

The Flash Turret log path does not provide a mathematically explicit "zero spawned" counter, so future runs should still be watched for regression.

## Consequence

The Currency/Flash-Turret gate no longer blocks BCMER reactivation.

Next stage became S1.41 with exact BCMER 1.71.0.
