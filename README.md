# Lethal Company AI Modding Project

## Current state

**Last fully accepted gameplay baseline:** S1.41

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

**Most recent valid runtime evidence:** `S1.42G_BCMER_OFF_RETEST`

`RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`

Log SHA-256:
`ac410c42e8174eb4f01aba1d3b7bf54100454e033ed87659a932f3b7f4a3c87e`

Confirmed by that clean run:
- periodic routed-moon freezes are resolved;
- Crawler/Thumper and Puffer spawn correctly with BCMER disabled;
- Puffer smoke/Pikmin guard activates;
- Coroner's previous per-frame Jetpack `PlayerController was null` flood is gone;
- the repeated zero-power DoorAudit/HangarShipDoor stack flood does not reproduce with BCMER disabled;
- Thumper contact still reproduced LethalMin's invalid invincible-Pikmin grabbed/leader-null state.

**Latest built test candidate:** S1.42H

`Profiles/LC V1 S1.42H Thumper Grab Guard.r2z`

SHA-256:
`5859e15ce71d8cd71d27e20205640af1f10ff91fe6d4b956d4a7064ac8400e58`

Compatibility plugin:
- version **1.3.5**
- DLL SHA-256 `d67f8f4bc2012f5b74086eb268fcb191f6990c93041617e9ef35c635ea33f186`

Build verification:
- GitHub Actions success;
- 0 warnings / 0 errors;
- 331 archive members;
- only the compatibility DLL and `export.r2x` changed against S1.42G.

S1.42H:
- patches exactly the declared `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` implementation once;
- blocks Crawler/Thumper -> Pikmin grabs before leader removal/death timer;
- retains Crawler in LethalMin's Pikmin Attack Blacklist for the reverse direction;
- carries forward the late-lifecycle EnemyIsolation without any continuous global EnemyAI scan;
- contains BCMER 1.71.0 already **disabled** for this final isolated enemy test;
- leaves Functional Microwave rarity unchanged.

**Current next gate:** runtime-test S1.42H. Do not build S1.42I first.

After the isolated enemy stage passes:
- remove/disable the temporary EnemyIsolation diagnostic;
- restore the full normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0.

The old oversized S1.42G ingest formerly under `RuntimeEvidence/S1.42G/20260903T100914Z/` was intentionally deleted and must not be restored or cited.

Game: **Lethal Company V81**

## Critical import requirement

Profiles containing the project-local compatibility DLL must be imported in Gale with:

**Advanced options -> Import all files**

Expected general marker:

`S1.39 Compatibility Fixes loaded.`

## ChatGPT — read first

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
11. `Current/README_Handover_S1.42H.txt`
12. `Current/DATEIINVENTAR_S1.42H.txt`
13. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
14. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
15. `Current/02_TECHNICAL_BASELINE.md`
16. `Current/18_JUIJUI_LEGACY_REFERENCE.md`
17. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
18. `Current/03_PROJECT_CHRONOLOGY.md`
19. `ProfileSources/S1.42H/`
20. `BuildSpecs/current.json`
21. `RuntimeInbox/ACTIVE_BUILD.txt`

Historical S1.42G/S1.42D handovers and evidence are read only when needed for diagnosis. Newer confirmed information always overrides older handover instructions.

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

Current S1.42H retained target:
- ButteRyBalance `Reduce Battery = false`;
- project-local compatibility code targets the loaded Jetpack Item asset at 140 seconds;
- `JetpackFixes MidAirExplosions = Off`;
- sustained/high-speed normal boost use must not self-explode the Jetpack.

### Current engineering priority

First: **runtime-test S1.42H.**

Primary acceptance:
- Main Menu/host succeeds;
- routed-moon periodic freezes remain gone;
- target enemies still populate and appear in `Enemies`;
- Thumper/Crawler contact with Pikmin triggers the new zero-interaction guard before leader removal/death timer;
- no new Thumper-caused `Leader is null when following` loop;
- Baboon Hawk generic recovery and Puffer smoke immunity are checked if conveniently encountered.

BCMER 1.71.0 is already disabled inside S1.42H. Do not manually alter package states or configs.

After the isolated enemy stage passes:
- remove/disable temporary EnemyIsolation;
- restore the full normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0.

## Build state

`BuildSpecs/current.json` is disabled and idle:

`IDLE_AFTER_S1.42H_BUILD_AWAITING_RUNTIME`

Do not create S1.42I before S1.42H runtime evidence is evaluated.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42H`

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
