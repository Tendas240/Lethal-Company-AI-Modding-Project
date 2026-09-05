# Current ChatGPT Handover Preparation Prompt

**Status:** CURRENT / CANONICAL HANDOVER PROCEDURE  
**Authority:** procedure the active ChatGPT chat must execute when the user requests transfer to a new ChatGPT chat  
**Canonical-For:** `chat_handover_preparation`, `fresh_new_chat_prompt_generation`  
**Execution cadence:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Machine State:** `Current/CURRENT_STATE.json`  
**Topic Router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority Registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Last-Validated:** 2026-09-05

## Purpose

This file is the durable handover instruction for the **currently active ChatGPT chat**.

When the user explicitly signals that the project should be handed over to a new ChatGPT chat, use this procedure instead of reconstructing a handover from conversation memory alone.

This file deliberately avoids hard-coding the current accepted build, latest build, candidate, runtime gate, successor state, hashes, CI run IDs or exact next gameplay action. Those facts change over time and must be resolved from repository authority at handover time.

The prompt itself should evolve only when the handover process, authority model, validation policy, segmented-execution policy or mandatory takeover UX changes. Ordinary build/runtime progression should update canonical state/evidence rather than requiring a rewrite here.

## Mandatory segmented execution

The handover workflow is subject to `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`.

Do **not** perform a long multi-stage handover in one uninterrupted assistant turn merely because all later steps are already known. Divide the handover into bounded segments, report a checkpoint after each non-final segment, stop, and wait for the user's explicit continuation signal before beginning the next segment.

A normal handover should use roughly these segments when applicable:

1. **Inspection/recovery segment:** resolve the actual current state, relevant conversation/PDF recovery evidence, open PRs and current CI/controller reality; determine whether repository repair is required.
2. **Repository-finalization segment:** make only the necessary handover/state repairs on a branch and prepare the repository for validation. Stop before PR/CI/merge unless those operations are inseparable from a small atomic repair.
3. **Validation/final handover segment:** run PR/CI, repair genuine gate failures, merge only after green validation, verify the resulting `main` push state, then produce the final handover and ready-to-copy new-chat prompt.

If no repository repair is needed, fewer segments are appropriate. A truly short/atomic handover may be one segment. Never leave an intentionally inconsistent repository/controller state merely to create a checkpoint.

## Trigger

Treat any explicit user request to transfer, hand over, migrate or continue the project in a new ChatGPT chat as the handover signal.

When triggered:

- do not ask the user to restate information already present in the repository;
- do not rely on a stale handover text from an earlier chat;
- do not automatically create a new build or runtime test merely because a handover is happening;
- announce the handover segments and execute only the current segment under the continuation gate.

## Step 1 — Resolve the actual current authority state

Use the repository as the Source of Truth and read the current `main` branch directly.

Start with:

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
4. `Current/CURRENT_STATE.json`
5. `Current/00_CURRENT_STATE.md`
6. `Current/01_HANDOVER_CORE.md`
7. `Current/PROJECT_KNOWLEDGE_MAP.md`
8. `Current/PROJECT_KNOWLEDGE_MAP.json`
9. `Current/DOCUMENT_AUTHORITY.md`
10. `Current/DOCUMENT_AUTHORITY.json`
11. `Knowledge/CURRENT_LIFECYCLE.md`
12. `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
13. `BuildSpecs/current.json`
14. `RuntimeInbox/ACTIVE_BUILD.txt`
15. this file: `Current/HANDOVER_PREPARATION_PROMPT.md`

Then follow the Knowledge Map to the canonical topic/evidence required by the exact next action. Do **not** perform a manual full-repository audit by default.

Read integrity/audit authorities when relevant, especially:

- `Current/INTEGRITY_ERRATA_REGISTRY.json`
- `Current/VALIDATOR_COVERAGE.json`
- `Current/OVERHAUL_VALIDATION_RESULTS.json`
- `Current/OVERHAUL_EXECUTION_STATE.json`
- the latest integrity/audit records referenced by those authorities

## Step 2 — Verify repository and CI reality

Before producing the handover, independently verify:

- current `main` HEAD;
- latest relevant `Knowledge Architecture` push run for that HEAD;
- every permanent validation step in that run;
- any open PR containing relevant unmerged project-state, handover, integrity, build or runtime changes;
- agreement among `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, build lineage and current lifecycle for accepted baseline, latest artifact, active candidate, runtime-test state, runtime-active/evidence-attribution build, successor/controller state and exact next action;
- authoritative build/profile/runtime hashes;
- any known superseded values through `Current/INTEGRITY_ERRATA_REGISTRY.json`.

Do not cite a green validator as proof of anything outside `Current/VALIDATOR_COVERAGE.json`.

## Step 3 — Decide whether repository changes are actually needed

If the repository is already internally consistent and contains everything a fresh chat needs, **do not create a cosmetic handover commit**. State that no repository commit was required.

If genuine drift or missing handover-critical information exists:

1. preserve historical evidence;
2. repair current authority/metadata rather than silently rewriting history;
3. do not change gameplay/config/mod/profile/runtime behavior solely for handover cleanup;
4. use a dedicated branch and PR;
5. run the complete relevant CI gate;
6. merge only after the PR gate is green;
7. verify the resulting `main` push gate;
8. use the final merged `main` commit and verified CI state in the handover output.

