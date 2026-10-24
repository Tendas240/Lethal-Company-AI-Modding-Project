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

## Cross-chat attachment and original-byte continuity

**Default: no inherited attachments.** Files uploaded to one ChatGPT conversation (including ZIPs, DLLs, logs and other attachments), conversation-local extracted files, and local/sandbox paths must **not** be assumed accessible in a new chat. A prior upload name, prior tool success, checksum cited in a handover or a path copied from a different chat is evidence *about* a file, not proof that its bytes exist in the new execution environment.

**Verify actual access at the point of use.** For each original-byte-dependent next task, first identify the exact required artifact (filename, package/version, source and expected SHA-256 when known) and distinguish: (a) original bytes actually present and readable in the current chat, (b) original bytes independently accessible in the repository or other currently authorized source, and (c) repository-only provenance/derived JSON/hash references without the underlying original bytes. A repository entry that records an uploaded ZIP hash does not mean that ZIP is stored there. Only classify an artifact as available after opening/verifying its concrete current source, and re-check pinned hashes before a byte-specific analysis. Never reuse a previous chat's sandbox path as though it were a cross-chat file transfer.

**Ask for missing originals only when material.** If the upcoming authorized action genuinely requires original bytes absent from accessible repository/current-chat sources, ask the user directly and promptly to **re-upload the named exact artifact**, including version and expected hashes if available. Do not run redundant acquisition attempts or historical analyses instead, and do not request a file when current repository-native evidence already suffices. Treat a prior-chats' successful byte analysis as handed-over historical evidence, not as fresh independent verification. On a new upload, verify all binding hashes and fail closed on mismatch. A new download, release/publication, PR, build or runtime action still requires its own applicable authorization; handover does not carry permissions forward automatically.

**Handover requirement:** Include each task-critical conversation-local-only attachment as explicitly **NOT TRANSFERRED / availability unverified in new chat**, alongside its exact identity, required use, expected hashes, and the new chat's first conditional action: verify actual accessibility through the repository/current conversation; if missing and needed, actively request re-upload before byte-dependent work. Do not claim that merely mentioning an attachment in PART 2 transfers the file.


## User-attested Gale profile continuity (2026-10-21)

**Default working assumption for user-operated profiles:** The user expressly states that they notify ChatGPT when they change their Gale profile, mods or configuration. When a particular profile is selected for a directed test and the user reports no changes, **treat its continued use without user-initiated modifications as the user's affirmative standing attestation**. Do not presuppose unreported user alterations, demand repeat gameplay or request a duplicate already-ingested original log merely because changes are theoretically possible. An explicit later user change report supersedes this continuity assumption for the affected period/artifacts; genuinely contradictory authenticated evidence must be evaluated rather than silently ignored.

**Concrete dated attestation:** `Current/S1.42AK_MINESHAFT_USER_PROFILE_CONTINUITY_ATTESTATION_20261021.md` records the user's direct 2026-10-21 confirmation that the 2026-10-20 Offense Mineshaft / `Level3Flow` runs used the unchanged `LC V1 S1.42AK LC Office Camera Enemy Balance` Gale profile and that it remains unchanged. Reference this record during the relevant Interior-first evidence and handover decisions, instead of reopening whether the user might have secretly edited their profile.

**Proof distinction is mandatory:** User testimony establishes **user-attested profile selection and no user-initiated change**, not an independently measured historical installed-profile byte hash, loaded-assembly manifest, exhaustive Harmony order or absolute selector-/RNG-intervention exclusion. Continue to label the independent P0/P1 gates according to their actual evidence; the receipt's `original_profile_bytes_independently_verified=false`, existing safety/owner/rights requirements and technical residual 21 remain unchanged until a separately authorized, independently justified canonical decision. Treat the user's credibility and the independent machine-proof standard as distinct questions. If stronger evidence is indispensable to a specific authorized action, state precisely what and why without reflexively demanding a repeat test or profile upload. Future handovers must carry both the affirmative attestation and these limits.

