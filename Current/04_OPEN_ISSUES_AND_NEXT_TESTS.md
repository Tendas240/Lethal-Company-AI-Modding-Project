# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-06

## Current gameplay state

Accepted baseline is **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`. Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`. Fresh acceptance evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`.

S1.42AF passed the shortened-path packaging gate and the Functional Microwave runtime contract: the nested SoundAPI LethalCompany binding was present and non-empty at a 226-character path, normal BepInEx/game startup succeeded, CodeRebirth `1.6.9` and DawnLib/Dusk `0.9.25` were validated, and exactly 18 Moon/tag curves were scaled by `0.5` while 18 Interior curves remained validation-only.

There is **no active candidate**, **no runtime test outstanding**, and **no successor armed**. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF` remains the runtime-evidence attribution pointer. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AF_ACCEPTANCE_MOUTHDOG_ANALYSIS` and guards accepted S1.42AF as the base.

## Current open compatibility issue

The S1.42AF acceptance run also exposed a separate inherited Mouth Dog / Eyeless Dog -> Pikmin compatibility gap. Runtime evidence confirms `Biting 2 Pikmin`, attachment to `EnemyAttackMouth`, and 2.5-second death timers. Pikmin invincibility prevented the final kill but did not prevent grab/death-timer state mutation; the two affected White Pikmin then generated 707 `Work state with no task assigned!` warnings.

This is **not classified as an S1.42AF regression** because AF changed no LethalMin package/config state. It is tracked as a baseline-resident compatibility finding in `Current/129_MOUTHDOG_PIKMIN_BASELINE_COMPATIBILITY_FINDING.md` and `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`.

## Exact next action

Perform focused source/contract analysis before authorizing any successor build:

1. inspect the exact LethalMin MouthDog/EyelessDog owner, targeting/bite method, inheritance and native configuration surface;
2. determine whether native configuration can block Mouth Dog -> Pikmin targeting/bite/grab while preserving Pikmin -> Mouth Dog combat;
3. confirm whether the harmful path reaches exact `PikminAI.GrabPikmin(Transform,float,int)` before all harmful state mutation;
4. if a project-local patch is required, prefer the smallest prevention-before-mutation extension under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`;
5. preserve native Pikmin -> Mouth Dog behavior and define adjacent/repetition/lifecycle regression checks before arming a build.

No new runtime run or log upload is currently required.

## Historical Microwave boundary

S1.42AD remains runtime-rejected because its frozen provider contract incorrectly required zero Interior curves and therefore failed closed without applying `0.5`. S1.42AE remains superseded for packaging/path-length reasons: its corrected provider code was never reached because the physically present SoundAPI binding sat at a 262-character path and BepInEx/Mono failed before chainloader startup. S1.42AF reused the corrected source under a short profile identity and is the accepted successor.

## Remaining open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Deferred items remain CullFactory junkrooms/shatteredrooms exceptions, Mausoleum fog, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair, and broader LethalMin teardown/despawn repair where supported by stronger evidence.
