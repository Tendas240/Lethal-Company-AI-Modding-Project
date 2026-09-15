#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

R2_ID = "S1.42AI-DIAG1R2"
R2_TITLE = "ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair"
R2_PROFILE = "Profiles/LC V1 S1.42AI-DIAG1R2 ShyGuy Isolation Applicability Repair.r2z"
R2_SHA = "9dd67d6ea015274596e11651a8c1a842d50c7f7b913332794cce43d389169d15"
R2_REQUEST = "BuildSpecs/S1.42AI-DIAG1R2_REQUEST.md"
R2_VALIDATION = "AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.json"
R2_VALIDATION_MD = "AnalysisEvidence/S1.42AI-DIAG1R2/MATERIALIZED_VALIDATION.md"
R2_APPLICABILITY = "AnalysisEvidence/S1.42AI-DIAG1R2/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json"
R2_BUILD_RUN = 34958254886
R2_BUILD_COMMIT = "854e4435676ef32648407dae9ba1e2e704a420d1"
R2_VALIDATION_RUN = 34990530260
R2_VALIDATION_COMMIT = "aa78a0f6c7da14f9caa8bacd1e0f2d2a0d2b709c"
R2_PLUGIN_SHA = "099a54571dc0595638fbd2f338c67137f42734b8aedf80478005dff314a0a3b3"

ACCEPTED_PROFILE = "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z"
ACCEPTED_SHA = "06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e"
IDLE_ID = "IDLE_AFTER_S1.42AI-DIAG1R2_MATERIALIZED_VALIDATION_AWAITING_RUNTIME_CANDIDATE_ACTIVATION"
MARKER = "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R2 candidate=none runtime_test_outstanding=false -->"


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, value: dict) -> None:
    (ROOT / rel).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def replace_section(text: str, start_heading: str, end_heading: str, replacement: str) -> str:
    start = text.index(start_heading)
    end = text.index(end_heading, start)
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


