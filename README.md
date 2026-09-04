# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current status

Game: **Lethal Company V81**

### Last accepted full-normal-stack baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Final handover:

`Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`

Repository handover audit:

`Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Runtime verdict:

**PASS — exact BCMER 1.71.0 restored, normal enemy stack retained, no critical compatibility regression or gameplay-visible technical problem.**

S1.42U remains the canonical accepted baseline until S1.42V passes fresh runtime validation.

### Newest built candidate

**S1.42V — Post-BCMER Balance Tuning**

`Profiles/LC V1 S1.42V Post-BCMER Balance Tuning.r2z`

SHA-256:

`06390fc2faaf5ef30918efb077a1728c75864777c79a084855ed4dc3e69b3f0d`

Status:

**BUILD PASS / RUNTIME VALIDATION REQUIRED / NOT ACCEPTED**

Candidate record:

`Current/81_S1.42V_BUILD_CANDIDATE_JETPACK_SNAIL_MICROWAVE.md`

Machine status:

`Current/Projektstatus_S1.42V_CANDIDATE.json`

Frozen plan / Patch Safety Review:

`BuildSpecs/S1.42V_PLAN.md`

Automated build result:

`Current/AUTO_BUILD_RESULT.json`

GitHub Actions run:

`33859188647` = **success**

Build commit:

`1f5dd23eeb5b23d565af624fd97b78dcea58b784`

The automated builder verified exactly three changed existing archive members (`export.r2x`, Immortal Snail config, CodeRebirth config) and one added project-local Jetpack DLL. No mod package state/add/remove change occurred.

## S1.42V exact scope

### Immortal Snail

- `Rarity = 80 -> 40`;
- `Max Snails = 2` preserved.

### Functional Microwave

- `Functional Microwave | Volume = 0.7 -> 0.5`;
- Microwave spawn rarity remains deferred.

### Always-on base Jetpack acceleration

Project source:

`Patches/S142VJetpackAcceleration/`

Injected DLL:

`BepInEx/plugins/S142VJetpackAcceleration/S142VJetpackAcceleration.dll`

DLL SHA-256:

`084fe47b5e47d3637fbb6d4fdd735429a37934993fc190fb4b6abbc51eada00c`

Frozen behavior:

- exact `JetpackItem.Update()` local-player prefix;
- ordered after ButteRyBalance;
- proven ButteRyBalance base `jetpackAcceleration = 10f -> 12f` (+20%);
- only an approximately-10f value is replaced;
- fail-closed dependency/version/Harmony-owner validation;
- no fallback target, original-method skip, or extra IL transpiler.

Preserved:

- ButteRyBalance `0.7.0`;
- `Control Scheme = V49`;
- `Warmup Period = false`;
- V49 inertia/handling and deceleration;
- Jetpack maximum-speed/power layer;
- battery and price;
- JetpackFixes `1.6.3` and `MidAirExplosions = Off`;
- More Ship Upgrades `3.14.1` Jet Fuel `20` initial / `20` incremental purchase-gated layer;
- More Ship Upgrades Jetpack Thrusters maximum-speed layer.

## Exact next action

**Runtime-test S1.42V. Do not build a successor yet.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42V`

Import/run:

`LC V1 S1.42V Post-BCMER Balance Tuning`

Because the profile contains project-local DLLs under `BepInEx/plugins/`, import it in Gale with:

**Advanced options -> Import all files**

unless the concrete Gale import flow already guarantees all custom files are retained.

The runtime gate is invalid if either project-local plugin load path is missing. The log must include the established Compatibility Fixes marker and the new S1.42V Jetpack plugin/armed markers before Jetpack behavior can count as tested.

Minimum focus:

