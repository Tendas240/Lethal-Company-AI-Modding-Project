# Functional Microwave and Immortal Snail

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted item/enemy tuning values plus active Microwave candidate boundary  
**Canonical-For:** `functional_microwave`, `immortal_snail`  
**Evidence:** `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, accepted profile snapshots, `Current/120_S1.42AD_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_SPAWN_RARITY_REDUCTION.md`  
**Related:** `Knowledge/CODEREBIRTH.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Functional Microwave

### Accepted audio value

- Volume = `0.15`

This value was accepted during the S1.42Z runtime/balance gate, carried forward by accepted S1.42AC, and is unchanged in S1.42AD.

### Spawn rarity — S1.42AD active candidate

The user explicitly specified on 2026-09-05 that Functional Microwaves should be encountered **half as often**.

The authorized target is therefore:

`SpawnScale = 0.5f`

This is a proportional spawn-curve amplitude target, not an absolute replacement rarity. The finalized S1.42AD plugin scales the validated Functional Microwave Moon/tag curve values and tangents by `0.5`, preserving each curve's shape and relative Moon/tag distribution.

S1.42AD candidate:

- Profile: `Profiles/LC V1 S1.42AD Functional Microwave Spawn Rarity Reduction.r2z`
- Profile SHA-256: `9fea61e677a154cbfe68380e7c9d6a1b9285ca821d7dcec93772413ede27cf8c`
- DLL SHA-256: `45f22f9b27e3ab7c853fe742bb7c2ce9bc94abc5a0856bb278c747076a2f99c7`
- Status: **BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

The exact target value is now user-authorized, but the S1.42AD artifact itself is **not yet gameplay-accepted** until its fresh runtime gate passes. S1.42AC remains the accepted baseline until that decision.

A short run is not expected to demonstrate an exact statistical 50% observed occurrence rate because effective map-object selection also depends on competing spawn weights and generation context. Runtime acceptance is based primarily on proof that the exact provider curves were deterministically scaled by `0.5` plus clean adjacent gameplay.

Historical intermediate volume proposals such as `0.7` or `0.5` are superseded by accepted Volume `0.15`; those old **volume** values must not be confused with the S1.42AD **spawn-scale** value `0.5`.

## Immortal Snail

Accepted current values:

- Rarity = `40`
- Max Snails = `2`

S1.42AD does not alter Immortal Snail tuning.

## Change discipline

Item/enemy balance values are gameplay state. Future retunes require an explicit gameplay scope/build rather than a documentation-only commit.

For S1.42AD, the exact target, narrow owner path, compiled DLL and profile diff are complete; fresh runtime evidence remains the outstanding acceptance gate.
