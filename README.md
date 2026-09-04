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

## Latest completed runtime evaluation — S1.42Y

Profile:

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Runtime evidence:

`RuntimeEvidence/S1.42Y/20260904T123817Z/`

Raw runtime log SHA-256:

`dc32b104b880199ef0b210be254946bad280d1992e6142f6913bf9602921435a`

Verdict:

**TECHNICAL PATHS PASS / MICROWAVE + CARRY TUNING ACCEPTED / JETPACK + INDOOR PIKMIN BALANCE RETUNE REQUIRED / NOT ACCEPTED**

Canonical assessment:

`Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`

Y runtime proved:

- exact Jetpack interception path loads/arms cleanly at `22f`;
- exact Air Control Unit provider validates with 18 curves;
- exact G.R.E.G. / Advanced Airspace Control provider validates with 18 curves;
- both CodeRebirth aerial-defense providers are transactionally scaled ×0.5;
- normal enemy activity remains present;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- unspawned NetworkObjectReference marker = 0;
- PikminNoticeZone regression marker = 0;
- Fatal = 0.

User decisions after Y:

- Functional Microwave volume `0.15` is **accepted**;
- Pikmin CarryStrength `3` / Purple `30` remains **accepted**;
- Jetpack `22f` should be reduced to `18f`;
- Indoor Pikmin Spawn Chance `0.08` should be raised to `0.09`.

The 32 Error-severity entries in the Y log are catalogued in the assessment and classified as existing/non-Y setup or mod messages rather than a new project-local regression.

## Newest built candidate — S1.42Z

**S1.42Z — Jetpack Pikmin Retune**

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

Gale profile name:

`LC V1 S1.42Z Jetpack Pikmin Retune`

SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

GitHub Actions build run:

`33874737048` — success

Automated build commit:

`267543634bb884bb447bf4bec320103ba75c9ff8`

Candidate record:

`Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`

Final handover:

`Current/88_FINAL_HANDOVER_S1.42Y_PASS_S1.42Z_NEXT.md`

Repository handover audit:

`Current/89_REPOSITORY_HANDOVER_AUDIT_S1.42Z.md`

Machine status:

`Current/Projektstatus_S1.42Z_CANDIDATE.json`

Frozen/finalized plan and Patch Safety Reviews:

`BuildSpecs/S1.42Z_PLAN.md`

S1.42Z was rebuilt directly from S1.42U so historical V/W/X/Y tuning DLLs are not stacked into the candidate.

### Exact S1.42Z tuning

- Jetpack base acceleration `10 -> 18`;
- More Ship Upgrades Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- configured non-Purple Pikmin CarryStrength `3`;
- Purple Pikmin CarryStrength `30`;
- CodeRebirth Air Control Unit 18 exact curves × `0.5`;
- CodeRebirth G.R.E.G. 18 exact curves × `0.5`;
- Functional Microwave volume `0.15` — user accepted;
- Immortal Snail `Rarity = 40`, `Max Snails = 2`.

Project-local DLL SHA-256 values:

- S1.42Z Jetpack: `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- S1.42Z aerial defense: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`.

Archive verification:

- ZIP members: 333;
- 15 changed existing members vs S1.42U;
- exactly 2 added members: the Z DLLs;
- no mod package state/add/remove changes;
- historical tuning DLLs absent.

The aerial-defense ×0.5 operation halves DawnLib animation-curve amplitude/spawn weight. DawnLib later evaluates and rounds the result, so short-run observed object counts are not required to be mathematically exact half-counts.

## Exact next action

**Runtime-test S1.42Z. Do not build a successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

Import/run:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Because the candidate contains two project-local DLLs, use Gale:

**Advanced options -> Import all files**

unless the actual import path independently guarantees all custom files are retained.

Primary runtime focus:

- both Z plugins load and validate;
- Jetpack exact `10 -> 18` armed marker;
- ACU 18-curve validation;
- G.R.E.G. 18-curve validation;
- final transactional ×0.5 applied marker;
- Jetpack 18f feels acceptable and calmer than Y/22f;
- V49 handling, release, repeated flight, landing and hard/high-speed contact remain sane;
- Indoor Pikmin density at 0.09 feels correct;
- CarryStrength stays correct at 3 / Purple 30;
- Microwave 0.15 remains correct;
- normal enemies, BCMER and Compatibility Fixes remain healthy;
- Work/no-task = 0;
- Leader-null = 0;
- Fatal = 0;
- no new project-local exception flood.

The candidate-specific one-line PowerShell uploader is recorded in `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md` and must be supplied whenever Z is handed to the user for testing.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/88_FINAL_HANDOVER_S1.42Y_PASS_S1.42Z_NEXT.md`
3. `Current/89_REPOSITORY_HANDOVER_AUDIT_S1.42Z.md`
4. `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`
5. `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`
6. `Current/Projektstatus_S1.42Z_CANDIDATE.json`
7. `Current/00_CURRENT_STATE.md`
8. `Current/01_HANDOVER_CORE.md`
9. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
10. `BuildSpecs/S1.42Z_PLAN.md`
11. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
12. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
13. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
14. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
15. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
16. `BuildSpecs/current.json`
17. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed information overrides older handover wording. `Archive/` is historical evidence, not an automatically current state source.

## Permanent anti-regression state

Preserve:

- exact BCMER 1.71.0; do not silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes v1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
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

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Monitor-only observations

Do not patch without stronger reproducibility or user-facing impact:

- S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- S1.42T one-off AloeChase FSB load-state message;
- S1.42W `PikminManager.DespawnLumiknulls()` collection-modified teardown exception;
- known loaforcsSoundAPI/HarmonyX and SoftMask/SoftMasking setup exception classes;
- S1.42Y existing/non-project-local Error-severity classes documented in `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`.

## Deferred after S1.42Z

Do not mix into the active Z gate:

- equal interior probability and future-interior equal-probability rule;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventType equalization to 8 × 12.5%;
- final long S1.42 full-stack acceptance;
- AdditionalNetworking patch without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42Z_BUILD_AWAITING_RUNTIME_VALIDATION` with S1.42Z as its guarded base.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`.

`RuntimeInbox/Current/` contains only `.gitkeep` until the next runtime upload.

No successor build is armed.

## Known non-functional drift

Older chronology wording in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` are not fully current. Actual current code/config/runtime evidence and chronologically newer canonical documents are authoritative. Keep cosmetic cleanup separate from active runtime work.

## Repository-first and runtime-upload rule

Do not ask for a local repository clone or manual profile rebuild when GitHub infrastructure can do the work.

For every new profile the user is told to runtime-test, ChatGPT must automatically provide the exact profile-specific, self-contained PowerShell one-liner that uploads its `BepInEx\LogOutput.log` to `RuntimeInbox/Current/LogOutput.log`. Binding policy:

`Current/09_REPOSITORY_FIRST_AUTOMATION.md`
