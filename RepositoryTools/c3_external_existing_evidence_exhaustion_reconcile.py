#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-29"
CHECKPOINT = "Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_section(text: str, heading: str, body: str) -> str:
    marker = heading + "\n"
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"missing section: {heading}")
    body_start = start + len(marker)
    next_heading = text.find("\n## ", body_start)
    if next_heading < 0:
        return text[:body_start] + "\n" + body.rstrip() + "\n"
    return text[:body_start] + "\n" + body.rstrip() + "\n" + text[next_heading:]


# Controller invariants: this reconciliation is documentation/state only.
buildspec = json.loads(read("BuildSpecs/current.json"))
assert buildspec["enabled"] is False
assert buildspec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS"
assert read("RuntimeInbox/ACTIVE_BUILD.txt").strip() == "S1.42AK-BMDSFIX1"

state_path = ROOT / "Current/CURRENT_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
assert state["accepted_baseline"]["build_id"] == "S1.42AK"
assert state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1"
assert state["runtime_test_outstanding"] is True
scope = state["selected_scope"]
assert scope["scope_id"] == "UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY"
assert scope["phase_b"]["phase_b3_matrix"] == "Current/167_S1.42AK_UNIVERSAL_INTERIOR_PHASE_B3_MATRIX.csv"
assert scope["phase_b"]["matrix_classification_totals"] == {
    "viable_equal_100": 662,
    "author_or_owner_hard_block": 14,
    "config_gap": 0,
    "known_technical_restriction": 0,
    "not_yet_proven": 914,
    "total": 1590,
}

state["updated"] = DATE
scope["status"] = "PHASE_C3_EXTERNAL_EXISTING_EVIDENCE_EXHAUSTED_OWNER_RULE_APPLICABILITY_RECONCILIATION_NEXT_BMDSFIX1_TARGET_PASSIVE_OUTSTANDING"
scope["finding"] = (
    "Post-Greenhouse Phase-C3 reconciliation has now exhausted the already-ingested External-moon pair evidence that can be resolved without a new run. "
    "Black Mesa x Greenhouse is a full bounded pair-specific runtime-compatibility PASS; Black Mesa x Slaughterhouse, ExpandedFacility, Decrepit store/StoreFlow and Substation have dedicated generation/topology/materialization reconciliations from existing evidence, with traversal strength varying by pair. "
    "No additional already-ingested Black Mesa pair remains available for the same reconciliation path. The regular exact-byte S1.42AK-BMDSFIX1 Black Mesa x DeepSewersFlow gameplay gate remains passive, outstanding and unwaived and must not be forced by dedicated rerolls. "
    "For Oxyde, existing C3E3H source/owner evidence establishes 23 selection-supported pairings at the metadata layer but also preserves spawnEnemiesAndScrap=false, the exact V81 early return before ordinary GenerateNewFloor, no directly identified serialized entrance topology, and no inspected independent dungeon/entrance-construction path. Therefore no concrete Oxyde interior pair may be promoted from current evidence into an executable ordinary runtime pairing. "
    "The Phase-B3 matrix remains the unchanged historical availability/effective-weight snapshot. No new runtime, build or universal availability override is authorized by this reconciliation."
)
scope["analysis_contract"] = (
    "Treat Current/199, 200, 201, 202 and 204 as the completed Black Mesa pair-specific Phase-C evidence set currently available without a new run, and SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md as the bounded Oxyde ordinary-generation applicability authority. "
    "Do not infer unobserved Black Mesa pair compatibility from the five reconciled pairs, do not reinterpret Oxyde selection metadata as executable ordinary dungeon generation, and do not rewrite the historical Phase-B3 matrix from pair-specific Phase-C evidence. "
    "Keep S1.42AK-BMDSFIX1 unaccepted, keep its exact regular DeepSewersFlow gameplay gate passive/outstanding/unwaived, preserve the accepted S1.42AB InteriorWeightNormalization mechanism, avoid duplicate Black Mesa LLL registration, preserve Shatteredrooms exclusions, and keep the separate Black Mesa/Pikmin routing-recovery scope closed."
)
scope["next_action"] = (
    "Perform a bounded repository-native Phase-C3 External owner-rule applicability reconciliation using existing source/owner/config evidence only. Across the 53 selectable interiors, classify which current owner/config matching mechanisms can legitimately target Black Mesa's External semantics without duplicate registration, and separately preserve Oxyde's proven ordinary-generation boundary rather than treating its 23 selection-supported metadata matches as executable pairings. Determine whether C3 can close with an explicit Oxyde exception plus a Black Mesa-supported applicability set, or whether a narrowly defined additional evidence requirement remains. Do not create or release a runtime/build in that source/metadata reconciliation, do not force DeepSewersFlow, and do not implement a universal availability override yet."
)
phase_c = scope["phase_c"]
phase_c["status"] = "C3_IN_PROGRESS_EXTERNAL_EXISTING_PAIR_EVIDENCE_EXHAUSTED_OWNER_RULE_APPLICABILITY_NEXT"
phase_c["external_existing_evidence_reconciliation"] = CHECKPOINT
phase_c["external_existing_evidence_inventory_status"] = "EXHAUSTED_NO_NEXT_PAIR_RESOLVABLE_FROM_ALREADY_INGESTED_EVIDENCE"
phase_c["black_mesa_reconciled_pair_checkpoints"] = [
    "Current/199_S1.42AK_BMGHDIAG3_RUNTIME_COMPATIBILITY_PASS.md",
    "Current/200_S1.42AK_BLACK_MESA_SLAUGHTERHOUSE_RUNTIME_TOPOLOGY_RECONCILIATION.md",
    "Current/201_S1.42AK_BLACK_MESA_EXPANDED_FACILITY_RUNTIME_TOPOLOGY_RECONCILIATION.md",
    "Current/202_S1.42AK_BLACK_MESA_DECREPIT_STORE_RUNTIME_TOPOLOGY_PARTIAL_TRAVERSAL_RECONCILIATION.md",
    "Current/204_S1.42AK_BLACK_MESA_SUBSTATION_RUNTIME_TOPOLOGY_PARTIAL_TRAVERSAL_RECONCILIATION.md",
]
phase_c["black_mesa_existing_pair_evidence_status"] = "EXHAUSTED_NO_ADDITIONAL_INGESTED_PAIR_RECONCILIATION_AVAILABLE_DEEP_SEWERS_TARGET_REMAINS_PASSIVE"
phase_c["oxyde_c3e3h_evidence"] = "SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md"
phase_c["oxyde_selection_supported_pairings"] = 23
phase_c["oxyde_ordinary_generation_status"] = "NOT_PROVEN_APPLICABLE_SPAWN_ENEMIES_AND_SCRAP_FALSE_ORDINARY_GENERATION_SKIPPED_NO_ALTERNATE_CONSTRUCTION_ESTABLISHED"
phase_c["external_owner_rule_applicability_status"] = "NEXT_SOURCE_METADATA_RECONCILIATION_NO_RUNTIME_RELEASED"
phase_c["external_owner_rule_applicability_next_action"] = scope["next_action"]
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

