# 00 — Current State

## Latest update — S1.42H runtime -> S1.42I

Valid S1.42H evidence:
`RuntimeEvidence/S1.42H/20260903T125734Z/`

Log SHA-256:
`81ed064ce97d25f250d6fba1585055baef8ce801cd0f13626d074bf4fef71029`

Confirmed:
- exact S1.42H common GrabPikmin hook loaded once; startup safe;
- isolated enemy spawning works;
- Puffer -> Pikmin smoke protection passes;
- in-game `Enemies` output works per user observation;
- Baboon Hawk + invincible Pikmin still fails: 64 bite calls, 59 grabbed/death-timer states, 56 repairs, 193 leader-null errors; enemy-side hold/re-grab persists;
- Crawler spawned but direct Thumper/Pikmin contact was not validated;
- Coroner Jetpack `PlayerController was null` remains at 0;
- DoorAudit remained normal.

Latest built candidate:

**S1.42I**

`Profiles/LC V1 S1.42I Baboon Hawk Grab Guard.r2z`

SHA-256:
`c7224aea97c51fb051da059648868bbae0421b9c3f02d5cc2dd60922efc28a97`

Compatibility plugin:
**v1.3.6**

DLL SHA-256:
`76544a536f5c626f0c81b50dc06a7bf1521c265cd23a7698917789e3846eecb2`

S1.42I:
- keeps the exact one-time `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` hook;
- blocks Baboon Hawk -> invincible Pikmin GrabPikmin before hold/leader/death-timer mutation;
- does not globally blacklist Baboon Hawks or mortal-Pikmin behavior;
- keeps Thumper/Crawler zero-interaction and Puffer smoke guards unchanged;
- keeps EnemyIsolation enabled and BCMER 1.71.0 disabled for this isolated gate.

Status:
**built successfully; awaiting runtime validation.**

Runtime route:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42I`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42I_BUILD_AWAITING_RUNTIME`

Canonical analysis:
`Current/32_S1.42H_RUNTIME_ANALYSIS_AND_S1.42I_BUILD.md`

Do not build S1.42J before S1.42I runtime evidence is evaluated.


## Latest update — S1.42G BCMER-off retest -> S1.42H

Valid clean evidence:
`RuntimeEvidence/S1.42G_BCMER_OFF_RETEST/20260903T115643Z/`

Confirmed:
- periodic routed-moon freezes are resolved;
- Crawler and Puffer spawn normally with BCMER disabled;
- Puffer smoke guard activates;
- Thumper contact still enters LethalMin's grabbed-Pikmin path and reproduces the invincible-Pikmin leader-null loop;
- the previous Coroner Jetpack `PlayerController was null` flood is gone;
- BCMER-off removes the prior repeated DoorFailure/DoorAudit stack flood.

Latest built candidate:

**S1.42H**

`Profiles/LC V1 S1.42H Thumper Grab Guard.r2z`

SHA-256:
`5859e15ce71d8cd71d27e20205640af1f10ff91fe6d4b956d4a7064ac8400e58`

Compatibility plugin:
**v1.3.5**

S1.42H:
- patches exactly `LethalMin.PikminAI.GrabPikmin(Transform,float,int)` once;
- blocks Crawler/Thumper -> Pikmin grab before leader removal/death timer;
- retains Crawler in the Pikmin Attack Blacklist for the reverse direction;
- applies generic post-grab recovery to non-Thumper interactions;
- carries forward late-lifecycle EnemyIsolation and throttled DoorAudit;
- embeds BCMER 1.71.0 as disabled for this final isolated regression stage;
- does **not** change Functional Microwave rarity.

Status:
**built successfully; awaiting runtime validation.**

Runtime route:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42H`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42H_BUILD_AWAITING_RUNTIME`

Canonical latest analysis:
`Current/30_S1.42G_BCMER_OFF_RETEST_ANALYSIS_AND_S1.42H_BUILD.md`


**Handover refreshed:** 2026-09-03  
**Game:** Lethal Company V81

## Historical runtime/build progression — S1.42F -> S1.42G

S1.42F runtime evidence:
`RuntimeEvidence/S1.42F/20260903T092728Z/`

Confirmed:
- Gordion/Company constructor-loop fix worked;
- ship lobby was smooth before routing;
- after routing to Offense, periodic freezes returned;
- diagnostic EnemyIsolation still performed a once-per-second global `FindObjectsOfType<EnemyAI>()` scan;
- Coroner produced 16,138 dying-player warnings because its `JetpackItem.Update` death detector queried an unheld Jetpack every frame.

At that historical point, the next built candidate was:

**S1.42G**

`Profiles/LC V1 S1.42G Routed Moon Performance Fix.r2z`

SHA-256:
`09364c11f8032645205b869ad760471259520cd57758e4d2d09a35665cf0d35a`

Compatibility plugin:
**v1.3.3**

Changes:
- EnemyIsolation is one-shot per SelectableLevel change;
- no continuous global EnemyAI scan;
- Coroner remains enabled, but only its faulty JetpackItem.Update prefix/postfix are removed.

Status:
**historical status at that point: built successfully; the first oversized evidence was discarded and the clean BCMER-off retest was still pending. That retest has since completed and produced S1.42H.**

