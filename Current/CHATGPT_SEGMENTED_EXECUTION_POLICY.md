# ChatGPT Segmented Execution Policy

**Status:** CURRENT / CANONICAL PROJECT-WIDE CHATGPT EXECUTION POLICY  
**Authority:** mandatory execution procedure for every ChatGPT chat working on this repository  
**Canonical-For:** `chatgpt_segmented_execution`, `project_task_segmentation`, `continuation_gate`  
**Applies to:** every user request that causes ChatGPT to perform project work, repository actions, research, analysis, build/runtime work, code/config changes, audits, migrations, or other non-trivial task execution  
**Last-Validated:** 2026-10-09

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

## Mandatory chat-local segment ordinal (since the new-chat handover prompt)

Every project execution segment **must display its own consecutive chat-local ordinal**, counted from the most recent new-chat handover prompt that began the **current ChatGPT conversation**. The **first executed segment after that starting prompt is Segment 1**, regardless of the project's much older PR/checkpoint count. After every executed bounded segment, increment by exactly one and display the next pending segment as **Segment N+1**. Do not reset at a new task, PR, milestone or a user message requesting handover preparation *inside the same chat*. Reset only when a **new chat** actually starts with its own handover prompt. When no formal handover prompt exists, use the first substantive project execution segment in the chat as Segment 1.

Count all real bounded execution segments, including one-segment tasks, user-requested repository-policy changes, CI/validation-only segments, failed or fail-closed segments and handover-preparation segments. A simple question, clarification or acknowledgment that performs no bounded project execution does not consume a segment. Count from the **actual visible conversation history**, not repository-global checkpoint numbers, PR numbers or an assumed persistent counter; do not write a mutable per-chat counter to the repository. If history is incomplete and the ordinal cannot be established reliably, label it **unverified** rather than inventing a precise number, and reconcile against the available current-chat handover/history before claiming an exact ordinal.

At the **beginning and checkpoint/end of every segment**, show the current ordinal, for example `Segment 3 seit dem Übergabe-Prompt`. At the **checkpoint**, also explicitly identify the next pending ordinal and its bounded action, for example `Nächstes Segment 4: PR-Status prüfen`. The functional **Weiter button must carry that same next ordinal in its visible label**, using exactly the convention `Weiter – Segment 4: PR-Status prüfen` (with a roughly 2–3-word concrete action after the colon). The number advances on the next authorized execution, **not just because a button was displayed**. The separate `Übergabe an neuen Chat` action is not a counter reset within the existing chat. This ordinal is independent of an optional planned `Segment 1/3` total, which may change as scope is revised.

## Segment sizing

A segment must be large enough to produce useful, durable progress, but small enough to avoid an unnecessarily long tool/research/build chain.

Prefer one coherent objective per segment, for example:

- inspect current authority/state and define scope;
- perform focused technical/source analysis;
- implement an isolated repository change;
- run PR/CI/build validation;
- merge and perform final state/handover verification.

Avoid combining broad repository discovery, implementation, CI repair, merge, runtime preparation and final handover into one uninterrupted assistant turn when they can be safely separated.

The initial number of planned task segments is a planning estimate, **separate from the mandatory chat-local ordinal**. If new evidence changes the scope, ChatGPT may revise the remaining planned segment count, but must explain the change at the next checkpoint; the consecutive ordinal since the new-chat handover prompt must not skip or reset.

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

- **Current chat segment ordinal:** `Segment N seit dem Übergabe-Prompt` (also shown at the segment start), plus the **next chat segment ordinal** `N+1` and its bounded action;
- **Completed:** what this segment actually finished;
- **Findings:** material results, blockers or surprises;
- **Remaining:** what is still required for the user's original request;
- **Next segment:** the exact next bounded action;
- an explicit statement that ChatGPT is stopping and waiting for the user's continuation signal.

At the end of the final segment, state that the requested task is complete, summarize the final verified state, and identify the next repository-authorized project task/gate (or state explicitly when the next task is not yet determined). The final segment of one task is not the end of the overall project's continuation UX; always offer both mandatory checkpoint action buttons below.

## Optional graphical segment checkpoint (when practical)

At the end of **each project execution segment**, including final segments and bounded handover-preparation segments, **prefer a compact graphical representation of the checkpoint** when the chat client supports it and producing it is straightforward, proportionate and genuinely useful.

