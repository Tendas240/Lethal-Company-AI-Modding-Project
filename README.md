# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current canonical state

Game: **Lethal Company V81**

**Accepted full-normal-stack baseline:**

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED**

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

Gale profile name:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Profile SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Canonical runtime acceptance:

`Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Machine-readable accepted state:

`Current/Projektstatus_S1.42Z_ACCEPTED.json`

S1.42U remains the previous pre-retune rollback artifact, but S1.42Z is now the latest accepted gameplay baseline.

## S1.42Z runtime evidence

Evidence root:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

Raw log SHA-256:

`ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

Coverage:

- 1,586,159 bytes;
- 16,094 lines;
- 15,325 parsed runtime events;
- 32 Error-severity events;
- Fatal = 0.

Confirmed runtime gate:

- `S1.42Z Jetpack Acceleration 1.0.0` loaded;
- ButteRyBalance `0.7.0`, JetpackFixes `1.6.3`, More Ship Upgrades `3.14.1` validated;
- exact Jetpack `10 -> 18` marker present;
- `S1.42Z CodeRebirth Aerial Defense Spawn Tuning 1.0.0` loaded;
- CodeRebirth `1.6.9`, DawnLib `0.9.25`, Dusk `0.9.25` validated;
- Air Control Unit provider validated with exactly 18 curves;
- G.R.E.G. / Advanced Airspace Control provider validated with exactly 18 curves;
- both complete provider sets transactionally scaled ×0.5;
- no aerial-defense contract refusal observed;
- EnemyIsolation diagnostic isolation disabled;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- unspawned NetworkObjectReference marker = 0;
- PikminNoticeZone regression marker = 0;
- Fatal = 0;
- neither S1.42Z project-local plugin emitted Error-severity output.

The user reported the tested S1.42Z runtime behavior as fully satisfactory, so the subjective balance gate is closed.

## Accepted S1.42Z tuning

- Jetpack base acceleration `10 -> 18`;
- More Ship Upgrades Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- configured non-Purple Pikmin CarryStrength `3`;
- Purple Pikmin CarryStrength `30`;
- CodeRebirth Air Control Unit 18 exact curves ×`0.5`;
- CodeRebirth G.R.E.G. 18 exact curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail `Rarity = 40`, `Max Snails = 2`.

Project-local DLL SHA-256 values:

- Jetpack: `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- aerial defense: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`.

The aerial-defense ×0.5 operation halves DawnLib animation-curve amplitude/spawn weight. DawnLib evaluates and rounds the result, so short-run observed counts are not required to be exact half-counts.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
3. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
4. `Current/00_CURRENT_STATE.md`
5. `Current/01_HANDOVER_CORE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/06_RECENT_WORK_S1.42N-S1.42Z.md`
8. `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`
9. `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`
10. `Current/88_FINAL_HANDOVER_S1.42Y_PASS_S1.42Z_NEXT.md`
11. `Current/89_REPOSITORY_HANDOVER_AUDIT_S1.42Z.md`
12. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
13. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
14. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
15. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
16. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
17. `BuildSpecs/current.json`
18. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed information overrides older handover wording. `Current/88`, `Current/89`, and `Current/87` are retained as pre-acceptance handover/build history; `Current/90` and `Projektstatus_S1.42Z_ACCEPTED.json` are authoritative for the current accepted state.

## Permanent anti-regression state

Preserve:

- exact BCMER `1.71.0`; do not silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14` / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy lifecycle;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`.

Never repeat the S1.42R whole-component disable approach.

Project-local patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Current next state

**No successor build is armed.**

`BuildSpecs/current.json` is disabled at:

`IDLE_AFTER_S1.42Z_ACCEPTANCE`

with accepted S1.42Z as its guarded base.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`.

`RuntimeInbox/Current/` contains only `.gitkeep` after successful S1.42Z runtime ingestion.

The next planned gameplay/config scope, when explicitly requested, is:

- equal effective probability for all currently installed interiors;
- preserve the same equal-probability rule for future added interiors unless explicitly overridden.

Keep unrelated deferred scopes separate unless the user explicitly combines them:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes fixed to `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair only with stronger evidence;
- cosmetic documentation cleanup.

## Known monitor-only / non-functional issues

Do not patch without stronger reproducibility or user-facing impact:

- historical S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- historical S1.42T one-off AloeChase FSB load-state message;
- historical S1.42W `PikminManager.DespawnLumiknulls()` teardown exception;
- known loaforcsSoundAPI/HarmonyX TypeLoadException class;
- known SoftMask/SoftMasking setup exception classes;
- other existing non-project-local Error-severity classes.

Known non-functional documentation drift remains in older chronology wording under `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs`. Newer canonical documents, actual code/config and runtime evidence are authoritative.

## Repository-first and runtime-upload rule

Do not ask for a local repository clone or manual profile rebuild when the GitHub infrastructure can perform the work.

For every future new profile designated for runtime testing, ChatGPT must automatically provide the exact profile-specific self-contained PowerShell one-liner that uploads its `BepInEx\LogOutput.log` to `RuntimeInbox/Current/LogOutput.log`.

Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
