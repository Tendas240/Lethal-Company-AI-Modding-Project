# 07 — Binding Future Roadmap: BCMER and Interior Expansion

This file is binding unless the user later changes the plan.

## Required sequence

Historical planned sequence:

**S1.40B accepted -> S1.41 BCMER 1.71.0 accepted -> S1.42A Interior Config Seed -> runtime config generation -> analyze/tune -> final S1.42 acceptance.**

The seed and two isolated regression stages have now happened. Do not collapse future phases together; isolation remains intentional so regressions can be attributed.

## Current progress checkpoint — after S1.42C

Completed:
- S1.42A seed built and runtime-generated real configs/IDs.
- 52 total dungeon flows discovered.
- exact CullFactory IDs: `junkrooms`, `shatteredrooms`.
- S1.42A LethalModDataLib NRE discovered.
- S1.42B null-safe LMDL guard runtime-confirmed.
- S1.42C Thumper/Puffer Pikmin guards built; LMDL fix remained healthy.
- S1.42C revealed a broader LethalMin enemy grab/bite + Invincible Pikmin leader-state bug.

Still pending before final S1.42:
- generic grab/bite + invincible follower-state repair;
- targeted Thumper/Puffer validation;
- equal interior probability tuning;
- CullFactory exceptions;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- final runtime acceptance.

`BuildSpecs/S1.42D_PLAN.md` is draft-only and not authorized to build automatically.

---

# S1.41 — BCMER reactivation

## Version rule

Current accepted S1.41 profile contains:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

**enabled**.

S1.41 uses exact 1.71.0 and has passed runtime acceptance.

Do **not** silently upgrade to BCMER 2.0.0. The 2.0 branch is a major compatibility change and must be a separate explicit future migration, if ever desired.

## Client requirement

BCMER must be present/consistent on all clients for multiplayer.

## Rain-related BCMER events to disable

All four BCMER rain-related event routes must be disabled.

Internal/config sections found in source:

1. `Raining`
   - visible README/event language may call it "Rainy"
   - executes rainy atmosphere

2. `HeavyRain`
   - executes Rainy + Flooded + Stormy

3. `AllWeather`
   - can include Rainy/Foggy/Stormy/Flooded/Eclipsed from its random weather set

4. `Hurricane`
   - custom/modded weather event with strong rain/wind behavior
   - may depend on WeatherRegistry/custom weather presence
   - disable defensively even if current profile does not expose WeatherRegistry functionality

BCMER source config generation uses event section `e.Name()` and key:

`Event Enabled?`

Setting false prevents that event from occurring.

Accepted S1.41 configuration shape, verified again in post-run runtime configs:

`BrutalCompanyMinusExtraReborn/VanillaEvents.cfg`

```ini
[Raining]
Event Enabled? = false

[HeavyRain]
Event Enabled? = false

[AllWeather]
Event Enabled? = false
```

`BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`

```ini
[Hurricane]
Event Enabled? = false
```

Name trap:
- visible "Rainy" can map to internal/config section `Raining`.

`WelcomeToTheFactory` includes `HeavyRain` in `EventsToSpawnWith`, but EventManager removes disabled events from that list. Therefore disabling HeavyRain closes that route; do not disable WelcomeToTheFactory solely for rain.

Do **not** disable unrelated events unless user asks:
- Gloomy = fog
- Windy = Tornado/custom wind
- MeteorShower etc. are not rain

Natural vanilla Lethal Company `Rainy` weather remains allowed. Requirement is specifically BCMER rain-related events off.

## Spawn ownership constraints

BCMER must not silently become the permanent owner of the project's established spawn architecture outside its events.

Accepted S1.41 uses the actual 1.71.0-generated keys:
- `Experimental Dont Handle Power? = true`
- `Experimental Dont Handle Spawn Chance? = true`
- `Let Brutal handle properties outside of events? = false`
- `Enable Randomizer? = false`

Goal remains:
- BCMER may change things as part of its events;
- outside events, existing project spawn weights/power/ownership should remain authoritative unless user explicitly chooses otherwise;
- Randomizer behavior should remain disabled unless explicitly wanted.

## S1.41 compatibility result / carry-forward warnings

