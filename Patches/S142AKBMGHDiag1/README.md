# S142AKBMGHDiag1

Diagnostic-only implementation for the C3F17 Black Mesa × Greenhouse runtime qualification contract.

It contains exactly two Harmony postfix surfaces:

- `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` — after the accepted S1.42AB normalizer, reduce only the exact real Black Mesa server-selection result to the already-viable `GreenhouseFlow` wrapper.
- installed-V81 `EntranceTeleport.TeleportPlayer()` — read-only post-call observation of native same-ID/opposite-side traversal plus a one-time active topology snapshot for IDs 0..3.

The observer does not call `FindExitPoint`, teleport the player, rewrite entrance IDs, invoke RPCs, repair topology or mutate registration/configuration.

This directory is source/static-test material only. C3F17.3 does not create a Gale candidate, does not touch `BuildSpecs/current.json`, does not arm runtime and is never an accepted gameplay baseline.

Authority: `BuildSpecs/S1.42AK-BMGHDIAG1_PLAN.md` and `SourceEvidence/UniversalInteriorViability/PhaseC3F17/CANDIDATE_CONTRACT.json`.
