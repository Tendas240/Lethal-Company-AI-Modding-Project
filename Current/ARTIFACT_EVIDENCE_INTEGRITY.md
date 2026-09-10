<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`
**Last-Validated:** 2026-09-10

## Accepted gameplay baseline: S1.42AH

Artifact: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`
Final decisive evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

S1.42AH remains the accepted full-normal-stack gameplay base while the independent ShyGuy correction is runtime-validated.

## Latest built artifact / active runtime candidate: S1.42AI

Artifact: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`
Candidate record: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`
Project status: `Current/Projektstatus_S1.42AI_CANDIDATE.json`
Build plan: `BuildSpecs/S1.42AI_PLAN.md`
Static evidence: `BuildSpecs/S1.42AI_BUILD_EVIDENCE/STATIC_VERIFICATION.md`
Readable snapshot: `ProfileSources/S1.42AI/`

S1.42AI is build-pass and static-delta-verified. Runtime validation is outstanding, so it is indexed in `pending_profiles` with `runtime_evidence_required=false` until a final explicit acceptance or rejection decision exists.

The exact static delta from S1.42AH changes only `export.r2x` and `BepInEx/config/BrutalCompanyMinusExtraReborn/ModdedEvents.cfg`; the semantic config change is exactly the three `[ShyGuy]` exterior values set to zero. Every other archive member is byte-identical to S1.42AH, including `Scopophobia.cfg`.

## Preserved accepted/rejected evidence chain

S1.42AH retains its three-stage runtime evidence chain and remains the accepted baseline. S1.42AF remains an accepted historical predecessor/rollback point. S1.42AG remains `RUNTIME_REJECTED_PARTIAL_FIX` and is not a gameplay/build base.

## Retrieval invariant

No future decision may depend only on opaque `.r2z`, DLL or giant-log bytes. A reasoning-critical fact must also exist in readable `ProfileSources`, `FILE_INDEX`, runtime `INDEX`/analysis, source, build record, or canonical documentation. The pending S1.42AI entry deliberately contains no runtime-log claim before the user performs the authorized runtime gate.
