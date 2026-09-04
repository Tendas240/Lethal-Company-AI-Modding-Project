# Repository Knowledge Inventory — Pre-Migration Classification

**Status:** PHASE 2 COMPLETE / INPUT TO NAVIGATION MIGRATION  
**Authority:** repository-overhaul execution inventory  
**Canonical-For:** what knowledge exists, where authority currently lives, and which files are unsafe to move/delete before semantic extraction  
**Frozen pre-overhaul checkpoint:** `5dbd0e637a480d8591773e422bbca4b0654cad20`  
**Verified standalone recovery repository:** `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`  
**Related:** `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`, `Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md`, `Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md`  
**Last-Validated:** 2026-09-04

## Phase-2 conclusion

The repository contains enough current truth and provenance to build the new semantic navigation layer without deleting historical records. The principal information-architecture problem is not missing evidence; it is **authority mixing**: stable rules, temporary checkpoints, chronological handovers, machine state and runtime evidence are all present, but some older files still use `current` language.

No tracked project file is approved for deletion by this inventory. Phase 3 must create the new routing/knowledge layer first. Historical movement or deletion remains prohibited until references and unique facts are migrated and validated.

## Exact project state carried into the overhaul

- Accepted baseline: **S1.42AB — Interior Weight Normalization**.
- Accepted profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`.
- Accepted profile SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`.
- Latest built artifact: **S1.42AC — BCMER EventType Equal Distribution**, formally rejected/not promoted.
- S1.42AC source-path interpretation is corrected by `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`.
- Runtime test outstanding: **no**.
- Successor armed: **no**.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`.
- `BuildSpecs/current.json` is disabled and guarded by S1.42AB.

The overhaul must not change these gameplay/controller facts.

## Document and artifact families

| Family | Classification | Authority / unique role | Migration treatment |
|---|---|---|---|
| `README.md`, `START_HERE_ChatGPT_Masterprompt.txt`, `Current/00_CURRENT_STATE.md`, `Current/01_HANDOVER_CORE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md` | current/bootstrap but highly duplicated | current state, read-first routing, UX rules | replace duplicated prose with compact pointers only after Knowledge Map exists |
| `Current/Projektstatus_*.json`, `Current/AUTO_BUILD_RESULT.*`, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt` | machine/controller state | lifecycle/build/runtime truth | retain; define one explicit canonical lifecycle state and validate mirrors |
| numbered build candidate/acceptance/rejection/runtime-analysis/handover files | chronological evidence | build-specific provenance, exact runtime decisions, hashes, failure reasoning | preserve as history/evidence; do not require normal current questions to traverse them |
| `Current/03_PROJECT_CHRONOLOGY.md` | historical synthesis | compact reconstruction of S1.x evolution | retain as historical chronology; feed build lineage, not live state |
| `Current/05_FAILED_AND_OBSOLETE_APPROACHES.md` | stable anti-regression history/policy | failed approaches and reasons not to repeat them | retain; route through semantic failed-approaches/patch topics |
| `Current/09_REPOSITORY_FIRST_AUTOMATION.md` | stable infrastructure/UX policy | GitHub-first build, runtime uploader, binary accessibility | retain as evidence/policy; extract semantic build/runtime topic |
| `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` | permanent engineering policy | authoritative patch-safety contract | retain as canonical policy; expose from Knowledge Map directly or via semantic wrapper |
| `Current/74_LARGE_RUNTIME_LOG_PIPELINE_AND_RETENTION.md` | canonical infrastructure policy | large-log ingestion, query and retention | retain; expose through runtime evidence topic |
| `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md` | canonical user workflow | validated Gale replacement/import flow | retain; expose through Gale topic |
| `Current/02_TECHNICAL_BASELINE.md` | mixed stable facts + stale-current wording | many durable config values, power caps, ownership rules, but obsolete S1.41/S1.42S/T current claims | high-risk refactor target: extract durable facts into semantic topics; then classify file historical/not-current |
| `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` | mixed binding rules + stale checkpoint | equal-interior rule, CullFactory IDs, package notes, BCMER target, Mausoleum fog; also obsolete S1.42U/S1.42V current position | high-risk refactor target: split live roadmap/topic truth from chronology; preserve old path/provenance |
| `Current/61_LETHALMIN_1.1.108_ATTACK_TASK_DECOMPILE.txt` and similar decompile/diagnostic records | source evidence | exact upstream behavior/root-cause proof | retain as evidence; never make bootstrap read it by default |
| `Patches/**` | project-local source | executable compatibility behavior and comments | retain; documentation comments may be corrected only where stale, without changing behavior |
| `BuildSpecs/*_PLAN.md` | build plans/history | exact intended deltas and safety reviews | retain; current.json remains controller, historical plans route through lineage |
| `Profiles/*.r2z` | binary artifacts | exact build archives | retain; never rely on binary-only retrieval |
| `ProfileSources/<build>/` | readable profile evidence | configs/export/member hashes | retain; active/accepted builds require `FILE_INDEX.json` |
| `RuntimeEvidence/<build>/<timestamp>/` | runtime provenance | logs, hashes, generated analysis | retain according to runtime retention policy; map accepted/rejected records to evidence roots |
| `RuntimeInbox/**`, `RuntimeAnalysis/**`, `RuntimeTools/**` | runtime control/tooling | upload/active-build/query/Gale helper | retain; semantic runtime/Gale topics route here |
| `BuildSystem/**`, `.github/workflows/**` | automation implementation | build/index/ingest/self-test execution | retain; semantic pipeline topic routes here |
| `Archive/**`, `Logs/**`, `References/**` | historical/reference evidence | deep reconstruction fallback | retain unless later positive deletion audit proves no unique value |
| `Aktive_Modliste_*`, `DATEIINVENTAR_*`, `SHA256SUMS_*`, `VERIFIKATION_*`, old takeover prompts | historical artifact manifests | exact point-in-time inventory/handoff evidence | preserve/classify; not current navigation |

