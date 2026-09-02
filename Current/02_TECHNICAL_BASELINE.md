# 02 — Technical Baseline

## Current canonical manifest: S1.41

Profile:

`Profiles/LC V1 S1.41 BCMER Reactivation.r2z`

SHA-256:

`d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`

Status:

**runtime accepted**

Manifest:
- 179 Thunderstore entries
- 174 enabled
- 5 explicitly disabled
- plus one project-local cumulative compatibility plugin

Explicitly disabled:
- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8

Exact package list:

`Current/Aktive_Modliste_S1.41.txt`

Readable exact profile contents:

`ProfileSources/S1.41/`

## Required project-local plugin

Source:

`Patches/S139CompatibilityFixes/`

Fallback package:

`Patches/S139CompatibilityFixes/Tendas-S139CompatibilityFixes-1.0.0.zip`

Embedded DLL:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

Expected runtime marker:

`S1.39 Compatibility Fixes loaded.`

Functions:
1. ship-door anti-lockout;
2. DoorAudit / DoorFailsafe diagnostics;
3. complete EnemyScan terminal output;
4. normal-scrap CodeRebirth Currency filtering;
5. defensive late map-object Currency filtering;
6. defensive Flash Turret filtering;
7. direct CodeRebirth utility-kill Pikmin/Puffmin guard.

The late map-object Currency filter is defense-in-depth only. S1.39 runtime proved it cannot replace the DawnLib-native config control.

### Gale import

Use **Advanced options -> Import all files**.

## Accepted CodeRebirth/DawnLib natural-spawn control

Critical post-run-retained values in S1.41:

```ini
[General]
Clean Unusued Configs = false

[Merchant Options]
Coin | Allow Editing Config = true
Coin | Inside Moon Spawn Weights =
Coin | Inside Interior Spawn Weights =

Crisp Dollar Bill | Allow Editing Config = true
Crisp Dollar Bill | Inside Moon Spawn Weights =
Crisp Dollar Bill | Inside Interior Spawn Weights =

Wallet | Allow Editing Config = true
Wallet | Inside Moon Spawn Weights =
Wallet | Inside Interior Spawn Weights =

[FlashTurret Options]
Flash Turret | Allow Editing Config = true
Flash Turret | Is Inside Hazard = false
Flash Turret | Inside Moon Spawn Weights =
Flash Turret | Inside Interior Spawn Weights =
```

Do not blank or otherwise alter `Money | Enemy Drop Rates` as collateral damage. The project requirement concerns natural dungeon generation, not dedicated CodeRebirth money-drop systems.

Historical root cause:
- S1.40 failed because CodeRebirth regenerated defaults.
- S1.40A made `Clean Unusued Configs=false` survive, but per-content `Allow Editing Config=false` still caused author defaults to win.
- S1.40B opened only the relevant edit gates and passed.
- S1.41 post-run evidence confirmed the S1.40B fix survives with BCMER enabled.

## Accepted BCMER baseline

Exact package:

`SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0`

Do not silently upgrade to 2.0.0. A 2.0 migration, if ever desired, is a separate future stage.

Post-run-retained guard:

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

Disabled BCMER rain-event routes:
- Raining
- HeavyRain
- AllWeather
- Hurricane

Natural vanilla Rainy weather remains allowed.

S1.41 runtime selected ordinary BCMER events and did not expose a severe startup/event regression.

Runtime evidence:

`RuntimeEvidence/S1.41/20260902T215804Z/`

## Stable gameplay/config decisions

### Biodiversity
- `OgopogoEnabled=false`
- `EnableVermin=false`

### GeneralImprovements
- `AddHealthRechargeStation=true`
- desired behavior: ship recharge station fully heals player
- runtime acceptance of the full-heal behavior still pending
- `SpeakerPlaysIntroVoice=true` is compatible with the accepted BCMER 1.71.0 reactivation baseline.

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

## Global equal-weight interior architecture

**Binding invariant:** every registered interior is intended to have the same effective selection probability as every other interior on every moon, including interiors added in future builds. The common project target is Weight 100 per interior/moon pairing where the owning system supports direct weighting.

This is not merely a rule for "normal moons" or for the current 26 interiors. New interiors must be normalized into the same architecture before final acceptance. Package defaults and thematic moon preferences do not override this project rule.

If an interior is explicitly hard-blocked by its author or proves technically unsafe on a moon, treat that as a compatibility issue to investigate. Do not silently convert such a block into a permanent balancing exception. Until technically validated, explicit hard blocks remain protected in test builds.

26 pre-S1.42A interiors:

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


## Repository-first build baseline

GitHub is the canonical build workspace.

Use:
- `BuildSpecs/current.json`
- `BuildSystem/profile_builder.py`
- `.github/workflows/profile-build.yml`
- `ProfileSources/<build_id>/`
- `RuntimeInbox/Current/`
- `RuntimeEvidence/`

Do not ask the user to run local PowerShell profile-build scripts or maintain a local repository clone while the required base profile is online.

Current S1.42A candidate:

`Profiles/LC V1 S1.42A Interior Config Seed.r2z`

SHA-256: `70f2c42655ed6bcea7630dc70a0de37134ae8ebfc302491a6f7cc7d3a47929fe`

Status: GitHub-Actions build verified; runtime config-generation seed test pending. S1.41 remains the accepted gameplay baseline.

Plan / runtime procedure:

`BuildSpecs/S1.42A_PLAN.md`

## New non-blocking regression surface

Mineshaft elevator + large Pikmin group:
- player clipped through moving elevator floor once in S1.41;
- died from fall/gravity damage;
- many NavMesh-agent creation failures appeared around the event;
- causality is not proven;
- BCMER is not implicated by current evidence.

Track during future interior/elevator tests without blocking the accepted S1.41 baseline.
