# 56 — Final Handover S1.42P to Next Chat

**Date:** 2026-09-03  
**Game:** Lethal Company V81  
**Repository:** Tendas240/Lethal-Company-AI-Modding-Project

## 1. Canonical state

Repository is the Source of Truth.

Last fully accepted normal-gameplay baseline:

**S1.41 — BCMER Reactivation**

Profile:
`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Current built candidate:

**S1.42P — Baboon Hawk Exact FinishTask Recovery**

Profile:
`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Git blob SHA:
`924b2bb3109bddbbe4558885b158960e19495768`

Size:
537,963 bytes.

Status:
**BUILT / STATICALLY VERIFIED / NOT YET RUNTIME-TESTED**

Compatibility plugin:
**S1.39 Compatibility Fixes v1.3.11**

## 2. Build verification

GitHub Actions:
- build run #48 / ID `33783386675`: SUCCESS;
- idle-guard run #49 / ID `33783508656`: SUCCESS.

Build commit:
`a6e97be239a3865be2adb03474b594cab960a539`

Archive:
- 331 members;
- 330 readable snapshot files;
- only changed existing members:
  - `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`
  - `export.r2x`
- no added members.

Readable snapshot:
`ProfileSources/S1.42P/`

## 3. Exact temporary profile state

Packages:
- total 188;
- enabled 182;
- disabled 6.

Disabled:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8
- SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0

Current mod list:
`Current/Aktive_Modliste_S1.42P.txt`

EnemyIsolation:
**ENABLED**

Config:
`Isolated Enemy Regression = true`

Exact BCMER package:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Current BCMER state:
**DISABLED**

Do not silently upgrade BCMER to 2.0.0.

Canonical normal-enemy restore point:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Restore profile:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

Restore SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

The restore point must not be deleted or reconstructed from memory.

## 4. Current LethalMin / SellBodies state

LethalMin:
- `No Knock Back = true`
- `Invinceable Pikmin = true`
- `Pikmin Die In Player Death Zones = false`
- Attack Blacklist does **not** contain Crawler/Thumper or Baboon Hawk.

SellBodies:
- Baboon Hawk bodies enabled;
- body spawn delay = 4 seconds.

Desired Baboon Hawk rules remain asymmetric:

Living Hawk -> Pikmin:
**blocked**

Pikmin -> living Hawk:
**normal latch / attack / kill allowed**

After Hawk death:
- attackers must stop stale attack state;
- attackers must remain visible/responsive/recoverable;
- Dead Baboon Hawk corpse remains present;
- players/Pikmin may carry corpse;
- Pikmin may carry corpse to Onion;
- living Baboon Hawks must not pick up/relocate corpse.

Do not restore the historical S1.42J two-way zero-interaction behavior.

## 5. Runtime progression that matters

### S1.42L — interaction gates passed, death regression exposed

Evidence:
`RuntimeEvidence/S1.42L/20260903T155132Z/`

Log SHA-256:
`812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10`

Confirmed:
- Thumper/Crawler -> Pikmin protection PASS;
- Pikmin -> Thumper/Crawler attack/latch PASS;
- Puffer -> Pikmin immunity PASS;
- Jetpack ~140 sec PASS;
- Baboon Hawk -> Pikmin ignore PASS;
- Pikmin -> living Baboon Hawk attack/latch/kill PASS;
- no leader-null loop.

New regression:
Pikmin attached to Hawk stale target disappear with old Hawk transform after death/SellBodies move.

### S1.42M — corpse side passed, child-transform resolver failed

Evidence:
`RuntimeEvidence/S1.42M/20260903T163446Z/`

Log SHA-256:
`0639d5cc04aa54f5d7943ef4689e0d705c818871b019287ca1a1cdc2aa2492fb`

PASS:
- Dead Baboon Hawk body appears;
- Pikmin can carry it to Onion;
- living Hawks ignore corpse;
- no leader-null loop.

FAIL:
death cleanup reported:
`released 0/0 latched Pikmin`

