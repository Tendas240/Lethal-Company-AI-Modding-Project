# 04 — Open Issues and Next Tests

## Active gate

**S1.42U — BCMER 1.71.0 Reactivation Gate** is built and build-verified, but **runtime validation is still open**.

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

Machine-readable status:

`Current/Projektstatus_S1.42U.json`

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

GitHub Actions build run:

`33818241873` = **success**

## Build delta — verified

Base:

`Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`

Base SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Archive members:

**331**

Changed existing members only:

- `export.r2x`

Exact package-state change:

- `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`: `disabled -> enabled`

No package addition/removal, config patch, local plugin build or compatibility-code change occurred.

Preserved and verified:

- `Isolated Enemy Regression = false`;
- compatibility plugin v1.3.14;
- compatibility DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- Puffer cannot poison Pikmin;
- accepted S1.42S Baboon/Pikmin lifecycle behavior;
- BCMER configuration carried forward unchanged.

## Accepted reference roles

Last fully accepted full normal-stack baseline:

**S1.41 — BCMER Reactivation**  
SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Newest runtime-accepted technical descendant:

**S1.42T — Normal Enemy Restore**  
SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`  
Verdict **PASS**

S1.42U must not replace either accepted role until runtime evidence passes.

## S1.42U runtime test

### Immediate user action

Import/run:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Perform a normal gameplay run with BCMER active. Then upload the complete `LogOutput.log` to:

`RuntimeInbox/Current/`

`RuntimeInbox/ACTIVE_BUILD.txt` is already set to `S1.42U`.

### Acceptance criteria

1. main menu/startup succeeds;
2. exact BCMER 1.71.0 is loaded/active;
3. normal non-isolated enemies remain available/spawn normally;
4. no startup/runtime crash or freeze;
5. `Work state with no task assigned!` = 0;
6. `Leader is null when following` = 0;
7. no new S1.39 Compatibility Fixes error/exception flood;
8. no BCMER-driven catastrophic event/system regression;
9. accepted Pikmin behavior remains intact;
10. fresh full runtime log is ingested and compared against S1.42T.

A heavy Baboon-Hawk stress retest is not required merely because BCMER is re-enabled; reopen that focused test only if new evidence indicates a regression.

## S1.42T comparison evidence

Acceptance:

`Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`

Evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Keep the S1.42T raw log through this immediate BCMER-on comparison gate.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42U_BUILD_AWAITING_RUNTIME_VALIDATION`
- base = S1.42U

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

## Monitor-only issues

### LethalMin disconnect NoticeZone

`PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects`

Seen during disconnect in S1.42S. No user-facing regression. Do not patch without reproducibility + Patch Safety Review.

### Aloe audio load marker

S1.42T one-off:

`Failed getting load state of FSB for audio clip "AloeChase"`

No flood, Aloe later active, no user-facing issue reported. Monitor only.

## Permanent do-not-regress references

Patch safety:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Focused S1.42S acceptance:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Corrected S1.42R root cause:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Canonical enemy restore baseline:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Forbidden mixed changes while S1.42U runtime gate is open

Do not include:

- BCMER upgrade;
- new custom patch code;
- interior probability tuning;
- CullFactory/fog tuning;
- microwave rarity change;
- BCMER EventType rebalance;
- structural repository migration;
- executable compatibility changes disguised as cleanup.

## Remaining broader S1.42 roadmap

After BCMER restoration/final normal-stack acceptance:

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwaves somewhat rarer;
- final S1.42 acceptance.
