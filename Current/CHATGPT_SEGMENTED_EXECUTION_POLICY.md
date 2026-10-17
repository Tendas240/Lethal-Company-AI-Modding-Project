# ChatGPT Segmented Execution Policy

**Status:** CURRENT / CANONICAL PROJECT-WIDE CHATGPT EXECUTION POLICY  
**Authority:** mandatory execution procedure for every ChatGPT chat working on this repository  
**Canonical-For:** `chatgpt_segmented_execution`, `project_task_segmentation`, `continuation_gate`  
**Applies to:** every user request that causes ChatGPT to perform project work, repository actions, research, analysis, build/runtime work, code/config changes, audits, migrations, or other non-trivial task execution  
**Last-Validated:** 2026-10-15 (bounded automatic continuation proposal; draft PR only)

## Purpose

This policy exists to reduce the risk that a ChatGPT work turn becomes too large, stalls for too long, or ends in an incomplete response such as `Message Delivery timed out` or `connection interrupted. waiting for the complete answer`.

It does not guarantee that platform/network interruptions can never occur. It deliberately reduces exposure by keeping each work turn bounded, observable and restartable.

This policy is stored in the repository and is part of the project contract. Do not rely on ChatGPT Memory to preserve it.

## Core rule

For every user request that requires ChatGPT to perform project work, divide the authorized task into sensible, bounded execution segments and process them sequentially. Preserve the consecutive chat-local segment ordinal.

**Bounded automatic continuation, within an existing authorization only:** An explicit user task may define a coherent, finite work package. Within that same assistant response, ChatGPT may automatically execute **at most two consecutive bounded segments** without an additional user message, provided both are independently permitted by the user's existing task authorization and all current repository authorities. Before entering the second segment, reassess scope, risk, repository state, available context and expected effort. Do not automatically enter a third segment in the same response.

For example: perform a focused repository/source inspection, record a short internal checkpoint, and then complete a tightly related read-only assessment; or, within an explicitly authorized implementation package, prepare the bounded change and verify its CI. These are examples of execution cadence, **not** permissions to mutate anything.

**Never cross an authorization boundary automatically.** A continuation signal or a broad work-package description is not a merge, draft-removal, build, publication, runtime instrumentation, profile/controller activation, Gale import, gameplay, acceptance, new hook, new external download or public redistribution authorization. Each such operation still needs the exact authorization and all security/evidence gates demanded by other repository authorities and the user's actual instructions. A task authorizing one PR does not authorize another PR. If scope or safety is unclear, stop fail-closed and ask.

For each segment:
1. identify its concrete bounded objective and chat-local ordinal;
2. execute only authorized actions;
3. record Completed / Findings / Remaining and the current risk or blocker;
4. if another authorized segment fits the two-segment response budget and the safety/time/context guards below, continue within this **same** response, showing the next ordinal;
5. otherwise finish a full user-visible checkpoint and stop for an explicit user continuation signal.

The user's ability to say "stop", change direction, or request an immediate checkpoint always takes precedence at the next safe interruption point. There is no autonomous background continuation, no unattended repeat loop and no automatic creation of a new chat. Once an assistant response ends, further project execution requires another user message. At the end of each assistant response, stop after the full checkpoint until the user sends another message. The handover button does not automatically create a new chat.

## Anti-loop / no-progress gate (v1; proposed process rule)

**Scope:** execution cadence and next-prerequisite routing only. This rule does **not** waive an existing proof requirement, change `Current/CURRENT_STATE.json` or its canonical `next_action`, approve risk on the user's behalf, or authorize a build, hook, diagnostic runtime, gameplay attempt, controller/profile change or merge.

Before repeating a previously **BLOCKED / REFUSED / UNPROVEN** work item, compare its *decision fingerprint*: exact target and proposed method, missing material evidence/guarantees, authenticated source/commit or artifact identity, applicable authority, and scope of the last explicit user authorization. A new chat, handover, elapsed time, unchanged successful CI, a generic "weiter", an unchanged repository snapshot, or a speculative observer architecture **does not** change that fingerprint.