def update_state() -> None:
    state = load_json("Current/CURRENT_STATE.json")
    if state.get("accepted_baseline", {}).get("build_id") != "S1.42AH":
        raise RuntimeError("accepted baseline drifted")
    if state.get("active_candidate") is not None or state.get("runtime_test_outstanding") is not False:
        raise RuntimeError("repair requires no active candidate and no outstanding runtime test")

    state["updated"] = "2026-09-15"
    state["latest_built_artifact"] = {
        "build_id": R2_ID,
        "title": R2_TITLE,
        "status": "BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION_NOT_ACCEPTED",
        "profile": R2_PROFILE,
        "sha256": R2_SHA,
        "request_record": R2_REQUEST,
        "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R2/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json",
        "workflow_run": R2_BUILD_RUN,
        "build_commit": R2_BUILD_COMMIT,
        "parent": "S1.42AI",
        "parent_full_normal": "S1.42AI",
        "materialized_validation": R2_VALIDATION,
        "materialized_validation_md": R2_VALIDATION_MD,
        "materialized_applicability": R2_APPLICABILITY,
        "materialized_validation_workflow_run": R2_VALIDATION_RUN,
        "validation_evidence_commit": R2_VALIDATION_COMMIT,
        "plugin_dll_sha256": R2_PLUGIN_SHA,
        "metadata_derived_pikmin_type": "LethalMin.Pikmin.PikminType",
    }
    state["active_candidate"] = None
    state["runtime_test_outstanding"] = False

    selected = state["selected_scope"]
    selected["status"] = "DIAGNOSTIC_R2_BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION_FULL_NORMAL_GATE_DEFERRED_NOT_WAIVED"
    selected["finding"] = (
        "S1.42AI-DIAG1R2 was rebuilt directly from the exact S1.42AI full-normal base after the landed "
        "kite.ZelevatorCode EndlessElevator applicability repair. Canonical post-build validation proves the exact R2 profile passes "
        "the DIAG1 static gate, materialized dependency-absent NOT_APPLICABLE contract, and semantic DLL equivalence to the repaired "
        "green-gate build. R2 is built and verified but is not yet an active runtime candidate; runtime attribution remains on failed "
        "R1 until a separate coordinated lifecycle transition explicitly arms R2."
    )
    selected["analysis_contract"] = R2_REQUEST
    selected["analysis_status"] = "DIAG1R2_BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION"
    selected["failed_candidate_build_id"] = "S1.42AI-DIAG1R1"
    selected["successor_build_id"] = R2_ID
    selected["profile"] = R2_PROFILE
    selected["sha256"] = R2_SHA
    selected["build_request_record"] = R2_REQUEST
    selected["build_plan"] = "BuildSpecs/S1.42AI_PLAN.md"
    selected["static_evidence"] = R2_VALIDATION_MD
    selected["materialized_validation"] = R2_VALIDATION
    selected["diagnostic_revision"] = {
        "build_id": R2_ID,
        "status": "BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION_NOT_ACCEPTED",
        "plan": "BuildSpecs/S1.42AI_PLAN.md",
        "request_record": R2_REQUEST,
        "guard_contract": "AnalysisEvidence/S1.42AI-DIAG1R1/MINIMAL_GUARD_CONTRACT.md",
        "base_build_id": "S1.42AI",
        "base_profile": "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z",
        "base_sha256": "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2",
        "enemy_allowlist": "Exact Shy Guy identity only: ShyGuyDef asset, enemyName Shy Guy, prefab component ShyGuy.AI.ShyGuyAI; fail closed if the identity triple is missing, ambiguous or contradictory",
        "bcmer_event_allowlist": ["ShyGuy"],
        "full_normal_validation": "DEFERRED_UNTIL_AFTER_DIAGNOSTIC_NOT_WAIVED",
        "profile": R2_PROFILE,
        "sha256": R2_SHA,
        "workflow_run": R2_BUILD_RUN,
        "build_commit": R2_BUILD_COMMIT,
        "plugin_dll_sha256": R2_PLUGIN_SHA,
        "materialized_validation": R2_VALIDATION,
        "materialized_validation_workflow_run": R2_VALIDATION_RUN,
        "endless_elevator_applicability": "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY",
    }
    selected["currently_irrelevant_actions"] = [
        "Do not rerun failed S1.42AI-DIAG1 or S1.42AI-DIAG1R1 unchanged.",
        "Do not rebuild S1.42AI-DIAG1R2 unchanged; the exact R2 artifact is already built and static/materialized validated.",
        "Do not import R2 into Gale or request gameplay until a separate coordinated lifecycle transition makes R2 the active candidate and sets runtime_test_outstanding = true.",
        "Do not execute the deferred full-normal S1.42AI acceptance gate before the diagnostic path is resolved; that gate remains mandatory and is not waived.",
        "Do not treat RuntimeInbox/ACTIVE_BUILD.txt as acceptance authority or as proof that a runtime test is currently outstanding.",
        "Do not fold Shy Guy inside-to-outside pursuit into the current failure root cause; Can Exit Facility is inherited false and that behavior is a separate scope unless explicitly selected.",
    ]

    state["next_action"] = (
        "S1.42AI-DIAG1R2 is built and repository-natively static/materialized validated. The next project action is a separate "
        "coordinated lifecycle transition that, after re-verifying the exact R2 profile/evidence and no-candidate state, activates R2 "
        "as the runtime diagnostic candidate, moves RuntimeInbox/ACTIVE_BUILD.txt to R2, changes the disabled BuildSpecs guard from "
        "accepted S1.42AH to R2, updates candidate/project-state and artifact-integrity authorities, and only then sets "
        "runtime_test_outstanding = true. Do not import/test R2 before that transition. The full-normal S1.42AI gate remains deferred, not waived."
    )
    state["controllers"] = {
        "buildspec": "BuildSpecs/current.json",
        "build_enabled": False,
        "build_id": IDLE_ID,
        "build_base_profile": ACCEPTED_PROFILE,
        "build_base_sha256": ACCEPTED_SHA,
        "runtime_active_build_file": "RuntimeInbox/ACTIVE_BUILD.txt",
        "runtime_active_build": "S1.42AI-DIAG1R1",
    }
    write_json("Current/CURRENT_STATE.json", state)


def update_buildspec() -> None:
    write_json(
        "BuildSpecs/current.json",
        {
            "enabled": False,
            "build_id": IDLE_ID,
            "base_profile": ACCEPTED_PROFILE,
            "base_sha256": ACCEPTED_SHA,
            "output_profile": "Profiles/DO_NOT_BUILD.r2z",
            "profile_name": "DO_NOT_BUILD",
            "overwrite": False,
            "mod_state_changes": [],
            "mod_additions": [],
            "mod_removals": [],
            "config_patches": [],
            "local_plugin_builds": [],
            "text_assertions": [],
        },
    )


