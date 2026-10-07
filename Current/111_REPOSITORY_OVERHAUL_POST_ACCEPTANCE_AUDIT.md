# Repository Overhaul — Post-Acceptance Audit Against Frozen Pre-Overhaul Contract

**Date:** 2026-09-04  
**Verdict:** POST_ACCEPTANCE_REAUDIT_PASS  
**Scope:** repository information architecture only; no gameplay/config/mod/profile/project-local patch behavior change  
**Authority:** strict re-audit requested after the initial overhaul acceptance  
**Original contract source:** frozen standalone pre-overhaul repository at commit `5dbd0e637a480d8591773e422bbca4b0654cad20`

## Why this audit exists

After the repository overhaul had been marked complete, the user explicitly requested a second validation against the **actual instructions stored in the old pre-overhaul repository**, not merely against the validator created during the overhaul.

That distinction mattered. The first final CI gate was genuinely green, but this second pass found that the validator did not yet encode every obligation from the frozen contract. The repository therefore was not treated as finally revalidated until those gaps were remediated and a stricter CI gate passed.

## Frozen contract re-read

The audit re-read these files directly from the standalone backup at the frozen source commit:

- `OVERHAUL_START_HERE_ChatGPT.txt`
- `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`
- `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`
- `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

The audit compared those frozen requirements against the current primary repository rather than assuming the prior acceptance was sufficient.

## Gaps found after the first acceptance

The post-acceptance audit found **information-architecture gaps, not gameplay defects**:

1. `Current/02_TECHNICAL_BASELINE.md` still contained obsolete historical `current` wording without the conspicuous top-of-file historical classification required by the original contract.
2. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` still contained an obsolete `Current progress` checkpoint without a conspicuous historical banner.
3. `OVERHAUL_START_HERE_ChatGPT.txt` still looked like an active instruction to execute phases 0–11, even though the one-time overhaul was already complete.
4. `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md` still showed its preserved original `PLANNED / ... / NOT YET EXECUTED` status without an explicit completion banner above it.
5. `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md` had the same ambiguity.
6. `Current/PROJECT_KNOWLEDGE_MAP.md` still had stale Phase-10 text pointing at the non-existent legacy machine-state name `PROJECT_STATE.json` instead of the completed `Current/CURRENT_STATE.json` architecture.
7. The original `RepositoryTools/knowledge_architecture_validator.py` checked live knowledge architecture correctly but did **not** independently enforce all one-time frozen-contract obligations such as visible stale-wording banners and backup-checkpoint-before-structural-migration ordering.

Therefore the earlier unqualified statement that every overhaul obligation had already been checked was too strong. These items are now corrected.

## Remediation completed

The current repository adds conspicuous authority/completion banners to all affected historical/execution-contract documents and registers them in `Current/DOCUMENT_AUTHORITY.json`.

`OVERHAUL_START_HERE_ChatGPT.txt` explicitly states that the instructions below it are the preserved historical one-time execution contract and that ordinary takeover starts at `START_HERE_ChatGPT_Masterprompt.txt`.

`Current/PROJECT_KNOWLEDGE_MAP.md` now identifies `Current/CURRENT_STATE.json` as machine lifecycle authority and no longer describes Phase 10 as pending.

A dedicated strict validator is now permanent:

`RepositoryTools/overhaul_contract_validator.py`

It validates obligations derived from the frozen pre-overhaul contract, including:

- all machine-required artifacts exist;
- the independent backup manifest is PASS and points to the exact frozen source commit/tree;
- the frozen commit/tree remain present in Git history;
- the backup-gate commit is an ancestor of current HEAD;
- structural knowledge-architecture artifacts did **not** yet exist at the backup gate, independently proving that the mandatory backup checkpoint preceded structural migration;
- stale historical/current wording has conspicuous visible classification;
- the authority registry classifies the stale documents;
- accepted/current build/controller state remains internally consistent;
- accepted `.r2z` state has readable `ProfileSources` and runtime evidence;
- all mandatory semantic topics from the old requirements exist and their concrete registered paths resolve;
- the compact bootstrap routes directly through the knowledge map within the required hop budget;
- build-lineage paths resolve, including corrected S1.42Z provenance;
- final execution/validation/migration records are present;
- canonical/current documents are checked for broken **concrete** path references while documented globs, placeholders, lifecycle destinations and JSON field selectors are treated as notation rather than files.

