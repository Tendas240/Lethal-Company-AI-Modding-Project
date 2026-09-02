# 01 - Handover Core

## Working rules for the next ChatGPT conversation

1. Treat **S1.39** as the current canonical build/test candidate unless the repository contains a newer confirmed state.
2. Treat **S1.38** as the latest runtime-tested reference until S1.39 is actually run.
3. S1.29D is diagnostic only and must never become the gameplay base.
4. Before changing enemy spawning, identify the actual spawn owner. Prefer one positive owner per enemy.
5. Preserve the binding spawn-rate screenshot ratios for the enemies shown on Experimentation, Assurance, Vow, Offense, March, Adamance and Titan.
6. Do not modify the confirmed 26xWeight100 interior architecture without a concrete runtime reason.
7. Unknown enemy PowerLevels must not be guessed.
8. Search `05_FAILED_AND_OBSOLETE_APPROACHES.md` before reviving old solutions.
9. **Malfunctions remains disabled until the user explicitly requests reactivation.**
10. **ProjectSCP-SCP999 remains disabled.** Earlier logs proved a startup NRE.
11. **BCMER remains disabled in S1.39.** It is a later isolated project, not part of this acceptance test.
12. AJB-Keep_hangar_ship_door_closed must stay disabled while the project-local door failsafe is active.
13. CodeRebirthLib must not be installed.
14. For Gale imports containing project-local DLLs, use **Advanced options -> Import all files** and verify the plugin load marker before judging behavior.
15. Distinguish build verification from runtime acceptance. S1.39 is structurally verified, not gameplay-approved yet.

## Current profile distinction

### Canonical test candidate

`Profiles/LC V1 S1.39 Cleanup Health Pikmin Shield.r2z`

SHA-256: `b510e519b4af8b683e9b9e9f4e18035f90910d2e8782f2b9e6ded5e4ecef95fe`

### Latest runtime-tested reference

`Profiles/LC V1 S1.38 1440p Old Bird Resonance.r2z`

S1.38 runtime evidence confirms the new camera-resolution plugin and S1.37 compatibility plugin loaded; the user explicitly accepted the 2560x1440 visual result. Mirage retention required manual intervention: the user set `neverDeleteRecordings=true` in the Main Menu/LethalConfig, and the subsequent S1.38 log confirmed the value. S1.38 nevertheless exposed issues now targeted by S1.39 and is therefore a reference, not the final desired endpoint.

## S1.39 targeted changes

- Biodiversity `OgopogoEnabled=false`.
- Biodiversity `EnableVermin=false`.
- Natural CodeRebirth Flash Turret generation is suppressed during `RoundManager.SpawnMapObjects`.
- Natural CodeRebirth currency map objects are suppressed during `SpawnMapObjects`; the S1.37 normal `SpawnScrapInLevel` currency filter remains.
- LethalMin CodeRebirth/Pikmin interaction toggles remain false, including `Crane Targets Pikmin=false` and `Crane Squishes Pikmin=false`.
- Because the crane still killed Pikmin in runtime despite those values, the S1.39 local plugin directly guards the CodeRebirth utility kill RPC and blocks Pikmin/Puffmin from `EnemyAI.KillEnemyOnOwnerClient` in that context.
- GeneralImprovements `AddHealthRechargeStation=true` is verified and preserved. Actual full-heal behavior still needs S1.39 runtime validation.
- S1.38's fixed 2560x1440 rendering and Old-Bird-only Lethal Resonance settings are carried forward.

## Stable spawn ownership

Especially:

- Rolling Giant -> native mod configuration.
- Shy Guy / Scopophobia -> native mod configuration.
- Siren Head -> native mod configuration.

Do not force them positive through LethalLevelLoader again without new evidence.

## Binding enemy-weight references

The seven screenshots under `References/Spawn-Rates/` are binding for relative ratios among the enemies shown. New enemies may enlarge the total pool, but reference enemies must not be independently rebalanced against one another without a deliberate new decision.

## Interiors

26 normal dungeon flows rotate at Weight 100. Black Mesa uses its own DawnLib/config path and must not be double-registered through LLL.

## Pikmin protection policy

Core settings:

- `No Knock Back = true`
- `Invinceable Pikmin = true`
- `Pikmin Die In Player Death Zones = false`

CodeRebirth switches must remain false:

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

Confirmed historically: Flash Turret protection against direct Pikmin interaction worked. S1.39 additionally removes natural Flash Turret spawning. In the S1.36 runtime test, the user also confirmed Pikmins were no longer affected by CodeRebirth microwaves; treat microwave protection as accepted unless a later regression is observed.

Still open despite immortality/config switches:

- enemy AI wasting target selection on immortal Pikmins;
- runtime validation of the new crane kill shield;
- remaining CodeRebirth hazard edge cases.

## Ship-door facts

The permanent lockout was caused by an ordinary/external close combined with AJB's unconditional power refill. The local cumulative plugin keeps power at 100% only when a living player is actually inside the landed ship, and leaves vanilla hydraulic drain intact when all living players are outside.

S1.36 runtime testing confirmed the local plugin loaded, produced DoorAudit markers, and the ship-door behavior worked as intended in the user's test. Keep AJB disabled.

## EnemyScan facts

EnemyScan 1.2.1 originally filtered the terminal list to EnemyAI that had a ScanNodeProperties child. The local plugin replaces only the output-building method so all active EnemyAI with EnemyType can be listed. In S1.36 the user's ~7pm terminal screenshot was cross-checked against the runtime log and the counts matched, so the complete-list fix is accepted. It does not change spawning, PowerLevels, AI, scan nodes or bestiary data.

## Mirage facts

Desired settings:

- `localPlayerVolume = 0.5`
- `neverDeleteRecordings = true`
- `allowRecordVoice = true`
- `muteVoiceMimic = false`

Storage is game-root, not BepInEx/config. The user had to set `neverDeleteRecordings=true` manually in the Main Menu/LethalConfig after an import; the later S1.38 log then confirmed it was true. Continue checking it after major profile imports and do not claim the `.r2z` alone guarantees this per-player setting.

## Important disabled/parked systems

- SCP999 stays disabled.
- Malfunctions stays disabled until explicit user instruction.
- Immortal Snail maximum: 2 simultaneously.
- Observer stays disabled.
- Don't Touch Me stays disabled.
- BCMER stays disabled for S1.39; reactivation is a later isolated build.
- Peepers enemy/hazard stays removed; do not confuse with the Peeper tool.
- LethalPlaytime Boxy Boo / Huggy Wuggy / Miss Delight should not be reactivated on V81.

## Unresolved Enemy PowerLevels

Do not invent values for:

- Rolling Giant
- Siren Head
- Immortal Snail
- Herobrine
- Football
- Faceless Stalker
- CodeRebirth Debt Collector / Boogey Man
