# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Latest valid runtime evidence:
**S1.42N — target resolver pass / native state-finalization bug exposed**

Current built candidate:
**S1.42O - Baboon Hawk Native Task Finalization**

Profile:
`Profiles/LC V1 S1.42O Baboon Hawk Native Task Finalization.r2z`

SHA-256:
`04d7e0df7f7a3b51d75832e9052c3e217ec07f91526c767323e1b5b0a3078d4d`

Compatibility plugin:
**v1.3.10**

Read:
- `Current/52_S1.42N_NATIVE_TASK_FINALIZATION_ANALYSIS.md`
- `Current/53_S1.42O_BABOON_HAWK_NATIVE_TASK_FINALIZATION_BUILD.md`
- `Current/Projektstatus_S1.42O.json`

## S1.42N runtime result

Evidence:
`RuntimeEvidence/S1.42N/20260903T165818Z/`

Log SHA-256:
`8ed6a79230e28535a01a4cb86a8971c358a5c9f57a53722e18ff4342474f51cf`

The S1.42N target resolver succeeded:
- 6/6 selected Pikmin were real Hawk attackers.

But direct `RemoveCurrentTask()` was the wrong lifecycle API:
- five selected Pikmin entered `Work state with no task assigned!`;
- total warning count = 2155;
- those five became non-following/unusable, matching user observation;
- one retained a stale hit loop.

Healthy control `PerDu` naturally ran:
`Task finished -> Setting to idle -> Removing current task`
and remained capable of taking a later task.

## Binding permanent behavior

Living Hawk -> Pikmin:
blocked.

Pikmin -> living Hawk:
normal attack/latch/kill allowed.

On Hawk death:
- attackers must finish their attack task through LethalMin's native completion path;
- they must remain recoverable/followable/reusable;
- corpse remains enabled and Onion-carryable;
- living Hawks cannot pick up corpse.

## S1.42O scope

Only lifecycle completion changes.

Retain:
- 4.0 m one-shot SpawnedEnemies resolver;
- exact PikminAI filtering;
- corpse guard.

Replace direct `RemoveCurrentTask()` with exact declared:
`PikminAI.TaskFinished()`.

No low-level fallback.
No continuous scan.
No broad/inherited LethalMin Harmony scan.

## Exact next action

Import S1.42O with:
**Gale -> Advanced options -> Import all files**

Focused test:
1. record following count;
2. attack/kill a Hawk with Pikmin;
3. verify attackers are responsive after death;
4. whistle/regain and verify they follow;
5. compare count;
6. verify no no-task Work loop;
7. verify no stale hit loop;
8. verify corpse/Onion behavior;
9. verify living-Hawk corpse ignore;
10. verify Hawk -> Pikmin ignore;
11. verify no leader-null loop;
12. upload full log to `RuntimeInbox/Current/`.

## Temporary state

EnemyIsolation:
enabled.

BCMER 1.71.0:
disabled.

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42O`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42O_BUILD_AWAITING_RUNTIME`

## Critical anti-regression

- no S1.42D broad/inherited LethalMin Harmony scan;
- no continuous global EnemyAI scan;
- do not restore direct RemoveCurrentTask death cleanup;
- no silent BCMER 2.0.0 upgrade;
- preserve S1.42C enemy restore baseline;
- CodeRebirthLib must not return;
- unknown Enemy PowerLevels must not be guessed.
