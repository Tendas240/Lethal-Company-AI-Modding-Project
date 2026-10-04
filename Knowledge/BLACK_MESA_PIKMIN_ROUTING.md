# Black Mesa / Interior / Pikmin Routing Evidence

**Status:** CURRENT / OPEN DEFERRED INVESTIGATION TOPIC  
**Authority:** scope boundary and routing to preserved evidence; no causal fix is currently accepted  
**Canonical-For:** `black_mesa_pikmin_routing`  
**Evidence:** S1.42AA/S1.42AC RuntimeEvidence and related runtime-analysis records; `Current/239_S1.42AK_BMAFR1I1_RUNTIME_ATTRIBUTION_RECONCILIATION.md`; `RuntimeEvidence/S1.42AK-BMAFR1I1/20261003T232317Z/`  
**Related:** `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/MONITOR_ONLY_ERRORS.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-10-04

## Current classification

Black Mesa/interior/Pikmin pathing remains a **separate deferred investigation**, not an accepted explanation for S1.42AC and not part of the repository information-architecture overhaul.

S1.42AC's config-only BCMER EventType delta preserved the S1.42AB interior-weighting regression checks, but its secondary runtime evidence still contained routing-related signatures. The project must not attribute those signatures to the BCMER EventType config without reproducibility.

Known AC secondary evidence included:

- 43 dominant `NavMeshAgent:SetDestination` error signatures;
- 26 LethalMin route-failure signatures.

These are evidence for a routing/pathing investigation, not proof of a specific root cause.

## Accepted facts that must remain separate

- S1.42AB's LLL post-viability rarity normalization passed and does not change flow membership.
- Black Mesa is single-registered and uses its own ownership path; do not duplicate-register it through LLL.
- The accepted S1.42AB Offense run generated `Expanded facility` and did not show a user-visible normalization regression.
- Prior Mineshaft/elevator + large Pikmin-group incidents also produced NavMesh-related failures, but causality was not established.

## Fresh BMAFR1I1 runtime evidence — SafeOutside / Pikmin lifecycle

The completed BMAFR1I1 multi-round log adds reproducible user-visible evidence without yet establishing one root cause:

- BCMER selected `SafeOutside` and explicitly logged `Outside spawning prevented by OutsideSafe`; this proves suppression of the ordinary outside-spawn path for that round.
- LethalMin nevertheless initialized many outdoor sprouts.
- A player-triggered Yellow Pikmin creation path reached `Spawning: Yellow Pikmin`, after which the spawned Pikmin was almost immediately removed from the exterior enemy list.
- An Onion withdrawal request for 15 Yellow Pikmin reached the spawn path. Repeated created Pikmin were staged around `(1000.78, 997.12, 996.33)`, emitted `Failed to create agent because it is not close enough to the NavMesh`, and were then repeatedly removed from the interior enemy list.
- Later scheduler additions for Maneater and Jester prove that this evidence does not support the stronger claim that SafeOutside disables every interior enemy spawn.
- The user's observed symptom — plucking/Onion withdrawal did not yield usable Pikmin — is therefore runtime-supported.

Interpretation remains bounded: SafeOutside is proven to block the normal outside-spawn route, but the Onion/interior classification plus staging/NavMesh failures establish a broader Pikmin lifecycle/routing problem that cannot be attributed solely to SafeOutside. No repair is authorized by this evidence alone.

## Investigation discipline

When this scope is explicitly selected:

1. reproduce on a controlled interior/moon/state;
2. distinguish interior geometry/NavMesh validity from LethalMin task/agent state;
3. identify whether Black Mesa-specific registration/table/navigation data is involved or whether the issue generalizes to other interiors;
4. avoid combining route recovery with unrelated balancing/config changes;
5. follow the project-local patch safety policy before adding any runtime repair hook;
6. preserve raw/log query evidence needed to prove causality.

Do not label the existing route signatures monitor-only if they become reproducibly user-facing. Conversely, do not patch them solely because they appear in a log without a demonstrated gameplay failure.

## Required future BCMER compatibility scope

`Current/251_BCMER_LETHALMIN_ALL_PIKMIN_EXEMPTION_SCOPE_CORRECTION.md` establishes the current desired compatibility boundary.

If source/static attribution proves a safe exemption point, BCMER hostile outside-enemy suppression/cleanup should exempt **Pikmins generally**, independent of player ownership or follow/assignment state. This includes Onion-withdrawn, plucked, idle/unassigned, player-following and other legitimate LethalMin Pikmin states.

Do not narrow the future fix to "player-owned Pikmin". Prefer an identity/classification-based Pikmin exemption while retaining BCMER suppression for unrelated hostile outside enemies.

This remains deferred and requires exact owner/callsite attribution before implementation.

