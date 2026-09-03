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

Build **S1.42Q as a minimal LethalMin-native rollback**.

Plan:
`Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`

Do not implement the previously proposed custom dead-Hawk target-identity/reacquisition layer first.

Instead:
1. remove `BaboonHawkDeathCleanup` completely;
2. return enemy-death task completion to LethalMin;
3. return corpse carrying/Onion routing entirely to LethalMin;
4. remove reflection-heavy post-grab state repair;
5. keep only the smallest proven Enemy -> Pikmin blockers/config switches.

The intended asymmetric rule is:
- Pikmin -> enemies: native LethalMin;
- enemies -> Pikmin: blocked;
- Pikmin -> dead enemy bodies: native LethalMin.

EnemyIsolation remains enabled.
BCMER 1.71.0 remains disabled.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_RUNTIME_FAIL_AWAITING_MINIMAL_ROLLBACK_BUILD`

## Anti-regression

- no broad/inherited LethalMin Harmony scan;
- no continuous global EnemyAI scan;
- no project-local FinishTask/RemoveCurrentTask enemy-death lifecycle;
- no custom Pikmin corpse carry/Onion routing;
- no reflection-heavy after-the-fact leader repair if the offending Enemy -> Pikmin interaction can be blocked before mutation;
- prefer native LethalMin config over Harmony when the config is proven effective;
- no silent BCMER 2.0.0 upgrade.
