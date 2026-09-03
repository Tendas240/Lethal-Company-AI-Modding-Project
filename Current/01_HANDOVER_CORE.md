# 01 — Handover Core

## CURRENT CANONICAL OVERRIDE — S1.42L THUMPER CLOSED — 2026-09-03

This section is newer than the earlier S1.42L gate text below.

Latest valid runtime evidence:
`RuntimeEvidence/S1.42L/20260903T151817Z/`
Log SHA-256: `402015463b9ed83a0835a4df8ac7f6298cac662609700715563041e5447885bd`

Thumper/Crawler is now **PASS / CLOSED**:
- Pikmin -> Thumper/Crawler attack/latch confirmed by user;
- Thumper/Crawler -> Pikmin broken GrabPikmin state blocked;
- 36 `[ThumperPikminGuard]` blocks;
- 0 `Leader is null when following`;
- visible snapping is accepted as harmless and should be ignored.

Also closed:
- Puffer -> Pikmin PASS;
- Jetpack PASS;
- Baboon Hawk -> Pikmin PASS.

Only remaining isolated enemy gate:
**Pikmin -> Baboon Hawk attack/latch**.

Keep using S1.42L. Do not build a successor yet.

Current handover:
`Current/44_HANDOVER_S1.42L_THUMPER_CLOSED.md`

Current analysis:
`Current/43_S1.42L_RUNTIME_ANALYSIS_THUMPER_CLOSED.md`

Runtime route remains:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42L`

Build controller remains:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42L_BUILD_AWAITING_RUNTIME`

Do not restore normal enemies/BCMER and do not start repository migration until the remaining Pikmin -> Baboon Hawk direction is explicitly validated.


## CURRENT CANONICAL OVERRIDE — S1.42L — 2026-09-03

This section supersedes the S1.42K current-gate override below.

Latest valid runtime evidence:
**S1.42J**
`RuntimeEvidence/S1.42J/20260903T145657Z/`
Log SHA-256: `a8ce035bf64fa5b704e18c588215f43cd1fd184eef4f467dfbafa6fcb1379963`

S1.42K was built successfully but never runtime-tested and is superseded.

Current candidate:
**S1.42L — Pikmin Counterattack Restore**
`Profiles/LC V1 S1.42L Pikmin Counterattack Restore.r2z`
SHA-256: `fd6156cc37c704e987a902ac88592c0d2b13b638b9194ce1556b376d9bc70722`

Binding interaction rules:
- Baboon Hawk -> Pikmin: no target/chase/bite/grab/hold;
- Pikmin -> Baboon Hawk: normal LethalMin attack/latch allowed;
- Thumper/Crawler -> Pikmin: no functional GrabPikmin/leader-removal/death-timer effect;
- Pikmin -> Thumper/Crawler: normal LethalMin attack/latch allowed;
- Puffer -> Pikmin: no effect.

S1.42L Attack Blacklist exactly matches the modern S1.40B/S1.41 baseline:
`Docile Locust Bees,Manticoil,Red Locust Bees,Blob,Nemo,InternNPC,BellCrab,Nancy,Transporter,Janior,Peace Keeper,Guardsman,Tornado,FireStorm,Hurricane,Cabinet, Leaf boy`

Thus neither `Crawler` nor `Baboon hawk` remains blacklisted.

Exact next action:
**runtime-test S1.42L** by throwing Pikmin onto both a Thumper/Crawler and a Baboon Hawk while confirming the enemy-side guards still prevent the old broken Pikmin grabbed-state behavior.

Runtime route:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42L`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42L_BUILD_AWAITING_RUNTIME`

Canonical handover:
`Current/42_HANDOVER_S1.42L_TO_NEXT.md`

Do not restore normal enemies/BCMER and do not start the repository migration before S1.42L is evaluated.


## CURRENT CANONICAL OVERRIDE — S1.42K — 2026-09-03

This section is chronologically newer than the S1.42J handover/history below.

Latest valid runtime evidence:
**S1.42J**
`RuntimeEvidence/S1.42J/20260903T145657Z/`
Log SHA-256: `a8ce035bf64fa5b704e18c588215f43cd1fd184eef4f467dfbafa6fcb1379963`

S1.42J accepted:
- Baboon Hawk <-> Pikmin complete zero interaction: **PASS**;
- Puffer -> Pikmin: **PASS / reconfirmed**;
- Jetpack 140-second target / normal-use behavior: **PASS, accepted by user**;
- Thumper/Crawler -> Pikmin protection: **PASS**; 19 Thumper guard blocks and 0 leader-null errors.

