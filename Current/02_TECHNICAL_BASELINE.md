# 02 - Technical Baseline

## Current manifest: S1.39

Profile:

`Profiles/LC V1 S1.39 Cleanup Health Pikmin Shield.r2z`

- 179 Thunderstore manifest entries
- 173 active
- 6 explicitly disabled
- plus one project-local cumulative compatibility plugin embedded in the archive and available separately under `Patches/`

Explicitly disabled:

- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8
- SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0

The exact package list is in `Current/Aktive_Modliste_S1.39.txt`.

## S1.38 package additions carried into S1.39

- Rumi-FixCameraResolution 1.5.3
- LethalResonance-LETHALRESONANCE 4.7.8
- loaforc-loaforcsSoundAPI_LethalCompany 1.0.2

Existing compatible dependencies were intentionally kept without downgrade, including loaforc-loaforcsSoundAPI 2.0.12, ButteryStancakes-EnemySoundFixes 1.9.14, Hardy-LCMaxSoundsFix 1.2.0 and BepInExPack 5.4.2305.

## Required local plugin

`Patches/S139CompatibilityFixes/`

Fallback package:

`Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip`

Embedded DLL:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

Expected runtime marker:

`S1.39 Compatibility Fixes loaded.`

### Functions

1. ship-door anti-lockout behavior;
2. DoorAudit / DoorFailsafe diagnostics;
3. complete EnemyScan terminal listing;
4. natural CodeRebirth currency/credit filtering from normal scrap generation;
5. natural CodeRebirth currency map-object filtering from indoor hazard generation;
6. natural CodeRebirth Flash Turret suppression;
7. CodeRebirth utility-kill Pikmin/Puffmin guard, intended to close the observed Autonomous Crane kill path.

### Gale import requirement

Use **Advanced options -> Import all files**. If the marker is absent, import the local-mod ZIP manually.

## S1.39 targeted config values

### Biodiversity Ogopogo

- `OgopogoEnabled = false`
- `EnableVermin = false`

No other Biodiversity component was deliberately disabled by this change.

### GeneralImprovements

- `AddHealthRechargeStation = true`

This value was already true in the canonical S1.36 baseline. S1.39 preserves and explicitly verifies it. Runtime full-heal acceptance remains pending.

### LethalMin CodeRebirth compatibility

All of these are asserted false in the S1.39 build:

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

The direct S1.39 kill guard exists because the CodeRebirth Autonomous Crane still killed a Pikmin in runtime even with the crane settings false. Separately, S1.36 runtime testing confirmed the microwave interaction no longer affected Pikmins; this is an accepted behavior unless a regression is observed.

## FixCameraResolution baseline

S1.38/S1.39 intended settings:

- internal render target: 2560x1440
- `Auto Size = false`
- `Check Resolution Every Frame = false`
- HUD fixed aspect ratio: true
- HDRP Bloom/Fog/Shadow/Post Processing/Vignette: Vanilla
- Antialiasing: None
- Visor: preserved

S1.38 runtime log confirms FixCameraResolutions 1.5.3 loaded, and the user explicitly reported the result worked as intended. Keep the fixed 2560x1440 configuration unless the display setup changes.

## Lethal Resonance baseline

Only these three groups are enabled:

- `EnabledSounds:old_bird`
- `EnabledSounds:old_bird_footsteps`
- `EnabledSounds:old_bird_speaker`

All other Lethal Resonance sound/config toggles are false.

Runtime plugin/SoundAPI loading occurred in S1.38, but an actual Old Bird encounter validating the intended replacement set is still pending.

## Indoor power caps

Unchanged from S1.31. Do not rebalance while testing unrelated S1.39 fixes.

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
| The Iris | 36 |
| Black Mesa | 28 |
| Oxyde | not separately controllable in current export |

Do not guess an Oxyde value.

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

Black Mesa uses its own DawnLib/config path; do not double-register through LLL.

## LethalMin baseline

Core Pikmin settings:

- No Knock Back = true
- Invinceable Pikmin = true
- Pikmin Die In Player Death Zones = false

Attack Blacklist must retain the current longer list plus `Leaf boy`; do not replace it with older shorter handover values.

## Mirage baseline

Desired/current latest-runtime-confirmed after **manual user setting**:

- localPlayerVolume=0.5
- neverDeleteRecordings=true
- allowRecordVoice=true
- muteVoiceMimic=false

The user had to set `neverDeleteRecordings=true` manually in the Main Menu/LethalConfig; the profile import did not reliably apply it. The later S1.38 log confirmed the manual value was active. Do not treat the embedded/profile copy as sufficient proof.

Paths:

- settings: `<Lethal Company>/Mirage/settings.json`
- recordings: `<Lethal Company>/Mirage/Recording`

## Identified S1.38 enemy: The Cabinet

The user's four-legged Jester-like indoor enemy was identified as **Cabinet** from `Cabinet_crew-TheCabinet 1.12.1`. The S1.38 runtime log explicitly recorded `Spawning Cabinet from vent` followed by `TheCabinet` debug output. This is an identification fact, not a request to disable the enemy.

## SpawnCycleFixes

Spawn Cycle Fixes 1.2.2 remains active. Do not disable it blindly if enemies feel late; inspect spawn probability/amount curves first.

## Known warnings / issues not to overreact to

- SellMyScrap warnings about ShipInventoryUpdated should only be acted on if user-facing functionality is actually broken.
- InjectionLibrary warnings for Mirage/Opus native DLLs are expected scanner noise for non-.NET binaries.
- CodeRebirth can log Weather Registry unavailable while continuing to load; treat as compatibility warning unless missing weather content matters.
- NavMeshInCompany NodeHelper warnings remain known; investigate only if Company navigation is actually broken.
