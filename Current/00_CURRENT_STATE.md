# 00 — Current State

**Canonical project state:** S1.31  
**Date:** 2026-09-02  
**Current gameplay profile:** `Profiles/LC V1 S1.31 Indoor Power Trim -4.r2z`  
**Game:** Lethal Company V81  
**Repository:** `https://github.com/Tendas240/Lethal-Company-AI-Modding-Project`

## Read order for ChatGPT

Read the machine-readable files in this order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/03_PROJECT_CHRONOLOGY.md`
8. `Current/Projektstatus_S1.31.json`
9. `Current/Aktive_Modliste_S1.31.txt`

Then inspect `Profiles/`, `Logs/`, and `References/` as needed.

`Current/HumanReadable/` contains DOCX/PDF secondary versions for human reading, visual verification, and archival purposes. They are **not required as the primary source for ChatGPT**.

## Priority rule

The chronologically newest confirmed runtime/profile fact overrides older assumptions.  
`Archive/` is historical reference material and must not override a newer confirmed state unless the current documentation explicitly refers back to it.

## Current build lineage

`S1.29 gameplay base` → `S1.30` → `S1.31`

`S1.29D` was a **diagnostic derivative** of S1.29 and is not a gameplay base.

## What S1.31 changes

S1.31 is derived from S1.30 and reduces every controllable indoor enemy power cap by **4**.

It intentionally does **not** change:

- enemy weight lists,
- the confirmed 26-interior equal-weight rotation,
- Pikmin protection settings from S1.30,
- Mimics removal,
- CodeRebirth integration.

## Confirmed working / stable

- Hold-to-Scan via LethalHUD.
- Pikmin water resistance.
- Deadline 0 → Company/Gordion routing and automatic landing via CompanyBuildingEnhancements.
- 26 normal interiors at equal Weight 100 including Black Mesa.
- Rolling Giant / Shy Guy / Siren Head native spawn ownership.
- RandomEnemiesSize.
- GeneralImprovements quota rollover.
- SCP-999 enemy remains disabled.
- x753-Mimics and CoronerMimics are removed.
- CodeRebirth Flash Turret no longer affects Pikmins.

## Latest relevant observations

The latest documented S1.30 run was on **Offense / Deep Sewers**.

Observed:

- Flash Turret protection for Pikmins succeeded.
- No Beehives were seen; on Offense this is not evidence of a bug because Offense is not a normal vanilla Red Locust Bees/Beehive moon.
- A disabled vanilla Turret was found. Cause is not confirmed.
- A recurring dungeon “theme song” was heard. Main candidates are Haunted Harpist / Phantom Piper versus PizzaTowerEscapeMusic.
- Indoor density felt somewhat too high, leading to S1.31.

## Next tests

Prefer **Assurance or March**:

- evaluate S1.31 indoor density,
- observe Beehives on a real vanilla bee moon,
- test Pikmins against a CodeRebirth Microwave,
- if dungeon music appears, record time, Apparatus state, directionality and EnemyScan,
- investigate disabled vanilla Turrets only if the behavior repeats without player/terminal/hacking interaction.

After the run, preserve the full `LogOutput.log`.
