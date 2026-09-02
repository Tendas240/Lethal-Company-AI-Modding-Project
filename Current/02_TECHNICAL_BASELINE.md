# 02 — Technical Baseline

## Current manifest

S1.31 export:

- 176 manifest entries
- 173 active
- 3 explicitly disabled

Explicitly disabled:

- `Kittenji-Dont_Touch_Me`
- `Reiko88-Observer`
- `SoftDiamond-BrutalCompanyMinusExtraReborn`

Relevant active versions include:

- CodeRebirth 1.6.9
- DawnLib 0.9.25
- CompanyBuildingEnhancements 2.6.0
- LethalLevelLoader 1.7.12
- Spawn Cycle Fixes 1.2.2
- LethalMinNightly 1.1.108
- RandomEnemiesSize 1.1.20
- RollingGiant 2.6.3
- SirenHead 2.0.7
- Scopophobia 1.3.4
- GeneralImprovements 1.5.5
- ImmortalSnailFork 0.1.1

The full list is in `Current/Aktive_Modliste_S1.31.txt`.

## S1.31 vanilla indoor power caps

| Moon | Indoor Power |
|---|---:|
| Experimentation | 4 |
| Assurance | 8 |
| Vow | 10 |
| Embrion | 12 |
| Rend | 16 |
| Dine | 16 |
| Offense | 20 |
| Adamance | 22 |
| Artifice | 22 |
| Liquidation | 22 |
| March | 24 |
| Titan | 32 |
| Gordion / Company | 0 |

The user explicitly requested S1.30 values “minus 4”. This preserves ordering and absolute differences, but not exact mathematical ratios.

## S1.31 custom/external indoor power caps

| Moon | Indoor Power |
|---|---:|
| EGypt | 20 |
| PsychSanctum | 18 |
| Abaddon | 36 |
| Cabal | 20 |
| Arcadia | 16 |
| Argent | 18 |
| Zenit | 18 |
| Lament | 10 |
| Flicker | 14 |
| Shutter | 0 |
| Pareidolia | 36 |
| Vigilance | 18 |
| Bozoros | 32 |
| Sanguine | 20 |
| Spectralis | 22 |
| The Iris | 36 |
| Black Mesa | 28 |
| Oxyde | not separately controllable in the current export |

Do not guess an Oxyde value unless the relevant external configuration/source becomes available.

## 26 equal-weight interiors

All intended at Weight 100 on normal moons:

1. Facility
2. Haunted Mansion
3. Mineshaft
4. Bunker
5. Drains
6. Substation
7. Liminal Facility
8. Storehouse
9. Tower
10. Circus Facility
11. Atlantean Citadel
12. Deep Sewers
13. Fractured Complex
14. Greenhouse
15. Art Gallery
16. Decrepit store
17. Expanded facility
18. Expanded Mineshaft
19. Grand Armory
20. Spooky manor
21. ScoopyCastle
22. Slaughterhouse
23. Storage Complex
24. Rubber Rooms
25. Toy Store
26. Black Mesa

Runtime previously confirmed all 26 viable at Weight 100 with an empty unviable list.

## SpawnCycleFixes

Spawn Cycle Fixes 1.2.2 remains active.

Approximate consistent spawn waves historically identified:

- 07:39
- 09:00
- 11:00
- 13:00
- 15:00
- 17:00
- 19:00
- 21:00
- 23:00

Do not disable it blindly. If enemies still feel too late, investigate probability/amount curves rather than merely removing SpawnCycleFixes.

## Beehives / Red Locust Bees

Offense is not a normal vanilla Bee/Beehive moon, so the absence of Beehives there is not evidence of a bug.

The raw vanilla Bee weights on the actual bee moons were not intentionally reduced.

Because additional daytime enemies such as GiantKiwi enlarge the pool, effective Bee percentages can be somewhat lower than vanilla.

Approximate documented comparison:

| Moon | Before added GiantKiwi | Extended pool |
|---|---:|---:|
| Experimentation | 14.9% | 13.7% |
| Assurance | 22.4% | 20.5% |
| Vow | 20.1% | 15.4% |
| March | 36.3% | 30.8% |
| Adamance | 10.9% | 10.0% |
| Artifice | 15.6% | 14.4% |

Only compensate Bee chance if several runs on actual Bee moons show a reproducible problem.

## Dungeon music candidates

### Haunted Harpist / Phantom Piper

Musical enemy source. Can sound like a “theme song” from several rooms away.

A spatial/directional song during normal exploration points more strongly toward this source.

### PizzaTowerEscapeMusic

Event/escape music source. Apparatus removal is a strong suspected trigger in the current configuration.

A global song beginning at/after Apparatus removal points more strongly toward this source.

The exact source of the user's observed theme song is not yet proven.

## Vanilla Turret observation

One disabled vanilla Turret was found during the latest documented run.

No log evidence proves a global Turret defect.

Legitimate disable paths exist, including terminal/hacking mechanisms. Do not modify Turret logic unless this repeats with player interaction ruled out.