- **Identical fingerprint:** do **not** rerun the same historical log analysis, static preflight, original-byte acquisition attempt, safety argument or status-only BLOCKED segment merely to fill a segment slot. Preserve the previous bounded conclusion and say which newly authenticated input or separate express approval would reopen it. A user-requested current-state check may perform only a narrowly necessary delta check; if nothing has changed, stop immediately. Do not pretend that another BLOCKED reply establishes progress.
- **Park the blocked *method*, not the whole active subproject.** A parked method stays BLOCKED; its target remains an unresolved proof gap, not a PASS, a waived gate or a removed residual. Propose a materially different, in-scope, evidence-grounded next prerequisite (for example a different viable Interior flow, independent owner/per-flow evidence, a specifically authorized diagnosis proposal, or a separately gated priority decision). Do not switch to an independent roadmap subproject contrary to Interior-first authority.
- **Canonical routing first:** `Current/CURRENT_STATE.json` and topic authorities select the current next action. An unmerged Draft PR or chat decision never rewrites that action. When the canonical prerequisite has already been analyzed only in chat or Draft form, explicitly identify the missing integration/approval gate; do not re-perform the analysis or unilaterally merge it. Any change to canonical next-action pointers requires its own separately authorized, validated repository transition.
- **At each blocked checkpoint:** state the fingerprint's missing condition, concrete *re-entry trigger*, and the closest materially different lawful action with its separate authorization needs. If no authorized forward action exists, stop and ask for a choice rather than cycling into an identical segment. Number actual performed segments consistently with this policy; neither invent advancement nor reset the count on a handover.

## Risk-scoped diagnostic proposals (v1; no blanket relaxation)

Use these categories when **proposing** a future evidence-acquisition path. They describe required scrutiny; they are not executable authorization levels.

| Category | Scope and decision boundary |
| --- | --- |
| **A — Existing-evidence/read-only** | Inspect already present repository, source and authenticated logs/bytes. No runtime execution, hook, mutation or fresh download without distinct permission. If exhausted, record and park the method. |
| **B — Bounded observational diagnostic** | A separately versioned, default-inactive and narrowly scoped proposal (e.g. a hook-free assembly-provenance snapshot) may acknowledge *bounded, documented* risk from plugin loading, file I/O, timing and environment effects rather than claim impossible-to-prove absolute non-influence. Require concrete source-grounded inspection of entry points, activation path, recorded fields, permissions, side effects, rollback and failure behavior; explicit approval of the exact residual risks **before** implementation, activation or runtime. Never claim a snapshot's file hashes establish live memory image identity, Harmony execution order or Museum selection safety. No Harmony patch, selector or wrapper mutation may be silently classified as B. |
| **C — Intervening diagnostic** | Any selector, Harmony hook, wrapper/list mutation, config/weight/seed/RNG manipulation or gameplay-affecting instrumentation. Existing exact method/owner/ABI/atomicity and Patch Safety requirements remain fully applicable. Risk acceptance alone cannot discharge a mandatory safety guarantee, unblock CKDIAG1, authorize unsafe Clear/Add or unproven `ref __result`, or override owner restrictions. If an existing contract prohibits the method, first obtain a separately scoped architecture/policy decision supported by new evidence; otherwise BLOCKED. |
| **D — Gameplay candidate/acceptance** | Normal profile changes, publication, Gale/runtime integration and acceptance preserve all applicable lifecycle, source/CI, regression, generation/materialization, traversal and independent passive proof gates. A diagnostic observation is never a Generation-PASS, natural-frequency witness, selector-free validation, or acceptance by itself. |

For any Category B or C proposal, first provide a **bounded diagnostic safety case** identifying: (1) exact target/question and the proof tier it can and cannot establish; (2) authenticated inputs, plugin/assembly identity, loading and timing assumptions; (3) all interventions, observable side effects and credible cross-mod failure modes; (4) stop/refusal behavior, isolated rollback and evidence provenance; (5) explicit remaining uncertainty and the precise user permissions needed separately for source/PR, build/publication, activation, Gale and gameplay/log collection. A hypothetical safe design or CI-green documentation is not proof of safety. If any binding security contract or essential precondition remains unmet, fail closed and park that *method* while pursuing other already-permitted Interior-first work.

