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

Tested candidate:
**S1.42P - Baboon Hawk Exact FinishTask Recovery**

`Profiles/LC V1 S1.42P Baboon Hawk Exact FinishTask Recovery.r2z`

SHA-256:
`11709548a924ddb3a174813eeecf23daf7aa6512267bfac1ab3b48b3b048fdc5`

Compatibility plugin:
**v1.3.11**

## S1.42P finding

The user observed a following-count drop from **20 to 18** after the Baboon Hawk fight.

The runtime log confirms exactly the same state:
- 20 Yellow Pikmin leader-assigned before the fight;
- 18 recovered before teardown;
- missing: `Yellow Pikmin_hcRGph` and `Yellow Pikmin_ruCpzY`.

`PikminAI.FinishTask()` itself is runtime-proven correct and executed successfully.

S1.42P nevertheless fails for two reasons:
1. the 4.0 m proximity selector missed real attacker `ruCpzY`, which continued hitting the dead Hawk for ~84.565 s;
2. FinishTask-finalized Pikmin immediately rediscovered the already-dead Hawk and could start a new `AttackEnemy` task.

Corpse behavior remains PASS: Pikmin carried the Dead Baboon Hawk to Onion, and living Hawks ignored the corpse.

Full analysis:
`Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`

## Next technical stage

S1.42Q should:
- retain exact native `LethalMin.PikminAI.FinishTask()`;
- replace proximity-only attacker selection with exact/direct dying-Hawk target identity;
- prevent already-dead Baboon Hawks from being selected as future Pikmin attack targets.

Do not merely widen the radius.
Do not restore direct `RemoveCurrentTask()`.
Do not restore normal enemies or BCMER yet.

## Temporary diagnostic state

EnemyIsolation:
**enabled**

BCMER exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42P`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42P_RUNTIME_FAIL_AWAITING_SUCCESSOR_DESIGN`

The runtime pointer stays on S1.42P until a successor is actually built.

Profiles containing the project-local DLL must be imported with Gale:

**Advanced options -> Import all files**

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/58_S1.42P_RUNTIME_TWO_PIKMIN_LOSS_REACQUIRE_ANALYSIS.md`
3. `Current/Projektstatus_S1.42P.json`
4. `Current/00_CURRENT_STATE.md`
5. `Current/01_HANDOVER_CORE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/55_S1.42P_BABOON_HAWK_EXACT_FINISHTASK_BUILD.md`
8. `Current/54_S1.42O_NO_CLEANUP_FINISHTASK_ANALYSIS.md`
9. `Current/VERIFIKATION_S1.42P.txt`
10. `Current/SHA256SUMS_S1.42P.txt`
11. `Current/Aktive_Modliste_S1.42P.txt`
12. `BuildSpecs/current.json`
13. `RuntimeInbox/ACTIVE_BUILD.txt`
14. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
15. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
16. `Current/56_HANDOVER_S1.42P_TO_NEXT_FINAL.md`
17. `Current/57_REPOSITORY_HANDOVER_AUDIT_S1.42P.md`
18. `Current/02_TECHNICAL_BASELINE.md`
19. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

The S1.42P final handover/audit files 56/57 describe the state **before** S1.42P was runtime-tested. Newer runtime evidence and Current files supersede their "awaiting runtime" wording.

## Critical persistent rules

- Do not reintroduce broad/inherited LethalMin reflection/Harmony scanning.
- Do not use continuous Update-driven global EnemyAI scans for this death cleanup.
- Do not restore direct low-level RemoveCurrentTask as the Hawk-death finalizer.
- Use runtime-confirmed `FinishTask()`; do not guess `TaskFinished()` again.
- Do not treat a fixed proximity radius as complete Hawk-attacker identity.
- Do not silently upgrade BCMER 1.71.0 to 2.0.0.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not let `CodeRebirthLib` return.
- Unknown Enemy PowerLevels must never be guessed.
- Profiles with the local compatibility DLL require Gale "Import all files".

## Deferred maintenance

General cleanup remains deferred while the enemy-regression chain is open:
- older "current" wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in untouched historical parts of `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural optimization:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
