# S1.39 Compatibility Fixes

Project-local cumulative plugin for the Tendas Lethal Company profile.

Current source version: **1.2.0**

Current runtime-tested embedded binary reference:
- profile: `Profiles/LC V1 S1.42C Pikmin Enemy Guard.r2z`
- embedded DLL SHA-256: `c3da6ee8220bec3b954ac62ca1a4d813efcb292eefd9b70fc0616a76e2f37af3`

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

- Import any current project `.r2z` containing this plugin with **Advanced options -> Import all files** so the embedded DLL is extracted.
- The current source is compiled directly by the repository-first GitHub Actions profile build and injected into the generated profile.
- **Do not use `Tendas-S139CompatibilityFixes-1.0.0.zip` or the standalone `S139CompatibilityFixes.dll` in this folder as a current fallback.** Those binary artifacts are historical v1.0.0-era files and do not contain the later LethalModDataLib/Puffer guards. They remain only for historical reconstruction; the authoritative current implementation is `Plugin.cs` compiled by the build workflow.

Expected runtime markers:

`S1.39 Compatibility Fixes loaded.`

When LethalModDataLib is present:

`[LMDLGuard] Safe ModDataAttribute scan completed:`

The next validation must also confirm LethalModDataLib continues past registration and logs its normal save/load-hook initialization.

Build status: cumulative compatibility plugin; every version bump must be compiled by the repository-first profile workflow and runtime-validated in the corresponding candidate.
