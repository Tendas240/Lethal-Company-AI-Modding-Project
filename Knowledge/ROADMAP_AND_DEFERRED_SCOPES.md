# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`, `BuildSpecs/S1.42AD_PLAN.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-05

## Current position

Accepted gameplay baseline: **S1.42AC — BCMER EventType Equal Distribution**.

Latest built artifact: **S1.42AD — Functional Microwave Spawn Rarity Reduction — RUNTIME REJECTED / NOT ACCEPTED**.

Active gameplay candidate: **none**.

Runtime test outstanding: **none**.

Successor armed: **no**.

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AC` and `BuildSpecs/current.json` is disabled against the accepted S1.42AC profile/SHA.

S1.42AD was built and runtime-tested. The user-authorized Functional Microwave target remains **half as often**, implemented conceptually as proportional `SpawnScale = 0.5`. The candidate was rejected because its fail-closed provider contract expected zero Interior/tag curves, while direct runtime evidence exposed **18 Interior/tag curves**, including `code_rebirth:functional_microwave_ultra_high`. The patch therefore correctly refused mutation and the `0.5` scale was not applied. Rejection authority: `Current/121_S1.42AD_RUNTIME_REJECTION_FUNCTIONAL_MICROWAVE_PROVIDER_CONTRACT_DRIFT.md`.

## Exact next scope

The selected work remains the **Functional Microwave provider-contract correction**, but no successor build ID is armed yet.

Before any corrected successor is built, independently resolve:

1. the actual runtime Moon-curve count and exact keys;
2. the actual runtime Interior-curve count and exact keys;
3. DawnLib/Dusk `MapObjectSpawnMechanics` selection/evaluation semantics when `PrioritiseMoons = true`;
4. which effective table or tables must be scaled to produce the user-authorized half-frequency target without collateral changes;
5. a revised fail-closed contract that verifies/logs both tables before mutation.

Do **not** simply delete the Interior-curve guard and do **not** blindly scale both dictionaries. S1.42AD is rejected and must not be used as a gameplay/build base.

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

The inherited S1.42AB implementation already solves equal effective rarity for all **LLL-viable** interiors by normalizing positive returned rarities to 100 after viability filtering. S1.42AC and rejected S1.42AD do not modify that path.

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