These process categories do not supersede `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`, `Current/250`, `Current/406`, `Current/409`, `Current/410`, `Current/412`, `Current/416` or any stronger exact current-topic authority. Where the approved risk envelope conflicts with a binding guarantee, the guarantee prevails until explicitly and validly changed. Existing BLOCKED Museum/CKDIAG1 findings and the independent selector-free BMDSFIX1 proof remain unchanged.

## Mandatory chat-local segment ordinal (since the new-chat handover prompt)

Every project execution segment **must display its own consecutive chat-local ordinal**, counted from the most recent new-chat handover prompt that began the **current ChatGPT conversation**. The **first executed segment after that starting prompt is Segment 1**, regardless of the project's much older PR/checkpoint count. After every executed bounded segment, increment by exactly one and display the next pending segment as **Segment N+1**, whether the next segment is immediately continued inside the same explicitly authorized assistant response or awaits a later user continuation. Do not reset at a new task, PR, milestone or a user message requesting handover preparation *inside the same chat*. Reset only when a **new chat** actually starts with its own handover prompt. When no formal handover prompt exists, use the first substantive project execution segment in the chat as Segment 1.

Count all real bounded execution segments, including one-segment tasks, user-requested repository-policy changes, CI/validation-only segments, failed or fail-closed segments and handover-preparation segments. A simple question, clarification or acknowledgment that performs no bounded project execution does not consume a segment. Count from the **actual visible conversation history**, not repository-global checkpoint numbers, PR numbers or an assumed persistent counter; do not write a mutable per-chat counter to the repository. If history is incomplete and the ordinal cannot be established reliably, label it **unverified** rather than inventing a precise number, and reconcile against the available current-chat handover/history before claiming an exact ordinal.

At the **beginning and checkpoint/end of every segment**, show the current ordinal, for example `Segment 3 seit dem Übergabe-Prompt`. At the **checkpoint**, also explicitly identify the next pending ordinal and its bounded action, for example `Nächstes Segment 4: PR-Status prüfen`. The functional **Weiter button must carry that same next ordinal in its visible label**, using exactly the convention `Weiter – Segment 4: PR-Status prüfen` (with a roughly 2–3-word concrete action after the colon). The number advances only when the next execution actually begins, including a permitted in-response automatic continuation, **not just because a button was displayed**. The separate `Übergabe an neuen Chat` action is not a counter reset within the existing chat. This ordinal is independent of an optional planned `Segment 1/3` total, which may change as scope is revised.

## Segment sizing

A segment must be large enough to produce useful, durable progress, but small enough to avoid an unnecessarily long tool/research/build chain.

Prefer one coherent objective per segment, for example:

- inspect current authority/state and define scope;
- perform focused technical/source analysis;
- implement an isolated repository change;
- run PR/CI/build validation;
- merge and perform final state/handover verification.

Avoid combining broad repository discovery, implementation, CI repair, merge, runtime preparation and final handover into one uninterrupted assistant turn when they can be safely separated. A two-segment automatic window must never be used to hide an additional authorization boundary.

The initial number of planned task segments is a planning estimate, **separate from the mandatory chat-local ordinal**. If new evidence changes the scope, ChatGPT may revise the remaining planned segment count, but must explain the change at the next checkpoint; the consecutive ordinal since the new-chat handover prompt must not skip or reset.

### Technical continuity and context guard

The two-segment limit is a **hard cap per assistant response**, not a target. Use one segment when sufficient. Before automatically entering a second segment, stop instead if the estimated total assistant-side work in the current response would exceed **approximately four minutes**, if an asynchronous operation requires extended polling, if tool failures or unexpected scope expansion occur, or if the evidence volume makes the next segment difficult to complete reliably. These are conservative planning guards, not a promised runtime or proof that network interruptions cannot occur. An already-started atomic safety-critical write must still be completed safely under the atomicity exception.

