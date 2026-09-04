# 01 — Handover Core

## Identity

Game: **Lethal Company V81**  
Repository: `Tendas240/Lethal-Company-AI-Modding-Project`  
Repository is the Source of Truth and canonical build/handover workspace.

Do not require a local repository clone or local profile build while repository-native artifacts and automation are available.

## Read first

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/107_FINAL_HANDOVER_S1.42AB_ACCEPTED_S1.42AC_REJECTED_NEXT.md`
4. `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`
5. `Current/Projektstatus_S1.42AC_REJECTED.json`
6. `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`
7. `Current/Projektstatus_S1.42AB_ACCEPTED.json`
8. `Current/00_CURRENT_STATE.md`
9. `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`
10. `BuildSpecs/current.json`
11. `RuntimeInbox/ACTIVE_BUILD.txt`
12. `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`
13. `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md`

If the user explicitly starts the planned repository overhaul, switch to `OVERHAUL_START_HERE_ChatGPT.txt` and follow `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md` and `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`. Otherwise do not execute that overhaul during normal gameplay/build work.

## Accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Machine state: `Current/Projektstatus_S1.42AB_ACCEPTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

Accepted architecture: LethalLevelLoader determines viable/excluded dungeon membership first; project-local S1.42AB Postfix changes only positive rarities in the returned list to `100`. Accepted Offense runtime preserved 40 viable entries, normalized 12/40 from `20..300`, kept Black Mesa single-registered, generated `Expanded facility`, and had Work/no-task `0`, Leader-null `0`, Compatibility Fixes Error `0` and Fatal `0`.

## Latest build — rejected

**S1.42AC — BCMER EventType Equal Distribution — BUILD PASS / RUNTIME FAIL / REJECTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Build run: `33903271224`  
Automated build commit: `a30b327580e28f42e55281e91abe03d32ae41363`  
Rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Machine state: `Current/Projektstatus_S1.42AC_REJECTED.json`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T181854Z/`  
Raw log SHA-256: `8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0`

AC set all eight BCMER `[_EventType Weights]` scales to the same constant `12.5, 0.0, 12.5, 12.5`, but five runtime roll contexts produced unequal final values:

`Insane 6843 / VeryBad 506 / Bad 355 / Neutral 1368 / Good 1244 / VeryGood 2737 / Rare 27375 / Remove 883`

Therefore the intended equal `8 × 12.5%` final distribution failed.

AC changed final values relative to AB, so the configured scales matter, but equal configured scales do not imply equal final weights. Do not repeat this implementation assumption.

## AC preserved checks / secondary evidence

AC still preserved BCMER execution and S1.42AB interior normalization. Offense final viable pool stayed 40 entries all positive `100`; `Mausoleum` generated; Work/no-task `0`; Leader-null `0`; Compatibility Fixes Error `0`; NetworkObjectReference regression `0`; PikminNoticeZone regression `0`; Fatal `0`.

Secondary log evidence: 43 dominant NavMeshAgent:SetDestination error signatures and 26 LethalMin route-failure signatures. Treat separately as interior/Pikmin routing evidence; do not attribute to the BCMER config-only change without reproducibility.

## Exact next action

No runtime test is outstanding and no successor is armed.

First inspect the exact BCMER `1.71.0` calculation producing final `Set eventType weight for <type> to <value>` values. Identify the final effective type-weight owner and all additional type-dependent inputs. Only then choose between proven config compensation and a narrow fail-closed project-local final-weight normalization, and only then plan/arm a successor.

Do not silently assign/build a successor before this analysis.

## Controllers

`BuildSpecs/current.json` is disabled at `IDLE_AFTER_S1.42AC_RUNTIME_REJECTION_ANALYSIS_REQUIRED`, guarded by the accepted S1.42AB profile/SHA. No successor is armed.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

## Mandatory runtime-test UX

Whenever a future runtime test is outstanding, the response that explains the test must also include the exact build-specific PowerShell one-line log uploader. Do not make the user ask for it afterwards.

## Permanent invariants

Preserve exact BCMER `1.71.0`; accepted BCMER rain disables; EnemyIsolation disabled; Compatibility Fixes `1.3.14`; BaboonBirdPikminEnemy enabled; narrow Hawk -> Pikmin prevention only; inherited PikminEnemy lifecycle; Pikmin -> Baboon Hawk attack allowed; Puffer protection; Thumper Bite Limit `3`; Crawler absent from Attack Blacklist; accepted S1.42C moon power/spawn baseline; `Consistent Spawn Times = true`; Jetpack `18`; Jet Fuel `18/18`; Thrusters `25/20`; Indoor Pikmin `0.09`; CarryStrength `3 / 30`; CodeRebirth ACU/G.R.E.G. exact 18 curves ×`0.5`; Functional Microwave volume `0.15`; Immortal Snail `40 / 2`; accepted S1.42AB interior normalization.

Never repeat S1.42R's whole-component disable approach. Follow `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` for new project-local patches.

## Deferred after AC rejection analysis

Keep separate unless explicitly selected/grouped:

- Functional Microwave spawn-rarity reduction;
- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- Mausoleum fog reduction;
- Black Mesa/interior/Pikmin route recovery;
- isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation;
- final long full-stack acceptance;
- AdditionalNetworking / LethalMin teardown repair only with stronger evidence;
- repository information-architecture overhaul.

## Repository overhaul continuity

Planned but not executed. Dedicated future entry: `OVERHAUL_START_HERE_ChatGPT.txt`. The actual overhaul must re-resolve the then-current state and create/verify a separate standalone pre-overhaul backup repository before its first structural migration change.
