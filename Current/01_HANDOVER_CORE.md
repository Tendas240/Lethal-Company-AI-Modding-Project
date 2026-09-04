# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the source of truth and canonical build/handover workspace.

Do not require a local repository clone or local profile build while repository-native artifacts and automation are available.

## Read first

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
4. `Current/Projektstatus_S1.42AC_CANDIDATE.json`
5. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
6. `Current/Projektstatus_S1.42AB_ACCEPTED.json`
7. `Current/00_CURRENT_STATE.md`
8. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
9. `BuildSpecs/S1.42AC_PLAN.md`
10. `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`
11. `Current/99_GALE_IMPORT_DIALOG_AUTOMATION_REVISION.md`
12. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
13. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`
14. `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`
15. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`
16. `BuildSpecs/current.json`
17. `RuntimeInbox/ACTIVE_BUILD.txt`

Chronologically newer confirmed documents override older version-specific wording.

## Accepted rollback baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

Accepted AB architecture: LethalLevelLoader determines viable/excluded flow membership first; a project-local Postfix changes only positive rarities in the returned list to `100`. The accepted Offense run preserved all 40 entries, normalized 12/40 from `20..300`, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

## Active runtime candidate

**S1.42AC — BCMER EventType Equal Distribution — BUILD PASS / RUNTIME OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
Gale profile name: `LC V1 S1.42AC BCMER EventType Equal Distribution`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Build run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`  
Candidate: `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_CANDIDATE.json`

Frozen delta: only `BepInEx/config/BrutalCompanyMinusExtraReborn/Difficulty_Settings.cfg` plus normal profile-name change in `export.r2x`.

`Use custom weights? = false` is preserved. All eight EventType scales are exactly `12.5, 0.0, 12.5, 12.5`, targeting Insane, VeryBad, Bad, Neutral, Good, VeryGood, Rare and Remove at equal `12.5%` normalized selection probability independent of difficulty.

Automated delta verification: ZIP members `334`; changed existing exactly `Difficulty_Settings.cfg` + `export.r2x`; added `0`; removed `0`; mod state/add/remove delta `0`; no DLL/code patch.

## Exact next action

The last confirmed installed Gale profile is S1.42AB. Import S1.42AC using:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

Then run one normal Offense gameplay round. Do not farm all eight event categories manually.

Primary acceptance evidence: all eight BCMER `Set eventType weight for <type> to <value>` lines must be present for the same roll context and all eight values must be identical. Also require normal BCMER execution, healthy S1.42AB interior normalization when emitted, Leader-null `0`, Fatal `0`, Work/no-task preferably `0`, and no new config-induced error flood.

After the run use the exact S1.42AC one-line runtime uploader stored in `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`.

## Mandatory runtime-test UX

Whenever a runtime test is outstanding, the response that explains the test must also include the exact build-specific PowerShell one-line log uploader. Do not make the user ask for it afterwards.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AC_BUILD_AWAITING_RUNTIME_VALIDATION`, guarded by S1.42AC SHA-256 `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`. No successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AC`

## Permanent invariants

Preserve exact BCMER `1.71.0`; EnemyIsolation disabled; Compatibility Fixes `1.3.14`; BaboonBirdPikminEnemy enabled; narrow Hawk -> Pikmin prevention only; inherited PikminEnemy lifecycle; Pikmin -> Baboon Hawk attack allowed; Puffer protection; Thumper Bite Limit `3`; Crawler absent from Attack Blacklist; accepted S1.42C moon power/spawn baseline; `Consistent Spawn Times = true`; Jetpack `18`; Jet Fuel `18/18`; Thrusters `25/20`; Indoor Pikmin `0.09`; CarryStrength `3 / 30`; CodeRebirth ACU/G.R.E.G. exact 18 curves ×`0.5`; Functional Microwave volume `0.15`; Immortal Snail `40 / 2`; accepted S1.42AB interior normalization.

Never repeat S1.42R's whole-component disable approach.

## Deferred after AC

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa table/NavMesh/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- cosmetic documentation cleanup.
