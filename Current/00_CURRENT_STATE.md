# 00 — Current State

**Canonical project state:** S1.40A  
**Date:** 2026-09-02  
**Current gameplay/test profile:** `Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z`  
**Current profile SHA-256:** `ab894ead158941d6f9d6c3463baab51c65486ebf6d40df8b2325fca626d966a5`  
**Latest runtime-tested profile:** `Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z`  
**Latest runtime result:** S1.40 failed acceptance  
**Game:** Lethal Company V81

## What happened in S1.40

The user ran S1.40 multiple times.

- In an early run the user found a Wallet and a Flash Turret.
- The user later suspected the first Gale import may have omitted **Advanced options -> Import all files**.
- In later runs the user did not visually find Coins/Wallets, but still saw a Flash Turret.
- Runtime logs also contained instantiated CodeRebirth Currency objects, so visual absence alone was not sufficient proof of suppression.
- The post-run `CodeRebirth.cfg` was decisive: S1.40's intended suppression values had not survived startup.

Observed post-run values included:

- `Clean Unusued Configs = true`
- `Flash Turret | Is Inside Hazard = true`
- Coin / Crisp Dollar Bill / Wallet had positive Inside Moon Spawn Weights again.

Therefore S1.40 is **not accepted** even if one earlier import may have been incomplete.

## Why S1.40A exists

S1.40A isolates the config-retention problem.

It is built from exact S1.40 and changes only the existing `BepInEx/config/CodeRebirth.cfg`.

New decisive value:

`[General] Clean Unusued Configs = false`

The S1.40 blank Currency inside weights and Flash Turret suppression remain present.

No Thunderstore package changes. Manifest remains:

- 179 manifest entries
- 173 active
- 6 disabled
- plus the unchanged project-local S139CompatibilityFixes plugin.

## Critical Gale rule

Import S1.40A with:

**Advanced options -> Import all files**

Expected runtime marker:

`S1.39 Compatibility Fixes loaded.`

## Immediate acceptance gate

1. Confirm the local compatibility marker.
2. Confirm no natural Coin / Crisp Dollar Bill / Wallet inside spawn.
3. Confirm no natural Flash Turret.
4. Preserve the full `LogOutput.log`.
5. After exiting, inspect the runtime-generated `BepInEx/config/CodeRebirth.cfg`; S1.40A values must still be present.
6. If the values survive but Currency/Flash Turret still naturally spawn, stop config-only iteration and patch the actual DawnLib runtime spawn path.

## Binding next stages

Do **not** start them until S1.40A passes:

- **S1.41:** exact existing BCMER 1.71.0 reactivation, four BCMER rain-related events disabled, spawn ownership constrained.
- **S1.42A:** install the eight binding interior packages only to generate real configs/IDs.
- **S1.42:** tune actual generated configs after the user supplies `BepInEx/config/` and `LogOutput.log`.

Full details: `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`.
