<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for **Lethal Company V81**.

## Fast takeover

Read, in order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
3. `Current/00_CURRENT_STATE.md`
4. `Current/PROJECT_KNOWLEDGE_MAP.md`

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`: execute one bounded segment, report the checkpoint, then stop and wait for explicit user continuation before the next non-final segment. Short atomic work may be one segment.

Then open only the topic/evidence needed for the user's question. Do not read the entire historical repository by default.

Machine-readable live state: `Current/CURRENT_STATE.json`.

Current-chat handover procedure: `Current/HANDOVER_PREPARATION_PROMPT.md`. Handover work is also continuation-gated by `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`.

## Current state

Accepted baseline: **S1.42AC — BCMER EventType Equal Distribution**  
Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`

Latest built artifact: **S1.42AE — Functional Microwave Provider Contract Correction — BUILD PASS GAMEPLAY RUNTIME VALIDATION OPEN NOT ACCEPTED**  
SHA-256: `d07d492b69a528e5af5e575719e88d9166c3f3a0b71ff1006d36e946304a98ee`

Active candidate: **S1.42AE**. Runtime test outstanding: **yes**. Build successor armed: **no**.

Exact next action: After the v2.4 Gale import-proof repair is merged and CI is green, re-import the same S1.42AE artifact with RuntimeTools/ReplaceActiveGaleProfileV24.ps1. Do not start the game unless revision 2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof successfully decodes non-empty export.r2x text, derives and lists exactly two SoundAPI critical materialization contracts, and verifies exactly one non-empty base SoundAPI DLL plus one non-empty LethalCompany binding DLL inside their respective Gale package roots. Then play one normal gameplay run far enough for normal moon/interior generation and upload the complete fresh LogOutput.log with the exact S1.42AE uploader from Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md. Evaluate dependency validation, PrioritiseMoons=true MoonCurves=18 InteriorCurves=18, both keyset markers, the final 18 Moon curves x0.5 / Interior validation-only marker, and project-critical regression markers before accepting or rejecting S1.42AE. Do not build a successor before this runtime evidence is evaluated.

## Semantic navigation

- ChatGPT segmented execution: `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
- Topic router: `Current/PROJECT_KNOWLEDGE_MAP.md` / `.json`
- Chat handover procedure: `Current/HANDOVER_PREPARATION_PROMPT.md`
- Build history: `Current/BUILD_LINEAGE.md` / `.json`
- Authority/history classification: `Current/DOCUMENT_AUTHORITY.md` / `.json`
- Artifact/runtime-evidence integrity: `Current/ARTIFACT_EVIDENCE_INTEGRITY.md` / `.json`
- Deferred work: `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
- Patch safety: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Historical handovers, candidate notes, rejection records and runtime decisions are preserved as evidence, but they do not override the current state/topic authority graph or a later explicit acceptance decision.

## Repository overhaul

Status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified pre-overhaul recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904` at frozen source commit `5dbd0e637a480d8591773e422bbca4b0654cad20`.  
Manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`.

No local repository clone or local profile build should be required from the user while repository-native artifacts and automation are sufficient.
