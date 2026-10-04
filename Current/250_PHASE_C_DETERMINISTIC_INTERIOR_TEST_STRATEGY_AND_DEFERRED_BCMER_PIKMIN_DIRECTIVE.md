# Phase C Deterministic Interior-Test Strategy and Deferred BCMER x Pikmin Compatibility Directive

**Date:** 2026-10-04  
**Status:** USER-DIRECTED TEST STRATEGY RECORDED / DETERMINISTIC TARGET SELECTION REQUIRED FOR FUTURE SINGLE-INTERIOR TESTS / BCMER x PIKMIN FIX DEFERRED-BUT-MANDATORY  
**Parent runtime reconciliation:** `Current/249_S1.42AK_PHASE_C_ART_GALLERY_ORDINARY_RUNTIME_NON_TARGET_RECONCILIATION.md`  
**Scope:** test-method policy for future Phase-C single-interior runtime qualification plus preservation of the separate BCMER x LethalMin/Pikmin compatibility work

## Decision

Future runtime qualification of an individual interior must not rely on random dungeon selection when the purpose of the run is to test that specific interior.

Once a specific flow is separately selected and authorized for runtime qualification, the runtime setup must **deterministically select that exact target flow** so the intended interior actually generates during the test.

The preferred mechanism is a separately versioned diagnostic-only selector or equivalent narrowly scoped deterministic selection mechanism that changes the selection outcome only and preserves the target interior's normal generation/materialization behavior as far as technically possible.

A selector used for this purpose is diagnostic infrastructure and is **NEVER ACCEPT** as gameplay content unless a later explicit decision says otherwise.

## Safety boundaries

Deterministic selection must not silently change a different proof question.

For a flow that is already viable/eligible on the chosen moon, deterministic selection may replace stochastic choice for the bounded runtime qualification.

For an `AUTHOR_OR_OWNER_HARD_BLOCK` flow, deterministic selection must **not** be used to bypass the owner/availability restriction as an incidental side effect. Such a flow first requires a separate availability/safety decision that explicitly authorizes the exact test condition. Only after that prerequisite may a deterministic selector be used for the actual interior runtime qualification.

The selector should not, merely for convenience:

- alter unrelated interior weights or owner metadata permanently;
- remove owner restrictions globally;
- change generation size, entrance topology, enemy/scrap behavior or other gameplay semantics unless the specific test requires and separately authorizes that change;
- be treated as acceptance evidence for the selector itself.

The evidence record must always identify the exact selector/diagnostic bytes used, so deterministic selection is distinguishable from the gameplay profile under test.

## Art Gallery consequence

The ordinary Art Gallery acquisition in record 248 is complete and missed `MuseumInteriorFlow`.

If Art Gallery is selected again as a runtime target after the current residual-priority reassessment, the next Art Gallery qualification attempt should use deterministic `MuseumInteriorFlow` selection rather than another random Offense roll.

This directive does not itself authorize that future run or build.

## Deferred BCMER x LethalMin/Pikmin compatibility work

The BCMER/Pikmin compatibility issue from records 241 and 249 is explicitly retained as a **deferred-but-mandatory follow-up scope** and must not be lost during subsequent interior qualification work.

The desired end state is:

- Brutal Company Minus events such as `SafeOutside` may continue suppressing the hostile outside-enemy behavior they are designed to suppress;
- player-owned LethalMin Pikmin should, if technically safe, be exempt from the hostile outside-enemy suppression/cleanup path so Onion/pluck-created Pikmin are not immediately killed or removed merely because such an event is active.

Current evidence strongly correlates `SafeOutside` with immediate exterior-list Pikmin death while also proving that the recurring Onion staging-position NavMesh warning exists independently on non-`SafeOutside` runs. The exact destructive owner remains unresolved.

Before implementation, perform a bounded source/static attribution across BCMER, LethalMin, vanilla outside-enemy/list handling and Starlancer AI Fix (or any other observed interceptor) to identify the exact cleanup/suppression path. Prefer a narrow identity-based player-owned-Pikmin exemption over globally disabling BCMER events if the evidence supports it.

This directive does not authorize a patch, build or runtime test now. It records that the compatibility fix **must be revisited later**.

## Current next action remains unchanged

Complete the record-249 integration, then perform the bounded Phase-C residual interior-proof priority reassessment over the 30-flow residual set. Any subsequent single-interior runtime acquisition chosen by that process must follow the deterministic-selection rule above.
