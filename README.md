# Lethal Company AI Modding Project

## Current state

**Last fully accepted gameplay baseline:** S1.41

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

**Latest runtime-tested technical candidate that reached gameplay:** S1.42C

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

**Failed diagnostic candidate:** S1.42D

Startup crashed during the new broad LethalMin reflection/Harmony scan. Do not retest S1.42D.

Evidence:
`RuntimeEvidence/S1.42D/20260903T084247Z/`

**Latest built test candidate:** S1.42E

`Profiles/LC V1 S1.42E Startup Safe Enemy Regression.r2z`

SHA-256:
`4df5d6417aad35ad327b183eb2dd25ecb6bd20382840198f74f0201007d57348`

S1.42E built successfully with 0 compiler warnings/errors and an unchanged 188/183/5 package manifest, but it has **not yet been runtime tested**.

Immediate next gate:
**import S1.42E and confirm the game reaches Main Menu without a startup crash before doing any further build work.**

Game: **Lethal Company V81**

## Critical import requirement

Profiles containing the project-local compatibility DLL must be imported in Gale with:

**Advanced options -> Import all files**

Expected general marker:

`S1.39 Compatibility Fixes loaded.`

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/01_HANDOVER_CORE.md`
4. `Current/22_HANDOVER_S1.42E_TO_NEXT.md`
5. `Current/21_S1.42D_CRASH_S1.42E_HOTFIX.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
8. `Current/06_RECENT_WORK_S1.42D-S1.42E.md`
9. `Current/18_JUIJUI_LEGACY_REFERENCE.md`
10. `Current/15_RUNTIME_EVIDENCE_S1.42C.md`
11. `Current/14_RUNTIME_EVIDENCE_S1.42B_LMDL_PIKMIN.md`
12. `Current/13_RUNTIME_EVIDENCE_S1.42A_INTERIORS.md`
13. `Current/02_TECHNICAL_BASELINE.md`
14. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
15. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
16. `Current/03_PROJECT_CHRONOLOGY.md`
17. `Current/Projektstatus_S1.42E.json`
18. `Current/Aktive_Modliste_S1.42E.txt`
19. `Current/VERIFIKATION_S1.42E.txt`
20. `Current/DATEIINVENTAR_S1.42E.txt`
21. `Current/SHA256SUMS_S1.42E.txt`
22. `ProfileSources/S1.42E/`
23. `BuildSpecs/current.json`
24. `RuntimeInbox/ACTIVE_BUILD.txt`

Then inspect `Profiles/`, `RuntimeEvidence/`, `Patches/`, `References/`, `Logs/`, and `Archive/` only as required by the task.

## Recent technical progression

### S1.42A — interior config-generation seed

Profile:
`Profiles/LC V1 S1.42A Interior Config Seed.r2z`

SHA-256:
`70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

Result:
- eight requested interior packages plus required LethalModDataLib 1.2.2 added;
- 188 total / 183 enabled / 5 disabled packages;
- runtime generated real configs and registered 52 dungeon flows total, 26 more than S1.41;
- exact CullFactory IDs discovered: `junkrooms`, `shatteredrooms`;
- Mausoleum generated on Offense and was much too foggy;
- LethalModDataLib initialization NRE discovered.

### S1.42B — LethalModDataLib guard

Profile:
`Profiles/LC V1 S1.42B LMDL NRE Guard.r2z`

SHA-256:
`8523754926e3f67c0ccef5aee976cbe72ab976f997876c59b51fedcfb293befe`

Runtime confirmed:
- offending null Chainloader entry: `MW.MagicWesleyInteriors`;
- project-local guard skipped exactly that null instance;
- `ModDataHandler initialised!`;
- moddata load/save succeeded.

**The S1.42A LethalModDataLib initialization NRE is resolved.**

### S1.42C — Pikmin enemy guards

Profile:
`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

Runtime evidence:
`RuntimeEvidence/S1.42C/20260902T235238Z/`

Result:
- LMDL fix remains healthy;
- Puffer guard registered, but no Puffer spawned -> not yet runtime-validated;
- Crawler/Thumper spawned, but there was no deliberate interaction test -> total Thumper/Pikmin noninteraction still not fully validated;
- a Baboon Hawk bit a Bulbmin and reproduced the same repeated `Leader is null when following` state.

Important new conclusion:
**the broken leader/follow state is a generic LethalMin enemy-grab/bite + Invincible-Pikmin interaction, not a Thumper-only issue.**

## Binding user decisions

### Interiors

Every registered interior should have the same effective selection probability as every other interior **on every moon**, including interiors added in future.

Project target:
- common Weight 100 per interior/moon pairing where technically supported;
- package defaults/theme rarity are not desired;
- hard author blocks are compatibility questions, not desired balancing exceptions.

### Mausoleum

Reduce fog specifically inside `MelanieMausoleum`. Do not globally reduce fog in all interiors.

### BCMER

Pin exact:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Do not silently upgrade to 2.0.0.

Carry forward ownership guards:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

BCMER rain-event routes stay disabled:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy remains allowed.

