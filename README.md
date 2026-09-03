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
**S1.42M - partial pass**

`RuntimeEvidence/S1.42M/20260903T163446Z/`

Log SHA-256:
`0639d5cc04aa54f5d7943ef4689e0d705c818871b019287ca1a1cdc2aa2492fb`

Current built candidate:
**S1.42N - Baboon Hawk Death Target Resolver**

`Profiles/LC V1 S1.42N Baboon Hawk Death Target Resolver.r2z`

SHA-256:
`c87d48464a750f87274e2848c44e5e1e24d4f1da087f59a33e2889744ebc13e9`

Compatibility plugin:
**v1.3.9**

## S1.42M runtime result

PASS:
- Pikmin can attack/latch/kill living Baboon Hawks;
- Dead Baboon Hawk body appears;
- Pikmin can carry the body to the Onion;
- living Baboon Hawks ignore the corpse;
- no `Leader is null when following` loop.

FAIL:
- Pikmin attacking the Hawk still disappear when it dies.

Critical log marker:
`[BaboonHawkDeathCleanup] ... released 0/0 latched Pikmin ...`

The exact `LethalMin.PikminAI.RemoveCurrentTask()` method resolved correctly. The failed assumption was target discovery: the attacking Pikmin are not `PikminAI` children of the dying Hawk transform.

## Active S1.42N runtime gate

S1.42N changes only the failed death target resolver.

At Hawk death it performs a **one-shot** pass through `RoundManager.Instance.SpawnedEnemies`, filters runtime `LethalMin.PikminAI` candidates, and calls the exact resolved `RemoveCurrentTask()` for candidates under/near the dying Hawk. It does not restore the failed continuous global scan architecture.

Required result:
1. Pikmin can still attack/latch/kill a living Baboon Hawk.
2. At Hawk death, attacking Pikmin remain visible and usable.
3. The log reports non-zero S1.42N death-release candidates/releases.
4. The Dead Baboon Hawk body still appears.
5. Pikmin can still carry the body to the Onion.
6. Living Hawks still ignore the corpse.
7. Hawk -> Pikmin ignore remains intact.
8. No leader-null loop appears.

Do **not** build a successor first unless S1.42N cannot start.

## Temporary diagnostic state

EnemyIsolation:
**enabled**

BCMER exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

After S1.42N passes:
1. remove/disable EnemyIsolation;
2. restore normal enemy state exactly from the S1.42C restore baseline;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted interaction/corpse rules;
5. runtime-check the restored normal state;
6. only then consider deferred repository maintenance.

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42N`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42N_BUILD_AWAITING_RUNTIME`

Profiles containing the project-local DLL must be imported with Gale:

**Advanced options -> Import all files**

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/Projektstatus_S1.42N.json`
3. `Current/50_S1.42M_DEATH_CLEANUP_PARTIAL_PASS_ANALYSIS.md`
4. `Current/51_S1.42N_BABOON_HAWK_DEATH_TARGET_RESOLVER_BUILD.md`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `BuildSpecs/current.json`
9. `RuntimeInbox/ACTIVE_BUILD.txt`
10. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
11. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
12. `Current/02_TECHNICAL_BASELINE.md`
13. `Current/48_HANDOVER_S1.42M_TO_NEXT_FINAL.md` for predecessor detail
14. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## Critical persistent rules

- Do not reintroduce the S1.42D broad/inherited LethalMin reflection/Harmony scan.
- Do not use continuous Update-driven global EnemyAI scene scans for EnemyIsolation/death cleanup.
- Do not silently upgrade BCMER 1.71.0 to 2.0.0.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not treat S1.42I or S1.42K as runtime evidence; both were built but never runtime-tested.
- Do not let `CodeRebirthLib` return.
- Unknown Enemy PowerLevels must never be guessed.
- Prefer one positive spawn owner per enemy.
- Profiles with the local compatibility DLL require Gale "Import all files".

## Deferred non-functional maintenance

Do not clean this during the open S1.42N runtime gate:
- older "current" wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in untouched historical parts of `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural optimization:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

No destructive Git history rewrite, filter-repo/BFG, Git LFS migration, or external-storage migration without explicit user approval.
