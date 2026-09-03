# Permanent custom-patch safety gate

All project-local Harmony/runtime/compatibility code is governed by
`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

Key invariant: a custom patch is not considered safe because it compiles, starts, or fixes its direct symptom. Before promotion, the exact patch surface, inherited/base lifecycle, secondary responsibilities, network/state ownership, reverse direction, adjacent behavior, and runtime regressions must be checked.

Whole-component disabling is forbidden as a convenience mechanism unless the complete foreign component lifecycle has been inspected and every lost responsibility is explicitly safe to suppress. Prefer narrow prevention-only hooks and preserve native lifecycle ownership.

Every future patch-build plan must include a `Patch Safety Review` section.

---
# 02 — Technical Baseline

## Accepted gameplay baseline manifest: S1.41

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

Current source version:

**1.3.14**

Current tested technical descendant:

**S1.42S — Baboon Adapter Lifecycle Restore**

Current profile:

`Profiles/LC V1 S1.42S Baboon Adapter Lifecycle Restore.r2z`

Profile SHA-256:

`addc5f0cd2508bf821e4e8eda80aca0f94234c7f2823c9acc6e8655060790fee`

Current embedded compatibility DLL:

`BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll`

SHA-256:

`3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`

Runtime evidence:

`RuntimeEvidence/S1.42S/20260903T205550Z/`

Runtime log SHA-256:

`9e0f771144ceb1679f340d5df7ff393df92a8541d7cfe27231a60bd514c6bfea`

Focused runtime status:

**PASS**

### Important compatibility chronology

Historical failures remain important:

- v1.3.0 / S1.42D: startup crash from an over-broad LethalMin Harmony scan;
- v1.3.1 / S1.42E: startup-safe, but EnemyIsolation constructor path caused periodic Gordion freezes;
- v1.3.2 / S1.42F: constructor loop fixed, but continuous global EnemyAI scanning and Coroner Jetpack spam still caused routed-moon problems;
- v1.3.3 / S1.42G: periodic routed-moon freeze and Coroner Jetpack flood resolved;
- later versions progressively narrowed Thumper/Puffer/Baboon-Hawk interaction handling;
- v1.3.13 / S1.42R: runtime failed because the project disabled complete `BaboonBirdPikminEnemy`, suppressing inherited native death/unlatch cleanup;
- v1.3.14 / S1.42S: keeps `BaboonBirdPikminEnemy` enabled and blocks only narrow Hawk -> Pikmin entry points; focused runtime gate passed.

Canonical S1.42R corrected root cause:

`Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`

Canonical S1.42S acceptance:

`Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`

Permanent patch-safety policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

### Current runtime markers

General load:

`S1.39 Compatibility Fixes loaded.`

Native ownership:

`[LethalMinNativeOwnership] ... BaboonBirdPikminEnemy component stays enabled.`

Baboon-Hawk guard initialization:

`[BaboonHawkPikminGuard] One-way Hawk -> Pikmin protection initialized; collisionPatched=True; bitePatched=True; BaboonBirdPikminEnemy remains ENABLED so native PikminEnemy.Update death/unlatch cleanup can run.`

Forbidden old marker:

`[BaboonHawkPikminGuard] Disabled LethalMin.BaboonBirdPikminEnemy`

### Current functions

The cumulative plugin includes:

1. ship-door anti-lockout;
2. state-change DoorAudit / DoorFailsafe diagnostics;
3. BCMER DoorFailure compatibility;
4. complete EnemyScan terminal output;
5. CodeRebirth Currency natural-spawn filtering;
6. defensive map-object Currency filtering;
7. Flash Turret suppression/filtering;
8. CodeRebirth utility-kill Pikmin/Puffmin protection;
9. null-safe LethalModDataLib ModDataAttribute registration;
10. targeted Puffer-smoke Pikmin-effect removal;
11. Coroner Jetpack log-spam guard;
12. Jetpack 140-second target;
13. temporary EnemyIsolation diagnostic;
14. exact PikminAI enemy-grab prevention for proven Thumper/Baboon Hawk gaps;
15. Baboon Hawk -> Pikmin collision/bite protection that preserves LethalMin's adapter lifecycle;
16. Dead Baboon Hawk corpse guard for living Hawks.

The temporary EnemyIsolation feature is **not** a permanent gameplay rule and must be disabled in the next restore build.

### S1.42S temporary state

EnemyIsolation:

**enabled**

`Isolated Enemy Regression = true`

BCMER exact 1.71.0:

**disabled**

LethalMin:

- `Thumper Bite Limit = 3`
- `Crawler` intentionally absent from Attack Blacklist

### Next technical descendant

Planned:

**S1.42T — Normal Enemy Restore**

Not built at this baseline update.

Exact plan:

`BuildSpecs/S1.42T_PLAN.md`

Exact restore contract:

`Current/70_S1.42S_POST_GATE_NORMAL_ENEMY_RESTORE_CONTRACT.md`

S1.42T must disable only the temporary EnemyIsolation diagnostic while preserving the v1.3.14 compatibility plugin and later accepted LethalMin values. Exact BCMER 1.71.0 remains disabled for this first restore gate.

### Gale import

Profiles containing the project-local compatibility DLL must be imported with:

**Advanced options -> Import all files**.

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

Current technical base for descendants:

`Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`

SHA-256: `22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`

Status: runtime-tested technical candidate. S1.41 remains the last fully accepted gameplay baseline.

Current build spec is disabled/idle after S1.42C runtime. `BuildSpecs/S1.42D_PLAN.md` is draft-only and must not be built automatically.

## New non-blocking regression surface

Mineshaft elevator + large Pikmin group:
- player clipped through moving elevator floor once in S1.41;
- died from fall/gravity damage;
- many NavMesh-agent creation failures appeared around the event;
- causality is not proven;
- BCMER is not implicated by current evidence.

Track during future interior/elevator tests without blocking the accepted S1.41 baseline.

## Historical comparison baseline — juijui

The current technical/gameplay baselines above remain unchanged.

Separately, the project now reserves:
`References/LegacyProfiles/juijui/juijui.r2z`

for the original historical juijui profile.

This is a comparison/reference baseline only. It represents the old desired mod constellation/configuration that the modern V81 project should approach where safe and technically compatible.

After upload, extract/index its readable metadata repository-first and use the original configs as primary evidence for historical-value questions such as Jetpack capacity.


## Post-S1.42C diagnostic lineage

### S1.42D — failed startup diagnostic

Profile:
`Profiles/LC V1 S1.42D Isolated Enemy Regression.r2z`

SHA-256:
`b455bd413a6da4ac059117d8fec667053c96ffeef7e239d9188d6e514d15bd5c`

Purpose:
focused generic LethalMin state repair + isolated Thumper/Puffer/Baboon Hawk test + Jetpack/Microwave tuning.

Runtime:
**failed before usable Main Menu.**

Evidence:
`RuntimeEvidence/S1.42D/20260903T084247Z/`

Root cause:
v1.3.0 broadly scanned and Harmony-patched inherited/generated LethalMin methods; HarmonyX warned against these targets and the process terminated during the scan.

### S1.42E — historical startup-safe hotfix

Profile:
`Profiles/LC V1 S1.42E Startup Safe Enemy Regression.r2z`

SHA-256:
`4df5d6417aad35ad327b183eb2dd25ecb6bd20382840198f74f0201007d57348`

Manifest:
- 188 total
- 183 enabled
- 5 disabled
- no package/version/state differences vs S1.42D

Compatibility plugin:
v1.3.1

DLL SHA-256:
`caf20c785245396d9f31ff32b556cbe75d64b87a5a676807184093a6cef78eab`

LethalMin scope:
- `*PikminEnemy` types only;
- `DeclaredOnly`;
- local `BitePikmin`, `GrabPikmin`, `GrabPikminWithTongue`;
- no RPC wrappers;
- no generic PikminAI/PikminItem patching.

Jetpack:
- historical target 140 seconds;
- `Reduce Battery = false`;
- `MidAirExplosions = Off`;
- loaded Jetpack Item asset targeting only;
- no inherited `GrabbableObject.Start` Harmony hook.

Diagnostics:
`Isolated Enemy Regression = true`

First acceptance gate:
reach Main Menu without crash.
