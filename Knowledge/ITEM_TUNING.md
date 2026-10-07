# Functional Microwave and Immortal Snail

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted item/enemy tuning values and Functional Microwave runtime contract  
**Canonical-For:** `functional_microwave`, `immortal_snail`  
**Evidence:** `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`, `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`  
**Related:** `Knowledge/CODEREBIRTH.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-06

## Functional Microwave

Accepted audio value is `Volume = 0.15`. Accepted spawn tuning is **half frequency weight**, represented by `SpawnScale = 0.5f`; this is proportional scaling of the effective Moon/tag curve amplitudes, not an absolute replacement rarity.

S1.42AD is rejected because its fail-closed provider contract assumed zero Interior curves while runtime exposed 18. The desired `0.5` target itself was not rejected.

S1.42AE corrected the provider model to exact 18 Moon/tag + 18 Interior/tag curves and scale only the Moon/tag table, but its code never executed because the long Gale profile identity produced a 262-character nested SoundAPI LC-binding path and BepInEx/Mono failed before chainloader startup despite the DLL being physically present. S1.42AE is superseded for packaging, not rejected for Microwave logic.

**S1.42AF — Path-Length-Safe Microwave Packaging is now accepted.** Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. It was built directly from S1.42AC, shortened the Gale identity, and reused the unchanged S1.42AE provider source. The tested nested LC binding path measured 226 characters and BepInEx reached normal runtime.

Fresh evidence at `RuntimeEvidence/S1.42AF/20260905T223738Z/` validated CodeRebirth `1.6.9`, DawnLib/Dusk `0.9.25`, `PrioritiseMoons=true`, exactly 18 Moon/tag curves and 18 Interior/tag curves, and the final marker that 18 Moon/tag curves were scaled by `0.5` while all 18 Interior curves were validation-only and were not mutated. Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`.

Historical volume proposals such as `0.7` or `0.5` are superseded by accepted Volume `0.15`; those old volume values must not be confused with the accepted spawn-scale value `0.5`.

## Immortal Snail

Accepted current values remain Rarity `40` and Max Snails `2`. S1.42AD, S1.42AE and S1.42AF do not alter Immortal Snail tuning.

## Change discipline

Item/enemy balance values are gameplay state. Future retunes require an explicit gameplay scope/build rather than a documentation-only commit. The Functional Microwave correction is closed by S1.42AF acceptance. The current open Mouth Dog / Pikmin compatibility finding is a separate interaction scope and does not alter Microwave or Immortal Snail tuning.