The permanent `.github/workflows/knowledge-architecture.yml` now checks out full Git history and runs this strict frozen-contract validator in addition to the existing navigation check, knowledge validator and answerability regression suite.

## Strict-validator calibration

The first strict-validator CI attempt, run `33919072718`, failed. That was useful rather than hidden: it exposed the genuine stale legacy machine-state name `PROJECT_STATE.json` in the knowledge map and also showed that an initial path checker was treating globs/placeholders such as `ProfileSources/<build>/` as if they were missing concrete files.

The genuine drift was corrected. The checker was then narrowed to distinguish concrete repository references from documented patterns without weakening checks on actual canonical targets.

During final documentation, three subsequent runs failed because the base validator still enumerated only the older completed status names and therefore rejected the new post-audit status string. That validator was changed to recognize completed/validated status semantically instead of by a brittle exact enumeration.

A further run then failed because the strict validator treated a historical sentence in this audit naming the removed legacy machine-state path as if it were a live concrete reference. The audit wording was corrected to preserve the historical fact without masquerading the obsolete name as a valid current path.

## Why `Plugin.cs` comments were not rewritten

The frozen requirements explicitly called out stale historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` as a refactor target. `Current/DOCUMENT_AUTHORITY.json` now records this explicitly as `code_comment_drift` with the current accepted invariants:

- Crawler attack/counterattack behavior is allowed and Crawler is absent from the LethalMin Attack Blacklist;
- Thumper uses Bite Limit 3 rather than complete two-way isolation;
- Puffer protection remains;
- Baboon compatibility blocks only the proven Hawk-to-Pikmin entry points before mutation while preserving native cleanup lifecycle ownership.

The accepted S1.42AB profile/binary provenance must not be disturbed merely to modernize comments. Editing accepted patch source without rebuilding/reaccepting the artifact would create source-versus-binary provenance drift. The correct repository-overhaul action is explicit authority metadata, not an after-the-fact source edit that would falsely imply the accepted binary was rebuilt from the edited file.

## Preservation / deletion result

The non-destructive migration decision remains valid. No historical evidence file was deleted merely because it is redundant or stale. `Current/REPOSITORY_MIGRATION_MANIFEST.md/.json` remains the deletion/retention authority.

## Gameplay state revalidated as unchanged

This audit/remediation does not alter gameplay state:

- accepted baseline: S1.42AB — Interior Weight Normalization;
- accepted SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`;
- S1.42AC remains formally rejected/not promoted;
- no active candidate;
- no runtime test outstanding;
- no successor armed;
- `BuildSpecs/current.json` remains disabled;
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`.

## Revalidation result — PASS

The first strict green `Knowledge Architecture` run was:

- run: `33919296323`
- head commit: `e3704877d309e40b092768430d0e81f7d86ed2e3`
- conclusion: **SUCCESS**

After the final post-audit status/schema and audit-wording cleanup, the confirmation run was:

- run: `33919943680`
- head commit: `18f5f24719a91986c954b0a59445db83d9571e77`
- conclusion: **SUCCESS**

That confirmation passed all four permanent gates:

1. generated current navigation — PASS;
2. knowledge/state/reference validator — PASS;
3. frozen original-overhaul-contract validator — PASS;
4. semantic answerability routing regression — PASS.

The machine record is `Current/OVERHAUL_VALIDATION_RESULTS.json`. The machine requirements are updated in `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json` so this stricter contract check remains part of future CI rather than being a one-time chat assertion.

## Final decision

**POST_ACCEPTANCE_REAUDIT_PASS.**

The repository overhaul is now accepted not only against the architecture produced by the new repository, but also against a direct re-read of the frozen old-repository instructions. The gaps found by that stricter comparison have been corrected without changing gameplay behavior.
