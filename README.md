# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for this project.

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

Accepted AB behavior includes post-viability LethalLevelLoader normalization: LLL owns viable/excluded membership first, then every positive rarity in the returned list becomes exactly `100`. The accepted Offense run preserved all 40 viable flows, normalized 12/40 values from `20..300`, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

Authoritative interior marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

### Latest build — rejected

**S1.42AC — BCMER EventType Equal Distribution — BUILD PASS / RUNTIME FAIL / REJECTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Build run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`  
Rejection record: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_REJECTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`  
Raw log SHA-256: `8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0`

AC set all eight BCMER EventType scales to the same constant `12.5, 0.0, 12.5, 12.5`, but five runtime contexts produced unequal final weights:

`Insane 6843 / VeryBad 506 / Bad 355 / Neutral 1368 / Good 1244 / VeryGood 2737 / Rare 27375 / Remove 883`

Therefore the intended fixed `8 × 12.5%` final distribution was not achieved. AC is not a gameplay base.

The scale changes did influence the final weights relative to AB, but equal configured scales do not imply equal final BCMER weights. Do not repeat that assumption.

### Exact next step

No runtime test is currently outstanding and no successor is armed.

Inspect the exact BCMER `1.71.0` calculation path that produces final `Set eventType weight for <type> to <value>` values. Identify all additional type-dependent inputs and the owner of the final effective type-weight pool. Only after that analysis choose a safe successor implementation: proven config compensation if mathematically reliable, or a narrow fail-closed project-local final-weight normalization if safer.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AC_RUNTIME_REJECTION_ANALYSIS_REQUIRED`, guarded by accepted S1.42AB.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

No successor is armed.

## Read first

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/107_FINAL_HANDOVER_S1.42AB_ACCEPTED_S1.42AC_REJECTED_NEXT.md`
3. `Current/108_REPOSITORY_HANDOVER_AUDIT_S1.42AC_REJECTED.md`
4. `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
5. `Current/Projektstatus_S1.42AC_REJECTED.json`
6. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
7. `Current/Projektstatus_S1.42AB_ACCEPTED.json`
8. `Current/00_CURRENT_STATE.md`
9. `Current/01_HANDOVER_CORE.md`
10. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
11. `BuildSpecs/current.json`
12. `RuntimeInbox/ACTIVE_BUILD.txt`
13. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
14. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

Historical candidate/build files remain evidence; chronologically newer confirmed rejection/acceptance records override older open-candidate wording.

## Planned repository information-architecture overhaul

The repository cleanup is now a binding information-architecture/retrieval-hardening project, but it is **not executed yet**.

If a future user explicitly starts the overhaul, begin with:

`OVERHAUL_START_HERE_ChatGPT.txt`

Binding plan: `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`  
Execution playbook: `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`  
Machine requirements: `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

The future overhaul must re-resolve the then-current project state and, before the first structural migration change, freeze the exact HEAD and create/verify a **separate standalone backup repository**. A branch/tag in the primary repository alone is insufficient. The backup provenance must be recorded in `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`.

The target architecture is compact bootstrap -> knowledge map -> canonical topic source -> evidence/config/code/history, with repository search as fallback, explicit current-vs-history authority, build lineage, redirects/supersession, readable binary/profile evidence, CI knowledge validation, answerability routing tests and at most three logical document hops from bootstrap to every major current topic.

## Permanent anti-regression state

Preserve exact BCMER `1.71.0`, accepted BCMER rain disables, EnemyIsolation off, Compatibility Fixes `1.3.14`, `BaboonBirdPikminEnemy` enabled, narrow Hawk -> Pikmin prevention only, native inherited PikminEnemy lifecycle, Pikmin -> Baboon Hawk attack allowed, Puffer -> Pikmin protection, Thumper Bite Limit `3`, Crawler absent from LethalMin Attack Blacklist, accepted S1.42C-derived moon power/spawn baseline, `Consistent Spawn Times = true`, Jetpack base acceleration `18`, Jet Fuel `18/18`, Thrusters `25/20`, Indoor Pikmin `0.09`, CarryStrength `3 / 30`, CodeRebirth ACU + G.R.E.G. exact 18 curves ×`0.5`, Functional Microwave volume `0.15`, Immortal Snail `40 / 2`, and accepted S1.42AB interior normalization.

Never repeat the S1.42R whole-component disable approach.

## Deferred separate scopes

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul.
