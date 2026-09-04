> **EXECUTED CONTRACT SNAPSHOT — OVERHAUL COMPLETE / VALIDATED**
> This document preserves the original execution playbook. Its original `PLANNED / NOT YET EXECUTED` wording below is historical text, not live state. Completion authority: `Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md`; machine result: `Current/OVERHAUL_VALIDATION_RESULTS.json`.

# 105 — Repository Overhaul Execution Playbook

**Date:** 2026-09-04  
**Status:** PLANNED / BINDING EXECUTION PROCEDURE / NOT YET EXECUTED  
**Authority:** execution companion to `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`  
**Canonical-For:** how a future ChatGPT session must execute the repository overhaul  
**Related:** `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

## Purpose

This file exists so a future fresh ChatGPT session can execute the repository overhaul correctly even when the original planning conversation is unavailable and the chat context is limited.

The overhaul is not a generic cleanup. It is a controlled migration from a chronology-heavy repository into a retrieval-hardened knowledge architecture while preserving every important fact, provenance link, runtime record, build artifact and historical explanation.

A future ChatGPT session must treat this playbook, `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, and `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json` as a single binding contract.

## Trigger rule

When the user explicitly asks to start, perform, execute, begin or carry out the repository overhaul/rework/restructure, the new ChatGPT session must:

1. use the GitHub repository as Source of Truth;
2. read this file completely;
3. read `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md` completely;
4. read `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json` completely;
5. read the then-current `README.md`, `START_HERE_ChatGPT_Masterprompt.txt`, `Current/00_CURRENT_STATE.md`, `Current/01_HANDOVER_CORE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, current project-status JSON, `BuildSpecs/current.json`, and `RuntimeInbox/ACTIVE_BUILD.txt`;
6. determine whether any gameplay/runtime/build gate is active;
7. do not perform structural changes until the mandatory standalone backup gate has passed;
8. execute the phases below in order and keep the repository usable between phases.

Do not ask for a local repository clone or local profile build merely to perform this documentation/information-architecture work while GitHub-native access is sufficient.

## Non-negotiable principles

- Preserve information before optimizing structure.
- Preserve provenance before reducing duplication.
- Current truth and historical truth must be distinguishable without deleting history.
- Search is fallback; explicit routing is primary.
- Important future reasoning must not depend on opaque binaries alone.
- Never silently change gameplay behavior, configs, mod versions, profile content or project-local patch behavior as part of this repository overhaul.
- Do not combine the overhaul with gameplay balancing, bug fixes, mod upgrades or a new runtime candidate.
- Do not delete a file merely because it appears redundant until its unique facts, inbound references, provenance role and historical value have been checked.
- Prefer redirects/classification over destructive removal when uncertain.
- At every phase, the repository must still identify the accepted baseline, active candidate if any, exact next step, controllers and rollback source unambiguously.

## Phase 0 — Establish the exact pre-overhaul project state

Before changing repository structure:

1. resolve the current default branch and exact HEAD commit SHA;
2. identify current accepted baseline and any active candidate;
3. verify `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt`, current project-status JSON and any `AUTO_BUILD_RESULT` are mutually consistent;
4. record whether a runtime test/build is currently open;
5. if an active gameplay gate exists, do not blur its technical attribution. Prefer closing that gate first unless the user explicitly directs otherwise;
6. produce an inventory of top-level folders and canonical/current documents;
7. record the pre-overhaul HEAD as the frozen source checkpoint.

No structural migration is permitted before Phase 1 passes.

## Phase 1 — Mandatory standalone pre-overhaul backup

This is a hard gate.

### Required backup properties

- Backup must be a **separate standalone GitHub repository**.
- A branch, tag, release or backup folder inside the primary repository is not sufficient by itself.
- Prefer a mirror-style repository copy preserving full Git history, branches and tags where technically practical.
- The backup must include the complete recovery-relevant tree: documentation, profiles, ProfileSources, RuntimeEvidence, BuildSpecs, patches/source, workflows, runtime tools, repository tools and other tracked project files.
- The backup repository must be clearly labeled historical/read-only and must state that the primary repository remains Source of Truth.
- Do not continue normal development in the backup repository.

### Required verification

Do not accept backup success merely because the target repository exists.

At minimum verify:

- frozen source repository + source commit SHA;
- backup repository identity;
- backup default-branch commit/tree correspondence;
- tracked file/tree equivalence to the frozen source checkpoint;
- history/branch/tag preservation status;
- important large/profile/evidence paths are present;
- any exclusions/limitations are explicitly documented.

Create `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json` in the primary repository only after verification. It must contain at least:

- `source_repository`;
- `frozen_source_commit_sha`;
- `backup_repository`;
- `backup_default_branch_commit_sha`;
- `backup_datetime`;
- `backup_method`;
- `history_branches_tags_preserved`;
- `verification_result`;
- `exclusions_or_limitations`.

The backup repository must also contain reciprocal provenance identifying the primary repository and frozen checkpoint.

**STOP CONDITION:** if the backup cannot be created or verified, stop the structural overhaul. Do not proceed by assuming a normal Git tag is good enough.

## Phase 2 — Inventory and knowledge extraction before moves

Before renaming/moving/deleting historical files, build an inventory of what knowledge exists.

For every meaningful current/historical document family determine:

- what topic(s) it contains;
- whether content is current, historical, evidence, policy, plan, acceptance, rejection, diagnostic or machine state;
- whether it contains unique facts not repeated elsewhere;
- inbound and outbound references;
- related build IDs;
- related config/code/runtime evidence;
- whether stale `current` wording exists;
- whether it should remain, be classified, be split, become a redirect/stub, or eventually be removed after proven duplication.

Primary known refactor targets include:

- `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` because it mixes binding long-term rules with historical S1.42U/S1.42V checkpoint language;
- `Current/02_TECHNICAL_BASELINE.md` because older subsections contain stale `current` wording;
- historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` that no longer perfectly describe the accepted later behavior.

