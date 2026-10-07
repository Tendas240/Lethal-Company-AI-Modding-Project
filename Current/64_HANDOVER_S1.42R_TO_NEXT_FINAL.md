# 64 — Final Handover: S1.42R to Next Chat

**Updated:** 2026-09-03T22:12:00+02:00  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

This file is the concise canonical handover for the next chat.

## 1. Source of truth

Use the GitHub repository as the source of truth.

Read in this order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/64_HANDOVER_S1.42R_TO_NEXT_FINAL.md`
3. `Current/65_REPOSITORY_HANDOVER_AUDIT_S1.42R.md`
4. `Current/Projektstatus_S1.42R.json`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`
9. `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`
10. `Current/63_S1.42R_LATCHED_DEAD_TARGET_COMPLETION_BUILD.md`
11. `Current/VERIFIKATION_S1.42R.txt`
12. `Current/SHA256SUMS_S1.42R.txt`
13. `Current/Aktive_Modliste_S1.42R.txt`
14. `BuildSpecs/S1.42R_PLAN.md`
15. `BuildSpecs/current.json`
16. `RuntimeInbox/ACTIVE_BUILD.txt`
17. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
18. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`

Older Q/P handover/build documents remain historical evidence and must not override the newer R files above.

## 2. Last fully accepted gameplay baseline

**S1.41 — BCMER Reactivation**

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:

**runtime accepted**

This remains the last fully accepted normal-play baseline.

## 3. Latest valid runtime evidence

**S1.42Q — FAIL**

Evidence:

`RuntimeEvidence/S1.42Q/20260903T195158Z/`

Raw log:

`RuntimeEvidence/S1.42Q/20260903T195158Z/raw/LogOutput.log`

Log SHA-256:

`e8949f87c0df2e3f5a8e7b985bf698aab9de68bba08ae45e3fe5b89e89f27aa5`

User observation and log evidence agree:

- multiple Pikmin attacked the first Baboon Hawk;
- after its death, two Pikmin were effectively lost/stuck;
- the second Baboon Hawk was attacked by one relevant Pikmin and that Pikmin did not disappear.

Exact first-Hawk attackers:

- `Yellow Pikmin_ruCpzY`
- `Yellow Pikmin_PerDu`
- `Yellow Pikmin_hcRGph`

Exact behavior:

- `hcRGph` reached native `Task finished`;
- `ruCpzY` never reached `Task finished`;
- `PerDu` never reached `Task finished`;
- `ruCpzY` and `PerDu` stayed on the stale AttackEnemy task and kept hitting the already-dead first Hawk;
- `Work state with no task assigned!`: 0;
- `Leader is null when following`: 0;
- old project-local `[BaboonHawkDeathCleanup]`: absent.

## 4. Exact upstream root cause

Exact package:

`NotezyTeam-LethalMinNightly 1.1.108`

Exact analyzed embedded DLL:

`NoteBoxz.LethalMin.dll`

SHA-256:

`9f7338a6a45d09e97b56965fc6efde7ab31476483d9d528ff0ce11563154a0df`

Focused decompile:

`Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt`

Root-cause analysis:

`Current/62_S1.42Q_RUNTIME_LATCHED_COATTACKER_ROOT_CAUSE.md`

In upstream:

`LethalMin.Pikmin.AttackEnemyTask.IntervaledUpdate()`

returns early while `IsPikminOnEnemy == true`.

The existing upstream dead-target branch:

`enemy.enemyScript.isEnemyDead -> PikminAI.FinishTaskServerRpc()`

is only reached **after** that early return.

Therefore a still-latched co-attacker cannot reach LethalMin's own dead-target completion branch.

This is a generic LethalMin 1.1.108 AttackEnemyTask defect, not a Baboon-Hawk-specific distance or corpse bug.

## 5. Current built candidate

**S1.42R — LethalMin Latched Dead Target Completion**

Profile:

`Profiles/LC V1 S1.42R LethalMin Latched Dead Target Completion.r2z`

SHA-256:

`009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

Git blob SHA:

`61e290182a0f056a20d81f31d340b27eb18f4be4`

Size:

**533,870 bytes**

Base:

`Profiles/LC V1 S1.42Q LethalMin Native Minimal Rollback.r2z`

Base SHA-256:

`50a8488a7d5f5c0a318db2557895d7029de3cfa1c0d704498bb9d90eaa481cb1`

Compatibility plugin:

**v1.3.13**

Embedded DLL SHA-256:

`0d39a8895a1324457c2ac135fa2ae129e58ba8155ce6bde1cdb59d340be420ff`

Build verification:

- GitHub Actions Build #54 / run ID `33800005390`: **SUCCESS**
- generated build commit: `80fc7bc37476612320925083f062bda2b841cf40`
- idle guard #55: **SUCCESS**
- 331 archive members
- 330 readable snapshot files
- added members: none
- changed existing members from S1.42Q:
  1. compatibility DLL
  2. `export.r2x`
- config delta S1.42Q -> S1.42R: **none**
- package/mod delta S1.42Q -> S1.42R: **none**

## 6. S1.42R patch semantics

Patch only exact:

`LethalMin.Pikmin.AttackEnemyTask.IntervaledUpdate()`

The prefix acts only when all are true:

