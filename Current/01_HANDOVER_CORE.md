<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Current-chat handover procedure:** `Current/HANDOVER_PREPARATION_PROMPT.md`  
**Last-Validated:** 2026-09-07

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
Latest built: **S1.42AH — Mouth Dog Pikmin Dual Prevention**, SHA-256 `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`, status **BUILD PASS RUNTIME VALIDATION OUTSTANDING**.  
Active candidate: **S1.42AH**. Runtime test: **pending**. Successor: **not armed**.

Exact next action: Import S1.42AH with the canonical Gale v2.4 replacement helper and run the full-normal MouthDog/Pikmin regression gate from Current/139. Deliberately provoke MouthDog/Pikmin collision, explicitly command/throw Pikmin onto the MouthDog for reverse-direction latch/attack/death/unlatch/task cleanup, verify MouthDog -> player and non-Pikmin neighbor behavior, repeat protected collisions, then upload the complete fresh S1.42AH LogOutput.log with the build-specific uploader in Current/139. Do not accept S1.42AH from build/startup success alone.

## Mandatory runtime-test UX

Whenever a future runtime test becomes outstanding, the response that explains what to test must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific one-line PowerShell log uploader in the same response. If a run is already complete but its log is not yet ingested, provide the uploader for the runtime-active build without requiring another test run.

## Historical authority warning

Old final handovers, audits, candidate notes, rejection records, `Current/02_TECHNICAL_BASELINE.md`, and the old progress blocks in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are retained history. They do not override the current-state/topic graph or a later explicit acceptance decision. See `Current/DOCUMENT_AUTHORITY.md` and `Current/REPOSITORY_MIGRATION_MANIFEST.md`.

## Recovery

Verified pre-overhaul repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`  
Manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`
