# 104 — Repository Overhaul: ChatGPT Retrieval and Information Architecture Plan

**Date:** 2026-09-04  
**Status:** PLANNED / BINDING OVERHAUL REQUIREMENTS / NOT YET EXECUTED  
**Purpose:** make the repository reliably navigable and answerable for fresh ChatGPT sessions with limited context.

## Why this overhaul exists

The repository is already the canonical source of truth and is usable for project continuation. It has strong current-state files, build/runtime evidence, readable profile snapshots, machine-readable project states and repository-native automation.

However, the current documentation architecture grew chronologically during rapid iteration. As a result:

- current facts are repeated across README, START_HERE, Current/00, Current/01, Current/04 and build-specific handovers;
- historical and current wording can coexist in the same large document;
- long `Read first` lists require more context than should be necessary;
- some historical files still contain stale `current` wording that is only overridden by newer authority rules;
- topic discovery sometimes depends on repository/code search, whose index can be incomplete or whose query wording may not match the document vocabulary;
- a fact may be retrievable if its exact path is known but not yet deterministically discoverable from a compact bootstrap context.

The overhaul must therefore be treated as **information architecture and retrieval hardening**, not merely cosmetic documentation cleanup.

Do not destroy historical evidence to make the repository look cleaner. The goal is to separate navigation/current truth from chronology while preserving provenance.

## Target capability

After this overhaul, a fresh ChatGPT session that can access the repository should be able to start from a small canonical bootstrap set, resolve the user's question to a topic, follow explicit pointers to the authoritative current source, and then open evidence/history only when needed.

The intended retrieval path is:

`README / START_HERE -> CURRENT STATE + KNOWLEDGE MAP -> TOPIC CANONICAL SOURCE -> EVIDENCE / CONFIG / CODE / HISTORY`

Repository search must be a fallback, not the primary navigation mechanism.

## Operational answerability contract

Absolute logical omniscience cannot be guaranteed merely by file layout. The repository can, however, provide a strong deterministic operational guarantee for knowledge that is actually stored and indexed.

The overhaul is complete only when all of the following are true:

1. every canonical/current document is registered in the repository knowledge map;
2. every major project topic is reachable from the bootstrap/knowledge map in at most three document hops;
3. every canonical claim points to its evidence, config/source path or accepted runtime record where applicable;
4. there are zero broken internal file references in canonical/current documents;
5. there are zero orphan canonical/current documents;
6. there is exactly one authoritative current accepted-baseline declaration and one authoritative active-candidate declaration, with machine-readable mirrors;
7. conflicts between current and historical wording are deterministically resolvable through explicit authority/supersession metadata, not only chronology intuition;
8. every build has a lineage/status entry identifying its base, profile, SHA-256, candidate record, acceptance/rejection/open state and runtime evidence when present;
9. every accepted or active binary `.r2z` has a readable `ProfileSources/<build>/` snapshot and `FILE_INDEX.json` so binary-only information is not hidden from text retrieval;
10. large runtime logs remain discoverable through indexed/summarized RuntimeEvidence, with raw logs opened only when necessary;
11. automated validation rejects broken knowledge-routing state;
12. representative user questions pass an answerability/routing regression suite.

If a fact exists only inside an unindexed binary, deleted external source, inaccessible artifact or malformed file, this contract does not magically make it retrievable. Such cases must instead be converted into readable/indexed repository evidence.

## 1. Compact bootstrap layer

The final architecture should require only a small initial context set. Target bootstrap files:

- `README.md` — repository identity and one-hop routing only;
- `START_HERE_ChatGPT_Masterprompt.txt` — compact takeover protocol and immediate state pointer;
- `Current/00_CURRENT_STATE.md` — sole concise human-readable current-state summary;
- `Current/PROJECT_KNOWLEDGE_MAP.md` — human topic router;
- `Current/PROJECT_KNOWLEDGE_MAP.json` — machine-readable router.

The bootstrap layer must not duplicate full technical histories. It should tell ChatGPT **where to look next**.

Target context budget: the bootstrap set should remain intentionally compact; implementation should establish and CI-enforce a reasonable combined size budget rather than allowing unlimited growth. Topic detail must be loaded on demand.

## 2. Project knowledge map

Create a permanent topic index with stable topic IDs. Each entry should contain at least:

- topic ID;
- human title;
- aliases and likely user/search vocabulary;
- canonical current document;
- machine-readable state file when applicable;
- evidence/runtime source;
- relevant config path(s);
- relevant code/patch path(s);
- related build IDs;
- related mod/package/GUID names;
- historical sources;
- related topics;
- authority/status;
- last validation date.

The aliases must include ordinary user phrasing and technical names so retrieval does not depend on remembering the exact repository vocabulary.

