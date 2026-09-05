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

Latest built artifact: **S1.42AF — Path-Length-Safe Microwave Packaging — BUILD PASS RUNTIME VALIDATION OPEN NOT ACCEPTED**  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`

Active candidate: **S1.42AF**. Runtime test outstanding: **yes**. Build successor armed: **no**.

Exact next action: Import S1.42AF with RuntimeTools/ReplaceActiveGaleProfileV24.ps1. Proceed only after v2.4 positively verifies non-empty export.r2x plus exactly one non-empty base SoundAPI DLL and one non-empty LethalCompany binding DLL. Confirm the shortened nested binding path is below the legacy 260-character boundary, then start Lethal Company, require preloader/main-menu success, play one normal run far enough for ordinary moon/interior generation, and upload the complete fresh S1.42AF LogOutput.log with the exact uploader in Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md. Evaluate the preserved S1.42AE plugin markers, dependency versions, PrioritiseMoons=true MoonCurves=18 InteriorCurves=18, both keysets, the 18 Moon curves x0.5 / 18 Interior validation-only marker, and regression/fatal markers before accepting or rejecting S1.42AF.

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
