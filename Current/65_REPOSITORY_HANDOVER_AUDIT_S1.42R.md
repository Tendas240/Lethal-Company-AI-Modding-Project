# 65 — Repository Handover Audit: S1.42R

**Audit time:** 2026-09-03T22:12:00+02:00  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Verdict:** **PASS — repository is ready for a new chat; runtime gate remains open.**

## Canonical state verified

### Accepted gameplay baseline

- build: S1.41
- profile: `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`
- SHA-256: `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`
- status: runtime accepted

### Latest runtime evidence

- build: S1.42Q
- path: `RuntimeEvidence/S1.42Q/20260903T195158Z/`
- log SHA-256: `e8949f87c0df2e3f5a8e7b985bf698aab9de68bba08ae45e3fe5b89e89f27aa5`
- verdict: FAIL
- root cause: still-latched AttackEnemyTask co-attackers cannot reach upstream dead-target completion due to LethalMin 1.1.108 early return

### Current candidate

- build: S1.42R
- profile: `Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`
- SHA-256: `009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`
- Git blob SHA: `61e290182a0f056a20d81f31d340b27eb18f4be4`
- size: 533,870 bytes
- plugin: v1.3.13
- embedded DLL SHA-256: `0d39a8895a1324457c2ac135fa2ae129e58ba8155ce6bde1cdb59d340be420ff`
- status: built / repository-verified / not runtime-tested

## Build verification

GitHub Actions Build #54 / run `33800005390`:

**SUCCESS**

Generated commit:

`80fc7bc37476612320925083f062bda2b841cf40`

Idle guard #55:

**SUCCESS**

Archive:

- members: 331
- readable snapshot files: 330
- added: none
- changed from S1.42Q:
  - compatibility DLL
  - `export.r2x`

No config delta and no package-state delta from S1.42Q.

## Exact upstream evidence verified

Focused decompile exists:

`Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`

Exact LethalMin DLL SHA-256:

`9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df`

Root-cause analysis exists:

`Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`

R build document exists:

`Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`

## Profile snapshot checks

S1.42R `FILE_INDEX.json` verifies:

- `BepInEx/config/NoteBoxz.LethalMin.cfg`
  - SHA-256: `47715647f755b3efd9a601b108440d7613645702830799d7ed59a2139ff082b3`
- compatibility DLL
  - SHA-256: `0d39a8895a1324457c2ac135fa2ae129e58ba8155ce6bde1cdb59d340be420ff`
- `export.r2x`
  - SHA-256: `05583f3c59d759a963d112e80e95225bcc1ee434bb909c67234860ec117650f1`

Package counts from S1.42R export:

- total: 188
- enabled: 182
- disabled: 6

## Runtime/control checks

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42R`

`BuildSpecs/current.json`:

- enabled: false
- build id: `IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`
- base profile: S1.42R
- base SHA-256 matches S1.42R profile SHA-256

`RuntimeInbox/Current/`:

- only `.gitkeep`

`RuntimeEvidence/S1.42R/`:

- does not exist yet

This is the expected state for an untested current candidate.

## Temporary test-state checks

EnemyIsolation remains enabled.

BCMER exact 1.71.0 remains disabled.

`Thumper Bite Limit = 3`.

Normal enemy restore baseline remains present:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Restore SHA-256:

`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

## Current source check

`Patches/S139CompatibilityFixes/Plugin.cs`:

- plugin version: 1.3.13
- contains S1.42R `PatchLethalMinLatchedDeadTargetCompletion()`
- contains `[LethalMinLatchedDeathGuard]` startup/runtime markers
- contains `[LethalMinNativeOwnership]`
- does not contain the historical live `BaboonHawkDeathCleanup` implementation

## Historical/anti-regression preservation

Kept intentionally:

- S1.42P runtime failure evidence
- S1.42Q runtime evidence
- exact LethalMin decompile
- failed/obsolete approaches register
- S1.42C enemy restore baseline
- older handover/build documents as chronology/evidence
- repository optimization/migration plan

No runtime evidence was deleted.

No historical information was deleted.

No repository file was identified as **certainly obsolete and valueless** enough to justify deletion during this handover.

## Known documentation drift

Some historical files contain wording that was correct at their creation time but is no longer current.

Examples include older S1.42P/Q handovers/plans and old lower-priority technical-baseline passages.

These are retained as historical evidence.

Priority rule:

**S1.42R current/handover/audit files override older versioned wording for current-state decisions.**

General documentation cleanup remains deferred until the active runtime gate closes.

## Exact next action verified

Do not build S1.42S first.

Import S1.42R through Gale:

**Advanced options -> Import all files**

Use multiple Pikmin on the same Baboon Hawk, kill it, verify:

- all co-attackers stop attacking the dead target;
- `[LethalMinLatchedDeathGuard] Requested native FinishTaskServerRpc` appears for still-latched co-attackers;
- native `Task finished` follows;
- exact follower count recovers;
- no stale dead-target hits continue;
- no Work/no-task loop;
- no Leader-null loop.

Repeat on a second Hawk and retain corpse/one-way protection checks.

Commit the full fresh `LogOutput.log` to `RuntimeInbox/Current/`.

## Local manual work

No PowerShell/Git commands are required.

No local clone is required.

No local build is required.

Repository is ready for takeover.
