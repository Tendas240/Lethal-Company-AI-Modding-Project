# 04 - Open Issues and Next Tests

## Immediate active gate — S1.42O native Pikmin task finalization

Analysis:
`Current/52_S1.42N_NATIVE_TASK_FINALIZATION_ANALYSIS.md`

Build:
`Current/53_S1.42O_BABOON_HAWK_NATIVE_TASK_FINALIZATION_BUILD.md`

Profile:
`Profiles/LC V1 S1.42O Baboon Hawk Native Task Finalization.r2z`

SHA-256:
`04d7e0df7f7a3b51d75832e9052c3e217ec07f91526c767323e1b5b0a3078d4d`

Compatibility plugin:
**v1.3.10**

## Why S1.42O exists

S1.42N successfully found 6/6 actual Hawk attackers, but direct `RemoveCurrentTask()` caused a lifecycle break.

Five selected Pikmin repeatedly logged:
`Work state with no task assigned!`

Total:
**2155 warnings**

User observed approximately 4–5 Pikmin running in place, no longer following, non-responsive and effectively unusable.

The healthy control Pikmin ran LethalMin's own:
`Task finished -> Setting to idle -> Removing current task`

Therefore S1.42O invokes exact `PikminAI.TaskFinished()` instead of direct `RemoveCurrentTask()`.

## Exact S1.42O test

Use:
**Gale -> Advanced options -> Import all files**

1. record approximate following Pikmin count;
2. throw several Pikmin onto a living Baboon Hawk;
3. let them kill it;
4. immediately inspect the attackers;
5. they must not remain running in place or become permanently unresponsive;
6. whistle/regain them and verify they can follow and be reused;
7. compare following count with pre-fight count;
8. wait for corpse;
9. verify corpse still travels to Onion;
10. verify living Hawk does not pick up corpse;
11. verify Hawk -> Pikmin ignore;
12. verify no leader-null loop;
13. commit full fresh log to `RuntimeInbox/Current/`.

Expected log:
- exact `PikminAI.TaskFinished()` resolution marker;
- one or more `Native TaskFinished finalized ...` markers;
- non-zero aggregate native-finalized count;
- no sustained `Work state with no task assigned!` loop for finalized attackers;
- no sustained dead-Hawk hit loop.

## Temporary state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER before this gate passes.

## After PASS

Then:
1. disable EnemyIsolation;
2. restore normal enemy configuration exactly from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted asymmetric interaction/corpse rules;
5. runtime-test restored normal gameplay;
6. monitor historical BCMER Door System ERROR / ship-door behavior;
7. only after that perform deferred repository cleanup/optimization.

## Lower-priority pending

- CodeRebirth Functional Microwaves somewhat rarer;
- equal effective interior selection probability where safe;
- CullFactory exact IDs `junkrooms` and `shatteredrooms`;
- MelanieMausoleum fog reduction;
- Shatteredrooms Experimentation/Embrion safety block stays until understood;
- monitor Mineshaft elevator/Pikmin crowding.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42O`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42O_BUILD_AWAITING_RUNTIME`
