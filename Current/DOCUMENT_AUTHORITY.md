# Document Authority and Historical Classification

**Status:** CURRENT / CANONICAL AUTHORITY REGISTRY  
**Authority:** repository knowledge-source precedence  
**Canonical-For:** authority resolution, historical/current classification  
**Related:** `Current/DOCUMENT_AUTHORITY.json`, `Current/PROJECT_KNOWLEDGE_MAP.md`, `Current/CURRENT_STATE.json`, `Current/INTEGRITY_ERRATA_REGISTRY.json`, `Current/HANDOVER_PREPARATION_PROMPT.md`  
**Last-Validated:** 2026-09-05

## Precedence

For a fresh session, resolve facts in this order:

1. `Current/CURRENT_STATE.json` and `Current/00_CURRENT_STATE.md` for global live state.
2. `Current/PROJECT_KNOWLEDGE_MAP.md/.json` for semantic routing.
3. The registered canonical topic/workflow source selected by that map.
4. `Current/INTEGRITY_ERRATA_REGISTRY.json` when a concrete value/status/provenance claim is known to have been corrected or superseded.
5. The exact controller/config/code/build/runtime evidence linked by that topic.
6. Historical handovers, candidate notes and chronology only for provenance.

A historical file never becomes current merely because it contains the word "current". Its authority is determined by this registry, the Knowledge Map and explicit integrity errata.

A later explicit acceptance or rejection may supersede an older lifecycle verdict while preserving the older record as historical evidence.

## Global current authority

