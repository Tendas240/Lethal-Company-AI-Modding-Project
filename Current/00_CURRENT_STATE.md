# 00 — Current State

**Canonical project state:** S1.36  
**Date:** 2026-09-02  
**Current gameplay/test profile:** Profiles/LC V1 S1.36 Handover Clean Baseline.r2z  
**Latest runtime-tested profile:** S1.34 — LC V1 S1.34 Malfunctions Disabled  
**Game:** Lethal Company V81  
**Repository:** https://github.com/Tendas240/Lethal-Company-AI-Modding-Project

S1.36 is the new canonical handover candidate and has passed archive/diff/build verification, but it has **not yet received a runtime test**. S1.34 is the most recent profile actually tested in game.

## Read order for ChatGPT

1. START_HERE_ChatGPT_Masterprompt.txt
2. Current/00_CURRENT_STATE.md
3. Current/01_HANDOVER_CORE.md
4. Current/02_TECHNICAL_BASELINE.md
5. Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md
6. Current/05_FAILED_AND_OBSOLETE_APPROACHES.md
7. Current/06_RECENT_WORK_S1.32-S1.36.md
8. Current/03_PROJECT_CHRONOLOGY.md
9. Current/Projektstatus_S1.36.json
10. Current/Aktive_Modliste_S1.36.txt
11. Current/S1.36_BUILD_VERIFICATION.txt
12. Current/VERIFIKATION_S1.36.txt

Then inspect Profiles/, Patches/, Logs/, and References/ as needed.

Historical S1.31 PDF/DOCX and versioned metadata belong under Archive/S1.31/ and must not be mistaken for current documentation.

## Critical Gale import rule for S1.36

S1.36 contains a project-local DLL:

BepInEx/plugins/Tendas-S135CompatibilityFixes/S135CompatibilityFixes.dll

When importing the .r2z in Gale, enable:

**Advanced options → Import all files**

Otherwise Gale may skip the embedded DLL. If that happens, import this local-mod package separately:

Patches/S135CompatibilityFixes/Tendas-S135CompatibilityFixes-1.0.0.zip

A valid S1.36 runtime must log both:

- S1.35 Compatibility Fixes loaded
- [EnemyScanFix] Patched EnemyScan to list every active EnemyAI ...

If these lines are absent, do not evaluate the ship-door or complete-enemy-list fixes; the local patch was not loaded.

## Priority rule

The chronologically newest confirmed runtime/profile fact overrides older assumptions. Runtime evidence overrides package-manifest assumptions when they disagree.

Archive/ is historical reference material and must not override a newer confirmed state unless current documentation explicitly refers back to it.

## Current build lineage

S1.29 gameplay base → S1.30 → S1.31 → S1.32 → S1.33 → S1.34 → S1.35 → S1.36

S1.29D was a diagnostic derivative of S1.29 and is never a gameplay base.

Recent distinctions:

- **S1.32:** Leaf Boy added to the existing LethalMin Attack Blacklist; Mirage recording retention enabled.
- **S1.33:** first custom ship-door failsafe attempt; AJB door mod disabled.
- **S1.34:** Malfunctions disabled by explicit user decision. Runtime proved the custom S1.33 DLL had not been imported/loaded, so door behavior fell back to vanilla.
- **S1.35:** rebuilt local patch for ship-door failsafe + complete EnemyScan output; structurally verified but not runtime-tested.
- **S1.36:** S1.35 plus one cleanup: ProjectSCP-SCP999 disabled because current logs proved it was still loading and throwing a startup NRE despite older documentation saying it was disabled.

## Explicitly disabled in S1.36

Manifest: 176 entries, 170 active, 6 disabled.

- AJB-Keep_hangar_ship_door_closed
- zealsprince-Malfunctions
- Reiko88-Observer
- ProjectSCP-SCP999
- Kittenji-Dont_Touch_Me
- SoftDiamond-BrutalCompanyMinusExtraReborn

**Malfunctions must remain disabled until the user explicitly asks for it to be re-enabled.**

## Confirmed working / stable from earlier runtime tests

- Hold-to-Scan via LethalHUD.
- Pikmin water resistance.
- Deadline 0 → Company/Gordion routing and automatic landing via CompanyBuildingEnhancements.
- 26 normal interiors at equal Weight 100 including Black Mesa.
- Rolling Giant / Shy Guy / Siren Head native spawn ownership.
- RandomEnemiesSize.
- GeneralImprovements quota rollover.
- x753-Mimics and CoronerMimics removed.
- CodeRebirth Flash Turret no longer affects Pikmins.
- Mirage neverDeleteRecordings=true is carried forward.

Leaf Boy attack-loop diagnosis is confirmed; S1.32+ blacklists Leaf boy. Runtime confirmation that the blacklist fully stops the loop is still desirable.

## Important recent findings

- The S1.32 ship-door close trigger itself was not conclusively identified. Malfunctions had no successful relevant door event in the analyzed run.
- A Masked enemy was nearby, but vanilla Masked AI has no hangar-button interaction. Poltergeist dead-player/ghost interaction is a separate mechanic.
- The permanent-lockout risk came from an external/normal close combined with unconditional door-power refill.
- S1.34 proved our custom door DLL had not loaded; its countdown/opening was vanilla behavior, not a failed test of the new algorithm.
- EnemyScan 1.2.1 intentionally omitted EnemyAI without ScanNodeProperties; the S1.35/S1.36 patch removes that display-only filter.
- Puma / PumaAI is the vanilla V80+ Feiopar, not a mod enemy.
- Coin is CodeRebirth currency collected/stored through the Denomination Analyzer and used by CodeRebirth merchant/vending systems.
- Current runtime logs showed ProjectSCP-SCP999 2.4.0 loading and throwing NullReferenceException in SCP999.Plugin.Awake(); S1.36 corrects the manifest state to disabled.

## Immediate next test

Import S1.36 with Import all files and verify the local patch loads before testing anything else.

Then:

1. Close the hangar door while the only living player is inside the landed ship: power should remain at 100%.
2. Close the door with all living players outside: vanilla hydraulic countdown should run and reopen the door.
3. Use enemies while known scanless/modded enemies are active and compare against visible/runtime-spawned enemies.
4. Confirm no SCP999 plugin load or startup NRE occurs.
5. Confirm Leaf Boy is no longer attacked by Pikmins.

After the run, preserve the full LogOutput.log.
