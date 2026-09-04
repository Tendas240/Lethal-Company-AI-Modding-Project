# 00 — Current State

**Updated:** 2026-09-04 — S1.42Y evaluated; S1.42Z built; runtime validation open  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Last fully accepted baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

S1.42U remains the canonical accepted rollback baseline until a later candidate passes fresh runtime validation.

## S1.42Y runtime result

Profile:

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

Profile SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Runtime evidence:

`RuntimeEvidence/S1.42Y/20260904T123817Z/`

Raw log SHA-256:

`dc32b104b880199ef0b210be254946bad280d1992e6142f6913bf9602921435a`

Verdict:

**TECHNICAL PATHS PASS / MICROWAVE + CARRY TUNING ACCEPTED / JETPACK + INDOOR PIKMIN BALANCE RETUNE REQUIRED / NOT ACCEPTED**

Canonical record:

`Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`

Confirmed:

- S1.42Y Jetpack plugin loaded, exact dependencies/owners validated and `10 -> 22` armed;
- Air Control Unit provider validated with exactly 18 curves;
- G.R.E.G. / Advanced Airspace Control provider validated with exactly 18 curves;
- both complete curve sets were transactionally scaled ×0.5;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes error = 0;
- Fatal = 0;
- normal enemy activity was present.

User decisions:

- Microwave volume `0.15` accepted;
- Pikmin CarryStrength `3` / Purple `30` accepted;
- Jetpack should move `22f -> 18f`;
- Indoor Pikmin Spawn Chance should move `0.08 -> 0.09`.

The 32 Error-severity entries in Y were classified as existing/non-Y setup or mod messages; neither Y project-local plugin emitted a runtime error and no Fatal followed.

## Active candidate

**S1.42Z — Jetpack Pikmin Retune**

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Build run:

`33874737048` — success

Automated build commit:

`267543634bb884bb447bf4bec320103ba75c9ff8`

Candidate record:

`Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`

Machine status:

`Current/Projektstatus_S1.42Z_CANDIDATE.json`

Plan / Patch Safety Reviews:

`BuildSpecs/S1.42Z_PLAN.md`

Snapshot:

`ProfileSources/S1.42Z/`

## Exact S1.42Z tuning

### Jetpack

- project-local base acceleration `10f -> 18f`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- V49 handling/deceleration untouched;
- JetpackFixes safety behavior untouched.

Jetpack DLL SHA-256:

`9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

### LethalMin

- Indoor Pikmin Spawn Chance `0.09`;
- all configured non-Purple CarryStrength `3`;
- Purple CarryStrength `30`.

### CodeRebirth aerial defense

- `code_rebirth:air_control_unit`: exact 18 curves ×0.5;
- `code_rebirth:gunslinger_greg`: exact 18 curves ×0.5;
- both contracts must validate before either is modified;
- no other map-object provider is touched.

Aerial-defense DLL SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

### Other tuning

- Functional Microwave Volume `0.15` — user accepted;
- Immortal Snail `Rarity = 40`, `Max Snails = 2`.

## Archive verification

S1.42Z was built directly from S1.42U:

- ZIP members = 333;
- changed existing members = 15;
- added members = exactly two S1.42Z DLLs;
- no mod package state/add/remove changes;
- historical V/W/X/Y tuning DLLs are absent.

## Immediate next action

**Runtime-test S1.42Z. Do not build a successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

Run:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Use Gale:

**Advanced options -> Import all files**

unless the exact import flow independently guarantees custom DLL retention.

Runtime focus:

1. both Z plugins load;
2. Jetpack dependency/Harmony-owner checks pass and exact `10 -> 18` marker appears;
3. CodeRebirth/Dawn/Dusk versions validate;
4. ACU and G.R.E.G. each validate 18 curves;
5. final transactional ×0.5 marker appears;
6. Jetpack 18f feels right relative to Y/22f and prior 16f;
7. V49 handling, release, repeated flight and landing/hard contact remain sane;
8. Indoor Pikmin density at 0.09 feels better than 0.08;
9. CarryStrength remains correct at 3 / Purple 30;
10. Microwave remains good at 0.15;
11. normal enemies, BCMER and Compatibility Fixes remain healthy;
12. Work/no-task = 0;
13. Leader-null = 0;
14. Fatal = 0;
15. upload the complete fresh log using the exact one-line PowerShell command in `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`.

## Permanent compatibility state to preserve

- exact BCMER 1.71.0 enabled;
- EnemyIsolation off;
- Compatibility Fixes 1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
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

## Deferred scopes — do not mix into Z

- equal interior probability and future-interior equal-probability rule;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Microwave spawn rarity reduction;
- BCMER EventType equalization to 8 × 12.5%;
- final long full-stack acceptance;
- AdditionalNetworking patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = built S1.42Z candidate;
- base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

No successor is armed.

## Mandatory runtime upload rule

For every new profile designated for testing, ChatGPT must provide one exact, self-contained PowerShell command using that exact Gale profile name to upload `BepInEx\LogOutput.log` to `RuntimeInbox/Current/LogOutput.log`.

Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
