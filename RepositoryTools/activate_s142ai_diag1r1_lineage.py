#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = "S1.42AI-DIAG1R1"
PROFILE = "Profiles/LC V1 S1.42AI-DIAG1R1 ShyGuy Isolation Repair.r2z"
PROFILE_SHA = "b83165ae27d9fa3b926c3f66701ba5c7a5db57b29f6136ab212c0fa2d2cfecdd"
CANDIDATE = "Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md"
PROJECT_STATUS = "Current/Projektstatus_S1.42AI-DIAG1R1_CANDIDATE.json"
MAT_MD = "AnalysisEvidence/S1.42AI-DIAG1R1/MATERIALIZED_VALIDATION.md"
BUILD_RUN = 34822019162
BUILD_COMMIT = "8329579d3481ab27db6407d2659ceb467eebd203"


def write_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_machine_lineage() -> None:
    path = ROOT / "Current/BUILD_LINEAGE.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["date"] = "2026-09-14"
    data["current_accepted_build_id"] = "S1.42AH"
    data["active_candidate_build_id"] = BUILD
    data["latest_built_artifact_id"] = BUILD

    builds = [b for b in data.get("builds", []) if isinstance(b, dict)]
    builds = [b for b in builds if b.get("id") != BUILD]
    builds.append(
        {
            "id": BUILD,
            "title": "ShyGuy Isolation Diagnostic Owner Type Resolution Repair",
            "status": "active-diagnostic-runtime-candidate-not-accepted",
            "parent": "S1.42AI",
            "profile": PROFILE,
            "sha256": PROFILE_SHA,
            "build_plan": "BuildSpecs/S1.42AI_PLAN.md",
            "candidate_record": CANDIDATE,
            "decision_record": CANDIDATE,
            "project_status": PROJECT_STATUS,
            "workflow_run": BUILD_RUN,
            "build_commit": BUILD_COMMIT,
            "static_evidence": MAT_MD,
            "safe_as_gameplay_base": False,
            "principal_feature": "repaired ShyGuy isolation diagnostic successor built directly from S1.42AI; derives the exact LethalMin WithdrawPikminFromOnion List<T> generic argument from CLR metadata, passed strengthened static/materialized gates, and awaits runtime validation without waiving the full-normal S1.42AI gate",
        }
    )
    data["builds"] = builds

    feature_index = data.setdefault("feature_index", {})
    feature_index["BCMER_ShyGuy_DIAG1_owner_type_resolution_repair"] = BUILD

    invariant = (
        "S1.42AI-DIAG1R1 was built directly from S1.42AI, not from the failed DIAG1 profile bytes. "
        "It repairs only the DIAG1 owner type-resolution/static-gate contract, is the active diagnostic runtime candidate, "
        "is not a safe gameplay base, and cannot waive the deferred full-normal S1.42AI runtime gate."
    )
    invariants = [str(x) for x in data.get("lineage_invariants", [])]
    if invariant not in invariants:
        invariants.append(invariant)
    data["lineage_invariants"] = invariants

    write_json(path, data)


def update_human_lineage() -> None:
    path = ROOT / "Current/BUILD_LINEAGE.md"
    text = path.read_text(encoding="utf-8")

    head_pattern = re.compile(
        r"## Current lineage head\n\n.*?\n\nFor live lifecycle state use `Knowledge/CURRENT_LIFECYCLE\.md`\.",
        re.S,
    )
    head = f"""## Current lineage head

- **Accepted gameplay baseline:** S1.42AH — Mouth Dog Pikmin Dual Prevention — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact:** {BUILD} — ShyGuy Isolation Diagnostic Owner Type Resolution Repair — **ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED**.
- **Active candidate:** {BUILD}.
- **Deferred full-normal gate:** S1.42AI — still mandatory after the R1 diagnostic decision.
- **Current action:** run the R1 diagnostic gameplay gate, then upload the fresh complete R1 `LogOutput.log` for repository-native ingestion and decision. Do not rerun failed S1.42AI-DIAG1 unchanged.

For live lifecycle state use `Knowledge/CURRENT_LIFECYCLE.md`."""
    text, count = head_pattern.subn(head, text, count=1)
    if count != 1:
        raise RuntimeError("Could not replace BUILD_LINEAGE current head exactly once")

    row = (
        f"| {BUILD} | **ACTIVE DIAGNOSTIC RUNTIME CANDIDATE / NOT ACCEPTED** | "
        "Repaired DIAG1 successor built directly from S1.42AI. Exact `WithdrawPikminFromOnion` `List<T>` owner type is metadata-derived; strengthened static and materialized equivalence gates pass; runtime evidence is now outstanding. |\n"
    )
    if row not in text:
        anchor = (
            "| S1.42AI-DIAG1 | **RUNTIME DIAGNOSTIC FAILED / REPAIR REQUIRED / NOT ACCEPTED** | "
            "Temporary exact ShyGuy isolation diagnostic built from S1.42AI. Build/static/materialized delta passed, but runtime owner prevalidation could not resolve the hardcoded `LethalMin.PikminType`, DIAG1 marked itself invalid and rolled back all of its own Harmony hooks. Repair source/static validation before any successor diagnostic test. |\n"
        )
        if anchor not in text:
            raise RuntimeError("Could not locate S1.42AI-DIAG1 human lineage row")
        text = text.replace(anchor, anchor + row, 1)

    feature_row = f"| ShyGuy isolation diagnostic owner-type resolution repair | {BUILD} / `Current/146...` |\n"
    if feature_row not in text:
        anchor = "| Mouth Dog dual Pikmin prevention with native reverse and non-Pikmin neighbor behavior preserved | S1.42AH / `Current/142...` |\n"
        if anchor not in text:
            raise RuntimeError("Could not locate human lineage feature lookup anchor")
        text = text.replace(anchor, anchor + feature_row, 1)

    parent_rule = (
        f"- {BUILD} was built **directly from S1.42AI**, not from the failed S1.42AI-DIAG1 profile bytes. "
        "It repairs only the diagnostic owner type-resolution/static-gate contract and is an active diagnostic runtime candidate, not a safe gameplay base; the deferred full-normal S1.42AI gate remains mandatory.\n"
    )
    if parent_rule not in text:
        anchor = "- S1.42AI-DIAG1 has an explicit failed diagnostic runtime decision in `Current/145...`; it must not be rerun unchanged or treated as an active runtime candidate.\n"
        if anchor not in text:
            raise RuntimeError("Could not locate S1.42AI-DIAG1 parentage-rule anchor")
        text = text.replace(anchor, anchor + parent_rule, 1)

    path.write_text(text, encoding="utf-8")


def main() -> int:
    update_machine_lineage()
    update_human_lineage()
    print("PASS: staged S1.42AI-DIAG1R1 build lineage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
