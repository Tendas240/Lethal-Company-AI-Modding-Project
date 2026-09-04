# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`
2. `Current/Projektstatus_S1.42AA_CANDIDATE.json`
3. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
4. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
5. `Current/00_CURRENT_STATE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `BuildSpecs/S1.42AA_PLAN.md`
8. `Current/06_RECENT_WORK_S1.42N-S1.42Z.md`
9. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
10. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
11. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
12. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
13. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
14. `BuildSpecs/current.json`
15. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific wording. `Current/91` and `Projektstatus_S1.42AA_CANDIDATE.json` are authoritative for the active test candidate; `Current/90` and `Projektstatus_S1.42Z_ACCEPTED.json` remain authoritative for the accepted rollback baseline.

## Accepted rollback baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED**

Profile:

`Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`

SHA-256:

`a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance:

`Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence:

`RuntimeEvidence/S1.42Z/20260904T135820Z/`

S1.42Z stays accepted until S1.42AA passes its own fresh runtime gate.

## Active candidate — S1.42AA

**S1.42AA — Interior Weight Equalization**

Profile:

`Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`

Gale profile name:

`LC V1 S1.42AA Interior Weight Equalization`

SHA-256:

`0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Status:

**BUILD PASS / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Build run:

`33884101262` — success

Automated build commit:

`4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`

## Exact S1.42AA scope

S1.42Z already carries normalized LethalLevelLoader configured tag weights `Vanilla:100,Custom:100`. The remaining effective inequality is caused by LethalLevelLoader re-injecting mod-author Level/Dungeon MatchingProperties on every landing while:

`Inject Dynamic Matching Weights = true`

S1.42AA changes that single functional key to:

`Inject Dynamic Matching Weights = false`

Automated archive delta vs accepted S1.42Z:

- ZIP members `333`;
- changed existing members exactly `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`;
- added members `0`;
- mod state/add/remove changes `0`.

No package or project-local DLL changed. Therefore accepted S1.42Z Jetpack, LethalMin, CodeRebirth aerial-defense, BCMER and compatibility state is retained byte-for-byte outside the LLL config and profile-name metadata.

Black Mesa remains on its dedicated native-owner config with equal `+100/+100` vanilla/custom weights. Do not create a duplicate LLL owner path.

The permanent rule is equal effective selection weight for every eligible installed interior on vanilla and custom moons. Future interiors must be normalized into the same model before acceptance unless a documented technical incompatibility requires an exception.

Shatteredrooms' Experimentation/Embrion restriction remains a technical compatibility guard pending dedicated evidence that removal is safe.

## Accepted S1.42Z state that must survive AA

- Jetpack base acceleration `18f`;
- Jet Fuel `18 / 18`;
- Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- CarryStrength non-Purple `3`, Purple `30`;
- ACU exact 18 curves ×`0.5`;
- G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail Rarity `40`, Max `2`;
- exact BCMER `1.71.0`;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
- Baboon Hawk/Pikmin narrow-interaction architecture and inherited lifecycle;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from Attack Blacklist;
- S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`.

## Exact next action

**Runtime-test S1.42AA. Do not build another successor first.**

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`

Import through Gale with:

**Advanced options -> Import all files**

Preferred direct before/after moon: **Offense**.

Do one normal Offense gameplay run, enter the generated interior, then upload the complete fresh log. The runtime log must show the eligible `Viable ExtendedDungeonFlows` normalized to common weight `100` instead of S1.42Z's unequal author weights, while normal dungeon generation and accepted gameplay remain healthy.

The exact candidate-specific corrected PowerShell uploader is in:

`Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`

## Deferred — do not mix into AA

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes `8 × 12.5%`;
- final long full-stack acceptance;
- monitor-only AdditionalNetworking / LethalMin teardown repairs;
- cosmetic documentation cleanup.

The local Gale replace-profile PowerShell helper remains pending user verification and is not yet canonical.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AA_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42AA candidate;
- base SHA-256 = `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`;
- no successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`

## Monitor-only / known drift

Do not patch known setup/teardown error classes without stronger reproducibility or user-facing impact. Older chronology wording in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` remain non-functional documentation drift; newer canonical docs, code/config and runtime evidence override them.
