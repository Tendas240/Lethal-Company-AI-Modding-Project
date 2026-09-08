# Current ChatGPT Handover Preparation Prompt

**Status:** CURRENT / CANONICAL HANDOVER PROCEDURE  
**Authority:** procedure the active ChatGPT chat must execute when the user requests transfer to a new ChatGPT chat  
**Canonical-For:** `chat_handover_preparation`, `fresh_new_chat_prompt_generation`  
**Execution cadence:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Machine State:** `Current/CURRENT_STATE.json`  
**Topic Router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-08

## Purpose

Use this workflow when the user explicitly asks to transfer the project to a new ChatGPT chat. The repository is the Source of Truth; do not reconstruct the handover from conversation memory or an old static handover snapshot.

This workflow deliberately does **not** hard-code the current accepted build, candidate, hashes, runtime gate, controller state or exact next action. Those volatile facts belong in `Current/CURRENT_STATE.json` and the canonical topic/evidence graph.

## Mandatory segmented execution

The handover is subject to `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`.

For non-trivial handover work, execute one bounded segment, report Completed / Findings / Remaining / Next segment, then stop, and wait for the user's explicit continuation signal before beginning the next non-final segment. A genuinely short atomic handover may be one segment. Do not split an atomic repository repair into a knowingly inconsistent checkpoint.

## Step 1 — Minimal authority read

Resolve the actual current state from `main`.

Read first:

1. `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
2. `Current/CURRENT_STATE.json`
3. `Current/PROJECT_KNOWLEDGE_MAP.md`
4. this file: `Current/HANDOVER_PREPARATION_PROMPT.md`

Then use the Topic Router to open only the canonical topic/evidence required by the current `selected_scope` / `next_action`. For lifecycle handovers this will normally include `Knowledge/CURRENT_LIFECYCLE.md`; other topics are read only when the router or exact task requires them.

Do not perform a manual full-repository audit by default. Do not reread `README.md`, `START_HERE_ChatGPT_Masterprompt.txt`, `Current/00_CURRENT_STATE.md`, `Current/01_HANDOVER_CORE.md`, both Knowledge Map mirrors, both Document Authority mirrors, Roadmap and integrity registries merely to restate the same live state.

Use these only when relevant:

- `Current/DOCUMENT_AUTHORITY.md/.json` for current-vs-history precedence;
- `Current/INTEGRITY_ERRATA_REGISTRY.json` for known bad/superseded values;
- `Current/BUILD_LINEAGE.md/.json` for build-history questions;
- `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Knowledge/GALE_PROFILE_WORKFLOW.md` for runtime import/upload semantics.

## Step 2 — Verify repository, CI and controllers

Before the final handover output, verify directly:

- current `main` HEAD;
- latest relevant `Knowledge Architecture` push run for that HEAD and whether every permanent gate passed;
- open relevant PRs;
- `BuildSpecs/current.json`;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- agreement of those controllers with `Current/CURRENT_STATE.json` and the routed lifecycle/topic authority;
- any hashes or evidence paths that are material to the exact next action.

`RuntimeInbox/ACTIVE_BUILD.txt` is runtime-active/evidence-attribution state, not acceptance authority. Do not claim CI proves runtime/gameplay behavior beyond documented validator coverage.

## Step 3 — Repair only genuine drift

If the repository is already internally consistent and a fresh chat can continue from the current authorities, do not create a cosmetic handover commit.

If genuine handover-critical drift exists:

1. preserve historical evidence;
2. repair the canonical current authority or validator contract instead of rewriting history;
3. do not change gameplay/config/profile/runtime behavior solely for handover cleanup;
4. use a dedicated branch and PR;
5. merge only after the relevant CI gate is green;
6. verify the resulting `main` push gate before the final handover.

If `Current/CURRENT_STATE.json` changes, regenerate renderer-controlled files with `RepositoryTools/render_current_navigation.py`; do not hand-edit those generated files independently.

## Step 4 — Runtime-test and completed-log UX

If a runtime test is outstanding, the same response that explains the test must include the repository-driven Gale replacement/import PowerShell one-liner when required and the exact build-specific self-contained PowerShell one-line runtime-log uploader.

If the run is already complete but its completed runtime log still needs upload/ingest, provide the uploader for the build identified by `RuntimeInbox/ACTIVE_BUILD.txt` and do not require another gameplay run solely for evidence submission.

If neither condition applies, do not provide an unnecessary uploader.

## Step 5 — Final handover response

Only the final handover segment produces these two parts.

### PART 1 — HANDOVER COMPLETION

Report the final verified repository state compactly:

- final `main` commit;
- final relevant green CI run and permanent-gate result;
- whether a relevant open PR remains;
- whether repository repair was required;
- any material controller/runtime fact that cannot be safely inferred by simply reading `Current/CURRENT_STATE.json`;
- whether the user must perform any manual repository action.

Do **not** duplicate the accepted baseline, latest artifact, candidate, every SHA, runtime gate and exact next action merely because they exist. Point to `Current/CURRENT_STATE.json` for the complete volatile state, and repeat a live fact only when it materially prevents ambiguity in the handover.

### PART 2 — READY-TO-COPY START PROMPT FOR THE NEW CHAT

Generate a fresh, compact prompt from the just-verified repository.

The new-chat prompt must:

- declare the repository as the complete Source of Truth;
- instruct the new chat to read `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` before performing project work;
- require bounded segments, checkpoint reporting and waiting for user continuation between non-final segments;
- use this initial read order: `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`, `Current/CURRENT_STATE.json`, `Current/PROJECT_KNOWLEDGE_MAP.md`;
- include the final verified `main` commit and relevant green CI run;
- tell the new chat to route the task through the Topic Router and read only the required canonical topic/evidence;
- tell the new chat not to perform a full-repository audit by default and not to treat historical "current" wording as live authority;
- preserve the runtime import/uploader rule and the completed-log rule;
- tell the new chat not to require local clone/build work while repository-native infrastructure is sufficient;
- explicitly state that when the user later signals another handover, it must execute `Current/HANDOVER_PREPARATION_PROMPT.md` under the segmented-execution policy.

Do not copy the entire live-state object into the ready-to-copy prompt. The new chat is required to read `Current/CURRENT_STATE.json`, which is the canonical volatile state.

## Integrity rules

During handover:

- never promote or reject a build implicitly;
- never treat `RuntimeInbox/ACTIVE_BUILD.txt` as acceptance authority;
- never fabricate missing provenance;
- never rewrite historical evidence merely to make search results look clean;
- never create a successor merely to make the handover appear active;
- never bypass the continuation gate when safe segmentation is available.

## Maintenance contract

Update this workflow only when the handover process, authority model, validation policy, segmented-execution policy or mandatory runtime UX changes. Ordinary build/runtime progression should update canonical state/evidence instead.

This workflow must remain discoverable from `README.md`, `START_HERE_ChatGPT_Masterprompt.txt`, `Current/01_HANDOVER_CORE.md`, `Current/PROJECT_KNOWLEDGE_MAP.md` and `Current/DOCUMENT_AUTHORITY.md/.json`.