If canonical machine state changes, update `Current/CURRENT_STATE.json` first and regenerate renderer-controlled navigation through `RepositoryTools/render_current_navigation.py` rather than hand-editing generated files independently.

Under the segmented policy, repository repair and final PR/CI/merge should normally be separate segments unless the whole change is a genuinely short atomic unit.

## Step 4 — Preserve runtime-test and completed-log UX

If **no runtime test is outstanding and no completed runtime log still needs evidence upload**, do not ask for a log upload and do not provide an unnecessary uploader.

If a runtime test **is** outstanding, the same response that explains what the user must test must also provide:

1. the canonical repository-driven Gale replacement/import PowerShell one-liner when applicable;
2. the exact build-specific self-contained PowerShell one-line runtime-log uploader.

If the runtime test is already complete but its log has not yet been ingested, provide the exact build-specific uploader for the build identified by `RuntimeInbox/ACTIVE_BUILD.txt` and do not ask the user to repeat the run solely because evidence submission is pending. `ACTIVE_BUILD` controls runtime-active/evidence-attribution; it is not acceptance authority and may differ from the accepted baseline.

Use `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Knowledge/GALE_PROFILE_WORKFLOW.md` as authority.

Do not require a local repository clone or local profile build while repository-native infrastructure is sufficient.

## Step 5 — Required final response from the current chat

Only the **final handover segment**, after all required repository/CI verification is complete, produces the final two-part handover response.

### PART 1 — HANDOVER COMPLETION

Give a compact but complete final state including:

- final verified `main` commit;
- final relevant green CI run and whether all permanent gates passed;
- whether any open relevant PR remains;
- accepted baseline with profile path and SHA-256;
- latest built artifact with profile path, SHA-256 and acceptance/rejection/pending status;
- active candidate;
- runtime-test state;
- runtime-active/evidence-attribution build;
- whether a completed runtime log still needs upload/ingest;
- successor/build-controller state;
- exact next project action;
- relevant current authority files;
- relevant known supersessions/errata;
- remaining non-blocking integrity qualifications or optional governance points that materially matter;
- whether the user must perform any manual repository action.

If no repository change was needed, say so explicitly.

### PART 2 — READY-TO-COPY START PROMPT FOR THE NEW CHAT

Generate a **fresh prompt from the just-verified repository state**. Do not copy an old static handover prompt without re-resolving its facts.

The new-chat prompt must:

- declare the repository as the complete Source of Truth;
- instruct the new chat to read `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` before performing project work;
- explicitly require bounded segments, checkpoint reporting and waiting for user continuation between non-final segments;
- give the exact initial read order for other current canonical files;
- include the final verified `main` commit and relevant green CI run;
- state actual accepted baseline, latest built artifact and authoritative hashes/statuses;
- state active candidate, runtime-test state, runtime-active/evidence-attribution build and successor/build-controller state;
- state exact next project action and governing canonical topic/evidence;
- include current errata/supersession facts likely to prevent wrong interpretation;
- preserve material historical/audit qualifications;
- tell the new chat to route normal questions through `Current/PROJECT_KNOWLEDGE_MAP.md/.json` rather than re-auditing the whole repository by default;
- tell the new chat not to require local clone/build work while repository-native infrastructure is sufficient;
- preserve the runtime-test rule requiring the exact PowerShell uploader in the same response as test instructions;
- preserve the completed-log rule for `RuntimeInbox/ACTIVE_BUILD.txt` without requiring another run;
- explicitly tell the new chat that **when the user later signals another handover**, it must execute `Current/HANDOVER_PREPARATION_PROMPT.md` under the segmented-execution policy;
- be self-contained enough that the new chat does not need access to the previous conversation.

The new-chat prompt may include additional topic-specific files if the exact next action requires them, but should not dump the entire repository into the startup read list.

## Step 6 — Handover-specific integrity rules

During handover:

- never promote a rejected build implicitly because a later analysis corrected only part of its rejection rationale;
- never treat `RuntimeInbox/ACTIVE_BUILD.txt` as acceptance authority;
- never treat a historical handover/candidate/status snapshot as current authority merely because it says `current`;
- never fabricate missing historical provenance/checkpoints;
- never replace superseded historical concrete values merely to make search results clean;
- never claim CI proves runtime/gameplay semantics beyond documented validator coverage;
- never create a successor just to make the handover appear to have an active task;
- never bypass the continuation gate merely to finish the whole handover faster when safe segmentation is available.

## Maintenance contract for this prompt

This file is a **current workflow authority**, not a historical snapshot.

Review/update it when any of the following changes:

- segmented-execution policy or continuation-gate semantics;
- canonical bootstrap/read order;
- location/semantics of `Current/CURRENT_STATE.json`;
- Knowledge Map or Document Authority routing;
- branch/PR/CI handover policy;
- runtime-test uploader/import UX requirements;
- completed-run evidence-upload semantics;
- required integrity/audit preflight;
- required fields in the generated new-chat start prompt.

Ordinary accepted-build/candidate/runtime progression should normally require no edit here because the procedure resolves those facts dynamically.

This prompt must remain discoverable from:

- `START_HERE_ChatGPT_Masterprompt.txt`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/PROJECT_KNOWLEDGE_MAP.md`;
- `Current/DOCUMENT_AUTHORITY.md/.json`.

It must itself expose `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` and require every generated new-chat start prompt to preserve that policy.

CI must treat loss of that discoverability as repository knowledge-architecture drift.
