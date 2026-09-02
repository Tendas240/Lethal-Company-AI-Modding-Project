# Lethal Company AI Modding Project

Current canonical project state: **S1.40A**

Current gameplay/test candidate:

`Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`

Latest runtime-tested reference: **S1.40** - `Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z`.

S1.40 was run in game on 2026-09-02 and failed acceptance. The cumulative S1.39 compatibility DLL loaded, but a Flash Turret was still observed. The post-run `CodeRebirth.cfg` proved the intended S1.40 overrides did not survive startup: `Clean Unusued Configs = true`, `Flash Turret | Is Inside Hazard = true`, and Currency moon curves had returned to positive defaults.

S1.40A is an isolated config-retention fix. It keeps the exact S1.40 package/mod architecture and changes only the existing `BepInEx/config/CodeRebirth.cfg`.

## Critical S1.40A import requirement

Use Gale **Advanced options -> Import all files**.

Expected marker: `S1.39 Compatibility Fixes loaded.`

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/06_RECENT_WORK_S1.32-S1.40A.md`
8. `Current/03_PROJECT_CHRONOLOGY.md`
9. `Current/Projektstatus_S1.40A.json`
10. `Current/Aktive_Modliste_S1.40A.txt`
11. `Current/S1.40A_BUILD_VERIFICATION.txt`
12. `Current/VERIFIKATION_S1.40A.txt`
13. `Current/DATEIINVENTAR_S1.40A.txt`
14. `Current/SHA256SUMS_S1.40A.txt`

## Exact S1.40A delta

Base: `Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z`

Exactly one existing ZIP member is replaced:

`BepInEx/config/CodeRebirth.cfg`

```ini
[General]

Clean Unusued Configs = false

[Merchant Options]

Coin | Inside Moon Spawn Weights =
Coin | Inside Interior Spawn Weights =
Crisp Dollar Bill | Inside Moon Spawn Weights =
Crisp Dollar Bill | Inside Interior Spawn Weights =
Wallet | Inside Moon Spawn Weights =
Wallet | Inside Interior Spawn Weights =

[FlashTurret Options]

Flash Turret | Is Inside Hazard = false
Flash Turret | Inside Moon Spawn Weights =
Flash Turret | Inside Interior Spawn Weights =
```

Do not change `Money | Enemy Drop Rates`.

## Persistent decisions

- Malfunctions stays disabled until explicitly requested.
- ProjectSCP-SCP999 stays disabled.
- AJB Keep hangar ship door closed stays disabled while the local failsafe is active.
- BCMER 1.71.0 stays disabled until S1.40A passes; do not upgrade to BCMER 2.0.0 during planned reactivation.
- Observer and Don't Touch Me stay disabled.
- CodeRebirthLib must not return.
- Unknown Enemy PowerLevels are never guessed.

## Roadmap

**S1.40A test -> if Currency + Flash Turret pass -> S1.41 BCMER 1.71.0 isolated reactivation -> S1.41 test -> S1.42A interior config seed -> collect generated config/log -> S1.42 tuned interior build.**

Newest confirmed runtime evidence overrides older assumptions. `Archive/` is historical only.
