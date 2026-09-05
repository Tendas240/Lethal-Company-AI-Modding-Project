# Functional Microwave and Immortal Snail

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted item/enemy tuning values plus currently selected Microwave scope boundary  
**Canonical-For:** `functional_microwave`, `immortal_snail`  
**Evidence:** `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, accepted profile snapshots, `Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`  
**Related:** `Knowledge/CODEREBIRTH.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Functional Microwave

Accepted current audio value:

- Volume = `0.15`

This value was accepted during the S1.42Z runtime/balance gate and is carried forward by accepted S1.42AC.

### Spawn rarity — selected S1.42AD scope

The Functional Microwave spawn-rarity reduction has now been explicitly selected as the next scope after S1.42AC.

A source-only implementation draft exists at:

`Patches/S142ADCodeRebirthMicrowaveSpawnTuning/`

Recovery/status record:

`Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`

The draft currently uses:

`SpawnScale = 0.5f`

but **0.5 / 50% is not yet an accepted target**. The current canonical requirement is qualitative: the Functional Microwave should be rarer. No exact reduction percentage is presently recorded as user-authorized project state.

Therefore:

- preserve accepted Volume `0.15`;
- do not treat the draft `0.5` as a finalized balance value;
- do not build the draft until the exact magnitude is resolved and the Patch Safety Review/build plan is completed;
- if the approved target differs from `0.5`, update the draft/source plan before building.

Historical intermediate volume proposals such as `0.7` or `0.5` are superseded by the accepted Volume `0.15`; those old **volume** values must not be confused with the new draft **spawn-scale** value.

## Immortal Snail

Accepted current values:

- Rarity = `40`
- Max Snails = `2`

The max-2 rule predates the final S1.42Z retune; S1.42Z accepted the current Rarity 40 / Max 2 combination and S1.42AC carries it forward.

## Change discipline

These values are gameplay balance state. Any future retune requires an explicit gameplay scope/build rather than a documentation-only commit.

For the selected S1.42AD Microwave spawn-rarity scope, source files are not equivalent to a candidate. The exact target, safe owner path, compiled DLL, profile diff and runtime evidence must all be established before promotion.
