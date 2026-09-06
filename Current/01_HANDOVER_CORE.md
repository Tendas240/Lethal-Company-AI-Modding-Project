<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Current-chat handover procedure:** `Current/HANDOVER_PREPARATION_PROMPT.md`  
**Last-Validated:** 2026-09-06

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

Accepted: **S1.42AF — Path-Length-Safe Microwave Packaging**, SHA-256 `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`.  
Latest built: **S1.42AG — Mouth Dog Pikmin One-Way Protection**, SHA-256 `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`, status **RUNTIME REJECTED PARTIAL FIX**.  
Active candidate: **none**. Runtime test: **none pending**. Successor: **not armed**.

Exact next action: Complete the successor-specific Mouth Dog Patch Safety Review under Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md using the now-closed source boundaries. Exact Vanilla V81 EnemyAI.OnCollideWithEnemy() is proven debug-only with no gameplay/lifecycle mutation. Exact LethalMin 1.1.108 PikminItem.CarryNumerator() repeatedly plays ItemCarry through each carrying Pikmin, and with Dont Make Audible Noises=false those Pikmin sounds can emit audible noise at the carrier position. Keep S1.42AF as the accepted base and S1.42AG as the rejected partial fix. Define the smallest exact Harmony boundary, preserve Mouth Dog -> player and native Pikmin -> Mouth Dog lifecycle, and specify one-variable build/runtime regression gates including deliberate reverse-direction validation. Do not arm/build a successor or start a runtime test until the safety review is complete.

## Mandatory runtime-test UX

Whenever a future runtime test becomes outstanding, the response that explains what to test must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific one-line PowerShell log uploader in the same response. If a run is already complete but its log is not yet ingested, provide the uploader for the runtime-active build without requiring another test run.

## Historical authority warning

Old final handovers, audits, candidate notes, rejection records, `Current/02_TECHNICAL_BASELINE.md`, and the old progress blocks in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are retained history. They do not override the current-state/topic graph or a later explicit acceptance decision. See `Current/DOCUMENT_AUTHORITY.md` and `Current/REPOSITORY_MIGRATION_MANIFEST.md`.

## Recovery

Verified pre-overhaul repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`  
Manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`
