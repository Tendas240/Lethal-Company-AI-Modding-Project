# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/00_CURRENT_STATE.md`
2. `Current/85_S1.42Y_BUILD_CANDIDATE_JETPACK_COMPLETE_AERIAL_DEFENSE.md`
3. `Current/84_S1.42X_RUNTIME_ASSESSMENT_AND_S1.42Y_NEXT.md`
4. `Current/Projektstatus_S1.42Y_CANDIDATE.json`
5. `BuildSpecs/S1.42Y_PLAN.md`
6. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
9. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
10. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
11. `BuildSpecs/current.json`
12. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer S1.42Y documents define the active test candidate. S1.42U remains the last fully accepted gameplay baseline.

## Accepted rollback baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

## Latest tested tuning result — S1.42X

S1.42X profile:

`Profiles/LC V1 S1.42X Jetpack Pikmin ACU Retune.r2z`

SHA-256:

`57d8f9251236cf40eacf4366a21646ae8c51500b9ed6fa79cbc9b56c8daa611d`

Runtime evidence:

`RuntimeEvidence/S1.42X/20260904T115324Z/`

Raw log SHA-256:

`6fe57bda1c2a2a9e2a910304890e47b3fffd606460225bfd142ffae9fd996a9d`

Verdict:

**TECHNICAL PATHS PASS / GAMEPLAY BALANCE AND AERIAL-SCOPE REJECT / NOT ACCEPTED**

Important findings:

- Jetpack `32f` proved `jetpackAcceleration` is the correct perceptible tuning lever but was far too strong;
- Pikmin CarryStrength `3` for configured non-Purple types and `30` for Purple is user-approved and must be preserved;
- Indoor Pikmin Spawn Chance remains `0.08`;
- the DawnLib Air Control Unit provider-level ×0.5 curve architecture worked;
- X missed CodeRebirth's separate `code_rebirth:gunslinger_greg` / G.R.E.G. / Advanced Airspace Control provider;
- Work/no-task = 0;
- Leader-null = 0;
- Fatal = 0;
- Compatibility Fixes error count = 0;
- normal enemies remained active.

Canonical record:

`Current/84_S1.42X_RUNTIME_ASSESSMENT_AND_S1.42Y_NEXT.md`

## Active candidate — S1.42Y

**S1.42Y — Jetpack Aerial Defense Retune**

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Actions build run:

`33871219861` = success

Candidate record:

`Current/85_S1.42Y_BUILD_CANDIDATE_JETPACK_COMPLETE_AERIAL_DEFENSE.md`

S1.42Y was rebuilt directly from S1.42U, so V/W/X tuning DLLs are not stacked into it.

## Exact S1.42Y scope

### Jetpack

- project plugin: `Patches/S142YJetpackAcceleration/`;
- DLL SHA-256: `fab15a520c1ff0172d33bc88303426d214b12135b34803f6e98689c295409c7e`;
- exact `JetpackItem.Update()` local-player Prefix after ButteRyBalance;
- validated base `10f -> 22f`;
- V49 handling/deceleration untouched;
- JetpackFixes safety logic untouched;
- exact dependency/Harmony-owner fail-closed checks.

More Ship Upgrades:

- Jet Fuel = `15 / 15`;
- Jetpack Thrusters = `25 / 20`.

### Pikmin

- Indoor Pikmin Spawn Chance = `0.08`;
- Blue / Red / Yellow / White / Winged / Rock / Ice / Glow / Bulbmin CarryStrength = `3`;
- Purple Pikmin CarryStrength = `30`.

### CodeRebirth aerial defense

- project plugin: `Patches/S142YCodeRebirthAerialDefenseSpawnTuning/`;
- DLL SHA-256: `e017ccb74d92df10442bb5f8651a776787954f4861309059ec6c497e000a3d45`;
- exact target 1: `code_rebirth:air_control_unit`;
- exact target 2: `code_rebirth:gunslinger_greg` / G.R.E.G. / Advanced Airspace Control;
- exactly 18 expected curves per target;
- both complete contracts validate before either changes;
- both complete curve sets then scale ×`0.5`;
- no global outside-hazard, prefab, RPC, network or save-state mutation.

The ×0.5 value is an exact curve-amplitude/spawn-weight reduction, not a guarantee of exactly half as many observed objects in a short sample after DawnLib's evaluation/rounding.

### Other tuning

- Functional Microwave Volume = `0.15`;
- Microwave rarity deferred;
- Immortal Snail `Rarity = 40`, `Max Snails = 2`.

## Permanent anti-regression state

Preserve:

- exact BCMER 1.71.0;
- EnemyIsolation off;
- Compatibility Fixes 1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin block only;
- native inherited PikminEnemy lifecycle;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`.

Never disable the entire `BaboonBirdPikminEnemy` just to block one interaction.

## Exact next action

**Runtime-test S1.42Y. Do not build another successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`

Run:

`LC V1 S1.42Y Jetpack Aerial Defense Retune`

Use Gale:

`Advanced options -> Import all files`

because Y contains two project-local DLLs.

Minimum gate:

1. Y Jetpack plugin loads, validates owners/dependencies and logs `10 -> 22` armed;
2. Y aerial-defense plugin loads;
3. CodeRebirth 1.6.9 / DawnLib 0.9.25 / DawnLib.Dusk 0.9.25 validate;
4. Air Control Unit provider validates with 18 curves;
5. G.R.E.G. provider validates with 18 curves;
6. final transactional marker confirms both complete curve sets ×0.5;
7. no contract-refusal marker;
8. 22f is clearly calmer than X/32f while still stronger than old 10/16 behavior;
9. V49 handling, release, landing, collision and repeated flight remain sane;
10. CarryStrength remains correct at 3 / Purple 30;
11. both aerial-defense systems remain functional and less common;
12. normal enemies, BCMER and Compatibility Fixes remain healthy;
13. Work/no-task = 0;
14. Leader-null = 0;
15. Fatal = 0;
16. no new compatibility/project-local error flood;
17. ingest the complete fresh runtime log.

## Deferred after Y

Do not mix into the Y gate:

- equal interior probability / future-interior rule;
- CullFactory exceptions;
- Mausoleum fog;
- Microwave rarity;
- BCMER 8 × 12.5% EventTypes;
- final long full-stack acceptance;
- AdditionalNetworking disconnect patch without new evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Y_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42Y candidate;
- base SHA-256 = `f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`

No successor is armed.
