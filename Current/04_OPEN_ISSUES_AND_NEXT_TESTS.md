# 04 — Open Issues and Next Tests

## Closed accepted baseline — S1.42U

**PASS**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

S1.42U remains the last fully accepted full-normal-stack gameplay baseline.

## Closed tuning evaluation — S1.42Y

Runtime evidence:

`RuntimeEvidence/S1.42Y/20260904T123817Z/`

Raw log SHA-256:

`dc32b104b880199ef0b210be254946bad280d1992e6142f6913bf9602921435a`

Verdict:

**Technical paths PASS; candidate not promoted because balance retune requested.**

Confirmed:

- S1.42Y Jetpack plugin loaded, validated and armed `10 -> 22`;
- Air Control Unit provider validated with exactly 18 curves;
- G.R.E.G. provider validated with exactly 18 curves;
- transactional ×0.5 scaling applied to both complete sets;
- normal enemy activity present;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes error = 0;
- Fatal = 0.

Accepted by user:

- Functional Microwave volume `0.15`;
- CarryStrength non-Purple `3`, Purple `30`.

Retune requested:

- Jetpack 22f -> 18f;
- Indoor Pikmin Spawn Chance 0.08 -> 0.09.

Record:

`Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`

## Active gate — S1.42Z

**BUILD PASS / RUNTIME VALIDATION OPEN**

Candidate:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Candidate record:

`Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`

Plan / Patch Safety Review:

`BuildSpecs/S1.42Z_PLAN.md`

Build run:

`33874737048` — success

Automated build commit:

`267543634bb884bb447bf4bec320103ba75c9ff8`

## Exact S1.42Z changes

### Jetpack

- base acceleration `10f -> 18f`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Z Jetpack DLL SHA-256 `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- V49 handling/deceleration untouched;
- JetpackFixes safety behavior untouched;
- exact dependency/Harmony-owner fail-closed validation retained.

### LethalMin

- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple configured CarryStrength `3`;
- Purple CarryStrength `30`.

### CodeRebirth aerial defense

- Air Control Unit exact 18-curve provider ×0.5;
- G.R.E.G. exact 18-curve provider ×0.5;
- transactional validation: both contracts must pass before either changes;
- Z aerial DLL SHA-256 `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`.

### Accepted carried tuning

- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`.

## Exact next test

**Run S1.42Z. Do not build a successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

Import/run:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Use Gale `Advanced options -> Import all files` unless all custom files are otherwise guaranteed to import.

Minimum checks:

1. startup/main menu succeeds;
2. `Loading [S1.42Z Jetpack Acceleration 1.0.0]` appears;
3. Jetpack dependency/owner validation succeeds;
4. exact `10 -> 18` armed marker appears;
5. `Loading [S1.42Z CodeRebirth Aerial Defense Spawn Tuning 1.0.0]` appears;
6. CodeRebirth 1.6.9 / DawnLib 0.9.25 / Dusk 0.9.25 validate;
7. ACU validates exactly 18 curves;
8. G.R.E.G. validates exactly 18 curves;
9. final transactional ×0.5 applied marker appears;
10. no aerial-defense contract refusal;
11. Jetpack 18f feels acceptable and calmer than Y/22f;
12. V49 handling/inertia, release, landing, hard contact and repeated flights remain sane;
13. Jet Fuel 18/18 and Thrusters 25/20 remain reasonable if practical;
14. Indoor Pikmin density at 0.09 feels better than 0.08;
15. CarryStrength remains correct at 3 / Purple 30;
16. Microwave remains functional at accepted volume 0.15;
17. Snail remains functional at 40 / max 2;
18. BCMER, normal enemies and Compatibility Fixes remain healthy;
19. Work/no-task = 0;
20. Leader-null = 0;
21. Fatal = 0;
22. no new project-local exception flood;
23. upload the complete fresh log with the one-line PowerShell uploader recorded in the Z candidate doc.

## Verified restore invariants — do not reopen without evidence

- S1.42C-derived `LethalLevelLoader.cfg` moon power/spawn baseline;
- `Consistent Spawn Times = true`;
- exact BCMER 1.71.0;
- EnemyIsolation off;
- Compatibility Fixes v1.3.14;
- narrow Baboon Hawk -> Pikmin block with native lifecycle;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- normal enemy population.

## Deferred after S1.42Z

Do not silently mix into the active gate:

- equal probability for all installed interiors and same rule for future interiors;
- CullFactory exceptions for `junkrooms` / `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave spawn rarity reduction;
- BCMER EventTypes fixed to 8 × 12.5%;
- final long full-stack acceptance;
- AdditionalNetworking patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42Z;
- base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

No successor is armed.

## Mandatory one-line runtime upload

Whenever a new runtime profile is designated, ChatGPT must supply one self-contained PowerShell command with that exact profile name that uploads its `BepInEx\LogOutput.log` to `RuntimeInbox/Current/LogOutput.log`.

Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
