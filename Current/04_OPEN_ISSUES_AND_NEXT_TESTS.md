# 04 - Open Issues and Next Tests

## Immediate active gate — S1.42P exact FinishTask recovery

Analysis:
`Current/54_S1.42O_NO_CLEANUP_FINISHTASK_ANALYSIS.md`

Build:
`Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`

Profile:
`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Compatibility plugin:
**v1.3.11**

## S1.42O failure

Evidence:
`RuntimeEvidence/S1.42O/20260903T171220Z/`

Log SHA-256:
`1a1251f19a1d82e90b72e82ac8e4babd523c32e695fe3d7923d4590debb0be71`

User observed:
**8 Pikmin disappeared after Hawk death.**

Reason:
S1.42O attempted exact `PikminAI.TaskFinished()`, but the runtime type has no such method. Cleanup was therefore inactive.

The runtime candidate list reveals:
`PikminAI.FinishTask():Void`

Eight attackers continued hitting the dead Hawk beyond the SellBodies body-spawn point.

## S1.42P change

Use exact runtime-confirmed:
`PikminAI.FinishTask()`

Keep:
- one-shot SpawnedEnemies resolver;
- 4.0 m selection;
- corpse guard;
- EnemyIsolation;
- BCMER disabled.

No RemoveCurrentTask fallback.

## Exact S1.42P test

Use:
**Gale -> Advanced options -> Import all files**

1. record following count;
2. throw several Pikmin onto living Hawk;
3. let them kill it;
4. attackers must stop dead-target hit activity;
5. affected Pikmin must remain visible and responsive;
6. whistle/regain them;
7. verify they follow and can be reused;
8. compare following count;
9. verify corpse still reaches Onion;
10. verify living Hawks ignore corpse;
11. verify Hawk -> Pikmin ignore;
12. verify no leader-null loop;
13. commit complete fresh log to `RuntimeInbox/Current/`.

Expected log:
- `Resolved exact declared LethalMin.PikminAI.FinishTask()`;
- one or more `Native FinishTask finalized ...`;
- non-zero `native-finished X/X`;
- no sustained no-task Work loop;
- no sustained hit loop after Hawk death.

## Temporary state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## After PASS

Then restore exact normal enemy config and exact BCMER 1.71.0, followed by a normal-state runtime test.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_BUILD_AWAITING_RUNTIME`

## Handover continuity

Primary continuation document:
`Current/56_HANDOVER_S1.42P_TO_NEXT_FINAL.md`

Final repository audit:
`Current/57_REPOSITORY_HANDOVER_AUDIT_S1.42P.md`

Do not treat repository cleanup, BCMER restore, or normal enemy restore as the next step. The next step remains the unchanged S1.42P focused runtime test.
