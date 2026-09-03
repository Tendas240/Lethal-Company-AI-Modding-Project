# 04 — Open Issues and Next Tests

## Immediate active gate — S1.42G BCMER-off clean retest

The oversized S1.42G runtime evidence formerly under `RuntimeEvidence/S1.42G/20260903T100914Z/` was intentionally deleted and must not be treated as project evidence.

Next runtime variant:
`S1.42G_BCMER_OFF_RETEST`

Use canonical S1.42G, manually disable BCMER only, and make no other profile/config changes.

Unconfirmed observations to reproduce:
- no visible enemies;
- `Enemies` terminal output empty even late in the day;
- repeated HangarShipDoor/DoorAudit stack spam possibly associated with BCMER `Door System: ERROR`;
- Functional Microwaves felt too common.

Do not patch or rebalance from those observations until the clean retest reproduces them.

## Previous active gate — S1.42G routed-moon smoothness

S1.42E fixed the S1.42D startup crash but exposed a new diagnostic-only performance regression.

Evidence:
`RuntimeEvidence/S1.42E/20260903T091053Z/`

Confirmed:
- safe LethalMin state guard registered on 4 declared enemy methods;
- Jetpack asset target successfully changed 50 -> 140 seconds;
- EnemyIsolation then attempted six invalid `SpawnableEnemyWithRarity` default-constructor creations per second on Gordion;
- this matches the user's short once-per-second freezes.

S1.42G:
`Profiles/LC V1 S1.42G Routed Moon Performance Fix.r2z`

SHA-256:
`09364c11f8032645205b869ad760471259520cd57758e4d2d09a35665cf0d35a`

First test:
- Main Menu;
- host into ship lobby in orbit;
- verify the periodic freeze cadence is gone.

If smooth, continue immediately with the focused Baboon Hawk / Thumper / Puffer / Jetpack / Microwave test.

## Highest engineering priority — generic LethalMin grab/bite + Invincible Pikmin state

S1.42C runtime evidence proves that the repeated `Leader is null when following` loop is not Thumper-specific.

Confirmed with a Baboon Hawk:
1. enemy bite/grab starts;
2. Pikmin leader is removed;
3. LethalMin starts its grabbed/death timer;
4. `Invinceable Pikmin = true` prevents final death;
5. follower remains in an invalid leader-less state;
6. repeated `Leader is null when following` errors follow.

Preferred solution:
- repair/reset the generic grabbed/follow state when invincibility prevents death;
- preserve intended enemy interactions;
- do not blindly blacklist every enemy.

Evidence:
`Current/15_RUNTIME_EVIDENCE_S1.42C.md`

## Specific retained Pikmin requirements

### Thumper / Crawler

User requirement:
**Thumper and Pikmin must not interact in either direction.**

Current S1.42C controls:
- `Thumper Bite Limit = 0`
- `Crawler` in LethalMin Attack Blacklist

Runtime:
- Crawler spawned;
- no clear Thumper-Pikmin bite/latch was logged;
- no deliberate controlled encounter was performed.

Status:
**retained but not fully validated.**

Targeted future validation:
- stand with Pikmin near a Thumper;
- no Thumper grab/bite;
- no Pikmin attack/latch;
- no resulting leader-null spam.

### Puffer

User requirement:
**Puffer attack/smoke must not affect Pikmin.**

Config already has:
`Puffer Can Poison Pikmin = false`

Project compatibility plugin v1.2.0 also adds a targeted Puffer smoke effect-trigger guard.

S1.42C:
- patch registration marker present;
- no Puffer spawned;
- actual smoke immunity remains unvalidated.

Targeted future validation:
- spawn/encounter Puffer;
- expose Pikmin to smoke;
- Pikmin should remain unaffected;
- player/vanilla Puffer behavior should remain normal;
- look for `[PufferPikminGuard] Removed ...`.

## Resolved — LethalModDataLib 1.2.2 initialization NRE

