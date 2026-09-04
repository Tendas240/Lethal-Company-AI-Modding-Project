# Current ChatGPT Handover Preparation Prompt

**Status:** CURRENT / CANONICAL HANDOVER PROCEDURE  
**Authority:** procedure the active ChatGPT chat must execute when the user requests transfer to a new ChatGPT chat  
**Canonical-For:** `chat_handover_preparation`, `fresh_new_chat_prompt_generation`  
**Machine State:** `Current/CURRENT_STATE.json`  
**Topic Router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority Registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Last-Validated:** 2026-09-05

## Purpose

This file is the durable handover instruction for the **currently active ChatGPT chat**.

When the user explicitly signals that the project should be handed over to a new ChatGPT chat, the active chat must use this procedure instead of reconstructing a handover from conversation memory alone.

This file deliberately avoids hard-coding the current accepted build, latest build, candidate, runtime gate, successor state, hashes, CI run IDs or exact next gameplay action. Those facts change over time and must be resolved from the repository at handover time.

The prompt itself should evolve only when the **handover process, authority model, validation policy or mandatory takeover UX** changes. Ordinary build/runtime progression should update the canonical project state and evidence, not require rewriting this procedure every time.

## Trigger

Treat any explicit user request to transfer, hand over, migrate or continue the project in a new ChatGPT chat as the handover signal.

When triggered:

- do not ask the user to restate information already present in the repository;
- do not rely on a stale handover text from an earlier chat;
- do not automatically create a new build or runtime test merely because a handover is happening;
- execute the verification and finalization procedure below in the current response/work session.

## Step 1 — Resolve the actual current authority state

Use the repository as the Source of Truth and read the current `main` branch directly.

Start with:

1. `README.md`
2. `START_HERE_ChatGPT_Masterprompt.txt`
3. `Current/CURRENT_STATE.json`
4. `Current/00_CURRENT_STATE.md`
5. `Current/01_HANDOVER_CORE.md`
6. `Current/PROJECT_KNOWLEDGE_MAP.md`
7. `Current/PROJECT_KNOWLEDGE_MAP.json`
8. `Current/DOCUMENT_AUTHORITY.md`
9. `Current/DOCUMENT_AUTHORITY.json`
10. `Knowledge/CURRENT_LIFECYCLE.md`
11. `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
12. `BuildSpecs/current.json`
13. `RuntimeInbox/ACTIVE_BUILD.txt`
14. this file: `Current/HANDOVER_PREPARATION_PROMPT.md`

Then follow the Knowledge Map to the canonical topic/evidence required by the current exact next action. Do **not** perform a manual full-repository audit by default.

Read integrity/audit authorities when they are relevant to the current state or to handover correctness, especially:

- `Current/INTEGRITY_ERRATA_REGISTRY.json`
- `Current/VALIDATOR_COVERAGE.json`
- `Current/OVERHAUL_VALIDATION_RESULTS.json`
- `Current/OVERHAUL_EXECUTION_STATE.json`
- the latest integrity/audit records referenced by those authorities

## Step 2 — Verify repository and CI reality

Before producing the handover, independently verify:

- the current `main` HEAD commit;
- the latest relevant `Knowledge Architecture` push run for that `main` HEAD;
- that every permanent validation step in that run completed successfully;
- whether any open PR contains relevant unmerged project-state, handover, integrity, build or runtime changes;
- that `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, build lineage and the current lifecycle topic agree on:
  - accepted baseline;
  - latest built artifact;
  - active candidate;
  - runtime-test state;
  - successor/build-controller state;
  - exact next action;
- that build/profile/runtime hashes used in the handover come from current authority/evidence rather than stale historical prose;
- that all known superseded values relevant to the current handover are interpreted through `Current/INTEGRITY_ERRATA_REGISTRY.json`.

Do not cite a green validator as proof of anything outside the declared scope in `Current/VALIDATOR_COVERAGE.json`.

## Step 3 — Decide whether repository changes are actually needed

If the current repository is already internally consistent and contains everything a fresh chat needs, **do not create a cosmetic handover commit**. State explicitly that no repository commit was required.

If genuine drift or missing handover-critical information exists:

1. preserve historical evidence;
2. repair current authority/metadata rather than silently rewriting history;
3. do not change gameplay/config/mod/profile/runtime behavior solely for handover cleanup;
4. use a dedicated branch and PR;
5. run the complete relevant CI gate;
6. merge only after the PR gate is green;
7. verify the resulting `main` push gate;
8. use the final merged `main` commit and its verified CI state in the handover output.