checkpoint = f"""# S1.42AK External-Moon Existing-Evidence Exhaustion Reconciliation

**Date:** {DATE}  
**Status:** EXISTING EXTERNAL-MOON PAIR EVIDENCE EXHAUSTED / NO NEXT PAIR RESOLVABLE WITHOUT NEW EVIDENCE / OWNER-RULE APPLICABILITY RECONCILIATION NEXT / NO NEW RUNTIME OR BUILD AUTHORIZED / NO B3 MATRIX CHANGE  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted  
**Runtime attribution pointer:** S1.42AK-BMDSFIX1 — attribution only, not acceptance authority  
**Controller:** `BuildSpecs/current.json` remains `enabled=false`, `build_id=IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`

## Bounded objective

This checkpoint closes the focused inventory requested by `Current/204_S1.42AK_BLACK_MESA_SUBSTATION_RUNTIME_TOPOLOGY_PARTIAL_TRAVERSAL_RECONCILIATION.md`.

The question is deliberately narrow:

> After Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation have been reconciled, does already-ingested External-moon evidence contain another concrete pair whose generation/topology/traversal obligations can be resolved without a new runtime run?

No new diagnostic, build, capture or gameplay mechanism is introduced here.

## Black Mesa existing pair evidence is exhausted

The already-ingested Black Mesa pair-specific Phase-C evidence currently available for post-Greenhouse reconciliation is now represented by:

- `Current/199_S1.42AK_BMGHDIAG3_RUNTIME_COMPATIBILITY_PASS.md` — Greenhouse, full bounded pair-specific runtime-compatibility PASS;
- `Current/200_S1.42AK_BLACK_MESA_SLAUGHTERHOUSE_RUNTIME_TOPOLOGY_RECONCILIATION.md` — Slaughterhouse topology/materialization reconciliation;
- `Current/201_S1.42AK_BLACK_MESA_EXPANDED_FACILITY_RUNTIME_TOPOLOGY_RECONCILIATION.md` — ExpandedFacility topology/materialization reconciliation;
- `Current/202_S1.42AK_BLACK_MESA_DECREPIT_STORE_RUNTIME_TOPOLOGY_PARTIAL_TRAVERSAL_RECONCILIATION.md` — Decrepit store / StoreFlow topology plus partial traversal reconciliation;
- `Current/204_S1.42AK_BLACK_MESA_SUBSTATION_RUNTIME_TOPOLOGY_PARTIAL_TRAVERSAL_RECONCILIATION.md` — Substation four-relationship / three-alternate topology/materialization PASS with at least one direct exterior-to-interior player traversal.

`Current/203_S1.42AK_BLACK_MESA_REMAINING_PAIR_EVIDENCE_INVENTORY_SUBSTATION_NEXT.md` had already identified Substation as the remaining already-ingested Black Mesa pair suitable for this evidence-only treatment. `204` has now consumed that opportunity.

No additional already-ingested Black Mesa pair is established by current repository evidence as another concrete generation/topology/traversal case ready for the same reconciliation without acquiring new evidence.

## Deep Sewers remains outside the inventory path

Black Mesa x `DeepSewersFlow` remains the exact regular `S1.42AK-BMDSFIX1` gameplay target gate.

That gate is still **passive, outstanding and unwaived**. The supporting DIAG1PATH1 PASS does not substitute for regular exact-byte gameplay qualification. No dedicated reroll, deterministic selector or seed-control mechanism is authorized merely to force Deep Sewers selection.

If unrelated normal exact-byte BMDSFIX1 gameplay later selects `DeepSewersFlow` naturally, that evidence may still be ingested against the existing gate.

## Oxyde is not a hidden next concrete pair

`SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md` remains the bounded Oxyde applicability authority.

Existing evidence establishes at the selection/metadata layer that 23 rules can match Oxyde. It does **not** establish an executable ordinary interior pairing because the exact inspected architecture also establishes:

1. Oxyde preserves `spawnEnemiesAndScrap=false`;
2. exact V81 returns before the ordinary `RuntimeDungeon` / `GenerateNewFloor` path;
3. the exact Oxyde scene bundle contains no directly identified serialized `EntranceTeleport` topology;
4. no inspected CodeRebirth/Dawn owner path establishes an independent dungeon or entrance-pair construction route.

Accordingly the existing 23 positive selection matches must not be reinterpreted as 23 runnable Oxyde pair cases. Current evidence also does not prove that Oxyde is broken, can never support interiors, or has zero runtime entrances; it proves only the bounded current ordinary-generation applicability limitation.

There is therefore no repository-supported basis to select an arbitrary Oxyde x Interior pair as the next evidence-only runtime reconciliation.

## Inventory result

**NO NEXT CONCRETE EXTERNAL-MOON PAIR IS RESOLVABLE FROM THE ALREADY-INGESTED EVIDENCE SET WITHOUT ACQUIRING NEW EVIDENCE.**

This is an evidence-exhaustion result, not a declaration that Phase C3 is globally complete and not an authorization to start a runtime test.

The result separates the two External rows correctly:

- **Black Mesa:** real ordinary interior generation and four-entrance topology are established, and five concrete pair lines now have dedicated Phase-C reconciliation; remaining unseen pairs are not inferred compatible merely from those examples.
- **Oxyde:** positive selection metadata exists, but ordinary executable interior generation is not established under the inspected current architecture.

## Historical matrix and accepted architecture remain unchanged

The Phase-B3 matrix remains the fixed historical snapshot:

- 662 `VIABLE_EQUAL_100`;
- 14 `AUTHOR_OR_OWNER_HARD_BLOCK`;
- 0 `CONFIG_GAP`;
- 0 `KNOWN_TECHNICAL_RESTRICTION`;
- 914 `NOT_YET_PROVEN`;
- 1,590 total cells.

Pair-specific Phase-C evidence does not rewrite those historical classifications.

Also preserved unchanged:

- accepted S1.42AK gameplay baseline;
- unaccepted S1.42AK-BMDSFIX1 candidate;
- accepted S1.42AB InteriorWeightNormalization mechanism;
- Black Mesa Dawn/native ownership without duplicate LLL registration;
- Shatteredrooms exclusions;
- separate closed Black Mesa/Pikmin routing-recovery scope;
- disabled build controller and exact BMDSFIX1 runtime-attribution pointer.

## Next bounded Phase-C3 action

Perform a repository-native **External Owner-Rule Applicability Reconciliation** using existing source/owner/config evidence only.

Across the 53 selectable interiors, classify which current owner/config matching mechanisms can legitimately target Black Mesa's External semantics without duplicate registration. Keep Oxyde separate: its 23 selection-supported metadata matches must remain bounded by the proven `spawnEnemiesAndScrap=false` / ordinary-generation-skipped architecture unless an independent construction path is actually established.

The purpose of that next step is to determine whether Phase C3 can close with an explicit Oxyde exception plus a supported Black Mesa applicability set, or whether a narrowly defined additional evidence requirement remains.

Do **not** create or release a runtime/build in that source/metadata reconciliation. Do not force `DeepSewersFlow`. Do not implement a universal availability override yet.
"""
write(CHECKPOINT, checkpoint)

