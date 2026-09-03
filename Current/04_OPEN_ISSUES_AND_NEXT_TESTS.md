# 04 - Open Issues and Next Tests

## Immediate active issue — S1.42P failed 20 -> 18 recovery

Newest analysis:
`Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`

Tested profile:
`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Runtime evidence:
`RuntimeEvidence/S1.42P/20260903T181706Z/`

Log SHA-256:
`d656095fb874a415a1bd2377c0411339d3d6eb002dce4ec3f6216e879294127f`

## Confirmed failure

User observation:
**20 following Pikmin before the fight, 18 recovered afterward.**

Log reconstruction:
**exactly 20 -> 18 confirmed.**

Missing:
- `Yellow Pikmin_hcRGph`
- `Yellow Pikmin_ruCpzY`

### Failure mode 1 — selector miss

Four Pikmin were actively hitting the Hawk before death, but the 4.0 m cleanup selected only three.

Missed attacker:
`Yellow Pikmin_ruCpzY`

It continued hitting the dead Hawk for 168 post-death entries, ending about 84.565 seconds after death.

A larger arbitrary radius is not an acceptable fix; attacker identity must be direct.

### Failure mode 2 — dead-target reacquisition

Native `FinishTask()` worked on:
- `hcRGph`
- `apYy5`
- `khCd`

All three then rediscovered the already-dead `BaboonHawkEnemy(Clone)` and assigned a new `AttackEnemy` task.

`apYy5` and `khCd` eventually recovered through later behavior.
`hcRGph` did not return to the leader.

## Passing S1.42P subchecks

- exact `PikminAI.FinishTask()` resolver: PASS
- native FinishTask invocation: PASS
- `Work state with no task assigned!`: 0
- `Leader is null when following`: 0
- Dead Baboon Hawk body creation/carry: PASS
- corpse reaches Onion: PASS
- living Baboon Hawk ignores corpse: PASS
- Thumper/Pikmin protection remains active.

## Next build direction — S1.42Q

Build from S1.42P only after implementation is exact enough to avoid guessing.

Required changes:
1. retain `PikminAI.FinishTask()`;
2. determine actual Pikmin attackers by dying-Hawk target identity rather than distance;
3. prevent dead `BaboonHawkEnemy` objects from being valid future Pikmin AttackEnemy targets.

Preserve:
- Pikmin -> living Hawk attack/latch/kill;
- living Hawk -> Pikmin ignore/protection;
- corpse carry to Onion;
- living Hawks ignore corpse.

Do not:
- simply widen the 4 m radius;
- use direct `RemoveCurrentTask()`;
- add continuous scene scanning;
- restore normal enemy state;
- re-enable BCMER yet.

If exact target-selection internals are not established, prefer a narrow diagnostic descendant that logs exact runtime task/target members over guessed reflection.

## Temporary state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_RUNTIME_FAIL_AWAITING_SUCCESSOR_DESIGN`

## After a future PASS

Only after the Baboon-Hawk death/recovery gate is actually clean:
1. disable EnemyIsolation;
2. restore exact normal enemy configuration from S1.42C baseline;
3. re-enable exact BCMER 1.71.0;
4. runtime-test normal gameplay;
5. then consider deferred repository cleanup/migration.
