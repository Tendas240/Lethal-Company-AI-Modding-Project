# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-06

## Current gameplay state

Accepted baseline is **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`. Fresh acceptance evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`.

Latest built artifact is **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**, `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`, SHA-256 `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`. Rejection authority: `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`. Runtime evidence: `RuntimeEvidence/S1.42AG/20260906T085500Z/`.

There is **no active runtime candidate**. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains only the last evidence-attribution target. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AG_RUNTIME_REJECTION_AWAITING_TARGETED_ANALYSIS` and guards accepted S1.42AF. No successor beyond S1.42AG is armed.

## Closed S1.42AG runtime gate

S1.42AG successfully proved a narrow partial fix:

- exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` was patched with the intended `Priority.First` prevention-only prefix;
- the guard executed during the encounter;
- the harmful LethalMin Mouth Dog -> Pikmin `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab/death-timer state-mutation path was absent;
- `Work state with no task assigned!` count was `0`, compared with 707 warnings in the S1.42AF exposure evidence;
- no compatibility-fix error or fatal marker was introduced;
- the inherited S1.42AF Functional Microwave contract stayed healthy (`PrioritiseMoons=true`, 18 Moon/tag, 18 Interior/tag, Moon curves scaled by `0.5`, Interior curves validation-only).

S1.42AG is nevertheless rejected because the full one-way interaction contract failed: the user directly observed a Mouth Dog visibly target and attack a scrap-carrying Purple Pikmin. The Pikmin was not visibly harmed, which is consistent with the successful mutation guard, but the Dog should not have selected/attacked it at all. The same encounter contains native Mouth Dog `Heard noise!` / `targetPos` diagnostics. Those diagnostics are investigation evidence, not yet a proved root cause.

The same run also did not positively prove that follower Pikmin could still attack/latch the Mouth Dog and complete native death/unlatch/task cleanup. Do not infer breakage solely from the non-event; this remains a targeted validation question.

## Exact next action

Perform **targeted repository-native analysis** of the remaining Mouth Dog targeting/attack path:

1. start from `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md` and `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`;
2. inspect exact current source/runtime ownership for the native Mouth Dog target/noise/attack path outside `MouthDogPikminEnemy.DoCheckInterval()`;
3. explicitly test the hypothesis that a scrap-carrying Pikmin or carried scrap noise/threat representation can attract the Dog, but do not assume it without source evidence;
4. determine whether the intended native Pikmin -> Mouth Dog combat/latch path is still present and what exact method/adapter owns it;
5. preserve Mouth Dog -> player attacks and the enabled `MouthDogPikminEnemy` adapter;
6. preserve the proven prevention-before-mutation concept from S1.42AG where valid;
7. do not add guessed fallback patches, broad EnemyAI scanning, manual Pikmin state reconstruction, or whole-component disable;
8. do not arm or build a successor until the exact remaining owner/method boundary is proved and reviewed under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

No new gameplay run is required at this point. The next step is source/runtime analysis, not another blind runtime retry.

## Interior findings / deferred LC Office scope

Current full-normal-stack runtime evidence proves that Wesley's `Art Gallery (MuseumInteriorFlow)` and `Rubber Rooms (RubberRoomsFlow)` both register successfully, are viable on Offense, and reach the final project-local normalized pool at effective rarity `100`. Their lack of observed natural player rolls is therefore not evidence of a bad spawn-weight configuration.

LC Office remains documented as a **deferred, not armed** integration scope in `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.

Planned package boundary only after the selected Mouth Dog compatibility scope is closed:

- `Piggy-LC_Office 2.3.4`;
- `MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix 2.0.0`;
- `JacobG5-DestroyItemInSlotFix 1.0.0`;
- `Alice-DungeonGenerationPlus 1.5.0 -> 1.5.1`;
- preserve `IAmBatby-LethalLevelLoader 1.7.12` as sole owner;
- explicitly forbid `pacoito-LethalLevelLoaderUpdated` from the final profile/export;
- preserve the accepted S1.42AB equal-effective-weight architecture;
- do not combine Wesley changes, DunGenReferenceFixer replacement, or universal LC Office moon forcing with the first compatibility candidate.

## Historical Microwave boundary

S1.42AD remains runtime-rejected because its frozen provider contract incorrectly required zero Interior curves and therefore failed closed without applying `0.5`. S1.42AE remains superseded for packaging/path-length reasons: its corrected provider code was never reached because the physically present SoundAPI binding sat at a 262-character path and BepInEx/Mono failed before chainloader startup. S1.42AF reused the corrected source under a short profile identity and is the accepted successor.

## Remaining open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Deferred items include LC Office V81 integration, CullFactory junkrooms/shatteredrooms exceptions, Mausoleum fog reduction, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair, broader LethalMin teardown/despawn repair where supported by stronger evidence, and any later LC Office universal-availability tuning after compatibility is proven.