# Current lifecycle topic.
lifecycle_path = "Knowledge/CURRENT_LIFECYCLE.md"
lifecycle = read(lifecycle_path).replace("**Last-Validated:** 2026-09-27", "**Last-Validated:** 2026-09-29")
section = """`Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` closes the post-Substation existing-evidence inventory.

The already-ingested Black Mesa pair set available without a new run is now exhausted after dedicated reconciliations for Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation. This does not generalize those pair results to unseen interiors. The separate regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` gameplay gate remains passive, outstanding and unwaived and is not converted into an active reroll target.

Oxyde remains governed by the bounded C3E3H source/owner result: 23 selection-supported metadata pairings exist, but `spawnEnemiesAndScrap=false` causes exact V81 to return before ordinary dungeon generation and no inspected independent dungeon/entrance-construction path is established. Those metadata matches are therefore not executable ordinary pair proof.

No additional concrete External-moon pair can currently be reconciled from already-ingested evidence alone. The next bounded C3 step is source/metadata-only External owner-rule applicability classification across the 53 interiors; no runtime/build is released by this evidence-exhaustion decision.
"""
if "## Phase C3 External existing-evidence exhaustion" not in lifecycle:
    lifecycle = lifecycle.replace("\n## Live execution state\n", "\n## Phase C3 External existing-evidence exhaustion\n\n" + section + "\n## Live execution state\n")