- startup/main menu;
- exact dependency/Harmony-owner validation for the Jetpack patch;
- no Harmony target/transpiler/ordering exception;
- BCMER 1.71.0 and Compatibility Fixes 1.3.14 still healthy;
- normal enemies still spawn;
- Jetpack accelerates modestly faster without changing V49 handling or maximum-speed behavior;
- takeoff, release/deactivation, safe landing, hard collision, high-speed ground touch and repeated flights remain sane;
- no random mid-air explosion/state accumulation;
- Immortal Snail works at `Rarity = 40`, `Max Snails = 2`;
- Functional Microwave works and is audibly lower at `Volume = 0.5`;
- if practical, Jet Fuel still layers as a separate percentage upgrade;
- Work/no-task = 0;
- Leader-null = 0;
- no new compatibility exception flood;
- commit/ingest a fresh complete runtime log.

## Restored moon/spawn state

S1.42U `LethalLevelLoader.cfg` is byte-identical to the canonical S1.42C restore baseline, Git blob SHA:

`14dcd076692cbc54e073ad281a63d046b0976e00`

S1.42V did not change this archive member, so the accepted per-moon inside/daytime/nighttime power counts and enemy spawn lists remain byte-identical in the candidate.

SpawnCycleFixes remains on:

`Consistent Spawn Times = true`

S1.42V did not change that member either.

These are verified restore invariants, not current repair tasks.

## Planned stages after S1.42V passes

Later build IDs are intentionally not assigned yet.

### Environment / Interior tuning

- equal probability for all installed interiors and the same rule for newly added interiors;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

### BCMER EventType balancing

- fixed equal distribution: **8 EventTypes x 12.5%**.

### Final S1.42 full-stack acceptance

After individual tuning stages pass, perform a longer normal run covering varied enemies, Pikmin lifecycle, BCMER events, interiors, Jetpack and CodeRebirth systems; ingest the complete log and promote only if the full stack remains clean.

Do not silently mix these later stages into S1.42V.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/81_S1.42V_BUILD_CANDIDATE_JETPACK_SNAIL_MICROWAVE.md`
3. `Current/00_CURRENT_STATE.md`
4. `Current/01_HANDOVER_CORE.md`
5. `Current/Projektstatus_S1.42V_CANDIDATE.json`
6. `BuildSpecs/S1.42V_PLAN.md`
7. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
8. `Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`
9. `Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`
10. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
11. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
12. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
13. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
14. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
15. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
16. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
17. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
18. `BuildSpecs/current.json`
19. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific handovers and historical local `current` wording.

## Permanent anti-regression state

- exact BCMER 1.71.0 stays enabled unless a controlled diagnostic gate explicitly says otherwise;
- Compatibility Fixes v1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- EnemyIsolation off;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- Puffer -> Pikmin protection;
- never disable complete `LethalMin.BaboonBirdPikminEnemy` merely to block Hawk -> Pikmin interaction; preserve native inherited death/unlatch/task lifecycle.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Gale import / project-local DLL guard

For S1.42V, Gale must retain both project-local DLL paths contained by the exported profile. Use:

**Advanced options -> Import all files**

unless the concrete import flow is independently verified to preserve all custom files.

Expected runtime markers include:

`Loading [S1.39 Compatibility Fixes 1.3.14]`

and the S1.42V Jetpack plugin's load/validation/`armed` messages.

If those markers are absent, fix the import/runtime load path before drawing conclusions about the corresponding patch behavior.

## Runtime-log infrastructure

Normal logs use `RuntimeInbox/Current/` and streaming every-line analysis.

Very large logs use the disposable `runtime-large` branch and `RuntimeInbox/Large/`, compact analysis/provenance on `main`, a temporary raw Actions artifact, and query-on-demand extraction through `RuntimeAnalysis/QUERY.json`.

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

## Known non-functional drift

`Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local `current` wording, and `Patches/S139CompatibilityFixes/Plugin.cs` contains historical comments that do not perfectly describe accepted v1.3.14 behavior. Current code/config/runtime evidence plus chronologically newer canonical docs are authoritative. Cleanup remains separate maintenance and should not be mixed into risky runtime patch changes.

## Repository-first rule

Do not ask the user for a local clone/build when the required profile, snapshots, build system and GitHub Actions workflow already exist in this repository.
