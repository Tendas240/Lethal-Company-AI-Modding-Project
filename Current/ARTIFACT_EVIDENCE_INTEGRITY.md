<!-- LIVE_STATE: accepted=S1.42AF latest=S1.42AH candidate=S1.42AH runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-08

## Current accepted profile: S1.42AF

Artifact: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`  
Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`

S1.42AF remains the sole accepted gameplay base.

## Active runtime candidate: S1.42AH

- Status: **ACTIVE_RUNTIME_CANDIDATE_PENDING / EXTENDED PARTIAL RUNTIME PASS / NOT ACCEPTED**
- Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
- Profile SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`
- Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`
- Latest partial decision: `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md`
- Latest evidence: `RuntimeEvidence/S1.42AH/20260908T174352Z/`
- Latest log SHA-256: `6fca32623eb350c53b4f81c98ea3ef1218dee9a4256a4bb70a8950f1b3ab06a6`
- Prior partial decision: `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md`
- Prior evidence: `RuntimeEvidence/S1.42AH/20260908T162411Z/`
- Prior log SHA-256: `1778ad5b572349cda261b3b848e0a697dfdb527a1e4be4ab72624a88f9c51ef3`

The first run proves installation/collision/player coverage. The second run proves explicit native Pikmin -> MouthDog attack/death/cleanup, corpse carry, live adapter prevention, preserved noise response and clean known regression markers. The only remaining runtime gate is the deliberately unexercised MouthDog/Paw -> non-Pikmin `EnemyAI` / native `BiteKillEnemyAI` pass-through.

Two indexed logs do not imply acceptance. S1.42AH remains in `pending_profiles` until an explicit final runtime decision.

## Rejected predecessor

S1.42AG remains `RUNTIME_REJECTED_PARTIAL_FIX` and must not be used as a gameplay/build base.

## DLL provenance

The S1.42AH cumulative `S139CompatibilityFixes.dll` SHA remains candidate provenance until explicit acceptance. Accepted historical DLL provenance is unchanged.

## Retrieval invariant

No future decision may depend only on opaque `.r2z`, DLL or giant-log bytes. A reasoning-critical fact must also exist in readable indexed evidence. For a pending candidate with multiple partial runs, the latest INDEX/log SHA/partial record is the current progress pointer while prior runs remain preserved evidence.