<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# 04 — Open Issues and Next Tests

**Status:** CURRENT / LIVE WORK QUEUE  
**Machine state:** `Current/CURRENT_STATE.json`  
**Last-Validated:** 2026-09-08

## Current gameplay state

Accepted baseline: **S1.42AF — ACCEPTED FULL NORMAL STACK**, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.

Active/latest candidate: **S1.42AH — BUILD PASS / EXTENDED PARTIAL RUNTIME PASS / FINAL NON-PIKMIN NEIGHBOR REMAINDER OUTSTANDING / NOT ACCEPTED**, SHA-256 `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`.

Runtime test outstanding: **yes**. Build controller remains disabled; `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`; no successor is armed.

## Runtime coverage already closed

First run (`Current/140`, `RuntimeEvidence/S1.42AH/20260908T162411Z/`): patch installation, repeated Vanilla MouthDog -> Pikmin collision blocking, MouthDog -> player preservation.

Second run (`Current/141`, `RuntimeEvidence/S1.42AH/20260908T174352Z/`, SHA-256 `6fca32623eb350c53b4f81c98ea3ef1218dee9a4256a4bb70a8950f1b3ab06a6`):

- explicitly thrown Pikmin latch, enter `AttackEnemy`, and damage the MouthDog;
- Pikmin combat kills the MouthDog;
- native idle/task removal/leader removal/unlatch cleanup succeeds;
- the corpse enters native Pikmin carry behavior;
- the adapter prevention executes live before bite/grab mutation with no known harmful adapter signature in the targeted interval;
- ordinary noise response remains present;
- known project regression markers remain zero.

## Exact next test

Perform only the final S1.42AH non-Pikmin neighbor remainder:

1. deliberately exercise MouthDog/Paw against a **non-Pikmin `EnemyAI`**;
2. positively exercise native Paw-initiated `BiteKillEnemyAI` / generic non-Pikmin `OnCollideWithEnemy` behavior;
3. confirm the Pikmin-only prefix does not filter that non-Pikmin path;
4. upload the complete fresh S1.42AH `LogOutput.log` using the build-specific uploader from `Current/139`.

Do not repeat already-proven startup, Pikmin collision blocking, player mauling, reverse-direction Pikmin attack/death/unlatch/task cleanup, or adapter-protection coverage merely to satisfy this final neighbor gate.

If it passes, explicitly accept S1.42AH. If it fails, explicitly reject S1.42AH and return to an S1.42AF-derived follow-up.

## Deferred independent scopes

Route through `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md` after the S1.42AH decision.