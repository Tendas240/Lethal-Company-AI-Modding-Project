# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical current pointers

Machine-readable status:
`Current/Projektstatus_S1.42P.json`

Newest runtime analysis:
`Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`

S1.42P build definition:
`Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`

Pre-test handover / audit, now historical:
- `Current/56_HANDOVER_S1.42P_TO_NEXT_FINAL.md`
- `Current/57_REPOSITORY_HANDOVER_AUDIT_S1.42P.md`

Verification:
`Current/VERIFIKATION_S1.42P.txt`

Current mod list:
`Current/Aktive_Modliste_S1.42P.txt`

## State separation

### Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

### Latest valid runtime evidence

**S1.42P - PARTIAL / FAIL**

Evidence:
`RuntimeEvidence/S1.42P/20260903T181706Z/`

Log:
`RuntimeEvidence/S1.42P/20260903T181706Z/raw/LogOutput.log`

Log SHA-256:
`d656095fb874a415a1bd2377c0411339d3d6eb002dce4ec3f6216e879294127f`

User observed a following-count drop from **20 to 18** after the Baboon Hawk fight.

The log confirms that exact 20 -> 18 transition.

Missing from the recovered leader set:
- `Yellow Pikmin_hcRGph`
- `Yellow Pikmin_ruCpzY`

### S1.42P result

PASS:
- exact declared `LethalMin.PikminAI.FinishTask()` resolves at startup;
- native FinishTask executes;
- three Pikmin are finalized at Hawk death;
- no `Work state with no task assigned!` loop;
- no `Leader is null when following` loop;
- Dead Baboon Hawk corpse remains Pikmin-carryable and reaches Onion;
- living Baboon Hawks ignore the corpse.

FAIL:
- 4.0 m proximity selection missed real attacker `Yellow Pikmin_ruCpzY`;
- `ruCpzY` continued hitting the dead Hawk for about 84.565 seconds after death;
- FinishTask-finalized Pikmin can immediately reacquire the already-dead `BaboonHawkEnemy(Clone)`;
- `hcRGph` reacquired the dead Hawk and never returned to the leader before teardown;
- final recovered following set was 18/20.

Therefore S1.42P is **not accepted** as the Baboon-Hawk death fix.

## Root cause now established

S1.42P proved that `FinishTask()` is the correct high-level native task finalizer.

The remaining defects are:

1. attacker identity cannot be inferred reliably from a fixed 4.0 m distance;
2. dead Baboon Hawks remain eligible for LethalMin attack-target discovery after death.

Do not merely widen the radius.
Do not return to direct `RemoveCurrentTask()`.

## Temporary test state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER yet.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

This remains S1.42P until a successor is actually built.

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_RUNTIME_FAIL_AWAITING_SUCCESSOR_DESIGN`

## Exact next step

**S1.42Q is now a minimal LethalMin-native rollback, not another Hawk-death algorithm.**

Canonical plan:
`Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`

Target architecture:
- Pikmin -> enemy attack/latch/kill: native LethalMin only;
- enemy death task completion: native LethalMin only;
- Pikmin -> enemy-body carry/Onion: native LethalMin only;
- project-local code: only proven minimal Enemy -> Pikmin prevention and unrelated compatibility gaps.

Remove from the next build:
- `BaboonHawkDeathCleanup`;
- project-local `FinishTask()` Hawk death calls;
- 4.0 m Hawk-death scan;
- reflection-heavy post-grab leader/follow state repair.

Prefer native LethalMin config switches where they already work.

The current S1.42P config differs from accepted S1.41 LethalMin config only at:
`Thumper Bite Limit = 0` vs accepted `3`.
Restore the accepted value unless fresh evidence proves otherwise.

Keep:
- EnemyIsolation enabled;
- BCMER 1.71.0 disabled;
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42P` until S1.42Q is actually built.

## Deferred maintenance

Do not perform general repository cleanup while this enemy-regression chain is still open.

Known non-functional drift in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Plugin.cs` remains deferred.