Minimum topic coverage should include:

- current accepted baseline;
- active candidate / exact next test;
- build pipeline;
- Gale profile replacement/import;
- runtime upload/ingest/log querying;
- BCMER configuration/events/rain guards/EventTypes;
- interiors/LLL/equal-weight architecture/CullFactory;
- enemy spawn baseline;
- Pikmin/Thumper/Puffer/Baboon Hawk compatibility;
- Jetpack tuning;
- CodeRebirth tuning;
- Functional Microwave;
- Immortal Snail;
- known monitor-only errors;
- Black Mesa/Pikmin routing evidence;
- roadmap / deferred scopes;
- project-local patch safety policy;
- repository overhaul itself.

## 3. Formal document authority metadata

Canonical and topic documents should use a standard metadata header where practical:

- `Status`;
- `Authority`;
- `Canonical-For`;
- `Supersedes`;
- `Superseded-By`;
- `Topics`;
- `Evidence`;
- `Related`;
- `Last-Validated`.

Historical files that retain obsolete `current` language must receive a conspicuous historical banner such as:

`HISTORICAL SNAPSHOT — NOT CURRENT AUTHORITY`

Do not rewrite historical evidence in a way that destroys what was known at that time. Add classification/routing around it instead.

## 4. Separate current truth from chronology

A current answer should not require reconciling dozens of chronological handover files.

During the overhaul:

- preserve chronological build/handover/acceptance records as evidence;
- move or clearly classify them as history/evidence where appropriate;
- create stable topic documents for long-lived rules;
- ensure current state points to topic documents rather than copying their full contents;
- avoid historical files serving as the sole source for a still-active invariant.

The existing `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` is a primary refactor candidate because it intentionally mixes binding long-term rules with historical checkpoints such as S1.42U/S1.42V. Preserve the evidence, but split live roadmap/topic truth from historical chronology so a model does not need to reconcile old and new `current` sections.

