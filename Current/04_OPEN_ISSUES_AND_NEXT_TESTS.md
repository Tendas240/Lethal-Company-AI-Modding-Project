# 04 — Open Issues and Next Tests

## Highest priority — S1.40A runtime acceptance

### 1. Valid import
Import `Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z` with Gale:

**Advanced options -> Import all files**

Confirm:

`S1.39 Compatibility Fixes loaded.`

If this marker is absent, do not evaluate any patch-dependent behavior.

### 2. Natural Currency
Primary acceptance condition:
- no naturally generated Coin inside;
- no naturally generated Crisp Dollar Bill inside;
- no naturally generated Wallet inside.

Currency obtained through intended CodeRebirth Merchant/Denomination Analyzer/vending/enemy-drop systems is not automatically a failure.

### 3. Flash Turret
No naturally generated Flash Turret.

### 4. Post-run config retention
After exiting the game, inspect the exact tested profile's:

`BepInEx/config/CodeRebirth.cfg`

It must still contain:
- `Clean Unusued Configs = false`
- blank Coin/Bill/Wallet Inside Moon Spawn Weights
- blank Coin/Bill/Wallet Inside Interior Spawn Weights
- `Flash Turret | Is Inside Hazard = false`
- blank Flash Turret inside weights

If these values survive but Currency/Flash Turret still naturally spawn, stop iterating the same config approach and patch the actual DawnLib runtime path.

### 5. Preserve evidence
Keep:
- full `LogOutput.log`;
- post-run `CodeRebirth.cfg`;
- exact Gale profile name;
- moon/interior/run observations.

## Other carry-forward checks

When naturally encountered:
- Ogopogo absent.
- Vermin absent.
- Autonomous Crane cannot kill Pikmin/Puffmin through CodeRebirth utility-kill path.
- GeneralImprovements recharge station performs desired full heal.
- Old Bird Resonance replacement set works in a real encounter.
- Mirage `neverDeleteRecordings=true` remains active after import.

## Do not do yet

Until S1.40A passes:
- do not enable BCMER;
- do not install the new interior wave;
- do not upgrade BCMER to 2.0.0;
- do not fabricate interior config IDs/sections in advance.

## After S1.40A acceptance

Follow exactly:

**S1.41 BCMER 1.71.0 isolated build -> runtime test -> S1.42A Interior Config Seed -> run/host/land/generate -> collect config + log -> tune -> S1.42.**

Details: `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.
