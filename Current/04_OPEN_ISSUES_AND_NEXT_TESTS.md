# 04 — Open Issues and Next Tests

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


## IMMEDIATE ACTIVE GATE — S1.42K

Profile:
`Profiles/LC V1 S1.42K Thumper Pikmin Attack Restore.r2z`

SHA-256:
`bbdc949c9477e138cc3dde7c261f36f014cf482dd930c393ab035d80f8560aa2`

Import:
**Gale -> Advanced options -> Import all files**

S1.42J established:
- Baboon Hawk <-> Pikmin zero interaction PASS;
- Puffer -> Pikmin PASS;
- Jetpack PASS/accepted;
- Thumper/Crawler -> Pikmin protection PASS with 19 guard blocks and zero leader-null errors.

Revised binding Thumper rule:
- Thumper/Crawler -> Pikmin: blocked functional grab/death-state effects;
- Pikmin -> Thumper/Crawler: normal attack/latch allowed.

S1.42K removes `Crawler` from LethalMin Attack Blacklist while retaining `Baboon hawk`.

Primary runtime test:
1. throw Pikmin directly onto a Thumper/Crawler;
2. verify Pikmin latch/attack normally;
3. allow Thumper to snap toward Pikmin;
4. verify `[ThumperPikminGuard]` still blocks GrabPikmin;
5. verify no grabbed death timer, leader removal, or `Leader is null when following`.

If PASS:
- isolated enemy interaction gate complete;
- restore enemy state from `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`;
- re-enable exact BCMER 1.71.0;
- then document resulting state before repository migration.

Do not build a successor before S1.42K runtime evidence is evaluated unless S1.42K itself cannot start.


## Immediate active gate — S1.42J Baboon Hawk Zero Interaction

