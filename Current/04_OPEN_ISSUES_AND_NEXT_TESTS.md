# 04 — Open Issues and Next Tests

## Closed gate — S1.42T Normal Enemy Restore

**PASS**

Acceptance:

`Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`

Evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Normal non-isolated enemy spawning is restored. No repeat S1.42T test is required solely for the missed terminal `Enemies` command.

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
- compatibility plugin v1.3.14 / DLL hash unchanged;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- current normal spawn-owner configs;
- all accepted Pikmin compatibility behavior.

Forbidden in S1.42U:

- BCMER 2.0.0 upgrade;
- new custom patch code;
- interior probability tuning;
- CullFactory/fog tuning;
- microwave rarity change;
- BCMER EventType rebalance;
- structural repository migration.

### S1.42U runtime acceptance

- normal stack starts and reaches gameplay;
- BCMER exact 1.71.0 is runtime-active;
- normal enemies still spawn;
- no new startup/runtime crash or freeze;
- no Work/no-task loop;
- no Leader-null loop;
- no new project compatibility exception flood;
- no BCMER-specific catastrophic event/system failure;
- fresh full runtime log ingested.

## Monitor-only issues

### LethalMin disconnect NoticeZone

`PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects`

Seen during disconnect in S1.42S. No user-facing regression. Do not patch without reproducibility + Patch Safety Review.

### Aloe audio load marker

S1.42T one-off:

`Failed getting load state of FSB for audio clip "AloeChase"`

No flood, Aloe later active, no user-facing issue reported. Monitor only.

## Runtime-log infrastructure

Canonical:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

The repository now supports streaming every-line analysis, small lossless chat chunks, a disposable very-large-log branch, temporary raw artifacts, and query-on-demand raw extraction.

Raw logs are not automatically permanent historical assets. Prune them after dependent gates/issues are closed and required evidence/provenance is preserved.

Keep the current S1.42T raw log through S1.42U because it is the immediate BCMER-off comparison baseline.

## Remaining broader S1.42 roadmap

After BCMER restoration/final normal-stack acceptance:

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwaves somewhat rarer;
- final S1.42 acceptance.
