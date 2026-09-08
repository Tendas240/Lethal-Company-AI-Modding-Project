# Repository Overhaul Migration / Retention Manifest

**Status:** CURRENT / CANONICAL MIGRATION RECORD  
**Authority:** path migration, supersession, compaction and deletion rationale  
**Canonical-For:** moved/redirected/deleted-files rationale  
**Machine mirror:** `Current/REPOSITORY_MIGRATION_MANIFEST.json`  
**Cold-history mapping:** `Current/COLD_HISTORY_STORAGE.json`  
**Last-Validated:** 2026-09-08

## Migration model

The original overhaul intentionally used a **non-destructive semantic migration**. It created the Knowledge/topic authority layer, current-state machine authority, build lineage, document authority, artifact/evidence integrity and answerability validation without moving historical paths.

A later cleanup may be more selective only after passing the positive deletion gate below. On 2026-09-08 that gate was satisfied for exactly two frozen legacy payload roots: `Archive/` and `Logs/`.

## Moved files

None.

Stable numbered historical records remain at their original paths. Moving them would create reference churn without meaningful size reduction.

## Externalized / deleted cold payloads

The current primary-repository HEAD no longer carries the old payload contents below:

- `Archive/` except `Archive/README.md`;
- `Logs/` except `Logs/README.md`.

This was permitted because immediately before externalization the primary-repository subtrees were byte-identical by Git tree SHA to the verified frozen recovery repository:

- `Archive/` = `0dd155347e3174d5bdef7b27922ff738a9a11f35` in both repositories;
- `Logs/` = `9e67fc1a098b869dab9ba86063f5c2396d69c03f` in both repositories.

Recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`  
Frozen commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`

Every historical textual reference beginning with `Archive/` or `Logs/` is resolved by preserving the same relative path in that frozen recovery commit. The exact translation rule and registered reference inventory are machine-authoritative in `Current/COLD_HISTORY_STORAGE.json`.

No Git history rewrite was performed. The exact bytes remain reachable both through primary-repository Git history and the independently verified recovery repository.

## Compacted live files

`Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md` was intentionally compacted from a duplicate state/history document into a current work-queue router.

Before compaction:

- its full pre-overhaul content was already preserved in Git history and the verified standalone recovery repository;
- durable S1.42AB/S1.42AC facts were present in build/decision/runtime records;
- technical topic facts had been extracted into `Knowledge/`;
- controller truth remained in `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, and `RuntimeInbox/ACTIVE_BUILD.txt`.

Result: no unique fact was lost, while ordinary current-state navigation no longer requires reconciling another large duplicate declaration.

## Explicit supersession / recovery routes

- `Current/02_TECHNICAL_BASELINE.md` -> current questions route to `Current/00_CURRENT_STATE.md`, `Knowledge/ENEMY_SPAWN_BASELINE.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, and patch-safety policy.
- `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` -> current questions route to `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, and `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`.
- `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` -> historical rejection preserved; weight-model interpretation routes to `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md` and `Knowledge/BCMER.md`.
- old final handovers/audits -> chronology only; fresh takeover routes through `START_HERE_ChatGPT_Masterprompt.txt` and `Current/01_HANDOVER_CORE.md`.
- legacy `Archive/` and `Logs/` paths -> `Current/COLD_HISTORY_STORAGE.json` -> same relative path in the verified frozen recovery repository.

## Why most historical Markdown remains in place

Historical decision records contain failed attempts, user decisions, exact runtime observations and provenance that remain useful when a symptom returns. They are small compared with the frozen binary/log/document payloads, and stable path retention avoids needless link rewrites. `Current/DOCUMENT_AUTHORITY.md/.json` prevents stale historical wording from competing with live truth.

The cold payload roots were different: they had no post-freeze changes, were byte-identical to the verified recovery copy, and had deterministic recovery mapping. Keeping a second working-tree copy therefore added weight without adding unique evidence.

## Positive deletion gate

A legacy file or subtree may be removed from current HEAD only when all of these are proven:

1. no unique factual/evidentiary bytes remain only in the current working tree;
2. every inbound reference has a valid migrated or deterministic recovery target;
3. semantic topic/build-lineage replacements preserve information needed for normal project answers;
4. the knowledge validator passes;
5. answerability regression remains green;
6. the deletion/recovery rationale is recorded here and in machine-readable metadata;
7. provenance is preserved without an unplanned history rewrite.

`Archive/` and `Logs/` are the first and currently only broad historical payload roots to pass that gate.
