# Lethal Company AI Modding Project

GitHub is the canonical source of truth and build/handover workspace for this project.

Game: **Lethal Company V81**

Do not require a local repository clone or local profile build while the required base artifacts and GitHub-native infrastructure are present.

## Current canonical state

### Accepted full-normal-stack baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`

Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`  
Raw log SHA-256: `42cfba3d157f6abdbeee114909d90749d1bfd043d4b0c224922ad5be976194ae`

S1.42AB is the rollback baseline while S1.42AC is under fresh runtime validation.

Accepted AB behavior includes the post-viability LethalLevelLoader normalization architecture: LLL owns viable/excluded membership first, then every positive rarity in the returned list becomes exactly `100`. The accepted Offense run preserved all 40 viable flows, normalized 12/40 values from a pre-range of `20..300`, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

Authoritative interior marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

LLL's earlier built-in `Viable ExtendedDungeonFlows` line is pre-Postfix and may remain unequal.

### Active runtime candidate

**S1.42AC — BCMER EventType Equal Distribution — BUILD PASS / RUNTIME OPEN / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
Gale profile name: `LC V1 S1.42AC BCMER EventType Equal Distribution`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Build workflow run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`

Candidate record: `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_CANDIDATE.json`  
Plan: `BuildSpecs/S1.42AC_PLAN.md`  
Snapshot: `ProfileSources/S1.42AC/`

S1.42AC is a deliberately isolated config-only change to:

`BepInEx/config/BrutalCompanyMinusExtraReborn/Difficulty_Settings.cfg`

`Use custom weights? = false` is preserved. All eight `[_EventType Weights]` scales are fixed to:

`12.5, 0.0, 12.5, 12.5`

Target distribution:

- Insane `12.5%`;
- VeryBad `12.5%`;
- Bad `12.5%`;
- Neutral `12.5%`;
- Good `12.5%`;
- VeryGood `12.5%`;
- Rare `12.5%`;
- Remove `12.5%`.

Automated archive verification vs accepted S1.42AB:

- ZIP members `334`;
- changed existing members exactly `Difficulty_Settings.cfg` and `export.r2x`;
- added members `0`;
- removed members `0`;
- mod state/add/remove changes `0`;
- no DLL or project-local code patch added.

Exact BCMER `1.71.0` is preserved. Do not silently upgrade to 2.x.

## Local Gale / next action

The last confirmed installed Gale profile is accepted S1.42AB. S1.42AC must be imported before testing.

Canonical replacement helper:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfile.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

The helper is fully end-to-end validated under Windows PowerShell 5.1. Select the old S1.42AB profile numerically and confirm `y`; the validated path handles the remaining Gale import, `Import all files`, verification and cleanup automatically.

After import, run one normal **Offense** gameplay round. Do not farm all eight EventTypes manually. The primary acceptance evidence is the eight BCMER runtime lines:

`Set eventType weight for <type> to <value>`

All eight values for the same roll context must be identical. Then upload the complete fresh log with the exact S1.42AC PowerShell uploader in `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AC_BUILD_AWAITING_RUNTIME_VALIDATION`, guarded by S1.42AC SHA-256 `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`. No successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AC`

## Read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/103_S1.42AC_BUILD_CANDIDATE_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
3. `Current/Projektstatus_S1.42AC_CANDIDATE.json`
4. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
5. `Current/Projektstatus_S1.42AB_ACCEPTED.json`
6. `Current/00_CURRENT_STATE.md`
7. `Current/01_HANDOVER_CORE.md`
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

Chronologically newer confirmed information overrides older version-specific wording.

## Planned repository information architecture overhaul

The deferred repository cleanup is now a binding information-architecture and retrieval-hardening project rather than merely cosmetic cleanup.

**If a future user asks to start/execute the overhaul, begin with:**

`OVERHAUL_START_HERE_ChatGPT.txt`

Binding plan: `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`  
Binding execution playbook: `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`  
Machine requirements: `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

The target is reliable fresh-chat operation under limited context through a compact bootstrap, human+JSON topic knowledge map, explicit authority/supersession metadata, build lineage, provenance links, readable profile snapshots, broken-link/orphan CI validation and answerability-routing regression tests.

Before any structural overhaul change, the complete pre-overhaul repository must be frozen and verified in a **separate standalone backup repository**; a branch/tag in this repository alone is insufficient. The primary repository must then record `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`. The full mandatory sequence, stop conditions, rollback rules and multi-chat handover requirements are defined in `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`.

The overhaul is planned but must not disturb or be mixed with the active S1.42AC runtime gate.

## Permanent anti-regression state

Preserve exact BCMER `1.71.0`, EnemyIsolation off, Compatibility Fixes `1.3.14`, `BaboonBirdPikminEnemy` enabled, narrow Hawk -> Pikmin prevention only, native inherited PikminEnemy lifecycle, Pikmin -> Baboon Hawk attack allowed, Puffer -> Pikmin protection, Thumper Bite Limit `3`, Crawler absent from LethalMin Attack Blacklist, accepted S1.42C-derived moon power/spawn baseline, `Consistent Spawn Times = true`, Jetpack base acceleration `18`, Jet Fuel `18/18`, Thrusters `25/20`, Indoor Pikmin `0.09`, CarryStrength `3 / 30`, CodeRebirth ACU + G.R.E.G. exact 18 curves ×`0.5`, Functional Microwave volume `0.15`, Immortal Snail `40 / 2`, and the accepted S1.42AB interior-normalization architecture.

Never repeat the S1.42R whole-component disable approach.

## Deferred after S1.42AC

Keep separate unless explicitly selected/grouped:

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa table/NavMesh/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul starting at `OVERHAUL_START_HERE_ChatGPT.txt`, governed by `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md` and `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`, including cosmetic drift cleanup as a subordinate task.
