<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-05  
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

**S1.42AE — Functional Microwave Provider Contract Correction — BUILD PASS GAMEPLAY RUNTIME VALIDATION OPEN NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AE Functional Microwave Provider Contract Correction.r2z`  
SHA-256: `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`  
Candidate record: `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **S1.42AE**
- Runtime test outstanding: **yes**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AE_BUILD_AWAITING_RUNTIME_VALIDATION`)
- Guarded build base: `Profiles/LC V1 S1.42AE Functional Microwave Provider Contract Correction.r2z` / `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AE`

## Exact next action

After the v2.4 Gale import-proof repair is merged and CI is green, re-import the same S1.42AE artifact with RuntimeTools/ReplaceActiveGaleProfileV24.ps1. Do not start the game unless revision 2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof successfully decodes non-empty export.r2x text, derives and lists exactly two SoundAPI critical materialization contracts, and verifies exactly one non-empty base SoundAPI DLL plus one non-empty LethalCompany binding DLL inside their respective Gale package roots. Then play one normal gameplay run far enough for normal moon/interior generation and upload the complete fresh LogOutput.log with the exact S1.42AE uploader from Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md. Evaluate dependency validation, PrioritiseMoons=true MoonCurves=18 InteriorCurves=18, both keyset markers, the final 18 Moon curves x0.5 / Interior validation-only marker, and project-critical regression markers before accepting or rejecting S1.42AE. Do not build a successor before this runtime evidence is evaluated.

A runtime test is pending for S1.42AE. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
