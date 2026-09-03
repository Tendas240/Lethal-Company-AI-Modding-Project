# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current state

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41 - BCMER Reactivation**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Latest valid runtime evidence:
**S1.42Q - FAIL**

`RuntimeEvidence/S1.42Q/20260903T195158Z/`

Log SHA-256:
`e8949f87c0df2e3f5a8e7b985bf698aab9de68bba08ae45e3fe5b89e89f27aa5`

## Current built candidate

**S1.42R - LethalMin Latched Dead Target Completion**

`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:
`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Compatibility plugin:
**v1.3.13**

## Root cause now proven

Exact LethalMinNightly:
**1.1.108**

Exact analyzed DLL SHA-256:
`9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df`

Decompiled:
`LethalMin.Pikmin.AttackEnemyTask.IntervaledUpdate()`

The method returns early while `IsPikminOnEnemy == true`, before its own dead-target check.

Therefore still-latched co-attackers can never reach LethalMin's existing:

`enemy.enemyScript.isEnemyDead -> FinishTaskServerRpc()`

branch.

S1.42Q reproduced this exactly:
- first Hawk attackers: `ruCpzY`, `PerDu`, `hcRGph`
- only `hcRGph` reached native `Task finished`
- `ruCpzY` and `PerDu` remained stuck on the dead first Hawk

Full evidence:
- `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`
- `Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`

## S1.42R fix

S1.42R patches only exact:

`LethalMin.Pikmin.AttackEnemyTask.IntervaledUpdate()`

When this exact task:
- is still latched;
- has its own target;
- and that target's `EnemyAI.isEnemyDead` is true;

the compatibility plugin requests native:

`PikminAI.FinishTaskServerRpc()`

before LethalMin's broken early return.

No:
- enemy death hook
- global scan
- proximity radius
- target-name guess
- direct RemoveCurrentTask
- manual unlatch
- custom leader repair
- custom corpse carry

All actual task ending/unlatching remains native LethalMin.

## Build verification

Compatibility DLL SHA-256:
`0d39a8895a1324457c2ac135fa2ae129e58ba8155ce6bde1cdb59d340be420ff`

GitHub Actions:
- Build #54: **SUCCESS**
- Idle guard #55: **SUCCESS**

S1.42Q -> R changed only:
1. compatibility DLL
2. `export.r2x`

No config or mod changes.

## Temporary state

EnemyIsolation:
**enabled**

BCMER 1.71.0:
**disabled**

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`

## Exact next step

Import S1.42R with:

**Gale -> Advanced options -> Import all files**

Use multiple Pikmin on the same Baboon Hawk.

After death:
- every attacker must stop;
- co-attackers should log `[LethalMinLatchedDeathGuard]`;
- they should immediately get native `Task finished`;
- follower count must fully recover.

Repeat on a second Hawk, then commit the complete fresh log to:

`RuntimeInbox/Current/`

Do not restore normal enemies or BCMER before R passes.

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/64_HANDOVER_S1.42R_TO_NEXT_FINAL.md`
3. `Current/65_REPOSITORY_HANDOVER_AUDIT_S1.42R.md`
4. `Current/Projektstatus_S1.42R.json`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`
9. `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`
10. `Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`
11. `Current/VERIFIKATION_S1.42R.txt`
12. `Current/SHA256SUMS_S1.42R.txt`
13. `Current/Aktive_Modliste_S1.42R.txt`
14. `BuildSpecs/S1.42R_PLAN.md`
15. `BuildSpecs/current.json`
16. `RuntimeInbox/ACTIVE_BUILD.txt`
17. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
18. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`


## Handover readiness

Final handover:
`Current/64_HANDOVER_S1.42R_TO_NEXT_FINAL.md`

Repository audit:
`Current/65_REPOSITORY_HANDOVER_AUDIT_S1.42R.md`

Audit verdict:
**PASS — ready for a new chat; S1.42R runtime validation is still pending.**

No local clone or local build is required.