## Standing user delegation: repository administration and user-owned data (2026-10-22)

**Source:** Explicit project-owner instruction in the 2026-10-22 ChatGPT project conversation. **Effect:** Standing user-originated delegation for future *user-triggered, bounded repository work*, not a self-granted ChatGPT permission, not an assertion that an AI identity independently owns the repository, and not a waiver of GitHub-enforced or higher-priority constraints. The connected GitHub identity must actually possess the required permission at action time.

### GitHub administration without repeated routine confirmations

- The owner directs ChatGPT to use available repository-admin capabilities to independently carry out the **specific GitHub work inside the concrete segment the owner starts**, without repeated generic administrator attestations or extra approval clicks for ordinary repository mechanics. Within an identified, bounded project task, this standing user instruction can cover creating/updating its working branch, exact-scoped commits and PRs, necessary repository-native CI checks/dispatches, converting an identified draft PR to ready, and pinned-head merging **when the started segment explicitly identifies that integration as its intended next action** and all applicable gates are independently satisfied. It does not authorize creating unrelated PRs, inventing new work or silently expanding scope.
- The **segment launch remains user-controlled** through the chat's functional Weiter/action buttons or an equivalent concrete user message. Keep consecutive chat-local ordinals, at most two already-permitted segments per response, the required checkpoint visuals, and STOP between turns. No unattended continuation, repeated status polling, background task, automatic handover or UI-button-triggered direct GitHub mutation. An approval/action button sends a user message first; server-side changes occur only in a later execution segment after rechecking permissions and state.
- Treat the owner's 2026-10-22 GitHub Settings attestation as existing **user-provided administrative evidence for `main`**: no classic branch-protection rules, applicable rulesets, mandatory reviews or required checks at that time. Do not require the owner to reassert it just because a formerly inaccessible endpoint remains inaccessible, and do not replay an unchanged 403 probe. It is an attestation, not an independent API observation or a timeless guarantee. Before a consequential operation, freshly verify exact repository and PR state, expected head, changes, CI and reviews, and all protection/rules information **actually available**; obey any GitHub-enforced requirement or materially new contradictory evidence. On drift, unknown new mandatory gates, failed CI or insufficient actual permissions: fail closed and seek only the specific missing fact.
- A routine admin confirmation is not the same as technical authorization or proof. Do not self-approve a review, bypass branch protection, relax exact-head/byte/CI/owner gates, or count documentation as runtime evidence. Separate deliberately scoped user decisions remain necessary for new gameplay/runtime execution, Gale/profile activation, original-byte destruction, irreversible publication outside the already authorized project-evidence path, source-rights waivers, acceptance and safety/owner-boundary changes. Do not reinterpret a generic Weiter as permission for such a distinct operation.
- Read older references in this policy to an **additional separate GitHub admin approval** in light of this standing directive: do not ask for redundant confirmation when the concrete user-triggered GitHub segment and all required gates already cover the operation. Other express safety and external-operation authorization boundaries remain effective.

### Owner's own personal data in Lethal Company project evidence

- The owner expressly permits processing, analysis, retention and **repository-native public inclusion of their own voluntarily supplied personal data** as part of relevant Lethal Company modding logs and evidence. Do not invent a fresh privacy-consent blocker or ask for repetitive privacy confirmations **solely because those owner-supplied data appear in an otherwise authorized project log**. This is affirmative owner consent for that defined purpose, not an unrestricted consent for any recipient, medium or unrelated processing.
- The attestation does **not** establish rights over third-party personal data, credentials, access tokens, confidential material or publisher-owned bytes; do not assume those may be made public. Observe applicable law, platform rules, required data minimization, secrets handling and specifically imposed retention. Do not claim privacy or data-protection law has ceased to apply; raise a precise new issue only when an independently material risk actually exists. User consent does not resolve DULL publisher-byte identity or source-publication rights.
- Preserve `PRESERVE_UNTIL_SEPARATE_P0_P6_AND_RETENTION_DECISION`, `no_automatic_deletion=true`, existing V1/V2 raw-original byte identity and the original-byte, safety, rights, owner, P0-P6 and anti-loop gates. The owner's standing privacy consent is not permission to delete original logs or rewrite authenticated evidence.

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

