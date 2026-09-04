# Repository Overhaul — Post-Acceptance Audit Against Frozen Pre-Overhaul Contract

**Date:** 2026-09-04  
**Status:** REMEDIATION IMPLEMENTED / FINAL REVALIDATION PENDING  
**Scope:** repository information architecture only; no gameplay/config/mod/profile/project-local patch behavior change  
**Authority:** strict re-audit requested after the initial overhaul acceptance  
**Original contract source:** frozen standalone pre-overhaul repository at commit `5dbd0e637a480d8591773e422bbca4b0654cad20`

## Why this audit exists

After the repository overhaul had been marked complete, the user explicitly requested a second validation against the **actual instructions stored in the old pre-overhaul repository**, not merely against the validator that had just been created by the overhaul itself.

That distinction mattered. The first final CI gate was genuinely green, but the second pass found that the validator did not yet encode every obligation from the frozen contract.

## Frozen contract re-read

The audit re-read these files directly from the standalone backup at the frozen source commit:

- `OVERHAUL_START_HERE_ChatGPT.txt`
- `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`
- `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`
- `Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json`

The audit then compared those requirements against the current primary repository rather than assuming the prior acceptance was sufficient.

## Gaps found after the first acceptance

The post-acceptance audit found **information-architecture gaps, not gameplay defects**:

1. `Current/02_TECHNICAL_BASELINE.md` still contained obsolete historical `current` wording without the conspicuous top-of-file historical classification required by the original contract.
2. `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` still contained an obsolete `Current progress` checkpoint without a conspicuous historical banner.
3. `OVERHAUL_START_HERE_ChatGPT.txt` still looked like an active instruction to execute phases 0–11, even though the one-time overhaul was already complete.
4. `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md` still showed its preserved original `PLANNED / ... / NOT YET EXECUTED` status without an explicit completion banner above it.
5. `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md` had the same ambiguity.
6. The original `RepositoryTools/knowledge_architecture_validator.py` checked the live knowledge architecture correctly but did **not** independently enforce all one-time contract obligations such as visible stale-wording banners and backup-checkpoint-before-structural-migration ordering.

Therefore the earlier statement “everything is complete” was too strong until these points were remediated.

## Remediation completed

The current repository now adds conspicuous authority/completion banners to all five affected historical/execution-contract documents and registers them in `Current/DOCUMENT_AUTHORITY.json`.

`OVERHAUL_START_HERE_ChatGPT.txt` now explicitly says that the instructions below it are the preserved historical one-time execution contract and that ordinary takeover starts at `START_HERE_ChatGPT_Masterprompt.txt`.

A dedicated strict validator has been added:

`RepositoryTools/overhaul_contract_validator.py`

It validates obligations that are specifically derived from the frozen pre-overhaul contract, including:

- all machine-required artifacts exist;
- the independent backup manifest is PASS and points to the frozen source commit/tree;
- the frozen commit/tree are still present in Git history;
- the backup-gate commit is an ancestor of current HEAD;
- structural knowledge-architecture artifacts did **not** yet exist at the backup gate, proving the mandatory backup checkpoint preceded the structural migration;
- stale historical/current wording has a conspicuous visible classification;
- the authority registry classifies the stale documents;
- accepted/current build/controller state remains internally consistent;
- accepted `.r2z` state has readable `ProfileSources` and runtime evidence;
- all mandatory semantic topics from the old requirements exist and their registered paths resolve;
- ordinary topics remain reachable from the compact bootstrap through the knowledge map within the required hop budget;
- build-lineage paths resolve, including the corrected S1.42Z provenance;
- final execution/validation/migration records are present;
- canonical/current documents are checked for broken backtick path references.

The permanent `.github/workflows/knowledge-architecture.yml` now checks out full Git history and runs this strict contract validator in addition to the existing navigation check, knowledge validator, and answerability regression suite.

## Why `Plugin.cs` comments were not rewritten

The frozen requirements explicitly called out stale historical comments in `Patches/S139CompatibilityFixes/Plugin.cs` as a refactor target. The audit confirmed that `Current/DOCUMENT_AUTHORITY.json` already records this as `known_comment_drift` together with the current invariants:

- Crawler attack is allowed;
- Thumper uses Bite Limit 3 rather than complete isolation;
- Puffer protection remains;
- Baboon compatibility blocks only the proven Hawk-to-Pikmin entry points before mutation while preserving native cleanup lifecycle ownership.

The accepted S1.42AB profile/binary provenance must not be disturbed merely to modernize comments. Editing accepted patch source without rebuilding/reaccepting the artifact would create a source-versus-binary provenance mismatch. The correct repository-overhaul action is therefore explicit authority metadata, not a behavior-neutral source edit that would falsely imply the accepted binary was rebuilt from the edited file.

## Preservation / deletion result

The non-destructive migration decision remains valid. No historical evidence file has been deleted merely because it is redundant or stale. `Current/REPOSITORY_MIGRATION_MANIFEST.md/.json` remains the deletion/retention authority.

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

## Final revalidation gate

The audit is not closed merely because the remediation files exist. The final step is a green `Knowledge Architecture` run on the remediated repository with all four permanent checks:

1. generated current navigation;
2. knowledge/state/reference validator;
3. frozen original-overhaul-contract validator;
4. semantic answerability routing regression.

Once that run is green, `Current/OVERHAUL_VALIDATION_RESULTS.json` and this audit record are updated to `POST_ACCEPTANCE_REAUDIT_PASS` with the exact validation run/commit.
