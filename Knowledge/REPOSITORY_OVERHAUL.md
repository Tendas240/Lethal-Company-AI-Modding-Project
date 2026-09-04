# Repository Information-Architecture Overhaul

**Status:** COMPLETE / INDEPENDENT REAUDIT PASS WITH PHASE-ORDER PROVENANCE QUALIFICATION / INTEGRITY HARDENING ADDED  
**Authority:** canonical semantic summary of the completed overhaul and its validation  
**Canonical-For:** `repository_overhaul`  
**Evidence:** `Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md`, `Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md`, `Current/116_INDEPENDENT_PREOVERHAUL_CONTRACT_AUDIT_20260905.md`, `Current/117_REPOSITORY_INTEGRITY_HARDENING_20260905.md`, `Current/OVERHAUL_VALIDATION_RESULTS.json`, `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`, `Current/INTEGRITY_ERRATA_REGISTRY.json`  
**Machine State:** `Current/OVERHAUL_EXECUTION_STATE.json`  
**Related:** `Knowledge/PRE_OVERHAUL_BACKUP_AND_RECOVERY.md`, `Current/REPOSITORY_MIGRATION_MANIFEST.md`, `Current/DOCUMENT_AUTHORITY.md`, `Current/VALIDATOR_COVERAGE.json`, `Current/HANDOVER_PREPARATION_PROMPT.md`  
**Last-Validated:** 2026-09-05

## Result

The one-time repository information-architecture overhaul is functionally complete. The repository now uses deterministic semantic routing for fresh ChatGPT sessions while preserving gameplay evidence, historical reasoning and recovery provenance.

Current retrieval path:

`README / START_HERE -> Current State + Knowledge Map -> Topic Canonical Source -> Evidence / Config / Code / History`

Repository search is a fallback rather than the primary way to answer ordinary project questions.

## Completed deliverables and phase-order provenance

All binding phase deliverables 0 through 11 are present and independently inspectable:

0. exact pre-overhaul state established;
1. standalone backup created and verified;
2. knowledge inventoried/extracted before moves;
3. new navigation/knowledge map created before old navigation was reduced;
4. build lineage and authority graph created;
5. live truth separated from chronology;
6. binary/large-evidence retrieval hardened;
7. references/redirects migrated with conservative deletion discipline;
8. repository validator + CI implemented;
9. answerability/routing regression suite implemented;
10. atomic current-state transitions hardened;
11. final validation performed against requirements and backup.

The independent 2026-09-05 re-audit distinguishes deliverable completion from historical checkpoint provenance. Git history directly proves Phase 0, the Phase-1 standalone-backup gate, Phase 2, and the transition into Phase 3 in the required order. `Current/OVERHAUL_EXECUTION_STATE.json` then remained at "Phase 2 complete / Phase 3 active" while the Phase 3–10 implementation artifacts were created and was later advanced to final validation/Phase 11 in one state update. Therefore the exact individual **phase-completion checkpoint order for Phases 3–10 is not independently reconstructible from execution-state checkpoints**. This is a non-blocking provenance limitation, not evidence of an out-of-order destructive migration: the implementation was non-destructive, old navigation/evidence was retained, and the final dependency graph satisfies all phase deliverables.

Do not restate "all phases completed in order" as an independently proven historical fact without this qualification.

The implementation remained non-destructive: no legacy evidence files were mass-moved or deleted, and gameplay/config/mod/profile/project-local patch behavior was not changed.

## Recovery gate

- Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`
- Frozen source tree: `0e17aac410cf600a164396b5586b5b50f084df22`
- Standalone recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`
- Primary backup manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`
- Verification: **PASS**

The same-repository freeze branch is supplemental only; the standalone repository is the independent recovery point.

## Post-acceptance re-audits

After initial acceptance, the overhaul was rechecked directly against the frozen original pre-overhaul instructions. That stricter audit found several information-architecture gaps and validator-calibration issues, including stale historical/current wording, an obsolete machine-state name in the human Knowledge Map and incomplete enforcement of one-time backup-ordering requirements.

The independent 2026-09-05 audit additionally found stale S1.42AC raw-log SHA metadata in retained historical records. The authoritative raw-log SHA-256 is `fe4b4a20996d0b76d9f1bdd8551a233138a032c1321c417a56e1ac3948ae8067`; the old `8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0` value is superseded historical metadata only. `Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json` explicitly classifies retained historical occurrences. `Current/INTEGRITY_ERRATA_REGISTRY.json` is now the central known-bad/supersession registry.

Those gaps were corrected without changing gameplay behavior.

## 2026-09-05 integrity hardening

The post-audit hardening adds defense-in-depth rather than new gameplay state:

- direct SHA-256 recomputation from the actual S1.42AB/S1.42AC profile bytes and linked raw runtime logs;
- repository-wide central known-bad/supersession registry and linter;
- explicit generated-file protection markers plus byte-exact renderer validation;
- machine-readable validator coverage/blindspot documentation;
- negative validator fixtures proving representative invalid states fail closed;
- prospective immutable per-phase checkpoint policy with Git commit/artifact verification;
- broader CI triggers covering profile, runtime-evidence, patch, build-system and runtime-tool changes relevant to repository authority.

This does **not** retroactively repair the missing Phase 3–10 historical checkpoints. Instead it prevents the same auditability class from recurring in future multi-phase work.

## Persistent current-chat handover workflow

`Current/HANDOVER_PREPARATION_PROMPT.md` is the canonical workflow executed by the active ChatGPT chat whenever the user requests transfer to a new ChatGPT chat.

It intentionally does not embed the current accepted build, latest artifact, hashes, active candidate, runtime gate, CI run or exact next action. At handover time the active chat resolves those facts from `Current/CURRENT_STATE.json`, controllers, the Knowledge Map, Document Authority, integrity errata and the actual current `main`/CI state, then produces a fresh new-chat start prompt.

The workflow is discoverable from generated `README.md`, `START_HERE_ChatGPT_Masterprompt.txt` and `Current/01_HANDOVER_CORE.md`, and is registered in both the Knowledge Map and Document Authority registry. `RepositoryTools/handover_workflow_validator.py` fails CI if that cross-link contract drifts. The answerability suite also contains an explicit natural-language handover trigger case.

This avoids maintaining a second stale build-specific handover truth while still allowing the handover procedure itself to evolve when repository workflow or authority policy changes.

The permanent CI now runs:

1. generated current-navigation validation;
2. repository knowledge/state/reference validation;
3. persistent ChatGPT handover-workflow validation;
4. actual artifact/runtime byte integrity validation;
5. repository-wide integrity/authority/known-bad-value validation;
6. S1.42AC runtime-SHA provenance validation;
7. future multi-phase checkpoint validation;
8. strict frozen original-overhaul-contract validation;
9. semantic answerability routing regression;
10. negative validator self-tests.

Coverage and explicit blindspots are documented in `Current/VALIDATOR_COVERAGE.json` so a green run is not interpreted as proof of obligations a validator does not test.

## Historical execution-contract rule

`OVERHAUL_START_HERE_ChatGPT.txt`, `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md` and `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md` are retained as historical one-time execution contracts. Their preserved planned/pending wording must not be interpreted as current project state.

Ordinary takeover now starts at `START_HERE_ChatGPT_Masterprompt.txt`, then `Current/00_CURRENT_STATE.md` and `Current/PROJECT_KNOWLEDGE_MAP.md`.

When the user later requests transfer again, the active chat must execute `Current/HANDOVER_PREPARATION_PROMPT.md` rather than manually reconstructing a handover from memory.

## Continuing safeguards

- preserve information/provenance before reducing duplication;
- do not delete historical evidence merely because it looks redundant;
- use `Current/DOCUMENT_AUTHORITY.md` when older documents contain stale `current` wording;
- qualify corrected concrete values through `Current/INTEGRITY_ERRATA_REGISTRY.json`;
- create immutable per-phase checkpoints for future ordered multi-phase work;
- use `Current/HANDOVER_PREPARATION_PROMPT.md` for future chat transfers;
- every future architecture change remains subject to `.github/workflows/knowledge-architecture.yml`;
- rollback/compare against the verified standalone backup if routing, authority or discoverability regresses.

## Current gameplay handoff

The overhaul itself is closed. Accepted gameplay baseline remains **S1.42AB**. S1.42AC remains formally rejected/not promoted, with its old BCMER weight interpretation superseded by `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`.

No runtime test is outstanding and no successor is armed. Resume normal project work from `Current/CURRENT_STATE.json` and `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`.
