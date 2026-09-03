# 00 — Current State

**Canonical project state:** S1.41  
**Handover refreshed:** 2026-09-03  
**Current gameplay profile:** `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
**Current profile SHA-256:** `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`  
**Latest runtime-tested profile:** `Profiles/LC V1 S1.41 BCMER Reactivation.r2z`  
**Latest runtime result:** S1.41 accepted  
**Game:** Lethal Company V81

## S1.41 runtime acceptance

The complete S1.41 evidence was ingested online under:

`RuntimeEvidence/S1.41/20260902T215804Z/`

The ingestion workflow completed successfully and preserved:
- `LogOutput.log`
- `CodeRebirth.cfg`
- full `BrutalCompanyMinusExtraReborn/` config ZIP, including extracted configs.

BCMER runtime:
- exact `BrutalCompanyMinusExtraReborn 1.71.0` loaded and finished patching;
- ordinary BCMER events executed: Arachnophobia + ScarceOutsideScrap, with LeaflessTrees as an additional event;
- observed event MapMultipliers did not show a permanent baseline takeover in this run;
- no severe BCMER startup/landing/event-selection regression was observed.

Post-run BCMER config retained:
```ini
[Events Features]
Disable all events? = false

[Mod Compatibility]
Experimental Dont Handle Power? = true
Experimental Dont Handle Spawn Chance? = true
Let Brutal handle properties outside of events? = false

[Randomizer]
Enable Randomizer? = false
```

Post-run BCMER rain-event routes remained disabled:
- `Raining`
- `HeavyRain`
- `AllWeather`
- `Hurricane`

S1.40B CodeRebirth regression guard also survived:
- `Clean Unusued Configs = false`
- Coin/Bill/Wallet editing gates true
- Coin/Bill/Wallet inside moon/interior weights blank
- Flash Turret editing gate true
- `Flash Turret | Is Inside Hazard = false`
- Flash Turret inside weights blank

No natural Currency/Flash-Turret regression was identified in the S1.41 test.

**S1.41 is accepted.**

## New non-blocking issue — Mineshaft elevator + large Pikmin group

During the accepted S1.41 run, the user clipped through the Mineshaft elevator floor while descending with many Pikmin and died from fall damage.

The log shows:
- many `Failed to create agent because it is not close enough to the NavMesh` warnings around the elevator period;
- Coroner recorded gravity/fall damage;
- the elevator completed its movement shortly around the death window.

This does **not** currently prove that Pikmin physically pushed the player through the floor, and there is no evidence that BCMER caused it.

Track as a separate regression surface:
**Mineshaft elevator + large Pikmin group / NavMesh crowding**.

Do not block S1.42A solely on this one occurrence, but test elevators carefully in later interior work.

## Repository-first automation

Repository-first migration is complete. Future builds use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`

No local repository clone or local PowerShell build chain is required.

## Binding next stage

**S1.42A runtime config-generation seed test**

S1.42A is now built and automation-verified:

`Profiles/LC V1 S1.42A Interior Config Seed.r2z`

SHA-256:

`70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

Automated QC:
- 188 Thunderstore entries;
- 183 enabled / 5 disabled;
- exact eight binding interior packages added;
- DULL hard dependency LethalModDataLib 1.2.2 added;
- only `export.r2x` differs from accepted S1.41;
- no config/DLL/archive-member collateral changes;
- Boom_Scraps intentionally not added;
- readable snapshot at `ProfileSources/S1.42A/`.

S1.42A is **not runtime-accepted yet**. The accepted gameplay baseline remains S1.41.

Next: import S1.42A with Gale **Advanced options -> Import all files**, reach Main Menu, host/load, land on a normal moon, allow a dungeon to generate, exit, then upload complete `BepInEx/config/` ZIP + `LogOutput.log` to `RuntimeInbox/Current/`.

See `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`, `Current/12_HANDOVER_S1.41_TO_S1.42A.md`, and `BuildSpecs/S1.42A_PLAN.md`.


## S1.42A runtime seed result

Runtime evidence has been ingested at:

`RuntimeEvidence/S1.42A/20260902T224318Z/`

Result:
- seed/config-generation objective succeeded;
- 52 ExtendedDungeonFlows registered versus 26 in S1.41;
- 26 new flow IDs are now known;
- Mausoleum generated successfully on Offense;
- CullFactory IDs `junkrooms` and `shatteredrooms` are confirmed;
- generated weights are not yet normalized;
- **LethalModDataLib 1.2.2 throws a new initialization NullReferenceException** and blocks clean S1.42 acceptance;
- S1.41 remains the accepted gameplay baseline.

Detailed evidence: `Current/13_RUNTIME_EVIDENCE_S1.42A_INTERIORS.md`.

New BCMER requirement: final tuning should use fixed global EventType weights independent of difficulty. Exact user percentages are pending.


## S1.42B isolated LMDL guard candidate

Built and automation-verified:

`Profiles/LC V1 S1.42B LMDL NRE Guard.r2z`

SHA-256:

`8523754926e3f67c0ccef5aee976cbe72ab976f997876c59b51fedcfb293befe`

Purpose: isolate the LethalModDataLib 1.2.2 initialization NRE fix before S1.42 balancing/visual changes.

Archive delta versus S1.42A:
- compatibility DLL replaced with project plugin v1.1.0;
- `export.r2x` renamed profile;
- no other members changed.

Next binding test: import S1.42B with Gale **Advanced options -> Import all files**, host/load, generate a dungeon, exit normally, then upload `LogOutput.log` to `RuntimeInbox/Current/`.

Required success markers:
- `[LMDLGuard] Safe ModDataAttribute scan completed:`
- LethalModDataLib `Hooking up save, load and delete events...`
- LethalModDataLib `ModDataHandler initialised!`
- no LethalModDataLib initialization NRE.

Accepted gameplay baseline remains S1.41 until later final acceptance.


## S1.42B runtime result — LMDL FIX CONFIRMED

Evidence:
`RuntimeEvidence/S1.42B/20260902T231959Z/`

The project-local LethalModDataLib null-instance guard is runtime-confirmed:
- offending null Chainloader entry: `MW.MagicWesleyInteriors`;
- guard skipped exactly one null instance;
- LMDL continued to `Hooking up save, load and delete events...`;
- `ModDataHandler initialised!`;
- LMDL loaded/saved moddata;
- original S1.42A LMDL initialization NRE is resolved.

Detailed evidence:
`Current/14_RUNTIME_EVIDENCE_S1.42B_LMDL_PIKMIN.md`.


## S1.42C isolated Pikmin enemy guard candidate

Built and automation-verified:

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256:
`22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Purpose:
- make Thumper/Crawler and Pikmin ignore each other in both directions;
- prevent Puffer smoke/attack from applying LethalMin Pikmin effects;
- retain the confirmed S1.42B LMDL fix.

Exact archive delta versus S1.42B:
- `BepInEx/config/NoteBoxz.LethalMin.cfg`
- cumulative compatibility DLL
- `export.r2x`

No other changes.

Next binding test: deliberate Thumper + Puffer interaction test, then upload full `LogOutput.log` to `RuntimeInbox/Current/`.


## S1.42C runtime result

Evidence:
`RuntimeEvidence/S1.42C/20260902T235238Z/`

- LMDL fix remains confirmed healthy.
- Puffer did not spawn; Puffer Pikmin smoke guard remains unvalidated.
- A Crawler/Thumper did spawn and was later killed, with no logged Thumper-specific Pikmin grab/bite during its observed lifetime, but there was no deliberate interaction test; keep status unconfirmed.
- Later, a Baboon Hawk explicitly bit a Bulbmin and reproduced the `Leader is null when following` spam. This proves a broader LethalMin grab/bite + Invincible Pikmin state issue.
- Detailed evidence: `Current/15_RUNTIME_EVIDENCE_S1.42C.md`.

Next-build tuning requests now recorded:
- match Jetpack capacity/duration to old juijui profile; current ButteryBalance forces 40s instead of 50s, exact historical juijui value still needs evidence;
- lower CodeRebirth Functional Microwave volume from 1 to target 0.7 with its edit gate enabled.
