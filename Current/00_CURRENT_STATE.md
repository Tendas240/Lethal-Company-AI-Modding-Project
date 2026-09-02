# 00 — Current State

**Canonical project state:** S1.40A  
**Date:** 2026-09-02  
**Current gameplay/test profile:** Profiles/LC V1 S1.40A CodeRebirth Config Cleanup Fix.r2z  
**Latest runtime-tested profile:** Profiles/LC V1 S1.40 Native Currency Flash Turret Cleanup.r2z  
**Game:** Lethal Company V81

S1.40A is the current build/test candidate. S1.40 is the newest profile actually run in game, but it failed the Currency/Flash-Turret acceptance gate.

## Why S1.40 failed

The user encountered a Flash Turret in later S1.40 runs. Currency was not always visually found, but runtime evidence included CodeRebirth Currency clone instances. More decisively, the post-run CodeRebirth config no longer contained the intended S1.40 values:

- `Clean Unusued Configs = true`
- `Flash Turret | Is Inside Hazard = true`
- Coin / Crisp Dollar Bill / Wallet inside moon curves restored to positive defaults

Therefore the S1.40 sparse overrides were not retained through CodeRebirth startup/config cleanup.

## Exact S1.40A delta

S1.40A is built from the exact S1.40 archive and replaces only:

`BepInEx/config/CodeRebirth.cfg`

The S1.40 suppression values are retained, plus:

`[General] Clean Unusued Configs = false`

No Thunderstore package changes. Manifest remains 179 total / 173 active / 6 disabled. The cumulative S139CompatibilityFixes DLL remains unchanged.

## Critical Gale import rule

Use **Advanced options -> Import all files**.

Expected marker: `S1.39 Compatibility Fixes loaded.`

## Immediate acceptance test

1. Confirm the local compatibility DLL marker.
2. Confirm no natural Coin / Crisp Dollar Bill / Wallet inside spawns.
3. Confirm no natural Flash Turret.
4. Preserve full `LogOutput.log`.
5. After the run, inspect runtime `BepInEx/config/CodeRebirth.cfg`; S1.40A values must still be present.

BCMER remains disabled until this gate passes.
