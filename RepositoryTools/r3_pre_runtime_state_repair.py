#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

R3_ID = "S1.42AI-DIAG1R3"
R3_TITLE = "ShyGuy Isolation Diagnostic Exact Identity Repair"
R3_PROFILE = "Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z"
R3_SHA = "13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768"
R3_REQUEST = "BuildSpecs/S1.42AI-DIAG1R3_REQUEST.md"
R3_VALIDATION = "AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.json"
R3_VALIDATION_MD = "AnalysisEvidence/S1.42AI-DIAG1R3/MATERIALIZED_VALIDATION.md"
R3_APPLICABILITY = "AnalysisEvidence/S1.42AI-DIAG1R3/ENDLESS_ELEVATOR_MATERIALIZED_APPLICABILITY.json"
R3_BUILD_RUN = 35021307391
R3_BUILD_COMMIT = "19914cff25cb768cffe22694e93df150e45bdd2f"
R3_VALIDATION_RUN = 35023265624
R3_VALIDATION_COMMIT = "bed4e8aa810c01eec608db24bccea5811fbdc7c8"
R3_PLUGIN_SHA = "98b464e559120dc43e8041f163ceab038506e045f4b3cd4c71be8687e9c5da7a"

R2_ID = "S1.42AI-DIAG1R2"
R2_FAILURE = "Current/149_S1.42AI-DIAG1R2_RUNTIME_FAILURE_SHYGUY_IDENTITY_CASE_MISMATCH.md"
R2_RUNTIME = "RuntimeEvidence/S1.42AI-DIAG1R2/20260915T164428Z/"

