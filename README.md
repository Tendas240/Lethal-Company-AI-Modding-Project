# Lethal Company AI Modding Project

## Current state

**Last fully accepted gameplay baseline:** S1.41

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

**Most recent valid runtime evidence:** S1.42H

`RuntimeEvidence/S1.42H/20260903T125734Z/`

Log SHA-256:
`81ed064ce97d25f250d6fba1585055baef8ce801cd0f13626d074bf4fef71029`

S1.42H confirmed:
- startup/exact common GrabPikmin hook PASS;
- isolated enemy spawning PASS;
- in-game `Enemies` output works per user observation;
- Puffer smoke -> Pikmin PASS;
- Baboon Hawk + invincible Pikmin FAIL because the enemy-side hold/re-grab loop persisted;
- direct Thumper/Crawler <-> Pikmin contact was not validated.

S1.42I:
- built successfully;
- **never runtime-tested**;
- superseded before test because the user selected a stronger gameplay rule.

**Binding rule from S1.42J onward:**
Baboon Hawks and Pikmin must not interact in either direction.

**Latest built test candidate:** S1.42J

`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

SHA-256:
`736d7a3b495e124d2469e392b9956c0c3a381a6ce0502baee30d05fabb346cb7`

Compatibility plugin:
- version **1.3.7**
- DLL SHA-256 `7a810d4164394146d64fea2fec300591f4647c9e1b9de834bce4cd1a726e63f2`

S1.42J:
- disables the exact `LethalMin.BaboonBirdPikminEnemy` adapter on spawned Baboon Hawks;
- directly blocks its known declared `BitePikmin`;
- blocks Baboon Hawk-owned common `GrabPikmin` as a final failsafe for all Pikmin;
- adds exact runtime enemy name `Baboon hawk` to LethalMin's Pikmin `Attack Blacklist`;
- retains Thumper/Crawler zero interaction and the accepted Puffer guard.

Build verification:
- GitHub Actions success;
- 0 warnings / 0 errors;
- 331 archive members;
- 330 readable snapshot files;
- changed members only: LethalMin config + compatibility DLL + `export.r2x`;
- no added members;
- 188 packages total / 182 enabled / 6 disabled;
- BCMER 1.71.0 remains disabled.

**Current next gate:** runtime-test S1.42J. Do not build S1.42K first.

Primary acceptance:
- Baboon Hawks ignore Pikmin instead of chasing/biting/grabbing/holding them;
- Pikmin do not attack/latch Baboon Hawks;
- the exact adapter-disable marker appears;
- direct Thumper/Crawler <-> Pikmin zero interaction is finally validated.

After the isolated enemy stage passes:
- remove/disable temporary EnemyIsolation;
- restore the full normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0.

Game: **Lethal Company V81**

## Critical import requirement

Profiles containing the project-local compatibility DLL must be imported in Gale with:

**Advanced options -> Import all files**

Expected general marker:

`S1.39 Compatibility Fixes loaded.`

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/36_HANDOVER_S1.42J_TO_NEXT.md`
3. `Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`
4. `Current/33_S1.42J_BABOON_HAWK_ZERO_INTERACTION_BUILD.md`
5. `Current/32_S1.42H_RUNTIME_ANALYSIS_AND_S1.42I_BUILD.md`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/Projektstatus_S1.42J.json`
10. `Current/VERIFIKATION_S1.42J.txt`
11. `Current/SHA256SUMS_S1.42J.txt`
12. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
13. `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md`
14. `Current/02_TECHNICAL_BASELINE.md`
15. `Current/18_JUIJUI_LEGACY_REFERENCE.md`
16. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
17. `Current/03_PROJECT_CHRONOLOGY.md`
18. `ProfileSources/S1.42J/`
19. `BuildSpecs/current.json`
20. `RuntimeInbox/ACTIVE_BUILD.txt`
21. `Current/NEXT_CHAT_START_PROMPT_S1.42J.txt`

S1.42H/S1.42I and earlier handovers remain historical/diagnostic evidence. Newer confirmed information always overrides older handover instructions.

Repository-maintenance note:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt` records the recommended later repository-architecture migration. It is intentionally deferred until the active critical runtime/build gate is evaluated and documented; it must not replace the immediate S1.42J runtime test.

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

- Thumper/Crawler and Pikmin must not interact in either direction.
- Baboon Hawks and Pikmin must not interact in either direction.
- Puffer smoke/attack must not affect Pikmin.
- Preserve intended interactions for other enemies; do not globally blacklist every enemy.

### Functional Microwave

Target:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

### Jetpack

Historical juijui primary config evidence:
- `JetpackBatteryUsage = 140`
- source: `References/LegacyProfiles/juijui/Extracted/BepInEx/config/dev.alexanderdiaz.biggerbattery.cfg`

Caveat: the final historical export no longer contains Bigger Battery and its DLL is absent, so 140 is the strongest intended/configured historical target rather than proof of final-export runtime activation.

Current S1.42J retained target:
- ButteRyBalance `Reduce Battery = false`;
- project-local compatibility code targets the loaded Jetpack Item asset at 140 seconds;
- `JetpackFixes MidAirExplosions = Off`;
- sustained/high-speed normal boost use must not self-explode the Jetpack.

### Current engineering priority

First: **runtime-test S1.42J. Do not build S1.42K first.**

Primary acceptance:
- Main Menu/host succeeds;
- routed-moon periodic freezes remain gone;
- target enemies still populate and appear in `Enemies`;
- Baboon Hawks completely ignore Pikmin instead of targeting/chasing/biting/grabbing/holding them;
- Pikmin do not attack/latch Baboon Hawks;
- the S1.42J Baboon adapter-disable marker appears;
- direct Thumper/Crawler <-> Pikmin zero interaction is finally validated;
- Puffer -> Pikmin is already accepted from S1.42H and needs only an optional spot-check.

BCMER 1.71.0 is already disabled inside S1.42J. Do not manually alter package states or configs.

After the isolated enemy stage passes:
- remove/disable temporary EnemyIsolation;
- restore the full normal enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0.

## Build state

`BuildSpecs/current.json` is disabled and idle:

`IDLE_AFTER_S1.42J_BUILD_AWAITING_RUNTIME`

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42J`

Do not create S1.42K before S1.42J runtime evidence is evaluated.

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

The highest active engineering priority is the S1.42J isolated runtime gate: validate Baboon Hawk <-> Pikmin and Thumper/Crawler <-> Pikmin zero interaction before restoring normal enemies and BCMER.


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