live_body = """- Accepted baseline: **S1.42AK**.
- Latest built artifact / active gameplay candidate: **S1.42AK-BMDSFIX1 — not accepted**.
- Runtime/evidence pointer: **S1.42AK-BMDSFIX1**.
- BMGHDIAG3: **Black Mesa x Greenhouse runtime-compatibility PASS / DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**.
- Black Mesa pair-specific Phase-C evidence reconciled from existing evidence: **Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow, Substation**; no additional already-ingested Black Mesa pair is currently available for the same evidence-only reconciliation path.
- Oxyde: **23 selection-supported metadata pairings, but ordinary executable interior generation is not proven applicable under the current inspected architecture; no independent alternate construction path is established**.
- Runtime test outstanding: **yes — solely the passive/unwaived regular BMDSFIX1 Black Mesa x `DeepSewersFlow` gameplay qualification**. No dedicated reroll is released.
- BMDSFIX1 regular Black Mesa x `DeepSewersFlow` gameplay qualification: **passive / outstanding / unwaived**; unrelated natural exact-byte target evidence may still satisfy the existing gate if later encountered and ingested.
- DIAG1PATH1: **supporting Deep Sewers diagnostic PASS / NEVER ACCEPT / not runtime-active**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 base bytes.
- Phase-B3 remains its unchanged historical 30x53 availability/effective-weight snapshot.
- The separate Black Mesa/Pikmin routing-recovery scope remains closed.
"""
lifecycle = replace_section(lifecycle, "## Live execution state", live_body)
next_body = scope["next_action"] + "\n\nNo Gale replacement/import command or runtime-log uploader is released because this reconciliation authorizes neither a new runtime test nor a finished-log upload."
lifecycle = replace_section(lifecycle, "## Exact next project action", next_body)
write(lifecycle_path, lifecycle)