**Chat-length guard:** When the current chat has accumulated **six project execution segments** since its last new-chat handover, proactively recommend preparing a repository-native handover *before the next substantial work package*, or sooner if responses, source material, tool outputs, uncertainties or retrievals become unusually large. The model cannot reliably measure a platform's remaining chat-context quota; these are heuristic early-warning signals, not a false exact token/length meter. Do not automatically create a new chat or prepare a handover without the user's explicit request. The user may explicitly choose to continue; maintain bounded execution and stop early if safe continuity is doubtful.

Do not silently shorten or skip substantive verification merely to stay below these bounds. Stop with a reusable evidence/PR/CI checkpoint rather than repeating a fragile operation. Do not claim that the limits eliminate Connection Lost, Message Delivery timeout or conversation-size limits.

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

At the **start of every segment**, display its consecutive chat-local ordinal. After **every segment**, preserve an identifiable checkpoint, even when a second segment will follow automatically in the same assistant response.

- For an **internal in-response checkpoint**, briefly report **Completed / Findings / Remaining**, identify the following ordinal and bounded action, and explicitly state that continuation uses the already granted scope. No separate user message is required at this intermediate boundary; do not claim new permissions.
- At the **end of each assistant response** performing project work (including a response containing two segments), present the full **Completed / Findings / Remaining / Next segment** summary, current and next chat-local ordinals, exact next bounded action, blockers and whether the original task is complete. Use the four distinct labels **Completed:**, **Findings:**, **Remaining:** and **Next segment:** so both users and validators can identify each checkpoint. Explicitly stop and wait for the user's next message.
- At final work-package completion, report the verified state and the next repository-authorized gate (or state that none is established). The separate handover option remains available.

The mandatory build/runtime outlook, both named runtime-test visualizations and the two functional checkpoint actions below appear at **every end-of-response checkpoint**; they need not be repeated inside the intermediate checkpoint between two permitted in-response segments. This preserves the user-facing safety view without inflating one response with duplicate diagrams.

## Optional graphical segment checkpoint (when practical)

At the end of **each project-work assistant response**, including final work-package responses and bounded handover-preparation responses, **prefer a compact graphical representation of the checkpoint** when the chat client supports it and producing it is straightforward, proportionate and genuinely useful.

- Choose the visualization to match the available facts: for example, a progress bar for completed versus planned **execution segments**, a short milestone/status timeline, or a simple chart of relevant verified counts.
- **Where meaningful and supported, optionally add interactive elements** to the checkpoint or visualization, such as expandable verification details, selectable milestone/status views or interactive charts. Use functional native controls with clearly described behavior; never present inert or decorative pseudo-interactions.
- Keep interactivity proportionate: add it only when it brings a concrete benefit without significant extra implementation work, latency or complexity. An informational interaction must not silently execute repository changes, launch gameplay/tests, advance to another segment or trigger handover. Those actions remain subject to explicit user authorization and the mandatory continuation/handover buttons below.
- Use only accurate, currently supported values. Clearly label what a quantity or progress bar measures; `3/4 segments` must not be mistaken for `75% of the whole project`. Never invent progress percentages, completion claims or measurements where none are available.
- Keep visual and interactive elements lightweight and readable. Prefer supported native UI over separate images, generated assets, external dependencies or repository files.
- Skip either the visual or interactive elements without blocking completion if the client does not support suitable controls, reliable values are unavailable, or creating them would add significant work, delay, complexity or merely decorative clutter.
- **Always retain** the required textual `Completed / Findings / Remaining / Next segment` checkpoint, its explicit stop/continuation gate and the functional action buttons described below. Visuals and interactive elements are supplementary, never replacements and never a reason to bypass safety or verification.

## Required next-build / next-runtime-test outlook and project orientation

At the end of **every project-work assistant response**, including final work-package responses and bounded handover-preparation responses, provide an immediately understandable **where-are-we-now** view and a forward-looking estimate for **the next build** and **the next runtime test**. This is a mandatory checkpoint communication rule, independent of whether the next event is already authorized. It extends, rather than replaces, the optional general graphical checkpoint rule above.

