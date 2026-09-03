# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Latest valid runtime evidence:
**S1.42P — PARTIAL / FAIL, exact 20 -> 18 Pikmin recovery failure**

Current tested candidate:
**S1.42P - Baboon Hawk Exact FinishTask Recovery**

Profile:
`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Compatibility plugin:
**v1.3.11**

Read first:
- `Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`
- `Current/Projektstatus_S1.42P.json`
- `Current/00_CURRENT_STATE.md`
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
- `Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`
- `Current/54_S1.42O_NO_CLEANUP_FINISHTASK_ANALYSIS.md`
- `Current/56_HANDOVER_S1.42P_TO_NEXT_FINAL.md` and `57_REPOSITORY_HANDOVER_AUDIT_S1.42P.md` only as pre-test handover history.

## S1.42P runtime result

Evidence:
`RuntimeEvidence/S1.42P/20260903T181706Z/`

Log SHA-256:
`d656095fb874a415a1bd2377c0411339d3d6eb002dce4ec3f6216e879294127f`

The user began with 20 following Yellow Pikmin and recovered only 18.

The log independently confirms exactly 20 leader-assigned Pikmin before the fight and exactly 18 recovered before teardown.

The two missing are:
- `Yellow Pikmin_hcRGph`
- `Yellow Pikmin_ruCpzY`

## What S1.42P proved

`PikminAI.FinishTask()` is correct:
- exact method resolves;
- three selected Pikmin receive native FinishTask;
- no low-level RemoveCurrentTask fallback is needed;
- no no-task Work loop is produced.

But S1.42P still fails because:
- `Yellow Pikmin_ruCpzY`, a real Hawk attacker, was missed by the 4.0 m distance selector;
- it continued hitting the dead Hawk for ~84.565 s;
- all three FinishTask-selected Pikmin rediscovered the already-dead Hawk almost immediately;
- `hcRGph` never returned to the leader.

Corpse side remains PASS:
- body exists;
- Pikmin carry it;
- it reaches Onion;
- living Hawks ignore it.

## Exact next action

Next technical stage:
**S1.42Q successor design/build**

Required:
1. keep exact native `PikminAI.FinishTask()`;
2. select actual dying-Hawk attackers by target identity, not fixed radius;
3. block already-dead Baboon Hawks from future Pikmin AttackEnemy acquisition;
4. preserve asymmetric living-Hawk/Pikmin behavior and corpse behavior.

Do not merely increase the radius.
Do not restore direct `RemoveCurrentTask()`.
Do not restore normal enemies or BCMER yet.

## Temporary state

EnemyIsolation:
enabled.

BCMER 1.71.0:
disabled.

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_RUNTIME_FAIL_AWAITING_SUCCESSOR_DESIGN`

## Anti-regression

- no broad/inherited LethalMin Harmony scan;
- no continuous global EnemyAI scan;
- no direct RemoveCurrentTask Hawk-death finalizer;
- no guessed TaskFinished() method;
- no proximity-only selector as the complete attacker identity solution;
- no silent BCMER 2.0.0 upgrade;
- preserve S1.42C enemy restore baseline.
