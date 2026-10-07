# 31 — HANDOVER S1.42H TO NEXT CHAT

**Date:** 2026-09-03  
**Game:** Lethal Company V81  
**Repository:** https://github.com/Tendas240/Lethal-Company-AI-Modding-Project

## Canonical state

Last fully accepted gameplay baseline:

**S1.41**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Latest built candidate:

**S1.42H**

`Profiles/LC V1 S1.42H Thumper Grab Guard.r2z`

SHA-256:
`5859e15ce71d8cd71d27e20205640af1f10ff91fe6d4b956d4a7064ac8400e58`

Status:
**built successfully, awaiting first runtime validation.**

Compatibility plugin:
- version **1.3.5**
- DLL SHA-256:
  `d67f8f4bc2012f5b74086eb268fcb191f6990c93041617e9ef35c635ea33f186`

GitHub Actions build:
- success;
- 0 warnings;
- 0 errors;
- 331 archive members;
- 330 readable snapshot files;
- changed existing archive members only:
  - `BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`
  - `export.r2x`;
- no added archive members.

## Most recent valid runtime evidence

Variant:
`S1.42G_BCMER_OFF_RETEST`

Evidence:
`RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`

Log SHA-256:
`ac410c42e8174eb4f01aba1d3b7bf54100454e033ed87659a932f3b7f4a3c87e`

Confirmed:
- routed-moon periodic freezes are resolved;
- isolated enemy spawning works with BCMER disabled;
- four Crawler/Thumper and two Puffer actually spawned;
- Puffer smoke/Pikmin guard activated;
- prior Coroner Jetpack `PlayerController was null` per-frame flood is gone;
- repeated zero-power HangarShipDoor/DoorAudit spam did not reproduce with BCMER disabled;
- Thumper contact still reproduced LethalMin's invalid grabbed-Pikmin state:
  - leader removed;
  - grabbed death timer started;
  - invincibility blocked death;
  - repeated `Leader is null when following` followed.

The earlier oversized S1.42G evidence formerly under:
`RuntimeEvidence/S1.42G/20260903T100914Z/`
was intentionally deleted and must **not** be searched for, restored, or cited.

## Why S1.42H exists

S1.42G's safe state guard only covered four declared LethalMin enemy-adapter methods. The reproduced Thumper path uses the common declared base method:

`LethalMin.PikminAI.GrabPikmin(Transform,float,int)`

S1.42H patches exactly this declared implementation once.

Do **not** reintroduce the S1.42D broad reflection/Harmony scan. S1.42D crashed during startup because inherited/non-declared Pikmin methods were scanned and patched.

## S1.42H behavior

### Thumper / Crawler <-> Pikmin

Binding gameplay rule:
**Thumper/Crawler and Pikmin must not interact in either direction.**

S1.42H:
- keeps `Crawler` in LethalMin's Pikmin Attack Blacklist;
- detects a Crawler/Thumper-owned `GrabPikmin` snap point;
- blocks the grab before leader removal and before the death timer.

Expected runtime marker on contact:

`[ThumperPikminGuard] Blocked Crawler/Thumper -> Pikmin GrabPikmin before leader/grab/death-timer state mutation.`

### Generic non-Thumper invincible-Pikmin recovery

For other enemy grabs:
- allow the intended interaction;
- capture valid Pikmin state before `PikminAI.GrabPikmin`;
- if an invincible Pikmin survives but becomes leader-less, invoke a release path or restore pre-grab state.

Expected startup marker:

`[LethalMinStateGuard] Directly patched declared LethalMin.PikminAI.GrabPikmin(Transform,float,int) exactly once. No inherited/derived PikminAI Harmony scan is used.`

### EnemyIsolation

Temporary diagnostic isolation remains enabled.

Target pools:
- indoor: Crawler/Thumper + Puffer;
- outdoor: Baboon Hawk;
- daytime: no normal enemies;
- Pikmin-family entities preserved where registered.

S1.42H carries forward the late-lifecycle hooks:
- `FinishGeneratingNewLevelClientRpc` postfix;
- `PredictAllOutsideEnemies` prefix;
- `BeginEnemySpawning` prefix.

There is no Update-driven continuous global EnemyAI scene scan.

### BCMER

Exact package:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

S1.42H state:
**disabled inside the profile itself.**

Do not manually disable it again and do not change other package states.

Expected profile manifest:
- 188 total;
- 182 enabled;
- 6 disabled.