- **Show two distinctly labeled build/test readiness progress bars whenever supported and grounded**, one for the next build and one for the next runtime test. Prefer compact native progress bars, segmented gate tracks, or equally clear native graphical equivalents; accompany them with the current phase/milestone and the next concrete prerequisite. The user should be able to distinguish the progress of *this chat's execution segments*, the *readiness gates to the next build/test*, and the *overall project*, which are different measurements.
- **Base any filled progress fraction on a real denominator**: count only explicitly identified required gates/milestones for the next specific event, report completed versus total known gates, and identify important remaining blockers. Do not silently treat a precedent's full build/publication/activation pipeline as mandatory when the currently authorized path is different. If the sequence is uncertain, has no defensible denominator, or no next build/test has been selected or authorized, use an honestly labeled **indeterminate / not scheduled / blocked** readiness bar or status track (when supported), without a fabricated percentage; state what decision or evidence would allow a grounded estimate.
- **Estimate how far away each next build/runtime test is**, not merely the completed segment count. Prefer a qualified estimate in remaining **known work steps, segments, or gates**; additionally provide a rough **elapsed-time range** only when the current evidence, workflow durations, scope and dependencies make that defensible. Label estimates as estimates and state the principal assumptions or uncertainties (such as CI, review, human gameplay/log upload or as-yet-unauthorized work). If a calendar-time estimate cannot be supported, say explicitly **"time not reliably estimable yet"** rather than inventing hours/days, deadlines, or a percent-to-time conversion. A readiness bar is *not* a clock or guaranteed ETA.
- **Maintain wider project orientation** whenever genuinely useful: show the current lifecycle/phase, the last verified milestone, the next actionable gate, and relevant established residual or completed-versus-outstanding counts using a short status timeline, milestone track, stacked bar, chart, or similarly concise visualization. Where useful and low-overhead, allow functional optional interactions (for example toggling between next-build and next-runtime prerequisites or expanding source-backed gate details); do not add controls that do nothing or silently trigger a project transition.
- Re-evaluate this outlook from sufficiently fresh repository lifecycle, build/runtime controllers, authorized scope, PR/CI and evidence at each end-of-response checkpoint; recheck exact expected heads and required gates immediately before any permitted mutation. **Never** turn a visual estimate into a build/runtime authorization, a claim that uncompleted work is done, an acceptance decision, or an automatic continuation. Preserve the required textual **Completed / Findings / Remaining / Next segment** report, stopping rule, and mandatory continuation/handover buttons. If the client cannot render the intended visuals, give a concise text-based progress/gate/status equivalent instead.

## Mandatory dual visualizations: progress to next runtime test and pipeline to next runtime test

**Status: REQUIRED AT EVERY END-OF-RESPONSE PROJECT CHECKPOINT / NOT OPTIONAL.** At the end of **every assistant response containing project execution** (including final/one-of-one work, repository-policy or documentation changes, blocked/status-only work, and handover preparation), show **both** of the following as **two distinct, visibly titled visualizations**. They supplement the existing separate **next-build / next-runtime-test readiness outlook**, the textual Completed / Findings / Remaining / Next segment report, and the mandatory action buttons; none replaces the others.

1. **"Fortschritt bis zum nächsten Runtime-Test" — graphical progress indicator.** Show a compact bar/track for the **actual next identified runtime-test target**, plus an evidence-based `completed/total known prerequisite milestones` count when a defensible denominator exists. State the target explicitly (e.g. a particular diagnostic or active runtime candidate), the current milestone, the immediate blocker and the fact that the track measures **readiness milestones, not elapsed time or whole-project completion**. Differentiate a future diagnostic's preparation from a distinct already-outstanding passive/selector-free gameplay proof gate; do not silently combine them.
2. **"Pipeline als Ablaufkette bis zum nächsten Runtime-Test" — graphical flow of prerequisites.** Directly below or next to the progress indicator, show the **ordered, concise chain** from the last verified milestone, through the current gate and remaining required gates, to **"Runtime-Test bereit"** (and the user-executed runtime test when useful). Distinguish each stage visually as **✅ complete, 🔄 current/in progress, ⏳ pending, or ⛔ blocked/not authorized** (or equivalent native icons). Include the concrete next action, and where applicable separately represent authorization, original-byte publication/integration, profile hash mapping/canonical indexing, runtime activation/integration, Gale replacement/import instructions, test preparation and user-executed log collection. **Derive the actual stages from fresh repository state, controllers, PR/CI, evidence and existing authorizations; this example is not a universally mandatory pipeline.** Never imply an unapproved build/runtime or automatically run any stage.

