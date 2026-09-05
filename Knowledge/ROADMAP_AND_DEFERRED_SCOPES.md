# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`, `BuildSpecs/S1.42AD_PLAN.md`, durable rules extracted from `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-05

## Current position

Accepted gameplay baseline: **S1.42AC — BCMER EventType Equal Distribution**.

Selected next scope: **S1.42AD — Functional Microwave Spawn Rarity Reduction**.

Active gameplay candidate: **none**.

Runtime test outstanding: **none**.

Successor armed: **no**.

S1.42AC is accepted under the corrected BCMER `1.71.0` static EventType probability model in `Current/118...`; S1.42AB is its accepted predecessor/rollback baseline.

After S1.42AC acceptance, the user explicitly requested the next build. The interrupted ChatGPT session selected the Functional Microwave rarity scope and committed a source-only project under `Patches/S142ADCodeRebirthMicrowaveSpawnTuning/`, but it did not build a profile or arm the controller. Recovery authority: `Current/119_S1.42AD_INTERRUPTED_IMPLEMENTATION_RECOVERY.md`.

A blocked pre-build plan now records the incomplete contract at `BuildSpecs/S1.42AD_PLAN.md`.

## S1.42AD pre-build gate

The current draft proposes a uniform Functional Microwave curve scale of `0.5`, implemented through the same narrow DawnLib provider-scaling pattern used by the accepted S1.42Z aerial-defense tuner.

However, the canonical user requirement currently establishes only that the Functional Microwave should become **rarer**. It does not specify an exact reduction percentage. Therefore the draft `0.5` value is not yet an accepted target.

Before S1.42AD may be armed:

1. resolve/confirm the exact desired spawn-rarity reduction magnitude;
2. independently verify the exact CodeRebirth `1.6.9` / DawnLib `0.9.25` / Dusk `0.9.25` owner path and 19-curve contract;
3. complete/finalize the Patch Safety Review and approved target/provenance in `BuildSpecs/S1.42AD_PLAN.md` under `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`;
4. only then arm/build the candidate repository-native.

Do not treat the source-only draft, blocked plan or its green Knowledge Architecture check as a built candidate.

## Remaining deferred independent gameplay/compatibility scopes

These remain separate unless the user explicitly selects or groups them:

- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown/despawn repair only with stronger evidence.

Functional Microwave spawn-rarity reduction is no longer merely deferred: it is the selected S1.42AD scope, currently stopped at the pre-build/source-review gate above.

## BCMER scope boundary

S1.42AC is the accepted BCMER 1.71.0 **static EventType probability** implementation. Eight equal `12.5` scales intentionally produce unequal inverse-population per-event weights while preserving approximately equal aggregate EventType mass within integer truncation.

Exact long-run 12.5% **executed** EventType frequency after all runtime eligibility filters would be a materially broader algorithm-design project and is not the same scope. It is not currently armed.

## Interior scope boundary

The inherited S1.42AB implementation already solves equal effective rarity for all **LLL-viable** interiors by normalizing positive returned rarities to 100 after viability filtering. S1.42AC does not modify that path.

Still separate:

- author/technical viability restrictions such as Shatteredrooms on Experimentation/Embrion;
- CullFactory compatibility;
- Mausoleum fog;
- route/NavMesh recovery.

Do not reopen the accepted interior-weight normalization just to solve one of those separate compatibility scopes.

## Repository-overhaul boundary

The overhaul is closed with `POST_ACCEPTANCE_REAUDIT_PASS`. Current summary: `Knowledge/REPOSITORY_OVERHAUL.md`. Final acceptance/audit evidence: `Current/110_REPOSITORY_OVERHAUL_FINAL_ACCEPTANCE.md`, `Current/111_REPOSITORY_OVERHAUL_POST_ACCEPTANCE_AUDIT.md` and `Current/OVERHAUL_VALIDATION_RESULTS.json`.

Future repository-architecture changes must remain separate from gameplay changes and continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves important historical planning and package research, but its S1.42U/S1.42V `current` checkpoint is historical. This file is the live roadmap authority after the repository overhaul.
