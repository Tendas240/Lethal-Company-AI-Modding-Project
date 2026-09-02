# 03 - Project Chronology

This is a technical reconstruction of the confirmed project history, not a verbatim chat transcript.

## S1.2 - profile/path-length stabilization
Long Gale profile names caused Windows/BepInEx path trouble. Permanent rule: keep profile names reasonably short.

## S1.3-S1.10 - early cleanup, Pikmin and ownership work
Wild Pikmin/falloff, stamina, batteries, facility distribution and several obsolete/broken mods were cleaned up. Gnomes were identified as a V81 `PlayerIsTargetable` MissingMethod spam source and removed. Peepers enemy/hazard was removed. LLL was proven not to be the only spawn authority.

## S1.11-S1.14 - spawn-owner isolation
A central LLL-only approach was tested and failed for some enemies. Rolling Giant, Shy Guy/Scopophobia and Siren Head returned to their native spawn configuration. Persistent rule: prefer one positive spawn owner per enemy.

## S1.15-S1.23 - gameplay stabilization
Rolling Giant movement tuned, RandomEnemiesSize added, Company automation went through failed AutoCompanyBuilding/RandomMoonFX attempts, and the confirmed solution became CompanyBuildingEnhancements 2.6.0. LethalHUD Hold-to-Scan replaced old Hold_Scan_Button. Pikmin water resistance was confirmed.

## S1.24-S1.28 - roster, balance and interiors
Enemy roster was restored, reference spawn-rate screenshots became binding, Immortal Snail max was set to 2, and 26 intended interiors were established at equal Weight 100. Black Mesa was integrated through its own DawnLib/config path.

## S1.29 / S1.29D - CodeRebirth and Power audit
CodeRebirth 1.6.9 integrated. S1.29D was a diagnostic-only RedPill enemy-power audit derivative; it must never become a gameplay base.

## S1.30 - caps, Mimicless, Pikmin shield
Mimics/CoronerMimics removed; CodeRebirth/Pikmin compatibility switches set false; indoor caps raised, then judged somewhat dense.

## S1.31 - indoor power trim -4
All controllable indoor power caps reduced by 4 without changing weights/interiors/Pikmin behavior. Runtime then exposed the Leaf Boy/Pikmin endless attack loop and SCP999 startup NRE regression.

## S1.32 - Leaf Boy blacklist + Mirage retention
`Leaf boy` appended to the current LethalMin Attack Blacklist. Mirage `neverDeleteRecordings=true` requested. A closed-ship-door lockout was observed; the original close trigger was not conclusively identified, but AJB's unconditional power refill caused the permanent lockout.

## S1.33 - first ship-door failsafe
AJB disabled. Custom door failsafe designed to keep 100% hydraulic power only while a living player is inside and allow vanilla drain when everyone is outside. Later discovered Gale had not imported the DLL, so this version did not runtime-test the algorithm.

## S1.34 - Malfunctions disabled / diagnosis
Malfunctions disabled by explicit user policy. Runtime proved S1.33 custom DLL had not loaded, confirmed EnemyScan's scan-node filter, identified Puma as vanilla Feiopar, and confirmed CodeRebirth Coin semantics. SCP999 still loaded and threw startup NRE.

## S1.35 - rebuilt local compatibility plugin
V81 local plugin compiled for door anti-lockout + DoorAudit + complete EnemyScan. Standalone fallback package created. Structurally verified.

## S1.36 - clean canonical baseline and first successful local-patch runtime acceptance
S1.35 plus ProjectSCP-SCP999 disabled. 176 manifest entries / 170 active / 6 disabled. This profile became the deterministic source baseline for later builds.

The subsequent runtime test confirmed the local S1.35 compatibility DLL actually loaded under Gale with `Import all files`. The user's ship-door test behaved as intended, and the `enemies` terminal output was cross-checked against the runtime log and matched the active enemy population. The user also confirmed Pikmins were no longer affected by CodeRebirth microwaves. These three behaviors are accepted and should not be reopened without a regression.

## S1.37 - CodeRebirth natural currency scrap filter
Cumulative local plugin replaced S135 with S137. During normal `RoundManager.SpawnScrapInLevel`, Coin, Crisp Dollar Bill, Wayfarer's Wallet and Credit Pad 100/500/1000cc are temporarily removed from the natural scrap pool and restored afterward so dedicated CodeRebirth systems remain usable.

Build verification passed. Later runtime logs confirmed `S1.37 Compatibility Fixes loaded` and the EnemyScan patch marker.

## S1.38 - 1440p + Old-Bird-only Lethal Resonance
Added:

- FixCameraResolution 1.5.3 with fixed 2560x1440 internal target;
- Lethal Resonance 4.7.8;
- loaforcsSoundAPI_LethalCompany 1.0.2.

Lethal Resonance was configured so only Old Bird, Old Bird footsteps and Old Bird speaker groups are enabled.

S1.38 was actually run in game and is the latest runtime-tested reference. Confirmed from the latest log:

- S1.37 compatibility plugin loaded;
- EnemyScanFix marker present;
- FixCameraResolutions 1.5.3 loaded;
- SoundAPI load pipeline completed;
- after the user manually set Mirage retention in the Main Menu/LethalConfig, the log loaded `neverDeleteRecordings=true` (profile import alone had not reliably applied it).

The test phase also exposed that normal generated CodeRebirth Coin objects were still appearing through a map-object/hazard path not covered by S1.37's scrap-only filter. The user also wanted Flash Turret natural spawns removed, Ogopogo/Vermin disabled, and reported the CodeRebirth Autonomous Crane could still kill Pikmin even though LethalMin's crane toggles were false. A four-legged Jester-like enemy seen indoors was identified from the same runtime log as `Cabinet` from `Cabinet_crew-TheCabinet 1.12.1` (`Spawning Cabinet from vent`).

Old Bird replacement audio still lacked a clean encounter-based acceptance test.

## S1.39 - cleanup + health + Pikmin kill shield
Built from the canonical S1.36 baseline while carrying forward S1.37/S1.38 behavior.

Changes:

- Biodiversity `OgopogoEnabled=false`;
- Biodiversity `EnableVermin=false`;
- natural Flash Turret suppressed during `SpawnMapObjects`;
- natural CodeRebirth currency map objects suppressed during `SpawnMapObjects` in both V81 `IndoorMapHazard[]` and legacy paths;
- S1.37 natural scrap currency filter retained;
- all relevant LethalMin CodeRebirth/Pikmin interaction toggles verified false;
- direct CodeRebirth utility-kill guard added for Pikmin/Puffmin, closing the observed crane-kill gap;
- GeneralImprovements `AddHealthRechargeStation=true` explicitly verified and preserved;
- S1.38 2560x1440 and Old-Bird-only Lethal Resonance carried forward;
- BCMER still disabled.

Build/CRC/member-delta/package/config/DLL-compilation checks all passed.

**Current status:** S1.39 is the canonical test candidate but is not yet runtime-accepted. S1.38 remains the latest runtime-tested reference.