Both visuals must be present **even if this particular response changes only documentation, CI, policy or a handover**: they orient the user within the ongoing project, not merely the completed segment. Prefer compact native UI progress/flow elements when available; if graphical rendering is unsupported, use **two separate, clearly titled plain-text bar/flow diagrams** (for example `[████░░░░] 2/4 verified gates` and `✅ Gate A → 🔄 Gate B → ⏳ Gate C → Runtime-Test bereit`). Do not omit either illustration merely because one cannot be made interactive.

**Truthfulness / unknowns:** Never invent a percentage, denominator, fixed number of remaining segments, date, duration, authorized milestone or completed gate. A bar should use a fraction only when the planned prerequisites are sufficiently known and counted from evidence. If the runtime-test target, readiness prerequisites or denominator are uncertain, render a clearly labeled **indeterminate / not yet scheduled / blocked** bar or status track, **not** an invented numeric fraction; show only grounded stages and explicitly mark any unknown path as **"weitere Gates noch zu bestimmen"**. Identify what decision/evidence would resolve uncertainty. Treat the bar as a readiness view, never an ETA or acceptance statement.

**Refresh every time:** Reconstruct both visuals from the currently verified project authority at each end-of-response checkpoint. Mark stages complete only with verified evidence; after merges or additional decisions recompute the bar and chain rather than repeating a stale snapshot. The paired diagrams must remain easy to scan, and do not authorize compilation, publication, Gale import, runtime tests or lifecycle promotions. Keep separate, truthful next-build status even where the next build is deliberately forbidden or no longer needed.

## Mandatory checkpoint action buttons (when supported)

At the end of **every assistant response performing project work**, including final work-package responses and bounded handover preparation, offer the user a functional, visible native choice between continuing and requesting a new-chat handover. Do not insert redundant continuation buttons at the internal in-response boundary between two permitted segments.

- **"Weiter – Segment N+1: <konkrete Aktion>"**: the visible label must contain the next consecutive chat-local ordinal and approximately two or three concrete German action words after the colon. This control submits a new user continuation turn and requests only the next **repository-authorized bounded work**, potentially up to the two-segment in-response window if the continued work remains within already granted scope. It never grants new mutation/build/runtime/merge rights. When the next action is unestablished or blocked, label the short determination honestly (e.g. "Freigabe klären") rather than suggesting forbidden actions. Keep this button even after work-package completion.
- **"Übergabe an neuen Chat"**: submits a new explicit user request to prepare the repository-native handover under Current/HANDOVER_PREPARATION_PROMPT.md. Re-verify main, open PRs, exact CI and controller state before the final handover prompt as required by that file. This action **does not** automatically create or populate another ChatGPT conversation, grant project mutations or reset the current-chat ordinal. The user opens the new chat and pastes the handover.
- If the client lacks native buttons, show the equivalent explicit text instructions, not inert pseudo-buttons.

### Mandatory explicit authorization button at permission gates

**A required user approval must have a direct, functional approval action, not merely a status explanation.** Whenever the next concrete project action needs a separate express user authorization that has **not** been granted, the assistant must present an additional visible native button labeled **"Freigabe: <genau begrenzte Aktion>"** in the same response that identifies the missing approval, provided an exact and currently permissible approval request can be formulated. Do this immediately; do not wait for the user to ask where the approval button is, and do not send the user through another identical `BLOCKED` status loop merely to offer consent. The continuing/handover buttons remain mandatory and are not approval substitutes.

