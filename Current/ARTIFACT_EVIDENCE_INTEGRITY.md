<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AH candidate=none runtime_test_outstanding=false -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-09

## Current accepted profile: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Compatibility DLL SHA-256: `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Final decisive evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`  
Final raw-log SHA-256: `ae57fb71a38952936e9056150240e2eaa70be9d89253b15644b3f5d35dd09729`

S1.42AH is the accepted full-normal-stack gameplay base and latest built artifact. There is no active runtime candidate and no runtime test outstanding.

## Preserved S1.42AH evidence chain

- Candidate: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`.
- First partial decision/evidence: `Current/140_S1.42AH_RUNTIME_PARTIAL_VALIDATION_MOUTHDOG_COLLISION_PLAYER.md` / `RuntimeEvidence/S1.42AH/20260908T162411Z/`, raw-log SHA-256 `1778ad5b572349cda261b3b848e0a697dfdb527a1e4be4ab72624a88f9c51ef3`.
- Second partial decision/evidence: `Current/141_S1.42AH_RUNTIME_PARTIAL_VALIDATION_REVERSE_DIRECTION_ADAPTER.md` / `RuntimeEvidence/S1.42AH/20260908T174352Z/`, raw-log SHA-256 `6fca32623eb350c53b4f81c98ea3ef1218dee9a4256a4bb70a8950f1b3ab06a6`.
- Final acceptance/evidence: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md` / `RuntimeEvidence/S1.42AH/20260909T162513Z/`, raw-log SHA-256 `ae57fb71a38952936e9056150240e2eaa70be9d89253b15644b3f5d35dd09729`.

The final decision uses only the last gameplay run of the final uploaded log, per user instruction. That last run contains MouthDogs and a Redwood Titan followed by normal Redwood Titan death. The log does not encode the attacker identity on the Titan death line; the explicit acceptance record preserves the exact evidence boundary.

## Accepted predecessor / rejected predecessor

S1.42AF remains an accepted historical predecessor and rollback/provenance point.

S1.42AG remains `RUNTIME_REJECTED_PARTIAL_FIX` and must not be used as a gameplay/build base.

## DLL provenance

The S1.42AH cumulative `S139CompatibilityFixes.dll` SHA-256 `bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573` is now accepted binary provenance for the current gameplay baseline. Its exact source remains `Patches/S139CompatibilityFixes/Plugin.cs`.

## Retrieval invariant

No future decision may depend only on opaque `.r2z`, DLL or giant-log bytes. A reasoning-critical fact must also exist in readable `ProfileSources`, `FILE_INDEX`, runtime `INDEX`/analysis, source, build record, or canonical documentation. Completed runtime decisions retain exact evidence paths and SHA-256 provenance; historical partial runs remain preserved when they prove distinct parts of an accepted contract.