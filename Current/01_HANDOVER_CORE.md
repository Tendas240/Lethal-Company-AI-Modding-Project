# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`
2. `Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`
3. `Current/78_S1.42U_RUNTIME_ACCEPTANCE_BCMER_REACTIVATION.md`
4. `Current/77_S1.42U_BUILD_VERIFICATION_BCMER_REACTIVATION.md`
5. `Current/00_CURRENT_STATE.md`
6. `Current/Projektstatus_S1.42U.json`
7. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
8. `BuildSpecs/S1.42V_PLAN.md`
9. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
10. `Current/73_S1.42T_RUNTIME_ACCEPTANCE_NORMAL_ENEMY_RESTORE.md`
11. `Current/69_S1.42S_RUNTIME_ACCEPTANCE_BABOON_PIKMIN_LIFECYCLE.md`
12. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
13. `Current/66_S1.42R_RUNTIME_BABOON_ADAPTER_LIFECYCLE_ROOT_CAUSE.md`
14. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
15. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
16. `BuildSpecs/current.json`
17. `RuntimeInbox/ACTIVE_BUILD.txt`

Older S1.42T/S handover records remain historical/diagnostic evidence. Chronologically newer S1.42U acceptance, final-handover and audit files define the active state.

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

Final handover:

`Current/79_FINAL_HANDOVER_S1.42U_PASS_S1.42V_NEXT.md`

Repository audit:

`Current/80_REPOSITORY_HANDOVER_AUDIT_S1.42U.md`

Evidence:

`RuntimeEvidence/S1.42U/20260904T082412Z/`

Raw log SHA-256:

`0a2e0839b106a7d6f9867d186a835252bc72a869ef63a62517ae1971fd93c5fc`

Raw log size / line count:

- `1,959,356 bytes`;
- `19,939` lines.

GitHub Actions build run:

`33818241873` = **success**

Build commit:

`29e7b36c3d09ff37551894438744d67089d7aba4`

There is **no newer built candidate**. S1.42V is plan-only.

Previous reference roles:

- S1.41 = previous accepted full-normal-stack historical baseline, SHA-256 `d69d0b59144002c24cfedf041ca5cbb70086e9218692aa3ac9359170f338cb2b`;
- S1.42T = accepted BCMER-off normal-enemy comparison baseline, SHA-256 `a2714d04777edc95490398367c9dad2e320b44b664e20e9fe0b0f85d6a5fea10`.

## S1.42U runtime summary

- exact BCMER 1.71.0 loads and completes patching;
- Compatibility Fixes 1.3.14 loads;
- EnemyIsolation disabled;
- normal enemy `ADDING ENEMY` count = 13;
- Work/no-task = 0;
- Leader-null = 0;
- project compatibility Error = 0;
- Fatal = 0;
- old disconnect NoticeZone exception did not recur;
- no crash/freeze or gameplay-visible technical problem reported.

Direct runtime enemy power evidence:

- Aloe = 1;
- ImmortalSnail = 1;
- Janitor = 1;
- Crawler = 3;
- Bunker Spider = 2.

## Permanent technical state

- BCMER exact 1.71.0: enabled;
- EnemyIsolation: off;
- compatibility plugin: v1.3.14;
- compatibility DLL SHA-256: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`;
- `Thumper Bite Limit = 3`;
- Crawler absent from Attack Blacklist;
- Puffer -> Pikmin poison/effect protection preserved;
- `BaboonBirdPikminEnemy` remains enabled;
- native inherited PikminEnemy death/unlatch/task lifecycle preserved;
- normal enemy population restored.

Never repeat the S1.42R approach of disabling the whole `BaboonBirdPikminEnemy` adapter to block one interaction.

## Moon/spawn verification

S1.42U `LethalLevelLoader.cfg` is byte-identical to S1.42C, Git blob SHA `14dcd076692cbc54e073ad281a63d046b0976e00`. All stored per-moon power-count overrides and enemy spawn lists are therefore exactly on the canonical restore baseline.

SpawnCycleFixes remains byte-identical to S1.42C with `Consistent Spawn Times = true`, preserving the standardized first wave around 07:39 including outside/daytime participation.

Do not treat these as still-broken systems unless new evidence shows a regression.

## Exact next planning stage

**S1.42V — Post-BCMER Balance Tuning**

Plan:

`BuildSpecs/S1.42V_PLAN.md`

Status:

**plan-only / not armed / no successor profile built.**

Confirmed/requested tuning:

- ImmortalSnail `Rarity = 80 -> 40`, keep `Max Snails = 2`;
- CodeRebirth Functional Microwave current volume `0.7`, proposed next value `0.5`;
- modest **always-on base Jetpack acceleration increase** requested.

### Exact next technical action

Do not arm S1.42V until the Jetpack implementation is frozen.

The new chat should first:

1. identify the exact runtime owner/method/field for the always-on Jetpack acceleration change;
2. preserve ButteRyBalance `Control Scheme = V49` unless exact evidence justifies changing it;
3. account for JetpackFixes interaction;
4. not substitute More Ship Upgrades `Jet Fuel` by default — its current `20` initial / `20` incremental acceleration only applies after purchase;
5. perform a Patch Safety Review if project-local code is required;
6. freeze the final S1.42V delta, then arm/build through GitHub Actions.

## Planned stages after S1.42V

Later build IDs are deliberately not assigned yet.

### Environment / Interior tuning

- equal probability for all installed interiors and the same rule for newly added interiors;
- CullFactory exceptions for `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction;
- CodeRebirth Microwave rarity reduction.

### BCMER EventType balancing

- fixed equal distribution: **8 x 12.5% EventTypes**.

### Final S1.42 full-stack acceptance

- longer normal full-stack gameplay run after individual tuning gates pass;
- exercise varied enemies, Pikmin lifecycle, BCMER events, interiors, Jetpack and CodeRebirth systems;
- ingest full log and re-check permanent counters/invariants;
- promote only if clean.

Do not reopen isolated-enemy diagnostics or heavy Baboon-Hawk stress unless a later change touches that path or new evidence reopens the issue.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42U_RUNTIME_PASS_AWAITING_S1.42V_TUNING`;
- base = S1.42U;
- base SHA-256 = `ff5fdebf22fefdd5515b95677174290f9666e491447138f074e5b65673173969`;
- no changes armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42U`

## Monitor-only observations

1. Historical S1.42S disconnect-only LethalMin NoticeZone `NetworkObjectReference` exception; absent in S1.42U.
2. Historical S1.42T one-off `AloeChase` FSB load-state message; no user-facing regression established.
3. Known setup SoundAPI/HarmonyX and SoftMaskKiller-handled exception classes remain non-blocking unless behavior changes, they flood, or become user-facing.

## Known non-functional drift

- `Current/02_TECHNICAL_BASELINE.md` contains older chronology subsections with stale local `current` wording.
- `Patches/S139CompatibilityFixes/Plugin.cs` contains historical comments that do not perfectly describe accepted v1.3.14 behavior.

Do not mix cosmetic cleanup with risky gameplay/runtime changes.

## Patch policy

All future project-local patches require `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and a Patch Safety Review.

## Local work

No local repository clone or local build is required. The accepted base and GitHub-native build infrastructure are already in the repository.