Do not alter accepted runtime behavior while resolving documentation drift.

## Phase 3 — Create the new navigation layer before removing old navigation

Create new navigation artifacts first so the repository never enters a state where information is less discoverable than before.

Required artifacts:

- `Current/PROJECT_KNOWLEDGE_MAP.md` — human-readable topic router;
- `Current/PROJECT_KNOWLEDGE_MAP.json` — machine-readable topic router;
- human-readable build lineage;
- machine-readable build lineage;
- redirect/supersession map if paths are moved;
- stable topic documents under `Knowledge/` or an equivalent semantic location as appropriate.

### Knowledge-map entry requirements

Each major topic should expose:

- stable topic ID;
- title;
- natural-language aliases/user vocabulary;
- technical aliases, GUIDs/package names/config names where useful;
- canonical current document;
- machine-readable state source when applicable;
- evidence/runtime source;
- config paths;
- code/patch paths;
- related builds;
- historical sources;
- related topics;
- authority/status;
- last validation date.

Aliases must account for how the user actually asks questions, not only internal technical terminology.

Minimum topic coverage is defined in `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json` and includes current baseline, candidate/next test, build pipeline, Gale import, runtime logs, BCMER, interiors/LLL/CullFactory, enemy spawn baseline, Pikmin compatibility, Jetpack, CodeRebirth, Microwave, Immortal Snail, monitor-only errors, Black Mesa routing, roadmap, patch safety, overhaul and backup/recovery.

## Phase 4 — Build lineage and authority graph

Create a build lineage that lets a fresh chat answer historical questions without reading every handover.

For each meaningful build record:

- build ID/title;
- status (`planned`, `build-pass`, `runtime-pass`, `accepted`, `rejected`, `superseded`, `diagnostic-only` etc.);
- parent/base build;
- profile path and SHA-256;
- build plan;
- candidate record;
- acceptance/rejection record;
- runtime evidence + raw-log hash when available;
- workflow run/build commit;
- exact delta summary;
- `supersedes` / `superseded_by` relationships;
- safe/unsafe as gameplay base;
- principal feature/fix introduced.

