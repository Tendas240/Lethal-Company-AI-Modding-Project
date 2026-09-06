# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-06

## Current gameplay state

Accepted baseline is **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact is **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**, `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`, SHA-256 `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`.

There is no active runtime candidate. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains only the last evidence-attribution target. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_MOUTHDOG_V81_CAPTURE_AWAITING_TARGETED_SOURCE_EXTENSION` and guards accepted S1.42AF. No successor is armed.

## Closed S1.42AG runtime gate

S1.42AG proved a narrow partial fix:

- exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()` was patched with the intended `Priority.First` prevention-only prefix;
- the guard executed during the encounter;
- the harmful LethalMin `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab/death-timer state-mutation path was absent;
- `Work state with no task assigned!` count was `0`, compared with 707 in the S1.42AF exposure evidence;
- the inherited S1.42AF Functional Microwave contract remained healthy.

S1.42AG remains rejected because the full one-way interaction contract failed: a Mouth Dog visibly pursued/attacked a scrap-carrying Purple Pikmin through a path outside the blocked LethalMin dispatcher.

Reverse-direction Pikmin -> Mouth Dog combat was not deliberately exercised. Passive follower Pikmin remaining non-aggressive is expected and is not a failure signal.

## Closed source-capture gate

The hardened `AnalysisTools/InspectMouthDogV81.ps1` capture has now succeeded. Do not repeat it merely because previous handover text said `AWAITING_RETRY`.

Authoritative provenance:

- branch `source-evidence/mouthdog-v81-20260906t121738z`;
- commit `a618b19bfc30234ca556c924d681d43b2c13d1d9`;
- capture base `3049b0fa52af79db39efb075d94684d229eed3c6`;
- assembly SHA-256 `5f7db5538b78dc408845a3002907619785ac9f9c6b6059d13dc9a602d9b65731`;
- Steam buildid `22825947`;
- current analysis: `Current/136_MOUTHDOG_V81_SOURCE_CAPTURE_AND_NATIVE_PATH_ANALYSIS.md`;
- evidence root: `SourceEvidence/VanillaV81/MouthDogAI/20260906T121738Z/`.

The old Windows bootstrap/postprocessing record `Current/135_MOUTHDOG_V81_SOURCE_CAPTURE_TOOL_WINDOWS_HARDENING_STATE.md` is resolved historical implementation evidence.

## Proven native boundary so far

The V81 source proves:

- `MouthDogAI.DetectNoise(...)` consumes a world-space noise position;
- `noisePositionGuess` drives native pursuit and can trigger `EnterLunge()` once the Dog is within less than 4 units;
- `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` is a separate generic enemy-collision path which calls the base method, can lunge toward a different enemy in chase state, and calls `collidedEnemy.HitEnemy(2, ...)`;
- exact LethalMin 1.1.108 evidence proves `PikminAI : EnemyAI`, so Pikmin can enter that generic native collision path;
- exact LethalMin evidence proves Pikmin audio can emit `RoundManager.PlayAudibleNoise(...)` at the Pikmin position;
- current config has `Dont Make Audible Noises = false`.

Runtime evidence proves a Purple Pikmin carried `GoldBar(Clone)`. It does **not** yet prove that the carried GoldBar itself was the causal noise emitter.

## Exact next action

Perform only the targeted source-evidence extension required to close the remaining pre-successor uncertainty:

1. inspect exact Vanilla V81 `EnemyAI.OnCollideWithEnemy()` base behavior and side effects;
2. inspect exact LethalMin 1.1.108 `PikminItem.CarryNumerator()` plus carry-item audio / `RoundManager.PlayAudibleNoise(...)` callsites;
3. use that evidence to prove or reject the narrower carried-GoldBar/noise hypothesis;
4. then apply `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and complete a successor-specific safety review.

No new gameplay run is required now. No build is armed. Do not patch guessed boundaries, return `false` from the MouthDog collision override before the base-method contract is understood, disable `MouthDogPikminEnemy`, add broad `EnemyAI` scanning, or manually reconstruct Pikmin state.

A future candidate's runtime gate must deliberately command/throw Pikmin onto the Mouth Dog to validate Pikmin -> Mouth Dog attack/latch/death-unlatch behavior. Passive follower non-aggression is not that test.

## Interior findings / deferred LC Office scope

Current full-normal-stack runtime evidence proves that Wesley's `Art Gallery (MuseumInteriorFlow)` and `Rubber Rooms (RubberRoomsFlow)` register successfully, are viable on Offense, and reach final project-local normalized rarity `100`. Their lack of observed natural rolls is not evidence of bad spawn-weight configuration.

LC Office remains deferred under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`. Preserve `IAmBatby-LethalLevelLoader 1.7.12` as sole LLL owner and keep the first Office compatibility candidate separate from Wesley changes, DunGenReferenceFixer replacement or universal moon forcing.

## Remaining open/deferred work

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Deferred items include LC Office V81 integration, CullFactory junkrooms/shatteredrooms exceptions, Mausoleum fog reduction, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair and broader LethalMin teardown/despawn repair only where stronger evidence supports it.
