# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth.

## Read first

1. `Current/94_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AA_RUNTIME_NEXT.md`
2. `Current/95_REPOSITORY_HANDOVER_AUDIT_S1.42AA.md`
3. `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`
4. `Current/Projektstatus_S1.42AA_CANDIDATE.json`
5. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
6. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
7. `Current/00_CURRENT_STATE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `Current/06_RECENT_WORK_S1.42AA.md`
10. `BuildSpecs/S1.42AA_PLAN.md`
11. `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`
12. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
13. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
14. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
15. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
16. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
17. `BuildSpecs/current.json`
18. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific wording. `Current/94`, `Current/95`, `Current/91` and `Projektstatus_S1.42AA_CANDIDATE.json` are authoritative for the active test gate. `Current/90` and `Projektstatus_S1.42Z_ACCEPTED.json` remain authoritative for the accepted rollback baseline.

## Accepted rollback baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`

Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z stays accepted until S1.42AA passes its own fresh runtime gate.

## Active candidate — S1.42AA

**S1.42AA — Interior Weight Equalization**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
Gale profile name: `LC V1 S1.42AA Interior Weight Equalization`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Status: **BUILD PASS / PROFILE IMPORT CONFIRMED / RUNTIME VALIDATION OPEN / NOT ACCEPTED**

Build run: `33884101262` — success  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`

The user has already imported S1.42AA in Gale using **Advanced options -> Import all files**. No S1.42AA gameplay runtime test has been completed yet.

## Exact S1.42AA scope

S1.42Z already carries normalized LethalLevelLoader configured tag weights `Vanilla:100,Custom:100`. The remaining effective inequality is caused by LethalLevelLoader re-injecting mod-author Level/Dungeon MatchingProperties while:

`Inject Dynamic Matching Weights = true`

S1.42AA changes that single functional key to:

`Inject Dynamic Matching Weights = false`

Automated archive delta vs accepted S1.42Z:

- ZIP members `333`;
- changed existing members exactly `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`;
- added members `0`;
- removed members `0`;
- mod state/add/remove changes `0`;
- no project-local DLL changed.

Black Mesa remains on its dedicated native-owner config with equal `+100/+100` vanilla/custom weights. Do not create a duplicate LLL owner path.

Permanent rule: every eligible installed interior should have the same effective selection weight on vanilla and custom moons. Future interiors must be normalized into the same model before acceptance unless a documented technical incompatibility requires an exception.

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

Never repeat the S1.42R whole-component disable approach.

## Exact next action

**Runtime-test S1.42AA on Offense. Do not build another successor first.**

Because the profile is already imported, do not require another replacement/re-import unless the user intentionally wants to reinstall it.

Do one normal Offense gameplay run, enter the generated interior and then upload the complete fresh `LogOutput.log`. The runtime log must show eligible `Viable ExtendedDungeonFlows` normalized to common effective weight `100` instead of S1.42Z's unequal author weights, while normal dungeon generation and accepted gameplay remain healthy.

The exact corrected S1.42AA PowerShell uploader is in:

`Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`

Required regression checks include Work/no-task `0`, Leader-null `0`, Fatal `0`, no new project-local exception class, no duplicate Black Mesa/native-owner regression and no dungeon-generation failure.

## Gale active-profile replacement workflow — permanent

Canonical implementation:

`RuntimeTools/ReplaceActiveGaleProfile.ps1`

Canonical contract:

`Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`

The final y/n helper was validated under Windows PowerShell 5.1 using a disposable `testpowershell` profile and was also used successfully in the S1.42AA import flow.

Canonical launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

For every future new build whose next step is runtime testing, ChatGPT must include both this profile-replacement launcher and the exact build-specific runtime-log uploader in the same response without waiting for the user to ask.

Do not reintroduce the failed helper patterns: case-sensitive `LOESCHEN`, fuzzy build/profile matching, Windows PowerShell 5.1 array assumptions, or a normal variable named `$matches` that collides with automatic `$Matches`.

## Deferred — do not mix into AA

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn rarity reduction;
- BCMER EventTypes `8 × 12.5%`;
- final long full-stack acceptance;
- monitor-only AdditionalNetworking / LethalMin teardown repairs;
- cosmetic documentation cleanup.

## Controllers

`BuildSpecs/current.json`:

- `enabled = false`;
- `build_id = IDLE_AFTER_S1.42AA_BUILD_AWAITING_RUNTIME_VALIDATION`;
- base = S1.42AA candidate;
- base SHA-256 = `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`;
- no successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`

`RuntimeInbox/Current/` contains only `.gitkeep`; no S1.42AA runtime log exists yet.

## Monitor-only / known drift

Do not patch known setup/teardown error classes without stronger reproducibility or user-facing impact. Older chronology wording in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` remain non-functional documentation/comment drift; newer canonical docs, code/config and runtime evidence override them.
