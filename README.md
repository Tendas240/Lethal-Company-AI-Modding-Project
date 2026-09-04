# Lethal Company AI Modding Project

GitHub is the canonical source of truth for this project.

## Current canonical state

Game: **Lethal Company V81**

### Accepted full-normal-stack baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Canonical runtime acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Machine-readable accepted state: `Current/Projektstatus_S1.42Z_ACCEPTED.json`

Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z remains the accepted rollback baseline until S1.42AA passes fresh runtime validation.

### Active runtime candidate

**S1.42AA — Interior Weight Equalization — BUILD PASS / PROFILE IMPORT CONFIRMED / RUNTIME OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
Gale profile name: `LC V1 S1.42AA Interior Weight Equalization`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`

Build workflow run: `33884101262` — success  
Automated build commit: `4d5e5e6c86a0bc8ab10e0adc32ab22ae6f5c0156`

Candidate record: `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`  
Machine-readable candidate state: `Current/Projektstatus_S1.42AA_CANDIDATE.json`

The user has already imported S1.42AA in Gale with **Advanced options -> Import all files**. No S1.42AA gameplay runtime test has been completed yet.

## Latest handover — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/94_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AA_RUNTIME_NEXT.md`
3. `Current/95_REPOSITORY_HANDOVER_AUDIT_S1.42AA.md`
4. `Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`
5. `Current/Projektstatus_S1.42AA_CANDIDATE.json`
6. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
7. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
8. `Current/00_CURRENT_STATE.md`
9. `Current/01_HANDOVER_CORE.md`
10. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
11. `Current/06_RECENT_WORK_S1.42AA.md`
12. `BuildSpecs/S1.42AA_PLAN.md`
13. `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`
14. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
15. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
16. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
17. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
18. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
19. `BuildSpecs/current.json`
20. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed information overrides older version-specific wording. `Current/94`, `Current/95`, `Current/91` and `Projektstatus_S1.42AA_CANDIDATE.json` are authoritative for the active runtime gate. `Current/90` and `Projektstatus_S1.42Z_ACCEPTED.json` remain authoritative for the accepted baseline.

## Why S1.42AA exists

S1.42Z already contained project-normalized LethalLevelLoader dungeon tag weights:

`Vanilla:100,Custom:100`

but still had:

`Inject Dynamic Matching Weights = true`

which caused mod-author Level/Dungeon MatchingProperties to be injected again on each landing. S1.42Z Offense runtime evidence therefore still showed unequal effective interior weights such as `300`, `275`, `250`, `75`, `70`, `50`, `35`, `25` and `20`.

S1.42AA makes one functional change:

`Inject Dynamic Matching Weights = false`

Automated build verification shows exactly two changed archive members vs S1.42Z:

- `BepInEx/config/LethalLevelLoader.cfg`;
- `export.r2x` profile-name metadata.

ZIP members remain `333`; added members = `0`; removed members = `0`; mod state/add/remove changes = `0`; no package or project-local DLL changed.

Black Mesa remains on its dedicated native-owner path with `lethal_company:vanilla=+100,lethal_company:custom=+100`. Shatteredrooms' Experimentation/Embrion restriction remains a technical compatibility guard pending dedicated proof that removing it is safe.

Permanent interior rule: every eligible installed interior should have the same effective selection weight on vanilla and custom moons. Future added interiors must be normalized into the same architecture before acceptance unless an explicitly documented technical incompatibility requires an exception.

## S1.42Z accepted runtime evidence

S1.42Z technical acceptance confirmed:

- Jetpack `10 -> 18`;
- CodeRebirth ACU exact 18 curves ×`0.5`;
- CodeRebirth G.R.E.G. exact 18 curves ×`0.5`;
- Work/no-task `0`;
- Leader-null `0`;
- Compatibility Fixes Error `0`;
- relevant NetworkObjectReference/PikminNoticeZone regression markers `0`;
- project-local Error-severity `0`;
- Fatal `0`;
- user acceptance of the resulting runtime behavior.

## Accepted tuning preserved in S1.42AA

- Jetpack base acceleration `10 -> 18`;
- Jet Fuel `18 / 18`;
- Jetpack Thrusters `25 / 20`;
- Indoor Pikmin Spawn Chance `0.09`;
- non-Purple CarryStrength `3`;
- Purple CarryStrength `30`;
- CodeRebirth Air Control Unit 18 exact curves ×`0.5`;
- CodeRebirth G.R.E.G. 18 exact curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail `Rarity = 40`, `Max Snails = 2`.

Project-local DLL SHA-256 values:

- Jetpack: `9624de844ab3913605eab2c35d96d9d9dec17b34d77823b33aaa434488022add`;
- aerial defense: `7313501540c3945ee3782903b8bb328574a87587859fce30faa2a301b7f1d98b`;
- Compatibility Fixes: `3fd38c0e8ff76b55c5c335cd9eb867e254a422caea2287fb95d46447e2167960`.

## Permanent anti-regression state

Preserve:

- exact BCMER `1.71.0`; do not silently upgrade to 2.x;
- EnemyIsolation off;
- Compatibility Fixes `1.3.14`;
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

Project-local patch policy: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Exact next state

**Runtime-test the already-imported S1.42AA on Offense before any successor is built.**

One normal successful Offense gameplay run is the intended minimum. Enter the generated interior and then upload the complete fresh `LogOutput.log` using the exact corrected S1.42AA one-line uploader in:

`Current/91_S1.42AA_BUILD_CANDIDATE_INTERIOR_WEIGHT_EQUALIZATION.md`

The log must show eligible `Viable ExtendedDungeonFlows` at common effective weight `100` rather than the previous unequal author weights and must show no dungeon-generation regression, duplicate Black Mesa/native-owner regression, Work/no-task, Leader-null, Fatal or new project-local exception class.

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AA_BUILD_AWAITING_RUNTIME_VALIDATION` with S1.42AA as guarded base.  
`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AA`.  
`RuntimeInbox/Current/` contains only `.gitkeep`.  
No successor is armed.

## Gale active-profile replacement workflow — canonical and binding

Implementation: `RuntimeTools/ReplaceActiveGaleProfile.ps1`  
Workflow contract: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
Binding chat/build policy: `Current/09_REPOSITORY_FIRST_AUTOMATION.md`

Canonical launcher:

```powershell
iex (iwr -UseBasicParsing 'https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1').Content
```

The final y/n version was user-validated under Windows PowerShell 5.1 with a disposable `testpowershell` profile and used successfully for the S1.42AA import flow. The helper downloads before deletion, verifies SHA-256, requires explicit `y/n`, opens Gale, leaves **Advanced options -> Import all files** manual, and cleans the temporary download only after confirmed import.

Every future response that announces a newly built ready-to-test profile must include both this launcher and the exact build-specific runtime-log uploader without waiting for the user to ask.

## Deferred — keep separate from S1.42AA runtime gate

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed to `8 × 12.5%`;
- final long full-stack acceptance;
- monitor-only AdditionalNetworking / LethalMin repairs;
- cosmetic documentation cleanup.

## Known monitor-only / non-functional issues

Do not patch known setup/teardown error classes without stronger reproducibility or user-facing impact. Known documentation drift remains in older chronology wording under `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs`; newer canonical documents, actual code/config and runtime evidence override them.

## Repository-first rule

Do not ask for a local repository clone or manual profile rebuild when GitHub infrastructure can perform the work. Profile builds, patch compilation, archive verification and repository handover are performed through the GitHub-native workflow. Local user action is reserved for actual gameplay/runtime testing and the documented profile-import/log-upload helpers.
