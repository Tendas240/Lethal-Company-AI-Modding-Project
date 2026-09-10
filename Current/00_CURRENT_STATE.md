<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-10  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

## Latest built artifact

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — BUILD PASS STATIC DELTA VERIFIED RUNTIME VALIDATION OUTSTANDING**

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Candidate record: `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **S1.42AI**
- Runtime test outstanding: **yes**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AI_BUILD_AWAITING_RUNTIME_VALIDATION`)
- Guarded build base: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z` / `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI`

## Exact next action

Import S1.42AI with the canonical Gale v2.4 replacement helper and run the full-normal BCMER ShyGuy runtime gate from Current/143. Positively obtain or force the BCMER ShyGuy event, confirm ShyGuy remains available through the intended interior event path, verify that BCMER adds no ShyGuy to the exterior path and that no 'ShyGuy(Clone) spawned outside; Switching to exterior AI' marker occurs from that event, then upload the complete fresh S1.42AI LogOutput.log with the build-specific uploader in Current/143. Do not accept S1.42AI from static/build success alone.

A runtime test is pending for S1.42AI. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
