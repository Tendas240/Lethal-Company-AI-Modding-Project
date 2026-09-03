# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical current pointers

Machine-readable status:
`Current/Projektstatus_S1.42O.json`

Latest runtime analysis:
`Current/52_S1.42N_NATIVE_TASK_FINALIZATION_ANALYSIS.md`

Current candidate build:
`Current/53_S1.42O_BABOON_HAWK_NATIVE_TASK_FINALIZATION_BUILD.md`

## State separation

### Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

### Latest valid runtime evidence

**S1.42N - TARGET RESOLVER PASS / STATE FINALIZATION FAIL**

Evidence:
`RuntimeEvidence/S1.42N/20260903T165818Z/`

Log SHA-256:
`8ed6a79230e28535a01a4cb86a8971c358a5c9f57a53722e18ff4342474f51cf`

Confirmed:
- SpawnedEnemies death resolver found 6/6 real Hawk attackers;
- all six had pre-death attack-hit activity;
- one-shot 4.0 m target selection is therefore validated for this run;
- corpse still appeared and was carried to the Onion;
- `Leader is null when following` = 0.

Failure:
- direct `PikminAI.RemoveCurrentTask()` left five resolver-touched Pikmin in Work state with no task;
- log contains 2155 `Work state with no task assigned!` warnings;
- those five match the user's observation of ~4–5 Pikmin running in place, non-following and unusable;
- `Yellow Pikmin_G5l3h` continued stale hit-loop output for more than a minute after Hawk death.

Natural healthy control:
`Yellow Pikmin_PerDu` executed LethalMin's native:
`Task finished -> Setting to idle -> Removing current task`
and later took a valid corpse CarryItem task.

### Current built candidate awaiting runtime

**S1.42O - Baboon Hawk Native Task Finalization**

Profile:
`Profiles/LC V1 S1.42O Baboon Hawk Native Task Finalization.r2z`

SHA-256:
`04d7e0df7f7a3b51d75832e9052c3e217ec07f91526c767323e1b5b0a3078d4d`

Compatibility plugin:
**v1.3.10**

Build:
- GitHub Actions #46: PASS;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only: compatibility DLL + `export.r2x`;
- no added members.

## S1.42O implementation

Keep:
- exact `BaboonBirdAI.KillEnemy(bool)`;
- one-shot `RoundManager.Instance.SpawnedEnemies` registry;
- exact/assignable `LethalMin.PikminAI`;
- 4.0 m death-release zone;
- passing Dead Baboon Hawk corpse guard.

Replace:
- direct low-level `RemoveCurrentTask()` cleanup.

Use:
- exact declared zero-argument `LethalMin.PikminAI.TaskFinished()`;
- void / exact declaring type / zero-parameter / method-body validation;
- no low-level RemoveCurrentTask fallback if unavailable.

## Active runtime gate

S1.42O must prove:
- Hawk attackers stop working against the dead target;
- affected Pikmin do not enter the repeated no-task Work state;
- affected Pikmin remain responsive/recoverable/followable;
- active/following Pikmin count can be restored after the fight;
- corpse behavior remains intact;
- living Hawks still ignore corpse;
- Hawk -> Pikmin ignore remains intact;
- no leader-null loop.

## Temporary test state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER before S1.42O passes.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42O`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42O_BUILD_AWAITING_RUNTIME`

## Exact next step

Import:
**Gale -> Advanced options -> Import all files**

Test S1.42O:
1. note approximate following Pikmin count before the Hawk attack;
2. throw several Pikmin onto a living Baboon Hawk;
3. let them kill it;
4. verify attackers no longer run in place / freeze permanently;
5. whistle/regain them and verify they follow and can be reused;
6. compare following count after recovery with before;
7. verify no repeated `Work state with no task assigned!` loop;
8. verify no stale attack-hit loop against dead Hawk;
9. verify corpse still reaches Onion;
10. verify living Hawks ignore corpse;
11. verify Hawk -> Pikmin ignore;
12. verify no leader-null loop;
13. commit the complete fresh log to `RuntimeInbox/Current/`.

## Deferred maintenance

Do not perform general cleanup during this gate.

Known non-functional drift:
- older current-wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in untouched historical sections of `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
