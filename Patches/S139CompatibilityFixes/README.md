# S1.39 Compatibility Fixes

Project-local cumulative plugin for the Tendas Lethal Company profile.

Functions:

- Keeps landed ship-door hydraulic power at 100% while at least one living controlled player is actually inside the ship.
- If all living players are outside and the door is closed, preserves vanilla hydraulic drain so the door can reopen instead of causing a permanent lockout.
- Adds DoorAudit/DoorFailsafe diagnostics.
- Patches EnemyScan so the terminal command `enemies` lists all active EnemyAI objects, not only enemies with ScanNodeProperties.
- Filters CodeRebirth currency/credit items from normal `SpawnScrapInLevel` natural scrap rolls, while restoring the entries afterward so dedicated CodeRebirth mechanics remain available.
- Filters CodeRebirth currency map objects and the CodeRebirth Flash Turret from normal `SpawnMapObjects` indoor hazard generation. V81 `IndoorMapHazard[]` and the legacy `SpawnableMapObject[]` path are both covered.
- Adds a direct failsafe around CodeRebirth's utility kill RPC: Pikmin and Puffmin are prevented from reaching `EnemyAI.KillEnemyOnOwnerClient` while that CodeRebirth kill context is active. This specifically closes the observed Autonomous Crane kill gap despite LethalMin's crane interaction toggles already being false.
- When LethalModDataLib 1.2.2 is present, replaces its unsafe bulk `ModDataAttribute` scan with a null-safe scan that skips `Chainloader.PluginInfo` entries whose `Instance` is null, while preserving per-type registration for all valid plugin instances. This targets the S1.42A initialization NRE without disabling LethalModDataLib save/load behavior.
- Removes only LethalMin-injected Pikmin effect-trigger components from vanilla Puffer smoke after `PufferAI.Start`. Vanilla Puffer/player behavior remains intact; the purpose is to make Puffer smoke/attack unable to apply LethalMin Pikmin status effects even though the nightly config already has `Puffer Can Poison Pikmin = false`.

Gale import rule:

- Import the S1.39 `.r2z` with **Advanced options -> Import all files** so the embedded DLL is extracted.
- If the plugin does not load, import `Tendas-S139CompatibilityFixes-1.0.0.zip` separately into the same Gale profile.

Expected runtime markers:

`S1.39 Compatibility Fixes loaded.`

When LethalModDataLib is present:

`[LMDLGuard] Safe ModDataAttribute scan completed:`

The next validation must also confirm LethalModDataLib continues past registration and logs its normal save/load-hook initialization.

Build status: cumulative compatibility plugin; every version bump must be compiled by the repository-first profile workflow and runtime-validated in the corresponding candidate.
