# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/75_FINAL_HANDOVER_S1.42T_PASS_S1.42U_NEXT.md`
2. `Current/00_CURRENT_STATE.md`
3. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
4. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
5. `Current/Projektstatus_S1.42T.json`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
8. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
9. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
10. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
11. `BuildSpecs/S1.42U_PLAN.md`
12. `BuildSpecs/current.json`
13. `RuntimeInbox/ACTIVE_BUILD.txt`
14. `Current/76_REPOSITORY_HANDOVER_AUDIT_S1.42T.md` when present.

Older S1.42S/Q/R handover/audit files remain historical evidence but no longer define the active next step.

## Accepted roles

Last fully accepted full normal gameplay baseline:

**S1.41 — BCMER Reactivation**  
Profile `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Newest accepted technical descendant:

**S1.42T — Normal Enemy Restore**  
Profile `Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`  
SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

S1.42T scope verdict: **PASS**.

S1.42U is **not built**. It is the next plan-only controlled gate.

## S1.42T build result

Base:

**S1.42S — Baboon Adapter Lifecycle Restore**

Base SHA-256:

`addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`

Canonical build result:

`Current/AUTO_BUILD_RESULT.json`

S1.42T contains 331 archive members and changed only:

- `export.r2x`;
- `BepInEx/config/tendas.s139.compatibilityfixes.cfg`.

No package state change occurred. Intended gameplay delta: `Isolated Enemy Regression = false`.

## Latest runtime evidence

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log size:

`1,965,803 bytes`

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

## Restore / do-not-regress baseline

Canonical enemy restore baseline:

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:

`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Machine-readable baseline:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

The historical `Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md` has been fulfilled by S1.42T. Preserve its diagnostic value, but do not use its old "S1.42T not built" text as an active instruction.

Do not wholesale-revert to S1.42C. Preserve later accepted `Thumper Bite Limit = 3`, Crawler attackability and v1.3.14 compatibility behavior.

## Exact next step

Prepare/build **S1.42U — BCMER 1.71.0 Reactivation Gate** from S1.42T.

Only intended package-state change:

- `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`: disabled -> enabled.

Do not upgrade BCMER. Do not change compatibility code. Do not mix other gameplay tuning, repository migration, or documentation/comment cleanup.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42T`

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42T_RUNTIME_PASS_AWAITING_S1.42U_BCMER_REACTIVATION`;
- base = S1.42T;
- no build is armed.

## Runtime log handling

See `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`.

- normal logs: `RuntimeInbox/Current/`;
- large logs: disposable `runtime-large` branch + `RuntimeInbox/Large/`;
- all logs receive streaming every-line analysis;
- very large raw evidence is temporary, not permanent `main` history;
- arbitrary raw context can be materialized while the 14-day artifact exists via `RuntimeAnalysis/QUERY.json`;
- raw/auxiliary logs may be pruned after dependent gates/issues close and canonical evidence is preserved.

Runtime pipeline self-test:

- `.github/workflows/runtime-pipeline-selftest.yml`;
- `BuildSystem/runtime_pipeline_selftest.py`;
- initial Actions run `33817297654` = **success**.

Keep the current S1.42T raw log through S1.42U because it is the clean BCMER-off comparison baseline.

## Open monitor-only observations

1. S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception. Non-blocking; no patch without reproducibility/user impact + Patch Safety Review.
2. S1.42T one-off `AloeChase` FSB load-state message. Non-blocking; monitor only.

## Known non-functional drift

`Current/02_TECHNICAL_BASELINE.md` contains older chronology sections that locally call S1.42S/earlier states "current". `Patches/S139CompatibilityFixes/Plugin.cs` also contains older comments that do not perfectly describe v1.3.14. Treat current code/config/runtime evidence and newer canonical docs as authoritative. Cleanup is separate maintenance and must not be mixed into S1.42U.

## Patch policy

All future project-local patches require `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and a Patch Safety Review.
