# 00 — Current State

**Updated:** 2026-09-04  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Current canonical state

Newest accepted technical descendant:

**S1.42T — Normal Enemy Restore**

Profile:

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Runtime acceptance:

`Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`

Evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Verdict:

**PASS — normal non-isolated enemy population restored; no critical LethalMin regression markers; no new compatibility exception flood.**

## Last fully accepted normal gameplay baseline

**S1.41 — BCMER Reactivation**

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

S1.41 remains the last fully accepted *full normal-stack* baseline because S1.42T intentionally keeps BCMER disabled. S1.42T is nevertheless runtime accepted for its isolated normal-enemy restoration scope.

## Permanent S1.42 compatibility state to preserve

Compatibility plugin:

**v1.3.14**

Embedded DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Preserve:

- `BaboonBirdPikminEnemy` remains enabled;
- only narrow Hawk -> Pikmin entry points are blocked;
- native PikminEnemy death/unlatch lifecycle remains active;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection remains;
- Thumper/Crawler counterattack capability remains;
- `Thumper Bite Limit = 3`;
- Crawler remains absent from LethalMin Attack Blacklist.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## S1.42T runtime findings

Confirmed:

- normal non-isolated enemies spawn again;
- direct `ADDING ENEMY`/active-instance evidence makes the missed terminal `Enemies` scan non-blocking;
- `Work state with no task assigned!` = 0;
- `Leader is null when following` = 0;
- `[Fatal` = 0;
- `[Error  :S1.39 Compatibility Fixes]` = 0;
- no runtime crash/freeze;
- player death was normal gameplay `DeathPlayerJetpackBlast`;
- known SoundAPI/SoftMask/etc. stack noise is non-blocking;
- one-off `AloeChase` FSB load-state message is monitor-only.

## Current package/diagnostic state

EnemyIsolation:

**disabled**

`Isolated Enemy Regression = false`

BCMER exact package:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

State in S1.42T:

**disabled intentionally**

Do not upgrade to BCMER 2.0.0.

## Exact next gameplay gate

Next controlled build identity:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Plan:

`BuildSpecs/S1.42U_PLAN.md`

Only intended package-state variable:

- re-enable exact BCMER `1.71.0`.

Preserve S1.42T and all accepted compatibility/config state. Do not mix interior tuning, fog, CullFactory, microwave rarity, EventType distribution, repository migration, or new custom patch code into this gate.

## Controllers

Runtime router:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42T`

Build controller:

`BuildSpecs/current.json`

- `enabled = false`
- idle after S1.42T runtime PASS
- base = S1.42T
- no successor build armed.

## Large runtime logs

Canonical policy/infrastructure:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

Normal logs continue through `RuntimeInbox/Current/` and now receive streaming full-line analysis plus bounded ChatGPT-readable chunks when small enough.

Very large logs use the disposable `runtime-large` branch, `RuntimeInbox/Large/`, compact analysis on `main`, a 14-day raw Actions artifact, and query-on-demand extraction through `RuntimeAnalysis/QUERY.json`.

Raw logs are not permanent by default. They may be removed once their dependent gate/issues are closed and canonical evidence/provenance has been preserved.

The current S1.42T raw log is retained for now because it is the immediate BCMER-off comparison baseline for S1.42U.

## Monitor-only issues

1. LethalMin disconnect-only `PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects` from S1.42S. Do not patch without reproducible user-facing impact and Patch Safety Review.
2. S1.42T one-off `Failed getting load state of FSB for audio clip "AloeChase"`. Monitor only unless user-facing/reproducible.

## Later S1.42 work

After BCMER restoration/final normal-stack gate:

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwave rarity reduction;
- final S1.42 acceptance.

Do not mix these into S1.42U.
