# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-06

## Current gameplay state

Accepted baseline is **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`. Fresh acceptance evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`.

Latest built artifact and active runtime candidate is **S1.42AG — Mouth Dog Pikmin One-Way Protection — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**, `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`, SHA-256 `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`. Candidate authority: `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG`. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AG_BUILD_AWAITING_RUNTIME_VALIDATION`. No successor beyond S1.42AG is armed.

## Current open runtime gate

S1.42AG exists to prevent only Mouth Dog / Eyeless Dog -> Pikmin target/bite/grab behavior before harmful state mutation while preserving the enabled LethalMin adapter, native Pikmin -> Mouth Dog combat/lifecycle and Mouth Dog -> player behavior.

The S1.42AF acceptance run had exposed the inherited compatibility gap: `Biting 2 Pikmin`, attachment to `EnemyAttackMouth`, 2.5-second death timers, and then 707 `Work state with no task assigned!` warnings from the affected White Pikmin. S1.42AG implements the exact prevention patch selected after source-contract analysis and safety review.

## Exact next action

Perform the outstanding **full-normal-stack S1.42AG runtime test** according to `Current/133_S1.42AG_BUILD_CANDIDATE_MOUTHDOG_PIKMIN_ONE_WAY_PROTECTION.md`:

1. import the exact S1.42AG profile with the canonical Gale v2.4 replacement helper;
2. exercise repeated real Mouth Dog lunge opportunities with Pikmin nearby;
3. prove no Mouth Dog -> Pikmin bite/grab/`EnemyAttackMouth`/2.5-second death-timer path occurs;
4. prove Pikmin can still attack/latch the Dog and native death/unlatch/task cleanup works;
5. prove the Mouth Dog still attacks players normally;
6. confirm normal startup, lobby, moon/interior generation and inherited S1.42AF Functional Microwave health;
7. upload the complete fresh S1.42AG `LogOutput.log` with the build-specific uploader from `Current/133...`;
8. only then decide S1.42AG acceptance or rejection/targeted analysis.

A clean startup without exercising the interaction is not acceptance. Do not build a successor before this gate closes.

## Interior findings / deferred LC Office scope

Current full-normal-stack runtime evidence proves that Wesley's `Art Gallery (MuseumInteriorFlow)` and `Rubber Rooms (RubberRoomsFlow)` both register successfully, are viable on Offense, and reach the final project-local normalized pool at effective rarity `100`. Their lack of observed natural player rolls is therefore not evidence of a bad spawn-weight configuration.

LC Office is now documented as a **deferred, not armed** integration scope in `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.

Planned package boundary after the active S1.42AG lifecycle closes:

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