## Anti-loop / no-progress gate (v2; PR-STAGED until separately integrated)

**Scope:** execution cadence and next-prerequisite routing only. This rule does **not** waive an existing proof requirement, change `Current/CURRENT_STATE.json` or its canonical `next_action`, approve risk on the user's behalf, or authorize a build, hook, diagnostic runtime, gameplay attempt, controller/profile change or merge.

Before repeating a previously **BLOCKED / REFUSED / UNPROVEN** work item, compare its *decision fingerprint*: exact target and proposed method, missing material evidence/guarantees, authenticated source/commit or artifact identity, applicable authority, and scope of the last explicit user authorization. A new chat, handover, elapsed time, unchanged successful CI, a generic "weiter", an unchanged repository snapshot, or a speculative observer architecture **does not** change that fingerprint.

- **Identical fingerprint:** do **not** rerun the same historical log analysis, static preflight, original-byte acquisition attempt, safety argument or status-only BLOCKED segment merely to fill a segment slot. Preserve the previous bounded conclusion and say which newly authenticated input or separate express approval would reopen it. A user-requested current-state check may perform only a narrowly necessary delta check; if nothing has changed, stop immediately. Do not pretend that another BLOCKED reply establishes progress.
- **Park the blocked *method*, not the whole active subproject.** A parked method stays BLOCKED; its target remains an unresolved proof gap, not a PASS, a waived gate or a removed residual. Propose a materially different, in-scope, evidence-grounded next prerequisite (for example a different viable Interior flow, independent owner/per-flow evidence, a specifically authorized diagnosis proposal, or a separately gated priority decision). Do not switch to an independent roadmap subproject contrary to Interior-first authority.
- **Canonical routing first:** `Current/CURRENT_STATE.json` and topic authorities select the current next action. An unmerged Draft PR or chat decision never rewrites that action. When the canonical prerequisite has already been analyzed only in chat or Draft form, explicitly identify the missing integration/approval gate; do not re-perform the analysis or unilaterally merge it. Any change to canonical next-action pointers requires its own separately authorized, validated repository transition.
- **At each blocked checkpoint:** state the fingerprint's missing condition, concrete *re-entry trigger*, and the closest materially different lawful action with its separate authorization needs. If no authorized forward action exists, stop and ask for a choice rather than cycling into an identical segment. Number actual performed segments consistently with this policy; neither invent advancement nor reset the count on a handover.

## Evidence-event preflight and dead-end avoidance (mandatory)

**Purpose:** Avoid repeatedly searching for evidence that could not have appeared since the last verified checkpoint. This is a decision-routing rule, not a relaxation of proof, rights, owner, safety, storage, CI, build, runtime or acceptance requirements. It applies to Interior-first work and every other evidence-dependent project scope, across segments and chat handovers.

**Before any renewed evidence search, perform a bounded event preflight:**
1. Identify the *last verified evidence baseline*: relevant main commit, already-ingested log/index/source identities, last authenticated user-provided inputs, and the parked method/decision fingerprints. Prefer the handover's exact identifiers and a narrow current main/ref delta; do not rescan historical logs, byte archives, source trees or all prior PRs just to see whether evidence has magically appeared.
2. State a **qualified re-entry trigger** before opening evidence. Either (a) a materially new authenticated evidence-bearing event, such as a relevant changed repository source/commit, a newly ingested original log, genuinely new user-provided bytes, or an independently authenticated new owner/source publication; or (b) a **specific, demonstrably unexhausted interpretive/source-access approach** to existing authenticated evidence, with an exact target, evidence locator, differentiating question and reason the prior blocked fingerprint does not already cover it. A timestamp, new chat, repeat user continuation, unchanged main, unrelated commit, green CI, hypothetical new URL, or reworded historical method is **not** a qualified trigger. A changed main SHA alone is not evidence; first establish relevance by a narrow delta.
3. If neither trigger exists, **do not run another evidence search, historical log query, source acquisition attempt or status-only BLOCKED segment**. A user-requested status check may read only the minimum necessary delta once. Do not imply that a user must upload a new file or conduct gameplay merely to make the same preflight repeatable.

