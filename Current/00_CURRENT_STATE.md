# 00 - Current State

**Date:** 2026-09-03  
**Game:** Lethal Company V81

## Current candidate

**S1.42R - LethalMin Latched Dead Target Completion**

Profile:
`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Compatibility plugin:
**v1.3.13**

DLL SHA-256:
`0d39a8895a1324457c2ac135fa2ae129e58ba8155ce6bde1cdb59d340be420ff`

Status:
**built and repository-verified; awaiting runtime**

Build:
- GitHub Actions #54: SUCCESS
- generated commit `80fc7bc37476612320925083f062bda2b841cf40`
- 331 archive members
- 330 readable snapshot files
- Q -> R changed only compatibility DLL and export profile name
- no config delta

## Latest runtime evidence

**S1.42Q - FAIL with exact root cause identified**

Evidence:
`RuntimeEvidence/S1.42Q/20260903T195158Z/`

Log SHA-256:
`e8949f87c0df2e3f5a8e7b985bf698aab9de68bba08ae45e3fe5b89e89f27aa5`

Exact failed co-attackers:
- Yellow Pikmin_ruCpzY
- Yellow Pikmin_PerDu

Successful control:
- Yellow Pikmin_hcRGph

## Exact root cause

Exact LethalMinNightly version:
**1.1.108**

Decompile:
`Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`

Analysis:
`Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`

`AttackEnemyTask.IntervaledUpdate()` returns while `IsPikminOnEnemy == true` before it reaches its own dead-target check.

Therefore a still-latched non-killing co-attacker never calls the existing native `FinishTaskServerRpc()` when its target dies.

## S1.42R fix

Patch exact:
`LethalMin.Pikmin.AttackEnemyTask.IntervaledUpdate()`

Only when:
- this exact task is still latched;
- this exact task's own target exists;
- that target's `enemyScript.isEnemyDead == true`;

call:
`PikminAI.FinishTaskServerRpc()`

Then native LethalMin performs:
TaskEnd -> SetToIdle -> reset/unlatch -> remove task.

No death hook, scan, radius, target guessing, direct RemoveCurrentTask, manual unlatch, or leader restoration.

## Temporary state

EnemyIsolation:
**enabled**

BCMER 1.71.0:
**disabled**

Thumper Bite Limit:
**3**

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`

## Exact next step

Import S1.42R using:

**Gale -> Advanced options -> Import all files**

Use at least three Pikmin on the same Baboon Hawk.

After death verify:
- all co-attackers stop;
- `[LethalMinLatchedDeathGuard]` appears for latched co-attackers;
- each is followed by native `Task finished`;
- exact full follower count is recoverable.

Repeat once, verify corpse carry/Onion and Hawk -> Pikmin blocking, then commit the complete fresh `LogOutput.log` to `RuntimeInbox/Current/`.

Do not restore normal enemies or BCMER before S1.42R passes.