- Choose the visualization to match the available facts: for example, a progress bar for completed versus planned **execution segments**, a short milestone/status timeline, or a simple chart of relevant verified counts.
- **Where meaningful and supported, optionally add interactive elements** to the checkpoint or visualization, such as expandable verification details, selectable milestone/status views or interactive charts. Use functional native controls with clearly described behavior; never present inert or decorative pseudo-interactions.
- Keep interactivity proportionate: add it only when it brings a concrete benefit without significant extra implementation work, latency or complexity. An informational interaction must not silently execute repository changes, launch gameplay/tests, advance to another segment or trigger handover. Those actions remain subject to explicit user authorization and the mandatory continuation/handover buttons below.
- Use only accurate, currently supported values. Clearly label what a quantity or progress bar measures; `3/4 segments` must not be mistaken for `75% of the whole project`. Never invent progress percentages, completion claims or measurements where none are available.
- Keep visual and interactive elements lightweight and readable. Prefer supported native UI over separate images, generated assets, external dependencies or repository files.
- Skip either the visual or interactive elements without blocking completion if the client does not support suitable controls, reliable values are unavailable, or creating them would add significant work, delay, complexity or merely decorative clutter.
- **Always retain** the required textual `Completed / Findings / Remaining / Next segment` checkpoint, its explicit stop/continuation gate and the functional action buttons described below. Visuals and interactive elements are supplementary, never replacements and never a reason to bypass safety or verification.

## Required next-build / next-runtime-test outlook and project orientation

At the end of **every project execution segment**, including final segments and bounded handover-preparation segments, provide an immediately understandable **where-are-we-now** view and a forward-looking estimate for **the next build** and **the next runtime test**. This is a mandatory checkpoint communication rule, independent of whether the next event is already authorized. It extends, rather than replaces, the optional general graphical checkpoint rule above.

- **Show two distinctly labeled build/test readiness progress bars whenever supported and grounded**, one for the next build and one for the next runtime test. Prefer compact native progress bars, segmented gate tracks, or equally clear native graphical equivalents; accompany them with the current phase/milestone and the next concrete prerequisite. The user should be able to distinguish the progress of *this chat's execution segments*, the *readiness gates to the next build/test*, and the *overall project*, which are different measurements.
- **Base any filled progress fraction on a real denominator**: count only explicitly identified required gates/milestones for the next specific event, report completed versus total known gates, and identify important remaining blockers. Do not silently treat a precedent's full build/publication/activation pipeline as mandatory when the currently authorized path is different. If the sequence is uncertain, has no defensible denominator, or no next build/test has been selected or authorized, use an honestly labeled **indeterminate / not scheduled / blocked** readiness bar or status track (when supported), without a fabricated percentage; state what decision or evidence would allow a grounded estimate.
- **Estimate how far away each next build/runtime test is**, not merely the completed segment count. Prefer a qualified estimate in remaining **known work steps, segments, or gates**; additionally provide a rough **elapsed-time range** only when the current evidence, workflow durations, scope and dependencies make that defensible. Label estimates as estimates and state the principal assumptions or uncertainties (such as CI, review, human gameplay/log upload or as-yet-unauthorized work). If a calendar-time estimate cannot be supported, say explicitly **"time not reliably estimable yet"** rather than inventing hours/days, deadlines, or a percent-to-time conversion. A readiness bar is *not* a clock or guaranteed ETA.
- **Maintain wider project orientation** whenever genuinely useful: show the current lifecycle/phase, the last verified milestone, the next actionable gate, and relevant established residual or completed-versus-outstanding counts using a short status timeline, milestone track, stacked bar, chart, or similarly concise visualization. Where useful and low-overhead, allow functional optional interactions (for example toggling between next-build and next-runtime prerequisites or expanding source-backed gate details); do not add controls that do nothing or silently trigger a project transition.
- Re-evaluate this outlook from freshly checked repository lifecycle, build/runtime controllers, authorized scope, PR/CI and evidence on each checkpoint. **Never** turn a visual estimate into a build/runtime authorization, a claim that uncompleted work is done, an acceptance decision, or an automatic continuation. Preserve the required textual **Completed / Findings / Remaining / Next segment** report, stopping rule, and mandatory continuation/handover buttons. If the client cannot render the intended visuals, give a concise text-based progress/gate/status equivalent instead.

## Mandatory dual visualizations: progress to next runtime test and pipeline to next runtime test

**Status: REQUIRED AT EVERY SEGMENT CHECKPOINT / NOT OPTIONAL.** At the end of **every project execution segment** (including final/one-of-one segments, repository-policy or documentation changes, blocked/status-only checkpoints, and bounded handover-preparation or final handover segments), show **both** of the following as **two distinct, visibly titled visualizations**. They supplement the existing separate **next-build / next-runtime-test readiness outlook**, the textual Completed / Findings / Remaining / Next segment report, and the mandatory action buttons; none replaces the others.