**Acquisition pivot instead of dead end:** If the evidence is genuinely missing, first distinguish *evidence absence* from *lack of a safe acquisition method*. Where a materially different in-scope route is supportable, propose **one bounded evidence-acquisition plan**: the exact residual target, missing proof and maximum achievable proof tier; authenticated source/owner and provenance or permitted acquisition route; rights/storage/retention controls; relevant original-byte requirement (if any); passive versus intervening effects, failure/rollback and STOP criteria; the smallest specific user action (if genuinely required); and separate permissions for PR/source, build, publication, profile/index, Gale, runtime and gameplay as applicable. This planning step is not an instruction to acquire or run anything, and is not itself a generation or safety PASS. Do not improvise an unverified selector/hook, bypass owner exclusions, downgrade a mandatory guarantee or demand a stochastic reroll.

**No duplicate acquisition plans:** Compare the proposed route against parked target/method/source/safety fingerprints before planning. If that route has already been exhausted, or no lawful evidence-grounded route can be differentiated, record **BLOCKED_NO_NEW_AUTHENTICATED_EVIDENCE_OR_AUTHORIZATION**, name the precise external/new-authorization re-entry condition, and **STOP** without manufacturing further next-search segments. The active scope and its unmet gates remain open; lack of immediate progress is not completion or acceptance.

### One-shot project-owner exploratory acquisition exception (2026-10-24; narrowly scoped)

**Explicit exception to repeated stochastic acquisition, not to evidence or safety guarantees.** The project owner has deliberately selected **one finite exploratory multi-interior natural Offense campaign** as a possible future source of *new* authentic gameplay originals, acknowledging that the technical method is the **same natural selection and normal-stack logging** already used for the S1.42AK V1/V2 batches. Do not call a smaller cap, a different chat or the narrowed residual a novel method or a newly authenticated evidence event. The exact canonical test-method boundary is appended in `Current/250_PHASE_C_DETERMINISTIC_INTERIOR_TEST_STRATEGY_AND_DEFERRED_BCMER_PIKMIN_DIRECTIVE.md`. This narrow exception becomes operative only after both policy changes have been independently CI-validated and integrated to `main`; it cannot be generalized to other targets, moons, profiles, methods or batches.

**Finite envelope:** at most **twelve natural landings total in one Offense S1.42AK accepted-normal-stack campaign**, opportunistically checking the five currently viable/equal-100 basic-generation gaps (Black Mesa interior/`Black Mesa`, Crimson Keep/`CrimsonKeep`, Goldstay Hotel/`GoldenHotel`, Museum/`MelanieMuseum`, Shatteredrooms/`shatteredrooms`). Stop at the first targeted selection attempt with loggable outcome, material failure, or twelve landings. No target-forcing, owner-rule changes, RNG/seed manipulation, diagnostic reuse or automatic retry. A non-target or inconclusive result does not justify additional automatic landings. This exception deliberately authorizes **policy eligibility for later proposal only**; the user's separate, exact later approvals and machine gates for any Gale/profile use, controller or ingest attribution, actual gameplay, log/publication, and any other operation are not provided by approving or merging these Markdown rules.

**2026-10-24 owner-issued cap amendment:** The originally documented six-landing ceiling was subsequently raised by the owner to **twelve landings total for this same one-time campaign**, after the owner separately authorized its gameplay preparation and user execution. This is not twelve *additional* landings, a second batch or a new evidence method. The higher cap becomes canonically operative only after the two-file amendment here and in `Current/250_PHASE_C_DETERMINISTIC_INTERIOR_TEST_STRATEGY_AND_DEFERRED_BCMER_PIKMIN_DIRECTIVE.md` is merged and permanent exact-main CI succeeds. First-target-attempt and material-failure STOP rules, five target identities, unchanged S1.42AK profile and controller separation, V3 unarmed status, independent originalbyte/upload authorization, rights, owner, safety, retention and anti-loop constraints remain unchanged. Neither this documentation nor the user's bounded gameplay approval authorizes Gale import, controller mutation or uploading a future log.

