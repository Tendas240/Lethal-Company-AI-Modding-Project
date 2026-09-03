# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current status

Game: **Lethal Company V81**

### Last fully accepted full normal gameplay baseline

**S1.41 — BCMER Reactivation**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

### Newest accepted technical descendant

**S1.42T — Normal Enemy Restore**

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Runtime verdict:

**PASS — normal non-isolated enemy population restored.**

Evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Compatibility plugin remains **v1.3.14** with embedded DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

S1.41 remains the last fully accepted *full normal-stack* baseline only because exact BCMER 1.71.0 is still intentionally disabled in S1.42T.

## Current state

- EnemyIsolation: **disabled** (`Isolated Enemy Regression = false`)
- BCMER exact `1.71.0`: **disabled intentionally**
- Thumper Bite Limit: **3**
- Crawler remains attackable by Pikmin / absent from Attack Blacklist
- no successor build is currently armed.

## Exact next step

Next controlled build:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Plan:

`BuildSpecs/S1.42U_PLAN.md`

Only intended package-state change:

- re-enable exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`.

Do not upgrade BCMER and do not mix unrelated gameplay tuning or custom patch changes into this gate.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
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

Newer confirmed current documentation overrides older version-specific handover files. Older S1.42S/Q/R material remains historical/diagnostic evidence, not the active next-step contract.

## Large runtime logs

Normal runtime logs continue through `RuntimeInbox/Current/` and are now processed by a streaming every-line analyzer. Smaller logs also receive lossless bounded `chat_chunks/` for direct ChatGPT reading.

Very large logs use the disposable `runtime-large` branch and `RuntimeInbox/Large/`. They are compressed/split if needed, fully streamed through analysis, retained temporarily as a 14-day Actions artifact for exact query-on-demand access, and are **not** meant to remain permanent raw history on `main`.

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

## Permanent patch-safety rule

Every project-local Harmony/runtime/compatibility patch must follow:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Compile/startup success alone is not acceptance. Custom patches must be narrow and regression-tested against adjacent/native lifecycle behavior.

## Repository-first rule

Do not ask the user for a local clone/build when the required profile, snapshots, build system, and GitHub Actions workflow already exist in this repository.