## Canonical acceptance state

Last fully accepted gameplay baseline:

**S1.41**

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:
`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

S1.41 remains the acceptance anchor because S1.42A/B/C are staged technical descendants, not yet the final tuned gameplay release.

## Historical runtime-tested technical checkpoint — S1.42C

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
- edit gate true;
- target volume 0.7;
- future tuning requirement: make Functional Microwaves somewhat rarer than in S1.42G; exact rarity reduction is not yet selected and should be implemented in a later build, not by manually changing this retest.

Jetpack:
- historical juijui config evidence target = 140 seconds;
- S1.42H retains ButteRyBalance `Reduce Battery = false`;
- S1.42H retains the project-local loaded Jetpack Item target at 140 seconds;
- S1.42H retains JetpackFixes `MidAirExplosions = Off`;
- do not restore obsolete Bigger Battery;
- actual ~140-second runtime duration and sustained/high-speed no-self-explosion behavior still require clean gameplay validation.

CullFactory:
- exact IDs: `junkrooms`, `shatteredrooms`.

Shatteredrooms:
- Experimentation/Embrion author block remains protected until technical safety is understood.

## Build state

`BuildSpecs/current.json`:
- `enabled = false`
- `build_id = IDLE_AFTER_S1.42H_BUILD_AWAITING_RUNTIME`
- base/reference = S1.42H

`RuntimeInbox/ACTIVE_BUILD.txt`:
- `S1.42H`

S1.42D:
**failed startup; do not retest.**

S1.42E:
**startup passed; interaction testing was blocked by the then-current EnemyIsolation freeze loop.**

S1.42F:
**Gordion smooth; routed-moon stalls and Coroner Jetpack spam remained.**

S1.42G:
**clean BCMER-off retest completed; freezes resolved, enemy spawning works without BCMER, Thumper invalid grab state reproduced.**

S1.42H:
**latest built candidate; GitHub Actions success; awaiting first runtime validation.**

Do not create S1.42I before S1.42H runtime evidence is evaluated.

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

## Primary current takeover

Read first after the master prompt:
- `Current/31_HANDOVER_S1.42H_TO_NEXT.md`
- `Current/30_S1.42G_BCMER_OFF_RETEST_ANALYSIS_AND_S1.42H_BUILD.md`
- `Current/00_CURRENT_STATE.md`
- `Current/01_HANDOVER_CORE.md`
- `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
- `Current/Projektstatus_S1.42H.json`
- `Current/VERIFIKATION_S1.42H.txt`
- `Current/SHA256SUMS_S1.42H.txt`
- `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Current start prompt:
`Current/NEXT_CHAT_START_PROMPT_S1.42H.txt`

Runtime route:
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42H`

Build controller:
`BuildSpecs/current.json = disabled / IDLE_AFTER_S1.42H_BUILD_AWAITING_RUNTIME`

## Historical juijui reference — committed and indexed

The old `juijui.r2z` profile is now formally classified as a historical primary reference for the project's intended gameplay/mod-configuration target.

Expected location:
`References/LegacyProfiles/juijui/juijui.r2z`

See:
`Current/18_JUIJUI_LEGACY_REFERENCE.md`

The project goal is to approach the old juijui constellation/configuration where technically reasonable while respecting current V81 compatibility and maintained mods.

Recovered historical Jetpack config evidence: `JetpackBatteryUsage = 140`. See `Current/18_JUIJUI_LEGACY_REFERENCE.md` for the evidence caveat.

This reference work does not supersede the current highest engineering priority: the generic LethalMin grab/bite + invincible-Pikmin invalid leader/follow-state fix.


## S1.42D startup failure

S1.42D is **failed** as a runtime candidate.

Evidence:
`RuntimeEvidence/S1.42D/20260903T084247Z/`

Log SHA-256:
`55cdbf6904c7d1acb74647c90a79820df9e3a39978cd60ccf4d6e25bc95d4107`

Root cause:
the new v1.3.0 LethalMin reflective scan attempted to Harmony-patch inherited/non-declared Pikmin methods. HarmonyX warned against these targets and the log terminated during the scan before its completion marker.

Do not retest S1.42D.

## Historical S1.42E startup-safe candidate

Profile:
`Profiles/LC V1 S1.42E Startup Safe Enemy Regression.r2z`

SHA-256:
`4df5d6417aad35ad327b183eb2dd25ecb6bd20382840198f74f0201007d57348`

Status:
**built successfully; awaiting runtime validation.**

Compatibility DLL SHA-256:
`caf20c785245396d9f31ff32b556cbe75d64b87a5a676807184093a6cef78eab`

S1.42E retains the S1.42D test goals but:
- only patches declared methods on LethalMin `*PikminEnemy` adapter classes;
- patches only local `BitePikmin`, `GrabPikmin`, `GrabPikminWithTongue` methods;
- does not patch RPC wrappers or generic PikminAI/PikminItem methods;
- removes the inherited `GrabbableObject.Start` Jetpack Harmony target and uses narrow loaded-Item asset targeting instead.

First runtime gate:
reach Main Menu without crash.
