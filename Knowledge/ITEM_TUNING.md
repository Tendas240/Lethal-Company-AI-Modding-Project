# Functional Microwave and Immortal Snail

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted item/enemy tuning values plus current Microwave correction boundary  
**Canonical-For:** `functional_microwave`, `immortal_snail`  
**Evidence:** `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, accepted profile snapshots, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`  
**Related:** `Knowledge/CODEREBIRTH.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Functional Microwave

### Accepted audio value

- Volume = `0.15`

This value was accepted during the S1.42Z runtime/balance gate and remains the accepted value in S1.42AC. S1.42AD did not change it.

### Spawn rarity target

The user explicitly specified on 2026-09-05 that Functional Microwaves should be encountered **half as often**.

The authorized target remains:

`SpawnScale = 0.5f`

This is a proportional spawn-frequency/curve-amplitude target, not an absolute replacement rarity.

### S1.42AD result — rejected

S1.42AD attempted to implement the target through the Functional Microwave DawnLib `InsideInfo` provider with a fail-closed contract requiring `PrioritiseMoons = true`, 18 Moon/tag curves and 0 Interior/tag curves.

Fresh runtime evidence disproved the zero-Interior assumption. The actual provider exposed **18 Interior/tag curves**, including `code_rebirth:functional_microwave_ultra_high`. The patch correctly refused mutation and emitted no final application marker.

Therefore:

- S1.42AD is **RUNTIME REJECTED / NOT ACCEPTED**;
- its profile SHA-256 is `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`;
- rejection authority is `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`;
- runtime evidence is `RuntimeEvidence/S1.42AD/20260905T103333Z/`;
- the desired half-frequency target itself is **not rejected**;
- S1.42AC remains the accepted baseline.

Do not interpret the S1.42AD failure as evidence that `0.5` is the wrong balance value. It proves only that the provider-contract model used to apply that value was incomplete.

Before a corrected successor, resolve the actual Moon and Interior curve tables plus DawnLib's selection/evaluation semantics under `PrioritiseMoons = true`. Do not blindly scale both tables.

Historical intermediate volume proposals such as `0.7` or `0.5` are superseded by accepted Volume `0.15`; those old **volume** values must not be confused with the current **spawn-scale** target `0.5`.

## Immortal Snail

Accepted current values:

- Rarity = `40`
- Max Snails = `2`

S1.42AD did not alter Immortal Snail tuning.

## Change discipline

Item/enemy balance values are gameplay state. Future retunes require an explicit gameplay scope/build rather than a documentation-only commit.

For Functional Microwave rarity, the target is authorized but the implementation path is currently back in analysis. No corrected successor is built or armed yet.