Conclusion:
attacking Pikmin are not children under the Hawk transform.

### S1.42N — target resolver passed, low-level cleanup broke Pikmin state

Evidence:
`RuntimeEvidence/S1.42N/20260903T165818Z/`

Log SHA-256:
`8ed6a79230e28535a01a4cb86a8971c358a5c9f57a53722e18ff4342474f51cf`

Resolver:
**6/6 actual attack participants selected**

Failure:
direct `PikminAI.RemoveCurrentTask()` left five selected attackers in:
`Work state with no task assigned!`

Total warnings:
**2155**

User observed ~4–5 Pikmin running in place, non-following and unusable.

One stale attacker continued `Hitting enemy with: 0.03` for more than a minute.

Do not use direct RemoveCurrentTask as Hawk-death finalizer again.

### S1.42O — safe no-op revealed exact method name

Evidence:
`RuntimeEvidence/S1.42O/20260903T171220Z/`

Log SHA-256:
`1a1251f19a1d82e90b72e82ac8e4babd523c32e695fe3d7923d4590debb0be71`

User observed:
**8 Pikmin disappeared after Hawk death.**

Reason:
S1.42O attempted `PikminAI.TaskFinished()`, but that method does not exist.

Important:
The plugin intentionally did **not** fall back to RemoveCurrentTask.

Runtime reflection exposed exact declared candidates, including:

`PikminAI.FinishTask():Void`

The eight attack participants kept hitting the dead Hawk after death and beyond SellBodies corpse creation.

This runtime-discovered method name is the basis of S1.42P.

## 6. S1.42P implementation

Source:
`Patches/S139CompatibilityFixes/Plugin.cs`

Plugin version:
`1.3.11`

Exact implementation:
- exact declared `BaboonBirdAI.KillEnemy(bool)` hook;
- one frame later, one-shot `RoundManager.Instance.SpawnedEnemies` registry read;
- candidates restricted to runtime objects assignable to `LethalMin.PikminAI`;
- death release radius = 4.0 m;
- exact declared `LethalMin.PikminAI.FinishTask()` resolution;
- requires exact declaring type;
- zero parameters;
- void return;
- method body present;
- invokes `FinishTask()` for selected Hawk-near Pikmin;
- no `RemoveCurrentTask()` fallback;
- per-Pikmin log marker:
  `[BaboonHawkDeathCleanup] Native FinishTask finalized ...`
- aggregate marker:
  `native-finished X/X`

The already-passing corpse protection remains unchanged.

No:
- continuous Update-driven scan;
- global once-per-second EnemyAI scan;
- broad/inherited LethalMin Harmony scan.

## 7. Exact next step

**Do not build S1.42Q first.**

Import S1.42P using:

**Gale -> Advanced options -> Import all files**

Focused test:
1. note approximate following Pikmin count before the Hawk fight;
2. throw several Pikmin directly onto a living Baboon Hawk;
3. confirm normal latch/attack;
4. let them kill it;
5. verify attackers stop hitting the dead Hawk promptly;
6. verify attackers remain visible and responsive;
7. whistle/regain them;
8. verify they follow and can be reused/thrown normally;
9. compare following count before and after recovery;
10. wait for Dead Baboon Hawk body;
11. verify corpse remains present and Pikmin can carry it to Onion;
12. if another live Hawk exists, verify it does not pick up the corpse;
13. confirm live Hawk -> Pikmin ignore remains intact;
14. confirm no `Leader is null when following`;
15. commit the complete fresh `LogOutput.log` to `RuntimeInbox/Current/`.

Expected S1.42P markers:
- `Resolved exact declared LethalMin.PikminAI.FinishTask()`
- one or more `Native FinishTask finalized ...`
- non-zero `native-finished X/X`

Acceptance additionally requires:
- no sustained `Work state with no task assigned!` loop;
- no sustained dead-Hawk `Hitting enemy with` loop.

## 8. Current controllers

`RuntimeInbox/ACTIVE_BUILD.txt`:
`S1.42P`

