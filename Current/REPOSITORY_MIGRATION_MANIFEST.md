# Repository Overhaul Migration / Retention Manifest

**Status:** CURRENT / CANONICAL MIGRATION RECORD  
**Authority:** path migration, supersession, compaction and deletion rationale  
**Canonical-For:** moved/redirected/deleted-files rationale  
**Machine mirror:** `Current/REPOSITORY_MIGRATION_MANIFEST.json`  
**Last-Validated:** 2026-09-04

## Migration model

The overhaul intentionally used a **non-destructive semantic migration**.

Instead of moving hundreds of historical files and breaking old links, the repository gained:

- `Knowledge/` topic authority;
- `Current/PROJECT_KNOWLEDGE_MAP.md/.json`;
- `Current/BUILD_LINEAGE.md/.json`;
- `Current/DOCUMENT_AUTHORITY.md/.json`;
- `Current/CURRENT_STATE.json`;
- `Current/ARTIFACT_EVIDENCE_INTEGRITY.md/.json`;
- `Current/CURRENT_STATE_TRANSITION_POLICY.md`;
- automated knowledge/answerability validation.

Historical paths remain reachable for provenance.

## Moved files

None.

No canonical evidence was physically moved because stable historical paths already have many references and moving them would add redirect maintenance without improving ordinary retrieval once the semantic router exists.

## Deleted files

None.

The standalone pre-overhaul recovery repository means rollback is possible, but that is **not** a reason to delete useful primary-repository history. No file passed the stricter unique-fact + inbound-reference + replacement-validation gate required for deletion.

## Compacted live files

`Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md` was intentionally compacted from a duplicate state/history document into a current work-queue router.

Before compaction:

- its full pre-overhaul content was already preserved in Git history and the verified standalone recovery repository;
- durable S1.42AB/S1.42AC facts were present in build/decision/runtime records;
- technical topic facts had been extracted into `Knowledge/`;
- controller truth remained in `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, and `RuntimeInbox/ACTIVE_BUILD.txt`.

Result: no unique fact was lost, while ordinary current-state navigation no longer requires reconciling another large duplicate declaration.

## Explicit supersession routes

- `Current/02_TECHNICAL_BASELINE.md` -> current questions route to `Current/00_CURRENT_STATE.md`, `Knowledge/ENEMY_SPAWN_BASELINE.md`, `Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md`, and patch-safety policy.
- `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` -> current questions route to `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, and `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`.
- `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md` -> historical rejection preserved; weight-model interpretation routes to `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md` and `Knowledge/BCMER.md`.
- old final handovers/audits -> chronology only; fresh takeover routes through `START_HERE_ChatGPT_Masterprompt.txt` and `Current/01_HANDOVER_CORE.md`.

## Why retention is safer

Historical files contain failed attempts, user decisions, exact runtime observations and provenance that are useful when a later symptom looks similar. The new authority registry prevents their stale "current" wording from competing with live truth, so retaining them is now low-risk and high-value.

## Future deletion gate

A later cleanup may delete a legacy file only when all of these are proven:

1. no unique factual/evidentiary content remains;
2. every inbound reference has a valid current target;
3. semantic topic/build-lineage replacements preserve the needed information;
4. the knowledge validator passes;
5. answerability regression remains green;
6. the deletion and rationale are added to this manifest.
