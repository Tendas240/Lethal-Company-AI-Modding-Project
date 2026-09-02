# 01 — Handover Core

## Working rules for the next ChatGPT conversation

1. Treat **S1.36** as the current canonical handover/test candidate unless the repository contains a newer confirmed state.
2. Treat **S1.34** as the latest runtime-tested profile until S1.36 is actually run.
3. Never treat S1.29D as a normal gameplay base; it existed only for the RedPill enemy-power audit.
4. Before changing enemy spawning, determine the actual spawn owner for the enemy.
5. Do not independently distort the binding screenshot reference ratios.
6. Do not modify the confirmed 26×Weight100 interior architecture without a concrete runtime reason.
7. Unknown enemy PowerLevels must not be guessed.
8. Do not reintroduce solutions listed in 05_FAILED_AND_OBSOLETE_APPROACHES.md without new evidence.
9. **Malfunctions remains disabled until the user explicitly requests re-enabling it.**
10. **ProjectSCP-SCP999 remains disabled.** Current logs proved it was accidentally active and throwing a startup NRE.
11. Do not enable AJB-Keep_hangar_ship_door_closed alongside the S1.35/S1.36 local patch.
12. For S1.36, verify the local plugin actually loads before judging door or EnemyScan behavior.

## Critical S1.36 import/install rule

The current profile embeds S135CompatibilityFixes.dll. Gale can skip extra arbitrary files on a normal profile import.

Use **Advanced options → Import all files**.

If the plugin does not appear in the BepInEx startup log, import this local mod separately into the same profile:

Patches/S135CompatibilityFixes/Tendas-S135CompatibilityFixes-1.0.0.zip

Expected startup evidence:

- S1.35 Compatibility Fixes loaded
- [EnemyScanFix] Patched EnemyScan to list every active EnemyAI regardless of ScanNodeProperties.

Absence of those messages means the fix is not installed.

## Gameplay-base lineage

### S1.29
LC V1 S1.29 CodeRebirth Runtime Test.r2z

Normal gameplay base with CodeRebirth 1.6.9.

### S1.29D
LC V1 S1.29D Enemy Power Audit.r2z

Diagnostic only. Never use as a gameplay base.

### S1.30
LC V1 S1.30 Power Caps Mimicless Pikmin Shield.r2z

Built from S1.29, not S1.29D.

Major changes:

- x753-Mimics removed.
- CoronerMimics removed.
- CodeRebirth↔Pikmin hazard switches set false.
- Indoor caps set to the then-selected higher values.
- Enemy weights and 26-interior rotation preserved.

### S1.31
LC V1 S1.31 Indoor Power Trim -4.r2z

All controllable indoor power caps reduced by 4. No intended weight/interior/Pikmin-protection changes.

### S1.32
LC V1 S1.32 Leaf Boy Blacklist + Mirage Keep Recordings.r2z

Changes:

- appended Leaf boy to the existing LethalMin Attack Blacklist;
- added Mirage game-root settings with neverDeleteRecordings=true while preserving the other observed Mirage values.

Runtime finding: the player returned from the dungeon to a closed ship hangar door and could be locked out indefinitely because the old AJB mod prevented the hydraulic countdown from recovering the door.

### S1.33
LC V1 S1.33 Ship Door Failsafe.r2z

First custom replacement for AJB:

- AJB disabled;
- custom DLL intended to freeze power only while a living player was inside;
- vanilla drain intended to resume when all living players were outside;
- DoorAudit logging added.

Later runtime evidence showed this DLL was not imported/loaded by Gale, so the algorithm was not actually tested.

### S1.34
LC V1 S1.34 Malfunctions Disabled

Latest runtime-tested profile.

Change: zealsprince-Malfunctions disabled by explicit user decision and intended to stay disabled until the user explicitly asks otherwise.

Runtime findings:

- custom S1.33 door plugin did not load;
- no DoorAudit/DoorFailsafe output;
- door energy drained and reopened at zero = vanilla behavior;
- EnemyScan omitted some spawned enemies;
- Puma was active and is vanilla Feiopar;
- Coin came from CodeRebirth;
- SCP999 still loaded and threw a startup NRE.

### S1.35
LC V1 S1.35 Door + Complete Enemy Scan.r2z

Structurally verified but not runtime-tested.

Rebuilt local patch:

- ship-inside detection using isInHangarShipRoom plus shipInnerRoomBounds fallback;
- door audit logging;
- anti-lockout behavior that allows vanilla drain only when all living players are outside;
- EnemyScan output patch that lists all active EnemyAI rather than requiring ScanNodeProperties.

### S1.36
LC V1 S1.36 Handover Clean Baseline.r2z

Current canonical candidate.

Exact intended delta from S1.35:

- profile name updated;
- ProjectSCP-SCP999 set enabled:false;
- no other archive member changed.

S1.36 carries all S1.35 fixes plus the S1.34 Malfunctions-disabled policy.

## Stable architecture

### Spawn ownership

Use one positive spawn owner per enemy wherever practical.

Especially:

- Rolling Giant → native mod configuration.
- Shy Guy / Scopophobia → native mod configuration.
- Siren Head → native mod configuration.

Do not force them positive through LethalLevelLoader again without new evidence.

### Binding enemy-weight references

The seven screenshots under References/Spawn-Rates/ are binding for relative ratios among the enemies shown on Experimentation, Assurance, Vow, Offense, March, Adamance and Titan.

New enemies may enlarge the total pool, but reference enemies must not be independently rebalanced against each other without a deliberate new decision.

### Interiors

26 normal dungeon flows rotate equally at Weight 100. Black Mesa uses its own DawnLib/config path and must not be double-registered through LLL.

### Company automation

Confirmed solution: CompanyBuildingEnhancements 2.6.0.

Do not return to AutoCompanyBuilding or RandomMoonFX for this purpose.

## Pikmin protection

Core settings:

- No Knock Back = true
- Invinceable Pikmin = true
- Pikmin Die In Player Death Zones = false

S1.30 CodeRebirth compatibility switches false:

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

Confirmed: Flash Turret protection works.

S1.31 Leaf Boy issue: Pikmins attacked LeafBoi(Clone) continuously for several minutes. S1.32+ appends Leaf boy to the current Attack Blacklist.

Still unconfirmed:

- Microwave burn/cook immunity;
- complete enemy-AI target exclusion for immortal Pikmins;
- remaining CodeRebirth hazards;
- runtime confirmation that the Leaf Boy blacklist fully stops the loop.

## Ship-door facts

- The original S1.32 close trigger was not conclusively identified.
- Malfunctions did not show a successful relevant door malfunction in the analyzed run.
- BCMER was disabled.
- A Masked enemy was nearby, but vanilla MaskedPlayerEnemy has no StartButton/StopButton/HangarShipDoor interaction.
- Poltergeist can allow dead players/ghosts to interact with ship-door buttons; this is distinct from Masked AI.
- Permanent lockout came from a close action combined with unconditional AJB door-power refill.
- S1.35/S1.36 replaces AJB with a narrower failsafe and reuses vanilla hydraulic drain/open logic when everyone living is outside.

## EnemyScan facts

EnemyScan 1.2.1 originally used a ScanNodeProperties filter in BuildEnemyCountString(), so spawned enemies without a scan node could be omitted from enemies.

S1.35/S1.36 patches only that list-building output. It does not change spawn rates, PowerLevels, AI, scan nodes, or bestiary data.

## Mirage facts

Current settings:

- localPlayerVolume = 0.5
- neverDeleteRecordings = true
- allowRecordVoice = true
- muteVoiceMimic = false

Mirage stores:

- settings: <Lethal Company installation folder>/Mirage/settings.json
- recordings: <Lethal Company installation folder>/Mirage/Recording

This is game-root storage, not BepInEx/config.

## Important enemy/system decisions

- SCP-999 stays disabled.
- Malfunctions stays disabled until explicit user instruction.
- Immortal Snail maximum: 2 simultaneously.
- Observer remains disabled.
- Don't Touch Me remains disabled.
- BCMER remains disabled but is not permanently obsolete.
- CodeRebirthLib must not be installed.
- Peepers enemy/hazard remains removed; do not confuse it with the Peeper tool.
- LethalPlaytime Boxy Boo / Huggy Wuggy / Miss Delight should not be reactivated on V81.

## Current unresolved enemy PowerLevels

Do not invent values for:

- Rolling Giant
- Siren Head
- Immortal Snail
- Herobrine
- Football
- Faceless Stalker
- CodeRebirth Debt Collector / Boogey Man
