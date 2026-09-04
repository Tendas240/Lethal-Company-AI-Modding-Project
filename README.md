# Lethal Company AI Modding Project

GitHub is the canonical source of truth and build/handover workspace for this project.

Game: **Lethal Company V81**

Do not require a local repository clone or local profile build while the required base artifacts and GitHub-native infrastructure are present.

## Current canonical state

### Accepted full-normal-stack baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`

Canonical runtime acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Machine-readable accepted state: `Current/Projektstatus_S1.42Z_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z remains the rollback baseline until S1.42AB passes fresh gameplay runtime validation.

### Rejected candidate

**S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AA Interior Weight Equalization.r2z`  
SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

The config-only change `Inject Dynamic Matching Weights = false` did not equalize effective LethalLevelLoader dungeon rarities. Offense still contained values from `20` through `300`. Root cause: LLL retains the highest matching rarity, so generic `Vanilla:100,Custom:100` matches cannot reduce stronger author/planet/mod matches.

Black Mesa generated successfully in the AA run. A separate Pikmin-on-table incident produced repeated unreachable entrance / `Unpathable` ToShip routing and is retained as a likely Black Mesa/NavMesh/LethalMin compatibility finding. The same run contained two Work/no-task warnings in a separate White-Pikmin lifecycle sequence; both are monitor-only unless reproduced.

### Active runtime candidate

**S1.42AB — Interior Weight Normalization — BUILD PASS / LOCAL IMPORT PASS / GAMEPLAY RUNTIME OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Build workflow run: `33892396551`  
Automated build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`  
Injected DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

Candidate record: `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine-readable state: `Current/Projektstatus_S1.42AB_CANDIDATE.json`  
Plan / Patch Safety Review: `BuildSpecs/S1.42AB_PLAN.md`

S1.42AB was built directly from accepted S1.42Z and retains `Inject Dynamic Matching Weights = true`; S1.42AA's failed config experiment is not inherited.

S1.42AB patches `LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)` with a Postfix. LLL decides viability/exclusions first; only positive rarity values in the already-returned viable list are then normalized to `100`. No flow membership is added/removed and Enemy/Scrap/MapObject rarity systems are untouched.

LLL's earlier built-in `Viable ExtendedDungeonFlows` log line may still show pre-normalization values. The authoritative runtime marker is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry there must be `(100)`.

## Local Gale state

S1.42AB is **already imported and current in Gale**. Do not ask the user to reinstall it before the immediate gameplay test.

The canonical replacement helper `RuntimeTools/ReplaceActiveGaleProfile.ps1` is now **FULL END-TO-END USER-VALIDATED** under Windows PowerShell 5.1.

Validated revision: `2026-09-04-import-uia-v2.1-download-hotfix`  
Validated helper blob SHA: `9458f427b538615249714e7f064f3107d6dcd36c`  
Validated implementation commit: `f711f53f4971f97200ed3605479ef887a14b243d`

After the user selects the old profile numerically and confirms `y`, the validated happy path automatically handles Missing Profiles, single-open `.r2z` import, `Advanced options -> Import all files -> Import`, exact target `export.r2x` hash verification and temporary download cleanup. No further Gale click or PowerShell Enter is required.

Permanent workflow: `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`  
Import automation history: `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`

## Latest handover — read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/100_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AB_RUNTIME_NEXT.md`
3. `Current/101_REPOSITORY_HANDOVER_AUDIT_S1.42AB.md`
4. `Current/00_CURRENT_STATE.md`
5. `Current/01_HANDOVER_CORE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`
8. `Current/Projektstatus_S1.42AB_CANDIDATE.json`
9. `Current/06_RECENT_WORK_S1.42AA-S1.42AB.md`
10. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
11. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
12. `BuildSpecs/S1.42AB_PLAN.md`
13. `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`
14. `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`
15. `Current/09_REPOSITORY_FIRST_AUTOMATION.md`
16. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
17. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
18. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
19. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
20. `BuildSpecs/current.json`
21. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed information overrides older version-specific wording. `Current/100` and `Current/101` are the newest dedicated handover/audit pair for the active gate.

## Exact next step

**Do not re-import S1.42AB and do not build a successor yet.**

Run one normal Offense gameplay round using the already-imported S1.42AB, enter the generated interior, then upload the complete fresh `LogOutput.log` with the exact one-line uploader in `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`.

One successful Offense run is sufficient if the authoritative final effective-pool marker is present. Judge equalization from that post-normalization marker, not from LLL's earlier built-in viable-flow line.

`RuntimeInbox/Current/` currently contains only `.gitkeep`; no S1.42AB gameplay log has been submitted yet.

## Current controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AB_BUILD_AWAITING_RUNTIME_VALIDATION`, guarded by S1.42AB SHA-256 `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`. No successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

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
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- `Consistent Spawn Times = true`;
- accepted S1.42Z Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning.

Never repeat the S1.42R whole-component disable approach.

Project-local patch policy: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

## Deferred / monitor-only

Keep separate from S1.42AB until its runtime gate closes unless the user explicitly changes scope:

- Black Mesa table/NavMesh/Pikmin route recovery;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes fixed `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- cosmetic documentation cleanup;
- isolated future evaluation of `woah25-LethalEscapeUpdated 2.5.0` after the AB gate.

Known non-functional drift remains intentionally in older chronology wording under `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs`; newer canonical documents, actual code/config and runtime evidence override them.
