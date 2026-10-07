# 71 — Final Handover: S1.42S -> Next Chat

**Date:** 2026-09-03  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Game:** Lethal Company V81

## 1. Current canonical state

### Last fully accepted normal gameplay baseline

**S1.41 — BCMER Reactivation**

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Why S1.41 is still the full baseline:

S1.42S passed its focused regression gate but still runs with temporary EnemyIsolation enabled and BCMER 1.71.0 disabled.

### Latest technical descendant / current tested candidate

**S1.42S — Baboon Adapter Lifecycle Restore**

Profile:

`Profiles/LC V1 S1.42S Baboon Adapter Lifecycle Restore.r2z`

SHA-256:

`addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`

Compatibility plugin:

**v1.3.14**

Embedded DLL SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Build verification:

- GitHub Actions Build canonical profile #56
- run ID `33803720934`
- result **SUCCESS**
- generated commit `3bb900342c41595504bf9ce6879477aad22a7d49`
- idle guard #57 **SUCCESS**
- archive members: 331
- readable snapshot files: 330
- S1.42R -> S1.42S changed only the compatibility DLL and `export.r2x`
- no package delta
- no config delta

## 2. Latest valid runtime evidence

**S1.42S — PASS for focused isolated Baboon-Hawk/Pikmin lifecycle gate**

Evidence:

`RuntimeEvidence/S1.42S/20260903T205550Z/`

Raw log:

`RuntimeEvidence/S1.42S/20260903T205550Z/raw/LogOutput.log`

Log SHA-256:

`9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`

Full analysis:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Relevant attackers:

- `Yellow Pikmin_IkVZWQe`
- `Yellow Pikmin_3wnH`
- `Yellow Pikmin_ruCpzY`

Baboon Hawk death:

`20:52:32.546`

Result:

- post-death stale attack-hit count across all three = **0**
- all three remained recoverable
- all three were later reassigned to player leader
- native task/unlatch lifecycle resumed
- corpse CarryItem lifecycle remained functional
- Dead Baboon Hawk reached the Onion and was consumed
- `Work state with no task assigned!` = **0**
- `Leader is null when following` = **0**
- old full-adapter-disable marker = **0**
- removed S1.42R dead-target shim marker = **0**

The one-way collision guard was exercised:

`[BaboonHawkPikminGuard] Blocked LethalMin BaboonBirdPikminEnemy.OnColideWithPikmin. Adapter remains enabled for native death/latch cleanup.`

## 3. Corrected root cause that must not regress

S1.42R failed because the project compatibility patch disabled the complete:

`LethalMin.BaboonBirdPikminEnemy`

component.

That also disabled inherited:

`PikminEnemy.Update() -> RemoveAndDisableTriggers() -> RemoveAllPikmin(3)`

and prevented native death/unlatch cleanup.

Canonical root-cause document:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

The earlier S1.42Q/R theory that the `AttackEnemyTask.IntervaledUpdate()` early return alone was the complete upstream root cause is superseded.

S1.42S fixed this by keeping `BaboonBirdPikminEnemy` enabled and blocking only narrow Hawk -> Pikmin entry points.

## 4. Permanent patch-safety rule

All future project-local patches must follow:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Especially:

- inspect inheritance/base lifecycle;
- inspect cleanup/state/network responsibilities;
- use the narrowest exact patch surface;
- do not disable a whole foreign component for one interaction without proving all lost responsibilities safe;
- compile/startup success is not gameplay acceptance;
- runtime-test adjacent/reverse behavior;
- rollback/narrow collateral damage instead of stacking repair layers.

Every future patch build plan requires a **Patch Safety Review**.

## 5. Temporary state that still exists

EnemyIsolation:

**enabled**

Exact config:

`BepInEx/config/tendas.s139.compatibilityfixes.cfg`

`Isolated Enemy Regression = true`

BCMER:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

State:

**disabled**

Thumper Bite Limit:

**3**

LethalMin Attack Blacklist:

`Crawler` is intentionally **not** blacklisted.

## 6. Restore baseline and exact next step

Canonical enemy restore baseline:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Baseline profile SHA-256:

`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Exact restore contract:

`Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`

Important comparison result:

All stored normal enemy/spawn-owner configs spot-checked from the restore baseline are byte-identical between S1.42C and S1.42S except the intentional later LethalMin values and the project diagnostic config.

Preserve later accepted LethalMin deltas:

- `Thumper Bite Limit = 3`
- do not re-add `Crawler` to Attack Blacklist

### Exact next action

Prepare/build **S1.42T — Normal Enemy Restore** from S1.42S.

For the first restore gate:

- set `Isolated Enemy Regression = false`
- keep the permanent v1.3.14 compatibility plugin/fixes
- keep later accepted LethalMin deltas
- keep exact BCMER 1.71.0 **disabled**
- make no unrelated package/config/gameplay changes
- validate that the normal enemy population has returned

Only after that restoration passes should exact BCMER 1.71.0 be re-enabled in a separate controlled stage.

Do not upgrade BCMER to 2.0.0.

## 7. Monitor-only issue

One LethalMin exception occurred exactly during lobby disconnect after ShipOnion save:

`ArgumentException: NetworkObjectReference can only be created from spawned NetworkObjects.`

Stack owner:

`LethalMin.PikminNoticeZone.OnTriggerStay`

Classification:

**monitor-only / non-blocking**

No user-facing failure was observed.

Do not add a custom patch unless it becomes reproducible/user-facing and a full Patch Safety Review supports intervention.

## 8. Controllers at handover

Runtime router:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42S`

This remains correct because S1.42S is the latest built/runtime-ingested profile and S1.42T does not exist yet.

Build controller:

`BuildSpecs/current.json`

must remain disabled/idle until S1.42T is deliberately prepared.

No local clone/build is required.

## 9. Historical evidence to preserve

Do not delete:

- S1.42Q runtime evidence/decompile;
- S1.42R failed runtime evidence;
- S1.42S passing runtime evidence;
- S1.42C enemy restore baseline;
- failed/obsolete approach register;
- patch safety policy;
- earlier build/runtime records needed to explain the fix chronology.

Historical S1.42R handover files remain historical only and are superseded by this handover.

## 10. Repository maintenance

The structural repository optimization plan remains:

`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

The critical S1.42S runtime gate is now closed, so the old reason for deferring migration is no longer active.

However, do **not** mix repository migration into the next gameplay restoration build. Keep the next S1.42T restore gate isolated. Repository migration can be scheduled as a separate maintenance phase after the next gameplay state is cleanly documented.

## 11. Read order for next chat

Read completely:

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

Then use topic-specific historical files only as needed.
