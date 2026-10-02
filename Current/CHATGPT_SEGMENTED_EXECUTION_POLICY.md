# ChatGPT Segmented Execution Policy

**Status:** CURRENT / CANONICAL PROJECT-WIDE CHATGPT EXECUTION POLICY  
**Authority:** mandatory execution procedure for every ChatGPT chat working on this repository  
**Canonical-For:** `chatgpt_segmented_execution`, `project_task_segmentation`, `continuation_gate`  
**Applies to:** every user request that causes ChatGPT to perform project work, repository actions, research, analysis, build/runtime work, code/config changes, audits, migrations, or other non-trivial task execution  
**Last-Validated:** 2026-10-02

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

## Temporary GPT-6 escalation recommendation

**Status:** TEMPORARY PROJECT RULE / RECOMMENDATION ONLY

Before starting the next execution segment, ChatGPT must assess whether using the user's **scarce GPT-6 quota** is justified through either of two independent escalation triggers. The default is **do not recommend GPT-6** unless at least one trigger applies.

The first trigger is **reasoning/risk complexity**. A recommendation is appropriate when the next not-yet-started segment is unusually demanding **and** there is a clear, material expected benefit from GPT-6 that is likely to outweigh the cost of consuming the limited quota. Strong justification can include one or more unusually severe factors such as: a genuinely hard multi-authority reconciliation with ambiguous/conflicting evidence; a high-risk transformation where a subtle reasoning error could corrupt canonical state or artifact provenance; a broad root-cause investigation with several plausible interacting causes and substantial source/runtime evidence; a difficult architecture or implementation decision with many coupled constraints and meaningful irreversible downstream cost; or another segment where materially deeper reasoning is expected to reduce failure/rework risk rather than merely make ordinary work more convenient.

The second trigger is **exceptional expected segment duration**. If, before beginning the next not-yet-started segment, it is reasonably foreseeable from the known scope, repository/tool chain, required validation and likely research/analysis work that the assistant-side processing for that segment would take **more than nine minutes**, ChatGPT must recommend switching to a new GPT-6 chat before starting that segment. This duration trigger is sufficient on its own even when the underlying work is otherwise routine. It is a planning threshold for whether to recommend the optional handover, not a promise, deadline or service-level guarantee about actual completion time. If the duration is genuinely uncertain and an over-nine-minute segment is not reasonably foreseeable, this trigger does not apply.

The following are **not sufficient by themselves** under the reasoning/risk trigger: involving many files, requiring several routine tool calls, waiting for CI, performing an ordinary PR review/merge, applying a well-established repository precedent, doing straightforward metadata/state reconciliation, completing repetitive validation steps that current tooling already makes deterministic, or merely being somewhat long. However, the explicit **more-than-nine-minute expected-duration trigger overrides this list** when it applies.

When either escalation trigger is met:

1. ChatGPT must stop **before beginning the complex segment** and recommend that the user switch to a new ChatGPT chat using GPT-6.
2. This is a recommendation only. ChatGPT must not assume consent and must not initiate the handover merely because the threshold is met.
3. If the user declines the recommendation, or instead explicitly instructs the current chat to continue, the current chat may proceed normally under the standard segmented-execution and continuation rules.
4. If the user explicitly agrees to switch to GPT-6, the current chat must not begin the upcoming complex segment. It must initiate the normal repository-native handover process through `Current/HANDOVER_PREPARATION_PROMPT.md`, freshly re-verifying repository/CI/controller state as required, and provide the ready-to-copy new-chat handover prompt.
5. The generated GPT-6 handover prompt must state that the GPT-6 chat may execute **at most two project execution segments**. After completing its second project execution segment, that GPT-6 chat must stop before beginning a third segment and hand control back through the normal handover/reassessment process.
6. The two-segment GPT-6 limit does not authorize combining work that should otherwise be separated under this policy. Each GPT-6 segment remains bounded by the same atomicity, checkpoint and continuation requirements as any other project segment.

Treat the limited GPT-6 quota as a scarce project resource. For the reasoning/risk trigger, when uncertain whether the benefit is substantial enough, **do not recommend the switch** and continue with the current model under normal segmented execution. Independently, apply the more-than-nine-minute duration trigger whenever that duration is reasonably foreseeable from the known next-segment scope. In either case the recommendation remains optional for the user: ChatGPT must not switch or initiate a handover without explicit user agreement. Do not interrupt an already-started atomic repository operation solely to make this recommendation; finish the safe atomic unit first and apply the recommendation before the next segment.

This rule is explicitly temporary. It remains in force until the user explicitly asks for it to be removed or superseded. It does not alter gameplay lifecycle authority, build/runtime controllers, acceptance state, or any model-independent repository evidence.

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
- `Current/00_CURRENT_STATE.md`;
- `Current/01_HANDOVER_CORE.md`;
- `Current/CURRENT_STATE.json` canonical navigation;
- `Current/PROJECT_KNOWLEDGE_MAP.md`;
- `Current/DOCUMENT_AUTHORITY.md/.json`;
- `Current/HANDOVER_PREPARATION_PROMPT.md`.

`Current/PROJECT_KNOWLEDGE_MAP.json` remains the machine semantic-topic router; this cross-cutting execution policy is anchored through canonical navigation/authority rather than being required to behave as a gameplay/content topic.

Repository CI should fail if this discoverability contract is lost.

## Maintenance contract

Update this file only when the segmented-execution process itself changes.

Ordinary gameplay/build/runtime progression must not require rewriting this policy.