`BuildSpecs/current.json`:
- enabled = false;
- build_id = `IDLE_AFTER_S1.42P_BUILD_AWAITING_RUNTIME`;
- base profile = S1.42P;
- base SHA-256 = `11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`.

`RuntimeInbox/Current/`:
only `.gitkeep`.

`RuntimeEvidence/S1.42P/`:
absent, as expected before runtime test.

## 9. After S1.42P PASS

Only after the focused gate passes:
1. disable/remove temporary EnemyIsolation;
2. restore enemy-related config exactly from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve accepted asymmetric Baboon Hawk/Pikmin rules and corpse behavior;
5. runtime-test restored normal gameplay;
6. specifically monitor historical BCMER `Door System: ERROR` / ship-door behavior;
7. document restored normal state;
8. only then consider repository structural migration/cleanup.

## 10. Critical do-not-regress rules

Do not repeat without new evidence:
- S1.42D broad/inherited LethalMin reflection/Harmony scan -> startup crash;
- inherited JetpackItem.Start patch resolving GrabbableObject.Start;
- S1.42E parameterless SpawnableEnemyWithRarity construction -> freezes;
- S1.42F continuous/global EnemyAI scan -> routed moon freezes;
- direct RemoveCurrentTask as Hawk-death finalizer -> broken Work state;
- guessed TaskFinished() method name -> method absent;
- CodeRebirthLib reintroduction;
- silent BCMER 2.0.0 upgrade;
- guessing unknown Enemy PowerLevels;
- treating S1.42I or S1.42K as runtime evidence (both built, never runtime-tested).

Keep Coroner enabled except the already-targeted Jetpack Update detector removal.

## 11. Persistent gameplay/project decisions

Retain:
- Malfunctions disabled;
- SCP999 disabled;
- Observer disabled;
- Don't Touch Me disabled;
- AJB Keep Hangar Ship Door Closed disabled while local failsafe exists;
- Ogopogo disabled;
- Vermin disabled;
- Leaf Boy on LethalMin Attack Blacklist;
- Autonomous Crane cannot kill Pikmin/Puffmin;
- recharge-station full-heal intent;
- Old Bird Resonance retained;
- Mirage recording retention retained;
- no natural CodeRebirth Coin / Crisp Dollar Bill / Wallet;
- no natural Flash Turret;
- LethalModDataLib 1.2.2 null-plugin guard retained;
- SpawnCycleFixes 1.2.2 active;
- interior long-term invariant: equal effective selection probability for every registered interior where technically safe.

## 12. Deferred non-functional repository drift

Do not clean during the open runtime gate:
- `Current/02_TECHNICAL_BASELINE.md` still contains older "current" wording;
- untouched historical comments/strings in `Patches/S139CompatibilityFixes/Plugin.cs` retain S1.42J-era "two-way zero-interaction" wording.

Actual S1.42P code path and newest canonical docs are authoritative.

Deferred structural plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

No destructive Git history rewrite, filter-repo/BFG, Git LFS migration, or external-storage migration without explicit user approval.

## 13. Read order for next chat

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/56_HANDOVER_S1.42P_TO_NEXT_FINAL.md`
3. `Current/57_REPOSITORY_HANDOVER_AUDIT_S1.42P.md`
4. `Current/Projektstatus_S1.42P.json`
5. `Current/54_S1.42O_NO_CLEANUP_FINISHTASK_ANALYSIS.md`
6. `Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`
7. `Current/00_CURRENT_STATE.md`
8. `Current/01_HANDOVER_CORE.md`
9. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
10. `Current/VERIFIKATION_S1.42P.txt`
11. `Current/SHA256SUMS_S1.42P.txt`
12. `Current/Aktive_Modliste_S1.42P.txt`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`
15. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
16. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
17. `Current/02_TECHNICAL_BASELINE.md`
18. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## 14. Deletion decision

**No repository files were deleted during this handover.**

Reason:
No currently identified file/evidence is certain to be both obsolete and devoid of future diagnostic/documentary value. Prefer archive over delete when cleanup is eventually performed.
