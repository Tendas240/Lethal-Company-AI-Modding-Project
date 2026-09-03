# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current status

Game:

**Lethal Company V81**

### Last fully accepted normal gameplay baseline

**S1.41 — BCMER Reactivation**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

### Latest built/tested technical descendant

**S1.42S — Baboon Adapter Lifecycle Restore**

`Profiles/LC V1 S1.42S Baboon Adapter Lifecycle Restore.r2z`

SHA-256:

`addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`

Compatibility plugin:

**v1.3.14**

DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Focused runtime verdict:

**PASS**

Evidence:

`RuntimeEvidence/S1.42S/20260903T205550Z/`

Log SHA-256:

`9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`

The Baboon-Hawk/Pikmin disappearance regression is resolved: all three focused attackers recovered after Hawk death and native corpse carry to Onion remained functional.

## Temporary state

EnemyIsolation:

**enabled**

BCMER exact 1.71.0:

**disabled**

Thumper Bite Limit:

**3**

Crawler remains attackable by Pikmin.

## Exact next step

Next planned build:

**S1.42T — Normal Enemy Restore**

Use:

`BuildSpecs/S1.42T_PLAN.md`

and:

`Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`

The first restore build should only disable the temporary EnemyIsolation diagnostic while preserving all accepted later fixes and keeping BCMER 1.71.0 disabled.

After that passes, restore exact BCMER 1.71.0 in a separate controlled stage.

Do not upgrade BCMER.

## New ChatGPT takeover

Read in this order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/71_HANDOVER_S1.42S_TO_NEXT_FINAL.md`
3. `Current/72_REPOSITORY_HANDOVER_AUDIT_S1.42S.md`
4. `Current/Projektstatus_S1.42S.json`
5. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
6. `Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`
7. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
8. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
9. `BuildSpecs/S1.42T_PLAN.md`
10. `BuildSpecs/current.json`
11. `RuntimeInbox/ACTIVE_BUILD.txt`

## Permanent patch-safety rule

Every project-local Harmony/runtime/compatibility patch must follow:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Compile/startup success alone is not acceptance. Custom patches must be narrow and must be regression-tested against adjacent/native lifecycle behavior.

## Repository-first rule

Do not ask the user for a local clone/build when the required profile, snapshots, build system, and GitHub Actions workflow already exist in this repository.
