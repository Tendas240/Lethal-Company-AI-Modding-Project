# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/00_CURRENT_STATE.md`
2. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
3. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
4. `Current/Projektstatus_S1.42T.json`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
7. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
8. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
9. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
10. `BuildSpecs/S1.42U_PLAN.md`
11. `BuildSpecs/current.json`
12. `RuntimeInbox/ACTIVE_BUILD.txt`

Older S1.42S handover/audit files remain historical evidence but no longer define the active next step.

## Accepted roles

Last fully accepted full normal gameplay baseline:

**S1.41 — BCMER Reactivation**  
SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Newest accepted technical descendant:

**S1.42T — Normal Enemy Restore**  
Profile `Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`  
SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

S1.42T scope verdict: **PASS**.

## Latest runtime evidence

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Normal enemy population is directly proven by runtime spawn/active-instance evidence. Manual `Enemies` terminal scan was missed because the player died, but is not required to repeat this gate.

Critical counts:

- Work/no-task = 0
- Leader-null = 0
- Fatal = 0
- project compatibility Error = 0
- no new compatibility exception flood.

Player death = `DeathPlayerJetpackBlast`, not crash.

## Current technical state

- EnemyIsolation: **off** (`Isolated Enemy Regression = false`)
- BCMER exact 1.71.0: **disabled intentionally**
- compatibility plugin: v1.3.14
- compatibility DLL SHA-256: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`
- Thumper Bite Limit: 3
- Crawler: not in Attack Blacklist

Never disable complete `LethalMin.BaboonBirdPikminEnemy`; preserve inherited native death/unlatch lifecycle.

## Exact next step

Prepare/build **S1.42U — BCMER 1.71.0 Reactivation Gate** from S1.42T.

Only intended package-state change:

- `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`: disabled -> enabled.

Do not upgrade BCMER. Do not change compatibility code. Do not mix other gameplay tuning.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42T`

`BuildSpecs/current.json` is disabled/idle after S1.42T runtime PASS. No build is armed.

## Runtime log handling

See `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`.

- normal logs: `RuntimeInbox/Current/`;
- large logs: disposable `runtime-large` branch + `RuntimeInbox/Large/`;
- all logs receive streaming every-line analysis;
- very large raw evidence is temporary, not permanent `main` history;
- arbitrary raw context can be materialized while the 14-day artifact exists via `RuntimeAnalysis/QUERY.json`;
- raw/auxiliary logs may be pruned after dependent gates/issues close and canonical evidence is preserved.

## Patch policy

All future project-local patches require `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and a Patch Safety Review.
