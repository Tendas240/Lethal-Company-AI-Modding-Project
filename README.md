# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current state

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41 - BCMER Reactivation**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Latest valid runtime evidence:
**S1.42N - target resolver PASS / state-finalization FAIL**

`RuntimeEvidence/S1.42N/20260903T165818Z/`

Log SHA-256:
`8ed6a79230e28535a01a4cb86a8971c358a5c9f57a53722e18ff4342474f51cf`

Current built candidate:
**S1.42O - Baboon Hawk Native Task Finalization**

`Profiles/LC V1 S1.42O Baboon Hawk Native Task Finalization.r2z`

SHA-256:
`04d7e0df7f7a3b51d75832e9052c3e217ec07f91526c767323e1b5b0a3078d4d`

Compatibility plugin:
**v1.3.10**

## S1.42N runtime finding

The one-shot `RoundManager.Instance.SpawnedEnemies` resolver worked: it selected **6/6 actual Pikmin attack participants** near the dying Hawk.

The failure moved one layer deeper. Direct `PikminAI.RemoveCurrentTask()` left five selected Pikmin in LethalMin Work state without a task:
- **2155** `Work state with no task assigned!` warnings;
- approximately five Pikmin matched the user's observed running-in-place, non-following, unusable group;
- one continued stale Hawk hit output after death.

The healthy control `PerDu` naturally executed:
`Task finished -> Setting to idle -> Removing current task`
and later accepted a normal CarryItem task.

## Active S1.42O runtime gate

S1.42O keeps the validated 4.0 m one-shot resolver and the passing corpse guard.

The only lifecycle change is:
- no direct low-level `RemoveCurrentTask()`;
- resolve and invoke exact declared zero-argument `LethalMin.PikminAI.TaskFinished()`;
- no harmful RemoveCurrentTask fallback if TaskFinished cannot be resolved.

Required result:
1. Pikmin still attack/latch/kill a living Baboon Hawk.
2. At Hawk death, selected attackers complete through native TaskFinished.
3. No sustained `Work state with no task assigned!` loop.
4. No stale dead-Hawk hit loop.
5. Affected Pikmin remain responsive/recoverable/followable and reusable.
6. Following count can be restored after the fight.
7. Dead Baboon Hawk corpse still reaches Onion.
8. Living Hawks still ignore corpse.
9. Hawk -> Pikmin ignore remains intact.
10. No leader-null loop.

## Temporary diagnostic state

EnemyIsolation:
**enabled**

BCMER exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER before S1.42O passes.

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42O`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42O_BUILD_AWAITING_RUNTIME`

Profiles containing the project-local DLL must be imported with Gale:

**Advanced options -> Import all files**

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/Projektstatus_S1.42O.json`
3. `Current/52_S1.42N_NATIVE_TASK_FINALIZATION_ANALYSIS.md`
4. `Current/53_S1.42O_BABOON_HAWK_NATIVE_TASK_FINALIZATION_BUILD.md`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `BuildSpecs/current.json`
9. `RuntimeInbox/ACTIVE_BUILD.txt`
10. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
11. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
12. `Current/02_TECHNICAL_BASELINE.md`
13. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## Critical persistent rules

- Do not reintroduce the S1.42D broad/inherited LethalMin reflection/Harmony scan.
- Do not use continuous Update-driven global EnemyAI scans for this death cleanup.
- Do not restore direct low-level RemoveCurrentTask as the Hawk death finalizer.
- Do not silently upgrade BCMER 1.71.0 to 2.0.0.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not let `CodeRebirthLib` return.
- Unknown Enemy PowerLevels must never be guessed.
- Profiles with the local compatibility DLL require Gale "Import all files".

## Deferred maintenance

Do not clean during the open S1.42O runtime gate:
- older "current" wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in untouched historical parts of `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural optimization:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
