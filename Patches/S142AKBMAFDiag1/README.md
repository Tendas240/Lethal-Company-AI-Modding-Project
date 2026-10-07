# S142AKBMAFDiag1

Source-only diagnostic successor for the bounded Black Mesa x Abandoned Foundry compatibility proof.

## Runtime role

- diagnostic only / NEVER ACCEPT;
- exact target moon: `Black Mesa`;
- exact target interior: `Abandoned Foundry` / `FoundryFlow`;
- runs after the accepted S1.42AB interior normalizer;
- requires Foundry to already exist exactly once in LLL's returned viable pool at normalized rarity `100`;
- only then reduces that fresh returned list to the same existing wrapper;
- observes native `EntranceTeleport.TeleportPlayer()` only after native traversal;
- never registers a dungeon, adds availability, edits config, writes entrance state, replaces an RPC, changes RNG, or teleports the player manually.

## Availability boundary

This plugin does not make Abandoned Foundry viable on Black Mesa. Any later review profile must separately use LethalLevelLoader's supported `Custom Dungeon:  Abandoned Foundry` content-configuration surface. The permitted semantic delta is limited to setting `Enable Content Configuration = true` on a fail-closed materialization of the owner-default section and adding exactly `Black Mesa:100` to its existing Manual Level Names mapping while preserving every other owner value.

If that exact config transformation cannot be proven, the later build must fail closed rather than substituting a runtime availability patch.

Any later profile must derive directly from exact accepted `S1.42AK`; neither historical BMGHDIAG3 bytes nor the separate active/not-accepted `S1.42AK-BMDSFIX1` candidate may be used as a profile parent.

## Source checkpoint

This directory is source/static only. It does not authorize compilation, profile construction, exact-byte publication, Gale import, runtime arming or gameplay testing.
