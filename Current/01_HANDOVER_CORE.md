# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth and canonical build/handover workspace.

Do not require a local repository clone or local profile build while the repository contains the required bases and GitHub-native infrastructure.

## Read first

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
4. `Current/Projektstatus_S1.42AB_ACCEPTED.json`
5. `Current/00_CURRENT_STATE.md`
6. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
7. `Current/96_S1.42AB_BUILD_CANDIDATE_INTERIOR_WEIGHT_NORMALIZATION.md`
8. `Current/100_FINAL_HANDOVER_S1.42Z_ACCEPTED_S1.42AB_RUNTIME_NEXT.md`
9. `Current/101_REPOSITORY_HANDOVER_AUDIT_S1.42AB.md`
10. `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`
11. `Current/Projektstatus_S1.42Z_ACCEPTED.json`
12. `BuildSpecs/S1.42AB_PLAN.md`
13. `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`
14. `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`
15. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
16. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
17. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
18. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
19. `BuildSpecs/current.json`
20. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific wording. `Current/102` plus `Current/Projektstatus_S1.42AB_ACCEPTED.json` are authoritative for the latest accepted state. `Current/100` and `Current/101` are historical handover/audit evidence from immediately before the AB gate closed.

## Canonical accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
Gale profile name: `LC V1 S1.42AB Interior Weight Normalization`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`  
Raw log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

Fresh Offense runtime proved the exact LLL `1.7.12` contract, armed the Postfix, preserved the same 40 viable flows and normalized every positive final effective rarity to `100`. `12 / 40` entries changed from a pre-normalization range of `20..300`. Black Mesa remained single-registered at `100`; normal dungeon generation selected `Expanded facility`; the user entered the generated interior, played normally until death and reported no problematic behavior.

Regression markers: Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0`, unspawned NetworkObjectReference `0`, PikminNoticeZone `0`, Fatal `0`.

The 32 Error-severity events match accepted S1.42Z and remain in previously monitored non-project-local/setup classes. S1.42AB emitted no project-local Error flood.

## Accepted interior architecture

Patch target:

`LethalLevelLoader.DungeonManager.GetValidExtendedDungeonFlows(ExtendedLevel, bool)`

LLL owns viability/exclusion membership. The project-local Harmony Postfix only normalizes positive rarity values in the already-returned viable list to `100`.

Permanent rule:

- flow not returned by LLL -> remains unavailable;
- returned positive rarity -> effective rarity `100`;
- no flow appended, removed, re-registered or deduplicated;
- no LLL matching/config rewrite;
- Enemy, Scrap and MapObject rarity systems untouched;
- future interiors automatically receive effective rarity `100` whenever LLL considers them viable.

Preserve the Shatteredrooms Experimentation/Embrion restriction until dedicated evidence proves removal safe.

The built-in LLL `Viable ExtendedDungeonFlows` line is pre-Postfix only. The authoritative accepted marker is:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

## Previous states

**S1.42Z — Jetpack Pikmin Retune** remains the previous accepted rollback/provenance artifact. Its accepted tuning is inherited by S1.42AB.

**S1.42AA — Interior Weight Equalization** remains runtime-rejected. The `Inject Dynamic Matching Weights = false` approach failed because LLL retains the highest matching rarity. Do not revive it.

The AA Black Mesa table/NavMesh/Pikmin routing issue remains deferred. Its separate two-warning Work/no-task lifecycle finding did not reproduce in AB.

## Local Gale / import tooling

S1.42AB remains current in Gale.

`RuntimeTools/ReplaceActiveGaleProfile.ps1` is **FULL END-TO-END USER-VALIDATED** under Windows PowerShell 5.1.

Validated revision: `2026-09-04-import-uia-v2.1-download-hotfix`  
Helper blob SHA: `9458f427b538615249714e7f064f3107d6dcd36c`  
Validated commit: `f711f53f4971f97200ed3605479ef887a14b243d`

See `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md` and `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`.

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
- Jetpack `18`, Jet Fuel `18/18`, Thrusters `25/20`;
- Indoor Pikmin `0.09`, CarryStrength `3 / 30`;
- CodeRebirth ACU + G.R.E.G. exact 18 curves ×`0.5`;
- Functional Microwave volume `0.15`;
- Immortal Snail `40 / 2`;
- accepted S1.42AB interior normalization architecture.

Never repeat the S1.42R whole-component disable approach.

## Exact next state

No successor is armed.

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AB_ACCEPTANCE`, guarded by the accepted S1.42AB profile SHA.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

The next isolated scope requires explicit selection. BCMER EventTypes equal distribution `8 × 12.5%` is now eligible to be selected next because the AB gate is closed, but it is not implicitly authorized.

## Deferred scopes

- BCMER EventTypes `8 × 12.5%`;
- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa table/NavMesh/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- cosmetic documentation cleanup.

Known stale wording in older chronology files/comments is non-functional and lower-authority than this handover, actual code/config and fresh runtime evidence.
