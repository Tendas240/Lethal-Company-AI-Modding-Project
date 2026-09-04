# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
2. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
3. `Current/00_CURRENT_STATE.md`
4. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
5. `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`
6. `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`
7. `Current/88_FINAL_HANDOVER_S1.42Y_PASS_S1.42Z_NEXT.md`
8. `Current/89_REPOSITORY_HANDOVER_AUDIT_S1.42Z.md`
9. `Current/06_RECENT_WORK_S1.42N-S1.42Z.md`
10. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
11. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
12. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
13. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
14. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
15. `BuildSpecs/current.json`
16. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific wording. In particular, the S1.42Y-to-Z handover files are historical pre-acceptance context; `Current/90` and `Projektstatus_S1.42Z_ACCEPTED.json` are authoritative for the current baseline.

## Canonical accepted baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED**

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

Profile SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance:

`Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

Raw log SHA-256:

`ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42U remains the previous pre-retune rollback artifact, not the latest accepted baseline.

## Why S1.42Z is accepted

Fresh runtime evidence confirms:

- S1.42Z Jetpack Acceleration `1.0.0` loaded;
- ButteRyBalance `0.7.0`, JetpackFixes `1.6.3`, More Ship Upgrades `3.14.1` validated;
- exact Jetpack baseline `10 -> 18` armed;
- S1.42Z CodeRebirth Aerial Defense Spawn Tuning `1.0.0` loaded;
- CodeRebirth `1.6.9`, DawnLib `0.9.25`, Dusk `0.9.25` validated;
- ACU provider exactly 18 curves;
- G.R.E.G. provider exactly 18 curves;
- complete ACU + G.R.E.G. curve sets transactionally scaled ×0.5;
- no aerial-defense contract refusal;
- EnemyIsolation runtime marker confirms diagnostic isolation is disabled;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- unspawned NetworkObjectReference marker = 0;
- PikminNoticeZone regression marker = 0;
- Fatal = 0;
- no Error-severity output from either S1.42Z project-local plugin.

The user reported that everything is in order from their side, closing the subjective balance/runtime gate.

Coverage:

- 1,586,159-byte log;
- 16,094 lines;
- 15,325 parsed runtime events;
- 32 Error-severity events;
- Fatal = 0.

The 32 Error-severity entries remain in known non-project-local/setup classes and do not justify a new patch without stronger evidence.

## Accepted S1.42Z scope

### Jetpack

- base acceleration `10 -> 18`;
- Jet Fuel `18 / 18`;
- Thrusters `25 / 20`;
- ButteRyBalance V49 handling/deceleration untouched;
- JetpackFixes safety behavior untouched.

Jetpack DLL SHA-256:

`9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

### LethalMin

- Indoor Pikmin Spawn Chance `0.09`;
- configured non-Purple CarryStrength `3`;
- Purple CarryStrength `30`.

### CodeRebirth aerial defense

- Air Control Unit: exact 18 curves ×0.5;
- G.R.E.G. / Advanced Airspace Control: exact 18 curves ×0.5;
- both exact contracts validate before either changes;
- no other map-object provider modified.

Aerial-defense DLL SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

The scaling is exact curve-amplitude/spawn-weight ×0.5, not a guarantee of exact half-counts in a short sample because DawnLib evaluates and rounds the resulting spawn amount.

### Other accepted tuning

- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`.

## Permanent anti-regression state

Preserve:

- exact BCMER `1.71.0`; do not silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`, DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin block only;
- native inherited PikminEnemy lifecycle;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`.

Do not repeat the S1.42R whole-component disable approach.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Monitor only

Do not patch without stronger reproducibility or user-facing impact:

- historical S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- historical S1.42T one-off AloeChase FSB load-state message;
- historical S1.42W `PikminManager.DespawnLumiknulls()` collection-modified teardown exception;
- known loaforcsSoundAPI/HarmonyX `TypeLoadException` class;
- known SoftMask/SoftMasking setup exception classes;
- existing non-project-local Error-severity classes.

## Exact next state

**No successor build is armed.**

S1.42Z is the accepted base for future work.

The next planned gameplay/config scope, when explicitly requested by the user, is:

- equal effective probability for every currently installed interior;
- keep the same equal-probability rule for future added interiors unless explicitly overridden.

Do not silently mix other deferred work into that stage.

Later deferred scopes:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking patch only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_ACCEPTANCE`;
- base = accepted S1.42Z;
- base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`;
- no build work armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

`RuntimeInbox/Current/` contains only `.gitkeep` after successful ingestion.

## Known non-functional drift

Older chronology wording in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` are not fully current. Newer canonical docs, code/config and runtime evidence are authoritative. Keep cosmetic cleanup separate from gameplay/runtime work.

## Mandatory runtime upload UX

Every future new test candidate response must contain exactly one self-contained PowerShell uploader with the exact Gale profile name. Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