- `Current/CURRENT_STATE.json` — single machine-readable global state object.
- `Current/00_CURRENT_STATE.md` — single concise human global state declaration.
- `Current/01_HANDOVER_CORE.md` — fresh-session takeover router.
- `Current/HANDOVER_PREPARATION_PROMPT.md` — current workflow executed by the active ChatGPT chat when the user requests transfer to a new ChatGPT chat; it verifies live repository/CI/controller state and generates the new chat's fresh start prompt.
- `Current/PROJECT_KNOWLEDGE_MAP.md/.json` — topic router.
- `Current/BUILD_LINEAGE.md/.json` — build history / introduced-by / rejected-build reasoning.
- `Current/INTEGRITY_ERRATA_REGISTRY.json` — known-bad values and supersession/provenance qualifications.
- `Current/VALIDATOR_COVERAGE.json` — explicit validator scope and blindspots.
- `Current/MULTIPHASE_CHECKPOINT_POLICY.json` — future ordered-workflow checkpoint policy.
- `BuildSpecs/current.json` — currently armed build controller only.
- `RuntimeInbox/ACTIVE_BUILD.txt` — runtime active-build controller only.
- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` — project-local patch safety policy.

## Current-chat handover workflow

When the user explicitly requests a transfer to a new ChatGPT chat, `Current/HANDOVER_PREPARATION_PROMPT.md` is the workflow authority. It is intentionally state-neutral: accepted build, latest artifact, hashes, CI run, runtime gate and next action must be resolved from the then-current repository instead of being duplicated as a static prompt snapshot.

The prompt should be updated when handover mechanics/authority/validation policy changes, not merely because normal build/runtime state advances. Its discoverability from generated bootstrap files, the Knowledge Map and this registry is part of the repository knowledge-architecture contract.

## Generated current navigation

`README.md`, `START_HERE_ChatGPT_Masterprompt.txt`, `Current/00_CURRENT_STATE.md` and `Current/01_HANDOVER_CORE.md` are generated from `Current/CURRENT_STATE.json` by `RepositoryTools/render_current_navigation.py`.

They carry an explicit `GENERATED — DO NOT MANUALLY EDIT` marker. Update the canonical machine state first, render the derived navigation, and commit the logical transition together. CI checks byte-for-byte renderer equality.

## Explicitly classified stale-current sources

### `Current/02_TECHNICAL_BASELINE.md`

**HISTORICAL MIXED SNAPSHOT — NOT GLOBAL CURRENT AUTHORITY.**

It preserves useful technical detail but mixes that detail with old S1.41/S1.42S "current" wording. Route present-day questions to:

- `Current/00_CURRENT_STATE.md`
- `Knowledge/ENEMY_SPAWN_BASELINE.md`
- `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`
- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Do not rewrite the historical body to pretend it was written at the current project state.

### `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`

**HISTORICAL ROADMAP SNAPSHOT — BINDING RULES EXTRACTED, OLD PROGRESS WORDING NOT CURRENT.**

The old S1.42U/S1.42V progress block is preserved as chronology. Current policy/roadmap authority is:

- `Knowledge/BCMER.md`
- `Knowledge/INTERIORS_AND_LLL.md`
- `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`

### S1.42AC rejection and later acceptance

`Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` remains a truthful historical decision record. The original interpretation that equal EventType probability requires identical eight per-event log weights is superseded by `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`.

That source-level analysis did not itself promote the artifact. After a fresh S1.42AC confirmation run under the corrected model, `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` explicitly accepted S1.42AC. Current live status is therefore accepted, while `Current/106...` remains reachable as historical rejection evidence. Machine acceptance detail is `Current/Projektstatus_S1.42AC_ACCEPTED.json`.

The old incorrect raw-runtime-log SHA is likewise retained only as qualified historical metadata. Byte authority for the original rejection-era run is `RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json`; detailed correction is `Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json`; repository-wide known-bad classification is `Current/INTEGRITY_ERRATA_REGISTRY.json`. The fresh acceptance run is `RuntimeEvidence/S1.42AC/20260904T235720Z/` with its own `INDEX.json`.

## Historical families

Treat these as history/evidence unless the Knowledge Map explicitly promotes one as current policy or `Current/CURRENT_STATE.json` explicitly references one as the current build decision/status source:

- `Current/*FINAL_HANDOVER*.md`
- `Current/*REPOSITORY_HANDOVER_AUDIT*.md`
- `Current/*BUILD_CANDIDATE*.md`
- `Current/*RUNTIME_ACCEPTANCE*.md`
- `Current/*RUNTIME_REJECTION*.md`
- old `Current/Projektstatus_*.json`
- old `BuildSpecs/S*` plans
- `RuntimeEvidence/**`
- `Archive/**`

These files are intentionally retained because they contain provenance, failed approaches and runtime evidence.

## Code-comment drift rule

`Patches/S139CompatibilityFixes/Plugin.cs` is executable current code, but comments are not an independent policy source. Use executable behavior, accepted runtime evidence and `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md` for current semantics.

Current accepted invariants are:

- Crawler attack/counterattack behavior is allowed; Crawler is absent from the LethalMin Attack Blacklist.
- Thumper is governed by Bite Limit 3 rather than complete two-way isolation.
- Puffer protection for Pikmin remains part of accepted compatibility behavior.
- Baboon Hawk compatibility blocks only the proven Hawk-to-Pikmin entry points before mutation while native cleanup lifecycle ownership remains enabled.

Therefore old S1.42J-era wording about complete two-way isolation or a Crawler blacklist is non-normative.

Do **not** edit accepted patch source solely to modernize comments unless the accepted binary/profile provenance is rebuilt and revalidated. A comment-only source edit after acceptance would make the tracked source no longer exactly represent the accepted binary build. Authority metadata is the safe repository-overhaul mechanism for this historical comment drift.

## Supersession rule

A newer source may supersede an interpretation or lifecycle verdict without deleting history. When that happens:

- preserve the old file;
- register its classification here, in the migration map, or in `Current/INTEGRITY_ERRATA_REGISTRY.json`;
- route current questions to the new source;
- keep the old source reachable for "why did we think that?" questions.

Known concrete bad values must be locally qualified or explicitly registered; an unqualified occurrence is a CI failure.

## Future multi-phase execution rule

New multi-phase migrations/maintenance workflows use immutable per-phase records under `ExecutionCheckpoints/<process>/phase_<NN>.json` according to `Current/MULTIPHASE_CHECKPOINT_POLICY.json`.

The validator requires monotonic predecessor PASS checkpoints and checks commit existence/artifact provenance. This policy is prospective; it does not retroactively manufacture missing phase 3-10 checkpoints for the 2026 overhaul. That historical limitation remains explicitly qualified by `Current/116_INDEPENDENT_PREOVERHAUL_CONTRACT_AUDIT_20260905.md`.

## Completed overhaul execution-contract snapshots

The following files are preserved as the original one-time overhaul contract, but their old `PLANNED` / `NOT YET EXECUTED` wording is **historical** and must not be interpreted as live state:

- `OVERHAUL_START_HERE_ChatGPT.txt`
- `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`
- `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`

Current completion authority is `Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md` with machine validation in `Current/OVERHAUL_VALIDATION_RESULTS.json`. The stricter frozen-contract re-audit is recorded in `Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md`; the independent frozen-state audit and phase-order qualification are recorded in `Current/116_INDEPENDENT_PREOVERHAUL_CONTRACT_AUDIT_20260905.md`. Ordinary project takeover starts at `START_HERE_ChatGPT_Masterprompt.txt`.