# Semantic topic authority.
interiors_path = "Knowledge/INTERIORS_AND_LLL.md"
interiors = read(interiors_path).replace("**Last-Validated:** 2026-09-19", "**Last-Validated:** 2026-09-29")
old = "No build or runtime test is currently authorized by this selection. Phases C1 and C2 are complete. The exact next action is Phase C3: resolve Black Mesa moon and Oxyde External-level tags, entrance/fire-exit topology and owner matching semantics before any availability rule is extended onto their External rows."
new = "No build or runtime test is currently authorized by this selection. Phases C1 and C2 are complete. Phase C3 has now exhausted the already-ingested concrete External-moon pair evidence available without a new run: Black Mesa has dedicated pair reconciliations for Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation, while Oxyde remains bounded by C3E3H's ordinary-generation applicability result. `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` records that no further concrete pair can be resolved from the existing evidence set. The next bounded action is an External owner-rule applicability reconciliation across all 53 selectable interiors using existing source/owner/config evidence only; no runtime/build is released by that step."
if old not in interiors:
    raise RuntimeError("INTERIORS_AND_LLL expected Phase-C3 next-action paragraph not found")
interiors = interiors.replace(old, new)
current_section = """`Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` is the current Phase-C3 inventory boundary.

Black Mesa's already-ingested concrete pair evidence is exhausted after Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation. Only Greenhouse has the stronger full all-four-ID bidirectional traversal plus visual geometry qualification; the other pair records retain their narrower topology/traversal proof boundaries. None is generalized to all 53 interiors.

Oxyde remains asymmetric: C3E3H preserves 23 selection-supported metadata matches but exact V81 ordinary generation is skipped while `spawnEnemiesAndScrap=false`, and no independent inspected dungeon/entrance-construction path is established. Selection support is therefore not executable ordinary pair proof.

The next C3 task is source/metadata-only owner-rule applicability classification for the External rows. It must identify which existing owner/config rules legitimately target Black Mesa External semantics and keep Oxyde's generation boundary explicit. No new runtime, build or universal availability override is authorized by this checkpoint.
"""
if "## Phase C3 current External evidence boundary" not in interiors:
    interiors = interiors.replace("\n## Shatteredrooms restriction\n", "\n## Phase C3 current External evidence boundary\n\n" + current_section + "\n## Shatteredrooms restriction\n")
write(interiors_path, interiors)

# Human router current lifecycle anchor.
map_path = "Current/PROJECT_KNOWLEDGE_MAP.md"
knowledge_map = read(map_path).replace("**Last-Validated:** 2026-09-28", "**Last-Validated:** 2026-09-29")
map_body = """Accepted gameplay baseline: **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**. Active gameplay candidate / latest built gameplay artifact: **S1.42AK-BMDSFIX1 — not accepted**.

The selected **Universal Interior Viability / Equal Availability** scope remains in Phase C3. The fixed Phase-B3 30x53 availability/effective-weight matrix remains an unchanged historical snapshot at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`; pair-specific Phase-C evidence does not rewrite those historical classifications.

The already-ingested External-moon pair evidence that can be reconciled without a new run is now exhausted. Black Mesa has dedicated current pair records for Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation. Greenhouse is the full bounded pair-specific runtime-compatibility PASS; the other records retain narrower topology/traversal boundaries. No additional already-ingested Black Mesa pair is available for the same evidence-only reconciliation path. Decision: `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md`.

Oxyde remains governed by `SourceEvidence/UniversalInteriorViability/PhaseC3E3H/FINDINGS.md`: 23 selection-supported metadata pairings exist, but exact V81 skips ordinary dungeon generation while `spawnEnemiesAndScrap=false`, and no independent inspected dungeon/entrance-construction path is established. Those metadata matches are not executable ordinary pair proof.

BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT** and is no longer runtime-active. Runtime/evidence routing remains exact `S1.42AK-BMDSFIX1`. BMDSFIX1 remains the separate active gameplay candidate / **NOT ACCEPTED**; its regular exact-byte Black Mesa x `DeepSewersFlow` qualification remains passive, outstanding and unwaived, with no dedicated reroll released. `BuildSpecs/current.json` remains disabled.

Exact next action: perform the bounded repository-native Phase-C3 **External owner-rule applicability reconciliation** across the 53 selectable interiors using existing source/owner/config evidence only. Classify which current rules legitimately target Black Mesa External semantics without duplicate registration, preserve Oxyde's ordinary-generation boundary, and determine whether C3 can close with an explicit Oxyde exception plus a supported Black Mesa applicability set or whether a narrowly defined additional evidence requirement remains. No runtime/build or universal availability override is authorized by this step.
"""
knowledge_map = replace_section(knowledge_map, "## Current lifecycle anchor", map_body)
write(map_path, knowledge_map)

