# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/00_CURRENT_STATE.md`
2. `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`
3. `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`
4. `Current/Projektstatus_S1.42Z_CANDIDATE.json`
5. `BuildSpecs/S1.42Z_PLAN.md`
6. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
9. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
10. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
11. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
12. `BuildSpecs/current.json`
13. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific wording.

## Accepted rollback baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

S1.42U remains the last fully accepted full-normal-stack baseline.

## Latest runtime result — S1.42Y

Profile SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Evidence:

`RuntimeEvidence/S1.42Y/20260904T123817Z/`

Raw log SHA-256:

`dc32b104b880199ef0b210be254946bad280d1992e6142f6913bf9602921435a`

Verdict:

**TECHNICAL PATHS PASS / BALANCE RETUNE REQUIRED / NOT ACCEPTED**

Y proved:

- exact Jetpack patch architecture works at 22f;
- complete ACU + G.R.E.G. transactional DawnLib provider scaling works;
- both providers validate with exactly 18 curves and are scaled ×0.5;
- normal enemies remain active;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes error = 0;
- Fatal = 0.

User accepted:

- Functional Microwave volume `0.15`;
- Pikmin CarryStrength non-Purple `3`, Purple `30`.

User requested successor tuning:

- Jetpack `22f -> 18f`;
- Indoor Pikmin Spawn Chance `0.08 -> 0.09`.

Canonical result:

`Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`

## Active runtime candidate — S1.42Z

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Build run:

`33874737048` — success

Build commit:

`267543634bb884bb447bf4bec320103ba75c9ff8`

S1.42Z was rebuilt directly from S1.42U and does not stack V/W/X/Y tuning DLLs.

## Exact S1.42Z scope

### Jetpack

- base acceleration `10 -> 18`;
- Jet Fuel `18 / 18`;
- Thrusters `25 / 20`;
- exact local-player `JetpackItem.Update()` Prefix after ButteRyBalance;
- V49 handling/deceleration untouched;
- JetpackFixes collision/death/control safety untouched.

Jetpack DLL SHA-256:

`9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

### LethalMin

- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple configured CarryStrength `3`;
- Purple CarryStrength `30`.

### CodeRebirth

- Air Control Unit: exact 18 curves ×0.5;
- G.R.E.G. / Advanced Airspace Control: exact 18 curves ×0.5;
- both exact contracts must validate before either is changed.

Aerial-defense DLL SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

### Other accepted tuning

- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`.

## Exact next action

**Runtime-test S1.42Z. Do not build another successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

Run:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Use Gale `Advanced options -> Import all files` unless custom files are otherwise guaranteed to import.

Minimum gate:

1. both S1.42Z project-local plugins load;
2. Jetpack dependency/owner validation passes and exact `10 -> 18` marker appears;
3. CodeRebirth/Dawn/Dusk versions validate;
4. ACU and G.R.E.G. each validate exactly 18 curves;
5. transactional ×0.5 applied marker appears;
6. Jetpack 18f feels acceptable;
7. V49 handling, release, landing, hard contact and repeated flight remain sane;
8. Indoor Pikmin density at 0.09 feels correct;
9. CarryStrength 3 / Purple 30 remains correct;
10. Microwave 0.15 remains correct;
11. normal enemies, BCMER and Compatibility Fixes remain healthy;
12. Work/no-task = 0;
13. Leader-null = 0;
14. Fatal = 0;
15. upload a complete fresh LogOutput.log with the exact self-contained PowerShell command in `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`.

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

## Deferred after Z

Do not mix into the Z gate:

- equal interior probability / future-interior rule;
- CullFactory exceptions;
- Mausoleum fog;
- Microwave spawn rarity;
- BCMER 8 × 12.5% EventTypes;
- final long full-stack acceptance;
- AdditionalNetworking patch without new evidence;
- LethalMin DespawnLumiknulls repair without stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42Z;
- base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

No successor is armed.

## Mandatory runtime upload UX

Every new test candidate response must contain exactly one self-contained PowerShell uploader with the exact Gale profile name. Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
