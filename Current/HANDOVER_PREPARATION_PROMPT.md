# Current ChatGPT Handover Preparation Prompt

**Status:** CURRENT / CANONICAL HANDOVER PROCEDURE  
**Authority:** procedure the active ChatGPT chat must execute when the user requests transfer to a new ChatGPT chat  
**Canonical-For:** `chat_handover_preparation`, `fresh_new_chat_prompt_generation`  
**Execution cadence:** `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`  
**Machine State:** `Current/CURRENT_STATE.json`  
**Topic Router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Last-Validated:** 2026-09-10

## Purpose

Use this workflow when the user explicitly asks to transfer the project to a new ChatGPT chat. The repository is the Source of Truth; do not reconstruct the handover from conversation memory or an old static handover snapshot.

This workflow deliberately does **not** hard-code the current accepted build, candidate, hashes, runtime gate, controller state or exact next action. Those volatile facts belong in `Current/CURRENT_STATE.json` and the canonical topic/evidence graph.

## Mandatory segmented execution

The handover is subject to `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`.

For non-trivial handover work, execute bounded segments with numbered checkpoints. Up to two already-authorized handover preparation segments may run within a single assistant response, with a brief internal checkpoint, provided all time/context and authorization guards in the segmented policy hold. At the end of each assistant response report Completed / Findings / Remaining / Next segment with both required visualizations and functional controls, then stop and wait for the user's explicit continuation signal. Never automatically create a new chat or infer permission for repository mutations from a handover request. A genuinely short atomic handover may be one segment. Do not split an atomic repository repair into a knowingly inconsistent checkpoint.

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

### Evidence-event continuity and anti-dead-end entry gate

When the handover follows an exhausted or blocked evidence path, preserve a compact **last-verified evidence-event checkpoint**, not a generic task to search again. Record the pinned main SHA; the latest actually authenticated, relevant evidence event (commit/log/index/source/user artifact with exact identifier and provenance), or **"no new evidence-bearing event since <baseline>"**; the exact parked target/method/source/guarantee fingerprints and unproven proof tiers; and the smallest qualified re-entry trigger. Distinguish a new relevant event from unchanged CI, a mere elapsed date, and a handover-created new chat. A narrow GitHub delta may establish that the event has not occurred; do not re-run historical evidence queries, speculative source searches or exhausted safety arguments.

If no qualified trigger exists, **do not prescribe renewed evidence searching as the next chat's automatic first task**. Route the next decision, if materially new and safe, to a bounded **evidence-acquisition planning** choice under the segmented policy: target, actual missing proof, authentic source/provenance, rights/storage/retention, intervention class and STOP criteria, smallest required user action, and independently authorized downstream gates. If that planning route also matches a parked fingerprint, explicitly mark no lawful forward action and STOP until an identified event or separately permissible decision exists. Neither a handover nor the plan authorizes implementation, source download, runtime, gameplay or publication.

**Mandatory no-polling handover gate:** A blocked integration or evidence path is not an instruction to keep watching for a change which cannot appear without a real external action. The next chat **must not** start or offer subsequent segments labeled "check for new evidence", "check new permissions", "assess new input" or any synonym if the identified external evidence has not actually been supplied. A generic "weiter", chat change, unchanged main or old CI is not such input. Route instead to one materially different independently scoped permitted evidence-acquisition step, or proactively ask the user **once** for the exact missing original with version/hash and lawful one-upload pipeline, or independently verifiable admin evidence/permission, as applicable. If none is available, record `WAITING_FOR_EXTERNAL_INPUT / STOP` and the precise re-entry event. Repeated continuations without that input receive only a concise reminder and **do not create another numbered segment or API call**. Keep the pending ordinal unchanged. Do not make the user's inaction into a segment generator; all safety, rights, original-byte, CI and explicit authorization requirements continue to apply.

## Step 2 — Verify repository, CI and controllers

Before the final handover output, verify directly:

- current `main` HEAD;
- latest relevant `Knowledge Architecture` **exact-head** run for that HEAD and whether every permanent gate passed. For ordinary commits this must be a `push` run. A `workflow_dispatch` run is acceptable only for a bot-generated follow-up commit when repository workflow wiring explicitly dispatches Knowledge Architecture because GitHub suppresses recursive `GITHUB_TOKEN` push workflows; its `head_sha` must exactly equal final `main`;
- open relevant PRs;
- `BuildSpecs/current.json`;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- agreement of those controllers with `Current/CURRENT_STATE.json` and the routed lifecycle/topic authority;
- any hashes or evidence paths that are material to the exact next action.

For a bot-generated follow-up from `.github/workflows/profile-index.yml` **or** `.github/workflows/runtime-ingest.yml`, verify the explicitly registered exact-head `workflow_dispatch` run rather than pretending a `push` run exists. Both workflows must fail closed if `main` moves before dispatch or if no Knowledge Architecture run is registered for the exact generated head. `RuntimeInbox/ACTIVE_BUILD.txt` is runtime-active/evidence-attribution state, not acceptance authority. Do not claim CI proves runtime/gameplay behavior beyond documented validator coverage.

### Cross-chat attachment inventory (required for the immediate next task)

Before producing PART 2, identify only attachments/original-byte inputs **actually needed for the next authorized segment**. Prior-chat uploaded ZIP/DLL/log/other files and sandbox paths **do not transfer to new chats by default**. Classify each as **repository-accessible original bytes (path verified)**, **current-chat-only attachment (NOT TRANSFERRED)**, or **metadata/derived evidence only (original bytes unavailable)**. Preserve filename, exact version and pinned SHA-256 for any material input, and distinguish independently verified current bytes from historical chat evidence.

If the next action needs a current-chat-only original, explicitly instruct the new chat to check repository/current-chat byte access first and, if missing, **immediately ask the user to re-upload that specific file** before attempting the byte-dependent work. If repository evidence already suffices, do not require an unnecessary upload. Never suggest that copying a filename, hash or previous sandbox link transfers an attachment. Do not silently initiate a new download; respect separate acquisition and mutation authorizations.

## Step 3 — Repair only genuine drift

If the repository is already internally consistent and a fresh chat can continue from the current authorities, do not create a cosmetic handover commit.

If genuine handover-critical drift exists:

1. preserve historical evidence;
2. repair the canonical current authority or validator contract instead of rewriting history;
3. do not change gameplay/config/profile/runtime behavior solely for handover cleanup;
4. use a dedicated branch and PR;
5. merge only after the relevant CI gate is green;
6. verify the resulting `main` exact-head gate before the final handover.

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
- final relevant green exact-head CI run, its event type, and permanent-gate result;
- whether a relevant open PR remains;
- whether repository repair was required;
- any material controller/runtime fact that cannot be safely inferred by simply reading `Current/CURRENT_STATE.json`;
- whether the user must perform any manual repository action.

If no repository change was needed, say so explicitly.

Do not duplicate the accepted baseline, latest artifact, candidate, every SHA, runtime gate and exact next action merely because they exist. Point to `Current/CURRENT_STATE.json` for the complete volatile state, and repeat a live fact only when it materially prevents ambiguity in the handover.

### PART 2 — READY-TO-COPY START PROMPT FOR THE NEW CHAT

Generate a fresh, compact prompt from the just-verified repository.

The new-chat prompt must:

- declare the repository as the complete Source of Truth;
- instruct the new chat to read `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` before performing project work;
- require bounded segments, checkpoint reporting and waiting for user continuation between non-final segments;
- use this initial read order: `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`, `Current/CURRENT_STATE.json`, `Current/PROJECT_KNOWLEDGE_MAP.md`;
- **require a segment-free landing checkpoint when PART 2 is pasted without an independently authorized executable task**: before STOP, show the carried-forward baseline explicitly as not freshly verified in the new chat, separate next-build and next-runtime readiness, both exact-titled visualizations "Fortschritt bis zum nächsten Runtime-Test" and "Pipeline als Ablaufkette bis zum nächsten Runtime-Test", and functional Weiter / Übergabe / precisely scoped Freigabe controls as applicable. Do not start Segment 1, perform no-input polling, imply a new approval, or advance the ordinal; start the ordered bootstrap and Segment 1 only on a later concrete project-work request.
- include the final verified `main` commit and relevant green exact-head CI run; if the exact-head run is the allowed bot-follow-up `workflow_dispatch`, state that event type explicitly rather than describing it as a push run;
- tell the new chat to route the task through the Topic Router and read only the required canonical topic/evidence;
- tell the new chat not to perform a full-repository audit by default and not to treat historical "current" wording as live authority;
- preserve the runtime import/uploader rule and the completed-log rule;
- tell the new chat not to require local clone/build work while repository-native infrastructure is sufficient;
- identify any exact next-segment original ZIP/DLL/log or other attachment that existed only in the previous chat; mark it **NOT TRANSFERRED** and include required filename/version/SHA-256, instructing the new chat to verify accessible repository/current-chat bytes first and, if genuinely missing and needed, **actively ask the user to re-upload it** before byte-dependent work (do not substitute provenance-only records, previous sandbox paths or unapproved downloads);
- explicitly state that when the user later signals another handover, it must execute `Current/HANDOVER_PREPARATION_PROMPT.md` under the segmented-execution policy.
- carry forward the pinned last evidence-bearing event or explicit **no new event since baseline**, all relevant parked target/method/source/guarantee fingerprints, unresolved proof tier and exact qualified re-entry trigger; never automatically start with another evidence search absent such a trigger;
- when evidence is missing, determine the precise previously unexhausted and safe acquisition action if one exists; otherwise proactively request the **one** necessary file/version/hash and safe one-upload pathway, or verifiable admin permission/protection evidence, or record **WAITING_FOR_EXTERNAL_INPUT / STOP**. Never create a "check for new input/permission" segment or continuation-button action, and never increment the chat-local segment counter for a no-input acknowledgement.

Do not copy the entire live-state object into the ready-to-copy prompt. The new chat is required to read `Current/CURRENT_STATE.json`, which is the canonical volatile state.

 
### Final handover action buttons

After **PART 2** contains the complete start prompt, show two functional controls: `Weiter – <next permitted project step>` and **`Übergabe-Prompt kopieren`**. The second control must perform a real clipboard-copy action on click (for example `GenUI.copy(fullNewChatStartPrompt)`), copying **exactly all of PART 2's new-chat prompt**, not PART 1, explanatory text, formatting controls or an abbreviated variant. Do **not** show `Übergabe an neuen Chat` or `Übergabe erneut vorbereiten` after the final handover is already prepared. Neither button opens a new ChatGPT chat; the user pastes the copied text into a separate new conversation. Do not claim a clipboard copy happened until confirmed by the host. If native copy actions are unsupported, present the prompt as directly selectable text for manual copying instead of a fake button; keep the `Weiter` action available.

At all **ordinary non-handover segment checkpoints**, keep the established `Weiter` + `Übergabe an neuen Chat` pair. This is a handover-UX change only; all PR, CI, controller and segmented-execution requirements remain in force.


## Integrity rules

During handover:

- never promote or reject a build implicitly;
- never treat `RuntimeInbox/ACTIVE_BUILD.txt` as acceptance authority;
- never fabricate missing provenance;
- never claim that a `workflow_dispatch` exact-head run was a `push` run;
- never rewrite historical evidence merely to make search results look clean;
- never create a successor merely to make the handover appear active;
- never bypass the continuation gate when safe segmentation is available.

## Maintenance contract

Update this workflow only when the handover process, authority model, validation policy, segmented-execution policy or mandatory runtime UX changes. Ordinary build/runtime progression should update canonical state/evidence instead.

This workflow must remain discoverable from `README.md`, `START_HERE_ChatGPT_Masterprompt.txt`, `Current/01_HANDOVER_CORE.md`, `Current/PROJECT_KNOWLEDGE_MAP.md` and `Current/DOCUMENT_AUTHORITY.md/.json`.
