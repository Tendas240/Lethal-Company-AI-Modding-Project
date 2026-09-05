# ChatGPT Segmented Execution Policy

**Status:** CURRENT / CANONICAL PROJECT-WIDE CHATGPT EXECUTION POLICY  
**Authority:** mandatory execution procedure for every ChatGPT chat working on this repository  
**Canonical-For:** `chatgpt_segmented_execution`, `project_task_segmentation`, `continuation_gate`  
**Applies to:** every user request that causes ChatGPT to perform project work, repository actions, research, analysis, build/runtime work, code/config changes, audits, migrations, or other non-trivial task execution  
**Last-Validated:** 2026-09-05

## Purpose

This policy exists to reduce the risk that a ChatGPT work turn becomes too large, stalls for too long, or ends in an incomplete response such as `Message Delivery timed out` or `connection interrupted. waiting for the complete answer`.

It does not guarantee that platform/network interruptions can never occur. It deliberately reduces exposure by keeping each work turn bounded, observable and restartable.

This policy is stored in the repository and is part of the project contract. Do not rely on ChatGPT Memory to preserve it.

## Core rule

For every user request that requires ChatGPT to **perform work**, ChatGPT must divide the task into sensible execution segments and process them sequentially.

A normal multi-segment task follows this pattern:

1. identify the overall objective and a small number of coherent segments;
2. announce the current segment, for example `Segment 1/4`;
3. execute only that segment;
4. report what was completed, important findings and what remains;
5. state the next segment;
6. stop;
7. wait for an explicit user continuation signal such as `weiter`, `mach weiter`, `nächster Schritt`, `continue`, or equivalent;
8. execute the next segment only after that signal.

Do not automatically continue into the next segment merely because it is obvious what comes next.

## Segment sizing

A segment must be large enough to produce useful, durable progress, but small enough to avoid an unnecessarily long tool/research/build chain.

Prefer one coherent objective per segment, for example:

- inspect current authority/state and define scope;
- perform focused technical/source analysis;
- implement an isolated repository change;
- run PR/CI/build validation;
- merge and perform final state/handover verification.

Avoid combining broad repository discovery, implementation, CI repair, merge, runtime preparation and final handover into one uninterrupted assistant turn when they can be safely separated.

The initial number of segments is a planning estimate. If new evidence changes the scope, ChatGPT may revise the remaining segment count, but must explain the change at the next checkpoint.

## One-segment tasks

A genuinely short and atomic task may be `Segment 1/1` and can be completed in one response.

Examples include:

- answering a narrow repository fact after a small read;
- returning a known command from an authoritative file;
- making one trivial, self-contained metadata correction whose required validation is part of the same small atomic action.

Do not artificially create multiple confirmation turns for work that is objectively one short safe unit.

## Atomicity and safety exception

The continuation gate must never leave the repository, build controller, runtime controller, or an external action in a knowingly unsafe or internally inconsistent partial state.

If several operations are technically inseparable for one safe atomic change, keep them in the same segment. Examples:

- updating a canonical machine state and regenerating its renderer-controlled files;
- finishing a commit that must contain all mutually dependent files;
- resolving an immediately discovered write conflict caused by the current segment;
- completing an already-started merge/write operation so the repository is not deliberately left malformed.

This exception allows completion of the current atomic unit only. It is not permission to continue into unrelated later segments.

## Required checkpoint message

At the end of every non-final segment, ChatGPT must provide a concise checkpoint containing:

- **Completed:** what this segment actually finished;
- **Findings:** material results, blockers or surprises;
- **Remaining:** what is still required for the user's original request;
- **Next segment:** the exact next bounded action;
- an explicit statement that ChatGPT is stopping and waiting for the user's continuation signal.

At the end of the final segment, state that the requested task is complete and summarize the final verified state.

## User continuation signal

The user does not need a special exact phrase. Any clear instruction to proceed is sufficient, including:

- `weiter`;
- `mach weiter`;
- `nächster Schritt`;
- `continue`;
- `go on`;
- an equivalent unambiguous instruction.

A follow-up that changes the objective is not merely a continuation signal; re-plan the work into appropriate segments for the new objective.

## Tool and repository behavior

Within a segment:

- prefer focused reads/searches over broad open-ended repository scans;
- use repository-native infrastructure when sufficient;
- do not ask the user to clone/build locally merely to avoid tool work;
- preserve project authority, provenance and atomic state-transition rules;
- do not start a runtime test unless the current lifecycle says one is outstanding;
- when a future runtime test is actually ready, preserve the permanent rule that test instructions include the exact Gale replacement/import command when required and the exact build-specific one-line PowerShell log uploader in the same response.

If a tool operation is asynchronous and must finish before the segment has a meaningful checkpoint, ChatGPT may wait/poll within that segment. It must not use that as a reason to perform the next planned segment automatically.

## Handover behavior

Chat handovers are also subject to this policy.

`Current/HANDOVER_PREPARATION_PROMPT.md` must divide handover work into bounded segments when repository verification, cleanup, PR/CI work or final prompt generation would otherwise form one long work session.

A typical handover may use:

1. current-state/PDF/chat recovery inspection;
2. repository repair or handover-state update if required;
3. PR/CI/merge/final verification and generation of the ready-to-copy new-chat prompt.

If no repository repair is required, the handover may use fewer segments.

Every generated new-chat start prompt must explicitly instruct the new chat to read and follow this policy before doing project work.

## Relationship to other authorities

This file controls **execution cadence and checkpointing**. It does not replace:

- `Current/CURRENT_STATE.json` for live project state;
- `Current/PROJECT_KNOWLEDGE_MAP.md/.json` for semantic routing;
- `Current/DOCUMENT_AUTHORITY.md/.json` for current-vs-history precedence;
- `Current/HANDOVER_PREPARATION_PROMPT.md` for the contents of a handover;
- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` for patch safety;
- build/runtime workflow authorities for build, Gale and log-upload semantics.

If another workflow says a change must be atomic, this policy segments around that atomic unit rather than splitting it unsafely.

## Mandatory discoverability

This policy must remain discoverable from the normal project bootstrap and handover path, including:

- `README.md`;
- `START_HERE_ChatGPT_Masterprompt.txt`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/CURRENT_STATE.json` canonical navigation;
- `Current/PROJECT_KNOWLEDGE_MAP.md/.json`;
- `Current/DOCUMENT_AUTHORITY.md/.json`;
- `Current/HANDOVER_PREPARATION_PROMPT.md`.

Repository CI should fail if this discoverability contract is lost.

## Maintenance contract

Update this file only when the segmented-execution process itself changes.

Ordinary gameplay/build/runtime progression must not require rewriting this policy.
