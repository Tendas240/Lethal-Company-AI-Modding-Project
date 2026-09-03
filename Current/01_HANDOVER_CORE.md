# 01 — Handover Core

## Binding state

### Accepted gameplay baseline
- build: **S1.41**
- profile: `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`
- SHA-256: `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`
- status: runtime accepted

### Latest runtime-tested technical candidate
- build: **S1.42C**
- profile: `Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`
- SHA-256: `22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`
- manifest: 188 total / 183 enabled / 5 disabled
- status: runtime-tested technical descendant, not final gameplay acceptance

Game: **Lethal Company V81**

## Critical lineage

### S1.39 -> S1.40B
The cumulative local compatibility plugin was established and CodeRebirth/DawnLib Currency + Flash Turret suppression was eventually fixed by opening the per-content editing gates.

S1.40B accepted solution must survive:
- `Clean Unusued Configs = false`
- Coin / Crisp Dollar Bill / Wallet editing gates true
- their inside weights blank
- Flash Turret editing gate true
- `Flash Turret | Is Inside Hazard = false`
- Flash Turret inside weights blank

### S1.41
Exact BCMER 1.71.0 reactivated and runtime accepted.

Carry-forward:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`
- Raining / HeavyRain / AllWeather / Hurricane disabled
- natural vanilla Rainy allowed

Do not silently upgrade BCMER to 2.0.0.

### S1.42A
Interior config seed added eight interior packages + required LethalModDataLib 1.2.2.

Runtime:
- 52 dungeon flows total;
- 26 new flows;
- generated configs/real IDs available;
- `junkrooms` and `shatteredrooms` exact CullFactory IDs;
- Mausoleum too foggy;
- LMDL initialization NRE exposed.

### S1.42B
Compatibility plugin v1.1.0 added null-safe LMDL bulk registration.

Runtime-confirmed:
- `MW.MagicWesleyInteriors` is the null `PluginInfo.Instance`;
- skipped safely;
- LMDL fully initializes;
- moddata load/save succeeds.

This fix is accepted technically and must be retained.

### S1.42C
Compatibility plugin v1.2.0 + LethalMin config:
- `Thumper Bite Limit = 0`
- `Crawler` in Attack Blacklist
- Puffer smoke effect-trigger guard
- LMDL guard retained

Runtime:
- no new startup regression;
- LMDL healthy;
- Puffer did not spawn -> Puffer guard not validated;
- Thumper not deliberately tested -> total noninteraction not fully validated;
- Baboon Hawk bite proved a generic LethalMin grab/bite + invincibility state bug.

## Project-local compatibility plugin

Source:
`Patches/S139CompatibilityFixes/`

Current source version:
**1.3.2**

Latest runtime-proven non-crashing startup version:
**1.3.1 in S1.42E**

S1.42F embedded DLL SHA-256:
`8172c75bbcf75108266e1ce8d2808ec072f6cfc164acaf562baa0345123915f3`

Gale:
**Advanced options -> Import all files**

Expected general marker:
`S1.39 Compatibility Fixes loaded.`

S1.42E safe LethalMin completion marker:
`[LethalMinStateGuard] Safe generic grab/bite state repair registered on N declared enemy method(s).`

Important:
S1.42D v1.3.0 broad reflection/Harmony scan caused a startup crash. Do not restore it.

## Highest engineering priority

Fix the generic:

**enemy grab/bite + Invincible Pikmin -> broken leader/follow state**

without disabling all enemy interactions.

Confirmed with Baboon Hawk in S1.42C.

Keep separate requested immunity:
- Thumper/Crawler <-> Pikmin: no interaction either direction
- Puffer attack/smoke -> Pikmin: no effect

## Binding balancing/design rules

### Interiors
All registered interiors should have equal effective selection probability on every moon, including future additions.

Common target: Weight 100 where technically safe.

### Mausoleum
Reduce fog specifically inside `MelanieMausoleum`.

### BCMER
Pin 1.71.0.

Eight EventTypes should each have equal global base probability:
12.5% each.

Keep:
`Use custom weights? = false`

Constant scale for every EventType:
`12.5, 0, 12.5, 12.5`

### Functional Microwave
Target:
- editing gate true
- volume 0.7

### Jetpack
Historical juijui config evidence target: 140 seconds.
Current = 40s via ButteRyBalance.
Implement 140s with a current-compatible/local mechanism; do not restore obsolete Bigger Battery blindly.
Jetpack must not explode from sustained/high-speed boost use.
S1.42C Jetpack Fixes: `MidAirExplosions = OnlyTooHigh`.
Next-build target: `MidAirExplosions = Off`.

## Remaining interior tuning

- normalize generated interior weights;
- use exact IDs;
- CullFactory exceptions `junkrooms`, `shatteredrooms`;
- investigate Shatteredrooms Experimentation/Embrion block before overriding;
- Mausoleum-specific fog reduction;
- final runtime validation.

## Persistent project rules

- S1.29D diagnostic only.
- Malfunctions disabled until explicit request.
- SCP999 disabled.
- Observer disabled.
- Don't Touch Me disabled.
- AJB ship-door mod disabled while local failsafe exists.
- CodeRebirthLib must not return.
- LethalModDataLib allowed/required for DULL but must retain our guard.
- Unknown Enemy PowerLevels are never guessed.
- Prefer one positive spawn owner per enemy.
- Leaf Boy remains in LethalMin Attack Blacklist.
- Ogopogo disabled.
- Vermin disabled.

## Repository-first workflow

GitHub is canonical.

Use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/<build_id>/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`

