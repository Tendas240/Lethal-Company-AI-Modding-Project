# 22 — Handover S1.42E to Next Chat

**Handover date:** 2026-09-03  
**Game:** Lethal Company V81

## 1. Canonical state

Last fully accepted gameplay baseline:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Latest runtime-tested technical candidate that reached gameplay:

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Latest built test candidate:

`Profiles/LC V1 S1.42E Startup Safe Enemy Regression.r2z`

SHA-256:
`4df5d6417aad35ad327b183eb2dd25ecb6bd20382840198f74f0201007d57348`

**S1.42E is built successfully but has NOT been runtime tested yet.**

## 2. Immediate next action

Do not build another profile first.

The user must test S1.42E.

Import with:
**Gale -> Advanced options -> Import all files**

First runtime gate:
**Does the game reach the Main Menu without crashing?**

If startup crashes:
- do not continue gameplay testing;
- user uploads full `LogOutput.log` to `RuntimeInbox/Current/`;
- `RuntimeInbox/ACTIVE_BUILD.txt` is already `S1.42E`;
- analyze the first new fatal/startup regression against S1.42D and S1.42C.

If startup succeeds:
1. verify `S1.39 Compatibility Fixes loaded.`;
2. verify a completed marker:
   `[LethalMinStateGuard] Safe generic grab/bite state repair registered on N declared enemy method(s).`
3. verify:
   `[EnemyIsolation] ISOLATED ENEMY TEST MODE ENABLED...`
4. then perform the isolated interaction tests below.

## 3. Why S1.42E exists

S1.42D was built as the first isolated enemy regression candidate but caused a startup crash before a usable Main Menu.

S1.42D:
`Profiles/LC V1 S1.42D Isolated Enemy Regression.r2z`

SHA-256:
`b455bd413a6da4ac059117d8fec667053c96ffeef7e239d9188d6e514d15bd5c`

Crash evidence:
`RuntimeEvidence/S1.42D/20260903T084247Z/`

Log SHA-256:
`55cdbf6904c7d1acb74647c90a79820df9e3a39978cd60ccf4d6e25bc95d4107`

The log reached:
`LethalLevelLoader: Custom Content Processed. Unlocking Main Menu.`

Then the new broad LethalMin reflection/Harmony scan began. HarmonyX repeatedly warned that inherited/non-declared methods were being patched. The log ended during that scan and never printed its completion marker.

**Do not retest S1.42D and do not restore the broad v1.3.0 scan.**

Detailed diagnosis:
`Current/21_S1.42D_CRASH_S1.42E_HOTFIX.md`

## 4. S1.42E compatibility plugin

Project source:
`Patches/S139CompatibilityFixes/Plugin.cs`

Version:
**1.3.1**

Embedded DLL SHA-256:
`caf20c785245396d9f31ff32b556cbe75d64b87a5a676807184093a6cef78eab`

S1.42E narrows the LethalMin patch to:
- types whose name contains `PikminEnemy`;
- `DeclaredOnly` methods;
- only local:
  - `BitePikmin`
  - `GrabPikmin`
  - `GrabPikminWithTongue`
- method must have an implementation body.

It intentionally does NOT patch:
- generated ServerRpc/ClientRpc wrappers;
- generic `PikminAI` methods;
- `PikminItem` methods;
- inherited implementations through derived Pikmin types.

The intended recovery behavior remains:
- capture a valid pre-grab leader/follow/grab state;
- wait beyond LethalMin's grabbed-death window;
- only intervene if the Pikmin survived and lost a previously valid leader;
- prefer a discoverable LethalMin release/save/drop/free method;
- fallback to restoring relevant pre-grab state and parent;
- preserve normal enemy interaction instead of globally blacklisting enemies.

## 5. Isolated enemy test

S1.42E has a **temporary diagnostic enemy isolation** enabled.

Allowed non-Pikmin enemies:
- indoor: Thumper/Crawler
- indoor: Puffer/Spore Lizard
- outdoor: Baboon Hawk
- daytime: none

