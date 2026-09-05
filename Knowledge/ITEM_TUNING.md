# Functional Microwave and Immortal Snail

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted item/enemy tuning values plus current Microwave correction boundary  
**Canonical-For:** `functional_microwave`, `immortal_snail`  
**Evidence:** `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`  
**Related:** `Knowledge/CODEREBIRTH.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Functional Microwave

Accepted audio value remains `Volume = 0.15`. The user-authorized spawn target remains **half as often**, represented by `SpawnScale = 0.5f`; this is a proportional curve-amplitude target, not an absolute replacement rarity.

S1.42AD is rejected because its fail-closed provider contract assumed zero Interior curves while runtime exposed 18. The desired 0.5 target was not rejected.

S1.42AE corrected the functional provider model to exact 18 Moon/tag + 18 Interior/tag curves and scale only the Moon/tag table, but its code never executed because the long Gale profile name pushed the nested SoundAPI LC-binding path to 262 characters and BepInEx/Mono failed before chainloader startup despite the DLL being physically present. S1.42AE is therefore superseded for packaging, not rejected for Microwave logic.

Current active candidate is **S1.42AF — Path-Length-Safe Microwave Packaging**: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. It was built directly from accepted S1.42AC, uses short Gale name `LC V1 S1.42AF Microwave Fix`, and reuses the unchanged S1.42AE provider source. Runtime validation is outstanding. See `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md` and `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`.

Historical volume proposals such as `0.7` or `0.5` are superseded by accepted Volume `0.15`; those old volume values must not be confused with the current spawn-scale target `0.5`.

## Immortal Snail

Accepted current values remain Rarity `40` and Max Snails `2`. S1.42AD, S1.42AE and S1.42AF do not alter Immortal Snail tuning.

## Change discipline

Item/enemy balance values are gameplay state. Future retunes require an explicit gameplay scope/build rather than a documentation-only commit. The immediate Functional Microwave work is the S1.42AF runtime gate; no later successor is armed.
