# 01 — Handover Core

## Identity

Game:

**Lethal Company V81**

Repository:

`Tendas240/Lethal-Company-AI-Modding-Project`

Repository is the source of truth.

## Read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/71_HANDOVER_S1.42S_TO_NEXT_FINAL.md`
3. `Current/72_REPOSITORY_HANDOVER_AUDIT_S1.42S.md`
4. `Current/Projektstatus_S1.42S.json`
5. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
6. `Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`
7. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
8. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
9. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
10. `BuildSpecs/S1.42T_PLAN.md`
11. `BuildSpecs/current.json`
12. `RuntimeInbox/ACTIVE_BUILD.txt`

## Accepted baseline

Last fully accepted normal gameplay baseline:

**S1.41 — BCMER Reactivation**

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

## Current technical descendant

**S1.42S — Baboon Adapter Lifecycle Restore**

Profile:

`Profiles/LC V1 S1.42S Baboon Adapter Lifecycle Restore.r2z`

SHA-256:

`addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`

Compatibility plugin:

**v1.3.14**

DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Status:

**focused runtime accepted / isolated regression pass**

## Runtime result

Evidence:

`RuntimeEvidence/S1.42S/20260903T205550Z/`

Log SHA-256:

`9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`

The three focused Pikmin stopped attacking immediately after Baboon Hawk death, remained recoverable, and native corpse carry/Onion delivery worked.

No Work/no-task loop.

No Leader-null loop.

## Do-not-regress root cause

Do not disable complete `LethalMin.BaboonBirdPikminEnemy`.

It owns inherited native death/unlatch cleanup.

S1.42S correctly keeps the component enabled and blocks only narrow Hawk -> Pikmin entry points.

See Current/66 and Current/69.

## Temporary state

EnemyIsolation:

**enabled**

`Isolated Enemy Regression = true`

BCMER exact 1.71.0:

**disabled**

Thumper Bite Limit:

**3**

Crawler:

**not in Attack Blacklist**

## Exact next step

Prepare/build:

**S1.42T — Normal Enemy Restore**

From S1.42S.

Only required gameplay delta for the first restore gate:

`Isolated Enemy Regression = false`

Preserve:

- compatibility v1.3.14;
- Thumper Bite Limit 3;
- Crawler attackable by Pikmin;
- all accepted permanent compatibility fixes.

Keep BCMER exact 1.71.0 disabled for S1.42T so normal-enemy restoration is tested as one variable.

Then runtime-test normal enemy population.

Only after S1.42T passes, re-enable exact BCMER 1.71.0 in a separate controlled stage.

## Controllers

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42S`

`BuildSpecs/current.json` is disabled and idle after S1.42S PASS.

Do not build from a local clone.

Use repository-first GitHub Actions/profile builder.

## Patch policy

All future custom patches require:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Every patch build plan must contain a Patch Safety Review.
