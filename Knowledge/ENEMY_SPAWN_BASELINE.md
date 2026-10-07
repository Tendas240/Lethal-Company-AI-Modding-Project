# Enemy Spawn Baseline and Ownership

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** semantic router to the accepted enemy-spawn restore baseline and ownership rules  
**Canonical-For:** `enemy_spawn_baseline`  
**Machine Evidence:** `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`  
**Related:** `ProfileSources/S1.42C/`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/BCMER.md`  
**Last-Validated:** 2026-09-04

## Restore baseline

S1.42C is the canonical restore point for the normal enemy-spawn/configuration state that existed before the temporary EnemyIsolation diagnostic chain.

- Profile: `Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`
- SHA-256: `22901e5459be4e10d30bb9011bb25e80899bd8b9838a9f487d2a800559777eb3`
- Readable snapshot: `ProfileSources/S1.42C/`
- Machine restore record: `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`

Later accepted builds carry this spawn/power baseline forward except where an explicitly accepted later gameplay change says otherwise.

## EnemyIsolation

`Isolated Enemy Regression` was diagnostic-only. It must remain **disabled** in normal gameplay. The isolated allowlist was never a new permanent enemy roster.

Do not permanently disable enemy packages or rewrite normal spawn-owner configs merely to reproduce the old focused diagnostic.

## Spawn ownership rule

Prefer one positive spawn owner per enemy. Do not force every enemy through LethalLevelLoader or BCMER.

Known native-owner examples retained by project history:

- Rolling Giant -> native config
- Shy Guy / Scopophobia -> native config
- Siren Head -> native config

BCMER is configured not to take over normal power/spawn chance outside events. See `Knowledge/BCMER.md`.

## Indoor power caps

The established per-moon indoor power values and exact config state are preserved in the readable S1.42C profile snapshot and earlier technical evidence. Do not reconstruct or retype them from memory when making a build; use the canonical profile/config snapshot.

Important anti-guess rule: Oxyde has no separately confirmed controllable value. Do not invent one.

## Unknown enemy PowerLevels

Do not guess project PowerLevel values for enemies whose exact owner/value has not been established. Historical technical evidence explicitly leaves several values unknown, including Rolling Giant, Siren Head, Immortal Snail, Herobrine, Football, Faceless Stalker and CodeRebirth Debt Collector/Boogey Man.

S1.29D is diagnostic-only and must never become a gameplay base.

## Current compatibility values carried forward

Current accepted full-stack state preserves:

- Thumper Bite Limit = `3`;
- `Crawler` absent from the LethalMin Attack Blacklist;
- Puffer -> Pikmin protection;
- Baboon Hawk -> Pikmin narrow protection while Pikmin -> Hawk remains allowed;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- EnemyIsolation disabled.

Detailed interaction ownership is in `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`.
