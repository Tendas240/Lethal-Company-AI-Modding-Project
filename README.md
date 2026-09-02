# Lethal Company AI Modding Project

Current canonical project state: **S1.40A**

Current gameplay/test candidate:

`Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`

SHA-256:

`ab894ead158941d6f9d6c3463baab51c65486ebf6d40df8b2325fca626d966a5`

Latest runtime-tested state: **S1.40 — failed acceptance**.

S1.40 was actually run in game on 2026-09-02. The cumulative project-local compatibility DLL loaded, but Flash Turret suppression was not reliable and the post-run `CodeRebirth.cfg` proved that the intended sparse CodeRebirth/DawnLib overrides did not survive startup/config cleanup. S1.40A is the isolated retention fix.

## Critical S1.40A import requirement

Use Gale:

**Advanced options -> Import all files**

Expected BepInEx marker:

`S1.39 Compatibility Fixes loaded.`

If the marker is absent, the cumulative local patch was not imported and the run is invalid for patch-dependent acceptance.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/06_RECENT_WORK_S1.32-S1.40A.md`
8. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
9. `Current/08_RUNTIME_EVIDENCE_S1.40_CODE_REBIRTH.md`
10. `Current/03_PROJECT_CHRONOLOGY.md`
11. `Current/Projektstatus_S1.40A.json`
12. `Current/Aktive_Modliste_S1.40A.txt`
13. `Current/S1.40A_BUILD_VERIFICATION.txt`
14. `Current/VERIFIKATION_S1.40A.txt`
15. `Current/DATEIINVENTAR_S1.40A.txt`
16. `Current/SHA256SUMS_S1.40A.txt`
17. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`

Then inspect `Profiles/`, `Patches/`, `Logs/`, `References/` and `Archive/` according to the task.

## Exact S1.40A delta

S1.40A is based on exact S1.40 and replaces only:

`BepInEx/config/CodeRebirth.cfg`

Critical values:

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

Do **not** change `Money | Enemy Drop Rates` unless the user explicitly requests it. Intended CodeRebirth Merchant/Denomination Analyzer/vending/enemy-drop currency systems remain desired.

## Binding roadmap

**S1.40A runtime test -> if Currency + Flash Turret pass -> S1.41 with exact existing BCMER 1.71.0 -> S1.41 runtime test -> S1.42A Interior Config Seed -> run/host/land/generate -> collect full config + LogOutput -> tune -> S1.42 final interior build.**

Do not skip directly to BCMER or interiors while S1.40A remains unaccepted.

## Persistent decisions

- Malfunctions disabled until explicit user request.
- ProjectSCP-SCP999 disabled.
- AJB Keep hangar ship door closed disabled while the local failsafe is active.
- BCMER 1.71.0 parked until S1.40A acceptance. Do not upgrade to BCMER 2.0.0 as part of reactivation.
- Observer disabled.
- Don't Touch Me disabled.
- CodeRebirthLib must not return.
- LethalModDataLib is **not** permanently banned; if DULL requires it, reintroduce only in the isolated interior stage and regression-test it.
- Unknown Enemy PowerLevels must never be guessed.
- Leaf Boy remains on the LethalMin attack blacklist.
- S1.29D is diagnostic only and never a gameplay base.

## Priority rule

Chronologically newer confirmed information overrides older assumptions. Runtime evidence overrides package/config assumptions. `Archive/` is historical reference material and must not override the current machine-readable files unless explicitly referenced.

`Current/HumanReadable/` is secondary. Outdated S1.39 DOCX/PDF handover files were archived so they cannot be mistaken for the current state.

## Repository-first automation

Future project work is **GitHub-first**. The repository is not only the handover source; it is also the canonical build workspace.

Binding workflow policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`

Key locations:
- `BuildSpecs/current.json` — build request edited by ChatGPT;
- `BuildSystem/profile_builder.py` — deterministic profile builder;
- `.github/workflows/profile-build.yml` — GitHub-native build/verification;
- `ProfileSources/<build_id>/` — readable snapshots of generated profile text/configs;
- `RuntimeInbox/Current/` — browser-upload inbox for unavoidable runtime-generated local evidence;
- `RuntimeEvidence/` — automatically persisted/extracted runtime evidence.

Do not require the user to maintain a local repository clone or run local PowerShell profile-build scripts when the required base profile already exists on GitHub. Binary manipulation belongs in GitHub Actions; text/config snapshots must be committed so ChatGPT can inspect them through GitHub.

A one-time migration of the exact locally built S1.41 binary is still required before the online chain is fully self-contained.

