# 00 — Current State

**Handover refreshed:** 2026-09-03  
**Game:** Lethal Company V81

## Canonical acceptance state

Last fully accepted gameplay baseline:

**S1.41**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

S1.41 remains the acceptance anchor because S1.42A/B/C are staged technical descendants, not yet the final tuned gameplay release.

## Latest runtime-tested technical candidate

**S1.42C**

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Manifest:
- 188 Thunderstore packages
- 183 enabled
- 5 disabled
- project-local cumulative compatibility plugin embedded

Runtime evidence:
`RuntimeEvidence/S1.42C/20260902T235238Z/`

Status:
**runtime-tested regression candidate; usable technical base for descendants; not final gameplay acceptance.**

## S1.42A interior seed — completed

Evidence:
`RuntimeEvidence/S1.42A/20260902T224318Z/`

Confirmed:
- config-generation objective succeeded;
- 52 ExtendedDungeonFlows registered vs 26 in S1.41;
- 26 new flow IDs discovered;
- exact CullFactory IDs `junkrooms`, `shatteredrooms`;
- Mausoleum generated on Offense;
- generated interior weights are unequal and need tuning;
- Mausoleum fog is too dense;
- LethalModDataLib 1.2.2 initialization NRE discovered.

## S1.42B LMDL guard — fix confirmed

Evidence:
`RuntimeEvidence/S1.42B/20260902T231959Z/`

The project-local null-safe LethalModDataLib scanner is runtime-confirmed.

Offending null Chainloader entry:
`MW.MagicWesleyInteriors`

Confirmed continuation:
- safe scan completed;
- save/load/delete hooks connected;
- `ModDataHandler initialised!`;
- moddata load/save succeeded.

**LethalModDataLib initialization NRE is resolved.**

Keep this guard while LethalModDataLib 1.2.2 remains present.

## S1.42C Pikmin interaction result

S1.42C retained:
- `Thumper Bite Limit = 0`;
- `Crawler` in Pikmin Attack Blacklist;
- `Puffer Can Poison Pikmin = false`;
- targeted project-local Puffer smoke effect-trigger guard.

Runtime:
- no new startup regression;
- LMDL remained healthy;
- Puffer did not spawn -> Puffer smoke guard not yet runtime-validated;
- Crawler spawned, but no deliberate interaction test -> Thumper/Pikmin total noninteraction not fully validated;
- Baboon Hawk explicitly bit a Bulbmin and reproduced repeated `Leader is null when following`.

### New highest-priority bug

The leader-null error loop is a **generic LethalMin enemy grab/bite + Invincible Pikmin state bug**.

Observed sequence:
1. enemy bite/grab;
2. Pikmin leader removed;
3. grabbed/death timer starts;
4. invincibility blocks death;
5. Pikmin remains in invalid follow state;
6. repeated `Leader is null when following`.

Preferred fix:
repair/reset generic grabbed/follow state without globally blacklisting enemies.

Specific user-requested exceptions remain:
- Thumper <-> Pikmin: total noninteraction;
- Puffer attack/smoke -> Pikmin: no effect.

## Binding interior rule

Every registered interior should have the same effective selection probability as every other interior on every moon, including future additions.

Target:
Weight 100 per interior/moon pairing where technically safe/supported.

Hard author restrictions are compatibility questions to investigate, not desired rarity rules.

## Mausoleum requirement

Reduce fog specifically in `MelanieMausoleum`. Do not globally change every interior.

## BCMER requirement

BCMER stays pinned to exact 1.71.0.

Carry-forward guards:
- power ownership guard
- spawn-chance ownership guard
- no baseline ownership outside events
- randomizer off
- Raining / HeavyRain / AllWeather / Hurricane events disabled

New fixed EventType distribution:
8 categories x 12.5%.

Keep `Use custom weights? = false`.
Use constant scale `12.5, 0, 12.5, 12.5` for all eight EventTypes.

## Other pending tuning

Functional Microwave:
- set edit gate true;
- target volume 0.7.

Jetpack:
- historical juijui config evidence target = 140 seconds;
- current = 40s via ButteRyBalance Reduce Battery;
- do not restore obsolete Bigger Battery; reproduce 140s with a current-compatible mechanism;
- Jetpack must not explode from sustained/high-speed boost use;
- current Jetpack Fixes `MidAirExplosions = OnlyTooHigh`;
- next-build target `MidAirExplosions = Off`.

CullFactory:
- exact IDs: `junkrooms`, `shatteredrooms`.

Shatteredrooms:
- Experimentation/Embrion author block remains protected until technical safety is understood.

## Build state

`BuildSpecs/current.json`:
- `enabled = false`
- `build_id = IDLE_HANDOVER_AFTER_S1.42C_RUNTIME`

`BuildSpecs/S1.42D_PLAN.md`:
**DRAFT ONLY — DO NOT BUILD YET**

Do not rebuild S1.42C by default.

## Repository-first workflow

Use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`

Do not ask for local clone or PowerShell profile build while GitHub contains the needed base.

Profiles with the project-local DLL require:
**Gale -> Advanced options -> Import all files**

## Primary handover

Read:
`Current/16_HANDOVER_S1.42C_TO_NEXT.md`

Next chat start prompt:
`Current/NEXT_CHAT_START_PROMPT_S1.42C.txt`

## Historical juijui reference — committed and indexed

The old `juijui.r2z` profile is now formally classified as a historical primary reference for the project's intended gameplay/mod-configuration target.

Expected location:
`References/LegacyProfiles/juijui/juijui.r2z`

See:
`Current/18_JUIJUI_LEGACY_REFERENCE.md`

The project goal is to approach the old juijui constellation/configuration where technically reasonable while respecting current V81 compatibility and maintained mods.

Recovered historical Jetpack config evidence: `JetpackBatteryUsage = 140`. See `Current/18_JUIJUI_LEGACY_REFERENCE.md` for the evidence caveat.

This reference work does not supersede the current highest engineering priority: the generic LethalMin grab/bite + invincible-Pikmin invalid leader/follow-state fix.


## Next candidate scope — S1.42D

Next runtime candidate should be a focused S1.42D descendant of S1.42C containing:
- generic LethalMin enemy grab/bite + Invincible Pikmin state repair;
- retained S1.42C Thumper/Puffer guards;
- Jetpack 140-second target;
- Jetpack boost/speed explosion disabled;
- Functional Microwave volume 0.7 with editing gate true.

Broader interior/BCMER/CullFactory/Mausoleum tuning is deferred until this focused regression stage passes.


## S1.42D temporary enemy isolation

For the next focused regression run, only these enemies should be allowed to spawn:
- indoor: Thumper/Crawler and Puffer/Spore Lizard;
- outdoor: Baboon Hawk.

This is diagnostic-only. The normal enemy setup must not be permanently changed.

Canonical restore baseline:
`Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Detailed test plan:
`Current/19_S1.42D_ISOLATED_ENEMY_TEST.md`

After the isolated run, remove the diagnostic isolation layer and restore the complete S1.42C enemy configuration exactly.
