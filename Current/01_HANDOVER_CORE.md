# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
2. `Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`
3. `Current/00_CURRENT_STATE.md`
4. `Current/Projektstatus_S1.42U.json`
5. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
6. `BuildSpecs/S1.42V_PLAN.md`
7. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
8. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
9. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
10. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
11. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
12. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`

Older S1.42T/S handover records remain historical/diagnostic evidence. Chronologically newer S1.42U acceptance files define the active state.

## Accepted current baseline

**S1.42U — BCMER 1.71.0 Reactivation Gate**

Profile:

`Profiles/LC V1 S1.42U BCMER 1.71.0 Reactivation Gate.r2z`

SHA-256:

`ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`

Runtime verdict:

**PASS — newest fully accepted full-normal-stack baseline and newest runtime-accepted technical descendant.**

Acceptance:

`Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Previous reference roles:

- S1.41 = previous accepted full-normal-stack historical baseline;
- S1.42T = accepted BCMER-off normal-enemy comparison baseline.

## S1.42U runtime summary

- exact BCMER 1.71.0 loads and completes patching;
- Compatibility Fixes 1.3.14 loads;
- EnemyIsolation disabled;
- normal enemy `ADDING ENEMY` count = 13;
- Work/no-task = 0;
- Leader-null = 0;
- project compatibility Error = 0;
- Fatal = 0;
- no old disconnect NoticeZone exception recurrence;
- no crash/freeze or gameplay-visible technical problem reported.

Direct runtime enemy power evidence:

- Aloe = 1;
- ImmortalSnail = 1;
- Janitor = 1.

## Permanent technical state

- BCMER exact 1.71.0: enabled;
- EnemyIsolation: off;
- compatibility plugin: v1.3.14;
- compatibility DLL SHA-256: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- Puffer -> Pikmin poison/effect protection preserved;
- BaboonBirdPikminEnemy remains enabled; native PikminEnemy death/unlatch lifecycle preserved.

## Moon/spawn verification

S1.42U `LethalLevelLoader.cfg` is byte-identical to S1.42C. All stored per-moon power-count overrides and enemy spawn lists are therefore restored exactly to the canonical baseline.

SpawnCycleFixes remains byte-identical to S1.42C with `Consistent Spawn Times = true`, preserving the standardized first wave around 7:39 AM including outside/daytime participation.

## Exact next planning stage

**S1.42V — Post-BCMER Balance Tuning**

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed**

Confirmed tuning:

- ImmortalSnail `Rarity = 80 -> 40`;
- CodeRebirth Functional Microwave current volume `0.7`, proposed `0.5`;
- modest Jetpack acceleration increase requested.

Jetpack implementation note:

- ButteRyBalance currently uses broad `Control Scheme = V49`; do not switch it merely to approximate acceleration;
- More Ship Upgrades `Jet Fuel` is the actual configurable acceleration upgrade (`20` initial / `20` incremental), but only after purchase;
- an always-on base acceleration buff requires an exact narrow implementation before S1.42V may be armed.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base = S1.42U.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

No successor profile is built or armed.

## Broader backlog — do not silently mix

- equal-interior probability tuning;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- BCMER fixed 12.5% x8 EventType distribution;
- CodeRebirth microwave rarity reduction.

## Patch policy

All future project-local patches require `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and a Patch Safety Review.
