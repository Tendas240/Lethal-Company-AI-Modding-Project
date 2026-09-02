# Lethal Company AI Modding Project

Current canonical project state: **S1.41**

Current accepted gameplay baseline:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Latest runtime-tested state: **S1.41 — accepted**.

S1.40B fixed the CodeRebirth/DawnLib editing gate for natural Currency and Flash Turret suppression. S1.41 reactivated BCMER 1.71.0 under the ownership/rain-event guard and is runtime-accepted.

## Critical import requirement

Use Gale:

**Advanced options -> Import all files**

Expected project-local patch marker:

`S1.39 Compatibility Fixes loaded.`

BCMER is accepted at exact **1.71.0**. Do not silently update it to 2.0.0; a 2.0 migration would be a separate explicit compatibility stage.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/02_TECHNICAL_BASELINE.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
7. `Current/06_RECENT_WORK_S1.32-S1.41.md`
8. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
9. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
10. `Current/11_RUNTIME_EVIDENCE_S1.41_BCMER.md`
11. `Current/12_HANDOVER_S1.41_TO_S1.42A.md`
12. `Current/03_PROJECT_CHRONOLOGY.md`
13. `Current/Projektstatus_S1.41.json`
14. `Current/Aktive_Modliste_S1.41.txt`
15. `Current/README_Handover_S1.41.txt`
16. `Current/VERIFIKATION_S1.41.txt`
17. `ProfileSources/S1.41/PROFILE_INDEX_RESULT.json`
18. `BuildSpecs/current.json`
19. `BuildSpecs/S1.42A_PLAN.md`

Then inspect `Profiles/`, `ProfileSources/`, `Patches/`, `RuntimeEvidence/`, `Logs/`, `References/` and `Archive/` according to the task.

## Current S1.41 state

Manifest:
- 179 total Thunderstore packages
- 174 enabled
- 5 disabled
- BCMER exact 1.71.0 enabled
- BCMER 2.0.0 not used

Persistent disabled packages:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8

BCMER ownership guard:

```ini
[Mod Compatibility]
Experimental Dont Handle Power? = true
Experimental Dont Handle Spawn Chance? = true
Let Brutal handle properties outside of events? = false

[Randomizer]
Enable Randomizer? = false
```

BCMER rain-event routes disabled:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy weather remains allowed.

## Binding roadmap

**S1.41 accepted -> S1.42A Interior Config Seed -> run/host/land/generate -> collect generated config + LogOutput through RuntimeInbox -> tune -> S1.42 final interior build.**

S1.41 has passed; the next isolated stage is S1.42A.

## Repository-first automation

GitHub is the canonical build and handover workspace.

Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`

Key locations:
- `BuildSpecs/current.json` — build request edited by ChatGPT
- `BuildSystem/profile_builder.py` — deterministic profile builder
- `.github/workflows/profile-build.yml` — online profile build
- `.github/workflows/profile-index.yml` — hash/index verification for uploaded profiles
- `ProfileSources/<build_id>/` — readable profile/config snapshots
- `RuntimeInbox/Current/` — browser upload point for unavoidable runtime-generated files
- `.github/workflows/runtime-ingest.yml` — runtime evidence ingestion
- `RuntimeEvidence/` — persisted/extracted online runtime evidence

The one-time migration is complete: exact S1.40B and S1.41 binaries are now online, hash-verified, and indexed.

Do not require a local repository clone or local PowerShell profile-build scripts when the required base profile exists in GitHub.

## Persistent decisions

- Malfunctions disabled until explicit user request.
- ProjectSCP-SCP999 disabled.
- AJB Keep hangar ship door closed disabled while the local failsafe is active.
- BCMER 1.71.0 is the accepted baseline; do not upgrade to 2.0.0 without an explicit isolated migration stage.
- Observer disabled.
- Don't Touch Me disabled.
- CodeRebirthLib must not return.
- LethalModDataLib is not permanently banned; if DULL requires it, reintroduce only in the isolated interior stage and regression-test it.
- Unknown Enemy PowerLevels must never be guessed.
- Leaf Boy remains on the LethalMin attack blacklist.
- S1.29D is diagnostic only and never a gameplay base.

## Priority rule

Chronologically newer confirmed information overrides older assumptions. Runtime evidence overrides package/config assumptions. `Archive/` is historical reference material and must not override the current machine-readable files unless explicitly referenced.


## Handover checkpoint

Repository handover refreshed on **2026-09-03**.

S1.41 is frozen as the accepted baseline. The next binding task is **S1.42A Interior Config Seed**, planned in `BuildSpecs/S1.42A_PLAN.md`.

No local repository clone and no local PowerShell profile build is required.
