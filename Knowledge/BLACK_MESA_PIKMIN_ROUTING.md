# Black Mesa / Interior / Pikmin Routing Evidence

**Status:** CURRENT / OPEN DEFERRED INVESTIGATION TOPIC  
**Authority:** scope boundary and routing to preserved evidence; no causal fix is currently accepted  
**Canonical-For:** `black_mesa_pikmin_routing`  
**Evidence:** S1.42AA/S1.42AC RuntimeEvidence and related runtime-analysis/handover records  
**Related:** `Knowledge/INTERIORS_AND_LLL.md`, `Knowledge/MONITOR_ONLY_ERRORS.md`, `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`  
**Last-Validated:** 2026-09-04

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

## Investigation discipline

When this scope is explicitly selected:

1. reproduce on a controlled interior/moon/state;
2. distinguish interior geometry/NavMesh validity from LethalMin task/agent state;
3. identify whether Black Mesa-specific registration/table/navigation data is involved or whether the issue generalizes to other interiors;
4. avoid combining route recovery with unrelated balancing/config changes;
5. follow the project-local patch safety policy before adding any runtime repair hook;
6. preserve raw/log query evidence needed to prove causality.

Do not label the existing route signatures monitor-only if they become reproducibly user-facing. Conversely, do not patch them solely because they appear in a log without a demonstrated gameplay failure.