S1.42B runtime-confirmed the project-local null-safe registration guard.

Offending null Chainloader entry:
`MW.MagicWesleyInteriors`

Confirmed:
- safe scan completed;
- save/load/delete hooks connected;
- `ModDataHandler initialised!`;
- moddata load/save succeeded.

Keep the guard while LethalModDataLib 1.2.2 remains installed.

## Interior tuning — pending

S1.42A generated the real config/ID set.

Known:
- 52 dungeon flows total;
- 26 new flows vs S1.41;
- exact CullFactory IDs:
  - `junkrooms`
  - `shatteredrooms`

### Binding equal-probability architecture

Every registered interior should have the same effective selection probability as every other interior on every moon, including future additions.

Target:
Weight 100 per interior/moon pairing where technically supported/safe.

Do not preserve package rarity/theme preferences as desired balancing.

Hard author restrictions are compatibility issues to investigate.

Current example:
Shatteredrooms excludes Experimentation/Embrion. Preserve until technical safety is understood; desired final architecture is still equality everywhere if safe.

### CullFactory

Pending final config:
- disable culling for `junkrooms`
- disable culling for `shatteredrooms`

Use exact generated IDs; do not guess variants.

### Mausoleum fog

Observed:
`MelanieMausoleum` is far too foggy for comfortable gameplay.

Requirement:
- reduce fog specifically inside Mausoleum;
- do not globally reduce fog in every dungeon;
- atmosphere may remain, but visibility has priority.

Generated Melanie config has no obvious fog-density key, so likely needs a targeted runtime/HDRP-volume solution.

## BCMER final tuning — pending

