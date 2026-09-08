<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-08

## Current gameplay state

Accepted baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact / active runtime candidate: **S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**, SHA-256 `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.

Runtime test outstanding: **yes**. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`. No successor beyond S1.42AH is armed.

## Closed predecessor/source/safety gates

- S1.42AG is runtime-rejected historical evidence only. Its exact `DoCheckInterval()` guard removed the LethalMin bite/grab/death-timer mutation path but did not close the remaining Vanilla MouthDog collision path.
- Vanilla MouthDog and base EnemyAI collision source boundaries are captured and integrated.
- `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md` passed and is already implemented by S1.42AH.
- No additional local source capture or repeat Patch Safety Review is required unless new evidence invalidates the exact contract.

## Exact next test

Perform the **S1.42AH full-normal runtime gate** from `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`.

Required coverage:

1. Provoke real MouthDog/Pikmin collision repeatedly and require the bounded Vanilla collision-block marker.
2. Require no Dog -> Pikmin LethalMin adapter bite/grab/death-timer mutation (`Biting N Pikmin`, `EnemyAttackMouth`, 2.5-second `GrabPikmin`, Dog-path Pikmin `HitEnemy(2)`).
3. Explicitly command/throw Pikmin onto a MouthDog; passive followers do not count.
4. Prove native Pikmin latch/attack, MouthDog death, death-triggered unlatch, attack-task finish and follow/idle cleanup.
5. Prove MouthDog -> player remains functional.
6. Verify non-Pikmin neighboring `EnemyAI` collisions remain unfiltered.
7. Preserve ordinary position-based audible-noise response; movement toward a Pikmin world position alone is not failure.
8. Upload the complete fresh S1.42AH `LogOutput.log` with the build-specific uploader in Current/139.

Do not accept S1.42AH from startup/build success alone.

## Currently irrelevant actions

- Do not repeat the completed Vanilla source captures.
- Do not request another S1.42AG runtime run/log.
- Do not repeat the Patch Safety Review without new contradicting source evidence.
- Do not rebuild S1.42AH or arm another gameplay build while this runtime gate is unresolved.

## Deferred independent scopes

Route through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`: LC Office V81 integration, CullFactory `junkrooms`/`shatteredrooms` exceptions, Mausoleum fog reduction, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair, and broader LethalMin teardown/despawn work only with stronger evidence.
