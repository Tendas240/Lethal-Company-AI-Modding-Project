# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Latest valid runtime evidence:
**S1.42O — no cleanup executed because TaskFinished() does not exist**

Current built candidate:
**S1.42P - Baboon Hawk Exact FinishTask Recovery**

Profile:
`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Compatibility plugin:
**v1.3.11**

Read:
- `Current/54_S1.42O_NO_CLEANUP_FINISHTASK_ANALYSIS.md`
- `Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`
- `Current/Projektstatus_S1.42P.json`

## S1.42O result

Evidence:
`RuntimeEvidence/S1.42O/20260903T171220Z/`

Log SHA-256:
`1a1251f19a1d82e90b72e82ac8e4babd523c32e695fe3d7923d4590debb0be71`

User observed 8 Pikmin disappearing after Hawk death.

S1.42O did not run cleanup:
- attempted `PikminAI.TaskFinished()`;
- runtime proves that method does not exist;
- no RemoveCurrentTask fallback was used.

Runtime reflection exposed the actual exact method:
`PikminAI.FinishTask():Void`

Eight Hawk attackers continued stale hit output after death and beyond corpse creation.

## S1.42P scope

Keep the validated one-shot 4.0 m SpawnedEnemies resolver and the passing corpse guard.

Use exact declared:
`PikminAI.FinishTask()`

No direct RemoveCurrentTask fallback.
No continuous global scan.
No broad/inherited LethalMin Harmony scan.

## Exact next action

Import with:
**Gale -> Advanced options -> Import all files**

Test S1.42P:
1. note following Pikmin count;
2. attack/kill Hawk with several Pikmin;
3. verify attackers stop attacking dead Hawk;
4. verify all remain visible/responsive;
5. whistle/regain and verify follow/reuse;
6. compare count;
7. verify corpse/Onion behavior;
8. verify living-Hawk corpse ignore;
9. verify Hawk -> Pikmin ignore;
10. verify no leader-null loop;
11. upload full log to `RuntimeInbox/Current/`.

## Temporary state

EnemyIsolation:
enabled.

BCMER 1.71.0:
disabled.

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_BUILD_AWAITING_RUNTIME`

## Anti-regression

- no S1.42D broad/inherited LethalMin Harmony scan;
- no continuous global EnemyAI scan;
- do not restore direct RemoveCurrentTask death cleanup;
- do not guess alternate method names now that FinishTask() is runtime-confirmed;
- no silent BCMER 2.0.0 upgrade;
- preserve S1.42C enemy restore baseline.
