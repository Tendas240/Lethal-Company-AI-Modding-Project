# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`
2. `Current/00_CURRENT_STATE.md`
3. `Current/Projektstatus_S1.42U.json`
4. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
5. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
6. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
7. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
8. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
9. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
10. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
11. `BuildSpecs/S1.42U_PLAN.md`
12. `BuildSpecs/current.json`
13. `RuntimeInbox/ACTIVE_BUILD.txt`

`Current/75_FINAL_HANDOVER_S1.42T_PASS_S1.42U_NEXT.md` and `Current/76_REPOSITORY_HANDOVER_AUDIT_S1.42T.md` are the immediately preceding handover records. They correctly describe the state before S1.42U was built, but chronologically newer S1.42U files now define the active state.

## Accepted roles

Last fully accepted full normal gameplay baseline:

**S1.41 — BCMER Reactivation**  
Profile `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Newest runtime-accepted technical descendant:

**S1.42T — Normal Enemy Restore**  
Profile `Profiles/LC V1 S1.42T Normal Enemy Restore.r2z`  
SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`  
Runtime verdict: **PASS**

Newest built candidate:

**S1.42U — BCMER 1.71.0 Reactivation Gate**  
Profile `Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`  
SHA-256 `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`  
Build verdict: **PASS**  
Runtime status: **awaiting validation**

Do not promote S1.42U before fresh runtime evidence passes.

## S1.42U build result

Base:

**S1.42T — Normal Enemy Restore**

Base SHA-256:

`a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`

Canonical build result:

`Current/AUTO_BUILD_RESULT.json`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

GitHub Actions run:

`33818241873` = **success**

Archive:

- 331 members;
- changed existing member only `export.r2x`;
- no added/removed members;
- no config patch;
- no compatibility code/DLL change.

Exact intended package-state delta:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0: disabled -> enabled`

## Preserved technical state

- EnemyIsolation: **off** (`Isolated Enemy Regression = false`)
- BCMER exact 1.71.0: **enabled in S1.42U**
- compatibility plugin: **v1.3.14**
- compatibility DLL SHA-256: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`
- Thumper Bite Limit: **3**
- Crawler: **not in Attack Blacklist**
- Puffer -> Pikmin poison interaction remains disabled

Never disable complete `LethalMin.BaboonBirdPikminEnemy`; preserve inherited native death/unlatch lifecycle.

## Runtime comparison baseline

S1.42T evidence:

`RuntimeEvidence/S1.42T/20260903T222109Z/`

Raw log SHA-256:

`b136464c55436fedc1d762aa9d961cea9ef53052d7cf829cdb93a4892184ec8f`

Keep that raw log until S1.42U is compared and the BCMER-on integration gate closes.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42U_BUILD_AWAITING_RUNTIME_VALIDATION`
- base = S1.42U
- base SHA-256 = `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

## Exact next step

Import and run:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

Perform a normal gameplay run with BCMER active and upload the complete `LogOutput.log` to:

`RuntimeInbox/Current/`

Runtime acceptance requires:

- startup/main menu succeeds;
- exact BCMER 1.71.0 is runtime-active;
- normal enemies still spawn;
- no crash/freeze;
- Work/no-task = 0;
- Leader-null = 0;
- no new project compatibility exception flood;
- no BCMER-specific catastrophic event/system regression;
- accepted Pikmin behavior remains intact;
- fresh full log compared against S1.42T.

Heavy Baboon-Hawk stress is not required solely for BCMER reactivation unless evidence reopens that regression.

## Open monitor-only observations

1. S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception. Non-blocking; no patch without reproducibility/user impact + Patch Safety Review.
2. S1.42T one-off `AloeChase` FSB load-state message. Non-blocking; monitor only.

## Forbidden mixed changes while S1.42U gate is open

Do not mix:

- BCMER upgrades;
- custom compatibility changes;
- interior probability tuning;
- CullFactory/fog tuning;
- CodeRebirth microwave rarity tuning;
- BCMER EventType rebalance;
- repository structural migration;
- cosmetic documentation/comment cleanup that touches executable behavior.

## Patch policy

All future project-local patches require `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and a Patch Safety Review.
