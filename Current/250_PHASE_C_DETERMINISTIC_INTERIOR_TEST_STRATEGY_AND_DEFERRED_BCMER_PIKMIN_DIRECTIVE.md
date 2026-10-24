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

## 2026-10-24 — Explicit one-shot exploratory normal-stack multi-interior exception (owner-directed)

**Scope and authority:** The project owner separately chose a **bounded exploratory multi-target acquisition**, not a targeted single-interior qualification, after the documented S1.42AK V1/V2 natural Offense evidence and the blocked CKDIAG1 selector path. This is a **new explicit test-policy exception**, **not a new technical method**, a new authenticated evidence event, a reversal of an old BLOCKED source finding, or a general repeal of the anti-loop gate. It takes effect only after this amendment is merged and validated on the exact new `main` head. The decision to document the exception is **not** an authorization to play, import Gale, edit a controller, upload a log, publish, build or run any tool.

**Exactly permitted proposal, subject to later separate operational authorization:**

- **One finite exploratory campaign only**, with **at most six naturally selected Offense landings total**. No per-target six-run quota, no automatic reset, seed/RNG manipulation, selection retry, target-specific weighting, synthetic eligibility, Harmony/selector hook, new DLL or gameplay config change.
- Use only the unchanged **accepted S1.42AK full normal stack**, profile `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`, pinned repository profile SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`, subject to the normal Gale/profile provenance and runtime-attribution preflight. `S1.42AK-BMDSFIX1` remains active **NOT ACCEPTED** with its separate passive selector-free Black Mesa **moon** x `DeepSewersFlow` proof outstanding and unwaived.
- Observe **all five** still-missing viable Offense flow-generation witnesses opportunistically: Black Mesa **INTERIOR** / `Black Mesa` (not the moon), Crimson Keep / `CrimsonKeep`, Goldstay Hotel / `GoldenHotel`, Museum / `MelanieMuseum` (not Art Gallery / `MuseumInteriorFlow`), Shatteredrooms / `shatteredrooms`. No owner-blocked flow is made viable. Shatteredrooms' Experimentation/Embrion exclusions and CullFactory risks remain.
- Stop the campaign at the **first naturally selected target attempt** once its normal generation outcome can be captured, at any material safety/generation failure, or after the sixth landing, whichever comes first. No success is presumed from merely selecting a name. A non-target or incomplete target attempt is **INCONCLUSIVE**, never negative target-compatibility evidence, and gives no automatic permission for more landings.
- If later separately authorized, retain **one unaltered original LogOutput.log for the bounded campaign**, including non-target outcomes; require exact profile/build attribution, observed selection/day-history, ordinary DunGen/player-floor completion, exact target-flow CullFactory materialization and genuinely observed entrance relationships, consistent episode boundaries, original byte SHA-256 and provenance. A positive episode may qualify only its own **Offense basic-generation/materialization tier** after independent ingestion and proof review; it never establishes natural frequency, traversal, NavMesh, other-moon compatibility, P0–P6 completion or acceptance.
- The current ordinary `RuntimeInbox/ACTIVE_BUILD.txt` and `CURRENT_STATE.controllers.runtime_active_build` point to **S1.42AK-BMDSFIX1**. Do **not** upload S1.42AK evidence through the ordinary BMDSFIX1-attributed inbox. A new separately approved exact S1.42AK upload/ingest attribution contract or appropriately approved controller transition is a **mandatory prerequisite**, and the consumed S1.42AK V1/V2 special-upload identities must not be reused. Follow original-byte retention `PRESERVE_UNTIL_SEPARATE_P0_P6_AND_RETENTION_DECISION`, no automatic deletion, and independent rights/safety protections.

**Rule precedence and stopping:** Current/250's **deterministic exact-target requirement remains fully binding for any future deliberately targeted individual-interior qualification**. This exception is only for the specified exploratory multi-target campaign and must not disguise repeated targeted stochastic rerolls. Historical CKDIAG1/Harmony/owner/selector/RNG fingerprints stay BLOCKED/parked. The anti-loop/no-input-poll ban still applies to previously exhausted source/evidence searches and to **all additional batches**; the finite campaign is a transparent owner-directed departure from the former stochastic-acquisition default, not proof of technical novelty. Another batch requires fresh specific evidence or a new, explicit, independently justified policy/safety decision: not a generic "weiter", missing target or unchanged log. **No mutation of `Current/CURRENT_STATE.json`, `BuildSpecs/current.json`, runtime pointers, source, profile, logs, original indices or actual gameplay is authorized by this documentation PR.**

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