def update_lineage() -> None:
    lineage = load_json("Current/BUILD_LINEAGE.json")
    lineage["date"] = "2026-09-15"
    lineage["latest_built_artifact_id"] = R2_ID
    builds = lineage["builds"]
    builds = [b for b in builds if b.get("id") != R2_ID]
    builds.append(
        {
            "id": R2_ID,
            "title": R2_TITLE,
            "status": "built-static-materialized-validated-awaiting-runtime-candidate-activation",
            "parent": "S1.42AI",
            "profile": R2_PROFILE,
            "sha256": R2_SHA,
            "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
            "decision_record": R2_REQUEST,
            "workflow_run": R2_BUILD_RUN,
            "build_commit": R2_BUILD_COMMIT,
            "materialized_validation": R2_VALIDATION,
            "safe_as_gameplay_base": False,
            "principal_feature": "DIAG1 EndlessElevator applicability repair rebuilt and canonical materialization verified before runtime activation",
        }
    )
    lineage["builds"] = builds
    write_json("Current/BUILD_LINEAGE.json", lineage)

    path = ROOT / "Current/BUILD_LINEAGE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("**Last-Validated:** 2026-09-14", "**Last-Validated:** 2026-09-15", 1)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("- **Latest built artifact:**"):
            lines[i] = "- **Latest built artifact:** S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**."
        elif line.startswith("- **Current action:**"):
            lines[i] = "- **Current action:** perform a separate coordinated lifecycle transition to activate exact verified R2 as the runtime diagnostic candidate; do not import/test before `runtime_test_outstanding = true`."
    if not any(line.startswith("| S1.42AI-DIAG1R2 |") for line in lines):
        for i, line in enumerate(lines):
            if line.startswith("| S1.42AI-DIAG1R1 |"):
                lines.insert(
                    i + 1,
                    "| S1.42AI-DIAG1R2 | **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME ACTIVATION / NOT ACCEPTED** | Rebuilt directly from exact S1.42AI with the landed `kite.ZelevatorCode` applicability repair; canonical profile SHA `9dd67d6e...` passed static, materialized applicability and semantic DLL-equivalence gates. |",
                )
                break
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_knowledge_map() -> None:
    path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    lines[0] = MARKER
    text = "\n".join(lines) + "\n"
    text = text.replace("**Last-Validated:** 2026-09-14", "**Last-Validated:** 2026-09-15", 1)
    anchor = f"""## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.

Latest built artifact: **S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — BUILT + STATIC/MATERIALIZED VALIDATED / NOT ACCEPTED**. Exact profile SHA-256: `{R2_SHA}`. Canonical validation: `{R2_VALIDATION}` with run `{R2_VALIDATION_RUN}`.

There is **no active runtime candidate** and no new runtime test is outstanding. `BuildSpecs/current.json` is disabled and guards accepted S1.42AH while awaiting the separate R2 runtime-candidate activation transition. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R1` remains attribution for the last completed failed runtime run only.

The next action is the coordinated lifecycle transition that explicitly activates exact verified R2 and only then sets `runtime_test_outstanding = true`. Do not import/test R2 before that transition. The ordinary full-normal S1.42AI gate remains deferred and not waived.
"""
    text = replace_section(text, "## Current lifecycle anchor", "## Authority rule", anchor)
    path.write_text(text, encoding="utf-8")