ACCEPTED_PROFILE = "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z"
ACCEPTED_SHA = "06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e"
IDLE_ID = "IDLE_AFTER_S1.42AI-DIAG1R3_MATERIALIZED_VALIDATION_AWAITING_RUNTIME_CANDIDATE_ACTIVATION"
MARKER = "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI-DIAG1R3 candidate=none runtime_test_outstanding=false -->"


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
    if state.get("latest_built_artifact", {}).get("build_id") != R2_ID:
        raise RuntimeError("pre-reconciliation latest artifact is not failed R2")
    if state.get("selected_scope", {}).get("successor_build_id") != R3_ID:
        raise RuntimeError("CURRENT_STATE does not identify R3 as prepared successor")

    state["updated"] = "2026-09-15"
    state["latest_built_artifact"] = {
        "build_id": R3_ID,
        "title": R3_TITLE,
        "status": "BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION_NOT_ACCEPTED",
        "profile": R3_PROFILE,
        "sha256": R3_SHA,
        "request_record": R3_REQUEST,
        "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
        "profile_sources": "ProfileSources/S1.42AI-DIAG1R3/",
        "file_index": "ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json",
        "workflow_run": R3_BUILD_RUN,
        "build_commit": R3_BUILD_COMMIT,
        "parent": "S1.42AI",
        "parent_full_normal": "S1.42AI",
        "materialized_validation": R3_VALIDATION,
        "materialized_validation_md": R3_VALIDATION_MD,
        "materialized_applicability": R3_APPLICABILITY,
        "materialized_validation_workflow_run": R3_VALIDATION_RUN,
        "validation_evidence_commit": R3_VALIDATION_COMMIT,
        "plugin_dll_sha256": R3_PLUGIN_SHA,
        "metadata_derived_pikmin_type": "LethalMin.Pikmin.PikminType",
        "shyguy_identity": {
            "asset": "ShyGuyDef",
            "enemyName": "Shy guy",
            "aiType": "ShyGuy.AI.ShyGuyAI",
            "comparison": "StringComparison.Ordinal",
        },
    }
    state["active_candidate"] = None
    state["runtime_test_outstanding"] = False

    selected = state["selected_scope"]
    selected["status"] = "DIAGNOSTIC_R3_BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION_FULL_NORMAL_GATE_DEFERRED_NOT_WAIVED"
    selected["finding"] = (
        "S1.42AI-DIAG1R3 was built directly from exact full-normal S1.42AI after the runtime-proven R2 identity failure. "
        "Canonical post-build validation proves the exact ShyGuyDef / enemyName 'Shy guy' / ShyGuy.AI.ShyGuyAI identity contract "
        "with StringComparison.Ordinal, preserves metadata-derived LethalMin owner resolution and dependency-absent EndlessElevator "
        "NOT_APPLICABLE behavior, and proves decompiled C# plus normalized IL semantic equivalence to the repaired SDK8 green gate. "
        "R3 is built and verified but is not yet an active runtime candidate; runtime attribution remains on completed failed R2 until "
        "a separate coordinated lifecycle transition explicitly activates R3."
    )
    selected["analysis_contract"] = R3_REQUEST
    selected["analysis_status"] = "DIAG1R3_BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION"
    selected["failed_candidate_build_id"] = R2_ID
    selected["successor_build_id"] = R3_ID
    selected["profile"] = R3_PROFILE
    selected["sha256"] = R3_SHA
    selected["build_request_record"] = R3_REQUEST
    selected["build_plan"] = "BuildSpecs/S1.42AI_PLAN.md"
    selected["static_evidence"] = R3_VALIDATION_MD
    selected["materialized_validation"] = R3_VALIDATION
    selected["candidate_build_id"] = None
    selected["diagnostic_revision"] = {
        "build_id": R3_ID,
        "status": "BUILT_STATIC_MATERIALIZED_VALIDATED_AWAITING_RUNTIME_CANDIDATE_ACTIVATION_NOT_ACCEPTED",
        "plan": "BuildSpecs/S1.42AI_PLAN.md",
        "request_record": R3_REQUEST,
        "base_build_id": "S1.42AI",
        "base_profile": "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z",
        "base_sha256": "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2",
        "enemy_allowlist": "Exact runtime-proven ShyGuy identity only: ShyGuyDef asset, enemyName Shy guy, prefab component ShyGuy.AI.ShyGuyAI, all exact/ordinal and fail closed if missing, ambiguous or contradictory",
        "bcmer_event_allowlist": ["ShyGuy"],
        "full_normal_validation": "DEFERRED_UNTIL_AFTER_DIAGNOSTIC_NOT_WAIVED",
        "profile": R3_PROFILE,
        "sha256": R3_SHA,
        "workflow_run": R3_BUILD_RUN,
        "build_commit": R3_BUILD_COMMIT,
        "plugin_dll_sha256": R3_PLUGIN_SHA,
        "materialized_validation": R3_VALIDATION,
        "materialized_validation_workflow_run": R3_VALIDATION_RUN,
        "endless_elevator_applicability": "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY",
        "identity_validation": "PASS_EXACT_SHYGUY_RUNTIME_IDENTITY_ORDINAL",
    }
    selected["currently_irrelevant_actions"] = [
        "Do not rerun S1.42AI-DIAG1, S1.42AI-DIAG1R1 or S1.42AI-DIAG1R2 unchanged.",
        "Do not rebuild S1.42AI-DIAG1R3 unchanged; the exact R3 artifact is already built and static/materialized validated.",
        "Do not import R3 into Gale or request gameplay until a separate coordinated lifecycle transition makes R3 the active candidate and sets runtime_test_outstanding = true.",
        "Do not broaden ShyGuy identity matching to case-insensitive, substring, alias, asset-only or AI-type-only matching; R3 preserves the exact runtime-proven ordinal identity triple.",
        "Do not execute the deferred full-normal S1.42AI acceptance gate before the diagnostic path is resolved; that gate remains mandatory and is not waived.",
        "Do not treat RuntimeInbox/ACTIVE_BUILD.txt as acceptance authority or as proof that a runtime test is currently outstanding.",
    ]

    state["next_action"] = (
        "S1.42AI-DIAG1R3 is built and repository-natively static/materialized validated. The next project action is a separate "
        "coordinated lifecycle transition that re-verifies the exact R3 artifact/evidence and no-candidate state, then activates R3 as "
        "the runtime diagnostic candidate, moves RuntimeInbox/ACTIVE_BUILD.txt from completed failed R2 to R3, changes the disabled "
        "BuildSpecs guard from accepted S1.42AH to R3, creates/updates R3 candidate/project-state and artifact-integrity authorities, "
        "and only then sets runtime_test_outstanding = true. Do not import/test R3 before that transition. The full-normal S1.42AI gate remains deferred, not waived."
    )
    state["controllers"] = {
        "buildspec": "BuildSpecs/current.json",
        "build_enabled": False,
        "build_id": IDLE_ID,
        "build_base_profile": ACCEPTED_PROFILE,
        "build_base_sha256": ACCEPTED_SHA,
        "runtime_active_build_file": "RuntimeInbox/ACTIVE_BUILD.txt",
        "runtime_active_build": R2_ID,
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
    lineage["latest_built_artifact_id"] = R3_ID
    builds = [b for b in lineage["builds"] if b.get("id") != R3_ID]
    builds.append(
        {
            "id": R3_ID,
            "title": R3_TITLE,
            "status": "built-static-materialized-validated-awaiting-runtime-candidate-activation",
            "parent": "S1.42AI",
            "profile": R3_PROFILE,
            "sha256": R3_SHA,
            "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
            "decision_record": R3_REQUEST,
            "workflow_run": R3_BUILD_RUN,
            "build_commit": R3_BUILD_COMMIT,
            "materialized_validation": R3_VALIDATION,
            "safe_as_gameplay_base": False,
            "principal_feature": "DIAG1 exact runtime-proven ShyGuy identity literal repair rebuilt and canonical materialization verified before runtime activation",
        }
    )
    lineage["builds"] = builds
    features = lineage.setdefault("feature_index", {})
    features.pop("BCMER_ShyGuy_DIAG1_exact_identity_repair_prepared", None)
    features["BCMER_ShyGuy_DIAG1_exact_identity_repair"] = R3_ID
    invariants = [x for x in lineage.get("lineage_invariants", []) if "S1.42AI-DIAG1R3" not in str(x)]
    invariants.append(
        "S1.42AI-DIAG1R3 was built directly from exact S1.42AI, not from failed R2 bytes. It changes only the exact runtime-proven enemyName literal to 'Shy guy' while preserving ordinal/fail-closed identity, owner and applicability guards; canonical materialized validation passed, but R3 is not an active runtime candidate and cannot waive the deferred full-normal S1.42AI gate."
    )
    lineage["lineage_invariants"] = invariants
    write_json("Current/BUILD_LINEAGE.json", lineage)

    path = ROOT / "Current/BUILD_LINEAGE.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    r3_row = "| S1.42AI-DIAG1R3 | **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME ACTIVATION / NOT ACCEPTED** | Built directly from exact S1.42AI with the literal-only runtime-proven `Shy guy` identity repair; canonical profile SHA `13d73d8a...` passed static, materialized applicability, decompiled-C# and normalized-IL semantic gates. No runtime candidate is active yet. |"
    out = []
    inserted = False
    for line in lines:
        if line.startswith("- **Latest built artifact:**"):
            line = "- **Latest built artifact:** S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — **BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**."
        elif line.startswith("- **Prepared successor:**"):
            line = "- **Prepared successor:** none; R3 is already built/verified and awaits a separate runtime-candidate activation transition."
        elif line.startswith("- **Current action:**"):
            line = "- **Current action:** perform a separate coordinated lifecycle transition to activate exact verified R3 as the runtime diagnostic candidate; do not import/test before `runtime_test_outstanding = true`."
        elif line.startswith("| S1.42AI-DIAG1R2 |"):
            line = "| S1.42AI-DIAG1R2 | **RUNTIME DIAGNOSTIC FAILED / REPAIR REQUIRED / NOT ACCEPTED** | R2 armed the owner/applicability repairs, then failed exact ShyGuy identity resolution because source required ordinal `Shy Guy` while runtime proved `Shy guy`; failure authority: `Current/149...`. |"
            out.append(line)
            if not any(x.startswith("| S1.42AI-DIAG1R3 |") for x in lines):
                out.append(r3_row)
                inserted = True
            continue
        elif line.startswith("| S1.42AI-DIAG1R3 |"):
            line = r3_row
            inserted = True
        out.append(line)
    if not inserted:
        raise RuntimeError("could not place R3 build-lineage row")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def update_knowledge_map() -> None:
    path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    lines[0] = MARKER
    text = "\n".join(lines) + "\n"
    anchor = f"""## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**.

Latest built artifact: **S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — BUILT + STATIC/MATERIALIZED VALIDATED / NOT ACCEPTED**. Exact profile SHA-256: `{R3_SHA}`. Canonical validation: `{R3_VALIDATION}` with run `{R3_VALIDATION_RUN}`.

R3 was built directly from exact full-normal S1.42AI and binds the runtime-proven exact identity `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` with `StringComparison.Ordinal`. Static, materialized applicability and semantic DLL-equivalence gates are green.

There is **no active runtime candidate** and no new runtime test is outstanding. `BuildSpecs/current.json` is disabled and guards accepted S1.42AH while awaiting the separate R3 runtime-candidate activation transition. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R2` remains attribution for the last completed failed runtime run only.

The next action is the coordinated lifecycle transition that explicitly activates exact verified R3 and only then sets `runtime_test_outstanding = true`. Do not import/test R3 before that transition. The ordinary full-normal S1.42AI gate remains deferred and not waived.
"""
    text = replace_section(text, "## Current lifecycle anchor", "## Authority rule", anchor)
    path.write_text(text, encoding="utf-8")


def update_live_docs() -> None:
    lifecycle = f"""{MARKER}
# Current Project Lifecycle

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** current lifecycle router; detailed acceptance/rejection remains in build-specific evidence  
**Canonical-For:** accepted baseline, active candidate, pending test/build state, exact next project action  
**Evidence:** `{R3_REQUEST}`, `{R3_VALIDATION_MD}`, `{R3_APPLICABILITY}`, `{R2_FAILURE}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`, `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
**Last-Validated:** 2026-09-15

## Accepted gameplay baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK** remains the sole accepted gameplay base.

## Latest built artifact

**S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — BUILT + STATIC/MATERIALIZED VALIDATED / AWAITING RUNTIME-CANDIDATE ACTIVATION / NOT ACCEPTED**  
Profile: `{R3_PROFILE}`  
SHA-256: `{R3_SHA}`  
Build request: `{R3_REQUEST}`  
Build workflow run: `{R3_BUILD_RUN}` (`workflow_dispatch`, success)  
Build commit: `{R3_BUILD_COMMIT}`  
Canonical post-build validation: `{R3_VALIDATION_MD}` / run `{R3_VALIDATION_RUN}` (`push`, success)

R3 was built directly from exact full-normal S1.42AI, not from failed R2 bytes. The persisted validation proves the exact runtime identity `ShyGuyDef` / `Shy guy` / `ShyGuy.AI.ShyGuyAI` with `StringComparison.Ordinal`, preserves metadata-derived LethalMin owner resolution and dependency-absent EndlessElevator `NOT_APPLICABLE` handling, and proves decompiled C# plus normalized IL semantic equivalence to the repaired SDK8 green gate.

## Live execution state

- Accepted baseline: **S1.42AH**.
- Latest built artifact: **S1.42AI-DIAG1R3**, verified but not accepted.
- Active candidate: **none**.
- Runtime test outstanding: **no**.
- `BuildSpecs/current.json` is disabled at `{IDLE_ID}` and guards accepted S1.42AH.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R2` remains evidence attribution for the last completed failed R2 run; it is not acceptance authority and does not authorize gameplay.

## R2 history and R3 repair

R2 remains a completed failed diagnostic under `{R2_FAILURE}` / `{R2_RUNTIME}`. It proved the metadata-derived owner and EndlessElevator applicability repairs at runtime, then rejected the real ShyGuy only because its exact ordinal `enemyName` literal was `Shy Guy` instead of runtime `Shy guy`. R3 repairs only that literal and preserves the exact fail-closed identity triple and all predecessor guards.

## Retained full-normal gate

S1.42AI remains unaccepted. Its full-normal BCMER ShyGuy gate remains mandatory and is **deferred, not waived**. Diagnostic success cannot accept the full-normal candidate.

## Exact next project action

Perform a **separate coordinated R3 runtime-candidate activation transition**. Re-verify exact R3 profile/evidence and no-candidate state, then atomically move the disabled BuildSpecs guard to R3, update `RuntimeInbox/ACTIVE_BUILD.txt` to R3, create/update the R3 candidate/project-state and artifact-integrity authorities, set `active_candidate = S1.42AI-DIAG1R3`, and only then set `runtime_test_outstanding = true`. Do not import R3 into Gale or request gameplay before that transition is merged and Exact-HEAD validated.
"""
    (ROOT / "Knowledge/CURRENT_LIFECYCLE.md").write_text(lifecycle, encoding="utf-8")

    roadmap = f"""{MARKER}
# Live Roadmap and Deferred Scopes

**Status:** CURRENT / CANONICAL TOPIC  
**Authority:** live selected/deferred-scope list only  
**Evidence:** `Current/CURRENT_STATE.json`, `Knowledge/CURRENT_LIFECYCLE.md`, `{R3_REQUEST}`, `{R3_VALIDATION_MD}`, `{R2_FAILURE}`, `Current/143_S1.42AI_BUILD_CANDIDATE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
**Last-Validated:** 2026-09-15

## Current position

Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1R3**, SHA-256 `{R3_SHA}`, is built and repository-natively static/materialized validated but is not accepted and is not yet an active runtime candidate. There is no new gameplay test outstanding.

R3 is the direct exact-S1.42AI rebuild that repairs only the R2 runtime-proven ShyGuy identity capitalization. Canonical materialization proves exact ordinal `Shy guy`, preserved metadata-derived owner resolution and preserved dependency-absent EndlessElevator `NOT_APPLICABLE` behavior.

## Active scope

Perform the separate coordinated lifecycle transition that activates exact verified R3 as the runtime diagnostic candidate. Until that transition sets `runtime_test_outstanding = true`, do not import/test R3 and do not move runtime attribution away from the last completed R2 run.

## Remaining deferred independent scopes

- Full-normal S1.42AI BCMER ShyGuy acceptance after the diagnostic path is resolved; the diagnostic path cannot replace it.
- LC Office V81 integration under `BuildSpecs/DEFERRED_LC_OFFICE_V81_PLAN.md`.
- CullFactory exceptions for exact IDs `junkrooms` / `shatteredrooms`.
- MelanieMausoleum fog reduction only for that interior.
- Black Mesa/interior/Pikmin route recovery.
- Isolated `woah25-LethalEscapeUpdated 2.5.0` evaluation.
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

## Latest built artifact: S1.42AI-DIAG1R3

Artifact: `{R3_PROFILE}`  
SHA-256: `{R3_SHA}`  
Build request: `{R3_REQUEST}`  
Readable snapshot: `ProfileSources/S1.42AI-DIAG1R3/`  
FILE_INDEX: `ProfileSources/S1.42AI-DIAG1R3/FILE_INDEX.json`  
Build workflow run: `{R3_BUILD_RUN}`  
Build commit: `{R3_BUILD_COMMIT}`  
Plugin DLL SHA-256: `{R3_PLUGIN_SHA}`  
Canonical materialized validation: `{R3_VALIDATION_MD}` / `{R3_VALIDATION}`  
Materialized EndlessElevator applicability: `{R3_APPLICABILITY}`  
Validation workflow run: `{R3_VALIDATION_RUN}`

R3 is built and verified but has **no runtime decision yet** and is **not an active candidate yet**. The machine index continues to classify runtime-decided profiles and runtime-pending candidates; R3 enters `pending_profiles` only in the later coordinated activation transition. Exact R3 artifact/snapshot/materialized evidence is already repository-readable.

## Completed failed diagnostic predecessor: S1.42AI-DIAG1R2

R2 remains preserved as completed failed diagnostic evidence under `{R2_FAILURE}`, `ProfileSources/S1.42AI-DIAG1R2/`, and `{R2_RUNTIME}`.

## Earlier failed diagnostics

S1.42AI-DIAG1 and S1.42AI-DIAG1R1 remain preserved as completed failed diagnostic evidence and must not be rerun unchanged.

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
