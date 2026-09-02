# 00 - Current State

**Canonical project state:** S1.39  
**Date:** 2026-09-02  
**Current gameplay/test candidate:** `Profiles/LC V1 S1.39 Cleanup Health Pikmin Shield.r2z`  
**Latest runtime-tested reference:** `Profiles/LC V1 S1.38 1440p Old Bird Resonance.r2z`  
**Game:** Lethal Company V81  
**Repository:** https://github.com/Tendas240/Lethal-Company-AI-Modding-Project

S1.39 is the new canonical handover/test candidate. It has passed deterministic build, archive CRC, member-delta, Thunderstore package-manifest and configuration assertions, but it has **not yet received a runtime acceptance test**.

S1.38 is the newest profile actually run in game. It successfully loaded the S1.37 compatibility plugin, and FixCameraResolution was visually accepted by the user at 2560x1440. Mirage retention did **not** reliably carry through profile import: the user manually set `neverDeleteRecordings=true` in the Main Menu/LethalConfig, after which the S1.38 log confirmed the value was true. That same test phase exposed remaining natural CodeRebirth currency/map-object noise and the crane/Pikmin kill gap, which are addressed by S1.39. Earlier S1.36 runtime testing had already accepted the ship-door failsafe, complete `enemies` output and Pikmin microwave immunity.

## Read order for ChatGPT

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/06_RECENT_WORK_S1.32-S1.39.md`
8. `Current/03_PROJECT_CHRONOLOGY.md`
9. `Current/Projektstatus_S1.39.json`
10. `Current/Aktive_Modliste_S1.39.txt`
11. `Current/S1.39_BUILD_VERIFICATION.txt`
12. `Current/VERIFIKATION_S1.39.txt`
13. `Current/DATEIINVENTAR_S1.39.txt`
14. `Current/SHA256SUMS_S1.39.txt`

## Critical Gale import rule for S1.39

S1.39 embeds:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

Import the `.r2z` with **Advanced options -> Import all files**.

If BepInEx does not log `S1.39 Compatibility Fixes loaded.`, import:

`Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip`

into the same profile.

Do not call the S1.39 runtime safeguards tested until the marker is present.

## Current build lineage

S1.29 gameplay base -> S1.30 -> S1.31 -> S1.32 -> S1.33 -> S1.34 -> S1.35 -> S1.36 -> S1.37 -> S1.38 -> S1.39

S1.29D was a diagnostic derivative only and is never a gameplay base.

Recent distinctions:

- **S1.36:** clean baseline with SCP999 disabled; source profile for deterministic later builds. Runtime accepted the local door failsafe and complete EnemyScan output; the user also confirmed Pikmins were no longer affected by CodeRebirth microwaves.
- **S1.37:** cumulative compatibility DLL adds normal natural-scrap filtering for CodeRebirth currency/credit items.
- **S1.38:** adds fixed 2560x1440 internal resolution and Lethal Resonance configured for Old Bird only. This is the latest runtime-tested reference.
- **S1.39:** disables Ogopogo/Vermin, suppresses natural Flash Turret and currency map-object generation, and adds direct CodeRebirth utility-kill protection for Pikmin/Puffmin. Health recharge is verified enabled in config.

## Explicitly disabled in S1.39

Manifest: 179 entries, 173 active, 6 disabled.

- AJB-Keep_hangar_ship_door_closed
- zealsprince-Malfunctions
- Reiko88-Observer
- ProjectSCP-SCP999
- Kittenji-Dont_Touch_Me
- SoftDiamond-BrutalCompanyMinusExtraReborn

## Persisting stable architecture

- Hold-to-Scan via LethalHUD.
- Pikmin water resistance.
- Company routing + auto landing via CompanyBuildingEnhancements.
- 26 intended normal interiors at Weight 100, Black Mesa through its DawnLib path.
- Rolling Giant / Shy Guy / Siren Head use native spawn ownership.
- RandomEnemiesSize active.
- x753-Mimics / CoronerMimics remain removed/disabled; fake Fire Exits must not be restored.
- Malfunctions remains off until explicit user request.
- BCMER remains off until a later isolated reactivation phase.

## S1.39 immediate acceptance test

1. Import with `Import all files` and confirm `S1.39 Compatibility Fixes loaded.`
2. Land on a suitable moon and verify no natural Flash Turret and no normal natural CodeRebirth currency/map-object spawns.
3. Confirm Ogopogo and Vermin do not spawn.
4. Reproduce CodeRebirth Autonomous Crane proximity with Pikmin/Puffmin and confirm they cannot be killed; look for `[PikminCraneShield]` only when a blocked utility kill is attempted.
5. Damage the player and use the GeneralImprovements recharge station; verify it restores health as desired.
6. Confirm FixCameraResolution remains sharp/native at 2560x1440.
7. If an Old Bird appears, validate mechanical/weapon/footstep/loudspeaker replacement audio from Lethal Resonance.
8. Check Mirage `neverDeleteRecordings` after import. If it reverted, set it manually in the Main Menu/LethalConfig; profile import alone is not trusted for this per-player setting.
9. Preserve the full `LogOutput.log`.