The earlier bidirectional Thumper zero-interaction wording is superseded.
Current binding rule:
- **Thumper/Crawler -> Pikmin:** functional grab/bite state effects remain blocked;
- **Pikmin -> Thumper/Crawler:** normal LethalMin attack/latch is allowed.

Current candidate:
**S1.42K — Thumper Pikmin Attack Restore**
`Profiles/LC V1 S1.42K Thumper Pikmin Attack Restore.r2z`
SHA-256: `bbdc949c9477e138cc3dde7c261f36f014cf482dd930c393ab035d80f8560aa2`

S1.42K removes only `Crawler` from LethalMin's Pikmin Attack Blacklist; `Baboon hawk` remains blacklisted. Compatibility DLL is unchanged.

Exact next action:
**runtime-test S1.42K** by throwing Pikmin onto a Thumper/Crawler. Pikmin must latch/attack normally while the Thumper-owned GrabPikmin route remains blocked.

Runtime route:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42K`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42K_BUILD_AWAITING_RUNTIME`

Canonical current handover:
`Current/39_HANDOVER_S1.42K_TO_NEXT.md`

Current analyses:
- `Current/37_S1.42J_RUNTIME_ANALYSIS_AND_S1.42K_PLAN.md`
- `Current/38_S1.42K_THUMPER_PIKMIN_ATTACK_RESTORE_BUILD.md`
- `Current/Projektstatus_S1.42K.json`

Do not restore normal enemies/BCMER and do not start the repository structural migration until S1.42K is evaluated.



## Current takeover override — S1.42J

Chronologically newer than the historical sections below.

Latest built candidate:
`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

SHA-256:
`736d7a3b495e124d2469e392b9956c0c3a381a6ce0502baee30d05fabb346cb7`

Compatibility plugin:
- version 1.3.7
- DLL SHA-256 `7a810d4164394146d64fea2fec300591f4647c9e1b9de834bce4cd1a726e63f2`

Latest runtime evidence remains:
`RuntimeEvidence/S1.42H/20260903T125734Z/`

S1.42H:
- Puffer -> Pikmin PASS;
- Baboon Hawk + invincible Pikmin FAIL because enemy-side hold/re-grab persisted;
- direct Thumper/Crawler <-> Pikmin contact still needs runtime validation.

S1.42I:
- built successfully;
- never runtime-tested;
- superseded before test.

Binding S1.42J gameplay rule:
**Baboon Hawks and Pikmin do not interact in either direction.**

Implementation:
- disable exact `LethalMin.BaboonBirdPikminEnemy` adapter after BaboonBirdAI.Start;
- block exact declared `BitePikmin`;
- retain common `GrabPikmin` Baboon failsafe for all Pikmin;
- add exact runtime enemy name `Baboon hawk` to LethalMin Attack Blacklist;
- no broad/inherited LethalMin scan.

Exact next action:
**runtime-test S1.42J; do not build S1.42K first.**

Also deliberately validate Thumper/Crawler <-> Pikmin zero interaction.

Runtime route:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42J`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42J_BUILD_AWAITING_RUNTIME`

Canonical newest analysis:
`Current/33_S1.42J_BABOON_HAWK_ZERO_INTERACTION_BUILD.md`

## Historical predecessor gate — S1.42H

S1.42H is no longer the active gate.

Profile:
`Profiles/LC V1 S1.42H Thumper Grab Guard.r2z`

SHA-256:
`5859e15ce71d8cd71d27e20205640af1f10ff91fe6d4b956d4a7064ac8400e58`

Valid runtime evidence:
`RuntimeEvidence/S1.42H/20260903T125734Z/`

Result:
- startup/exact common GrabPikmin hook PASS;
- isolated enemy spawning PASS;
- Puffer -> Pikmin PASS;
- Baboon Hawk + invincible Pikmin FAIL due to repeated hold/re-grab;
- direct Thumper/Crawler <-> Pikmin validation incomplete.

S1.42I was built from this result but never runtime-tested. The user then selected complete Baboon Hawk <-> Pikmin zero interaction, producing S1.42J.

Details:
`Current/32_S1.42H_RUNTIME_ANALYSIS_AND_S1.42I_BUILD.md`

## Binding state

### Accepted gameplay baseline
- build: **S1.41**
- profile: `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`
- SHA-256: `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`
- status: runtime accepted

### Historical runtime-tested technical checkpoint — S1.42C
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
**1.3.7**

Historical note:
**v1.3.5 was the S1.42H-stage source/embedded version and is not the current source version.**

Latest runtime-proven predecessor:
**v1.3.3 in the clean S1.42G BCMER-off retest**

S1.42H embedded DLL SHA-256:
`d67f8f4bc2012f5b74086eb268fcb191f6990c93041617e9ef35c635ea33f186`

Gale:
**Advanced options -> Import all files**

Expected general marker:
`S1.39 Compatibility Fixes loaded.`

Expected S1.42H exact grab-hook marker:
`[LethalMinStateGuard] Directly patched declared LethalMin.PikminAI.GrabPikmin(Transform,float,int) exactly once. No inherited/derived PikminAI Harmony scan is used.`

Expected Thumper encounter marker:
`[ThumperPikminGuard] Blocked Crawler/Thumper -> Pikmin GrabPikmin before leader/grab/death-timer state mutation.`

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
- future build: reduce Functional Microwave occurrence somewhat; exact rarity value remains to be selected after clean runtime confirmation

### Jetpack
Historical juijui config evidence target: 140 seconds.
S1.42H retains ButteRyBalance `Reduce Battery = false`.
S1.42H retains the loaded Jetpack Item target at 140 seconds.
S1.42H retains JetpackFixes `MidAirExplosions = Off`.
Do not restore obsolete Bigger Battery blindly.
Runtime still needs to validate approximately 140 seconds of usable duration and no sustained/high-speed normal-boost self-explosion.

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

S1.42E:
**startup pass; historical freeze-regression candidate.**

S1.42F:
**historical routed-moon performance failure.**

S1.42G BCMER-off retest:
**VALID RUNTIME EVIDENCE — periodic freezes resolved; target enemies spawn without BCMER; Thumper invalid grab state reproduced.**

Evidence:
`RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`

Latest built candidate:
**S1.42J**

`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