If a repository change also changes the canonical machine state, update `Current/CURRENT_STATE.json` first and regenerate renderer-controlled navigation through `RepositoryTools/render_current_navigation.py` rather than hand-editing generated files independently.

## Step 4 — Preserve runtime-test UX

If **no runtime test is outstanding**, do not ask for a log upload and do not provide an unnecessary uploader.

If a runtime test **is** outstanding, the same response that explains what the user must test must also provide:

1. the canonical repository-driven Gale replacement/import PowerShell one-liner when applicable;
2. the exact build-specific self-contained PowerShell one-line runtime-log uploader.

Use `Knowledge/BUILD_AND_RUNTIME_PIPELINE.md` and `Knowledge/GALE_PROFILE_WORKFLOW.md` as authority for that workflow.

Do not require a local repository clone or local profile build while repository-native infrastructure is sufficient.

## Step 5 — Required final response from the current chat

The handover response must contain exactly these two logical parts.

### PART 1 — HANDOVER COMPLETION

Give a compact but complete final state including:

- final verified `main` commit;
- final relevant green CI run and whether all permanent gates passed;
- whether any open relevant PR remains;
- accepted baseline with profile path and SHA-256;
- latest built artifact with profile path, SHA-256 and acceptance/rejection/pending status;
- active candidate;
- runtime-test state;
- successor/build-controller state;
- exact next project action;
- current runtime active-build controller;
- relevant current authority files;
- relevant known supersessions/errata that a new chat must not misread;
- remaining non-blocking integrity qualifications or optional governance points that materially matter;
- whether the user must perform any manual repository action.

If no repository change was needed for the handover, say so explicitly.

### PART 2 — READY-TO-COPY START PROMPT FOR THE NEW CHAT

Generate a **fresh prompt from the just-verified repository state**. Do not copy an old static handover prompt without re-resolving its facts.

The new-chat prompt must:

- declare the repository as the complete Source of Truth;
- give the new chat the exact initial read order for current canonical files;
- include the final verified `main` commit and relevant green CI run;
- state the actual accepted baseline, latest built artifact and their current authoritative hashes/statuses;
- state active candidate, runtime-test state and successor/build-controller state;
- state the exact next project action;
- name the canonical topic/evidence that governs that next action;
- include any current errata/supersession facts that would otherwise cause a likely wrong interpretation;
- preserve any current historical/audit qualification that remains materially relevant;
- explicitly tell the new chat to route normal project questions through `Current/PROJECT_KNOWLEDGE_MAP.md/.json` rather than re-auditing the whole repository by default;
- explicitly tell the new chat not to require local clone/build work while repository-native infrastructure is sufficient;
- explicitly preserve the future runtime-test UX rule requiring the exact PowerShell uploader in the same response as test instructions;
- explicitly tell the new chat that **when the user later signals another handover, it must execute `Current/HANDOVER_PREPARATION_PROMPT.md`**;
- be self-contained enough that the new chat does not need access to the previous conversation.

The new-chat prompt may include additional topic-specific files if the current exact next action requires them, but should not dump the entire repository into the startup read list.

## Step 6 — Handover-specific integrity rules

During handover:

- never promote a rejected build implicitly because a later analysis corrected only part of its rejection rationale;
- never treat a historical handover, candidate record or old project-status snapshot as current authority merely because it says `current`;
- never fabricate missing historical provenance/checkpoints;
- never replace a superseded historical concrete value in retained history merely to make search results look clean; use explicit errata/supersession authority;
- never claim a CI gate proves runtime/gameplay semantics that its documented validator coverage does not test;
- never create a successor just to make the handover appear to have an active task.

## Maintenance contract for this prompt

This file is a **current workflow authority**, not a historical snapshot.

Review and update it when any of the following changes:

- canonical bootstrap/read order;
- location or semantics of `Current/CURRENT_STATE.json`;
- Knowledge Map or Document Authority routing;
- branch/PR/CI handover policy;
- runtime-test uploader/import UX requirements;
- required integrity/audit preflight;
- required fields in the generated new-chat start prompt.

Ordinary accepted-build/candidate/runtime progression should normally require **no edit here** because the procedure resolves those facts dynamically from repository authority.

This prompt must remain discoverable from:

- `START_HERE_ChatGPT_Masterprompt.txt`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/PROJECT_KNOWLEDGE_MAP.md/.json`;
- `Current/DOCUMENT_AUTHORITY.md/.json`.

CI must treat loss of that discoverability as repository knowledge-architecture drift.