Do not request a local repo clone or PowerShell profile build while the base exists online.

## Current build status

S1.42D:
**FAILED STARTUP — DO NOT RETEST**

Evidence:
`RuntimeEvidence/S1.42D/20260903T084247Z/`

S1.42E runtime:
**STARTUP PASS, BUT INTERACTION TEST BLOCKED BY PERIODIC ENEMY-ISOLATION FREEZES**

Evidence:
`RuntimeEvidence/S1.42E/20260903T091053Z/`

Latest built candidate:
**S1.42F**

`Profiles/LC V1 S1.42F Enemy Isolation Freeze Fix.r2z`

SHA-256:
`f09404a8195b46261570331f736d921fb1cb25cd304e8952e5f6fcb404ed9e6b`

Status:
**built successfully; awaiting runtime lobby-smoothness test**

`BuildSpecs/current.json`:
`IDLE_AFTER_S1.42F_BUILD_AWAITING_RUNTIME`

`RuntimeInbox/ACTIVE_BUILD.txt`:
`S1.42F`

Do not build another candidate before S1.42F runtime evidence is evaluated.

## New-chat takeover

Primary detailed handover:
`Current/22_HANDOVER_S1.42E_TO_NEXT.md`

Start prompt:
`Current/NEXT_CHAT_START_PROMPT_S1.42E.txt`

## Historical target reference — juijui

The original historical profile is committed and indexed:

`References/LegacyProfiles/juijui/juijui.r2z`

SHA-256:
`ddd10bcec3329c155b3a0a2d74460928b02df147356701fb6cf79ebb5a9f7e00`

Recovered Jetpack config evidence:
`JetpackBatteryUsage = 140`

Use juijui as a historical target/reference, not a V81 build base.

## Immediate next action

Test S1.42F.

First gate:
**reach Main Menu, host into the ship lobby in orbit, and confirm the S1.42E once-per-second freezes are gone.**

If smooth, continue in the same run:
- Baboon Hawk generic invincible-Pikmin state recovery;
- Thumper/Crawler <-> Pikmin zero interaction;
- Puffer smoke/attack no Pikmin effect;
- Jetpack ~140 seconds and no sustained/high-speed mid-air self-explosion;
- Microwave volume 0.7.

The temporary isolated-enemy mode must be removed after this regression stage and the full enemy roster restored from:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
