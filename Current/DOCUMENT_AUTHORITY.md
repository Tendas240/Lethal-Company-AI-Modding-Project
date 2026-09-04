# Document Authority and Historical Classification

**Status:** CURRENT / CANONICAL AUTHORITY REGISTRY  
**Authority:** repository knowledge-source precedence  
**Canonical-For:** authority resolution, historical/current classification  
**Related:** `Current/DOCUMENT_AUTHORITY.json`, `Current/PROJECT_KNOWLEDGE_MAP.md`, `Current/CURRENT_STATE.json`  
**Last-Validated:** 2026-09-04

## Precedence

For a fresh session, resolve facts in this order:

1. `Current/CURRENT_STATE.json` and `Current/00_CURRENT_STATE.md` for global live state.
2. `Current/PROJECT_KNOWLEDGE_MAP.md/.json` for semantic routing.
3. The registered `Knowledge/*.md` canonical topic.
4. The exact controller/config/code/build/runtime evidence linked by that topic.
5. Historical handovers, candidate notes and chronology only for provenance.

A historical file never becomes current merely because it contains the word "current". Its authority is determined by this registry and the Knowledge Map.

## Global current authority

- `Current/CURRENT_STATE.json` — single machine-readable global state object.
- `Current/00_CURRENT_STATE.md` — single concise human global state declaration.
- `Current/01_HANDOVER_CORE.md` — fresh-session takeover router.
- `Current/PROJECT_KNOWLEDGE_MAP.md/.json` — topic router.
- `Current/BUILD_LINEAGE.md/.json` — build history / introduced-by / rejected-build reasoning.
- `BuildSpecs/current.json` — currently armed build controller only.
- `RuntimeInbox/ACTIVE_BUILD.txt` — runtime active-build controller only.
- `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` — project-local patch safety policy.

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

### S1.42AC rejection records

`Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` remains a truthful historical decision record. The original interpretation that equal EventType probability requires identical eight per-event log weights is superseded by `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`.

The historical rejection itself is not erased; S1.42AC remains formally rejected/not promoted until a later explicit decision changes that status.

## Historical families

Treat these as history/evidence unless the Knowledge Map explicitly promotes one as current policy:

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

In particular, do not infer an old complete two-way Pikmin/Thumper ban or a current Crawler Attack Blacklist from historical wording. Current invariant: the proven enemy -> Pikmin corrupting grab path is prevented narrowly; native Pikmin counterattack/lifecycle remains; Crawler is absent from the LethalMin Attack Blacklist.

## Supersession rule

A newer source may supersede an interpretation without deleting history. When that happens:

- preserve the old file;
- register its classification here or in the migration map;
- route current questions to the new source;
- keep the old source reachable for "why did we think that?" questions.


## Completed overhaul execution-contract snapshots

The following files are preserved as the original one-time overhaul contract, but their old `PLANNED` / `NOT YET EXECUTED` wording is **historical** and must not be interpreted as live state:

- `OVERHAUL_START_HERE_ChatGPT.txt`
- `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`
- `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`

Current completion authority is `Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md` with machine validation in `Current/OVERHAUL_VALIDATION_RESULTS.json`. Ordinary project takeover starts at `START_HERE_ChatGPT_Masterprompt.txt`.
