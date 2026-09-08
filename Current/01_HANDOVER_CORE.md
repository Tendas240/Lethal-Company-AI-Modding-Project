<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Project execution policy:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Current-chat handover procedure:** `Current/HANDOVER_PREPARATION_PROMPT.md`  
**Last-Validated:** 2026-09-08

## Fresh-session procedure

1. Read `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` and follow it for every project task.
2. Read `Current/CURRENT_STATE.json`.
3. Read `Current/PROJECT_KNOWLEDGE_MAP.md`.
4. Route the request to the registered canonical topic and open only linked evidence/config/code that is actually needed.

For non-trivial work, execute one bounded segment per assistant turn, report the checkpoint, stop, and wait for explicit user continuation before the next segment. Short atomic work may be Segment 1/1; never create a knowingly inconsistent checkpoint.

Use `Current/DOCUMENT_AUTHORITY.md` only when old/current wording conflicts, and `Current/BUILD_LINEAGE.md` only for build-history questions. Human-readable state is available in `Current/00_CURRENT_STATE.md` but does not need to be reread when `Current/CURRENT_STATE.json` already answers the task.

## Future handover signal

When the user later requests transfer to another ChatGPT chat, execute `Current/HANDOVER_PREPARATION_PROMPT.md` under `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. Verify then-current repository/CI/controller reality and generate the compact new-chat prompt from current authority; do not reuse an old static handover snapshot.

## Runtime-test UX

Whenever a runtime test is outstanding, the test instructions must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific one-line PowerShell log uploader. If a completed run still needs ingestion, provide the uploader for the runtime-active build without requiring another test run.

Do not require a local repository clone or local profile build while repository-native infrastructure is sufficient.
