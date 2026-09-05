# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only; historical build sequencing remains in chronology/lineage  
**Canonical-For:** `roadmap_and_deferred_scopes`  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md`, `Current/118_S1.42AC_RUNTIME_ACCEPTANCE_CORRECTED_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`, `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, `Current/127_S1.42AE_PATH_LENGTH_SUPERSESSION_AND_S1.42AF_PROMOTION.md`  
**Related:** `Knowledge/BCMER.md`, `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/BLACK_MESA_PIKMIN_ROUTING.md`, `Knowledge/ITEM_TUNING.md`, `Knowledge/CODEREBIRTH.md`, `Knowledge/REPOSITORY_OVERHAUL.md`  
**Last-Validated:** 2026-09-05

## Current position

Accepted gameplay baseline: **S1.42AC — BCMER EventType Equal Distribution**. Latest built artifact and active gameplay candidate: **S1.42AF — Path-Length-Safe Microwave Packaging — BUILD PASS / RUNTIME VALIDATION OUTSTANDING / NOT ACCEPTED**. Runtime test outstanding: **yes**. Successor armed: **no**. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AF`; `BuildSpecs/current.json` is disabled and guards S1.42AF.

S1.42AD remains runtime-rejected historical provider-contract evidence. S1.42AE's corrected provider code was never reached; it is superseded for packaging after the physically present SoundAPI binding failed through a 262-character runtime path. S1.42AF preserves the same functional source contract but shortens only the Gale profile identity.

## Exact next scope

The selected work is the **S1.42AF runtime acceptance gate**. Import through v2.4, require both SoundAPI materialization proofs, confirm the shortened binding path is below 260, start normally, play one ordinary run far enough for moon/interior generation, upload the fresh S1.42AF log with `Current/126_S1.42AF_BUILD_CANDIDATE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`, then accept or reject from deterministic provider and regression evidence. A single normal run is sufficient for this technical gate; it is not expected to statistically demonstrate an exact 50% observed Microwave count.

## Remaining deferred independent gameplay/compatibility scopes

- CullFactory disable-culling exceptions for exact IDs `junkrooms` / `shatteredrooms`;
- MelanieMausoleum fog reduction only for that interior;
- Black Mesa/interior/Pikmin route recovery;
- isolated evaluation of `woah25-LethalEscapeUpdated 2.5.0`;
- final long full-stack acceptance;
- AdditionalNetworking repair only with reproducible user-facing evidence;
- LethalMin teardown/despawn repair only with stronger evidence.

## BCMER scope boundary

S1.42AC remains the accepted BCMER 1.71.0 static EventType-probability implementation. Exact long-run executed EventType frequency after runtime eligibility filters is a broader algorithm-design scope and is not armed.

## Interior scope boundary

The inherited S1.42AB implementation already equalizes effective rarity for LLL-viable interiors after viability filtering. S1.42AC and S1.42AF do not alter that path. Author/technical viability restrictions, CullFactory compatibility, Mausoleum fog and route/NavMesh recovery remain separate.

## Repository-overhaul boundary

The overhaul is closed and validated. Future repository-architecture changes remain separate from gameplay changes and must continue to pass `.github/workflows/knowledge-architecture.yml`.

## Historical roadmap warning

`Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` preserves historical planning/package research only. This file plus `Current/CURRENT_STATE.json` and `Knowledge/CURRENT_LIFECYCLE.md` are the live roadmap/lifecycle authorities.
