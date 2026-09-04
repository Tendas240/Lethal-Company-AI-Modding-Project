# Interiors, LethalLevelLoader and Equal Effective Weighting

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** accepted interior-selection architecture and deferred compatibility exceptions  
**Canonical-For:** `interiors_and_lll`  
**Evidence:** `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`, `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`  
**Related:** `ProfileSources/S1.42AB/`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-04

## Accepted architecture

S1.42AB established the accepted permanent rule:

1. LethalLevelLoader `1.7.12` remains authoritative for whether a dungeon flow is viable/excluded on the current moon.
2. The project-local normalization runs **after** LLL's viability determination.
3. Every returned positive rarity is normalized to exactly `100`.
4. The patch does not add, remove, re-register or deduplicate flows.
5. Enemy, Scrap and MapObject rarity systems are untouched.

This means newly installed interiors automatically inherit effective rarity `100` whenever LLL itself returns them as viable.

## Runtime proof

Accepted S1.42AB Offense evidence:

- viable entries before normalization: 40;
- viable entries after normalization: 40;
- changed rarities: 12/40;
- pre-normalization range: 20..300;
- all positive final effective rarities: 100;
- Black Mesa appears exactly once;
- no excluded flow was inserted;
- `Expanded facility` generated successfully;
- no user-visible S1.42AB regression was reported.

Authoritative runtime marker:

`[InteriorWeightNormalization] Final effective viable pool for <moon>: ...`

## Equality rule

The project target is equal **effective** probability for every viable registered interior, not equal package shares and not theme-weighted author defaults. A package containing multiple flows contributes multiple independently normalized flows.

A technical author hard block is not a desired balancing exception. Do not blindly override one until its compatibility reason is understood and runtime-tested.

## Shatteredrooms restriction

Shatteredrooms is explicitly restricted on Experimentation and Embrion. S1.42AB intentionally preserves that LLL-side restriction because the project-local patch changes rarity only after viability filtering.

Desired long-term architecture is still equal availability/effective probability everywhere **if** the restriction can later be proven technically safe to remove. Until then, preserve it.

## CullFactory compatibility

Historically generated/confirmed exact interior IDs:

- Junkrooms: `junkrooms`
- Shatteredrooms: `shatteredrooms`

The deferred CullFactory compatibility scope is to add/validate disable-culling exceptions for those exact IDs. Do not guess alternate identifiers.

## Black Mesa ownership

Black Mesa uses its own DawnLib/native owner path. Do not duplicate-register it through LLL merely to force equal weighting. S1.42AB runtime confirms it remains single-registered and receives final effective rarity 100 in the viable list.

## Duplicate-registration rule

Avoid:

- pack + standalone duplication;
- LLL registration for content already owned by DawnLib/JLL/native configuration;
- duplicate Black Mesa registration.

## Deferred interior work

Keep separate from the already accepted S1.42AB weighting architecture:

- CullFactory `junkrooms` / `shatteredrooms` exceptions;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- any future attempt to remove the Shatteredrooms Experimentation/Embrion safety restriction.

Package-specific historical research remains in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`; this topic file is the current authority for the live interior-selection rule.