1. **"Fortschritt bis zum nächsten Runtime-Test" — graphical progress indicator.** Show a compact bar/track for the **actual next identified runtime-test target**, plus an evidence-based `completed/total known prerequisite milestones` count when a defensible denominator exists. State the target explicitly (e.g. a particular diagnostic or active runtime candidate), the current milestone, the immediate blocker and the fact that the track measures **readiness milestones, not elapsed time or whole-project completion**. Differentiate a future diagnostic's preparation from a distinct already-outstanding passive/selector-free gameplay proof gate; do not silently combine them.
2. **"Pipeline als Ablaufkette bis zum nächsten Runtime-Test" — graphical flow of prerequisites.** Directly below or next to the progress indicator, show the **ordered, concise chain** from the last verified milestone, through the current gate and remaining required gates, to **"Runtime-Test bereit"** (and the user-executed runtime test when useful). Distinguish each stage visually as **✅ complete, 🔄 current/in progress, ⏳ pending, or ⛔ blocked/not authorized** (or equivalent native icons). Include the concrete next action, and where applicable separately represent authorization, original-byte publication/integration, profile hash mapping/canonical indexing, runtime activation/integration, Gale replacement/import instructions, test preparation and user-executed log collection. **Derive the actual stages from fresh repository state, controllers, PR/CI, evidence and existing authorizations; this example is not a universally mandatory pipeline.** Never imply an unapproved build/runtime or automatically run any stage.

Both visuals must be present **even if this particular segment changes only documentation, CI, policy or a handover**: they orient the user within the ongoing project, not merely the completed segment. Prefer compact native UI progress/flow elements when available; if graphical rendering is unsupported, use **two separate, clearly titled plain-text bar/flow diagrams** (for example `[████░░░░] 2/4 verified gates` and `✅ Gate A → 🔄 Gate B → ⏳ Gate C → Runtime-Test bereit`). Do not omit either illustration merely because one cannot be made interactive.

**Truthfulness / unknowns:** Never invent a percentage, denominator, fixed number of remaining segments, date, duration, authorized milestone or completed gate. A bar should use a fraction only when the planned prerequisites are sufficiently known and counted from evidence. If the runtime-test target, readiness prerequisites or denominator are uncertain, render a clearly labeled **indeterminate / not yet scheduled / blocked** bar or status track, **not** an invented numeric fraction; show only grounded stages and explicitly mark any unknown path as **"weitere Gates noch zu bestimmen"**. Identify what decision/evidence would resolve uncertainty. Treat the bar as a readiness view, never an ETA or acceptance statement.

**Refresh every time:** Reconstruct both visuals from the freshly checked current project authority at each checkpoint. Mark stages complete only with verified evidence; after merges or additional decisions recompute the bar and chain rather than repeating a stale snapshot. The paired diagrams must remain easy to scan, and do not authorize compilation, publication, Gale import, runtime tests or lifecycle promotions. Keep separate, truthful next-build status even where the next build is deliberately forbidden or no longer needed.

## Mandatory checkpoint action buttons (when supported)

At the end of **every project execution segment**, including each bounded handover-preparation segment, offer the user an explicit choice between continuing project work and requesting a fresh-chat handover. Use **functional, visible, native interactive buttons** when the chat client supports them; do not show inert or decorative pseudo-buttons.

**Mandatory next-segment ordinal and action-preview labeling:** The first button's **visible label itself** must identify the *next* consecutive chat-local segment number **and** preview its concrete bounded action, using approximately two or three German action words after the colon. Required form: `Weiter – Segment N+1: <kurze nächste Aktion>` (for example `Weiter – Segment 4: PR-Status prüfen`). Naming the segment number or the action only in surrounding prose or in a tooltip is insufficient. Keep the label compact and specific; its click behavior remains the same explicit continuation gate.

