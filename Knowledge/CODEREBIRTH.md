# CodeRebirth and DawnLib Tuning

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted CodeRebirth ownership/tuning rules plus current Functional Microwave candidate boundary  
**Canonical-For:** `coderebirth`  
**Evidence:** `Current/03_PROJECT_CHRONOLOGY.md`, `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`  
**Related:** `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CURRENT_LIFECYCLE.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-05

## Package architecture

Modern project stack uses CodeRebirth with DawnLib. **Do not reinstall CodeRebirthLib**; it is a historical removed/forbidden dependency. Current owner versions remain CodeRebirth `1.6.9`, DawnLib `0.9.25`, DawnLib.Dusk `0.9.25`.

## Natural Currency / Flash Turret control

S1.40B established the accepted native-owner solution: keep `Clean Unusued Configs = false`; Coin/Crisp Dollar Bill/Wallet/Flash Turret editable; Currency inside moon/interior weights blank; Flash Turret inside weights blank with `Is Inside Hazard = false`. Do not blank `Money | Enemy Drop Rates`.

## CodeRebirth -> Pikmin utility protection

The cumulative compatibility plugin retains the direct utility-kill shield for Pikmin/Puffmin because config toggles alone did not cover every Autonomous Crane kill path.

## Accepted aerial-defense tuning

S1.42Z accepted transactional scaling of exactly `code_rebirth:air_control_unit` and `code_rebirth:gunslinger_greg`: all 18 Moon/tag curves x `0.5`; no other provider is modified. Accepted aerial-defense DLL SHA-256: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`.

## Functional Microwave rarity

Authorized target remains `SpawnScale = 0.5f` for `code_rebirth:functional_microwave` through `DawnMapObjectInfo.InsideInfo.SpawnWeights -> ProviderTable -> Dusk.MapObjectSpawnMechanics`.

S1.42AD is rejected history because its zero-Interior assumption drifted; runtime exposed 18 Interior/tag curves and the patch correctly refused mutation. The corrected contract established for S1.42AE and reused unchanged in S1.42AF is: one `MapObjectSpawnMechanics`, `PrioritiseMoons=true`, exactly 18 Moon/tag curves, exactly 18 Interior/tag curves, all curves valid. With Dusk 0.9.25 Moon priority, selection is exact Moon -> exact Interior fallback -> matching Moon tags; the tables are not combined. Scale only `CurvesByMoonOrTagName` x0.5 including values/tangents; validate but do not mutate `CurvesByInteriorOrTagName`.

### S1.42AE supersession

S1.42AE's functional code was never reached because BepInEx/Mono failed on the physically present nested SoundAPI binding at a 262-character full path. It is superseded for packaging/path-length reasons, not rejected for provider behavior. Authority: `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`.

### Current S1.42AF candidate

- Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`
- Gale profile name: `LC V1 S1.42AF Microwave Fix`
- Profile SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`
- DLL SHA-256: `41ae2442983d89d9b317b3930f1f53aefaa63e56bfeae0cdb198f43b0bac089f`
- Build run: `33993880634` — SUCCESS
- Build commit: `2cab9044579e74739669440699c763a32f0fe379`
- Candidate record: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`
- Status: **BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**

S1.42AF is built directly from accepted S1.42AC and reuses the unchanged S1.42AE source project. Expected runtime plugin identity therefore remains `S1.42AE CodeRebirth Microwave Spawn Tuning 1.0.0`. Archive delta remains isolated to Gale `export.r2x` metadata plus the plugin DLL, with no mod-state or config change.

Runtime acceptance requires healthy preloader/main menu/lobby under the short profile path, exact dependency validation, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both keysets, the final 18 Moon/tag curves x0.5 and 18 Interior validation-only marker, ordinary round generation/gameplay, and no new fatal/project-critical regression. S1.42AC remains the rollback baseline until explicit AF acceptance.
