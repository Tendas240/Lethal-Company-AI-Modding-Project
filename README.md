# Lethal Company AI Modding Project

Current canonical project state: **S1.36**

Current gameplay/test profile:

Profiles/LC V1 S1.36 Handover Clean Baseline.r2z

Latest runtime-tested state: **S1.34** — `Profiles/LC V1 S1.34 Malfunctions Disabled.r2z`.

S1.36 is build/diff/archive verified but **not yet runtime-tested**.

## Critical S1.36 import requirement

S1.36 contains a project-local compatibility DLL for the ship-door failsafe and complete EnemyScan output.

When importing the .r2z in Gale, enable:

**Advanced options → Import all files**

If BepInEx does not log S1.35 Compatibility Fixes loaded, import this local mod separately into the S1.36 profile:

Patches/S135CompatibilityFixes/Tendas-S135CompatibilityFixes-1.0.0.zip

Do not evaluate the door/EnemyScan fixes unless the local plugin load is confirmed.

## ChatGPT — read first

A new ChatGPT conversation should use the machine-readable repository content in this order:

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

Then inspect Profiles/, Patches/, Logs/, and References/ according to the task.

## Current key decisions

- **Malfunctions stays disabled** until the user explicitly asks to re-enable it.
- **ProjectSCP-SCP999 stays disabled.** Current runtime logs proved it had accidentally remained active and was throwing a startup NRE; S1.36 corrects the manifest.
- AJB-Keep_hangar_ship_door_closed stays disabled while the S1.35/S1.36 local door patch is used.
- BCMER, Observer and Don't Touch Me remain disabled.
- Leaf Boy remains in the LethalMin Attack Blacklist.
- Mirage neverDeleteRecordings=true remains enabled.
- Unknown PowerLevels must not be guessed.

## Markdown-first rule

.md, .txt, and .json files are the **primary machine-readable handover sources**.

Historical S1.31 PDF/DOCX documents are archived under Archive/S1.31/HumanReadable/ instead of being left under Current/.

A GitHub PDF viewer failure must not block project takeover when equivalent machine-readable sources exist.

For GitHub text files, ChatGPT may prefer raw content:

https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/<PATH>

## Repository structure

- Current/ — current machine-readable state and metadata
- Profiles/ — current and still-relevant Gale/r2modman .r2z profiles
- Patches/ — project-local compatibility source and installable local-mod packages
- Logs/ — runtime logs and diagnostic summaries
- References/ — binding screenshots and reference values
- Archive/ — older primary sources retained for historical diagnosis

## Priority rule

The chronologically newest confirmed information overrides older assumptions.

Runtime evidence overrides package-manifest assumptions when they disagree about what actually loaded.

Files under Archive/ are historical references and must not override a newer confirmed project state unless current documentation explicitly points back to them.

Do not repeat solutions documented as failed or obsolete without new evidence.

## Current first test

Import S1.36 with **Import all files**, launch once, and verify:

- S1.35 Compatibility Fixes loaded
- [EnemyScanFix] ...
- no Loading [SCP999 ...]

Then perform the controlled inside/outside hangar-door tests and compare enemies output against known active enemies.

See Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md for the exact test sequence.

## Handover master prompt

The durable repository workflow and takeover instructions are in START_HERE_ChatGPT_Masterprompt.txt.

The repository is the canonical handover source. A ZIP backup is optional, not required.
