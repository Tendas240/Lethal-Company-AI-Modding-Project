# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth and canonical build/handover workspace.

Do not require a local repository clone or local profile build while the repository contains the required bases and GitHub-native infrastructure.

## Read first

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/100_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AB_RUNTIME_NEXT.md`
4. `Current/101_REPOSITORY_HANDOVER_AUDIT_S1.42AB.md`
5. `Current/00_CURRENT_STATE.md`
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

Chronologically newer confirmed documents override older version-specific wording. `Current/100`, `Current/101`, `Current/00`, `Current/04`, `Current/96` and `Current/Projektstatus_S1.42AB_CANDIDATE.json` are authoritative for the active runtime gate. `Current/90` and `Current/Projektstatus_S1.42Z_ACCEPTED.json` remain authoritative for the accepted rollback baseline. Older handovers are historical evidence only.

## Accepted rollback baseline

**S1.42Z — Jetpack Pikmin Retune — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42Z Jetpack Pikmin Retune.r2z`  
SHA-256: `a030d4b280b4768f6859f6fea43981004c48f31060f100322206b6016a1477e4`  
Acceptance: `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`  
Runtime evidence: `RuntimeEvidence/S1.42Z/20260904T135820Z/`  
Raw log SHA-256: `ca61e82e5a7d12f96dcb51849e291582df4d45568da4fa1e10b476551c897db8`

S1.42Z remains accepted until S1.42AB passes its own fresh gameplay runtime gate.

## Rejected candidate — S1.42AA

**S1.42AA — Interior Weight Equalization — RUNTIME FAIL / NOT ACCEPTED**

Profile SHA-256: `0490abe0ceb441489d5cef98a78df979387d2e5de513f0cdbb42d84b084ba364`  
Runtime evidence: `RuntimeEvidence/S1.42AA/20260904T153744Z/`

The config-only experiment `Inject Dynamic Matching Weights = false` did not equalize the actual LethalLevelLoader pool. Offense still showed values from `20` to `300`. Root cause: LLL keeps the highest matching rarity, so a generic `100` match cannot reduce stronger author/planet/mod matches.

Black Mesa generated successfully. A separate Pikmin carrying scrap from a Black Mesa table became stuck and the log showed repeated unreachable entrance / `Unpathable` ToShip routing. Track that as a map/NavMesh/LethalMin compatibility issue, not as the interior-weight failure. The AA log also contained two Work/no-task warnings in a separate White-Pikmin lifecycle sequence; monitor if reproduced.

## Active candidate — S1.42AB

**S1.42AB — Interior Weight Normalization**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Status: **BUILD PASS / LOCAL IMPORT PASS / GAMEPLAY RUNTIME OPEN / NOT ACCEPTED**

Successful build run: `33892396551`  
Automated build commit: `9bf3085d82990ca565ad81f992d896855c21f1c6`  
DLL SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`

S1.42AB was built directly from accepted S1.42Z. It retains `Inject Dynamic Matching Weights = true`; AA's failed `false` change is not inherited.

The patch is a Postfix on `DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`. LLL first decides which flows are viable/excluded. The patch only changes positive rarity values in the already-returned list to `100`. It does not add/remove/re-register flows and does not touch Enemy/Scrap/MapObject rarity systems.

LLL's built-in `Viable ExtendedDungeonFlows` line is emitted before the Postfix and may still show the old values. The authoritative AB marker is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

Every positive entry there must be `(100)`.

## Local Gale state — already complete

S1.42AB is **already imported locally and is the current Gale profile**. Do not ask for a reinstall before the immediate gameplay test.

The canonical helper `RuntimeTools/ReplaceActiveGaleProfile.ps1` is **FULL END-TO-END USER-VALIDATED** under Windows PowerShell 5.1.

Validated revision: `2026-09-04-import-uia-v2.1-download-hotfix`  
Helper blob SHA: `9458f427b538615249714e7f064f3107d6dcd36c`  
Validated commit: `f711f53f4971f97200ed3605479ef887a14b243d`  
AB archive `export.r2x` evidence SHA: `331c01bfe5eda5d4ce9bc2a887fd322b302f32dccf9d95918d6c7d0c7fb6cf40`

On the validated happy path, after selecting the old profile numerically and confirming `y`, the helper automatically resolves Missing Profiles, opens the candidate exactly once, enables `Import all files`, invokes Import, verifies the exact target `export.r2x` hash, and cleans the temporary archive. No further Gale click or PowerShell Enter is required.

Canonical launcher for future new-build replacements:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Do **not** run the replacement helper again for the immediate AB test because AB is already installed and current.

## Exact next action

**Run one normal Offense gameplay test with the already-imported S1.42AB. Do not build a successor first.**

1. start normally and reach lobby;
2. route to Offense and land;
3. enter the generated interior;
4. play normally;
5. upload the complete fresh `LogOutput.log` using the exact uploader in `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`;
6. analyze before deciding any successor.

One successful Offense run is sufficient if the authoritative final-pool marker is present. Do not farm every interior manually.

Minimum gate: final effective viable pool all positive `100`, no excluded-flow insertion, successful dungeon generation, accepted Z gameplay healthy, Leader-null `0`, Fatal `0`, and no new project-local exception flood. Work/no-task should preferably be `0`; if the AA two-warning lifecycle case reproduces, analyze separately.

`RuntimeInbox/Current/` currently contains only `.gitkeep`; there is no S1.42AB gameplay runtime log yet.

## Permanent compatibility / anti-regression state

Preserve:

- exact BCMER `1.71.0`; never silently upgrade to 2.x;
- EnemyIsolation disabled;
- Compatibility Fixes `1.3.14`;
- `BaboonBirdPikminEnemy` enabled;
- narrow Hawk -> Pikmin prevention only;
- inherited PikminEnemy lifecycle preserved;
- Pikmin -> Baboon Hawk attack allowed;
- Puffer -> Pikmin protection;
- Thumper Bite Limit `3`;
- Crawler absent from LethalMin Attack Blacklist;
- accepted S1.42C-derived moon power/spawn baseline;
- SpawnCycleFixes `Consistent Spawn Times = true`;
- accepted Z Jetpack/Pikmin/CodeRebirth/Microwave/Snail tuning.

Never repeat the S1.42R whole-component disable approach.

## Deferred — do not mix into AB

- Black Mesa table/NavMesh/Pikmin route recovery;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Functional Microwave spawn-rarity reduction;
- BCMER EventTypes `8 × 12.5%`;
- final long full-stack acceptance;
- AdditionalNetworking repair without reproducible user-facing evidence;
- LethalMin teardown repair without stronger evidence;
- cosmetic documentation cleanup.

Potential later isolated evaluation after AB: `woah25-LethalEscapeUpdated 2.5.0` for V81. Do not add it to AB; inspect the actual 2.5.0 package/config first and protect the existing LethalMin/Pikmin/Baboon Hawk pathfinding/lifecycle architecture.

## Controllers

`BuildSpecs/current.json` is correctly disabled at `IDLE_AFTER_S1.42AB_BUILD_AWAITING_RUNTIME_VALIDATION`, guarded by the AB profile SHA. No successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

Known old wording in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` is intentional non-functional drift; newer canonical docs, actual code/config and fresh runtime evidence override it.