All normal enemy mods/packages remain enabled. The isolation is runtime-only.

Canonical full-roster restore point:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

After this isolated test passes, the next normal gameplay candidate MUST disable:
`[Diagnostics] Isolated Enemy Regression = false`

and restore/carry forward the full S1.42C enemy configuration exactly.

### Baboon Hawk
Primary generic state-repair reproduction:
- allow a Hawk to bite/grab an invincible Pikmin/Bulbmin;
- Pikmin survives;
- Pikmin must return to a valid leader/follow state;
- no repeated `Leader is null when following` spam.

### Thumper
Binding requirement:
**zero interaction in both directions**.

Carry-forward:
- `Thumper Bite Limit = 0`
- `Crawler` on LethalMin Attack Blacklist.

Validate:
- Thumper does not bite/grab Pikmin;
- Pikmin does not attack/latch onto Thumper.

### Puffer
Binding requirement:
Puffer smoke/attack must not affect Pikmin.

Carry-forward:
- `Puffer Can Poison Pikmin = false`
- project-local Puffer smoke effect-trigger guard.

Validate:
- Pikmin unaffected;
- normal player/Puffer behavior retained;
- Puffer guard runtime marker appears.

## 6. Jetpack in S1.42E

Historical primary reference:
`References/LegacyProfiles/juijui/juijui.r2z`

Historical profile SHA-256:
`ddd10bcec3329c155b3a0a2d74460928b02df147356701fb6cf79ebb5a9f7e00`

Recovered historical config:
`References/LegacyProfiles/juijui/Extracted/BepInEx/config/dev.alexanderdiaz.biggerbattery.cfg`

Value:
`JetpackBatteryUsage = 140`

Evidence caveat:
the final historical `export.r2x` no longer contains Bigger Battery and no corresponding DLL is present. Treat 140 seconds as the strongest historical intended/configured target, not proof the old plugin was active at the final export instant.

Modern S1.42E target:
- ButteRyBalance `Reduce Battery = false`;
- local patch attempts to set the loaded Jetpack Item `batteryUsage` to 140;
- no inherited `GrabbableObject.Start` Harmony patch;
- retry only until the Jetpack Item asset becomes available;
- JetpackFixes `MidAirExplosions = Off`.

Binding user requirement:
**normal/continuous/high-speed boost use must not make the Jetpack self-explode.**

Runtime validation:
- duration approximately 140 seconds;
- sustained/high-speed boosting does not create a mid-air self-explosion;
- collision-with-solid-geometry behavior may remain unless user later requests otherwise.

## 7. Functional Microwave

S1.42E:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

Check subjectively in runtime.

## 8. Existing accepted guards to preserve

Do not regress:
- LethalModDataLib null-instance guard; runtime-proven needed with LMDL 1.2.2;
- offending null Chainloader entry was `MW.MagicWesleyInteriors`;
- CodeRebirth direct Pikmin/Puffmin kill-RPC shield;
- CodeRebirth natural Currency/Flash-Turret suppression from S1.40B;
- ship-door anti-lockout;
- complete EnemyScan output;
- Puffer smoke Pikmin effect-trigger guard;
- Lethal Resonance Old-Bird-only configuration;
- BCMER exact 1.71.0 ownership guards;
- Leaf Boy on LethalMin Attack Blacklist.

## 9. Historical juijui reference

The old juijui profile is now committed and indexed.

Original:
`References/LegacyProfiles/juijui/juijui.r2z`

Readable snapshot:
`References/LegacyProfiles/juijui/Extracted/`

It is a historical primary target/reference, **not** a V81 build base.

Project intent:
approximate the old juijui mod constellation/configuration as closely as technically reasonable while respecting V81, maintained mods, current dependencies/APIs and newer confirmed runtime decisions.

## 10. Broader tuning intentionally deferred until after isolated enemy validation

Do not fold these into the current startup/enemy diagnosis:

### Interiors
Binding design:
every registered interior should have equal effective selection probability on every moon, including future additions.

Pending:
- normalize safely available interiors;
- exact CullFactory exceptions:
  - `junkrooms`
  - `shatteredrooms`
- investigate Shatteredrooms Experimentation/Embrion author restrictions;
- reduce fog only in Melanie Mausoleum.

### BCMER
Keep exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Future target:
all eight EventTypes at fixed global base 12.5%.

Use:
- `Use custom weights? = false`
- every EventType scale `12.5, 0, 12.5, 12.5`

Retain disabled BCMER rain routes:
- Raining
- HeavyRain
- AllWeather
- Hurricane

## 11. Do-not-regress / do-not-reintroduce

- Malfunctions disabled.
- ProjectSCP-SCP999 disabled.
- Observer disabled.
- Don't Touch Me disabled.
- AJB Keep Hangar Ship Door Closed disabled while local failsafe exists.
- CodeRebirthLib hard rule: do not reinstall.
- Gnomes removed.
- FacilityMeltdown removed.
- ASTeam racist Hoarding Bugs replacer removed.
- FearOverhauled removed.
- LethalPlaytime Boxy Boo/Huggy Wuggy/Miss Delight not reactivated on V81.
- Ogopogo disabled.
- Vermin disabled.
- S1.29D diagnostic only, never gameplay base.
- do not globally force Rolling Giant/Shy Guy/Siren Head through LLL; native ownership applies.
- do not globally blacklist all enemies from Pikmin merely to hide the generic grab/bite state bug.
- do not restore S1.42D's broad reflection/Harmony scan.

## 12. Build control state

`BuildSpecs/current.json` is disabled/idle:

`IDLE_AFTER_S1.42E_BUILD_AWAITING_RUNTIME`

Do not rebuild S1.42E before runtime evidence exists.

Repository-first only:
- no local clone needed;
- no PowerShell profile build while required bases exist on GitHub;
- use GitHub Actions for future profile builds.

## 13. Runtime evidence routing

`RuntimeInbox/ACTIVE_BUILD.txt`:
`S1.42E`

User uploads locally produced evidence to:
`RuntimeInbox/Current/`

Runtime ingest then persists it under:
`RuntimeEvidence/S1.42E/<timestamp>/`

Important history:
the first S1.42D crash log was initially misclassified as S1.42C because `ACTIVE_BUILD.txt` was stale. That was corrected; the canonical crash evidence is now under S1.42D.

## 14. Read first in the new chat

1. `README.md`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. **this file**
5. `Current/21_S1.42D_CRASH_S1.42E_HOTFIX.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
8. `Current/06_RECENT_WORK_S1.42D-S1.42E.md`
9. `Current/18_JUIJUI_LEGACY_REFERENCE.md`
10. `Current/15_RUNTIME_EVIDENCE_S1.42C.md`
11. `Current/14_RUNTIME_EVIDENCE_S1.42B_LMDL_PIKMIN.md`
12. `Current/02_TECHNICAL_BASELINE.md`
13. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
14. `Current/Projektstatus_S1.42E.json`
15. `Current/VERIFIKATION_S1.42E.txt`
16. `Current/Aktive_Modliste_S1.42E.txt`
17. `ProfileSources/S1.42E/`
18. `BuildSpecs/current.json`
19. `RuntimeInbox/ACTIVE_BUILD.txt`

## 15. Binding next-chat behavior

The next chat should **not start by redesigning or rebuilding**.

First determine whether the user has already runtime-tested S1.42E.

If no:
tell the user to test S1.42E, with Main Menu startup as the first gate.

If yes:
inspect the newly ingested S1.42E runtime evidence first and decide from evidence whether:
- startup is fixed;
- safe LethalMin patch registration completed;
- enemy isolation works;
- generic Baboon Hawk state recovery works;
- Thumper/Puffer requirements pass;
- Jetpack target works;
- Microwave target works.

Only then plan the next build.