## Known authority-drift findings

### `Current/02_TECHNICAL_BASELINE.md`

Durable facts coexist with obsolete claims such as S1.41 being the accepted gameplay baseline, S1.42S being the current technical descendant and S1.42T being next. Those statements are historical and must not remain eligible to answer a current-state question.

Unique/durable content to extract before classification includes:

- exact Compatibility Fixes v1.3.14 provenance and responsibilities;
- CodeRebirth/DawnLib natural-spawn ownership/config rule;
- exact BCMER 1.71.0 and rain/ownership guards;
- LethalMin compatibility decisions;
- indoor power-cap table;
- equal-interior architecture and Black Mesa ownership rule;
- enemy spawn-owner rules and unknown power-level list;
- monitor-only warning classes;
- repository-first build architecture.

### `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`

Durable/binding rules coexist with a historical S1.42U/S1.42V current checkpoint. Extract and preserve:

- all installed/future interiors use equal effective probability after owner viability filtering;
- explicit technical hard blocks remain protected until compatibility evidence supports removal;
- Shatteredrooms Experimentation/Embrion exclusion is a technical compatibility restriction, not a desired rarity exception;
- exact CullFactory IDs `junkrooms` and `shatteredrooms`;
- Mausoleum fog reduction is interior-specific;
- duplicate-registration rules, especially Black Mesa ownership;
- the intended BCMER eight-way equal static EventType target, interpreted through the newer exact 1.71.0 source analysis;
- package-specific interior/dependency evidence that remains useful for later compatibility work.

The obsolete S1.42U/S1.42V current-position block belongs to chronology, not live roadmap authority.

### `Patches/S139CompatibilityFixes/Plugin.cs`

Current executable code already reflects the later narrow-ownership architecture: `BaboonBirdPikminEnemy` remains enabled, Hawk -> Pikmin entry points are blocked narrowly, the common `GrabPikmin` guard is prevention-only, and EnemyIsolation defaults off. Code comments must be treated as implementation documentation and audited during Phase 5 for any remaining historical wording; no behavioral code change is authorized by the repository overhaul.

## Mandatory topic extraction matrix

