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
**S1.42O - FAIL / no Hawk-death cleanup executed**

`RuntimeEvidence/S1.42O/20260903T171220Z/`

Log SHA-256:
`1a1251f19a1d82e90b72e82ac8e4babd523c32e695fe3d7923d4590debb0be71`

Current built candidate:
**S1.42P - Baboon Hawk Exact FinishTask Recovery**

`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Compatibility plugin:
**v1.3.11**

## S1.42O finding

S1.42O attempted `LethalMin.PikminAI.TaskFinished()`, but the loaded LethalMin type has no such method. The patch therefore correctly performed no low-level fallback.

User result:
**8 Pikmin disappeared after Hawk death.**

The runtime method list explicitly exposes the actual high-level method:
`LethalMin.PikminAI.FinishTask():Void`

The same eight attackers continued `Hitting enemy with: 0.03` after Hawk death and beyond the SellBodies corpse-spawn point.

## Active S1.42P runtime gate

S1.42P keeps:
- one-shot `RoundManager.Instance.SpawnedEnemies` resolver;
- exact/assignable `LethalMin.PikminAI` filtering;
- 4.0 m Hawk-death zone;
- passing Dead Baboon Hawk corpse guard.

It now uses the runtime-confirmed exact:
`PikminAI.FinishTask()`

No `RemoveCurrentTask()` fallback.

Required result:
1. exact FinishTask resolves at startup;
2. real Hawk attackers are selected;
3. native FinishTask runs at Hawk death;
4. attackers stop hitting the dead Hawk;
5. affected Pikmin remain visible/responsive;
6. they can be whistled/regained and follow/reuse normally;
7. following count can be restored;
8. corpse still reaches Onion;
9. living Hawks ignore corpse;
10. Hawk -> Pikmin ignore remains intact;
11. no leader-null loop.

## Temporary diagnostic state

EnemyIsolation:
**enabled**

BCMER exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER before S1.42P passes.

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_BUILD_AWAITING_RUNTIME`

Profiles containing the project-local DLL must be imported with Gale:

**Advanced options -> Import all files**

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/Projektstatus_S1.42P.json`
3. `Current/54_S1.42O_NO_CLEANUP_FINISHTASK_ANALYSIS.md`
4. `Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`
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

- Do not reintroduce broad/inherited LethalMin reflection/Harmony scanning.
- Do not use continuous Update-driven global EnemyAI scans for this death cleanup.
- Do not restore direct low-level RemoveCurrentTask as the Hawk-death finalizer.
- Use runtime-confirmed `FinishTask()`; do not guess `TaskFinished()` again.
- Do not silently upgrade BCMER 1.71.0 to 2.0.0.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not let `CodeRebirthLib` return.
- Unknown Enemy PowerLevels must never be guessed.
- Profiles with the local compatibility DLL require Gale "Import all files".

## Deferred maintenance

Do not clean during the open S1.42P runtime gate:
- older "current" wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in untouched historical parts of `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural optimization:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
