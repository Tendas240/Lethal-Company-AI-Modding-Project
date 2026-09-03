# 01 - Handover Core

## Current identity

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41**

Latest runtime evidence:
**S1.42Q — FAIL, exact LethalMin 1.1.108 latched co-attacker bug identified**

Current built candidate:
**S1.42R — LethalMin Latched Dead Target Completion**

Profile:
`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Compatibility plugin:
**v1.3.13**

Read first:
- `Current/64_HANDOVER_S1.42R_TO_NEXT_FINAL.md`
- `Current/65_REPOSITORY_HANDOVER_AUDIT_S1.42R.md`
- `Current/Projektstatus_S1.42R.json`
- `Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`
- `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`
- `BuildSpecs/S1.42R_PLAN.md`
- `Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`
- `Current/VERIFIKATION_S1.42R.txt`
- `Current/SHA256SUMS_S1.42R.txt`

## Exact root cause

LethalMinNightly 1.1.108:

`AttackEnemyTask.IntervaledUpdate()`

returns immediately when `IsPikminOnEnemy == true`.

Its existing `enemy.enemyScript.isEnemyDead -> FinishTaskServerRpc()` branch occurs only **after** that return.

Therefore:
- the Pikmin whose native path transitions can finish;
- still-latched co-attackers never execute dead-target completion;
- they stay on the dead target indefinitely.

S1.42Q proved this exactly:
- first Hawk attackers: `ruCpzY`, `PerDu`, `hcRGph`
- `hcRGph`: native Task finished
- `ruCpzY`: no Task finished, stale
- `PerDu`: no Task finished, stale

## S1.42R patch

One exact generic LethalMin shim:

`AttackEnemyTask.IntervaledUpdate()` prefix.

Only if:
- currently latched;
- this task's own target exists;
- that target's `EnemyAI.isEnemyDead` is true;

call the same native:
`PikminAI.FinishTaskServerRpc()`

that upstream already uses for the unlatched dead-target case.

No Hawk death hook.
No radius.
No global scan.
No direct RemoveCurrentTask.
No manual unlatch.
No custom leader restoration.

## Verification

Build #54:
**SUCCESS**

Idle guard #55:
**SUCCESS**

Profile SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Embedded DLL SHA-256:
`0d39a8895a1324457c2ac135fa2ae129e58ba8155ce6bde1cdb59d340be420ff`

S1.42Q -> R:
- DLL changed
- profile name changed
- configs unchanged
- mods unchanged

## Exact next action

Import with:
**Gale -> Advanced options -> Import all files**

Use multiple Pikmin on one Baboon Hawk.

After death:
- every attacker must stop;
- stale co-attackers should emit `[LethalMinLatchedDeathGuard]`;
- each should then emit native `Task finished`;
- follower count must fully recover.

Repeat with a second Hawk and re-check corpse carry and one-way Hawk -> Pikmin protection.

Commit complete fresh log to `RuntimeInbox/Current/`.

## Temporary state

EnemyIsolation:
enabled.

BCMER 1.71.0:
disabled.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`


## Handover status

Repository takeover audit:
**PASS**

Final handover:
`Current/64_HANDOVER_S1.42R_TO_NEXT_FINAL.md`

Audit:
`Current/65_REPOSITORY_HANDOVER_AUDIT_S1.42R.md`

S1.42R has not yet been runtime-tested.
Do not interpret the absence of `RuntimeEvidence/S1.42R/` as missing ingestion; no R test has been performed yet.