1. this exact task is still latched;
2. this exact task's own `enemy` exists;
3. that enemy's `enemyScript.isEnemyDead` is true.

Then request native:

`PikminAI.FinishTaskServerRpc()`

and skip the broken upstream interval for that tick.

The normal finish path remains LethalMin-owned:

`FinishTaskServerRpc -> FinishTaskClientRpc -> FinishTask -> TaskEnd -> SetToIdle -> Unlatch/RemoveTask`

The patch does **not**:

- hook Baboon Hawk death;
- hook generic enemy death;
- scan Pikmin;
- scan enemies;
- use a proximity radius;
- guess target identity;
- match enemy names;
- call `RemoveCurrentTask()`;
- manually unlatch;
- manually repair leader/follow state;
- implement corpse carrying.

## 7. Intended interaction architecture

Keep this asymmetry:

- **Pikmin -> living enemies:** native LethalMin attack/latch/kill.
- **Enemy death/task completion:** native LethalMin, with only the exact S1.42R bridge for the proven latched early-return defect.
- **Pikmin -> dead enemy bodies / Onion:** native LethalMin + SellBodies path.
- **Enemies -> Pikmin:** blocked through native config first and only proven minimal compatibility shims second.

Do not rebuild LethalMin's normal attack/carry lifecycle in the project plugin.

## 8. Temporary isolated test state

EnemyIsolation:

**enabled**

Exact BCMER package:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

BCMER state:

**disabled**

Do not silently upgrade BCMER to 2.0.0.

LethalMin:

`Thumper Bite Limit = 3`

Package state:

- total: 188
- enabled: 182
- disabled: 6

Disabled exactly:

- `AJB-Keep_hangar_ship_door_closed 1.0.0`
- `zealsprince-Malfunctions 1.10.3`
- `Reiko88-Observer 2.0.1`
- `ProjectSCP-SCP999 2.4.0`
- `Kittenji-Dont_Touch_Me 1.2.8`
- `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

## 9. Controllers

`RuntimeInbox/ACTIVE_BUILD.txt`:

`S1.42R`

`BuildSpecs/current.json`:

- `enabled = false`
- `build_id = IDLE_AFTER_S1.42R_BUILD_AWAITING_RUNTIME`
- base profile = S1.42R
- base SHA-256 = `009bb12c57410ebb851c6604b588ab8f04f7f0ea618fd497696d538d7b4f0101`

`RuntimeInbox/Current/` currently contains only `.gitkeep`.

There is currently **no `RuntimeEvidence/S1.42R/` evidence**, which is correct because R has not yet been runtime-tested.

## 10. Exact next step

**Do not build S1.42S first.**

Import S1.42R with Gale:

**Advanced options -> Import all files**

Focused runtime gate:

1. start with a known follower count, preferably 20;
2. latch at least 3 Pikmin onto the same Baboon Hawk;
3. kill the Hawk;
4. verify every attacker stops hitting the dead Hawk immediately;
5. expected for still-latched co-attackers:
   `[LethalMinLatchedDeathGuard] Requested native FinishTaskServerRpc ...`
6. expected native follow-up for the same Pikmin:
   `Task finished`
7. whistle/recover all Pikmin and verify the exact original follower count;
8. repeat on a second Hawk;
9. verify Dead Baboon Hawk body remains naturally carryable to Onion;
10. verify living Hawk still ignores Pikmin and the corpse;
11. verify no `Work state with no task assigned!`;
12. verify no `Leader is null when following`;
13. commit the complete fresh `LogOutput.log` to `RuntimeInbox/Current/`.

Then analyze R before any normal-enemy/BCMER restoration.

## 11. Restore rule after the enemy gate

Canonical enemy restore baseline:

`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Restore profile:

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:

`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

After the isolated regression chain passes:

- remove only diagnostic EnemyIsolation;
- restore/carry forward enemy-related configuration from the S1.42C baseline unless a later explicitly accepted gameplay decision supersedes it;
- re-enable exact BCMER 1.71.0;
- do not reconstruct enemy spawn configuration from memory.

## 12. Critical do-not-regress rules

Do not restore:

- broad/inherited LethalMin reflection/Harmony scanning;
- continuous `FindObjectsOfType<EnemyAI>()` scanning;
- direct `RemoveCurrentTask()` as death finalizer;
- 4 m / widened-radius Hawk death cleanup;
- project-local generic Hawk death `FinishTask()` sweep;
- reflection-heavy post-grab leader/follow restoration;
- custom Pikmin corpse-carry/Onion logic;
- historical two-way Baboon Hawk/Pikmin zero-interaction;
- CodeRebirthLib;
- BCMER 2.0.0 as a silent replacement for 1.71.0.

Do not guess unknown Enemy PowerLevels.

## 13. Historical evidence / cleanup

Do not delete runtime evidence or historical Q/P analyses.

They prove why earlier approaches failed.

Known non-functional documentation drift in older/historical lower-priority files remains deferred until the open runtime gate closes. General structural repository migration is also deferred:

`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

No destructive history rewrite, filter-repo/BFG, LFS migration, or external-storage migration without explicit user approval.

## 14. Local user actions

No local repository clone, local build, or manual Git cleanup is required for this handover.

The only user-side action currently required is the S1.42R Gale import/runtime test described above.
