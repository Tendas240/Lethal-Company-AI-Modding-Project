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

Current built and runtime-tested candidate:
**S1.42L - Pikmin Counterattack Restore**

`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`

SHA-256:
`fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Latest valid runtime evidence:
`RuntimeEvidence/S1.42L/20260903T151817Z/`

Log SHA-256:
`402015463b9ed83a0835a4df8ac7f6298cac662609700715563041e5447885bd`

Runtime verdict:
**PARTIAL PASS - only Pikmin -> Baboon Hawk explicit attack/latch validation remains.**

## Closed/PASS from the current isolated enemy stage

- **Thumper/Crawler -> Pikmin:** broken GrabPikmin/leader/death-timer state is blocked.
- **Pikmin -> Thumper/Crawler:** normal LethalMin attack/latch is restored and user-confirmed.
- **Puffer -> Pikmin:** smoke/attack has no effect.
- **Jetpack:** accepted at approximately 140 seconds; `MidAirExplosions = Off`; old Coroner Jetpack null flood absent.
- **Baboon Hawk -> Pikmin:** exact LethalMin Baboon adapter is disabled; Hawk-side target/chase/bite/grab/hold behavior is blocked.

Accepted cosmetic behavior:
the Thumper may still visibly snap at Pikmin. Pikmin are not held and do not enter a broken state, so this should be ignored unless a future functional regression appears.

## Only remaining active runtime gate

**Pikmin -> Baboon Hawk**

Keep using S1.42L unchanged.

Test:
1. throw Pikmin onto a Baboon Hawk;
2. confirm Pikmin latch/attack normally;
3. confirm the Hawk still ignores Pikmin from its own AI side;
4. confirm no `Leader is null when following` loop;
5. upload the complete fresh log to `RuntimeInbox/Current/`.

Do **not** build a successor first.

Current router:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42L`

Current build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42L_BUILD_AWAITING_RUNTIME`

## Temporary diagnostic state

EnemyIsolation:
**enabled**

BCMER:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`
**disabled**

Diagnostic allowlist:
- indoor: Crawler/Thumper + Puffer
- outdoor: Baboon Hawk
- daytime: none
- Pikmin-family entities retained

After the last S1.42L direction passes:
1. remove/disable EnemyIsolation;
2. restore normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
3. re-enable exact BCMER 1.71.0;
4. preserve all accepted asymmetric Pikmin interaction rules;
5. document the resulting normal-enemy/BCMER state;
6. only then consider the deferred repository optimization.

## Critical import requirement

Profiles containing the project-local compatibility DLL must be imported in Gale using:

**Advanced options -> Import all files**

Expected plugin marker:

`S1.39 Compatibility Fixes loaded.`

## ChatGPT - read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/45_HANDOVER_S1.42L_TO_NEXT_FINAL.md`
3. `Current/Projektstatus_S1.42L.json`
4. `Current/43_S1.42L_RUNTIME_ANALYSIS_THUMPER_CLOSED.md`
5. `Current/41_S1.42L_PIKMIN_COUNTERATTACK_RESTORE_BUILD.md`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/VERIFIKATION_S1.42L.txt`
10. `Current/SHA256SUMS_S1.42L.txt`
11. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
12. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
13. `Current/02_TECHNICAL_BASELINE.md`
14. `Current/03_PROJECT_CHRONOLOGY.md`
15. `BuildSpecs/current.json`
16. `RuntimeInbox/ACTIVE_BUILD.txt`
17. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

## Repository-first workflow

Canonical build/runtime control:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`
- `Patches/`

Do not require a local repository clone or local PowerShell build while the required base artifacts and GitHub build infrastructure exist.

## Critical persistent rules

- Do not reintroduce the S1.42D broad/inherited LethalMin reflection/Harmony scan; it caused startup crash.
- Do not use continuous Update-driven global EnemyAI scans for EnemyIsolation.
- Do not upgrade BCMER 1.71.0 to 2.0.0 without explicit user decision.
- Do not remove `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.
- Do not treat S1.42I or S1.42K as runtime evidence; both were built but never runtime-tested.
- Do not restore/cite the intentionally deleted oversized S1.42G evidence path.
- Do not let `CodeRebirthLib` return.
- Unknown Enemy PowerLevels must never be guessed.
- Prefer one positive spawn owner per enemy.
- Historical evidence, failed approaches, restore baselines and RuntimeEvidence remain preserved.

## Deferred repository optimization

Plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Status:
**DEFERRED_UNTIL_ACTIVE_GATE_COMPLETE**

Do not begin structural migration until the remaining Pikmin -> Baboon Hawk gate has been evaluated and the resulting normal-enemy/BCMER state has been documented.
