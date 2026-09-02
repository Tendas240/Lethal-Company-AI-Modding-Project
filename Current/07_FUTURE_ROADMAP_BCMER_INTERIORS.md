# 07 — Binding Future Roadmap: BCMER and Interior Expansion

This file is binding unless the user later changes the plan.

## Required sequence

**S1.40B accepted -> S1.41 BCMER 1.71.0 built -> S1.41 runtime test -> if accepted -> S1.42A Interior Config Seed -> runtime config generation -> collect full config + LogOutput -> analyze/tune -> S1.42 final interior build -> S1.42 test.**

Do not collapse these phases together. Isolation is intentional so regressions can be attributed.

---

# S1.41 — BCMER reactivation

## Version rule

Current profile contains:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

disabled.

S1.41 uses **exact existing 1.71.0** and is now the canonical runtime-test candidate.

Do **not** upgrade to BCMER 2.0.0 during this stage. The 2.0 branch is a major compatibility change and should be a separate future migration only.

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

Expected configuration shape, **but verify exact 1.71.0 generated file paths/keys before final build**:

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

Before S1.41 finalization, inspect actual **1.71.0-generated** config names for settings conceptually documented as:
- `Experimental dont handle spawn chance`
- `Let Brutal handle properties outside of events?`

Use the real 1.71.0 section/key names, not guesses from BCMER 2.0 documentation.

Goal:
- BCMER may change things as part of its events;
- outside events, existing project spawn weights/power/ownership should remain authoritative unless user explicitly chooses otherwise;
- Randomizer behavior should remain disabled unless explicitly wanted.

## Compatibility checks for S1.41

Audit:
- GeneralImprovements compatibility. BCMER has documented issues around intro skip; verify our current GeneralImprovements intro/launch settings before reactivation.
- DawnLib compatibility. Generally usable, but some custom hazards may not be fully handled.
- Black Mesa Half Life Moon Interior: BCMER custom hazards such as barnacles/trip mines may have limited support.
- BCMER config generation may require loading/landing on a moon and/or pulling the lever before all config files exist.

Do not combine any interior additions with S1.41. S1.41 is already built and hash-verified; only runtime acceptance remains.

---

# S1.42A — Interior Config Seed

After S1.41 is runtime-accepted, install all binding interior packages **without speculative deep tuning**.

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

## Required S1.42A runtime generation procedure

After importing S1.42A via Gale with **Advanced options -> Import all files**:

1. reach Main Menu;
2. host/load a save;
3. land on at least one normal moon;
4. allow a dungeon to actually generate;
5. exit game.

Then user provides from that exact seeded profile:
- complete `BepInEx/config/` directory, preferably ZIP;
- full `LogOutput.log`.

Only after this should exact config tuning happen.

---

# S1.42 — final interior tuning

Use the actual generated configs/IDs.

## General tuning rule

For ordinary new interiors:
- normalize to Weight 100 where technically supported and consistent with the project architecture;
- respect author-defined safety restrictions;
- do not fabricate IDs;
- do not double-register content;
- do not automatically override special moon restrictions.

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
- reintroduce LethalModDataLib only in S1.42A;
- treat it as a regression surface for save/mod-data/netcode;
- test it in isolation as part of that staged build.

## CullFactory

Before S1.42 final:
- inspect generated identifiers for Junkrooms and Shatteredrooms;
- add correct disable-culling exceptions using exact syntax;
- do not guess the IDs.

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
