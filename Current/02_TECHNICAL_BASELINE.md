# 02 — Technical Baseline

## Current manifest: S1.40A

Profile:

`Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`

SHA-256:

`ab894ead158941d6f9d6c3463baab51c65486ebf6d40df8b2325fca626d966a5`

Manifest:
- 179 Thunderstore entries
- 173 active
- 6 explicitly disabled
- plus one project-local cumulative compatibility plugin

Explicitly disabled:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8
- SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0

Exact package list:

`Current/Aktive_Modliste_S1.40A.txt`

## Required local plugin

`Patches/S139CompatibilityFixes/`

Fallback package:

`Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip`

Fallback package SHA-256:

`ec02f79c56f2f3ce24c8f625be3b51cea68b5a71a2a24d3ac8b4996f02c055c1`

Embedded DLL:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

Expected marker:

`S1.39 Compatibility Fixes loaded.`

Functions:
1. ship-door anti-lockout;
2. DoorAudit / DoorFailsafe diagnostics;
3. complete EnemyScan terminal output;
4. normal-scrap CodeRebirth Currency filtering;
5. defensive late map-object Currency filtering;
6. defensive Flash Turret filtering;
7. direct CodeRebirth utility-kill Pikmin/Puffmin guard.

The late map-object filtering remains only a defense-in-depth layer; S1.39 proved it is not sufficient as the primary DawnLib Currency control.

### Gale import

Use **Advanced options -> Import all files**.

## S1.40A native CodeRebirth control

Critical config:
- `Clean Unusued Configs = false`
- Coin / Crisp Dollar Bill / Wallet Inside Moon + Interior Spawn Weights blank
- Flash Turret `Is Inside Hazard = false`
- Flash Turret Inside Moon + Interior Spawn Weights blank

Do not touch `Money | Enemy Drop Rates` unless explicitly requested.

## Stable gameplay/config decisions

### Biodiversity
- `OgopogoEnabled=false`
- `EnableVermin=false`

### GeneralImprovements
- `AddHealthRechargeStation=true`
- desired behavior: ship recharge station fully heals player
- runtime acceptance of the full-heal behavior still pending
- GeneralImprovements intro-skip behavior must be audited before BCMER reactivation because BCMER documents compatibility concerns around intro skipping.

### FixCameraResolution
Accepted visual configuration:
- 2560x1440 internal target
- Auto Size false
- Check Resolution Every Frame false
- HUD fixed aspect true
- AA None
- HDRP effects Vanilla
- visor preserved

### Lethal Resonance
Only:
- `old_bird`
- `old_bird_footsteps`
- `old_bird_speaker`

All other groups false. Runtime pipeline loaded; encounter-based Old Bird validation remains open.

### Mirage
Desired/current latest confirmed:
- `localPlayerVolume=0.5`
- `neverDeleteRecordings=true`
- `allowRecordVoice=true`
- `muteVoiceMimic=false`

Mirage retention is stored outside the profile and may need manual Main Menu/LethalConfig correction after import.

Paths:
- `<Lethal Company>/Mirage/settings.json`
- `<Lethal Company>/Mirage/Recording`

### LethalMin
Core:
- No Knock Back = true
- Invinceable Pikmin = true
- Pikmin Die In Player Death Zones = false

Attack Blacklist must retain the long current list plus `Leaf boy`.

CodeRebirth compatibility toggles remain false:
- ACU Targets Winged Pikmin
- ACU Bullet Knockbacks Pikmin
- Crane Targets Pikmin
- Crane Squishes Pikmin
- Fan Knockbacks Pikmin
- Microwave Knockbacks Pikmin
- Flash Turret Knockbacks Pikmin
- Laser Turret Kills Pikmin
- Tornado Pulls Pikmin
- Compactor Squishes Pikmin

S1.36 confirmed microwaves no longer affect Pikmin. S1.39 added the direct kill guard because the crane could still kill despite config toggles.

## Indoor power caps

### Vanilla

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

### Custom/external

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
| Iris | 36 |
| Black Mesa | 28 |
| Oxyde | unknown / not separately controllable |

Never guess an Oxyde value.

## Current equal-weight interior architecture

26 current interiors, intended Weight 100 on normal moons:

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

Black Mesa uses its own DawnLib path; do not double-register through LLL.

SpawnCycleFixes 1.2.2 stays active.

## Spawn ownership

Native owners retained:
- Rolling Giant -> native config
- Shy Guy / Scopophobia -> native config
- Siren Head -> native config

Prefer one positive spawn owner per enemy. Do not force these through LLL without evidence.

## Unknown Enemy PowerLevels

Do not guess:
- Rolling Giant
- Siren Head
- Immortal Snail
- Herobrine
- Football
- Faceless Stalker
- CodeRebirth Debt Collector
- CodeRebirth Boogey Man

S1.29D remains diagnostic-only for power auditing.

## Identified enemy

The four-legged Jester-like indoor enemy is **Cabinet** from `Cabinet_crew-TheCabinet 1.12.1`. Identification only; no disable request.

## Known warnings not to overreact to

- SellMyScrap ShipInventoryUpdated warnings: act only if user-facing behavior breaks.
- InjectionLibrary native Mirage/Opus scan warnings: expected non-.NET scanner noise.
- CodeRebirth Weather Registry unavailable: compatibility warning unless missing weather content matters.
- NavMeshInCompany NodeHelper warnings: investigate only if Company navigation is actually broken.
