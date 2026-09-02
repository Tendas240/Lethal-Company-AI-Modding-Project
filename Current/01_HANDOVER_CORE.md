# 01 — Handover Core

## Working rules for the next ChatGPT conversation

1. Treat S1.31 as the current gameplay state unless a newer repository state exists.
2. Never treat S1.29D as a normal gameplay base. It existed only for the RedPill enemy-power audit.
3. Before changing enemy spawning, determine the actual spawn owner for the enemy.
4. Do not independently distort the binding screenshot reference ratios.
5. Do not modify the confirmed 26×Weight100 interior architecture without a concrete runtime reason.
6. Do not replace the confirmed Company automation solution without a demonstrated bug.
7. Unknown enemy PowerLevels must not be guessed.
8. Do not reintroduce solutions listed in `05_FAILED_AND_OBSOLETE_APPROACHES.md` without new evidence.

## Gameplay-base lineage

### S1.29
`LC V1 S1.29 CodeRebirth Runtime Test.r2z`

Normal gameplay base with CodeRebirth 1.6.9.

### S1.29D
`LC V1 S1.29D Enemy Power Audit.r2z`

Diagnostic only: S1.29 plus RedPillEnemySpawn 0.3.0, configured to rarity 0. The plugin loaded, but did not produce the intended complete runtime EnemyType PowerLevel table.

### S1.30
`LC V1 S1.30 Power Caps Mimicless Pikmin Shield.r2z`

Built from S1.29, not S1.29D.

Major changes:

- x753-Mimics removed completely.
- CoronerMimics removed completely.
- CodeRebirth↔Pikmin hazard switches set to false.
- Indoor caps initially set to the then-selected higher values.
- Enemy weights preserved.
- 26-interior rotation preserved.

### S1.31
`LC V1 S1.31 Indoor Power Trim -4.r2z`

Built from S1.30.

Only intended gameplay change: all controllable indoor power caps reduced by 4. Black Mesa 32→28. No enemy-weight, interior-weight, or Pikmin-protection changes.

## Stable architecture

### Spawn ownership

Use one positive spawn owner per enemy wherever practical.

Especially:

- Rolling Giant → native mod configuration.
- Shy Guy / Scopophobia → native mod configuration.
- Siren Head → native mod configuration.

Older attempts to force these through LethalLevelLoader were unreliable.

### Binding enemy-weight references

The seven screenshots under `References/Spawn-Rates/` are binding for the relative ratios among the enemies shown on:

- Experimentation
- Assurance
- Vow
- Offense
- March
- Adamance
- Titan

New enemies may enlarge the total pool. That may reduce final percentages, but reference enemies must not be independently rebalanced against each other without a deliberate new decision.

### Interiors

26 normal dungeon flows are intended to rotate equally at Weight 100.

Black Mesa is included through its own DawnLib/config path and should not be double-registered through LethalLevelLoader.

Gordion/Company is not treated as a normal dungeon moon.

### Company automation

Confirmed solution: CompanyBuildingEnhancements 2.6.0.

Do not return to AutoCompanyBuilding or RandomMoonFX for this purpose.

## Pikmin protection

Core settings include:

- `No Knock Back = true`
- `Invinceable Pikmin = true`
- `Pikmin Die In Player Death Zones = false`

S1.30 set these CodeRebirth compatibility interactions to false:

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

Practical confirmation so far:

- Flash Turret protection works.

Still unconfirmed:

- Microwave burn/cook immunity.
- Complete enemy-AI target exclusion.
- Remaining CodeRebirth hazards.

## Important enemy/system decisions

- SCP-999 enemy stays disabled.
- Immortal Snail maximum: 2 simultaneously.
- Giant Sapsucker/GiantKiwi should occur on normal moons without dominating the daytime pool.
- Observer remains disabled.
- Don't Touch Me remains disabled.
- BCMER remains disabled.
- CodeRebirthLib must not be installed.
- Peepers enemy/hazard mod remains removed; do not confuse it with the Peeper tool.
- Old LethalPlaytime enemies Boxy Boo / Huggy Wuggy / Miss Delight should not be reactivated on V81 due to AI/collision problems.

## Performance history to remember

- Active SCP-999 previously caused an enormous repeated SCP999AI/SnowyLib NullReferenceException flood. Do not re-enable it.
- Historical NavMesh warning spam reached tens of thousands of lines.
- In the S1.29D audit run the relevant NavMesh warning count fell to roughly 10 and was associated with Pikmin initialization.
- Historical `Enemy Spawner tried to spawn a null EnemyType!` occurrences were no longer observed in the later audit run.

## Current unresolved enemy PowerLevels

Do not invent values for:

- Rolling Giant
- Siren Head
- Immortal Snail
- Herobrine
- Football
- Faceless Stalker
- CodeRebirth Debt Collector / Boogey Man

Use runtime dumping or asset/DLL analysis if an exact value becomes necessary.
