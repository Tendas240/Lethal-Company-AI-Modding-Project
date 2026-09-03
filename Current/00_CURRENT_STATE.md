# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical current pointers

Machine-readable status:
`Current/Projektstatus_S1.42P.json`

Primary final handover:
`Current/56_HANDOVER_S1.42P_TO_NEXT_FINAL.md`

Final repository audit:
`Current/57_REPOSITORY_HANDOVER_AUDIT_S1.42P.md`

Verification:
`Current/VERIFIKATION_S1.42P.txt`

Current mod list:
`Current/Aktive_Modliste_S1.42P.txt`

Latest runtime analysis:
`Current/54_S1.42O_NO_CLEANUP_FINISHTASK_ANALYSIS.md`

Current candidate build:
`Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`

## State separation

### Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

### Latest valid runtime evidence

**S1.42O - FAIL / no Hawk death cleanup executed**

Evidence:
`RuntimeEvidence/S1.42O/20260903T171220Z/`

Log SHA-256:
`1a1251f19a1d82e90b72e82ac8e4babd523c32e695fe3d7923d4590debb0be71`

User-observed:
**8 Pikmin disappeared after the Baboon Hawk died.**

Critical startup evidence:
- `PikminAI.TaskFinished()` does not exist in loaded LethalMin;
- S1.42O therefore performed no death cleanup;
- no low-level RemoveCurrentTask fallback ran.

Runtime reflection exposed exact declared:
`PikminAI.FinishTask():Void`

After Hawk death, the eight attackers continued `Hitting enemy with: 0.03` beyond the SellBodies corpse-spawn point.

## Current built candidate awaiting runtime

**S1.42P - Baboon Hawk Exact FinishTask Recovery**

Profile:
`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Compatibility plugin:
**v1.3.11**

Build:
- GitHub Actions #48: PASS;
- 331 archive members;
- 330 readable snapshot files;
- changed existing members only: compatibility DLL + `export.r2x`;
- no added members.

## S1.42P implementation

Retain:
- exact `BaboonBirdAI.KillEnemy(bool)`;
- one-shot `RoundManager.Instance.SpawnedEnemies`;
- exact/assignable `LethalMin.PikminAI`;
- 4.0 m death zone;
- passing Dead Baboon Hawk corpse guard.

Use runtime-confirmed exact:
`LethalMin.PikminAI.FinishTask()`

Validation:
- exact declaring type;
- zero parameters;
- void return;
- implementation body.

No direct `RemoveCurrentTask()` fallback.

## Active runtime gate

S1.42P must prove:
- exact FinishTask resolves at startup;
- real Hawk attackers are selected;
- FinishTask runs at Hawk death;
- dead-Hawk attack-hit loop stops promptly;
- no sustained Work-state-with-no-task loop;
- attackers remain visible, responsive and recoverable;
- following count can be restored;
- corpse remains Onion-carryable;
- living Hawks ignore corpse;
- Hawk -> Pikmin ignore remains intact;
- no leader-null loop.

## Temporary test state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER before S1.42P passes.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_BUILD_AWAITING_RUNTIME`

## Exact next step

Import:
**Gale -> Advanced options -> Import all files**

Then:
1. note approximate following Pikmin count;
2. throw several Pikmin onto a living Baboon Hawk;
3. let them kill it;
4. confirm attackers stop hitting the dead Hawk;
5. verify they remain visible/responsive;
6. whistle/regain and verify follow/reuse;
7. compare count before/after;
8. verify corpse still appears and reaches Onion;
9. verify living Hawks ignore corpse;
10. verify Hawk -> Pikmin ignore;
11. verify no leader-null loop;
12. commit full fresh log to `RuntimeInbox/Current/`.

## Deferred maintenance

Do not perform general cleanup during this runtime gate.

## Handover integrity

- No repository files were deleted during the final S1.42P handover.
- Runtime evidence S1.42L through S1.42O remains preserved.
- S1.42P has no runtime evidence yet; this is expected.
- The next chat must not build a successor before the focused S1.42P test unless S1.42P cannot start.