**Anti-loop remains in force:** do not rerun exhausted historical log/source/acquisition analyses, poll for absent external bytes, reinterpret the same original as new, or revive blocked selector/CKDIAG1/owner fingerprints. A policy-approved *future acquisition* is not a retrospective qualified evidence event. Only a subsequently **new and authenticated original** can become an evidence-bearing event for re-entry after the campaign. Further stochastic batches are **not** automatically eligible, even if all five targets are missed; require a genuinely new qualifying event or a separate, explicit and substantively justified rule/safety revision. Current/250's deterministic requirement for targeted **single-interior** qualification, Current/412 Interior-first priority, P0–P6, rights, original-byte retention, and BMDSFIX1's unwaived passive proof remain intact.

### No-input polling prohibition and actionable recovery (mandatory)

**Hard STOP after a verified unchanged blocker.** A segment whose sole objective is to ask whether new evidence, uploads, administrator permissions, branch-protection settings, review duties or other external input have arrived is **forbidden** after that exact missing-input fingerprint has already been established. Never manufacture consecutive "check new evidence", "evaluate new input", "check protection again", or reworded status-only segments. The rule also applies to generic "weiter" messages, continuation buttons, repeated chat handovers and elapsed time. None of those creates an evidence event. Do not repeat an unchanged 403 endpoint or a historical log query. A genuinely explicit new current-state request may justify **one** narrowly scoped delta check, but is not permission to schedule serial polls.

**Replace the poll with this ordered, finite route, respecting the canonical selected subproject:**
1. **Specify the exact proof gap.** Distinguish missing authentic evidence, missing safely provable acquisition method, unavailable original bytes, missing rights/storage clearance, missing GitHub admin access, and required separate user permission. A green CI, documentation change or old hash does not establish generation or access.
2. **Reuse real existing inputs.** Consult the exact indexed repository/RuntimeEvidence/RuntimeInbox artifact, original source, or current-chat file only if relevant and not already exhausted. Check original byte availability at point of use; previous-chat file paths/hashes are not transferred bytes. Never demand an archived log again when the necessary source is actually available.
3. **Independently determine one novel feasible action.** When an authorized, materially different evidence-grounded method exists, define its precise target, achievable proof tier, provenance, risk/owner/rights/storage limits and STOP conditions. Execute its already permitted read-only portion, if any. If a new method requires source edits, PR, download, diagnostic hook/selector, build, publication, Gale or runtime/gameplay, **ask for its own specific authorization first** and preserve every technical safety guarantee. A hypothetical route or another stochastic reroll is not a PASS.
4. **Request concrete user cooperation immediately when essential.** If the exact evidence cannot be accessed independently and one user action is necessary, specify **the one exact artifact/version/source/hash or authenticated administrative attestation**, why it is required, what it will prove and cannot prove, and the permitted destination, privacy/rights/retention constraints. Offer an actual single-use repository upload procedure or build-specific PowerShell uploader only when the repository's established pipeline and rights permit it. One artifact should require at most one manual upload; reuse it rather than repeatedly asking. If an upload would not be lawful, request the rights/storage decision instead of the bytes. Never request an unnecessary re-upload or replay an already completed gameplay test.
5. **Park and wait if none is lawful.** Record `WAITING_FOR_EXTERNAL_INPUT / STOP`, the missing named action, unchanged blocker fingerprint and concrete re-entry event. Pursue genuinely independent permitted Interior-first prerequisites if known, but do not silently change the active subproject or scope. If no separate lawful task remains, stop completely; waiting is not a further execution segment, and no expected-success percentage or artificial milestone may be invented.