- **"Weiter – Segment N+1: <kurze nächste Aktion>" — mandatory after EVERY segment, including final segments and bounded handover-preparation segments**: Always show a functional button whose **visible label starts with `Weiter – Segment N+1:` (using the actual next chat-local ordinal) and names the next concrete, repository-authorized action in roughly two or three German words** (examples: `Weiter – Segment 4: PR integrieren`, `Weiter – Segment 5: CI-Grenzen prüfen`, `Weiter – Segment 6: Build autorisieren`). **Never use the bare label `Weiter` when a next action is known**; avoid uninformative labels such as `Weiter – Nächster Schritt` or generic segment numbers without the actual task. After a final project segment, name the next separately authorized project gate, not the just-completed action. When the next actionable gate is unknown, blocked or not yet authorized, use a truthful short determination label such as `Weiter – Status prüfen` or `Weiter – Freigabe klären`, never suggest a forbidden implementation, build or runtime action. The button must remain available even when no next task is authorized. Clicking it must submit a **new user continuation turn** (for example `GenUI.issueNewTurn("weiter")`). At a non-final checkpoint this authorizes **only the next bounded segment** of the current task; at a final checkpoint it requests continuation with **the next repository-authorized bounded project task/segment**, not repetition of the completed task. Re-read mandatory fresh repository authorities, verify the current next action and reassess the temporary GPT-6 escalation rule before starting any new work. If the repository does not currently establish an actionable/authorized next task, keep the `Weiter` button visible: its click permits only a fresh, bounded status/next-step determination and a transparent blocker or request for scope, **not** an invented authorization for a build, runtime attempt, implementation, acceptance or repository mutation. Never continue automatically or imply that a completed work package is still open.
- **"Übergabe an neuen Chat"**: At the end of **every segment, including the final segment**, also show a separate button labeled `Übergabe an neuen Chat`. Its click must submit a **new explicit user request to initiate the repository-native handover preparation in this current chat**, for example `GenUI.issueNewTurn("Bereite jetzt eine Übergabe an einen neuen Chat gemäß Current/HANDOVER_PREPARATION_PROMPT.md vor.")`. This is an alternative to "Weiter", not an additional project segment to execute automatically. Follow the handover file and this segmented-execution policy, freshly verifying repository/PR/CI/controllers before producing a ready-to-copy new-chat starting prompt. Do not silently merge pending PRs or mutate project state merely because the user requested handover.
- The handover button **does not itself create, open or populate a new ChatGPT conversation**. The current chat prepares and supplies the start prompt, and the user opens a new chat and transfers that prompt. Do not claim otherwise.
- Keep the required `Completed / Findings / Remaining / Next segment` report and explicit stop statement for every non-final segment. At a final segment, summarize the completed work package, report the next known repository-authorized project step (or its currently missing authorization), explicitly stop, and show **both** `Weiter` and `Übergabe an neuen Chat`. The `Weiter` button remains available even when the next step is not yet established; it must not silently authorize or execute that step.
- If functional native buttons are unavailable, offer the same choice as explicit text instructions **after every segment, including the final segment**: `Zum Fortfahren mit dem nächsten zulässigen Projektschritt "weiter" senden; für die Übergabe "Übergabe an neuen Chat" senden.` Never omit the `weiter` option just because the current work package ended. Never claim a text link or dummy button provides one-click execution.
- These button rules govern **chat UX and explicit user choice only**. They do not modify runtime/build/acceptance authorities, override atomicity, waive CI gates or silently consume GPT-6 quota. Every future chat must obey them after reading this canonical policy.

### Completed final handover: copy prompt instead of re-preparing it

**Specific mandatory exception to the generic second-button rule above:** When the response already provides the final complete new-chat start prompt from `Current/HANDOVER_PREPARATION_PROMPT.md` (PART 1 handover completion + PART 2 ready-to-copy prompt), the two functional buttons must be **`Weiter – <kurze nächste Aktion>`** (or **`Weiter – Status prüfen`** when the next action is unestablished) and **`Übergabe-Prompt kopieren`** — **not** `Übergabe an neuen Chat` or `Übergabe erneut vorbereiten`. This applies to **every final handover output** and takes precedence over the general rule above that normally requires the handover-initiation button at other checkpoints. Keep the action-labeled `Weiter – ...` button even though this handover work package is finished; its click still requests only the next authorized, bounded segment.

The copy button must use a real clipboard action initiated by the user's click, for example `GenUI.copy(fullNewChatStartPrompt)`, with the exact, entire text of PART 2 as its argument. Preserve every URL, SHA, PR/CI reference, instruction and constraint; do not omit, summarize, regenerate or include PART 1/status text, UI labels or formatting markup. The button must **not** issue a new turn, re-run the completed handover, or claim to open a new chat. The user opens the new chat and pastes the copied prompt there. Do not claim clipboard success without platform confirmation.

If native clipboard controls are unsupported, provide PART 2 in a clearly selectable prompt block for manual copying rather than an inert pseudo-button, and still show/provide a text or functional `Weiter – <kurze nächste Aktion>` option. Ordinary non-handover checkpoints continue to show the action-labeled `Weiter – ...` button + `Übergabe an neuen Chat`. This is only a chat-UX exception; no build, runtime, CI, PR or acceptance authority changes.

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