def update_live_docs() -> None:
    lifecycle = f"""{MARKER}
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `{R2_REQUEST}`, `{R2_VALIDATION_MD}`, `{R2_APPLICABILITY}`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1R2 — ShyGuy Isolation Diagnostic EndlessElevator Applicability Repair — BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**  
Profile: `{R2_PROFILE}`  
SHA-256: `{R2_SHA}`  
Build request: `{R2_REQUEST}`  
Build workflow run: `{R2_BUILD_RUN}` (`workflow_dispatch`, success)  
Build commit: `{R2_BUILD_COMMIT}`  
Canonical post-build validation: `{R2_VALIDATION_MD}` / run `{R2_VALIDATION_RUN}` (`push`, success)

R2 is the newly compiled successor of failed R1 and remains directly derived from exact full-normal S1.42AI, never from R1 bytes. The persisted validation proves the DIAG1 static contract, the materialized `kite.ZelevatorCode` dependency-absent `NOT_APPLICABLE` behavior, and semantic DLL equivalence to the repaired green-gate build.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R2**, verified but not accepted.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `{IDLE_ID}` and guards accepted S1.42AH.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R1` remains evidence attribution for the last completed failed R1 run; it is not acceptance authority and does not authorize gameplay.

## R1 history and R2 repair

R1 remains a completed failed diagnostic: it proved metadata-derived `LethalMin.Pikmin.PikminType`, then invalidated because it incorrectly required `ElevatorMod.Patches.EndlessElevator` when dependency GUID `kite.ZelevatorCode` was absent. The permanent source contract is now: dependency absent => only that compat target is `NOT_APPLICABLE`; dependency present => exact provider/type/owner/signature/install remains required and fail-closed. R2 contains and materializes that repaired contract.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate remains mandatory and is **deferred, not waived**. Diagnostic success cannot accept the full-normal candidate.

## Exact next project action

Perform a **separate coordinated R2 runtime-candidate activation transition**. Re-verify exact R2 profile/evidence and no-candidate state, then atomically move the disabled BuildSpecs guard to R2, update `RuntimeInbox/ACTIVE_BUILD.txt` to R2, create/update the R2 candidate/project-state and artifact-integrity authorities, set `active_candidate = S1.42AI-DIAG1R2`, and only then set `runtime_test_outstanding = true`. Do not import R2 into Gale or request gameplay before that transition is merged and Exact-HEAD validated.
"""
    (ROOT / "Knowledge/CURRENT_LIFECYCLE.md").write_text(lifecycle, encoding="utf-8")

    roadmap = f"""{MARKER}
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{R2_REQUEST}`, `{R2_VALIDATION_MD}`, `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-15

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1R2**, SHA-256 `{R2_SHA}`, is built and repository-natively static/materialized validated but is not accepted and is not yet an active runtime candidate. There is no new gameplay test outstanding.

R2 is the rebuilt successor of failed R1 and contains the landed `kite.ZelevatorCode` EndlessElevator applicability repair. Canonical R2 materialization proves dependency absent => this compat target is `NOT_APPLICABLE`; dependency present => the exact provider/owner/signature/install contract remains required and fail-closed.

## Active scope

Perform the separate coordinated lifecycle transition that activates exact verified R2 as the runtime diagnostic candidate. Until that transition sets `runtime_test_outstanding = true`, do not import/test R2 and do not move runtime attribution away from the last completed R1 run.

The observed Shy Guy failure to follow the player from inside to outside remains a separate scope explained by inherited Scopophobia `Can Exit Facility = false`; it is not part of the current BCMER interior-only spawn correction.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the diagnostic path is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation, including inside-to-outside enemy transition compatibility as a separate scope from ordinary exterior spawning.
- Final long full-stack acceptance.
- AdditionalNetworking repair only with reproducible evidence.
- Broader LethalMin teardown/despawn repair only with stronger evidence.
"""
    (ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md").write_text(roadmap, encoding="utf-8")

    integrity = f"""{MARKER}
# Artifact and Runtime Evidence Integrity

**Status:** CURRENT / CANONICAL EVIDENCE-RETRIEVAL INDEX  
**Machine mirror:** `Current/ARTIFACT_EVIDENCE_INTEGRITY.json`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline: S1.42AH

Artifact: `{ACCEPTED_PROFILE}`  
SHA-256: `{ACCEPTED_SHA}`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

## Latest built artifact: S1.42AI-DIAG1R2

Artifact: `{R2_PROFILE}`  
SHA-256: `{R2_SHA}`  
Build request: `{R2_REQUEST}`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R2/`  
FILE_INDEX: `ProfileSources/S1.42AI-DIAG1R2/FILE_INDEX.json`  
Build workflow run: `{R2_BUILD_RUN}`  
Build commit: `{R2_BUILD_COMMIT}`  
Canonical materialized validation: `{R2_VALIDATION_MD}` / `{R2_VALIDATION}`  
Materialized EndlessElevator applicability: `{R2_APPLICABILITY}`  
Validation workflow run: `{R2_VALIDATION_RUN}`

R2 is built and verified but has **no runtime decision yet** and is **not an active candidate yet**. The machine index continues to classify runtime-decided profiles and runtime-pending candidates; R2 enters the pending-candidate section only in the later coordinated activation transition. Exact R2 artifact/snapshot/materialized evidence is already repository-readable.

## Completed failed diagnostic predecessor: S1.42AI-DIAG1R1

R1 remains preserved as completed failed diagnostic evidence under `Current/147_S1.42AI-DIAG1R1_RUNTIME_FAILURE_COMPLEX_OWNER_TARGET_RESOLUTION.md`, `ProfileSources/S1.42AI-DIAG1R1/`, and `RuntimeEvidence/S1.42AI-DIAG1R1/20260914T110719Z/`.

## Failed predecessor diagnostic

S1.42AI-DIAG1 remains preserved under `Current/145_S1.42AI-DIAG1_RUNTIME_FAILURE_OWNER_TYPE_RESOLUTION.md` and `RuntimeEvidence/S1.42AI-DIAG1/20260913T202638Z/`.

## Deferred full-normal S1.42AI gate

S1.42AI remains `DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED`. Its full-normal runtime acceptance gate remains mandatory after the diagnostic path is resolved.

## Retrieval invariant

Reasoning-critical facts must exist in readable ProfileSources, FILE_INDEX, runtime INDEX/analysis, source, build record, or canonical documentation rather than only opaque binary/log bytes.
"""
    (ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md").write_text(integrity, encoding="utf-8")


def main() -> None:
    update_state()
    update_buildspec()
    update_lineage()
    update_knowledge_map()
    update_live_docs()


if __name__ == "__main__":
    main()