| Topic ID | Primary current evidence to route/extract from | Stable fact / purpose |
|---|---|---|
| `accepted_baseline` | `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`, S1.42AB project status, profile/evidence | one authoritative accepted baseline + exact profile/SHA/evidence |
| `active_candidate_and_next_test` | current project status, `BuildSpecs/current.json`, `RuntimeInbox/ACTIVE_BUILD.txt` | explicit NONE candidate/test now; deterministic next action |
| `build_pipeline` | `Current/09_REPOSITORY_FIRST_AUTOMATION.md`, `BuildSystem/`, profile-build workflow | repository-first build contract |
| `gale_import` | `Current/93_GALE_ACTIVE_PROFILE_REPLACEMENT_WORKFLOW.md`, `RuntimeTools/ReplaceActiveGaleProfile.ps1` | validated import/replacement UX |
| `runtime_upload_and_ingest` | `Current/09...`, `Current/74...`, runtime workflows/tools | normal and very-large log paths, retention/query |
| `bcmer` | `Current/109...`, exact ProfileSources configs, historical S1.41/AC records | exact 1.71.0 ownership, rain guards, corrected EventType semantics |
| `interiors_and_lll` | S1.42AB acceptance, `Current/07...`, ProfileSources | post-viability Weight 100 normalization, restrictions, CullFactory/Black Mesa |
| `enemy_spawn_baseline` | `Current/ENEMY_SPAWN_BASELINE_S1.42C.json`, technical baseline/history | moon power/spawn ownership and anti-guess rules |
| `pikmin_enemy_compatibility` | patch safety policy, S1.42S acceptance/root-cause records, plugin source | Thumper/Puffer/Baboon Hawk asymmetric protections and lifecycle ownership |
| `jetpack` | `Current/90_S1.42Z_RUNTIME_ACCEPTANCE_JETPACK_PIKMIN_RETUNE.md`, profile/source | acceleration 18 and accepted Jet Fuel/Thruster values/provenance |
| `coderebirth` | S1.40B chronology/evidence, S1.42Z acceptance, profile configs/source | natural Currency/Flash-Turret control and ACU/G.R.E.G. tuning |
| `functional_microwave` | S1.42Z acceptance + profile config | volume 0.15 accepted; spawn-rarity reduction deferred |
| `immortal_snail` | S1.42Z acceptance + profile config | rarity 40 / max 2 |
| `monitor_only_errors` | S1.42AB/S1.42Z acceptance + failed-approaches/technical records | known warning/error classes not to patch without stronger evidence |
| `black_mesa_pikmin_routing` | S1.42AA/AB runtime evidence and routing diagnostics | separate unresolved routing evidence; not caused by AC config-only delta |
| `roadmap_and_deferred_scopes` | current state/open issues + durable rules from `Current/07...` | explicit deferred scopes without stale build nomination |
| `patch_safety_policy` | `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` | permanent narrow-patch safety gate |
| `repository_overhaul` | overhaul start/plan/playbook/requirements/execution state | current migration phase and acceptance contract |
| `pre_overhaul_backup_and_recovery` | `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json` + backup reciprocal manifest | exact recovery checkpoint and standalone backup |

## Build-lineage extraction source priority

1. build-specific project-status JSON and candidate/acceptance/rejection records;
2. `Current/03_PROJECT_CHRONOLOGY.md` for early/aggregate S1.x history;
3. `Current/06_RECENT_WORK_*` family for transition detail;
4. `BuildSpecs/*_PLAN.md` for planned intent;
5. profile/member SHA manifests and RuntimeEvidence for exact provenance.

Later accepted/rejected records override the status interpretation of an earlier plan. Historical files are not rewritten to pretend later knowledge existed at the time.

## Reference and deletion risk rules from the inventory

- No mass move is approved in Phase 2.
- No deletion is approved in Phase 2.
- Existing numbered historical paths should remain valid during navigation migration.
- When a semantic topic supersedes mixed current/history wording, retain the original as history/evidence and add explicit authority classification rather than erasing its contents.
- Redirect stubs are required only if a path is actually moved; retaining historical files in place is preferred when it lowers reference risk.
- `Current/02...` and `Current/07...` must not be used as unqualified current authority after Phase 5.
- Project-local source comments may be corrected for accuracy, but behavioral code and compiled profile state must remain unchanged.

## Phase-3 entry condition

Satisfied. The repository now has:

- exact frozen pre-overhaul checkpoint;
- verified standalone recovery repository;
- classified knowledge/document families;
- identified stale-current risk surfaces;
- mandatory topic extraction matrix;
- no premature move/delete.

Phase 3 must now create `Current/PROJECT_KNOWLEDGE_MAP.md`, `Current/PROJECT_KNOWLEDGE_MAP.json`, stable semantic topic documents, and initial human/machine build-lineage artifacts **before** old bootstrap/navigation is reduced.