Canonical/topic documents should use formal authority metadata where practical:

- `Status`;
- `Authority`;
- `Canonical-For`;
- `Supersedes`;
- `Superseded-By`;
- `Topics`;
- `Evidence`;
- `Related`;
- `Last-Validated`.

Historical documents retaining obsolete `current` wording must be visibly classified as historical, e.g. `HISTORICAL SNAPSHOT — NOT CURRENT AUTHORITY`.

## Phase 5 — Separate live truth from chronology

After the knowledge map and lineage exist:

- make `Current/` small and genuinely current/controller-facing;
- place stable long-lived topic knowledge in `Knowledge/` or equivalent;
- keep historical handovers, diagnostics and experiments as evidence/history;
- split live roadmap from old checkpoints;
- ensure no active invariant depends solely on an old chronological handover;
- reduce duplicate current-state prose across README/START_HERE/00/01/04;
- keep README and START_HERE compact routing/bootstrap documents rather than giant duplicated state dumps.

Target bootstrap retrieval path:

`README / START_HERE -> Current State + Knowledge Map -> Topic Canonical Source -> Evidence / Config / Code / History`

Target: any major current topic reachable in **at most three document hops** from bootstrap.

## Phase 6 — Binary and large-evidence retrieval hardening

Verify that important facts do not exist only in opaque files.

Required permanent rules:

- every active/accepted `.r2z` has `ProfileSources/<build>/` readable snapshot;
- every active/accepted profile snapshot has `FILE_INDEX.json`;
- important project-local DLLs have source/build records and SHA-256 provenance;
- large logs have indexed/summarized `RuntimeEvidence` while preserving raw logs;
- if a future decision depends on a binary-only fact, extract/index that fact into readable repository evidence.

## Phase 7 — Redirects, reference migration and deletion discipline

For every move/rename:

- update canonical references;
- preserve old paths as redirect/stub documents where useful or record redirects machine-readably;
- ensure historical inbound references do not become dead ends;
- do not delete a source until all unique facts are migrated and references validated.

Deletion rule:

A file may be removed only when there is positive evidence that it contains no unique fact/provenance needed for future reasoning, no unresolved inbound reference, and no historical recovery value that is not preserved elsewhere. When uncertain, retain/classify it.

## Phase 8 — Repository knowledge validator and CI

Implement repository-native validation, e.g. `RepositoryTools/validate_knowledge_architecture.py`, and CI execution.

Validator must cover at minimum:

- all canonical/current referenced paths exist;
- knowledge-map targets exist;
- no orphan canonical/current documents;
- exactly one authoritative current accepted-baseline declaration;
- exactly one authoritative current active-candidate declaration when applicable;
- human/machine current state consistency;
- `ACTIVE_BUILD`, candidate state, `AUTO_BUILD_RESULT` and `BuildSpecs/current.json` lifecycle consistency;
- BuildSpecs guarded base profile/SHA correctness;
- active/accepted profiles have readable snapshots + FILE_INDEX;
- runtime evidence references exist;
- build lineage and supersession/redirect targets resolve;
- live roadmap does not nominate superseded builds as current;
- bootstrap/read-first size/routing remains bounded;
- standalone backup manifest exists for this overhaul and proves backup predates first structural overhaul change.

The validator should fail CI on broken knowledge architecture rather than leaving drift for a future chat to discover manually.

## Phase 9 — Answerability / routing regression suite

Create `RepositoryTools/answerability_cases.json` or equivalent.

The suite should map representative natural-language questions/aliases to expected topic IDs/canonical sources. It must include at least questions equivalent to:

