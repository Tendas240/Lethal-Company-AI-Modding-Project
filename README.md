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

### S1.42V result

S1.42V's narrow Jetpack implementation path **passed runtime validation**, but the user rejected its balance magnitude: Jetpack `12f` still lifted too slowly and Microwave `0.5` remained too loud.

Evidence:

`RuntimeEvidence/S1.42V/20260904T095739Z/`

Raw log SHA-256:

`5e094086efef862abdbaf1bfdaab85fb8c8ed20d73d865c9f1bc902e08180dfd`

Canonical record:

`Current/82_S1.42V_RUNTIME_TECHNICAL_PASS_BALANCE_REJECTED.md`

The log proved the S1.42V Jetpack plugin loaded, validated ButteRyBalance 0.7.0 / JetpackFixes 1.6.3 / More Ship Upgrades 3.14.1 and armed successfully. Work/no-task and Leader-null remained zero and no S1.39 Compatibility Fixes error occurred.

One AdditionalNetworking `NetworkObjectReference` Fatal occurred during local-disconnect teardown after BCMER `OnLocalDisconnect`. It is monitor-only unless it becomes reproducible outside disconnect or user-facing.

### Newest built candidate

**S1.42W — Lift-Off Microwave Retune**

`Profiles/LC V1 S1.42W Lift-Off Microwave Retune.r2z`

SHA-256:

`f34ebcf18bd2b475da5546e6c391bd15bf70df5648b5f69ffb668d196df057dc`

Status:

**BUILD PASS / RUNTIME VALIDATION REQUIRED / NOT ACCEPTED**

Candidate record:

`Current/83_S1.42W_BUILD_CANDIDATE_LIFT_MICROWAVE_LGU.md`

Machine status:

`Current/Projektstatus_S1.42W_CANDIDATE.json`

Frozen plan / Patch Safety Review:

`BuildSpecs/S1.42W_PLAN.md`

Build commit:

`165d102364438cace2fd2184af3fd091855ff0d7`

GitHub Actions run:

`33861561173` = **success**

S1.42W was built directly from S1.42U, not from S1.42V, so the superseded S1.42V Jetpack DLL is not stacked into the new candidate.

## S1.42W exact tuning

### Jetpack base acceleration

Project source:

`Patches/S142WJetpackAcceleration/`

Injected DLL SHA-256:

`95b7e689f68246ebda2fa6a0cab9fbe2ead206a00d85e6cbf64653d1f69d1fa8`

Behavior:

- exact `JetpackItem.Update()` local-player Prefix;
- ordered after ButteRyBalance;
- ButteRyBalance owner-written base `10f -> 16f`;
- only the proven approx-10f baseline is replaced;
- V49 inertia/handling and deceleration remain untouched;
- JetpackFixes collision/death/control logic remains untouched;
- fail-closed dependency/version/Harmony-owner validation.

### LateGameUpgrades / More Ship Upgrades

Jet Fuel remains:

- `Initial Acceleration Increase = 20`;
- `Incremental Acceleration Increase = 20`.

This is intentional: Jet Fuel is percentage-based and automatically scales with the stronger 16f base. Its 20/40/60/80% effects produce approximately 19.2 / 22.4 / 25.6 / 28.8 acceleration.

Jetpack Thrusters:

- `Initial Maximum Speed Increase = 25`;
- `Incremental Maximum Speed Increase = 20`.

The slightly stronger first Thrusters tier keeps the independent speed-cap upgrade relevant as the stronger base acceleration reaches that ceiling sooner.

### Functional Microwave

`Functional Microwave | Volume = 0.15`

Microwave spawn rarity remains deferred.

### Immortal Snail

- `Rarity = 40`;
- `Max Snails = 2`.

## Exact S1.42W archive delta vs S1.42U

Changed existing members only:

- `export.r2x`;
- `BepInEx/config/dev.idjut.SnailFork.cfg`;
- `BepInEx/config/CodeRebirth.cfg`;
- `BepInEx/config/com.malco.lethalcompany.moreshipupgrades.cfg`.

Added member only:

`BepInEx/plugins/S142WJetpackAcceleration/S142WJetpackAcceleration.dll`

No mod package state/add/remove changes occurred.

## Exact next action

**Runtime-test S1.42W. Do not build a successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42W`

Import/run:

`LC V1 S1.42W Lift-Off Microwave Retune`

Because the candidate contains a project-local DLL, use Gale:

**Advanced options -> Import all files**

unless your concrete import path already guarantees all custom files are retained.

The runtime log must contain:

- `Loading [S1.42W Jetpack Acceleration 1.0.0]`;
- successful dependency/owner validation;
- `S1.42W Jetpack acceleration patch armed`;
- `Loading [S1.39 Compatibility Fixes 1.3.14]`.

Gameplay focus:

- clearly faster lift-off than S1.42V;
- acceptable V49 handling/inertia;
- sane release/deactivation and safe landing;
- no new hard-collision/high-speed-ground regression;
- repeated flights without state accumulation/random mid-air explosion;
- Jet Fuel and Jetpack Thrusters remain worthwhile;
- Microwave remains functional and `0.15` is quiet enough;
- Snail remains functional at rarity 40 / max 2;
- normal enemies and BCMER remain healthy;
- Work/no-task = 0;
- Leader-null = 0;
- no new Compatibility Fixes error flood;
- ingest the complete fresh log.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/83_S1.42W_BUILD_CANDIDATE_LIFT_MICROWAVE_LGU.md`
4. `Current/Projektstatus_S1.42W_CANDIDATE.json`
5. `BuildSpecs/S1.42W_PLAN.md`
6. `Current/82_S1.42V_RUNTIME_TECHNICAL_PASS_BALANCE_REJECTED.md`
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

## Deferred after S1.42W

Do not mix into the active W gate:

- equal interior probability and same rule for future interiors;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave rarity reduction;
- BCMER EventType equalization to 8 x 12.5%;
- final long S1.42 full-stack acceptance;
- AdditionalNetworking disconnect patch without reproducible/user-facing evidence.

## Runtime-log infrastructure

Normal logs use `RuntimeInbox/Current/` and the streaming analyzer. Very large logs follow `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`.

## Known non-functional drift

Older chronology sections in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` may contain stale local wording. Current code/config/runtime evidence and chronologically newer canonical documents are authoritative.

## Repository-first rule

Do not ask for a local repository clone or manual profile rebuild when the necessary profiles, build system and GitHub Actions infrastructure exist here.