Pin:
`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Do not silently migrate to 2.0.0.

Carry-forward ownership guards:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

BCMER rain-event routes remain disabled:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy remains allowed.

User-selected global EventType distribution:
- Insane = 12.5%
- VeryBad = 12.5%
- Bad = 12.5%
- Neutral = 12.5%
- Good = 12.5%
- VeryGood = 12.5%
- Rare = 12.5%
- Remove = 12.5%

Keep:
`Use custom weights? = false`

Apply constant scale:
`12.5, 0, 12.5, 12.5`

to all eight EventTypes.

## Functional Microwave — volume configured; future rarity reduction requested

S1.42E configured values:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

User target:
- `Allow Editing Config = true`
- `Volume = 0.7`
- Functional Microwaves should be somewhat rarer in a future build than in S1.42G.

The exact rarity reduction is not yet selected. Do not change Microwave rarity during the manual BCMER-off retest, because that retest must alter BCMER only.

Use config first; do not Harmony-patch audio unless runtime proves the config is ignored.

## Jetpack capacity — historical primary evidence recovered

User wants the old juijui-profile capacity/duration.

Current S1.42G:
- ButteRyBalance `Reduce Battery = false`;
- project-local loaded Jetpack Item target = 140 seconds;
- JetpackFixes `MidAirExplosions = Off`;
- actual runtime duration/explosion behavior is still unvalidated in a clean representative run.

The committed/indexed juijui profile contains historical Bigger Battery v1.0.2 config:
- `JetpackBatteryUsage = 140`
- config states then-game default = 60.

Caveat:
- BiggerBattery is absent from the final juijui `export.r2x` and no plugin binary is present, so the config may be retained from an earlier active state.

Project target:
- treat 140 seconds as the strongest historical intended/configured juijui target unless contradictory primary evidence appears;
- implement it with a current-compatible/local mechanism;
- do not blindly restore obsolete Bigger Battery.

Reference:
`References/LegacyProfiles/juijui/Extracted/`
`References/juijui_Referenzwerte.txt`

## Monitor-only — Mineshaft elevator + Pikmin crowding

Observed once in S1.41:
- player in Mineshaft elevator with many Pikmin;
- floor clipping during descent;
- fall death;
- heavy NavMesh-agent creation warnings nearby.

Causality remains unproven.

Track in future multi-floor/elevator runs.

## Monitor-only — outdoor Pikmin Sprout density

User had a subjective impression of lower outdoor sprout density.

Current evidence does not justify rebalance.

Collect statistical evidence only if concern persists.

## Carry-forward regression guards

When naturally encountered, continue checking:
- no unwanted natural Coin / Crisp Dollar Bill / Wallet;
- no natural Flash Turret;
- BCMER ownership/rain guards survive;
- Ogopogo absent;
- Vermin absent;
- Autonomous Crane cannot kill Pikmin/Puffmin;
- recharge station full-heal behavior;
- Old Bird Resonance encounter;
- Mirage recording retention;
- LMDL safe scan + ModDataHandler initialization.

## Known noise / only escalate with user-facing symptoms

- SoundAPI TypeLoadException during floor reporting;
- SoftMaskKiller-protected SoftMask NREs;
- duplicate NetworkPrefab hash warnings;
- RuntimeNavMeshBuilder unreadable-mesh messages;
- BCMER ButlerSword missing-script warning;
- S1.42C scene-teardown `Collection was modified` exception.

## Build state

`BuildSpecs/current.json`:
- disabled
- `IDLE_S1.42G_BCMER_OFF_RETEST`

S1.42D:
**FAILED STARTUP — DO NOT RETEST**

S1.42E:
**startup pass; interaction test aborted because of periodic EnemyIsolation freezes.**

S1.42G:
`Profiles/LC V1 S1.42G Routed Moon Performance Fix.r2z`
SHA-256:
`09364c11f8032645205b869ad760471259520cd57758e4d2d09a35665cf0d35a`

Status:
**built; previous oversized runtime evidence discarded; awaiting clean BCMER-off manual retest.**

Do not build a new candidate before evaluating the clean S1.42G BCMER-off retest.

## Historical juijui profile — uploaded and indexed

Canonical path:
`References/LegacyProfiles/juijui/juijui.r2z`

Readable snapshot:
`References/LegacyProfiles/juijui/Extracted/`

Purpose:
- preserve the original project target profile as primary historical evidence;
- recover exact historic configuration values instead of guessing;
- specifically resolve the current Jetpack capacity/duration question.

See:
`Current/18_JUIJUI_LEGACY_REFERENCE.md`

This is a reference task and must not delay the higher-priority generic LethalMin enemy grab/bite + invincible-Pikmin state repair.


## Jetpack explosion behavior — next build

User requirement:
the Jetpack must not explode merely because it is boosted/used for too long.

S1.42E:
- Jetpack Fixes v1.6.3
- `MidAirExplosions = Off`
- local loaded-Item target = 140 seconds

Runtime acceptance target:
- sustained/high-speed boost must not trigger a Jetpack self-explosion;
- Jetpack runtime duration should be approximately 140 seconds.

Jetpack Fixes still documents collision-with-solid-geometry crash behavior separately. The immediate binding requirement is to eliminate boost/speed/self-destruction during normal Jetpack use. If runtime shows another non-collision usage explosion path, patch it narrowly.

Combined next Jetpack target:
- historical juijui capacity target: 140 seconds;
- no mid-air/high-speed/continuous-boost explosion.

## S1.42G immediate runtime gate

Use:
`Profiles/LC V1 S1.42G Routed Moon Performance Fix.r2z`

SHA-256:
`09364c11f8032645205b869ad760471259520cd57758e4d2d09a35665cf0d35a`

Manual test variant:
`S1.42G_BCMER_OFF_RETEST`

Before launch:
- disable BCMER only;
- leave every other mod/config unchanged.

First check:
- game reaches Main Menu;
- host/routing remains smooth;
- no Coroner Jetpack warning flood;
- isolated enemies appear and are visible through the `Enemies` terminal command.

If the enemy spawn path works, continue with Baboon Hawk / Thumper / Puffer tests.

S1.42D must not be retested.
The deleted oversized S1.42G evidence must not be cited.
