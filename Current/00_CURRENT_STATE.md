<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-06  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AC — BCMER EventType Equal Distribution — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Acceptance: `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AC/20260904T235720Z/`

## Latest built artifact

**S1.42AF — Path-Length-Safe Microwave Packaging — TARGETED RUNTIME GATE PASS ACCEPTANCE DEFERRED NOT REJECTED**

Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`  
Candidate record: `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **S1.42AF**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AF_RUNTIME_GATE_PASS_MOUTH_DOG_ANALYSIS_SELECTED`)
- Guarded build base: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z` / `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`

## Exact next action

Investigate the Mouth Dog / Eyeless Dog -> Pikmin compatibility gap documented in Current/129_MOUTH_DOG_PIKMIN_BASELINE_COMPATIBILITY_GAP_NEXT_ANALYSIS.md. Inspect LethalMin 1.1.108 configuration first for a native one-way noninteraction contract. If configuration cannot fully prevent Dog -> Pikmin bite/grab while preserving Pikmin -> Dog combat, prove the exact LethalMin Mouth-Dog adapter/bite/grab ownership path and design the smallest prevention-before-mutation extension to Patches/S139CompatibilityFixes/Plugin.cs under Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md. Do not rerun S1.42AF merely for its completed Microwave gate, and do not name or arm a successor until the owner/method contract and isolated build plan are proven.

No new runtime test is pending. A completed run may still require its build-specific PowerShell uploader before evidence ingestion; `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
