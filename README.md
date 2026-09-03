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

Current built candidate:
**S1.42M - Baboon Hawk Death Cleanup**

`Profiles/LC V1 S1.42M Baboon Hawk Death Cleanup.r2z`

SHA-256:
`9e0172e7ce8fef8b961f39466e6bdf18f8498e594fee850b2cc0ceaa4088d5c7`

Compatibility plugin:
- v1.3.8
- DLL SHA-256 `47fff0272b00ce776150c203eb65710216eba4390f5f5864fdbffec686692adf`

Latest valid runtime evidence is still S1.42L:
`RuntimeEvidence/S1.42L/20260903T155132Z/`

Log SHA-256:
`812523f8c838b9f76af4a215171755734aa53c556af7bdeeef46a27a43239d10`

## Closed/PASS from the isolated enemy stage

- **Thumper/Crawler -> Pikmin:** broken GrabPikmin/leader/death-timer state blocked.
- **Pikmin -> Thumper/Crawler:** normal attack/latch works.
- **Puffer -> Pikmin:** no effect.
- **Jetpack:** accepted at ~140 seconds; MidAirExplosions Off.
- **Baboon Hawk -> Pikmin:** target/chase/bite/grab/hold protection works.
- **Pikmin -> living Baboon Hawk:** normal latch/attack works and Pikmin can kill the Hawk.
- latest S1.42L run had **0** `Leader is null when following`.

Visible Thumper snapping remains accepted harmless cosmetic behavior.

## Active S1.42M runtime gate

S1.42L exposed a post-kill compatibility problem:
latched Pikmin remained on the dead original Hawk target. SellBodiesFixed later created the carryable `BaboonHawkBody(Clone)` and moved the original enemy transform away, so the attacking Pikmin disappeared with the stale target. Living Hawks could also pick up the new corpse as scrap.

S1.42M must validate:

1. Pikmin can still attack/latch a living Baboon Hawk.
2. When they kill it, those Pikmin detach and remain visible/usable.
3. After the SellBodies delay, the Dead Baboon Hawk body remains present.
4. Players and Pikmin can still carry the corpse.
5. Pikmin can carry the corpse toward the Onion.
6. Living Baboon Hawks do not pick up the corpse.
7. Hawk -> Pikmin ignore remains intact.
8. No leader-null loop appears.

Do **not** build a successor first.

## Temporary diagnostic state

EnemyIsolation:
**enabled**

BCMER exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`
**disabled**

Restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

After S1.42M passes:
1. remove/disable EnemyIsolation;
2. restore normal enemy state from the S1.42C restore baseline;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted interaction/corpse rules;
5. runtime-check the normal state;
6. only then consider deferred repository maintenance.

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42M`

`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42M_BUILD_AWAITING_RUNTIME`

Profiles containing the project-local DLL must be imported with Gale:

**Advanced options -> Import all files**

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/Projektstatus_S1.42M.json`
4. `Current/46_S1.42M_BABOON_HAWK_DEATH_CLEANUP_BUILD.md`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/VERIFIKATION_S1.42M.txt`
8. `Current/SHA256SUMS_S1.42M.txt`
9. `Current/45_HANDOVER_S1.42L_TO_NEXT_FINAL.md` for predecessor context
10. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
11. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
12. `BuildSpecs/current.json`
13. `RuntimeInbox/ACTIVE_BUILD.txt`
14. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## Critical persistent rules

- Do not reintroduce the S1.42D broad/inherited LethalMin reflection/Harmony scan.
- Do not use continuous Update-driven global EnemyAI scene scans for EnemyIsolation.
- Do not silently upgrade BCMER 1.71.0 to 2.0.0.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not treat S1.42I or S1.42K as runtime evidence; both were built but never runtime-tested.
- Do not let `CodeRebirthLib` return.
- Unknown Enemy PowerLevels must never be guessed.
- Prefer one positive spawn owner per enemy.
- Profiles with the local compatibility DLL require Gale "Import all files".

## Deferred non-functional maintenance

Do not clean this during the open S1.42M runtime gate:
- older "current" wording in `Current/02_TECHNICAL_BASELINE.md`;
- stale S1.42J-era comments in untouched parts of `Patches/S139CompatibilityFixes/Plugin.cs`.

Structural optimization:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

No destructive Git history rewrite, filter-repo/BFG, Git LFS migration, or external-storage migration without explicit user approval.
