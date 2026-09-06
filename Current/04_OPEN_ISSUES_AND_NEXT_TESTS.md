# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-06

## Current gameplay state

Accepted baseline is **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, `Profiles/LC V1 S1.42AF Microwave Fix.r2z`, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact is **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED / PARTIAL FIX / NOT ACCEPTED**, `Profiles/LC V1 S1.42AG Mouth Dog Fix.r2z`, SHA-256 `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`.

There is no active candidate. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AG` remains evidence-attribution only. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_MOUTHDOG_SOURCE_BOUNDARIES_AWAITING_PATCH_SAFETY_REVIEW`, guarding accepted S1.42AF. No successor is armed and no runtime test is pending.

## Closed S1.42AG runtime gate

S1.42AG proved a narrow useful prevention result on exact `LethalMin.MouthDogPikminEnemy.DoCheckInterval()`:

- intended Priority.First guard armed and executed;
- prior `Biting N Pikmin` / `EnemyAttackMouth` / 2.5-second grab/death-timer mutation signature disappeared;
- `Work state with no task assigned!` fell from 707 in the S1.42AF exposure evidence to 0;
- inherited S1.42AF behavior remained otherwise healthy in the tested run.

S1.42AG remains rejected because a Mouth Dog still visibly pursued/attacked a scrap-carrying Purple Pikmin through a path outside that adapter dispatcher.

Reverse-direction Pikmin -> Mouth Dog combat was not deliberately tested.

## Closed source-proof gates

Current source-boundary authority is `Current/137_MOUTHDOG_SOURCE_BOUNDARY_CLOSURE_AND_PRE_SUCCESSOR_SAFETY_STATE.md`.

The required proofs are now complete:

1. Vanilla V81 `MouthDogAI.DetectNoise(...)` is position-based and native pursuit can lunge near `noisePositionGuess`.
2. Vanilla V81 `MouthDogAI.OnCollideWithEnemy(Collider, EnemyAI)` is an independent generic enemy collision/lunge/damage surface.
3. Exact LethalMin proves `PikminAI : EnemyAI`.
4. Exact V81 `EnemyAI.OnCollideWithEnemy()` is debug-only and has no gameplay/lifecycle mutation.
5. Exact LethalMin `PikminItem.CarryNumerator()` repeatedly calls `PlayAudioOnLocalClient("ItemCarry", ...)` for each carrier; with `Dont Make Audible Noises = false`, Pikmin audio can emit audible noise at the carrier's position.

The stronger GoldBar-specific semantic-target hypothesis is unsupported/rejected. The source does not prove which exact audible event caused the observed S1.42AG pursuit.

No additional local source capture is currently required.

## Exact next action

Perform the **successor-specific Patch Safety Review** under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`.

The review must define the smallest exact Harmony boundary and document:

- exact owner/type/method/signature and Pikmin identification;
- base/inheritance/lifecycle responsibilities;
- whether the proven S1.42AG `DoCheckInterval()` guard remains part of the successor;
- preservation of MouthDog -> player behavior;
- preservation of native Pikmin -> MouthDog attack/latch/death/unlatch/task ownership;
- one-variable build delta against accepted S1.42AF;
- build diagnostics and archive-diff checks;
- runtime target/adjacent/repetition/neighbor/log checks;
- deliberate reverse-direction Pikmin -> MouthDog validation.

Do not arm/build a successor or start a runtime test until this review is complete.

## Currently irrelevant actions

- Do not repeat either completed Vanilla capture merely to reproduce evidence.
- Do not ask for `Assembly-CSharp.dll`, full decompiles, `-AssemblyPath`, manual .NET/ILSpy installation or a user-side repository clone for the closed source boundaries.
- Do not repeat the S1.42AG gameplay run or request another S1.42AG log upload.

## Deferred independent scopes

Route scope decisions through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`. Deferred items remain LC Office V81 integration, CullFactory `junkrooms`/`shatteredrooms` exceptions, Mausoleum fog reduction, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair and broader LethalMin teardown/despawn repair only with stronger evidence.
