# 00 — Current State

**Updated:** 2026-09-04 — S1.42W built, runtime validation open  
**Game:** Lethal Company V81  
**Repository:** `Tendas240/Lethal-Company-AI-Modding-Project`

## Last fully accepted baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

S1.42U remains the rollback/canonical accepted gameplay baseline until a newer candidate passes fresh runtime validation.

## S1.42V runtime result

S1.42V profile SHA-256:

`06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`

Evidence:

`RuntimeEvidence/S1.42V/20260904T095739Z/`

Raw log SHA-256:

`5e094086efef862abdbaf1bfdaab85fb8c8ed20d73d865c9f1bc902e08180dfd`

Verdict:

**Jetpack implementation architecture runtime PASS; balance magnitude rejected/superseded.**

The log proved:

- `S1.42V Jetpack Acceleration 1.0.0` loaded;
- ButteRyBalance 0.7.0 validated;
- JetpackFixes 1.6.3 validated;
- More Ship Upgrades 3.14.1 validated;
- the exact Jetpack prefix armed;
- Compatibility Fixes 1.3.14 loaded;
- Work/no-task = 0;
- Leader-null = 0;
- S1.39 Compatibility Fixes Error = 0;
- no Jetpack Harmony target/owner/order failure.

User feedback:

- `12f` upward acceleration was still too weak / lift-off too slow;
- Microwave `0.5` was still too loud.

Canonical record:

`Current/82_S1.42V_RUNTIME_TECHNICAL_PASS_BALANCE_REJECTED.md`

One AdditionalNetworking `NetworkObjectReference` Fatal occurred during local-disconnect teardown immediately after BCMER `OnLocalDisconnect`. It is monitor-only and not attributed to Jetpack gameplay without reproducibility/user impact.

## Newest built candidate

**S1.42W — Lift-Off Microwave Retune**

Profile:

`Profiles/LC V1 S1.42W Lift-Off Microwave Retune.r2z`

SHA-256:

`f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`

Status:

**BUILD PASS / RUNTIME VALIDATION REQUIRED / NOT ACCEPTED**

Build commit:

`165d102364438cace2fd2184af3fd091855ff0d7`

GitHub Actions run:

`33861561173` = **success**

Candidate record:

`Current/83_S1.42W_BUILD_CANDIDATE_LIFT_MICROWAVE_LGU.md`

Machine status:

`Current/Projektstatus_S1.42W_CANDIDATE.json`

Frozen plan / Patch Safety Review:

`BuildSpecs/S1.42W_PLAN.md`

Snapshot:

`ProfileSources/S1.42W/`

## Exact S1.42W tuning

S1.42W was built directly from S1.42U so the historical S1.42V Jetpack DLL is not stacked into the successor.

### Jetpack

Project-local plugin:

`Patches/S142WJetpackAcceleration/`

DLL SHA-256:

`95b7e689f68246ebda2fa6a0cab9fbe2ead206a00d85e6cbf64653d1f69d1fa8`

Behavior:

- exact `JetpackItem.Update()` local-player Prefix;
- ordered after ButteRyBalance;
- owner-written base acceleration `10f -> 16f`;
- only the proven approx-10f value is replaced;
- V49 handling/deceleration untouched;
- JetpackFixes collision/death/control logic untouched;
- no new RPC/network/save state;
- fail-closed version and Harmony-owner validation.

### LateGameUpgrades / More Ship Upgrades

Jet Fuel remains `20 / 20` because it is percentage-based and therefore automatically scales with the stronger 16f base:

- base 16.0;
- +20% = 19.2;
- +40% = 22.4;
- +60% = 25.6;
- +80% = 28.8.

Jetpack Thrusters:

- `Initial Maximum Speed Increase = 25`;
- `Incremental Maximum Speed Increase = 20`.

This modestly strengthens the independent speed ceiling as the stronger base acceleration reaches it sooner.

### Functional Microwave

`Functional Microwave | Volume = 0.15`

Microwave rarity remains deferred.

### Immortal Snail

- `Rarity = 40`;
- `Max Snails = 2`.

## Exact build delta vs S1.42U

Changed existing archive members only:

- `export.r2x`;
- `BepInEx/config/dev.idjut.SnailFork.cfg`;
- `BepInEx/config/CodeRebirth.cfg`;
- `BepInEx/config/com.malco.lethalcompany.moreshipupgrades.cfg`.

Added member only:

`BepInEx/plugins/S142WJetpackAcceleration/S142WJetpackAcceleration.dll`

No mod package state/add/remove changes occurred.

## Immediate next action

**Runtime-test S1.42W. Do not build a successor yet.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42W`

Import/run:

`LC V1 S1.42W Lift-Off Microwave Retune`

Use Gale `Advanced options -> Import all files` unless the import flow already guarantees all custom files are retained.

Required focus:

1. `S1.42W Jetpack Acceleration 1.0.0` loads and logs dependency/owner validation plus `armed`;
2. lift-off is clearly faster and subjectively acceptable;
3. V49 handling/inertia remains acceptable;
4. release/deactivation and safe landing remain sane;
5. hard collision/high-speed ground contact produce no new regression;
6. repeat flights show no state accumulation/random mid-air explosion;
7. Jet Fuel and Jetpack Thrusters remain useful purchase-gated progression;
8. Microwave works and `0.15` is acceptably quiet;
9. Snail works at `Rarity = 40`, `Max Snails = 2`;
10. BCMER 1.71.0, Compatibility Fixes 1.3.14 and normal enemies remain healthy;
11. Work/no-task = 0;
12. Leader-null = 0;
13. no new compatibility error flood;
14. ingest the complete fresh runtime log.

## Permanent compatibility state to preserve

- exact BCMER 1.71.0 enabled;
- EnemyIsolation off;
- Compatibility Fixes v1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- native inherited PikminEnemy death/unlatch/task lifecycle;
- Puffer -> Pikmin protection;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- accepted S1.42C-derived LethalLevelLoader moon spawn/power baseline;
- `Consistent Spawn Times = true`.

Never disable the whole `BaboonBirdPikminEnemy` merely to block Hawk -> Pikmin interaction.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Deferred scopes — do not mix into S1.42W

- equal probability for all installed interiors and same rule for future interiors;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- Functional Microwave rarity reduction;
- BCMER EventType equalization to 8 x 12.5%;
- final long S1.42 full-stack acceptance;
- AdditionalNetworking disconnect patch unless the issue becomes reproducible/user-facing.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42W_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = built S1.42W candidate;
- base SHA-256 = `f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`;
- no successor delta armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42W`

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local `current` wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains older historical comments that do not perfectly describe accepted v1.3.14 behavior.

Chronologically newer current documents, code/config and runtime evidence are authoritative. Keep cosmetic cleanup separate from gameplay/runtime tuning.
