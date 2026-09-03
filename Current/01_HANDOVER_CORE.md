# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Latest runtime evidence:
**S1.42Q — FAIL, exact LethalMin latched-co-attacker root cause identified**

Current built candidate:
**S1.42R — LethalMin Latched Dead Target Completion**

Profile:
`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Compatibility plugin:
**v1.3.13**

## Read first

1. `Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`
2. `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`
3. `Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`
4. `Current/Projektstatus_S1.42R.json`
5. `Current/VERIFIKATION_S1.42R.txt`
6. `BuildSpecs/S1.42R_PLAN.md`

## Exact bug

LethalMinNightly 1.1.108 `AttackEnemyTask.IntervaledUpdate()` returns for a currently latched Pikmin before checking whether its own target is dead.

S1.42Q runtime mapped this to the exact two lost Pikmin.

## S1.42R

Adds only the missing dead-target completion to the exact task:

latched + own target dead -> native `FinishTaskServerRpc()`.

No death hook.
No scan.
No radius.
No guessed attacker identity.
No custom state restoration.

## Next action

Import S1.42R using Gale "Advanced options -> Import all files" and perform the focused multi-Pikmin Baboon Hawk test.

Expected:
`[LethalMinLatchedDeathGuard]`
followed by native:
`Task finished`

Then commit complete `LogOutput.log` to `RuntimeInbox/Current/`.

## Temporary state

EnemyIsolation: enabled  
BCMER 1.71.0: disabled

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`
