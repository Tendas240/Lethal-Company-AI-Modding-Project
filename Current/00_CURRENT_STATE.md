# 00 — Current State

**Updated:** 2026-09-04  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Current canonical state

Newest built candidate:

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

Machine-readable status:

`Current/Projektstatus_S1.42U.json`

GitHub Actions build run:

`33818241873` = **success**

**Runtime status: awaiting validation.** S1.42U is build-verified but must not be promoted before a fresh runtime log passes the BCMER-on integration gate.

## Accepted role separation

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

Runtime acceptance:

`Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`

Evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

S1.42T verdict:

**PASS — normal non-isolated enemy population restored.**

S1.41 remains the last fully accepted full-normal-stack baseline until S1.42U passes runtime because S1.42U has not yet been runtime validated with BCMER active.

## S1.42U exact build delta

Base:

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

Base SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Archive members:

**331**

Changed existing members only:

- `export.r2x`

Added members:

**none**

Exact package-state change:

- `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`: `disabled -> enabled`

No package addition/removal, config patch, local plugin build or compatibility-code change occurred.

Canonical generated result:

`Current/AUTO_BUILD_RESULT.json`

Readable snapshot:

`ProfileSources/S1.42U/`

## Permanent compatibility state to preserve

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

Focused accepted predecessor:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Corrected failed-root-cause reference:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

## Current package / diagnostic state

EnemyIsolation:

**disabled**

`Isolated Enemy Regression = false`

BCMER:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

S1.42U package state:

**enabled**

Do not upgrade to BCMER 2.0.0 or another version.

Thumper Bite Limit:

**3**

Crawler:

**not in Attack Blacklist**

## Controllers

Build controller:

`BuildSpecs/current.json`

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42U_BUILD_AWAITING_RUNTIME_VALIDATION`
- base = S1.42U
- base SHA-256 = `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime router:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

## Exact next step

Run a normal gameplay test with:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Then upload the complete `LogOutput.log` to:

`RuntimeInbox/Current/`

Runtime acceptance requires:

1. main menu/startup succeeds;
2. exact BCMER 1.71.0 is runtime-active;
3. normal non-isolated enemies remain available/spawn normally;
4. no crash/freeze;
5. `Work state with no task assigned!` = 0;
6. `Leader is null when following` = 0;
7. no new S1.39 Compatibility Fixes error/exception flood;
8. no BCMER-driven catastrophic event/system regression;
9. accepted Pikmin interaction behavior remains intact;
10. fresh full runtime evidence is compared against S1.42T.

A heavy Baboon-Hawk stress retest is not required solely for BCMER reactivation unless new evidence reopens that regression.

## Runtime-log infrastructure

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

Normal logs:

`RuntimeInbox/Current/`

Very large logs:

- disposable `runtime-large` branch;
- `RuntimeInbox/Large/`;
- compact analysis/provenance on `main`;
- temporary 14-day raw Actions artifact;
- query-on-demand through `RuntimeAnalysis/QUERY.json`.

Keep the S1.42T raw log until the S1.42U BCMER-on comparison gate is closed.

## Monitor-only issues

1. S1.42S disconnect-only LethalMin `PikminNoticeZone.OnTriggerStay` / unspawned `NetworkObjectReference` exception. Do not patch without reproducible user impact and Patch Safety Review.
2. S1.42T one-off `Failed getting load state of FSB for audio clip "AloeChase"`. Monitor only unless reproducible/user-facing.

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local "current" wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains older comments that do not perfectly describe accepted v1.3.14 behavior.

Actual current code/config/runtime evidence and chronologically newer canonical documents are authoritative. Do not mix cosmetic cleanup into the open S1.42U runtime gate.

## Later S1.42 roadmap — do not mix into S1.42U

After the BCMER restoration/final normal-stack gate closes:

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwave rarity reduction;
- final S1.42 acceptance.
