# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current state

Game:
**Lethal Company V81**

Last fully accepted gameplay baseline:
**S1.41 - BCMER Reactivation**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Latest valid runtime evidence:
**S1.42P - PARTIAL / FAIL**

`RuntimeEvidence/S1.42P/20260903T181706Z/`

Log SHA-256:
`d656095fb874a415a1bd2377c0411339d3d6eb002dce4ec3f6216e879294127f`

S1.42P confirmed the user's exact **20 -> 18** follower loss after the Baboon Hawk fight.

## Current built candidate

**S1.42Q - LethalMin Native Minimal Rollback**

`Profiles/LC V1 S1.42Q LethalMin Native Minimal Rollback.r2z`

SHA-256:
`50a8488a7d5f5c0a318db2557895d7029de3cfa1c0d704498bb9d90eaa481cb1`

Git blob SHA:
`9e1beec739c193c95e936a56fefb060a84577559`

Compatibility plugin:
**v1.3.12**

Embedded DLL SHA-256:
`f6a4e7b060af6a779da1c92236b2ce63d1bd5d890a21c9492517e568a9aaac45`

Build verification:
- GitHub Actions Build #52: **SUCCESS**
- generated commit: `bd6e1ca023921e5fecb14e301e9c24cf73cb4aea`
- idle-guard Build #53: **SUCCESS**
- 331 archive members
- 330 readable snapshot files
- no added profile members

Changed existing profile members only:
1. `BepInEx/config/NoteBoxz.LethalMin.cfg`
2. `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`
3. `export.r2x`

## S1.42Q architecture

Normal LethalMin ownership has been restored as far as possible.

Native LethalMin owns:
- Pikmin -> living enemy targeting/latch/attack;
- enemy-death task completion;
- Pikmin -> dead enemy body carrying;
- Onion delivery.

Project-local code now keeps only proven narrow Enemy -> Pikmin protection and unrelated compatibility shims.

Removed:
- `BaboonHawkDeathCleanup`;
- project-local Hawk-death `PikminAI.FinishTask()`;
- 4.0 m death-release scan;
- delayed post-grab recovery;
- leader/follow/grab state snapshots and reflection restoration.

Kept:
- prevention-only exact `PikminAI.GrabPikmin(Transform,float,int)` prefix for proven Crawler/Thumper and Baboon Hawk Enemy -> Pikmin gaps;
- one-way Baboon Hawk -> Pikmin adapter/bite protection;
- Puffer effect guard;
- CodeRebirth utility-kill Pikmin protection;
- Dead Baboon Hawk corpse `CanGrabScrap` guard;
- unrelated accepted compatibility fixes.

Exact LethalMin config delta from S1.42P:
- `Thumper Bite Limit = 0` -> `3`

That is the **only** LethalMin config change and restores the accepted S1.41 value.

Expected S1.42Q startup marker:

`[LethalMinNativeOwnership]`

Forbidden old runtime marker:

`[BaboonHawkDeathCleanup]`

## Temporary diagnostic state

EnemyIsolation:
**enabled**

BCMER exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Do not restore normal enemies or BCMER before S1.42Q passes.

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Q`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42Q_BUILD_AWAITING_RUNTIME`

Profiles containing the project-local DLL must be imported with Gale:

**Advanced options -> Import all files**

## Exact next step

Do **not** build S1.42R first.

Import S1.42Q and perform the focused Crawler/Thumper + Baboon Hawk + Puffer runtime test.

Record follower counts before and after the fights. Verify that native LethalMin releases Pikmin correctly after enemy death, enemy -> Pikmin protection remains intact, and Dead Baboon Hawk carrying to Onion still works.

Then commit the complete fresh `LogOutput.log` to:

`RuntimeInbox/Current/`

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/59_S1.42Q_MINIMAL_LETHALMIN_NATIVE_ROLLBACK_PLAN.md`
3. `Current/60_S1.42Q_MINIMAL_NATIVE_ROLLBACK_BUILD.md`
4. `Current/Projektstatus_S1.42Q.json`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `Current/VERIFIKATION_S1.42Q.txt`
9. `Current/SHA256SUMS_S1.42Q.txt`
10. `Current/Aktive_Modliste_S1.42Q.txt`
11. `Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`
12. `BuildSpecs/S1.42Q_PLAN.md`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`
15. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
16. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
17. `Current/02_TECHNICAL_BASELINE.md`
18. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Historical S1.42P handover/build files remain evidence but are superseded for current-state decisions by the S1.42Q files above.

## Critical persistent rules

- Do not reintroduce broad/inherited LethalMin reflection/Harmony scanning.
- Do not use continuous Update-driven global EnemyAI scans.
- Do not own normal LethalMin Pikmin -> enemy death/task lifecycle in the compatibility plugin.
- Do not restore direct low-level `RemoveCurrentTask()` or project-local Hawk-death `FinishTask()`.
- Do not add custom Pikmin corpse-carry/Onion logic.
- Prefer native LethalMin config where it is proven effective.
- Prefer blocking unwanted Enemy -> Pikmin behavior before it mutates Pikmin state.
- Do not silently upgrade BCMER 1.71.0 to 2.0.0.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not let `CodeRebirthLib` return.
- Unknown Enemy PowerLevels must never be guessed.
- Profiles with the local compatibility DLL require Gale "Import all files".

## Deferred maintenance

General cleanup remains deferred while the enemy-regression gate is open.

Structural optimization:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
