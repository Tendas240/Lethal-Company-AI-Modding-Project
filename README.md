# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current status

Game: **Lethal Company V81**

### Newest built candidate

**S1.42U — BCMER 1.71.0 Reactivation Gate**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

GitHub Actions run `33818241873`: **success**

**Runtime validation is still required. Do not treat S1.42U as accepted gameplay state yet.**

### Accepted reference roles

Last fully accepted full normal gameplay baseline:

**S1.41 — BCMER Reactivation**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Newest runtime-accepted technical descendant:

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

S1.41 remains the last fully accepted full-normal-stack baseline until S1.42U passes runtime.

## S1.42U exact delta

Base:

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

Only intended and verified package-state change:

- `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`: **disabled -> enabled**

Build result:

- 331 archive members;
- changed existing member only `export.r2x`;
- no added/removed members;
- no config patch;
- no local plugin/compatibility-code change.

Preserved:

- EnemyIsolation off (`Isolated Enemy Regression = false`);
- compatibility plugin v1.3.14;
- compatibility DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted Pikmin compatibility behavior.

Do not upgrade BCMER to 2.0.0.

## Exact next step

Import/run:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Perform a normal gameplay run with BCMER active, then upload the complete `LogOutput.log` to:

`RuntimeInbox/Current/`

`RuntimeInbox/ACTIVE_BUILD.txt` is already `S1.42U`.

Runtime gate requires startup success, exact BCMER 1.71.0 active, normal enemies still spawning, no crash/freeze, no Work/no-task or Leader-null regression, no new compatibility exception flood, no catastrophic BCMER system/event regression, and accepted Pikmin behavior intact.

Keep the S1.42T raw log through this immediate BCMER-on comparison.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`
3. `Current/00_CURRENT_STATE.md`
4. `Current/01_HANDOVER_CORE.md`
5. `Current/Projektstatus_S1.42U.json`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
8. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
9. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
10. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
11. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
12. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
13. `BuildSpecs/S1.42U_PLAN.md`
14. `BuildSpecs/current.json`
15. `RuntimeInbox/ACTIVE_BUILD.txt`

`Current/75_FINAL_HANDOVER_S1.42T_PASS_S1.42U_NEXT.md` and `Current/76_REPOSITORY_HANDOVER_AUDIT_S1.42T.md` are preserved as the immediately preceding pre-build handover state. Chronologically newer confirmed S1.42U files override their old "S1.42U not built" status.

## Permanent anti-regression references

Patch safety:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Focused S1.42S lifecycle acceptance:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Corrected S1.42R root cause:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Canonical S1.42C enemy restore baseline:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Never disable complete `LethalMin.BaboonBirdPikminEnemy` merely to block Hawk -> Pikmin interaction; preserve native inherited death/unlatch lifecycle and use the narrowest exact interception point.

## Runtime-log infrastructure

Normal logs use `RuntimeInbox/Current/` and streaming every-line analysis.

Very large logs use the disposable `runtime-large` branch and `RuntimeInbox/Large/`, with compact analysis/provenance on `main`, a temporary 14-day raw Actions artifact, and query-on-demand extraction through `RuntimeAnalysis/QUERY.json`.

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

## Known non-functional drift

`Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local "current" wording, and `Patches/S139CompatibilityFixes/Plugin.cs` contains historical comments that do not perfectly describe accepted v1.3.14 behavior. Current code/config/runtime evidence plus chronologically newer canonical docs are authoritative. Do not mix cosmetic cleanup into the open S1.42U runtime gate.

## Repository-first rule

Do not ask the user for a local clone/build when the required profile, snapshots, build system, and GitHub Actions workflow already exist in this repository.
