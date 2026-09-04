# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, durable rules extracted from `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`  
**Last-Validated:** 2026-09-04

## Current position

Accepted gameplay baseline: **S1.42AB**.

Active gameplay candidate: **none**.

Runtime test outstanding: **none**.

Successor armed: **no**.

The repository information-architecture overhaul is the currently active maintenance scope and must not modify gameplay behavior.

## Deferred independent gameplay/compatibility scopes

These remain separate unless the user explicitly selects or groups them:

- reconsider existing S1.42AC under the corrected BCMER static EventType acceptance model;
- Functional Microwave spawn-rarity reduction;
- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown/despawn repair only with stronger evidence.

## BCMER scope boundary

The existing S1.42AC equal-scale concept is the correct BCMER 1.71.0 **static EventType probability** implementation. Its old rejection interpretation is superseded, but the artifact is still not promoted automatically.

Exact long-run 12.5% **executed** EventType frequency after all runtime eligibility filters would be a materially broader algorithm-design project and is not the same scope.

## Interior scope boundary

S1.42AB already solves equal effective rarity for all **LLL-viable** interiors by normalizing positive returned rarities to 100 after viability filtering.

Still separate:

- author/technical viability restrictions such as Shatteredrooms on Experimentation/Embrion;
- CullFactory compatibility;
- Mausoleum fog;
- route/NavMesh recovery.

Do not reopen the accepted interior-weight normalization just to solve one of those separate compatibility scopes.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves important historical planning and package research, but its S1.42U/S1.42V `current` checkpoint is historical. This file is the live roadmap authority after the repository overhaul.
