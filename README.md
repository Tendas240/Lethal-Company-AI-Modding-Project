# Lethal Company AI Modding Project

GitHub is the canonical source of truth.

## Current built candidate

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
**built and repository-verified; awaiting runtime test**

## Latest runtime evidence

**S1.42Q — FAIL, exact upstream root cause identified**

Evidence:
`RuntimeEvidence/S1.42Q/20260903T195158Z/`

Log SHA-256:
`e8949f87c0df2e3f5a8e7b985bf698aab9de68bba08ae45e3fe5b89e89f27aa5`

Exact failed co-attackers:
- `Yellow Pikmin_ruCpzY`
- `Yellow Pikmin_PerDu`

Successful control:
- `Yellow Pikmin_hcRGph`

## Root cause

Exact LethalMin version:
**NotezyTeam-LethalMinNightly 1.1.108**

Exact analyzed DLL SHA-256:
`9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df`

`AttackEnemyTask.IntervaledUpdate()` returns while a Pikmin is still latched before it reaches LethalMin's own `enemy.enemyScript.isEnemyDead` check.

S1.42R patches only that missing branch and invokes LethalMin's existing native `FinishTaskServerRpc()` for the exact task whose own target is dead.

No enemy death hook, no Pikmin scan, no radius, no target guessing, no direct state mutation.

## Build verification

GitHub Actions Build #54:
**SUCCESS**

Generated commit:
`80fc7bc37476612320925083f062bda2b841cf40`

Q -> R changed only:
- local compatibility DLL
- `export.r2x` profile name

All configs are unchanged.

## Temporary state

EnemyIsolation:
**enabled**

BCMER 1.71.0:
**disabled**

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`

## Exact next step

Import S1.42R through Gale:

**Advanced options -> Import all files**

Put at least 3 Pikmin on the same Baboon Hawk, kill it, verify full follower recovery, repeat once, and commit the complete fresh `LogOutput.log` to `RuntimeInbox/Current/`.

Expected for stale co-attackers:

`[LethalMinLatchedDeathGuard] Requested native FinishTaskServerRpc ...`

followed by native:

`Task finished`

## Read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`
3. `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`
4. `Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`
5. `Current/Projektstatus_S1.42R.json`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/VERIFIKATION_S1.42R.txt`
10. `Current/SHA256SUMS_S1.42R.txt`
11. `Current/Aktive_Modliste_S1.42R.txt`
12. `BuildSpecs/S1.42R_PLAN.md`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`
