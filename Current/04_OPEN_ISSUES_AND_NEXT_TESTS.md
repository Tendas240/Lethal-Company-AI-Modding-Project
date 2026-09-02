# 04 — Open Issues and Next Tests

## Highest priority — S1.40 runtime acceptance

### 1. Plugin carry-forward
Confirm startup contains `S1.39 Compatibility Fixes loaded.`. If missing, the import is invalid for the cumulative DLL features.

### 2. Native currency cleanup
Primary S1.40 acceptance test:
- no naturally generated Coin in dungeon;
- no naturally generated Crisp Dollar Bill in dungeon;
- no naturally generated Wallet in dungeon.

Currency obtained through intended CodeRebirth systems is not automatically a failure. The target is natural inside map-object generation.

### 3. Flash Turret
Confirm no naturally generated Flash Turret. S1.39 had no user-observed Flash Turret, but one run was not enough to prove suppression.

### 4. Other S1.39 checks still open
- Ogopogo absent.
- Vermin companion mechanic absent.
- Autonomous Crane cannot kill Pikmin/Puffmin through the CodeRebirth utility-kill RPC path.
- GeneralImprovements recharge station performs desired full heal.
- 2560x1440 carry-forward remains correct.
- Old Bird Lethal Resonance can be validated during a real encounter.
- Mirage `neverDeleteRecordings=true` should be checked after import and set manually in Main Menu/LethalConfig if it reverted.

## Confirmed failed approach

S1.39 filtering of `SelectableLevel.indoorMapHazards` / legacy `spawnableMapObjects` around `RoundManager.SpawnMapObjects` did not stop natural CodeRebirth Coins/Wallets even though the plugin loaded. Do not treat additional naming heuristics in that same late filter as the preferred next fix.

## After S1.40 acceptance

BCMER may be reintroduced only as a separate isolated build/re-audit. Do not combine BCMER reactivation with S1.40 acceptance.