- **Make scope and consequences explicit:** adjacent to the button, state the exact action and target (source/package/version/PR/head/build/profile/runtime when relevant), the existing evidence/safety preconditions, what the proposed permission would and would not authorize, and whether other independent approval gates remain. A prior one-time authorization is not automatically reusable.
- **Make the button functional and unambiguous:** the button must submit a new user turn containing standalone, explicit, narrowly scoped approval text for that **one** operation, rather than generic `weiter`, a question, or an implied authorization. A click requests the separately authorized operation in the following turn; it must **not directly perform** a download, repository write, PR creation, merge, build, publication, activation, Gale import, runtime execution, gameplay test, acceptance or any other protected operation. Re-evaluate all repository authorities, exact bytes/heads, remaining proof gates and safety constraints before performing the action. An approval cannot itself establish missing technical evidence or waive mandatory safeguards.
- **No deceptive approval offer:** when a binding safety/legal rule prohibits the method, evidence required to authorize it is missing, or the action cannot yet be scoped precisely enough, do not present a misleading button that purports to override those blockers. Instead state the blocker and, if a distinct lawful request can resolve uncertainty, offer a functional **"Freigabeumfang klären"** button that submits a targeted clarification question; this is **not** approval. If there is no user-authorizable next action, explain the material re-entry trigger and park the method under the anti-loop rule.
- **One operation, one gate:** do not bundle unrelated permissions or hide independent future authorization gates behind a broad `Go` button. Examples include independently gated original-source acquisition, Draft PR preparation, review/merge, build, publication, Gale/runtime integration, and gameplay/acceptance. Do not conflate the user's approval of a policy change with approval of previously blocked project work.
- **Fallback:** if the client cannot render functional native buttons, provide the **exact complete consent text** for the user to send manually and clearly distinguish it from a mere continuation signal. Never present an inert decorative pseudo-button or imply that the client automatically creates a native permission prompt.

### Completed final handover: copy prompt instead of re-preparing it

**Specific precedence exception:** When an assistant response already contains the complete final new-chat start prompt (PART 1 status plus PART 2 ready-to-copy prompt), replace the second button with **"Übergabe-Prompt kopieren"**. Its actual click action must copy the **entire exact PART 2 text only** via the host clipboard action; never copy a summary, PART 1 or formatting wrappers. Do not claim copy success without confirmation. The first button must still show **"Weiter – Segment N+1: <konkrete Aktion>"** and submit a new authorized continuation message. If clipboard actions are unavailable, present the complete selectable PART 2 text for manual copying instead.

These controls govern chat continuation and navigation only. Neither automatic in-response continuation nor a button click overrides lifecycle, independent approvals, frozen evidence, security, CI or atomicity requirements.

## User continuation signal

A continuation message is required when the assistant response has stopped, not between two otherwise authorized segments performed in the same bounded response. The user does not need a special exact phrase. Any clear instruction to proceed is sufficient, including:

- `weiter`;
- `mach weiter`;
- `nächster Schritt`;
- `continue`;
- `go on`;
- an equivalent unambiguous instruction.

A follow-up that changes the objective is not merely a continuation signal; re-plan the work into appropriate segments for the new objective.

## Temporary GPT-6 escalation recommendation

**Status:** TEMPORARY PROJECT RULE / RECOMMENDATION ONLY

Before starting every execution segment, **including an automatically continued in-response segment**, ChatGPT must assess whether using the user's **scarce GPT-6 quota** is justified through either of two independent escalation triggers. The default is **do not recommend GPT-6** unless at least one trigger applies.

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

Within a segment (including any automatically continued segment):

- prefer focused reads/searches over broad open-ended repository scans;
- use repository-native infrastructure when sufficient;
- do not ask the user to clone/build locally merely to avoid tool work;
- preserve project authority, provenance and atomic state-transition rules;
- do not start a runtime test unless the current lifecycle says one is outstanding;
- when a future runtime test is actually ready, preserve the permanent rule that test instructions include the exact Gale replacement/import command when required and the exact build-specific one-line PowerShell log uploader in the same response.

If a tool operation is asynchronous and must finish before the segment has a meaningful checkpoint, ChatGPT may wait/poll within that segment. It must not use that as a reason to perform the next planned segment automatically.

## Handover behavior

Chat handovers are also subject to this policy. An in-response two-segment window may cover only already authorized handover-preparation actions, subject to the same time/context guards; actual chat creation and handover always require explicit user action.

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
