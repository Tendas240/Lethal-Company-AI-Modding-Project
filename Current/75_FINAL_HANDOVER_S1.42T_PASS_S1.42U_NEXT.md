# 75 — Final Handover: S1.42T PASS / S1.42U NEXT

**Prepared:** 2026-09-04  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

## Read first in a new chat

1. `Current/75_FINAL_HANDOVER_S1.42T_PASS_S1.42U_NEXT.md`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
5. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
6. `Current/Projektstatus_S1.42T.json`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
9. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
10. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
11. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
12. `BuildSpecs/S1.42U_PLAN.md`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`

After the repository audit is present, also read `Current/76_REPOSITORY_HANDOVER_AUDIT_S1.42T.md`.

Older S1.42S/Q/R handover and analysis files are historical/diagnostic evidence. They do not override this file or chronologically newer confirmed documentation.

## Role separation

### Last fully accepted full normal gameplay baseline

**S1.41 — BCMER Reactivation**

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

S1.41 remains the last accepted **full normal-stack** baseline only because BCMER is intentionally still disabled in S1.42T.

### Newest accepted technical descendant

**S1.42T — Normal Enemy Restore**

Profile:

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Runtime verdict:

**PASS — normal non-isolated enemy population restored.**

S1.42T is accepted for its defined normal-enemy-restore scope. It is not yet promoted to the final full normal-stack baseline because exact BCMER 1.71.0 is still intentionally disabled.

## S1.42T build identity and delta

Canonical automated build result:

`Current/AUTO_BUILD_RESULT.json`

Base:

**S1.42S — Baboon Adapter Lifecycle Restore**

Base profile SHA-256:

`addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`

Output SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Archive members:

**331**

Changed existing members only:

- `export.r2x`
- `BepInEx/config/tendas.s139.compatibilityfixes.cfg`

Added members:

**none**

Package-state changes:

**none**

Intended gameplay delta from S1.42S:

`Isolated Enemy Regression = true -> false`

Compatibility code/DLL did **not** change in S1.42T.

## Latest runtime evidence — S1.42T

Evidence directory:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log:

`RuntimeEvidence/S1.42T/20260903T222109Z/raw/LogOutput.log`

Raw log size:

`1,965,803 bytes`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Acceptance document:

`Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`

Confirmed in the complete runtime evidence:

- normal non-isolated enemies spawn again;
- direct `ADDING ENEMY` and active-instance evidence proves the restoration;
- the missed manual terminal `Enemies` scan is non-blocking and does not require a repeat S1.42T run;
- `Work state with no task assigned!` = **0**;
- `Leader is null when following` = **0**;
- `[Fatal` = **0**;
- `[Error  :S1.39 Compatibility Fixes]` = **0**;
- no new project compatibility exception flood;
- no crash/freeze;
- the player's run-ending death was normal gameplay `DeathPlayerJetpackBlast`.

Examples of restored normal population include Men-stalker, Puffer, Bagpipe, Flowerman/Bracken, ImmortalSnail, Spring/Coil-Head, MouthDog, Butler, Bunker Spider, Aloe and HauntedMask.

## Permanent compatibility state — do not regress

Compatibility plugin:

**v1.3.14**

Embedded DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Focused accepted predecessor:

**S1.42S — Baboon Adapter Lifecycle Restore**

Profile SHA-256:

`addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`

S1.42S runtime log SHA-256:

`9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`

Canonical acceptance:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Permanent root-cause correction:

S1.42R failed because project compatibility code disabled the entire `LethalMin.BaboonBirdPikminEnemy` component. That also disabled inherited `PikminEnemy.Update()` lifecycle work and prevented native death/unlatch cleanup. The accepted S1.42S/v1.3.14 solution keeps the adapter enabled and blocks only narrow Hawk -> Pikmin entry points.

Preserve all of the following:

- `BaboonBirdPikminEnemy` stays enabled;
- native `PikminEnemy` death/unlatch/task lifecycle stays owned by LethalMin;
- Hawk -> Pikmin unwanted interaction remains narrowly blocked;
- Pikmin -> Baboon Hawk attacks remain allowed;
- Puffer -> Pikmin protection remains;
- Pikmin -> Thumper/Crawler attack behavior remains available;
- Thumper/Crawler counterattack capability remains;
- `Thumper Bite Limit = 3`;
- `Crawler` remains absent from the LethalMin Attack Blacklist.

Every future custom patch must follow:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Core rule:

**Custom compatibility code must fix less than it understands, never more.**

Do not disable a complete foreign component to suppress one interaction unless its complete lifecycle is proven safe to suppress. Prefer narrow prevention before manual state repair.

## Restore baseline retained for regression recovery

Canonical enemy/spawn restore baseline:

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:

`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Machine-readable baseline:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Historical restore contract:

`Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`

That contract has now been **fulfilled by S1.42T**. Its old wording that S1.42T is not yet built is historical and must not be treated as the active next step.

Important accepted deviations from S1.42C that must remain:

- `Thumper Bite Limit = 3`, not S1.42C's old 0;
- `Crawler` remains removed from Attack Blacklist;
- all later accepted v1.3.14 compatibility fixes remain.

Do not restore all configs wholesale to S1.42C.

## Current package / diagnostic state

EnemyIsolation:

**disabled**

Config:

`BepInEx/config/tendas.s139.compatibilityfixes.cfg`

Current value:

`Isolated Enemy Regression = false`

BCMER package:

`SoftDiamond-BrutalCompanyMinusExtraReborn`

Exact version:

**1.71.0**

Current S1.42T state:

**disabled intentionally**

Never silently upgrade to BCMER 2.0.0 or another version.

## Controllers at handover

Runtime router:

`RuntimeInbox/ACTIVE_BUILD.txt`

Value:

`S1.42T`

Build controller:

`BuildSpecs/current.json`

State:

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42T_RUNTIME_PASS_AWAITING_S1.42U_BCMER_REACTIVATION`
- base profile = S1.42T
- base SHA-256 = `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`
- no successor build is armed.

Do not infer that S1.42U exists as a built candidate. It is **plan-only** until `BuildSpecs/current.json` is explicitly armed and GitHub Actions produces/verifies it.

## Runtime-log infrastructure

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

Normal logs:

`RuntimeInbox/Current/`

Very large logs:

- disposable branch `runtime-large`;
- `RuntimeInbox/Large/`;
- compression/splitting helper `BuildSystem/prepare_large_runtime_log.py`;
- every-line streaming analysis;
- compact analysis/provenance committed to `main`;
- raw very-large source retained temporarily as a **14-day GitHub Actions artifact**;
- exact pattern/regex/line-range context may be materialized through `RuntimeAnalysis/QUERY.json` while the artifact exists.

Automated pipeline self-test:

- workflow `.github/workflows/runtime-pipeline-selftest.yml`;
- program `BuildSystem/runtime_pipeline_selftest.py`;
- initial GitHub Actions verification run **33817297654 = success** on 2026-09-04.

The self-test covers analyzer marker counts, chat chunks, normalized signatures, split-ZIP reconstruction, large-ingest provenance, pattern query, line-range query and upload-manifest preparation.

The production very-large path has not yet been exercised with an actual 100–500 MB game log; the same core code paths have been synthetically end-to-end verified.

### S1.42T evidence retention

Do **not** delete the current S1.42T raw log yet. It is the clean BCMER-off normal-enemy comparison baseline for the immediate S1.42U gate.

After the BCMER comparison/final normal-stack dependency closes, it may be pruned according to `Current/74...` if build identity, SHA-256, verdict and unique evidence remain canonically preserved.

## Open non-blocking observations

### LethalMin disconnect NoticeZone

S1.42S one-off disconnect exception:

`PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects`

Classification:

**monitor-only / non-blocking**

Do not patch unless it becomes reproducible/user-facing and a Patch Safety Review supports intervention.

### Aloe audio-load marker

S1.42T one-off:

`Failed getting load state of FSB for audio clip "AloeChase"`

Classification:

**monitor-only / non-blocking**

Aloe later existed as an active runtime enemy and no user-facing regression was reported.

## Known non-functional documentation/comment drift

Two historical-text drift areas are intentionally **not gameplay blockers**:

1. `Current/02_TECHNICAL_BASELINE.md` still contains older subsections whose local wording says S1.42S or earlier states are "current". Treat those as chronology/history. For active state, this handover, `Current/00_CURRENT_STATE.md`, `Current/01_HANDOVER_CORE.md` and `Current/Projektstatus_S1.42T.json` override them.
2. `Patches/S139CompatibilityFixes/Plugin.cs` contains some older comments from the S1.42J-era that no longer perfectly describe the accepted v1.3.14 behavior. The actual current code path/config/runtime evidence is authoritative. Do not change executable compatibility behavior merely to clean comments during a gameplay gate.

Repository cleanup may normalize those historical labels/comments later as a separate maintenance change. Do not mix that cleanup into S1.42U.

## Exact next step

Next controlled build:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Plan:

`BuildSpecs/S1.42U_PLAN.md`

Base:

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

Base SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Only intended package-state change:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0: disabled -> enabled`

Preserve every accepted S1.42T/S1.42S compatibility/config value.

Do **not**:

- upgrade BCMER;
- modify compatibility code;
- modify EnemyIsolation other than keeping it false;
- change Thumper/Crawler behavior;
- tune interiors;
- tune CullFactory/fog;
- change CodeRebirth microwave rarity;
- rebalance BCMER EventType probabilities;
- perform structural repository migration.

### S1.42U runtime acceptance

Require:

1. main menu/startup succeeds;
2. exact BCMER 1.71.0 is runtime-active;
3. normal non-isolated enemies remain available/spawn normally;
4. no crash/freeze;
5. Work/no-task = 0;
6. Leader-null = 0;
7. no new project compatibility exception flood;
8. no BCMER-driven catastrophic event/system regression;
9. accepted Pikmin interaction behavior remains intact;
10. fresh full runtime log is ingested and compared against S1.42T.

No heavy Baboon-Hawk stress retest is required merely for BCMER reactivation because the compatibility code is unchanged, unless runtime evidence gives a reason to reopen it.

## Later S1.42 roadmap — do not mix into S1.42U

After BCMER restoration/final normal-stack acceptance:

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwaves somewhat rarer;
- final S1.42 acceptance.

## Manual user action at this handover

**None required.**

The repository already contains the required S1.42T profile, readable snapshot, build infrastructure, S1.42U plan, runtime evidence and controllers. Do not ask the user for a local clone or local profile build.

When the user explicitly requests S1.42U, arm `BuildSpecs/current.json` repository-first and let GitHub Actions build/verify it.
