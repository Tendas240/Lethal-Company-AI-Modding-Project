<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/134_S1.42AG_RUNTIME_REJECTION_REMAINING_MOUTHDOG_TARGETING_PATH.md`, `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`, `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`, `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`, `RuntimeEvidence/S1.42AH/20260908T162411Z/`, `RuntimeEvidence/S1.42AH/20260908T174352Z/`  
**Last-Validated:** 2026-09-08

## Accepted baseline

**S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`  
Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`

S1.42AF remains the only accepted gameplay base.

## Latest built artifact / active candidate

**S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS / EXTENDED PARTIAL RUNTIME PASS / FINAL NON-PIKMIN NEIGHBOR REMAINDER OUTSTANDING / NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`  
Latest partial decision: `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`  
Latest runtime evidence: `RuntimeEvidence/S1.42AH/20260908T174352Z/`  
Latest runtime log SHA-256: `6fca32623eb350c53b4f81c98ea3ef1218dee9a4256a4bb70a8950f1b3ab06a6`

The first run in `Current/140` already proved patch installation, repeated live Vanilla MouthDog -> Pikmin collision blocking, and MouthDog -> player preservation. The second targeted run in `Current/141` additionally proves explicit thrown Pikmin -> MouthDog latch/`AttackEnemy`/damage, MouthDog death through that combat path, native idle/task-removal/unlatch cleanup, corpse-carry transition, live adapter prevention before bite/grab mutation, preserved ordinary audible-noise response, and zero known project regression markers.

These are positive partial-runtime observations, not an implicit promotion. S1.42AH remains neither accepted nor rejected.

## Final runtime remainder

Only the adjacent non-Pikmin contract remains:

1. deliberately exercise MouthDog/Paw against a **non-Pikmin `EnemyAI`**;
2. positively prove native Paw-initiated `BiteKillEnemyAI` / generic non-Pikmin `OnCollideWithEnemy` behavior still runs;
3. confirm the Pikmin-only prefix does not filter that path;
4. upload the complete fresh S1.42AH `LogOutput.log`.

Do not repeat already-proven Pikmin -> MouthDog attack/death/unlatch/task-cleanup, adapter protection, startup/patch-install, Vanilla Pikmin collision-block or player-maul coverage merely to obtain this final neighboring-path evidence.

## Controllers and decision boundary

- `BuildSpecs/current.json` is disabled: `IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`.
- No successor beyond S1.42AH is armed.

If the final neighbor check passes, explicitly accept S1.42AH. If it fails, explicitly reject S1.42AH and return to an S1.42AF-derived follow-up. Do not rebuild S1.42AH before this decision.

## Canonical Gale workflow

Use `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` as governed by `Knowledge/GALE_PROFILE_WORKFLOW.md`. Whenever the remaining runtime test is explained to the user, include both the Gale replacement/import one-liner and the exact S1.42AH build-specific log uploader in the same response.