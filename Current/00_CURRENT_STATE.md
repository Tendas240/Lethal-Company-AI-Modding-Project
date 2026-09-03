# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical current pointers

Final handover:
`Current/64_HANDOVER_S1.42R_TO_NEXT_FINAL.md`

Repository handover audit:
`Current/65_REPOSITORY_HANDOVER_AUDIT_S1.42R.md`

Machine-readable status:
`Current/Projektstatus_S1.42R.json`

Exact upstream decompile:
`Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`

S1.42Q root-cause analysis:
`Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`

S1.42R build:
`Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`

S1.42R build plan:
`BuildSpecs/S1.42R_PLAN.md`

Verification:
`Current/VERIFIKATION_S1.42R.txt`

Hashes:
`Current/SHA256SUMS_S1.42R.txt`

Current mod list:
`Current/Aktive_Modliste_S1.42R.txt`

## Last fully accepted gameplay baseline

**S1.41 - BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

## Latest runtime evidence

**S1.42Q - FAIL**

Evidence:
`RuntimeEvidence/S1.42Q/20260903T195158Z/`

Log SHA-256:
`e8949f87c0df2e3f5a8e7b985bf698aab9de68bba08ae45e3fe5b89e89f27aa5`

The user's observation is confirmed exactly.

First Baboon Hawk:
- three Yellow Pikmin attacked it:
  - `Yellow Pikmin_ruCpzY`
  - `Yellow Pikmin_PerDu`
  - `Yellow Pikmin_hcRGph`
- `hcRGph` reached native `Task finished`;
- `ruCpzY` and `PerDu` never reached `Task finished`;
- those two remained on the stale attack task and kept hitting the already-dead first Hawk;
- these are the two effectively "missing" Pikmin.

Second Hawk:
- the correctly transitioned attacker completed cleanly;
- the two stale Pikmin from the first Hawk were still stuck on the first dead target.

## Exact upstream root cause

Exact package:
`NotezyTeam-LethalMinNightly 1.1.108`

Exact analyzed DLL SHA-256:
`9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df`

Decompiled:
`LethalMin.Pikmin.AttackEnemyTask.IntervaledUpdate()`

The upstream method does:

1. while latched and attacking, keep/restart attack;
2. then:
   `if (CurrentIntention != Attack || IsPikminOnEnemy) return;`
3. only after that early return:
   - null-target handling
   - pathing
   - `enemy.enemyScript.isEnemyDead`
   - `FinishTaskServerRpc()`

Therefore **a still-latched co-attacker can never reach LethalMin's own dead-target completion branch**.

This explains every prior runtime symptom without a radius or Hawk-specific theory.

## Current built candidate

**S1.42R - LethalMin Latched Dead Target Completion**

Profile:
`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Git blob SHA:
`61e290182a0f056a20d81f31d340b27eb18f4be4`

Compatibility plugin:
**v1.3.13**

Embedded DLL SHA-256:
`0d39a8895a1324457c2ac135fa2ae129e58ba8155ce6bde1cdb59d340be420ff`

Build:
- GitHub Actions #54: SUCCESS
- generated commit `80fc7bc37476612320925083f062bda2b841cf40`
- idle guard #55: SUCCESS
- 331 archive members
- 330 readable snapshot files
- no added members

Exact S1.42Q -> S1.42R profile delta:
1. compatibility DLL
2. `export.r2x`

**No config changes. No mod changes.**

## S1.42R exact patch

Patch only:

`LethalMin.Pikmin.AttackEnemyTask.IntervaledUpdate()`

Before the broken upstream latched early-return, the prefix checks the task itself:

- `IsPikminOnEnemy == true`
- this exact task's own `enemy` exists
- `enemy.enemyScript.isEnemyDead == true`

Then it invokes native:

`PikminAI.FinishTaskServerRpc()`

and skips the broken upstream interval for that tick.

It does **not**:
- hook enemy death;
- scan Pikmin;
- scan enemies;
- use distance/radius;
- match names;
- call `RemoveCurrentTask`;
- manually unlatch;
- restore leader/follow state;
- implement corpse carrying.

The rest of the lifecycle remains native LethalMin.

## Temporary state

EnemyIsolation:
**enabled**

BCMER exact 1.71.0:
**disabled**

Thumper Bite Limit:
**3**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`

## Exact next step

Do not build S1.42S first.

Import S1.42R through:

**Gale -> Advanced options -> Import all files**

Then use **multiple Pikmin on the same Baboon Hawk** and kill it.

Expected:
- one `[LethalMinLatchedDeathGuard] Requested native FinishTaskServerRpc` per stale latched co-attacker;
- native `Task finished` immediately afterward;
- no continued hits on the dead Hawk;
- exact follower count recoverable.

Repeat on a second Hawk.

Then commit the complete fresh `LogOutput.log` to:
`RuntimeInbox/Current/`

Do not restore normal enemies or BCMER before S1.42R passes.


## Handover readiness

Repository audit:
**PASS — ready for a new chat; S1.42R runtime gate remains open.**

`RuntimeInbox/Current/` contains only `.gitkeep`.

`RuntimeEvidence/S1.42R/` does not exist yet, which is correct because S1.42R has not been runtime-tested.

No files were deleted during handover.
No local clone/build/PowerShell work is required.