- What is the current accepted build?
- What must I test now?
- Where is the exact log uploader?
- Which BCMER version is allowed?
- Are BCMER EventTypes equally likely?
- What is the Thumper Bite Limit?
- Why is Shatteredrooms restricted on Experimentation/Embrion?
- What happened with Black Mesa/Pikmin routing?
- How are interior weights normalized?
- Where does Jetpack acceleration come from?
- Which errors are monitor-only?
- How do I import a Gale build?
- Where is the pre-overhaul repository backup?
- Which build introduced/rejected a given fix?

This tests routing, not prose quality. A fresh model should reach the expected canonical source without reading the entire repository.

## Phase 10 — Atomic state-transition hardening

Reduce manual duplication of changing state.

Where practical, derive/update current navigation from one structured source so acceptance/rejection/build transitions update together:

- accepted baseline;
- active candidate;
- next action;
- build lineage current pointer;
- knowledge map pointers;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- `BuildSpecs/current.json`;
- README/START_HERE compact state pointers.

Do not leave five independently edited prose files as the only synchronization mechanism if generation/validation can prevent drift.

## Phase 11 — Final migration verification

Before declaring success:

1. run the knowledge validator;
2. run answerability/routing cases;
3. validate all canonical links/pointers;
4. validate build lineage coverage;
5. validate accepted/current controller state;
6. validate active/accepted ProfileSources/FILE_INDEX coverage;
7. validate runtime evidence references;
8. validate backup manifest and recovery repository accessibility;
9. confirm README/START_HERE bootstrap is compact;
10. manually sample both current and historical questions and confirm deterministic routing;
11. compare against the pre-overhaul backup to confirm no required information disappeared;
12. document known intentional exclusions/remaining limitations.

## Overhaul acceptance criteria

Do not call the overhaul complete until all criteria in `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md` and `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json` pass.

Key gates include:

- verified standalone pre-overhaul backup;
- backup manifest present;
- all major topics indexed;
- zero broken canonical references;
- zero orphan canonical/current documents;
- one authoritative accepted baseline and active-candidate declaration;
- explicit current-vs-history authority;
- meaningful build lineage complete;
- major current topics <= 3 hops from bootstrap;
- readable active/accepted profile snapshots;
- answerability regression PASS;
- CI knowledge validator PASS.

## Rollback / abort rule

If the new structure loses information, produces ambiguous authority, breaks routing, cannot pass validation, or becomes less usable for fresh ChatGPT sessions:

- stop further migration;
- compare against the standalone pre-overhaul backup;
- restore missing information/references;
- if necessary revert the primary repository to the frozen checkpoint and redesign the migration;
- never continue deleting/moving files merely to finish the planned shape.

The independent backup is the authoritative recovery reference for what existed before the overhaul, not the new current Source of Truth for ongoing project development.

## Required completion records

When the overhaul eventually completes, create at least:

- a final overhaul implementation/acceptance report;
- updated machine-readable requirements status;
- final knowledge map MD + JSON;
- final build lineage MD + JSON;
- final backup manifest;
- validator and test results;
- list of moved/redirected/deleted files with rationale;
- explicit statement of any information intentionally omitted and why;
- fresh takeover instructions for a new ChatGPT session under the new architecture.

## Handover requirement during the overhaul

If the overhaul spans multiple ChatGPT chats, the current chat must update repository state before handover so the next chat can resume from the exact phase/checkpoint without relying on conversation memory.

Each handover must record:

- last completed phase;
- current phase;
- changes already committed;
- validation status;
- unresolved issues;
- backup repository + frozen checkpoint;
- exact next operation;
- files that must not yet be moved/deleted;
- whether rollback remains cleanly possible.

Do not rely on the previous chat transcript as the only record of overhaul progress.

## Current timing constraint

As of creation of this playbook, S1.42AC is the active runtime candidate and S1.42AB is the accepted baseline. The overhaul is planned but **must not disturb or become mixed with the S1.42AC runtime-validation gate**.

When a future user starts the overhaul, re-read the then-current project state. Do not assume S1.42AC is still current merely because this historical execution playbook was authored during that gate.
