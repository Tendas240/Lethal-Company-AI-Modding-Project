# 04 — Open Issues and Next Tests

## Handover status

Primary takeover:

`Current/75_FINAL_HANDOVER_S1.42T_PASS_S1.42U_NEXT.md`

S1.42T is accepted. S1.42U is plan-only and **not built**. `BuildSpecs/current.json` is disarmed.

## Closed gate — S1.42T Normal Enemy Restore

**PASS**

Acceptance:

`Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`

Evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log size:

`1,965,803 bytes`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Profile SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Normal non-isolated enemy spawning is restored. No repeat S1.42T test is required solely for the missed terminal `Enemies` command.

Critical runtime results:

- Work/no-task = 0;
- Leader-null = 0;
- Fatal = 0;
- project compatibility Error = 0;
- no new compatibility exception flood;
- no crash/freeze;
- player death = normal `DeathPlayerJetpackBlast`.

Keep the S1.42T raw log through the immediate BCMER restoration comparison because it is the clean BCMER-off normal-enemy reference run.

## Active next task — S1.42U BCMER 1.71.0 Reactivation Gate

Plan:

`BuildSpecs/S1.42U_PLAN.md`

Base:

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

Base SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Required variable:

- re-enable exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`.

Preserve:

- `Isolated Enemy Regression = false`;
- compatibility plugin v1.3.14;
- compatibility DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- current normal spawn-owner configs;
- all accepted Pikmin compatibility behavior;
- native `BaboonBirdPikminEnemy` / `PikminEnemy` death-unlatch lifecycle.

Forbidden in S1.42U:

- BCMER 2.0.0 or any other version upgrade;
- new custom patch code;
- interior probability tuning;
- CullFactory/fog tuning;
- microwave rarity change;
- BCMER EventType rebalance;
- structural repository migration;
- cosmetic documentation/comment cleanup mixed into the gameplay gate.

### S1.42U runtime acceptance

- main menu/startup succeeds;
- exact BCMER 1.71.0 is runtime-active;
- normal enemies still spawn;
- no new startup/runtime crash or freeze;
- no Work/no-task loop;
- no Leader-null loop;
- no new project compatibility exception flood;
- no BCMER-specific catastrophic event/system failure;
- accepted Pikmin behavior remains intact;
- fresh full runtime log ingested and compared against S1.42T.

A heavy Baboon-Hawk stress retest is not required merely because BCMER is re-enabled; reopen that focused test only if new evidence indicates a regression.

## Permanent do-not-regress / restore references

Patch safety:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Focused S1.42S acceptance:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Corrected S1.42R root cause:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Canonical enemy restore baseline:

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:

`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Machine-readable restore baseline:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

The historical `Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md` was fulfilled by S1.42T and is retained for diagnostic/history value.

## Monitor-only issues

### LethalMin disconnect NoticeZone

`PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects`

Seen during disconnect in S1.42S. No user-facing regression. Do not patch without reproducibility + Patch Safety Review.

### Aloe audio load marker

S1.42T one-off:

`Failed getting load state of FSB for audio clip "AloeChase"`

No flood, Aloe later active, no user-facing issue reported. Monitor only.

## Known non-functional documentation/comment drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology sections with local "current" wording for S1.42S/earlier.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains some older comments that do not perfectly describe accepted v1.3.14 behavior.

These are not gameplay defects. Newer canonical state documents and actual code/config/runtime evidence override the stale wording. Cleanup should be a separate maintenance change after the active gameplay gate.

## Runtime-log infrastructure

Canonical:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

The repository supports streaming every-line analysis, small lossless chat chunks, a disposable very-large-log branch, temporary raw artifacts, and query-on-demand raw extraction.

Automated self-test:

- `.github/workflows/runtime-pipeline-selftest.yml`;
- `BuildSystem/runtime_pipeline_selftest.py`;
- initial GitHub Actions run `33817297654` = **success**.

Raw logs are not automatically permanent historical assets. Prune them only after dependent gates/issues are closed and required evidence/provenance is preserved.

## Remaining broader S1.42 roadmap

After BCMER restoration/final normal-stack acceptance:

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwaves somewhat rarer;
- final S1.42 acceptance.