Profile:
`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

SHA-256:
`736d7a3b495e124d2469e392b9956c0c3a381a6ce0502baee30d05fabb346cb7`

Import with:
**Gale -> Advanced options -> Import all files**

Binding Baboon Hawk rule:
**Baboon Hawks and Pikmin do not interact in either direction.**

Primary test:
1. startup/Main Menu and host;
2. route/land on a normal moon;
3. confirm `Enemies` still shows diagnostic targets;
4. deliberately place a Pikmin group around one or more Baboon Hawks;
5. Baboon Hawks must ignore Pikmin rather than target/chase/bite/grab/hold them;
6. Pikmin must not attack/latch Baboon Hawks;
7. expected initialization marker:
   `[BaboonHawkPikminGuard] Zero-interaction initialized; ...`
8. expected spawned-Hawk marker:
   `[BaboonHawkPikminGuard] Disabled LethalMin.BaboonBirdPikminEnemy on BaboonHawkEnemy(Clone). Baboon Hawk -> Pikmin targeting/chase/bite adapter is inactive.`
9. `BitePikmin` / `GrabPikmin` failsafe markers should ideally not be needed during normal zero-interaction; if one fires, note whether visible chase/interaction occurred;
10. deliberately let a Crawler/Thumper cross a Pikmin group and validate zero interaction in both directions;
11. Puffer does not need another forced test; spot-check only if convenient;
12. upload the complete fresh log to `RuntimeInbox/Current/`.

BCMER 1.71.0 remains intentionally disabled.
EnemyIsolation remains intentionally enabled.
Functional Microwave rarity remains unchanged.

Do not build S1.42K before this runtime gate is evaluated.

## Superseded untested candidate — S1.42I

S1.42I was built successfully but never runtime-tested.

It is not the active gate because the user changed the desired Baboon-Hawk behavior before testing:
instead of merely preventing the broken invincible-Pikmin grab state, Baboon Hawks and Pikmin should now completely ignore each other.

S1.42I remains historical build evidence only.

## Completed gate — S1.42H runtime analysis

Evidence:
`RuntimeEvidence/S1.42H/20260903T125734Z/`

Result:
- startup/exact hook PASS;
- enemy isolation/spawning PASS;
- `Enemies` terminal PASS by user gameplay observation;
- Puffer smoke -> Pikmin PASS;
- Baboon Hawk + invincible Pikmin FAIL because enemy-side hold/re-grab persists despite post-grab state restoration;
- Crawler spawned, but direct Thumper/Pikmin contact was not validated.

Key Baboon counts:
- 64 bite calls;
- 59 grabbed states;
- 59 grabbed death timers;
- 59 invincibility-blocked kill attempts;
- 56 repairs;
- 193 leader-null errors.

This gate directly produced S1.42I.

## Completed gate — S1.42G BCMER-off clean retest

Valid evidence:
`RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`

Result:
- periodic routed-moon freezes are gone;
- Crawler/Thumper and Puffer spawn without BCMER;
- Puffer smoke guard activates;
- Coroner's prior Jetpack `PlayerController was null` flood is absent;
- the repeated zero-power DoorAudit/HangarShipDoor stack flood does not reproduce with BCMER disabled;
- Thumper contact reproduces the invalid grabbed/leader-null Pikmin state.

This gate is complete and directly produced S1.42H.

The earlier oversized S1.42G ingest formerly under
`RuntimeEvidence/S1.42G/20260903T100914Z/`
remains intentionally deleted and must not be cited.

## Historical gate — S1.42G routed-moon smoothness

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

Binding user requirement:
**Thumper and Pikmin must not interact in either direction.**

Confirmed predecessor behavior in the clean S1.42G BCMER-off retest:
- four Crawler/Thumper instances spawned;
- deliberate contact produced a bite/grab sequence;
- LethalMin removed a Pikmin leader and started the grabbed death timer;
- invincibility blocked death;
- repeated `Leader is null when following` followed.

S1.42H fix:
- exact one-time hook on `LethalMin.PikminAI.GrabPikmin(Transform,float,int)`;
- block Crawler/Thumper-owned grabs before leader removal/death timer;
- retain `Crawler` in LethalMin Attack Blacklist for Pikmin -> Thumper.

Runtime acceptance:
- Thumper can cross into/through a Pikmin group without grabbing them;
- no leader removal;
- no grabbed death timer;
- no Pikmin latch/attack on Crawler;
- no new Thumper-caused leader-null loop;
- expected marker:
  `[ThumperPikminGuard] Blocked Crawler/Thumper -> Pikmin GrabPikmin before leader/grab/death-timer state mutation.`

Status:
**fix retained through S1.42J; deliberate direct-contact runtime validation pending.**

### Puffer

Binding user requirement:
**Puffer attack/smoke must not affect Pikmin.**

Config:
`Puffer Can Poison Pikmin = false`

Project-local smoke guard remains active.

Clean S1.42G BCMER-off evidence:
- two Puffers spawned;
- the compatibility guard removed LethalMin Pikmin-effect components from their smoke path;
- first Puffer: 3 components removed;
- second Puffer: 2 components removed.

Status:
**PASS from S1.42H runtime evidence. Recheck only if conveniently encountered; no forced Puffer test is required for S1.42J.**

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

Current S1.42J retained values:
- `Functional Microwave | Allow Editing Config = true`
- `Functional Microwave | Volume = 0.7`

User target:
- `Allow Editing Config = true`
- `Volume = 0.7`
- Functional Microwaves should be somewhat rarer in a future post-isolation build than in the current S1.42J/S1.42H behavior.

The exact rarity reduction is not yet selected. Do not change Microwave rarity during the S1.42J isolated enemy runtime gate.

Use config first; do not Harmony-patch audio unless runtime proves the config is ignored.

## Jetpack capacity — historical primary evidence recovered

User wants the old juijui-profile capacity/duration.

Current S1.42J:
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
- disabled;
- `IDLE_AFTER_S1.42J_BUILD_AWAITING_RUNTIME`;
- base/reference = S1.42J.

`RuntimeInbox/ACTIVE_BUILD.txt`:
- `S1.42J`

S1.42D:
**FAILED STARTUP — DO NOT RETEST**

S1.42G BCMER-off:
**valid completed runtime gate**

S1.42H:
**valid runtime evidence — Puffer PASS, Baboon Hawk hold/re-grab FAIL, Thumper direct validation incomplete.**

S1.42I:
**built successfully but never runtime-tested; superseded before test by the binding Baboon Hawk <-> Pikmin zero-interaction rule.**

S1.42J:
`Profiles/LC V1 S1.42J Baboon Hawk Zero Interaction.r2z`

SHA-256:
`736d7a3b495e124d2469e392b9956c0c3a381a6ce0502baee30d05fabb346cb7`

Status:
**built successfully; awaiting runtime validation.**

Do not build S1.42K before evaluating S1.42J.

## Deferred repository-maintenance task — structural migration

Status:
**recommended, but intentionally deferred until the active critical runtime/build gate is evaluated and the resulting state is documented.**

Canonical plan:
`Current/35_REPOSITORY_OPTIMIZATION_MIGRATION_PLAN_PENDING.txt`

Purpose:
- shrink the mandatory ChatGPT bootstrap context;
- make Current/ truly current;
- introduce stable canonical state/read-order paths;
- separate active state from historical evidence;
- improve ProfileSources/ and RuntimeEvidence/ indexes;
- preserve failed approaches and primary evidence;
- add automated repository consistency validation.

This maintenance task must not displace the immediate S1.42J runtime test. A future chat must first re-evaluate the then-current repository state and only begin the migration when no critical gate is left half-finished.


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

This is a reference task and must not delay the higher-priority S1.42J isolated enemy runtime gate.


## Pending later gameplay validation — Jetpack explosion behavior

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

## Historical S1.42G runtime gate — completed

The clean BCMER-off retest is complete.

Evidence:
`RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`

Its results are incorporated into S1.42H and summarized in:
`Current/30_S1.42G_BCMER_OFF_RETEST_ANALYSIS_AND_S1.42H_BUILD.md`

Current active gate is S1.42J at the top of this file.
S1.42D must not be retested.
The deleted oversized S1.42G evidence must not be cited.

