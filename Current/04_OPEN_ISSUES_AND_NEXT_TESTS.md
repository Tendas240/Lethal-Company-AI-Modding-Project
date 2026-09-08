<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Authority:** concise current work queue only  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-08

## Current gameplay state

Accepted baseline: **S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Latest built artifact / active runtime candidate: **S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / PARTIAL RUNTIME PASS / TARGETED REMAINDER OUTSTANDING / NOT ACCEPTED**, SHA-256 `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.

Runtime test outstanding: **yes**. S1.42AH is neither accepted nor rejected. `BuildSpecs/current.json` is disabled with controller id `IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`. No successor beyond S1.42AH is armed.

## First S1.42AH runtime run — already closed

`Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md` records the first ingested S1.42AH run at `RuntimeEvidence/S1.42AH/20260908T162411Z/`; authoritative raw-log SHA-256 is in its `INDEX.json` and groups as `1778ad5b 572349cd a261b3b8 48e0a697 dfdb527a 1e4be4ab 72624a88 f9c51ef3`.

Already positively evidenced:

- adapter-side `EatPikmin` / `HandleEnemyBite` patches install;
- the project-local Vanilla MouthDog collision prefix installs;
- real Vanilla MouthDog -> Pikmin collision handling is blocked repeatedly in live gameplay;
- MouthDog -> player attack remains functional in the exercised interval, including a real `Mauling` player death.

Do not repeat those checks merely because the remaining reverse-direction gate is open.

## Closed predecessor/source/safety gates

- S1.42AG is runtime-rejected historical evidence only. Its exact `DoCheckInterval()` guard removed the LethalMin bite/grab/death-timer mutation path but did not close the remaining Vanilla MouthDog collision path.
- Vanilla MouthDog and base EnemyAI collision source boundaries are captured and integrated.
- `Current/138_MOUTHDOG_SUCCESSOR_PATCH_SAFETY_REVIEW_PASS.md` passed and is already implemented by S1.42AH.
- No additional local source capture or repeat Patch Safety Review is required unless new evidence invalidates the exact contract.

## Exact next test

Perform only the **targeted S1.42AH runtime remainder** from `Current/140`.

Required remaining coverage:

1. Explicitly command/throw Pikmin onto a MouthDog; passive followers do not count.
2. Prove native Pikmin -> MouthDog latch/attack/damage remains functional.
3. Prove MouthDog death through the Pikmin attack path, death-triggered unlatch/release, attack-task finish and follow/idle cleanup.
4. Exercise the adapter-side MouthDog bite-protection path itself and require no Paw/Pikmin bite/grab/death-timer mutation (`Biting N Pikmin`, `EnemyAttackMouth`, 2.5-second `GrabPikmin`, Dog-path Pikmin `HitEnemy(2)`).
5. Preserve Paw-initiated `BiteKillEnemyAI` behavior.
6. Verify non-Pikmin neighboring `EnemyAI` collisions remain unfiltered and combat/UI membership invariants remain sane.
7. Re-check known project regression markers around the reverse-direction/death-cleanup sequence.
8. Preserve ordinary position-based audible-noise response; movement toward a Pikmin world position alone is not failure evidence.
9. Upload the complete fresh S1.42AH `LogOutput.log` with the build-specific uploader in Current/139 after this targeted run.

The first run's `Enemy Not Hit By Pikmin. Reason: [Invalid Enemy States]` / `Not hitting MouthDog` messages do not satisfy the reverse-direction gate and, without the required explicit attack conditions, do not by themselves establish a candidate defect.

If all remaining required checks pass, accept S1.42AH explicitly. If any targeted required check fails, reject it explicitly and return to an S1.42AF-derived follow-up.

## Currently irrelevant actions

- Do not repeat the completed Vanilla source captures.
- Do not request another S1.42AG runtime run/log.
- Do not repeat the Patch Safety Review without new contradicting source evidence.
- Do not rebuild S1.42AH or arm another gameplay build while this runtime gate is unresolved.
- Do not repeat already-proven S1.42AH startup/patch-install, Vanilla collision-block or player-maul coverage solely to obtain the missing reverse-direction evidence.

## Deferred independent scopes

Route through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`: LC Office V81 integration, CullFactory `junkrooms`/`shatteredrooms` exceptions, Mausoleum fog reduction, Black Mesa/Pikmin routing, isolated LethalEscapeUpdated evaluation, final long full-stack acceptance, evidence-driven AdditionalNetworking repair, and broader LethalMin teardown/despawn work only with stronger evidence.
