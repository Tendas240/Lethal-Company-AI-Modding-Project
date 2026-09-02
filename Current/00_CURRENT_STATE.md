# 00 — Current State

**Canonical project state:** S1.40  
**Date:** 2026-09-02  
**Current gameplay/test profile:** Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z  
**Latest runtime-tested profile:** Profiles/LC V1 S1.39 Cleanup Health Pikmin Shield.r2z  
**Game:** Lethal Company V81

S1.40 is the current build/test candidate. S1.39 is the newest profile actually run in game.

## Read order for ChatGPT

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/06_RECENT_WORK_S1.32-S1.40.md`
8. `Current/03_PROJECT_CHRONOLOGY.md`
9. `Current/Projektstatus_S1.40.json`
10. `Current/Aktive_Modliste_S1.40.txt`
11. `Current/S1.40_BUILD_VERIFICATION.txt`
12. `Current/VERIFIKATION_S1.40.txt`
13. `Current/DATEIINVENTAR_S1.40.txt`
14. `Current/SHA256SUMS_S1.40.txt`

## S1.39 runtime result that triggered S1.40

The S1.39 local plugin loaded correctly, so the test was valid for the custom DLL. Natural CodeRebirth Coins and Wallets nevertheless still spawned in the dungeon. This disproved the assumption that filtering `SelectableLevel` map-object arrays around `RoundManager.SpawnMapObjects` was sufficient for CodeRebirth currency.

CodeRebirth 1.6.9 registers Coin, Crisp Dollar Bill and Wallet through DawnLib/Dusk as their own inside map objects with native spawn curves. Therefore S1.40 disables the natural inside spawn source through CodeRebirth's generated config instead of adding another late Harmony filter.

The user did not encounter a Flash Turret in the S1.39 run. Treat that as inconclusive positive evidence, not proof.

## Exact S1.40 delta

S1.40 is based on S1.39 and adds one archive member:

`BepInEx/config/CodeRebirth.cfg`

Critical values:

- `[Merchant Options] Coin | Inside Moon Spawn Weights =`
- `[Merchant Options] Coin | Inside Interior Spawn Weights =`
- `[Merchant Options] Crisp Dollar Bill | Inside Moon Spawn Weights =`
- `[Merchant Options] Crisp Dollar Bill | Inside Interior Spawn Weights =`
- `[Merchant Options] Wallet | Inside Moon Spawn Weights =`
- `[Merchant Options] Wallet | Inside Interior Spawn Weights =`
- `[FlashTurret Options] Flash Turret | Is Inside Hazard = false`
- Flash Turret inside moon/interior weights are also blank.

DawnLib parses blank spawn-weight strings as no registered curves; its map-object provider then returns a constant zero curve when no moon/interior curve matches.

No Thunderstore package was added/removed. Manifest remains 179 total / 173 active / 6 disabled. The S1.39 local DLL is carried forward unchanged.

## Critical Gale import rule

Use **Advanced options -> Import all files** because the cumulative local S1.39 compatibility DLL is still embedded.

Expected marker:

- `S1.39 Compatibility Fixes loaded.`

## Persistent decisions

- Malfunctions remains disabled until explicitly requested otherwise.
- SCP999 remains disabled.
- BCMER remains disabled through S1.40 acceptance.
- AJB ship-door mod remains disabled.
- CodeRebirthLib must not be reintroduced.
- Unknown PowerLevels are never guessed.

## Immediate next test

1. Confirm the S1.39 compatibility DLL still loads.
2. Confirm no natural Coin / Crisp Dollar Bill / Wallet spawns in the dungeon.
3. Confirm no natural Flash Turret spawns.
4. Check Ogopogo/Vermin remain absent.
5. Retest Autonomous Crane against Pikmin/Puffmin if encountered.
6. Verify GeneralImprovements recharge station full-heal behavior.
7. Preserve full `LogOutput.log`.
