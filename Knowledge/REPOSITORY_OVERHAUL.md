# Repository Information-Architecture Overhaul

**Status:** CURRENT / EXECUTION IN PROGRESS  
**Authority:** semantic router to the binding overhaul contract and execution state  
**Canonical-For:** `repository_overhaul`  
**Evidence:** `OVERHAUL_START_HERE_ChatGPT.txt`, `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`, `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`  
**Machine State:** `Current/OVERHAUL_EXECUTION_STATE.json`  
**Related:** `Knowledge/PRE_OVERHAUL_BACKUP_AND_RECOVERY.md`, `Current/REPOSITORY_KNOWLEDGE_INVENTORY.md`  
**Last-Validated:** 2026-09-04

## Goal

Convert the chronology-heavy repository into deterministic retrieval architecture for fresh ChatGPT sessions while preserving all gameplay evidence, historical reasoning and recovery provenance.

Target retrieval path:

`README / START_HERE -> Current State + Knowledge Map -> Topic Canonical Source -> Evidence / Config / Code / History`

Repository search becomes fallback rather than the primary way to answer ordinary project questions.

## Binding execution order

0. establish exact pre-overhaul state;
1. create and verify standalone backup;
2. inventory and extract knowledge before moves;
3. create new navigation/knowledge map before removing old navigation;
4. create build lineage and authority graph;
5. separate live truth from chronology;
6. harden binary/large-evidence retrieval;
7. migrate references/redirects with conservative deletion discipline;
8. implement repository knowledge validator + CI;
9. implement answerability/routing regression suite;
10. harden atomic current-state transitions;
11. final validation against requirements and backup.

## Completed gates

- Phase 0: exact source state frozen at commit `5dbd0e637a480d8591773e422bbca4b0654cad20`, tree `0e17aac410cf600a164396b5586b5b50f084df22`.
- Phase 1: verified standalone backup repository established; machine manifest at `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`.
- Phase 2: repository knowledge inventory/classification recorded in `Current/REPOSITORY_KNOWLEDGE_INVENTORY.md` + `.json`.

For the exact active phase, always read `Current/OVERHAUL_EXECUTION_STATE.json`; do not infer progress from this prose if the execution state is newer.

## Non-negotiable migration rules

- preserve information/provenance before reducing duplication;
- do not alter gameplay configs, mod versions, profile behavior or project-local runtime behavior as part of the overhaul;
- do not delete merely because something looks old;
- create navigation before removing old navigation;
- classify historical stale-current wording explicitly;
- active/accepted binary profiles require readable ProfileSources + FILE_INDEX;
- validator and answerability suite must pass before completion;
- rollback to/compare with the verified standalone backup if discoverability or authority gets worse.

## Completion contract

The overhaul is complete only when the plan, playbook and machine requirements all pass, including zero broken canonical references, zero orphan canonical/current documents, one authoritative accepted baseline/current-candidate state, all major topics indexed within at most three hops, complete useful build lineage, readable active/accepted profile evidence, CI validation PASS and answerability routing PASS.