The known drift in `Current/02_TECHNICAL_BASELINE.md` and historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` must also be resolved/classified during this stage without changing accepted runtime behavior.

## 5. Build lineage index

Create a human and machine-readable build lineage/index covering every meaningful S1.x build.

Each build entry should include:

- build ID and title;
- status: planned / build-pass / runtime-pass / accepted / rejected / superseded / diagnostic-only;
- exact base build/profile;
- profile path and SHA-256;
- BuildSpec/plan;
- candidate record;
- acceptance or rejection record;
- runtime evidence root and raw-log hash when available;
- automated build commit/run;
- exact delta summary;
- `supersedes` / `superseded_by` relationships;
- whether it is safe as a gameplay base.

This must make questions such as "Was war vor S1.42AB?", "Warum wurde AA verworfen?" or "Welcher Build hat Fix X eingeführt?" answerable without opening every handover sequentially.

## 6. Stable topic paths and redirect policy

Prefer stable semantic topic files for long-lived knowledge instead of relying only on numbered chronological filenames.

If files are moved or renamed:

- preserve old paths as lightweight redirect/stub documents where useful, or maintain a machine-readable redirect map;
- update all canonical references;
- validate that historical links still resolve;
- never silently strand older handovers.

## 7. Binary and large-file discoverability

ChatGPT/repository text retrieval cannot be assumed to semantically inspect arbitrary binary archives.

Permanent rule:

- every accepted and active candidate `.r2z` must have a readable `ProfileSources/<build>/` snapshot;
- `FILE_INDEX.json` must identify all archive members and hashes;
- important binary DLLs must have source/README/build records plus SHA-256;
- large runtime logs must be represented by RuntimeEvidence summaries/indexes while retaining raw evidence;
- if information matters for future reasoning, it must not exist only in an opaque binary.

## 8. Automated repository knowledge validator

Add a repository-native validation script/workflow, e.g. `RepositoryTools/validate_knowledge_architecture.py`, and run it in CI.

At minimum validate:

- every path referenced by canonical/current documents exists;
- every knowledge-map canonical target exists;
- no canonical/current file is orphaned from the map;
- no duplicate/conflicting current accepted-baseline declarations;
- no duplicate/conflicting active-candidate declarations;
- `RuntimeInbox/ACTIVE_BUILD.txt`, candidate state, `AUTO_BUILD_RESULT`, and `BuildSpecs/current.json` are mutually consistent for the current lifecycle stage;
- BuildSpecs guarded base path/SHA matches the intended profile;
- every active/accepted profile has `ProfileSources/<build>/FILE_INDEX.json`;
- runtime evidence roots referenced by accepted/rejected states exist;
- build lineage links resolve;
- supersession/redirect targets resolve;
- live roadmap pointers do not nominate a superseded build as current;
- bootstrap/read-first routing does not expand without bound.

The validator should fail CI for broken navigation/authority state instead of relying on a future chat to notice drift manually.

## 9. Answerability / routing regression suite

Create a machine-readable test set such as `RepositoryTools/answerability_cases.json`.

Each test case should contain a representative user question or aliases and the expected topic/canonical source(s). Examples:

- "Was ist der aktuelle akzeptierte Build?"
- "Was muss ich jetzt testen?"
- "Wo ist der Log-Uploader?"
- "Welche BCMER-Version ist erlaubt?"
- "Sind BCMER-Events gleich wahrscheinlich?"
- "Wie hoch ist das Thumper Bite Limit?"
- "Warum ist Shatteredrooms auf Experimentation/Embrion eingeschränkt?"
- "Was war das Black-Mesa/Pikmin-Problem?"
- "Wie werden Interior-Gewichte normalisiert?"
- "Woher kommt die Jetpack-Beschleunigung?"
- "Welche Fehler sind nur monitor-only?"
- "Wie importiere ich einen neuen Gale-Build?"

This suite validates repository routing, not natural-language quality. A future AI should be able to map the question to the expected source without reading the entire repository.

## 10. Provenance-first canonical claims

Wherever a current rule or value is important, the topic document should expose both the value and its provenance.

Examples:

- accepted value -> exact config path/key;
- runtime-confirmed behavior -> exact RuntimeEvidence/acceptance record;
- project-local code behavior -> exact patch source/project and DLL hash;
- package/version invariant -> exact export/snapshot evidence;
- historical reason -> exact diagnostic/rejection record.

This prevents the knowledge map from becoming an unsupported summary layer.

## 11. Atomic state-transition maintenance

Build acceptance/rejection should update navigation as one logical transition.

Where practical, automate generation/update of:

- accepted/current machine state;
- active candidate state;
- build lineage;
- knowledge-map current pointers;
- `RuntimeInbox/ACTIVE_BUILD.txt`;
- `BuildSpecs/current.json` guard state;
- exact next action;
- README/START_HERE compact pointer state.

Prefer generated references from one structured state source over manually copying the same facts into five files.

## 12. Repository search is fallback only

GitHub/code search remains useful for unknown historical details, code strings and unexpected error messages. It must not be required for ordinary canonical questions because:

- search indexing can be incomplete;
- terminology can differ from user wording;
- binary content is not semantically searchable;
- stale historical matches can outrank current truth.

The knowledge map + authority graph must provide deterministic routing first. Search is used after that when the question genuinely asks for deep history or an unclassified symbol/error.

## 13. Planned structure direction

Exact folder names may be refined during implementation, but the target separation should resemble:

- `Current/` — small current-state/controller-facing documents only;
- `Knowledge/` or equivalent — stable topic documents + human/machine knowledge map;
- `History/` or clearly classified existing numbered records — chronological handovers, experiments and superseded plans;
- `RuntimeEvidence/` — runtime provenance;
- `ProfileSources/` — readable profile snapshots;
- `BuildSpecs/` — build plans/control plane;
- `Patches/` — project-local source;
- `RepositoryTools/` — navigation validators, lineage generation and answerability tests.

Do not perform mass moves merely for aesthetics. Every move must preserve references/provenance and pass validation.

## 14. Overhaul acceptance criteria

The repository overhaul may be called complete only when:

- the human + JSON knowledge maps exist and cover all major topics;
- the build lineage exists and covers the meaningful build history;
- current/historical authority is explicit;
- README/START_HERE are compact routing documents rather than giant duplicated state dumps;
- current truth is no longer scattered across multiple mutually dependent `current` narratives;
- the roadmap is split into live roadmap and historical chronology where needed;
- all internal canonical links validate;
- all active/accepted binaries have readable snapshots;
- no canonical/current topic is orphaned;
- routing to any current major topic takes at most three hops from bootstrap;
- answerability regression cases pass;
- CI knowledge validation passes;
- a fresh-chat takeover can answer ordinary project questions by loading only the bootstrap plus the relevant topic/evidence files, not the entire repository.

## Current implementation timing

This plan is **binding but not an instruction to disturb the active S1.42AC runtime gate**.

S1.42AC remains the active gameplay candidate and S1.42AB remains accepted until AC runtime validation closes. The information-architecture overhaul should be executed as an explicit repository-maintenance stage when doing so will not blur attribution of gameplay/config changes.

Until the overhaul is executed, use the current authority rule: newest confirmed Current/candidate/acceptance records override older historical wording, and verify important facts against actual config/code/runtime evidence.

## Scope classification change

Where older current documents say only `cosmetic documentation cleanup`, interpret that deferred item from this point forward as:

**Repository information-architecture overhaul per `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, including cleanup of cosmetic drift as a subordinate task.**
