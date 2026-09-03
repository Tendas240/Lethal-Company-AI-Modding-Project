# 00 — Current State

**Updated:** 2026-09-03  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Canonical handover

Final handover:

`Current/71_HANDOVER_S1.42S_TO_NEXT_FINAL.md`

Repository audit:

`Current/72_REPOSITORY_HANDOVER_AUDIT_S1.42S.md`

Machine-readable status:

`Current/Projektstatus_S1.42S.json`

Exact next-step contract:

`Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`

Next build plan:

`BuildSpecs/S1.42T_PLAN.md`

Permanent patch-safety policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Last fully accepted normal gameplay baseline

**S1.41 — BCMER Reactivation**

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:

**runtime accepted**

S1.41 remains the last full normal-gameplay baseline because the newer S1.42S test profile still has temporary EnemyIsolation enabled and BCMER disabled.

## Latest built and tested technical descendant

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

- Build canonical profile #56: **SUCCESS**
- run ID: `33803720934`
- generated commit: `3bb900342c41595504bf9ce6879477aad22a7d49`
- idle guard #57: **SUCCESS**

## Latest valid runtime evidence

**S1.42S — PASS for focused isolated Baboon-Hawk/Pikmin lifecycle gate**

Evidence:

`RuntimeEvidence/S1.42S/20260903T205550Z/`

Raw log:

`RuntimeEvidence/S1.42S/20260903T205550Z/raw/LogOutput.log`

Log SHA-256:

`9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`

Full analysis:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Confirmed:

- three focused Pikmin attacked the same Baboon Hawk;
- Hawk death at approximately `20:52:32.546`;
- post-death stale attack-hit count = **0** for all three;
- all three remained recoverable;
- all three were later assigned back to the player;
- native idle/task removal/unlatch resumed;
- dead Hawk body was naturally carried to the Onion;
- `Work state with no task assigned!` = **0**;
- `Leader is null when following` = **0**.

## Corrected root cause

Canonical analysis:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

The project compatibility patch had disabled the complete:

`LethalMin.BaboonBirdPikminEnemy`

component.

That also disabled inherited:

`PikminEnemy.Update() -> RemoveAndDisableTriggers() -> RemoveAllPikmin(3)`

and suppressed native dead-enemy unlatch cleanup.

The older claim that the `AttackEnemyTask.IntervaledUpdate()` early return alone was the complete upstream root cause is superseded.

S1.42S fixes this by keeping `BaboonBirdPikminEnemy` enabled and blocking only narrow Hawk -> Pikmin entry points.

## Temporary current state

EnemyIsolation:

**enabled**

Config:

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

## Canonical restore baseline

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Baseline profile SHA-256:

`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Verified restore rule:

- normal enemy/spawn-owner configs remain byte-identical to S1.42C in the spot-checked files;
- disable only the temporary EnemyIsolation diagnostic;
- preserve later accepted LethalMin deltas:
  - `Thumper Bite Limit = 3`;
  - do not re-add `Crawler` to Attack Blacklist.

## Exact next action

Next planned build:

**S1.42T — Normal Enemy Restore**

Status:

**planned only / not built**

Build from S1.42S.

For S1.42T:

1. set `Isolated Enemy Regression = false`;
2. keep compatibility plugin v1.3.14 unchanged;
3. keep `Thumper Bite Limit = 3`;
4. keep Crawler attackable by Pikmin;
5. keep exact BCMER 1.71.0 **disabled** for this first restoration gate;
6. make no unrelated package/config/gameplay changes;
7. runtime-test that normal non-isolated enemies spawn again.

Only after that passes should exact BCMER 1.71.0 be re-enabled in a separate controlled stage.

Do not upgrade BCMER.

## Controllers

Runtime router:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42S`

This is correct until a new build actually exists.

Build controller:

`BuildSpecs/current.json`

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42S_FOCUSED_RUNTIME_PASS_AWAITING_S1.42T_RESTORE_BUILD`
- base = S1.42S

No build is currently armed.

## Monitor-only issue

One disconnect-only LethalMin exception:

`PikminNoticeZone.OnTriggerStay -> NetworkObjectReference can only be created from spawned NetworkObjects`

It occurred after ShipOnion save during lobby disconnect.

Classification:

**monitor-only / non-blocking**

Do not patch without a reproducible user-facing issue and a Patch Safety Review.

## Permanent engineering rule

Every project-local runtime/Harmony/compatibility patch must comply with:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Compile success, startup success, or removal of the direct symptom is not sufficient acceptance.

## Repository maintenance

Structural migration remains tracked in:

`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

The old S1.42S runtime-gate reason for deferring migration is closed, but repository migration must not be mixed into the immediate S1.42T gameplay restore build.
