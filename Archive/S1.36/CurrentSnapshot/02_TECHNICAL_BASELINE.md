# 02 — Technical Baseline

## Current manifest: S1.36

Profile:

Profiles/LC V1 S1.36 Handover Clean Baseline.r2z

- 176 Thunderstore manifest entries
- 170 active
- 6 explicitly disabled
- plus one required project-local compatibility plugin embedded in the archive and available separately under Patches/

Explicitly disabled:

- AJB-Keep_hangar_ship_door_closed 1.0.0
- zealsprince-Malfunctions 1.10.3
- Reiko88-Observer 2.0.1
- ProjectSCP-SCP999 2.4.0
- Kittenji-Dont_Touch_Me 1.2.8
- SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0

The full package list is in Current/Aktive_Modliste_S1.36.txt.

## Required local plugin

Patches/S135CompatibilityFixes/

Package:

Patches/S135CompatibilityFixes/Tendas-S135CompatibilityFixes-1.0.0.zip

Embedded DLL inside S1.36:

BepInEx/plugins/Tendas-S135CompatibilityFixes/S135CompatibilityFixes.dll

Functions:

1. ship-door anti-lockout behavior,
2. door audit logging,
3. EnemyScan complete-list patch.

### Gale import requirement

Use **Advanced options → Import all files** when importing S1.36.

If BepInEx does not log S1.35 Compatibility Fixes loaded, import the local-mod ZIP manually into the same profile.

## Package versions vs runtime plugin versions

The export lists Thunderstore package versions. Current logs prove that some packages contain assemblies whose internal plugin versions differ.

For code/error analysis, prefer the newest runtime log over the manifest when they disagree.

Examples from current runs:

- SirenHead package 2.0.7 → runtime plugin 2.0.3
- ImmortalSnailFork package 0.1.1 → runtime plugin 0.1.0
- Black Mesa package 3.4.4 → runtime plugin 3.4.1
- Coroner package 2.4.1 → runtime plugin 2.3.0
- darmuhsTerminalStuff package 3.10.2 → runtime plugin 3.10.1
- Lethal Doors Fixed package 1.2.1 → runtime plugin 1.2.0
- FairAI package 1.6.1 → runtime plugin 1.6.0

Do not silently treat these as package corruption; package version and assembly/plugin version can legitimately differ. Always state which source is being used.

## Indoor power caps

Unchanged from S1.31.

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

These came from the explicit S1.30-values-minus-4 decision. Do not rebalance them while testing unrelated fixes.

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

Runtime previously confirmed all 26 viable at Weight 100 with an empty unviable list.

Black Mesa uses its own DawnLib/config path; do not double-register through LLL.

## LethalMin baseline

Core Pikmin settings:

- No Knock Back = true
- Invinceable Pikmin = true
- Pikmin Die In Player Death Zones = false

Current S1.36 Attack Blacklist line:

Docile Locust Bees,Manticoil,Red Locust Bees,Blob,Nemo,InternNPC,BellCrab,Nancy,Transporter,Janior,Peace Keeper,Guardsman,Tornado,FireStorm,Hurricane,Cabinet, Leaf boy

Do not replace this with an older shorter list. S1.32 appended Leaf boy to the existing current list.

## Mirage baseline

S1.36 carries:

localPlayerVolume=0.5  
neverDeleteRecordings=true  
allowRecordVoice=true  
muteVoiceMimic=false

Mirage paths:

- settings: <Lethal Company installation folder>/Mirage/settings.json
- recordings: <Lethal Company installation folder>/Mirage/Recording

neverDeleteRecordings=true is intentional and must remain unless the user asks otherwise.

## Ship-door compatibility patch

The S1.35/S1.36 local plugin patches HangarShipDoor.Update() with a late postfix.

Behavior only while landed and hangar closed:

- living player inside ship → doorPower forced back to 1f after vanilla Update, so power stays 100%;
- living players exist but all are outside → no refill, vanilla hydraulic drain continues and opens the door at zero;
- no living controlled players, ship leaving/orbit/ship phase, or open door → no intervention.

Inside detection uses both:

- player.isInHangarShipRoom
- StartOfRound.shipInnerRoomBounds.bounds.Contains(player.transform.position) fallback

Diagnostics:

- [DoorAudit]
- [DoorFailsafe]

The patch also logs stack traces for SetDoorClosed, SetDoorOpen, PlayDoorAnimation and Start/Stop ship-door button interactions.

AJB-Keep_hangar_ship_door_closed is disabled to avoid competing postfixes.

## EnemyScan complete-list patch

Original EnemyScan 1.2.1 only listed EnemyAI that had a ScanNodeProperties child.

S1.35/S1.36 patches only BuildEnemyCountString() so that it groups every active EnemyAI with a valid EnemyType by enemyType.enemyName.

It does not modify:

- spawn weights,
- spawn caps,
- PowerLevels,
- AI,
- ScanNodes,
- bestiary registration.

## Coin / CodeRebirth currency

Coin is CodeRebirth content, namespaced as code_rebirth:coin.

CodeRebirth Money.TryCollectCoin():

- requires a MoneyCounter supplied by the Denomination Analyzer;
- without it, displays a hint telling the player to buy the analyzer from the ship terminal;
- with it, adds the coin value to stored CodeRebirth currency and destroys/despawns the coin.

The stored currency is used by CodeRebirth merchant/vending systems.

## Puma / Feiopar

PumaAI is the internal vanilla AI class for the V80+ enemy Feiopar. Puma log lines do not imply a Puma mod is installed.

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

Do not disable it blindly. If enemies feel too late, investigate probability/amount curves rather than simply removing SpawnCycleFixes.

## Known current warnings/issues

### SCP999 startup NRE

S1.31–S1.34 logs showed Loading [SCP999 2.4.0], immediately followed by NullReferenceException in SCP999.Plugin.Awake().

S1.36 disables the package. Next runtime must verify the load/NRE is gone.

### SellMyScrap

Current logs show warnings because several methods cannot load ShipInventoryUpdated, Version=2.0.0.0. SellMyScrap otherwise continues loading. Investigate only if related functionality is broken.

### InjectionLibrary native DLL warnings

Mirage/Opus native DLLs are skipped as non-.NET assemblies by InjectionLibrary. Those scanner warnings alone are not a failure.

### CodeRebirth Weather Registry

Weather Registry not found, skipping weather content registration appears while CodeRebirth otherwise continues loading. Treat as an open compatibility warning, not a proven blocker.

### NavMeshInCompany

Missing NodeHelper script warnings remain known. Reassess only if Company navigation is actually broken.