**Example: GitHub branch-protection 403.** After `Resource not accessible by integration`, neither `protected=false`, an empty ruleset list nor green PR-CI independently establishes all effective branch/review requirements. Do not try the same endpoint or relabel that check in another segment. Ask once for independently verifiable administrator-authoritative `main` protection/review/ruleset evidence or an actually granted appropriate access path; preserve the Draft PR and the failed fingerprint. No conditional earlier merge approval carries forward. Other Interior-first work remains subject to separate proof and permission gates.

**Continuation / segment-number guard.** A "weiter" after this wait-state **without providing the requested input or a distinct executable scope** receives a brief explanation of that exact outstanding user action, **no API check and no new numbered execution segment**. Keep the next pending ordinal unchanged. The mandatory functional "Weiter – Segment N+1" action must point to genuinely new permitted work or a specific request to obtain missing user cooperation/permission; it **must never submit a renamed "new evidence check" or blocked status poll**. If there is no other action available, explain that work cannot start until the named external input arrives. New chat handovers must preserve this wait-state rather than resetting the poll.

**Handover continuity:** Carry the last *actually verified* evidence-bearing event (or explicitly "none since <pinned baseline>"), relevant main SHA, source/log/commit identifier when applicable, parked method fingerprints and unresolved proof dimensions, whether the acquisition-pivot route is novel/parked, and the exact next qualified trigger. Never describe a historical upload/hash as newly available bytes, or turn "check for new evidence" into an automatic first segment when no event has occurred.

### STOP / new-chat landing UX continuity (mandatory)

**Execution STOP is not checkpoint/UI STOP.** At every user-facing project checkpoint or wait-state response, including actual project work, BLOCKED, WAITING_FOR_EXTERNAL_INPUT, final completion, handover, and subsequent no-input acknowledgements without a new execution segment, preserve the separate next-build/next-runtime readiness outlook, both visibly titled runtime-test visualizations, Completed / Findings / Remaining / Next segment, and the functional Weiter, handover and (where precisely permissible) authorization controls. These are presentation duties, not permissions or completed readiness gates.

**Handover-only landing without a segment.** If the first message in a new chat supplies only a completed repository-native handover and no distinct executable project task, do not invent Segment 1, perform a status-only bootstrap/API poll or silently continue into project execution. Instead present a segment-free landing checkpoint from the explicitly identified handed-over evidence, clearly marked "handover snapshot / not independently reverified in this chat". Render both named visualizations and the separate next-build/next-runtime outlook with indeterminate readiness wherever the target or denominator is not established; show the exact missing input or approval and functional navigation/approval controls. Read the mandatory bootstrap in its fixed order when a later actual project-work segment begins.

**Action and ordinal guard.** A Weiter control may submit only materially distinct authorized work or a precisely identified decision/cooperation request, never an unchanged-input poll. A request for clarification or consent does not consume the pending segment ordinal. An approval control submits one explicit narrowly scoped new user message; it never executes a protected operation on click. If there is no lawful executable next task, retain the checkpoint and available decision/handover controls, state the re-entry condition and STOP. Neither presentation nor consent bypasses review, merge, rights, owner, safety, original-byte, controller, build, publication, Gale, runtime or gameplay gates.

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

- **"Weiter – Segment N+1: <konkrete Aktion>"**: the visible label must contain the next consecutive chat-local ordinal and approximately two or three concrete German action words after the colon. This control submits a new user continuation turn and requests only the next **repository-authorized bounded work**, potentially up to the two-segment in-response window if the continued work remains within already granted scope. It never grants new mutation/build/runtime/merge rights. When the next action is unestablished or blocked, label the short determination honestly (e.g. "Freigabe klären") rather than suggesting forbidden actions. **Do not send a continuation message that only checks for new external input on a previously verified identical blocker.** Instead request the one exact missing user action or select a genuinely distinct lawful task. An input-free acknowledgement must not consume a new segment number. Keep this button even after work-package completion.
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
