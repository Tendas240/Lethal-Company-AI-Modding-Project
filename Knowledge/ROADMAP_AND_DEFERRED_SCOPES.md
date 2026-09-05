# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `Current/122_S1.42AE_PROVIDER_CONTRACT_CORRECTION_ANALYSIS.md`, `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`, `BuildSpecs/S1.42AE_PLAN.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-05

## Current position

Accepted gameplay baseline: **S1.42AC — BCMER EventType Equal Distribution**.

Latest built artifact: **S1.42AE — Functional Microwave Provider Contract Correction — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**.

Active gameplay candidate: **S1.42AE**.

Runtime test outstanding: **yes**.

Successor armed: **no**.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AE` and `BuildSpecs/current.json` is disabled with S1.42AE as the guarded candidate artifact while runtime validation is open.

S1.42AD remains runtime-rejected historical evidence: its fail-closed provider contract expected zero Interior/tag curves, while direct runtime evidence exposed 18, so the `0.5` mutation did not apply.

The follow-up provider analysis is complete. Dusk 0.9.25 with `PrioritiseMoons=true` evaluates exact Moon -> exact Interior fallback -> matching Moon tags; Moon and Interior tables are not combined. The corrected shipped provider contract is exact 18 Moon/tag curves plus exact 18 Interior/tag curves. S1.42AE validates/logs both exact tables and scales only the 18 Moon/tag curves by `SpawnScale = 0.5`; Interior curves are validation-only.

## Exact next scope

The selected work is now the **S1.42AE runtime acceptance gate**. Do not build another successor before this evidence is evaluated.

Required next steps:

1. replace/import S1.42AE with the canonical repository Gale helper;
2. play one normal run far enough for ordinary moon/interior generation;
3. upload the complete fresh `LogOutput.log` with the exact S1.42AE uploader from `Current/123_S1.42AE_BUILD_CANDIDATE_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_CORRECTION.md`;
4. verify exact dependency versions, the armed lifecycle marker, `PrioritiseMoons=true, MoonCurves=18, InteriorCurves=18`, both logged keysets, and the final marker that 18 Moon/tag curves were scaled by `0.5` while 18 Interior curves were not mutated;
5. verify no S1.42AE contract-refusal/error marker and no new fatal/project-critical regression;
6. accept or reject S1.42AE from that evidence.

A single normal gameplay run is sufficient for the immediate technical gate. It is not expected to statistically demonstrate an exact 50% observed Microwave count; deterministic provider mutation is the primary rarity evidence.

## Remaining deferred independent gameplay/compatibility scopes

These remain separate unless the user explicitly selects or groups them:

- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown/despawn repair only with stronger evidence.

## BCMER scope boundary

S1.42AC is the accepted BCMER 1.71.0 **static EventType probability** implementation. Eight equal `12.5` scales intentionally produce unequal inverse-population per-event weights while preserving approximately equal aggregate EventType mass within integer truncation.

Exact long-run 12.5% **executed** EventType frequency after all runtime eligibility filters would be a materially broader algorithm-design project and is not the same scope. It is not currently armed.

## Interior scope boundary

The inherited S1.42AB implementation already solves equal effective rarity for all **LLL-viable** interiors by normalizing positive returned rarities to 100 after viability filtering. S1.42AC and S1.42AE do not modify that path.

Still separate:

- author/technical viability restrictions such as Shatteredrooms on Experimentation/Embrion;
- CullFactory compatibility;
- Mausoleum fog;
- route/NavMesh recovery.

Do not reopen the accepted interior-weight normalization just to solve one of those separate compatibility scopes.

## Repository-overhaul boundary

The overhaul is closed and validated. Current summary: `Knowledge/REPOSITORY_OVERHAUL.md`. Final acceptance/audit evidence remains in the registered overhaul authorities and `Current/OVERHAUL_VALIDATION_RESULTS.json`.

Future repository-architecture changes must remain separate from gameplay changes and continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves historical planning/package research only. This file plus `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md` are the live roadmap/lifecycle authorities.
