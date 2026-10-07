# 88 — Final Handover: S1.42Y Technical PASS / S1.42Z Runtime Next

**Date:** 2026-09-04  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`  
**Game:** Lethal Company V81  
**Repository is the source of truth.**

## Handover summary

The last fully accepted full-normal-stack baseline remains **S1.42U**. The newest completed runtime evaluation is **S1.42Y**, which passed the targeted technical paths but was not promoted because the user requested narrower balance values. The newest built and active runtime candidate is **S1.42Z**.

Do not reconstruct V/W/X/Y tuning by stacking their DLLs. S1.42Z was rebuilt directly from S1.42U and contains only the two Z project-local tuning DLLs.

## 1. Last fully accepted baseline — S1.42U

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Acceptance record:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Status:

**ACCEPTED FULL NORMAL STACK / ROLLBACK BASELINE**

Permanent accepted facts include:

- exact `SoftDiamond-BrutalCompanyMinusExtraReborn 1.71.0` enabled;
- EnemyIsolation disabled;
- S1.39 Compatibility Fixes `1.3.14` active;
- Compatibility Fixes DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- normal enemy population restored;
- accepted S1.42C-derived moon power/spawn baseline preserved;
- SpawnCycleFixes `Consistent Spawn Times = true`.

S1.42U remains accepted until a newer candidate passes its own fresh runtime gate.

## 2. Latest runtime-tested candidate — S1.42Y

Profile:

`Profiles/LC V1 S1.42Y Jetpack Aerial Defense Retune.r2z`

Profile SHA-256:

`f4ae0d93c9cff4f9441c24d1021e5d9b816861b8317d9ed8995fde67ebbd8d89`

Runtime evidence:

`RuntimeEvidence/S1.42Y/20260904T123817Z/`

Raw log SHA-256:

`dc32b104b880199ef0b210be254946bad280d1992e6142f6913bf9602921435a`

Raw log coverage:

- 1,507,644 bytes;
- 15,447 lines;
- 14,730 parsed runtime events;
- 32 Error-severity events;
- Fatal = 0.

Canonical runtime assessment:

`Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`

Verdict:

**TECHNICAL PATHS PASS / MICROWAVE + CARRY TUNING ACCEPTED / JETPACK + INDOOR PIKMIN BALANCE RETUNE REQUIRED / NOT ACCEPTED**

Confirmed technical results:

- `S1.42Y Jetpack Acceleration 1.0.0` loaded;
- ButteRyBalance `0.7.0`, JetpackFixes `1.6.3`, More Ship Upgrades `3.14.1` validated;
- exact local-player Jetpack patch armed at `10 -> 22`;
- `S1.42Y CodeRebirth Aerial Defense Spawn Tuning 1.0.0` loaded;
- CodeRebirth `1.6.9`, DawnLib `0.9.25`, Dusk `0.9.25` validated;
- `code_rebirth:air_control_unit` validated with exactly 18 curves;
- `code_rebirth:gunslinger_greg` validated with exactly 18 curves;
- both complete provider contracts were validated before mutation;
- all 18 ACU curves and all 18 G.R.E.G. curves were scaled by `0.5` transactionally;
- normal enemy activity present;
- Work/no-task = 0;
- Leader-null = 0;
- Compatibility Fixes Error = 0;
- unspawned NetworkObjectReference marker = 0;
- PikminNoticeZone regression marker = 0;
- Fatal = 0.

User-confirmed balance decisions after Y:

- Functional Microwave volume `0.15` = **accepted**;
- configured non-Purple Pikmin CarryStrength `3` = **accepted**;
- Purple Pikmin CarryStrength `30` = **accepted**;
- Jetpack `22f` should be reduced to `18f`;
- Indoor Pikmin Spawn Chance `0.08` should be increased to `0.09`.

The 32 Error-severity entries were classified as existing/non-Y setup or mod messages rather than a new project-local Y regression. The known classes are documented in `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`.

## 3. Active runtime candidate — S1.42Z

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

Gale profile name:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Profile SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

GitHub Actions build run:

`33874737048` — success

Automated build commit:

`267543634bb884bb447bf4bec320103ba75c9ff8`

Candidate record:

`Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`

Machine status:

`Current/Projektstatus_S1.42Z_CANDIDATE.json`

Plan / Patch Safety Reviews:

`BuildSpecs/S1.42Z_PLAN.md`

Readable profile snapshot:

`ProfileSources/S1.42Z/`

### S1.42Z exact tuning

Jetpack:

- base acceleration `10f -> 18f`;
- More Ship Upgrades Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- ButteRyBalance V49 handling/deceleration preserved;
- JetpackFixes collision/death/control safety preserved.

Jetpack DLL:

`BepInEx/plugins/S142ZJetpackAcceleration/S142ZJetpackAcceleration.dll`

SHA-256:

`9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`

LethalMin:

- `Indoor Pikmin Spawn Chance = 0.09`;
- Blue / Red / Yellow / White / Winged / Rock / Ice / Glow / Bulbmin `CarryStrength = 3`;
- Purple Pikmin `CarryStrength = 30`.

Authoritative LethalMin raw configs are under:

- `BepInEx/config/NoteBoxz.LethalMin.cfg`;
- `BepInEx/config/Pikmin/*.cfg`.

Gale/LethalConfig does not necessarily expose every LethalMin setting in its GUI; the raw BepInEx config files remain authoritative.

CodeRebirth aerial defense:

- `code_rebirth:air_control_unit`: exact 18 curves × `0.5`;
- `code_rebirth:gunslinger_greg`: exact 18 curves × `0.5`;
- both contracts must validate before either one is changed;
- no other map-object provider is modified.

Aerial-defense DLL:

`BepInEx/plugins/S142ZCodeRebirthAerialDefenseSpawnTuning/S142ZCodeRebirthAerialDefenseSpawnTuning.dll`

SHA-256:

`7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`

Important probability semantics: the patch halves DawnLib animation-curve amplitude/spawn weight. DawnLib evaluates and rounds the result, so this is not a guarantee of exactly half the observed objects in a short gameplay sample.

Other carried tuning:

- Functional Microwave `Volume = 0.15` — user accepted;
- Functional Microwave editing remains enabled;
- Immortal Snail `Rarity = 40`;
- Immortal Snail `Max Snails = 2`.

### Archive verification

S1.42Z was built directly from S1.42U:

- ZIP members = `333`;
- changed existing members vs U = `15`;
- added members = exactly two S1.42Z project-local DLLs;
- mod state changes = none;
- mod additions = none;
- mod removals = none;
- historical V/W/X/Y tuning DLLs are absent from the Z archive.

## 4. Exact next action

**Runtime-test S1.42Z. Do not build a successor first.**

Controller state:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

Import/run:

`LC V1 S1.42Z Jetpack Pikmin Retune`

Because Z contains two project-local DLLs, use Gale:

**Advanced options -> Import all files**

unless the exact import flow independently guarantees every custom file is retained.

Minimum runtime gate:

1. startup/main menu succeeds;
2. `S1.42Z Jetpack Acceleration 1.0.0` loads;
3. ButteRyBalance / JetpackFixes / More Ship Upgrades validation succeeds;
4. exact `10 -> 18` Jetpack armed marker appears;
5. `S1.42Z CodeRebirth Aerial Defense Spawn Tuning 1.0.0` loads;
6. CodeRebirth / DawnLib / Dusk exact versions validate;
7. ACU validates exactly 18 curves;
8. G.R.E.G. validates exactly 18 curves;
9. final transactional applied marker confirms both complete curve sets ×0.5;
10. no aerial-defense contract-refusal marker;
11. Jetpack 18f feels correct relative to Y/22f and old 16f;
12. release, V49 directional handling, repeated flight, ordinary landing and hard/high-speed contact remain sane;
13. Indoor Pikmin density at 0.09 feels correct;
14. CarryStrength remains correct at 3 / Purple 30;
15. Microwave remains good at accepted volume 0.15;
16. Snail remains functional at Rarity 40 / Max 2;
17. normal enemies remain active;
18. BCMER 1.71.0 remains healthy;
19. Compatibility Fixes 1.3.14 remains healthy;
20. Work/no-task = 0;
21. Leader-null = 0;
22. Fatal = 0;
23. no new project-local exception flood;
24. upload one complete fresh `LogOutput.log` using the exact self-contained PowerShell one-liner in `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`.

## 5. Permanent do-not-regress rules

Preserve all of the following unless new evidence explicitly reopens them:

- exact BCMER `1.71.0`; do not silently upgrade to 2.x;
- EnemyIsolation disabled;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- block only the narrow Hawk -> Pikmin entry points;
- preserve inherited PikminEnemy death/unlatch/task/lifecycle behavior;
- Pikmin -> Baboon Hawk attack remains allowed;
- Puffer -> Pikmin protection remains;
- `Thumper Bite Limit = 3`;
- Crawler remains absent from LethalMin Attack Blacklist;
- normal enemy population remains restored;
- S1.42C-derived moon power/spawn baseline remains authoritative;
- SpawnCycleFixes `Consistent Spawn Times = true`.

Never repeat the S1.42R approach of disabling the entire `LethalMin.BaboonBirdPikminEnemy` component just to prevent one interaction.

Every project-local runtime/Harmony/compatibility patch must comply with:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Prefer the narrowest exact interception point. Do not replace a broad foreign lifecycle, global hazard loop, shared spawn loop, network lifecycle, or save path when a specific contract can be modified safely.

## 6. Monitor-only observations

Do not patch these without stronger reproducibility or user-facing impact:

- historical S1.42S disconnect-only PikminNoticeZone / unspawned NetworkObjectReference exception;
- historical S1.42T one-off AloeChase FSB load-state message;
- historical S1.42W `InvalidOperationException: Collection was modified` in `PikminManager.DespawnLumiknulls()` during teardown/despawn;
- known loaforcsSoundAPI/HarmonyX TypeLoadException class;
- known SoftMask/SoftMasking setup exceptions;
- Y's existing setup/mod Error-severity classes documented in `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`.

## 7. Deferred scopes after Z

Do not silently mix these into the active Z runtime gate:

- equal effective probability for all installed interiors;
- permanent rule that newly added interiors receive the same effective probability unless deliberately overridden;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes equalization to fixed `8 × 12.5%`;
- final long S1.42 full-stack acceptance run;
- AdditionalNetworking patching without reproducible/user-facing evidence;
- LethalMin `DespawnLumiknulls()` repair without stronger evidence;
- cosmetic documentation cleanup.

## 8. Known non-functional documentation drift

Older chronology subsections in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` may contain stale local wording. The accepted code/config/runtime evidence and the chronologically newer canonical files are authoritative.

Keep cosmetic cleanup separate from active runtime/gameplay work.

## 9. Controllers at handover

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42Z_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base profile = `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`;
- base SHA-256 = `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`;
- no patches/builds/assertions armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42Z`

`RuntimeInbox/Current/` is expected to contain only `.gitkeep` until the next local S1.42Z runtime log is uploaded.

## 10. Read order for the next chat

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/88_FINAL_HANDOVER_S1.42Y_PASS_S1.42Z_NEXT.md`
3. `Current/87_S1.42Z_BUILD_CANDIDATE_JETPACK_PIKMIN_RETUNE.md`
4. `Current/86_S1.42Y_RUNTIME_ASSESSMENT_AND_S1.42Z_NEXT.md`
5. `Current/Projektstatus_S1.42Z_CANDIDATE.json`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `BuildSpecs/S1.42Z_PLAN.md`
10. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
11. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
12. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
13. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
14. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
15. `BuildSpecs/current.json`
16. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed information overrides older version-specific wording.