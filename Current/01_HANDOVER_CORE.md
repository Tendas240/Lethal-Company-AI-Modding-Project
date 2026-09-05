<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Current-chat handover procedure:** `Current/HANDOVER_PREPARATION_PROMPT.md`  
**Last-Validated:** 2026-09-05

## Fresh-session procedure

1. Read `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` and follow it for every project task.
2. Read `Current/00_CURRENT_STATE.md`.
3. Read `Current/PROJECT_KNOWLEDGE_MAP.md`.
4. Route the user's question to the registered semantic topic.
5. Open linked config/code/runtime/history only when needed.
6. Use `Current/BUILD_LINEAGE.md` for build-history questions and `Current/DOCUMENT_AUTHORITY.md` when an older file says "current".

For non-trivial work, execute one bounded segment per assistant turn, report the checkpoint, stop, and wait for explicit user continuation before the next segment. Short atomic work may be Segment 1/1; never create a knowingly inconsistent checkpoint.

Do not require a local repository clone or local profile build while repository-native artifacts and automation are sufficient.

## Future handover signal

When the user later requests transfer to another ChatGPT chat, execute `Current/HANDOVER_PREPARATION_PROMPT.md` under `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. That procedure verifies the then-current repository/CI/controller state and generates the new chat's start prompt from current authority; do not reuse an old static handover snapshot.

## Current anchors

Accepted: **S1.42AC — BCMER EventType Equal Distribution**, SHA-256 `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`.  
Latest built: **S1.42AF — Path-Length-Safe Microwave Packaging**, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`, status **BUILD PASS RUNTIME VALIDATION OPEN NOT ACCEPTED**.  
Active candidate: **S1.42AF**. Runtime test: **pending**. Successor: **not armed**.

Exact next action: Import S1.42AF with RuntimeTools/ReplaceActiveGaleProfileV24.ps1. Proceed only after v2.4 positively verifies non-empty export.r2x plus exactly one non-empty base SoundAPI DLL and one non-empty LethalCompany binding DLL. Confirm the shortened nested binding path is below the legacy 260-character boundary, then start Lethal Company, require preloader/main-menu success, play one normal run far enough for ordinary moon/interior generation, and upload the complete fresh S1.42AF LogOutput.log with the exact uploader in Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md. Evaluate the preserved S1.42AE plugin markers, dependency versions, PrioritiseMoons=true MoonCurves=18 InteriorCurves=18, both keysets, the 18 Moon curves x0.5 / 18 Interior validation-only marker, and regression/fatal markers before accepting or rejecting S1.42AF.

## Mandatory runtime-test UX

Whenever a future runtime test becomes outstanding, the response that explains what to test must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific one-line PowerShell log uploader in the same response. If a run is already complete but its log is not yet ingested, provide the uploader for the runtime-active build without requiring another test run.

## Historical authority warning

Old final handovers, audits, candidate notes, rejection records, `Current/02_TECHNICAL_BASELINE.md`, and the old progress blocks in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are retained history. They do not override the current-state/topic graph or a later explicit acceptance decision. See `Current/DOCUMENT_AUTHORITY.md` and `Current/REPOSITORY_MIGRATION_MANIFEST.md`.

## Recovery

Verified pre-overhaul repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`  
Manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`
