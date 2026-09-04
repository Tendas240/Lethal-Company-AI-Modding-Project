# 00 — Current State

**Updated:** 2026-09-04 — S1.42Z runtime accepted  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Repository is the source of truth.**

## Canonical accepted baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED**

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

Gale profile name:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Profile SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Canonical runtime acceptance:

`Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Machine-readable accepted status:

`Current/Projektstatus_S1.42Z_ACCEPTED.json`

S1.42U remains the previous pre-retune rollback artifact, but S1.42Z is now the latest accepted full-normal-stack baseline.

## S1.42Z runtime evidence

Evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

Raw LogOutput.log SHA-256:

`ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

Coverage:

- 1,586,159 bytes;
- 16,094 lines;
- 15,325 parsed runtime events;
- 32 Error-severity events;
- Fatal = 0.

Runtime gate confirmed:

- S1.42Z Jetpack Acceleration `1.0.0` loaded;
- ButteRyBalance `0.7.0`, JetpackFixes `1.6.3`, More Ship Upgrades `3.14.1` validated;
- exact Jetpack `10 -> 18` armed marker present;
- S1.42Z CodeRebirth Aerial Defense Spawn Tuning `1.0.0` loaded;
- CodeRebirth `1.6.9`, DawnLib `0.9.25`, Dusk `0.9.25` validated;
- Air Control Unit provider validated with exactly 18 curves;
- G.R.E.G. / Advanced Airspace Control provider validated with exactly 18 curves;
- both full provider sets transactionally scaled ×0.5;
- no aerial-defense contract refusal observed;
- EnemyIsolation diagnostic isolation disabled at runtime;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- unspawned NetworkObjectReference marker = 0;
- PikminNoticeZone regression marker = 0;
- Fatal = 0;
- neither S1.42Z project-local plugin emitted an Error-severity entry.

The user reported the tested runtime behavior as satisfactory and stated that everything is in order from their side. The subjective balance gate is therefore closed and S1.42Z is accepted.

## Accepted S1.42Z tuning

### Jetpack

- project-local base acceleration `10f -> 18f`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- ButteRyBalance V49 handling/deceleration preserved;
- JetpackFixes collision/death/control safety preserved.

Jetpack DLL SHA-256:

`9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

### LethalMin

- Indoor Pikmin Spawn Chance `0.09`;
- configured non-Purple CarryStrength `3`;
- Purple CarryStrength `30`.

### CodeRebirth aerial defense

- `code_rebirth:air_control_unit`: exact 18 curves ×0.5;
- `code_rebirth:gunslinger_greg`: exact 18 curves ×0.5;
- both contracts validate before either is modified;
- no other map-object provider is touched.

Aerial-defense DLL SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

The ×0.5 operation is exact curve-amplitude/spawn-weight scaling. DawnLib evaluates and rounds the result, so short-run observed counts do not need to be exact half-counts.

### Other accepted tuning

- Functional Microwave Volume `0.15`;
- Immortal Snail `Rarity = 40`, `Max Snails = 2`.

## Error-severity assessment

The S1.42Z log contains 32 Error-severity events, equal to the preceding S1.42Y total. Observed exception classes remain within already monitored non-project-local/setup classes, including the known loaforcsSoundAPI/HarmonyX `TypeLoadException` and SoftMask/SoftMasking setup `NullReferenceException` class.

There is no S1.42Z project-local Error-severity source and no Fatal. Do not patch these monitor-only classes without stronger reproducibility or user-facing impact.

## Permanent compatibility state to preserve

- exact BCMER `1.71.0` enabled; do not silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`, DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy lifecycle preserved;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection preserved;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`.

Never repeat the S1.42R approach of disabling the complete `BaboonBirdPikminEnemy` component merely to block one interaction.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Monitor-only observations

Do not patch without stronger reproducibility or user-facing impact:

- historical S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- historical S1.42T one-off AloeChase FSB load-state message;
- historical S1.42W `PikminManager.DespawnLumiknulls()` collection-modified teardown exception;
- known loaforcsSoundAPI/HarmonyX TypeLoadException class;
- known SoftMask/SoftMasking setup exceptions;
- existing non-project-local Error-severity classes.

## Next planned work

**No successor build is armed.**

S1.42Z is accepted and should be used as the base for the next explicitly requested stage.

The next planned gameplay/config scope is:

- equal effective probability for all currently installed interiors;
- preserve the same equal-probability rule for future added interiors unless explicitly overridden.

Do not silently mix unrelated deferred scopes into that stage.

Later deferred scopes:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes fixed to `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking patch only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.

## Known non-functional drift

- older chronology subsections in `Current/02_TECHNICAL_BASELINE.md` contain stale local current wording;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` do not perfectly describe accepted v1.3.14 behavior.

Chronologically newer current documents, actual code/config and runtime evidence are authoritative. Keep cosmetic cleanup separate from gameplay/runtime changes.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_ACCEPTANCE`;
- base = accepted S1.42Z;
- base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`;
- no patches/builds/assertions armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

`RuntimeInbox/Current/` contains only `.gitkeep` after successful S1.42Z ingestion.

No successor is armed.

## Mandatory runtime upload rule

For every future new profile designated for testing, ChatGPT must provide one exact, self-contained PowerShell command using that exact Gale profile name to upload `BepInEx\LogOutput.log` to `RuntimeInbox/Current/LogOutput.log`.

Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