New EventType target:
- Insane 12.5%
- VeryBad 12.5%
- Bad 12.5%
- Neutral 12.5%
- Good 12.5%
- VeryGood 12.5%
- Rare 12.5%
- Remove 12.5%

Keep `Use custom weights? = false`.

Use constant EventType scale:
`12.5, 0, 12.5, 12.5`

for all eight categories.

### Pikmin-specific

- Thumper/Crawler and Pikmin should not interact in either direction.
- Puffer smoke/attack must not affect Pikmin.
- Do not solve the new general bite/grab bug by blindly blacklisting every enemy. Prefer a generic state repair.

### Functional Microwave

Target:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

### Jetpack

Historical juijui primary config evidence:
- `JetpackBatteryUsage = 140`
- source: `References/LegacyProfiles/juijui/Extracted/BepInEx/config/dev.alexanderdiaz.biggerbattery.cfg`

Caveat: the final historical export no longer contains Bigger Battery and its DLL is absent, so 140 is the strongest intended/configured historical target rather than proof of final-export runtime activation.

S1.42E target:
- ButteRyBalance `Reduce Battery = false`;
- project-local compatibility code targets the loaded Jetpack Item asset at 140 seconds;
- `JetpackFixes MidAirExplosions = Off`;
- sustained/high-speed normal boost use must not self-explode the Jetpack.

### Current engineering priority

First: **runtime-test S1.42E startup.**

S1.42D failed before a usable Main Menu because the v1.3.0 broad LethalMin patch scan targeted inherited/non-declared methods.

S1.42E v1.3.1 narrows the scan to declared `*PikminEnemy` interaction methods only.

If S1.42E reaches Main Menu, then validate the generic LethalMin state repair, isolated Thumper/Puffer/Baboon Hawk behavior, Jetpack and Microwave.



First:
**repair the generic LethalMin enemy-grab/bite + Invincible-Pikmin leader/follow state.**

Confirmed failure sequence in S1.42C:
- enemy bites/grabs Pikmin;
- leader is removed;
- death timer starts;
- invincibility prevents final death;
- Pikmin remains in invalid follow state;
- repeated `Leader is null when following` errors.

Specific Thumper/Puffer guards remain retained and require targeted validation when encountered.

## Build state

`BuildSpecs/current.json` is disabled and idle:

`IDLE_AFTER_S1.42E_BUILD_AWAITING_RUNTIME`

Do not rebuild or create another candidate before S1.42E runtime evidence is evaluated.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42E`

## Repository-first automation

GitHub is the canonical build and handover workspace.

Binding policy:
`Current/09_REPOSITORY_FIRST_AUTOMATION.md`

Use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/<build_id>/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`

Do not require a local repository clone or local PowerShell profile-build scripts while the required base exists in GitHub.

## Persistent decisions

- Malfunctions disabled until explicit user request.
- ProjectSCP-SCP999 disabled.
- Observer disabled.
- Don't Touch Me disabled.
- AJB Keep Hangar Ship Door Closed disabled while local failsafe is active.
- CodeRebirthLib must not return.
- LethalModDataLib remains installed for DULL and must retain the confirmed null-instance guard.
- Unknown Enemy PowerLevels must never be guessed.
- Leaf Boy remains on LethalMin Attack Blacklist.
- S1.29D is diagnostic only and never a gameplay base.
- Ogopogo disabled.
- Vermin disabled.

## Priority rule

Chronologically newer confirmed information overrides older assumptions. Runtime evidence overrides config/package assumptions. `Archive/` is historical reference material and must not override current machine-readable files unless explicitly referenced.

## Historical juijui reference profile

The original historical `juijui.r2z` profile is a primary project reference because the project was originally intended to reproduce its mod constellation/configuration as closely as reasonably possible on modern Lethal Company.

Canonical reference path:
`References/LegacyProfiles/juijui/juijui.r2z`

Detailed handling:
- `Current/18_JUIJUI_LEGACY_REFERENCE.md`
- `References/LegacyProfiles/juijui/README.md`
- `References/juijui_Referenzwerte.txt`

juijui is a historical target/reference, **not** a current build base. Modern game-version, maintenance and compatibility constraints remain authoritative.

The binary is committed and repository-first indexed. The historical Jetpack config evidence has been recovered as `JetpackBatteryUsage = 140`. Do not revert to the old unevidenced 50-second fallback.

The highest active engineering priority remains the generic LethalMin enemy-grab/bite + invincible-Pikmin leader/follow-state repair confirmed in S1.42C.


### S1.42D / S1.42E — isolated enemy regression

S1.42D introduced the focused enemy isolation and generic LethalMin recovery attempt but failed startup during an over-broad Harmony scan.

S1.42E is the startup-safe hotfix:
- compatibility plugin v1.3.1;
- only declared `BitePikmin`, `GrabPikmin`, `GrabPikminWithTongue` on `*PikminEnemy` adapter types;
- no RPC wrappers or generic PikminAI/PikminItem Harmony patching;
- no inherited GrabbableObject.Start Jetpack patch;
- temporary enemy isolation still enabled: indoor Crawler/Puffer, outdoor Baboon Hawk;
- full normal enemy restore source remains `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`.

See `Current/22_HANDOVER_S1.42E_TO_NEXT.md`.
