# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current status

Game: **Lethal Company V81**

### Current accepted full-normal-stack baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Build verification:

`Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`

Runtime acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Runtime verdict:

**PASS — exact BCMER 1.71.0 restored, normal enemy stack retained, no critical compatibility regression or gameplay-visible technical problem.**

S1.42U is now both the newest runtime-accepted technical descendant and the newest fully accepted full-normal-stack gameplay baseline.

S1.41 remains historical as the previous full-normal-stack baseline. S1.42T remains the clean accepted BCMER-off comparison point from the restoration chain.

## S1.42U runtime highlights

- BCMER `1.71.0` loads and reports that patching completed;
- S1.39 Compatibility Fixes `1.3.14` loads;
- EnemyIsolation is disabled;
- `ADDING ENEMY` = 13;
- Work/no-task = 0;
- Leader-null = 0;
- S1.39 Compatibility Fixes Error = 0;
- Fatal = 0;
- no crash/freeze;
- old disconnect-only Pikmin NoticeZone exception did not recur.

## Restored moon/spawn state

S1.42U `LethalLevelLoader.cfg` is byte-identical to the canonical S1.42C restore baseline. This preserves all configured per-moon inside/daytime/nighttime power counts and enemy spawning lists.

SpawnCycleFixes also remains byte-identical to S1.42C and keeps:

`Consistent Spawn Times = true`

The intended standardized first spawn wave at approximately 7:39 AM is therefore preserved, including outside/daytime enemy participation rather than the possible vanilla delay while vents are occupied.

## Next planned stage

**S1.42V — Post-BCMER Balance Tuning**

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed**

Confirmed/requested items:

- ImmortalSnail spawn rarity/weight `80 -> 40`;
- CodeRebirth Functional Microwave volume is currently `0.7`; proposed next value `0.5`;
- modest Jetpack acceleration increase requested, exact narrow implementation still to be frozen.

Jetpack note: ButteRyBalance's current `Control Scheme = V49` is a broad handling/inertia mode, not a small numeric acceleration knob. More Ship Upgrades' `Jet Fuel` is an actual acceleration upgrade, currently `20` initial / `20` incremental, but only affects purchased upgrade tiers. Do not fake an always-on base acceleration change through the wrong owner.

No successor build is armed.

## ChatGPT — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
3. `Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`
4. `Current/00_CURRENT_STATE.md`
5. `Current/01_HANDOVER_CORE.md`
6. `Current/Projektstatus_S1.42U.json`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `BuildSpecs/S1.42V_PLAN.md`
9. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
10. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
11. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
12. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
13. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
14. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
15. `BuildSpecs/current.json`
16. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific handovers.

## Permanent anti-regression state

- exact BCMER 1.71.0 stays enabled unless a controlled diagnostic gate explicitly says otherwise;
- compatibility plugin v1.3.14 / DLL SHA-256 `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- EnemyIsolation off;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- Puffer -> Pikmin protection;
- never disable complete `LethalMin.BaboonBirdPikminEnemy` merely to block Hawk -> Pikmin interaction; preserve native inherited death/unlatch lifecycle.

Patch policy:

`Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Runtime-log infrastructure

Normal logs use `RuntimeInbox/Current/` and streaming every-line analysis.

Very large logs use the disposable `runtime-large` branch and `RuntimeInbox/Large/`, compact analysis/provenance on `main`, a temporary raw Actions artifact, and query-on-demand extraction through `RuntimeAnalysis/QUERY.json`.

Canonical policy:

`Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

## Known non-functional drift

`Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local "current" wording, and `Patches/S139CompatibilityFixes/Plugin.cs` contains historical comments that do not perfectly describe accepted v1.3.14 behavior. Current code/config/runtime evidence plus chronologically newer canonical docs are authoritative. Cleanup remains separate maintenance.

## Repository-first rule

Do not ask the user for a local clone/build when the required profile, snapshots, build system, and GitHub Actions workflow already exist in this repository.
