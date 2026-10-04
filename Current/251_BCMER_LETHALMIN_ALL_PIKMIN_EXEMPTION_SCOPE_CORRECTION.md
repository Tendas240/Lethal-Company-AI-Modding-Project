# BCMER x LethalMin Pikmin Exemption Scope Correction

**Date:** 2026-10-04  
**Status:** USER-DIRECTED SCOPE CORRECTION / ALL PIKMIN EXEMPTION TARGET / DEFERRED-BUT-MANDATORY  
**Supersedes only:** the "player-owned Pikmin" identity limitation in `Current/250_PHASE_C_DETERMINISTIC_INTERIOR_TEST_STRATEGY_AND_DEFERRED_BCMER_PIKMIN_DIRECTIVE.md` and related current summaries  
**Preserves:** record 250's deterministic single-interior test strategy and all existing evidence/causal uncertainty

## Correction

The intended future BCMER compatibility outcome is **not limited to player-owned Pikmin**.

The target scope is:

> **Pikmins generally should be exempt from Brutal Company Minus outside-enemy suppression/cleanup behavior that would otherwise kill, remove, block or invalidate them solely because they are represented through an exterior-enemy path or list.**

This applies regardless of current ownership/follow state, including but not limited to Pikmin associated with:

- Onion withdrawal;
- plucking/sprout creation;
- idle or unassigned Pikmin;
- following/player-associated Pikmin;
- other legitimate LethalMin Pikmin lifecycle states.

The exemption criterion should therefore be based on **Pikmin identity / LethalMin Pikmin classification**, not player ownership.

## Intended compatibility boundary

The future fix should preserve BCMER event semantics for ordinary hostile outside enemies while excluding Pikmin from destructive outside-enemy suppression/cleanup when technically safe.

The preferred architecture, if source/static attribution supports it, is a narrow identity/classification-based exemption for all Pikmin rather than:

- a player-ownership-only exemption;
- globally disabling `SafeOutside` or other BCMER events;
- broadly disabling outside-enemy cleanup for unrelated enemies.

## Evidence boundary

Current runtime evidence still proves correlation, not the exact destructive owner:

- `SafeOutside` explicitly suppresses outside spawning;
- Pikmin creation paths still instantiate Pikmin;
- the SafeOutside episode shows rapid exterior-list Pikmin death/removal;
- comparable non-SafeOutside episodes retain the recurring Onion staging/NavMesh warning without the same immediate death cascade.

Before implementation, the mandatory deferred source/static attribution must identify the exact cleanup/suppression path across BCMER, LethalMin, vanilla enemy-list handling, Starlancer AI Fix and any other relevant interceptor.

## No current implementation authorization

This correction changes the **required eventual compatibility scope only**.

It does not authorize a patch, build, runtime test, BCMER event disable, or immediate switch away from the current Phase-C interior-proof sequence.

## Current project progression

The current next action remains the bounded Phase-C residual interior-proof priority reassessment over the 30-flow residual set.

For future single-interior qualification, record 250's deterministic exact-target selection rule remains fully in force.
