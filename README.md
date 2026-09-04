# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current status

Game: **Lethal Company V81**

### Last fully accepted full-normal-stack baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

S1.42U remains the accepted rollback baseline until a newer candidate passes fresh runtime validation.

### Latest runtime-tested tuning candidate

**S1.42X — Jetpack Pikmin ACU Retune**

`Profiles/LC V1 S1.42X Jetpack Pikmin ACU Retune.r2z`

SHA-256:

`57d8f9251236cf40eacf4366a21646ae8c51500b9ed6fa79cbc9b56c8daa611d`

Runtime evidence:

`RuntimeEvidence/S1.42X/20260904T115324Z/`

Raw runtime log SHA-256:

`6fe57bda1c2a2a9e2a910304890e47b3fffd606460225bfd142ffae9fd996a9d`

Verdict:

**TECHNICAL PATHS PASS / GAMEPLAY BALANCE AND AERIAL-DEFENSE SCOPE REJECT / NOT ACCEPTED**

Confirmed from S1.42X:

- project-local Jetpack architecture works;
- `jetpackAcceleration = 32f` is clearly perceptible but far too strong;
- Pikmin CarryStrength tuning is accepted at `3` for configured non-Purple types and `30` for Purple;
- Indoor Pikmin Spawn Chance remains `0.08`;
- the DawnLib provider-level Air Control Unit spawn-weight scaling path works;
- X only covered `code_rebirth:air_control_unit` and missed CodeRebirth's separate G.R.E.G. / Advanced Airspace Control object `code_rebirth:gunslinger_greg`.

Canonical assessment:

`Current/84_S1.42X_RUNTIME_ASSESSMENT_AND_S1.42Y_NEXT.md`

### Newest built candidate

**S1.42Y — Jetpack Aerial Defense Retune**

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Build run:

`33871219861` = **success**

Candidate record:

`Current/85_S1.42Y_BUILD_CANDIDATE_JETPACK_COMPLETE_AERIAL_DEFENSE.md`

Machine status:

`Current/Projektstatus_S1.42Y_CANDIDATE.json`

Frozen plan / Patch Safety Review:

`BuildSpecs/S1.42Y_PLAN.md`

S1.42Y was built directly from S1.42U; historical V/W/X tuning DLLs are not stacked into Y.

## S1.42Y exact tuning

### Jetpack

Project source:

`Patches/S142YJetpackAcceleration/`

Injected DLL SHA-256:

`fab15a520c1ff0172d33bc88303426d214b12135b34803f6e98689c295409c7e`

Behavior:

- exact `JetpackItem.Update()` local-player Prefix after ButteRyBalance;
- validated ButteRyBalance-owned baseline `10f -> 22f`;
- only the proven approximately-10f value is replaced;
- V49 handling/deceleration remains untouched;
- JetpackFixes collision/death/control behavior remains untouched;
- fail-closed dependency/version/Harmony-owner validation.

More Ship Upgrades progression:

- Jet Fuel `15 / 15`;
- Jetpack Thrusters `25 / 20`.

### Pikmin

- Indoor Pikmin Spawn Chance = `0.08`;
- Blue / Red / Yellow / White / Winged / Rock / Ice / Glow / Bulbmin CarryStrength = `3`;
- Purple Pikmin CarryStrength = `30`.

The CarryStrength values are user-confirmed and should not be reverted without new feedback.

### CodeRebirth aerial-defense systems

Project source:

`Patches/S142YCodeRebirthAerialDefenseSpawnTuning/`

Injected DLL SHA-256:

`e017ccb74d92df10442bb5f8651a776787954f4861309059ec6c497e000a3d45`

The Y patch transactionally validates and scales both exact DawnLib outside-map-object providers:

1. `code_rebirth:air_control_unit` — all 18 native moon/tag curves × `0.5`;
2. `code_rebirth:gunslinger_greg` — G.R.E.G. / Advanced Airspace Control — all 18 native moon/tag curves × `0.5`.

Both contracts must validate before either is modified. No other map-object provider is changed.