After the isolated enemy stage passes:
- disable/remove the temporary EnemyIsolation diagnostic;
- restore full normal enemy configuration from:
  `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0.

BCMER is required for the normal gameplay profile and must not remain disabled after this diagnostic stage.

### Door System: ERROR

The clean BCMER-off retest strongly supports BCMER DoorFailure / `Door System: ERROR` as the source of the prior repeated forced-open zero-power ship-door behavior.

S1.42H carries forward:
- no per-call ship-door stacktrace flood;
- state-change DoorAudit only;
- general anti-lockout failsafe;
- transition-only recognition of the BCMER forced-open zero-power state.

Do not weaken the general anti-lockout failsafe.

A narrow BCMER compatibility adjustment should only be extended if later BCMER-on runtime evidence requires it.

### Puffer

Binding rule:
**Puffer attack/smoke must not affect Pikmin.**

Current config:
`Puffer Can Poison Pikmin = false`

The project-local smoke guard activated successfully in the S1.42G BCMER-off retest. Still perform a visible gameplay check if convenient.

### Functional Microwave

Current:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

User wants Functional Microwaves somewhat less common.

**S1.42H intentionally does not change rarity.**

Do not mix that balancing change into the current isolated enemy runtime gate. Implement later after this stage is accepted.

### Jetpack

Keep:
- ButteRyBalance `Reduce Battery = false`;
- project-local target = 140 seconds;
- JetpackFixes `MidAirExplosions = Off`.

Do not restore obsolete Bigger Battery.

The S1.42G retest confirmed the old Coroner Jetpack null-player flood is gone. Actual ~140-second duration and sustained-use behavior can still receive normal gameplay validation later.

## Exact next action

**No new build. Runtime-test S1.42H first.**

Import:
**Gale -> Advanced options -> Import all files**

Do not modify any package state or config before this test.

Primary runtime test:
1. reach Main Menu and host successfully;
2. route/land on a normal moon;
3. confirm the periodic routed-moon freezes remain gone;
4. use terminal `Enemies` and confirm target enemies are listed/spawn;
5. deliberately let a Thumper/Crawler approach through a Pikmin group;
6. verify the Thumper does not grab Pikmin, remove their leader, start a grabbed death timer, or enter the prior broken interaction;
7. verify Pikmin do not attack/latch onto Crawler;
8. if possible, test Baboon Hawk grab/bite on an invincible Pikmin and verify state recovery;
9. if possible, expose Pikmin to Puffer smoke and verify no effect;
10. exit and upload the complete fresh log to `RuntimeInbox/Current/`.

If a new log is already committed when the next chat starts, evaluate it immediately instead of repeating the test instructions.

## Runtime/build control

`RuntimeInbox/ACTIVE_BUILD.txt`:
`S1.42H`

`BuildSpecs/current.json`:
- disabled;
- `IDLE_AFTER_S1.42H_BUILD_AWAITING_RUNTIME`.

Do not create S1.42I before S1.42H runtime evidence is evaluated.

## Persistent do-not-regress rules

- S1.42D startup-crash reflection strategy must not return.
- BCMER stays pinned to 1.71.0 for normal gameplay.
- full normal enemy state must be restored from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json` after isolation.
- one positive spawn owner per enemy where possible.
- unknown enemy PowerLevels are never guessed.
- Thumper/Crawler <-> Pikmin: no interaction.
- Puffer attack/smoke -> Pikmin: no effect.
- Leaf Boy remains in LethalMin Attack Blacklist.
- Malfunctions disabled.
- SCP999 disabled.
- Observer disabled.
- Don't Touch Me disabled.
- AJB Keep Hangar Ship Door Closed disabled while the local failsafe exists.
- CodeRebirthLib must not return.
- LethalModDataLib remains required for DULL and retains the null-plugin guard.
- Ogopogo disabled.
- Vermin disabled.
- every registered interior should ultimately have equal effective selection probability on every moon where technically safe.
- reduce fog specifically in MelanieMausoleum, not globally.
- Functional Microwave rarity reduction is pending, not part of S1.42H.

## Read-first order for the next chat

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/31_HANDOVER_S1.42H_TO_NEXT.md`
3. `Current/30_S1.42G_BCMER_OFF_RETEST_ANALYSIS_AND_S1.42H_BUILD.md`
4. `Current/00_CURRENT_STATE.md`
5. `Current/01_HANDOVER_CORE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/Projektstatus_S1.42H.json`
8. `Current/VERIFIKATION_S1.42H.txt`
9. `Current/SHA256SUMS_S1.42H.txt`
10. `Current/Aktive_Modliste_S1.42H.txt`
11. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
12. `ProfileSources/S1.42H/`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`

Then inspect historical S1.42G/S1.42D evidence only as needed.