SHA-256:
`736d7a3b495e124d2469e392b9956c0c3a381a6ce0502baee30d05fabb346cb7`

Compatibility plugin:
**v1.3.7**

DLL SHA-256:
`7a810d4164394146d64fea2fec300591f4647c9e1b9de834bce4cd1a726e63f2`

Status:
**built successfully; awaiting runtime validation**

`BuildSpecs/current.json`:
`IDLE_AFTER_S1.42J_BUILD_AWAITING_RUNTIME`

`RuntimeInbox/ACTIVE_BUILD.txt`:
`S1.42J`

Do not build S1.42K before S1.42J runtime evidence is evaluated.

## New-chat takeover

Canonical current handover:
`Current/36_HANDOVER_S1.42J_TO_NEXT.md`

Latest build analysis:
`Current/33_S1.42J_BABOON_HAWK_ZERO_INTERACTION_BUILD.md`

Predecessor runtime/build analysis:
`Current/32_S1.42H_RUNTIME_ANALYSIS_AND_S1.42I_BUILD.md`

Verification:
`Current/VERIFIKATION_S1.42J.txt`

Start prompt:
`Current/NEXT_CHAT_START_PROMPT_S1.42J.txt`

Pending repository-optimization plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

The repository migration is recommended but deferred until the active critical runtime/build gate is evaluated and the resulting canonical state is documented. It is not the immediate next gameplay task.

Older S1.42H/I handovers remain historical/diagnostic context and must not override S1.42J instructions.

## Historical target reference — juijui

The original historical profile is committed and indexed:

`References/LegacyProfiles/juijui/juijui.r2z`

SHA-256:
`ddd10bcec3329c155b3a0a2d74460928b02df147356701fb6cf79ebb5a9f7e00`

Recovered Jetpack config evidence:
`JetpackBatteryUsage = 140`

Use juijui as a historical target/reference, not a V81 build base.

## Immediate next action

Runtime-test **S1.42J**.

Profile:
`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

Import:
**Gale -> Advanced options -> Import all files**

Do not manually change package states or configs. BCMER 1.71.0 is already disabled in S1.42J.

Primary questions:
- does the game reach Main Menu and host cleanly;
- do routed moons remain free of periodic stalls;
- do target enemies still populate the `Enemies` terminal output;
- do Baboon Hawks completely ignore Pikmin instead of targeting/chasing/biting/grabbing/holding them;
- do Pikmin avoid attacking/latching Baboon Hawks;
- does the expected Baboon adapter-disable marker appear;
- does direct Crawler/Thumper contact produce zero interaction in both directions and the `[ThumperPikminGuard]` marker;
- Puffer only needs an optional spot-check because S1.42H already established PASS.

Upload the complete fresh log to:
`RuntimeInbox/Current/`

If a new S1.42J log is already committed, analyze it immediately instead of requesting another test.

After this isolated stage passes:
- remove/disable temporary EnemyIsolation;
- restore full enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0.

Do not build S1.42K before S1.42J runtime evidence is evaluated.
