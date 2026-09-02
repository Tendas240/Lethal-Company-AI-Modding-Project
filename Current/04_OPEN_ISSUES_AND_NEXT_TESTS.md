# 04 — Open Issues and Next Tests

## Highest priority — S1.40A runtime acceptance

### 1. Valid import
Use Gale **Advanced options -> Import all files** and confirm:
`S1.39 Compatibility Fixes loaded.`

### 2. Currency
No naturally generated Coin, Crisp Dollar Bill or Wallet inside the dungeon. Currency from intended CodeRebirth enemy-drop/merchant/vending systems is not automatically a failure.

### 3. Flash Turret
No naturally generated Flash Turret.

### 4. Post-run config retention
After exiting the test, inspect `BepInEx/config/CodeRebirth.cfg`. It must still contain:
- `Clean Unusued Configs = false`
- blank Coin/Bill/Wallet inside moon/interior weights
- `Flash Turret | Is Inside Hazard = false`
- blank Flash Turret inside weights

If these values survive but objects still naturally spawn, stop config iteration and patch the real DawnLib runtime spawn path instead.

## Other carry-forward checks

- Ogopogo absent.
- Vermin absent.
- Autonomous Crane cannot kill Pikmin/Puffmin through the CodeRebirth utility-kill path.
- GeneralImprovements recharge station performs desired full heal.
- FixCameraResolution 2560x1440 remains correct.
- Old Bird Resonance encounter validation remains open.
- Mirage `neverDeleteRecordings=true` may require manual Main Menu/LethalConfig check.

## After S1.40A acceptance

Build **S1.41** with exact existing BCMER 1.71.0, all four BCMER rain-related events disabled and spawn ownership constrained.
