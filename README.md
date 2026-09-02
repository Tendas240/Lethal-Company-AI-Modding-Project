# Lethal Company AI Modding Project

Current canonical project state: **S1.40**

Current gameplay/test candidate:

`Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z`

Latest runtime-tested reference: **S1.39** - `Profiles/LC V1 S1.39 Cleanup Health Pikmin Shield.r2z`.

S1.39 was run in game on 2026-09-02. The S1.39 compatibility DLL loaded correctly, but natural CodeRebirth Coins and Wallets still spawned in the dungeon. No Flash Turret was observed by the user in that run, which is positive but not sufficient to prove deterministic suppression. S1.40 changes the spawn authority directly at CodeRebirth/DawnLib config level.

## Critical S1.40 import requirement

S1.40 still embeds the cumulative project-local S1.39 compatibility DLL. When importing the `.r2z` in Gale, enable:

**Advanced options -> Import all files**

Expected BepInEx marker:

- `S1.39 Compatibility Fixes loaded.`

If that marker is absent, import this local mod separately:

`Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip`

The local DLL is unchanged in S1.40; the S1.40 delta is config-only.

## ChatGPT - read first

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

Then inspect `Profiles/`, `Patches/`, `Logs/`, `References/`, and `Current/HumanReadable/` according to the task.

## What S1.40 changes

S1.40 is built directly from the verified S1.39 archive and adds exactly one profile member:

`BepInEx/config/CodeRebirth.cfg`

Native DawnLib/CodeRebirth inside spawning is disabled for:

- Coin
- Crisp Dollar Bill
- Wallet
- Flash Turret

Currency items remain registered. The existing CodeRebirth merchant, denomination analyzer, vending and enemy-drop systems are not intentionally removed. Flash Turret is disabled as an inside hazard at the native config source.

The S1.39 compatibility plugin remains unchanged and continues to provide ship-door anti-lockout, complete EnemyScan output, older currency/map-object defensive filters, Flash Turret defensive filtering and the CodeRebirth utility-kill Pikmin/Puffmin shield.

## Persistent decisions

- **Malfunctions stays disabled** until the user explicitly requests reactivation.
- **ProjectSCP-SCP999 stays disabled.**
- AJB-Keep_hangar_ship_door_closed stays disabled while the local door failsafe is used.
- **BCMER stays disabled during S1.40 acceptance.** Reactivation remains a later isolated audit.
- Observer and Don't Touch Me stay disabled.
- Leaf Boy remains in the LethalMin Attack Blacklist.
- Mirage `neverDeleteRecordings=true` remains desired; profile import of this game-root setting is not considered reliable.
- Unknown enemy PowerLevels must never be guessed.
- CodeRebirthLib must not be reintroduced.

## Runtime distinction

**Runtime-tested:** S1.39.

Confirmed: S1.39 compatibility plugin loaded. Natural Coins and Wallets were still present, so the S1.39 currency cleanup is a confirmed failed approach for the natural DawnLib map-object path. Flash Turrets were not observed in the user run but require deterministic retest.

**Build-tested only:** S1.40.

S1.40 archive structure and critical config delta are verified. Runtime acceptance remains open.

## Priority rule

The chronologically newest confirmed information overrides older assumptions. Runtime evidence overrides package-manifest assumptions when they disagree.

`Archive/` is historical reference material and must not override a newer confirmed state unless current documentation explicitly points back to it.