Confirmed for acceptance:
- GeneralImprovements compatibility requirement was handled with `SpeakerPlaysIntroVoice=true`.
- BCMER 1.71.0 loaded and normal events ran.
- post-run config generation was complete enough to verify ownership/rain guards.

Carry forward as monitor-only unless user-facing breakage appears:
- DawnLib/custom hazard compatibility can still be incomplete in edge cases.
- Black Mesa Half Life Moon Interior may have limited support for some BCMER custom hazards such as barnacles/trip mines.
- S1.41 emitted a ButlerSword missing-script warning without blocking the run.

Do not retroactively combine interior additions with S1.41. S1.41 is accepted and frozen as the BCMER reactivation baseline.

---

# S1.42A — Interior Config Seed

S1.42A was built through the repository-first GitHub Actions workflow on 2026-09-03 and passed automated QC. Do not rebuild it by default.

Candidate:
`Profiles/LC V1 S1.42A Interior Config Seed.r2z`

SHA-256:
`70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

Accepted gameplay baseline remains S1.41. S1.42A runtime generation has already completed; do not rerun it by default.

Purpose:
- allow LLL/JLL/DawnLib/content mods to generate their real config sections;
- discover actual registered IDs;
- discover actual CullFactory identifiers;
- discover any runtime dependency behavior.

## Binding interior packages

These are required planned additions, not optional suggestions:

1. `Beaniebe-Liminal_House 1.1.6`
2. `MelanieMelicious-Melanie_Interiors`
   - researched current target: 1.2.1 unless a newer version is deliberately adopted after fresh audit
3. `Beaniebe-Deepcore_Mines 1.0.9`
4. `MrKixcat-Junkrooms 4.0.2`
5. `Beaniebe-Super_Market 1.0.3`
6. `MrKixcat-Shatteredrooms 2.1.6`
7. `Lead Interiors 0.0.7`
8. `Dungeons_Ultimately_Lacking_Liveliness 1.8.8`

Do not install `Beaniebe-Beanies_Interiors 1.0.6` if it duplicates the already-present standalone Storage Complex. Use the selected standalone interiors.

## Current dependency infrastructure already present

Known current stack includes:
- BepInExPack 5.4.2305
- LethalLevelLoader 1.7.12
- JLL 1.10.1
- DungeonGenerationPlus 1.5.0
- BeanieLib 1.0.9
- itolib 0.9.3
- WaterAssetRestorer 1.0.1
- LethalLib 1.2.0
- HookGen/AutoHookGen infrastructure
- CullFactory 2.0.7
- LethalSponge 1.4.3

Still audit each package's current manifest at build time. Do not assume old researched metadata is unchanged.

## S1.42A runtime generation result

Completed.

Evidence:
`RuntimeEvidence/S1.42A/20260902T224318Z/`

The seed produced the full generated config set and runtime registration data needed for tuning.

---

# S1.42 — final interior tuning

Use the actual generated configs/IDs.

## Global equal-interior probability invariant

This is a **binding long-term architecture rule**, including all future interior additions:

- every registered interior should have the **same selection probability as every other interior on every moon**;
- use a common project weight (normally Weight 100) for every interior/moon pairing when LethalLevelLoader or the native owner permits direct weighting;
- no interior should be made rarer or more common merely for theme, moon preference, package defaults, or author balancing recommendations;
- whenever a future mod adds one or more interiors, normalize those new interiors into this equal-probability architecture before final acceptance;
- package count is irrelevant: a package that adds six interiors contributes six independently equal-weight interiors, not one package-level share;
- Black Mesa/native-owner content must reach the same effective probability without duplicate registration.

**Technical restriction handling:**
- the user's target is still equality on *all* moons;
- if an author hard-blocks an interior on a moon, or forcing it would create a crash/generation/geometry incompatibility, treat that as a compatibility issue to investigate rather than a desired balancing exception;
- do not blindly override an explicit hard block until its technical reason is understood and runtime-tested;
- any unavoidable exception must be documented explicitly and must be technical, not a rarity/balancing choice.

Current example: Shatteredrooms explicitly excludes Experimentation and Embrion. That remains temporarily preserved until we determine whether the restriction is technically required. The desired final architecture is still equal availability/probability everywhere if safely achievable.

Also:
- do not fabricate IDs;
- do not double-register content.

The final interior count will be **more than +8**, because some packages contain multiple interiors. Count actual registered interiors before updating the architecture documentation.

## Package-specific notes

### Liminal House 1.1.6
V81-compatible in prior research. Existing dependency stack should already cover it, but re-audit manifest before build.

### Melanie Interiors
Contains at least Museum + Mausoleum.
- researched target 1.2.1 fixed a latest-LLL/DawnLib incompatibility involving door sockets;
- default weights vary by moon;
- normalize new entries to Weight 100 where supported after generated configs exist.

### Deepcore Mines 1.0.9
Five-floor mine with elevator/ladder/dynamite mechanics. Existing dependency stack appeared compatible in prior research. Test carefully for routing and multi-floor generation.

### Junkrooms 4.0.2
Known CullFactory incompatibility.
Author guidance: add `junkrooms` to CullFactory `Disable culling for interiors`.
Verify exact current config syntax and actual registered identifier before editing.

### Super Market 1.0.3
Recent/less mature in prior research. Uses existing LLL/HookGen infrastructure. Test carefully.

### Shatteredrooms 2.1.6
Known CullFactory incompatibility.
Cannot appear on Experimentation/Embrion per author; preserve that restriction.
Determine actual registered CullFactory interior ID from generated config/package/runtime; do not guess.

### Lead Interiors 0.0.7
Large/fresh package with:
- Lead Factory
- Lantern Manor
- Goldstay Hotel
- Belleville Apartments
- Crimson Keep

Prior dependency research included:
- DungeonGenerationPlus
- BeanieLib
- BepInEx
- LLL
- JLL
- itolib
- WaterAssetRestorer

Some functionality reportedly does not work without `Boom_Scraps`.
Before final integration determine whether Boom_Scraps is:
- a hard manifest dependency,
- optional integration,
- or required only for specific features.

Do not blindly add Boom_Scraps unless required for the desired full behavior or actual package dependency.

### Dungeons Ultimately Lacking Liveliness 1.8.8
Prior research showed dependency on:

`MaxWasUnavailable-LethalModDataLib 1.2.2`

LethalModDataLib is **not** permanently banned. Historical chronology only says the old NRE disappeared after a ShipWindows update and LethalModDataLib removal; causality was never proven.

For DULL:
- LethalModDataLib 1.2.2 was reintroduced in S1.42A;
- its upstream null-instance NRE was fixed by the project compatibility plugin in S1.42B;
- S1.42B and S1.42C runtime-confirmed `ModDataHandler initialised!` plus moddata load/save;
- keep the guard while LethalModDataLib 1.2.2 remains present.

## CullFactory

Before S1.42 final:
- exact runtime IDs are now confirmed:
  - Junkrooms = `junkrooms`
  - Shatteredrooms = `shatteredrooms`
- add these exact disable-culling exceptions;
- do not guess alternate IDs.

## Duplicate registration rule

Avoid:
- pack + standalone duplicate interiors;
- LLL registration for content already owned by DawnLib/JLL/native mod config;
- duplicate Black Mesa registration.

## Final acceptance

S1.42 should only be accepted after runtime checks for:
- successful interior generation;
- no duplicate dungeon registrations;
- correct Weight100 architecture where intended;
- preserved author safety restrictions;
- CullFactory exceptions working;
- no LethalModDataLib save/netcode regression;
- no Boom_Scraps dependency failure;
- no new severe routing/elevator/navmesh regression.


---

# Additional binding S1.42 tuning decisions

## BCMER fixed global EventType distribution

Use equal base probability for all eight BCMER EventTypes:
12.5% each.

Keep:
`Use custom weights? = false`

Set every EventType scale to:
`12.5, 0, 12.5, 12.5`

This is intended to remove moon/day/difficulty drift from the EventType base distribution.

## Mausoleum fog

`MelanieMausoleum` was reported much too foggy in S1.42A.

Reduce fog only for this interior. Do not globally reduce fog.

## Generic Pikmin state blocker

Before final S1.42 acceptance, resolve or safely contain the generic LethalMin enemy grab/bite + Invincible Pikmin leader-state bug confirmed with Baboon Hawk in S1.42C.

Do not solve it by blacklisting all enemies.
