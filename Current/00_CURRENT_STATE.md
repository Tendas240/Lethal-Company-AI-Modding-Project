# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical acceptance state

### Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:
runtime accepted gameplay baseline.

### Current candidate

**S1.42L - Pikmin Counterattack Restore**

Profile:
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Compatibility plugin:
- version 1.3.7
- DLL SHA-256 `7a810d4164394146d64fea2fec300591f4647c9e1b9de834bce4cd1a726e63f2`

Build:
- GitHub Actions success;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only:
  - `BepInEx/config/NoteBoxz.LethalMin.cfg`
  - `export.r2x`;
- no added members;
- compatibility DLL unchanged.

## Latest valid runtime evidence

Evidence:
`RuntimeEvidence/S1.42L/20260903T151817Z/`

Log:
`RuntimeEvidence/S1.42L/20260903T151817Z/raw/LogOutput.log`

Log SHA-256:
`402015463b9ed83a0835a4df8ac7f6298cac662609700715563041e5447885bd`

Verdict:
**PARTIAL PASS - only Pikmin -> Baboon Hawk explicit attack/latch validation remains.**

Observed counts:
- `[ThumperPikminGuard]`: 36
- `Leader is null when following`: 0
- Baboon guard markers: 9
- Puffer guard markers: 8
- Coroner Jetpack `PlayerController was null`: 0

## Closed topics

### Thumper/Crawler

**PASS / CLOSED**

Permanent rule:
- Thumper/Crawler -> Pikmin: no functional GrabPikmin / leader removal / grabbed death timer / broken state.
- Pikmin -> Thumper/Crawler: normal LethalMin attack/latch allowed.

User confirmed Pikmin can again be thrown onto the Thumper and attack it.

Visible Thumper snapping is accepted as harmless cosmetic/AI behavior because Pikmin are not functionally affected. Do not patch this further unless a future regression appears.

### Puffer -> Pikmin

**PASS / CLOSED**

Puffer smoke/attack has no effect on Pikmin.

### Jetpack

**PASS / CLOSED**

Accepted:
- approximately 140-second target;
- `MidAirExplosions = Off`;
- historical Coroner Jetpack null flood absent.

### Baboon Hawk -> Pikmin

**PASS / CLOSED**

Retained exact protection:
- disable exact `LethalMin.BaboonBirdPikminEnemy` after `BaboonBirdAI.Start`;
- block exact declared `BitePikmin`;
- retain exact common `PikminAI.GrabPikmin(Transform,float,int)` Baboon failsafe.

## Only remaining runtime gate

**Pikmin -> Baboon Hawk**

S1.42L removes `Baboon hawk` from LethalMin's Pikmin Attack Blacklist and LethalMin registers the Hawk with one latch trigger, but direct Pikmin attack/latch was not explicitly confirmed in the latest run.

Exact next step:
- keep S1.42L unchanged;
- throw Pikmin directly onto a Baboon Hawk;
- confirm normal latch/attack;
- confirm Hawk-side ignore protection remains intact;
- upload a fresh complete log to `RuntimeInbox/Current/`.

Do not build a successor first.

## Current Attack Blacklist

`Docile Locust Bees,Manticoil,Red Locust Bees,Blob,Nemo,InternNPC,BellCrab,Nancy,Transporter,Janior,Peace Keeper,Guardsman,Tornado,FireStorm,Hurricane,Cabinet, Leaf boy`

This exactly matches modern S1.40B/S1.41.

Recent project-added entries:
- `Crawler` - removed again;
- `Baboon hawk` - removed again.

## Temporary isolated test state

EnemyIsolation:
**enabled**

BCMER 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

After the remaining direction passes:
1. remove/disable EnemyIsolation;
2. restore normal enemy configuration from the S1.42C restore baseline;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted asymmetric enemy/Pikmin interaction rules;
5. document the resulting normal-enemy/BCMER state.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt`:
`S1.42L`

`BuildSpecs/current.json`:
disabled / `IDLE_AFTER_S1.42L_BUILD_AWAITING_RUNTIME`

`RuntimeInbox/Current/`:
empty except `.gitkeep` after successful ingestion.

## Superseded untested builds

- S1.42I - built, never runtime-tested.
- S1.42K - built, never runtime-tested.

Neither is runtime evidence.

## Deferred repository optimization

Plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Status:
**DEFERRED_UNTIL_ACTIVE_GATE_COMPLETE**

Do not perform structural migration before the last S1.42L gate and the resulting normal-enemy/BCMER state are documented.

## Canonical takeover files

- `Current/45_HANDOVER_S1.42L_TO_NEXT_FINAL.md`
- `Current/Projektstatus_S1.42L.json`
- `Current/43_S1.42L_RUNTIME_ANALYSIS_THUMPER_CLOSED.md`
- `Current/41_S1.42L_PIKMIN_COUNTERATTACK_RESTORE_BUILD.md`
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
- `Current/VERIFIKATION_S1.42L.txt`
- `Current/SHA256SUMS_S1.42L.txt`
- `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Historical detail is preserved in:
- `Current/03_PROJECT_CHRONOLOGY.md`
- `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
- older dedicated handovers/analyses;
- `RuntimeEvidence/`.
