# 76 — Repository Handover Audit: S1.42T PASS / S1.42U NEXT

**Date:** 2026-09-04  
**Purpose:** final repository consistency audit for transfer to a new ChatGPT chat.

## Audit result

**PASS — canonical project state is consistent for handover.**

The repository remains the source of truth. No local repository clone or local profile build is required for the next step.

## Canonical role separation verified

Last fully accepted full normal gameplay baseline:

- **S1.41 — BCMER Reactivation**
- profile `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`
- SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Newest accepted technical descendant:

- **S1.42T — Normal Enemy Restore**
- profile `Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`
- SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`
- runtime verdict **PASS**

Next controlled identity:

- **S1.42U — BCMER 1.71.0 Reactivation Gate**
- status **plan-only / not built**
- plan `BuildSpecs/S1.42U_PLAN.md`

No document should describe S1.42U as an existing candidate/profile until the build controller is explicitly armed and GitHub Actions creates it.

## S1.42T build verification

`Current/AUTO_BUILD_RESULT.json` confirms:

- base S1.42S SHA-256 `addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`;
- output SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`;
- 331 archive members;
- changed existing members only `export.r2x` and `BepInEx/config/tendas.s139.compatibilityfixes.cfg`;
- no added members;
- no mod-state/addition/removal changes;
- intended gameplay delta only `Isolated Enemy Regression = false`.

## S1.42T runtime verification

Evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

`INDEX.json` confirms:

- raw file `LogOutput.log`;
- size `1,965,803 bytes`;
- SHA-256 `b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`.

Canonical acceptance:

`Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`

Verified verdict facts:

- normal non-isolated enemy population restored;
- Work/no-task = 0;
- Leader-null = 0;
- Fatal = 0;
- project compatibility Error = 0;
- no new compatibility exception flood;
- no runtime crash/freeze;
- player death was normal `DeathPlayerJetpackBlast`;
- missed manual terminal `Enemies` command is non-blocking because direct runtime spawning/instance evidence is stronger.

## Permanent compatibility / restore invariants verified

Compatibility plugin:

- v1.3.14;
- embedded DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`.

S1.42S focused evidence retained:

- profile SHA-256 `addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`;
- runtime log SHA-256 `9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`;
- acceptance `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`.

Do-not-regress root cause retained:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Permanent patch policy retained:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Canonical enemy restore baseline retained:

- `Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`;
- SHA-256 `22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`;
- machine-readable `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.

Historical `Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md` remains intentionally preserved. Its restore action was fulfilled by S1.42T; old next-step wording is historical, not active.

## Controller audit

`RuntimeInbox/ACTIVE_BUILD.txt`:

`S1.42T`

This is correct because S1.42T is the most recent built/runtime-tested evidence target and S1.42U does not yet exist.

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42T_RUNTIME_PASS_AWAITING_S1.42U_BCMER_REACTIVATION`;
- base profile = S1.42T;
- base SHA-256 = `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`;
- no mod/config/plugin change is armed.

Controller state is therefore safe at handover: **no unintended build can trigger from the canonical controller.**

## Runtime-log infrastructure audit

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

Verified infrastructure includes:

- normal ingest via `RuntimeInbox/Current/`;
- every-line analyzer `BuildSystem/runtime_log_analyzer.py`;
- bounded lossless chat chunks for smaller logs;
- disposable `runtime-large` branch and `RuntimeInbox/Large/` for very large evidence;
- compression/splitting helper;
- compact analysis/provenance to `main`;
- 14-day raw Actions artifact for very-large inputs;
- targeted raw query controller `RuntimeAnalysis/QUERY.json`;
- automatic runtime-pipeline self-test.

Self-test verification:

- workflow `.github/workflows/runtime-pipeline-selftest.yml`;
- program `BuildSystem/runtime_pipeline_selftest.py`;
- GitHub Actions run `33817297654` = **success**.

The production very-large path has not yet been exercised with an actual 100–500 MB game log; synthetic end-to-end verification of the core code paths is complete.

## Evidence retention audit

No runtime evidence was deleted during this handover.

Specifically retained:

- S1.42S focused runtime evidence;
- S1.42T normal-enemy runtime evidence;
- S1.42C restore baseline/profile;
- failed/root-cause history needed for regression prevention.

The S1.42T raw log must remain until the immediate S1.42U BCMER-on comparison/final normal-stack dependency is closed. It is currently the clean BCMER-off reference run.

No file was identified as safe enough to delete during this handover without reducing future diagnostic or documentary value.

## Canonical documentation synchronization

Updated for this handover:

- `Current/75_FINAL_HANDOVER_S1.42T_PASS_S1.42U_NEXT.md` — new;
- `Current/00_CURRENT_STATE.md`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`;
- `Current/Projektstatus_S1.42T.json`;
- `README.md`;
- this audit file.

Verified and intentionally left functionally unchanged:

- `START_HERE_ChatGPT_Masterprompt.txt` — its current takeover block already states S1.42T PASS / S1.42U NEXT, correct hashes/controller state and the large-log policy; the permanent master workflow remains valuable and was not destructively rewritten merely to add another handover pointer;
- `RuntimeInbox/ACTIVE_BUILD.txt` — already correct;
- `BuildSpecs/current.json` — already correct/disarmed;
- `BuildSpecs/S1.42U_PLAN.md` — already correct one-variable plan;
- `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md` — accepted evidence record;
- `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md` — already includes the successful runtime-pipeline self-test.

## Known non-functional drift classification

The audit confirms two non-blocking documentation/comment drift areas:

1. `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections whose local text calls S1.42S or earlier states "current".
2. `Patches/S139CompatibilityFixes/Plugin.cs` contains some older comments that do not perfectly describe the accepted v1.3.14 behavior.

These do **not** change the accepted code path/config/runtime state. Newer canonical documentation is authoritative. Do not modify executable compatibility behavior just to clean historical wording, and do not mix cleanup into S1.42U. A later dedicated repository-maintenance pass may normalize them.

## Open issues at transfer

Blocking gameplay issues:

**none identified for the closed S1.42T gate.**

Monitor-only:

1. S1.42S disconnect-only `PikminNoticeZone.OnTriggerStay` / unspawned `NetworkObjectReference` exception.
2. S1.42T one-off `AloeChase` FSB load-state message.

Do not create project-local patches for either without reproducible user-facing impact and the mandatory Patch Safety Review.

## Exact next action after takeover

When the user asks to proceed, build **S1.42U — BCMER 1.71.0 Reactivation Gate** repository-first from S1.42T.

Only intended package-state change:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0: disabled -> enabled`

Do not upgrade BCMER and do not mix any unrelated tuning or code changes.

At the moment of handover, no local user action is required.
