# 00 — Current State

**Updated:** 2026-09-04 — S1.42Y built, runtime validation open  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Last fully accepted baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

S1.42U remains the canonical accepted rollback/gameplay baseline until a newer candidate passes fresh runtime validation.

## Latest runtime-tested tuning state — S1.42X

Profile:

`Profiles/LC V1 S1.42X Jetpack Pikmin ACU Retune.r2z`

SHA-256:

`57d8f9251236cf40eacf4366a21646ae8c51500b9ed6fa79cbc9b56c8daa611d`

Runtime evidence:

`RuntimeEvidence/S1.42X/20260904T115324Z/`

Raw log SHA-256:

`6fe57bda1c2a2a9e2a910304890e47b3fffd606460225bfd142ffae9fd996a9d`

Verdict:

**TECHNICAL PATHS PASS / GAMEPLAY BALANCE AND AERIAL-DEFENSE SCOPE REJECT / NOT ACCEPTED**

Confirmed findings:

- the project-local Jetpack architecture works;
- `jetpackAcceleration = 32f` is clearly perceptible but far too strong;
- user accepted Pikmin CarryStrength `3` for all configured non-Purple types and `30` for Purple;
- Indoor Pikmin Spawn Chance remains `0.08`;
- Air Control Unit DawnLib-provider curve scaling works technically;
- S1.42X only tuned `code_rebirth:air_control_unit` and therefore missed the separate CodeRebirth G.R.E.G. / Advanced Airspace Control map object `code_rebirth:gunslinger_greg`;
- Work/no-task = 0;
- Leader-null = 0;
- Fatal = 0;
- Compatibility Fixes project error count = 0;
- normal enemy population remained active.

Canonical record:

`Current/84_S1.42X_RUNTIME_ASSESSMENT_AND_S1.42Y_NEXT.md`

## Newest built candidate — S1.42Y

**S1.42Y — Jetpack Aerial Defense Retune**

Profile:

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Actions build run:

`33871219861` = success

Candidate record:

`Current/85_S1.42Y_BUILD_CANDIDATE_JETPACK_COMPLETE_AERIAL_DEFENSE.md`

Machine status:

`Current/Projektstatus_S1.42Y_CANDIDATE.json`

Plan / Patch Safety Review:

`BuildSpecs/S1.42Y_PLAN.md`

Snapshot:

`ProfileSources/S1.42Y/`

S1.42Y was rebuilt directly from S1.42U; no V/W/X tuning DLL is stacked into it.

## Exact S1.42Y tuning

### Jetpack

Project-local plugin:

`Patches/S142YJetpackAcceleration/`

Embedded DLL SHA-256:

`fab15a520c1ff0172d33bc88303426d214b12135b34803f6e98689c295409c7e`

Behavior:

- exact parameterless `JetpackItem.Update()` local-player Prefix;
- ordered after ButteRyBalance;
- validated owner-written baseline `10f -> 22f`;
- V49 handling/deceleration untouched;
- JetpackFixes safety behavior untouched;
- no original-method skip, extra transpiler, network or save-state mutation;
- fail-closed version/Harmony-owner validation.

More Ship Upgrades:

- Jet Fuel initial/incremental acceleration = `15 / 15`;
- Jetpack Thrusters initial/incremental maximum speed = `25 / 20`.

### Pikmin

- Indoor Pikmin Spawn Chance = `0.08`;
- Blue / Red / Yellow / White / Winged / Rock / Ice / Glow / Bulbmin CarryStrength = `3`;
- Purple Pikmin CarryStrength = `30`.

The CarryStrength values are user-confirmed and should be preserved.

### CodeRebirth aerial defense

Project-local plugin:

`Patches/S142YCodeRebirthAerialDefenseSpawnTuning/`

Embedded DLL SHA-256:

`e017ccb74d92df10442bb5f8651a776787954f4861309059ec6c497e000a3d45`

Exact targets:

1. `code_rebirth:air_control_unit` — Air Control Unit;
2. `code_rebirth:gunslinger_greg` — G.R.E.G. / Advanced Airspace Control.

The plugin validates both exact 18-curve DawnLib/Dusk provider contracts before changing either one, then scales both complete curve sets by `0.5`. No other map-object provider is modified.

This is an exact 50% curve-amplitude/spawn-weight reduction. Because DawnLib evaluates and rounds quantities later, do not require exactly half the observed objects in a short sample.

### Other carried tuning

- Functional Microwave Volume = `0.15`; subjective validation remains open if none is encountered;
- Microwave spawn rarity remains deferred;
- Immortal Snail `Rarity = 40`;
- Immortal Snail `Max Snails = 2`.

## Immediate next action

**Runtime-test S1.42Y. Do not build a successor yet.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`

Import/run:

`LC V1 S1.42Y Jetpack Aerial Defense Retune`

Use Gale:

`Advanced options -> Import all files`

because the profile contains two project-local DLLs.

Required runtime focus:

1. Y Jetpack plugin loads and logs exact `10 -> 22` armed marker;
2. Y aerial-defense plugin loads;
3. CodeRebirth 1.6.9 / DawnLib 0.9.25 / DawnLib.Dusk 0.9.25 validate;
4. Air Control Unit provider validates with exactly 18 curves;
5. G.R.E.G. provider validates with exactly 18 curves;
6. final transactional marker confirms both curve sets ×0.5;
7. no aerial-defense contract-refusal marker;
8. 22f Jetpack feels materially calmer than X/32f while stronger than old 10/16 behavior;
9. V49 handling, release/deactivation, landing, hard contact and repeated flights remain sane;
10. CarryStrength remains correct at 3 / Purple 30;
11. both aerial-defense systems remain functional and less common;
12. normal enemies, BCMER 1.71.0 and Compatibility Fixes 1.3.14 remain healthy;
13. Work/no-task = 0;
14. Leader-null = 0;
15. Fatal = 0;
16. no new compatibility/project-local error flood;
17. commit/ingest a complete fresh runtime log.

## Permanent compatibility state to preserve

- exact BCMER 1.71.0 enabled;
- EnemyIsolation off;
- Compatibility Fixes v1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy death/unlatch/task lifecycle;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived LethalLevelLoader moon spawn/power baseline;
- `Consistent Spawn Times = true`.

Never disable the whole `BaboonBirdPikminEnemy` merely to block Hawk -> Pikmin interaction.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Deferred scopes — do not mix into S1.42Y

- equal probability for all installed interiors and the same rule for future interiors;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- Functional Microwave rarity reduction;
- BCMER EventType equalization to 8 × 12.5%;
- final long S1.42 full-stack acceptance;
- AdditionalNetworking disconnect patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Y_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = built S1.42Y candidate;
- base SHA-256 = `f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`;
- no successor delta armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local `current` wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains historical comments that do not perfectly describe accepted v1.3.14 behavior.

Chronologically newer current documents, code/config and runtime evidence are authoritative. Keep cosmetic cleanup separate from gameplay/runtime tuning.
