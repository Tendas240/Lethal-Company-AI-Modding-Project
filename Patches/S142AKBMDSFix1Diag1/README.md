# S1.42AK-BMDSFIX1-DIAG1 — Deterministic Deep Sewers Selector

Diagnostic-only selector. **Never accept as a gameplay baseline.**

This plugin exists only to make the already-viable Black Mesa `Deep Sewers` entry deterministic for a controlled truth test of the unchanged S1.42AK-BMDSFIX1 size-fix DLL.

## Sole patch surface

One Harmony postfix on:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

The postfix is ordered after `tendas.lethalcompany.s142abinteriorweightnormalization` at `Priority.Last` and may reduce only the fresh returned local list from `N` entries to the same existing Deep Sewers wrapper as a singleton.

It does not register flows, change rarity, alter global LLL lists, hook RNG, replace RPCs, patch entrances/teleports/NavMesh, or reproduce BMDSFIX1's `GetClampedDungeonSize()` logic.

## Fail-closed target contract

Selection is permitted only for exact LLL 1.7.12 / SHA-256 `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`, exact accepted S1.42AB normalizer 1.0.0 / SHA-256 `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`, exactly one normalizer postfix on the exact target, the real `GetRandomExtendedDungeonFlowServerRpc` managed call stack, non-simulation execution, Black Mesa, exact result-list identity, no null wrappers, exactly one `Deep Sewers` ExtendedDungeonFlow, exact asset `DeepSewersFlow`, and normalized rarity `100`.

Any validation failure refuses the diagnostic and preserves normal viable selection behavior.

## Acceptance boundary

A successful DIAG1 run is supporting deterministic target evidence only. It does not replace the regular unchanged-byte S1.42AK-BMDSFIX1 target qualification required by `Current/175_S1.42AK_BMDSFIX1_PARTIAL_RUNTIME_EVIDENCE_NON_TARGET_CONTROL.md`.