This is an exact 50% curve-amplitude/spawn-weight reduction. DawnLib later evaluates and rounds the resulting quantity, so a short runtime sample is not expected to show mathematically exact half-counts.

### Other carried tuning

- Functional Microwave Volume = `0.15`; subjective volume remains unverified if no Microwave is encountered;
- Microwave spawn rarity remains deferred;
- Immortal Snail `Rarity = 40`, `Max Snails = 2`.

## Exact S1.42Y archive result

ZIP members: `333`.

Changed existing members relative to S1.42U:

- `export.r2x`;
- `BepInEx/config/dev.idjut.SnailFork.cfg`;
- `BepInEx/config/CodeRebirth.cfg`;
- `BepInEx/config/com.malco.lethalcompany.moreshipupgrades.cfg`;
- `BepInEx/config/NoteBoxz.LethalMin.cfg`;
- the ten configured `BepInEx/config/Pikmin/*.cfg` files.

Added members only:

- `BepInEx/plugins/S142YJetpackAcceleration/S142YJetpackAcceleration.dll`;
- `BepInEx/plugins/S142YCodeRebirthAerialDefenseSpawnTuning/S142YCodeRebirthAerialDefenseSpawnTuning.dll`.

No mod package state/add/remove changes occurred.

## Exact next action

**Runtime-test S1.42Y. Do not build a successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`

Import/run:

`LC V1 S1.42Y Jetpack Aerial Defense Retune`

Because the candidate contains two project-local DLLs, use Gale:

**Advanced options -> Import all files**

unless the concrete import flow independently guarantees all custom files are retained.

Required log markers include:

- `Loading [S1.42Y Jetpack Acceleration 1.0.0]`;
- successful Jetpack dependency/Harmony-owner validation;
- `10 -> 22` Jetpack armed marker;
- `Loading [S1.42Y CodeRebirth Aerial Defense Spawn Tuning 1.0.0]`;
- CodeRebirth 1.6.9 / DawnLib 0.9.25 / DawnLib.Dusk 0.9.25 validation;
- Air Control Unit provider validated with exactly 18 curves;
- G.R.E.G. provider validated with exactly 18 curves;
- final transactional marker confirming both 18-curve sets were scaled by 0.5.

Gameplay focus:

- 22f should be clearly calmer than X/32f while stronger than the old 10/16 behavior;
- V49 handling, release, landing, hard contact and repeated flights remain sane;
- CarryStrength remains correct at 3 / Purple 30;
- both CodeRebirth aerial-defense systems remain functional and less common;
- Microwave 0.15 only needs evaluation if one appears;
- normal enemies, BCMER and Compatibility Fixes remain healthy;
- Work/no-task = 0;
- Leader-null = 0;
- Fatal = 0;
- no new project-local/compatibility exception flood;
- ingest a complete fresh runtime log.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/85_S1.42Y_BUILD_CANDIDATE_JETPACK_COMPLETE_AERIAL_DEFENSE.md`
3. `Current/84_S1.42X_RUNTIME_ASSESSMENT_AND_S1.42Y_NEXT.md`
4. `Current/Projektstatus_S1.42Y_CANDIDATE.json`
5. `BuildSpecs/S1.42Y_PLAN.md`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
10. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
11. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
12. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed information overrides older handover wording.

## Permanent anti-regression state

Preserve:

- exact BCMER 1.71.0;
- EnemyIsolation off;
- Compatibility Fixes v1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy lifecycle;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Deferred after S1.42Y

Do not mix into the active Y gate:

- equal interior probability and same rule for future interiors;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave rarity reduction;
- BCMER EventType equalization to 8 × 12.5%;
- final long S1.42 full-stack acceptance;
- AdditionalNetworking disconnect patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42Y_BUILD_AWAITING_RUNTIME_VALIDATION`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Y`.

No successor build is armed.

## Known non-functional drift

Older chronology sections in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` may contain stale local wording. Current code/config/runtime evidence and chronologically newer canonical documents are authoritative.

## Repository-first rule

Do not ask for a local repository clone or manual profile rebuild when the necessary profiles, build system and GitHub Actions infrastructure exist here.