# Live roadmap.
roadmap_path = "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
roadmap = read(roadmap_path).replace("**Last-Validated:** 2026-09-28", "**Last-Validated:** 2026-09-29")
position = """Accepted gameplay baseline remains **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**, SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

Latest built artifact and active gameplay candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted and its exact regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding/unwaived.

The Black Mesa x Greenhouse BMGHDIAG3 diagnostic remains a completed pair-specific runtime-compatibility PASS and diagnostic only / NEVER ACCEPT. Subsequent existing-evidence reconciliations cover Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation. `Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` now records that no additional concrete External-moon pair can be resolved from already-ingested evidence without acquiring new evidence. `RuntimeInbox/ACTIVE_BUILD.txt` remains exact BMDSFIX1 for attribution only; `BuildSpecs/current.json` remains disabled.
"""
roadmap = replace_section(roadmap, "## Current position", position)
selected = """**Universal Interior Viability / Equal Availability — SELECTED / PHASE C3 IN PROGRESS / EXISTING EXTERNAL PAIR EVIDENCE EXHAUSTED / EXTERNAL OWNER-RULE APPLICABILITY RECONCILIATION NEXT / BMDSFIX1 GAMEPLAY QUALIFICATION PASSIVE OUTSTANDING.**

The authoritative 30x53 B3 matrix and accepted S1.42AB post-viability normalizer remain unchanged. Black Mesa's five reconciled pair lines are additive Phase-C evidence only. Oxyde retains 23 selection-supported metadata pairings but ordinary executable generation is not proven applicable under the inspected `spawnEnemiesAndScrap=false` architecture. No universal override is authorized.

Plan: `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`.
"""
roadmap = replace_section(roadmap, "## Selected scope", selected)
roadmap = replace_section(roadmap, "## Exact next selected-scope action", scope["next_action"])
write(roadmap_path, roadmap)

# Investigation plan: preserve original C3 contract but record the current checkpoint and exact next bounded analysis.
plan_path = "BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md"
plan = read(plan_path)
old_status = "**Status:** SELECTED / PHASE A + B1 + B2 + B3 + C1 + C2 COMPLETE / PHASE C3 EXTERNAL-MOON ANALYSIS OUTSTANDING / NOT IMPLEMENTED / NOT ARMED  "
new_status = "**Status:** SELECTED / PHASE A + B1 + B2 + B3 + C1 + C2 COMPLETE / PHASE C3 EXTERNAL-MOON ANALYSIS IN PROGRESS / EXISTING PAIR EVIDENCE EXHAUSTED / OWNER-RULE APPLICABILITY RECONCILIATION NEXT / NOT IMPLEMENTED / NOT ARMED  "
if old_status not in plan:
    raise RuntimeError("plan status line not found")
plan = plan.replace(old_status, new_status)
phase_c_note = """### Phase C3 current evidence-exhaustion checkpoint

`Current/205_S1.42AK_EXTERNAL_MOON_EXISTING_EVIDENCE_EXHAUSTION_RECONCILIATION.md` records that the already-ingested concrete External-moon pair evidence is exhausted: Black Mesa Greenhouse, Slaughterhouse, ExpandedFacility, Decrepit store / StoreFlow and Substation have dedicated Phase-C reconciliations, while no additional concrete pair can be resolved without new evidence. The passive regular BMDSFIX1 Deep Sewers gameplay gate is not converted into a dedicated reroll target.

Oxyde remains bounded by C3E3H: 23 selection-supported metadata matches exist, but exact V81 ordinary generation is skipped while `spawnEnemiesAndScrap=false`, with no inspected independent dungeon/entrance-construction path established. Selection support is not executable ordinary pair proof.

The next bounded C3 task is therefore owner-rule applicability classification across the 53 interiors using existing source/owner/config evidence only. This step decides which current rules legitimately target Black Mesa External semantics and whether C3 can close with an explicit Oxyde exception or needs a narrowly defined additional evidence requirement. No runtime/build or universal override is authorized by this checkpoint.

"""
if "### Phase C3 current evidence-exhaustion checkpoint" not in plan:
    plan = plan.replace("\n## Phase D — candidate rule\n", "\n" + phase_c_note + "## Phase D — candidate rule\n")
plan = replace_section(plan, "## Exact next action", scope["next_action"] + "\n\nNo universal override, gameplay build or runtime test is authorized by this step.")
write(plan_path, plan)

print("C3 external existing-evidence exhaustion reconciliation staged successfully")
