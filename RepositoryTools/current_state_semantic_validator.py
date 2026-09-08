#!/usr/bin/env python3
"""Validate semantic agreement of current/live authorities with CURRENT_STATE.

This gate prevents a green repository from routing a new ChatGPT session into stale
pre-candidate or pre-runtime instructions. Historical evidence is intentionally excluded.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LIVE_DOCS = (
    "Knowledge/CURRENT_LIFECYCLE.md",
    "Current/PROJECT_KNOWLEDGE_MAP.md",
    "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md",
    "Current/04_OPEN_ISSUES_AND_NEXT_TESTS.md",
    "Current/ARTIFACT_EVIDENCE_INTEGRITY.md",
)
STALE_RUNTIME_PENDING_PHRASES = (
    "no runtime test is currently pending",
    "no runtime test is pending",
    "there is no active runtime candidate",
    "do not start a runtime test before a later candidate is built",
    "do not start a runtime test until a later successor candidate is actually built",
    "successor not armed / no build yet",
    "perform the successor-specific patch safety review",
)


def load_json(root: Path, rel: str, errors: list[str]) -> dict[str, Any]:
    path = root / rel
    if not path.is_file():
        errors.append(f"missing JSON: {rel}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {rel}: {exc}")
        return {}


def read_text(root: Path, rel: str, errors: list[str]) -> str:
    path = root / rel
    if not path.is_file():
        errors.append(f"missing live authority: {rel}")
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def expected_marker(state: dict[str, Any]) -> str:
    accepted = str(state.get("accepted_baseline", {}).get("build_id", "none"))
    latest = str(state.get("latest_built_artifact", {}).get("build_id", "none"))
    candidate = state.get("active_candidate")
    candidate_id = str(candidate.get("build_id")) if isinstance(candidate, dict) and candidate.get("build_id") else "none"
    pending = "true" if state.get("runtime_test_outstanding") is True else "false"
    return f"<!-- LIVE_STATE: accepted={accepted} latest={latest} candidate={candidate_id} runtime_test_outstanding={pending} -->"


def validate_live_state(root: Path) -> list[str]:
    errors: list[str] = []
    state = load_json(root, "Current/CURRENT_STATE.json", errors)
    km = load_json(root, "Current/PROJECT_KNOWLEDGE_MAP.json", errors)
    integrity = load_json(root, "Current/ARTIFACT_EVIDENCE_INTEGRITY.json", errors)

    accepted = state.get("accepted_baseline", {})
    latest = state.get("latest_built_artifact", {})
    candidate = state.get("active_candidate")
    accepted_id = str(accepted.get("build_id", ""))
    latest_id = str(latest.get("build_id", ""))
    candidate_id = str(candidate.get("build_id", "")) if isinstance(candidate, dict) else ""
    runtime_pending = state.get("runtime_test_outstanding") is True

    if not accepted_id or not latest_id:
        errors.append("CURRENT_STATE must declare accepted and latest build ids")
        return errors

    marker = expected_marker(state)
    for rel in LIVE_DOCS:
        text = read_text(root, rel, errors)
        lowered = text.lower()
        if text and marker not in text[:500]:
            errors.append(f"{rel}: live-state marker mismatch; expected {marker}")
        if accepted_id and accepted_id not in text:
            errors.append(f"{rel}: accepted build {accepted_id} absent from live authority")
        if latest_id and latest_id not in text:
            errors.append(f"{rel}: latest build {latest_id} absent from live authority")
        if runtime_pending and candidate_id:
            if candidate_id not in text:
                errors.append(f"{rel}: active candidate {candidate_id} absent from live authority")
            for phrase in STALE_RUNTIME_PENDING_PHRASES:
                if phrase in lowered:
                    errors.append(f"{rel}: stale runtime-pending contradiction: {phrase!r}")
            if latest_id.casefold() != "s1.42ag" and re.search(r"latest built artifact[^\n]*s1\.42ag", lowered):
                errors.append(f"{rel}: still declares S1.42AG as latest built artifact")

    selected = state.get("selected_scope", {})
    if runtime_pending and candidate_id:
        if selected.get("candidate_build_id") != candidate_id:
            errors.append("CURRENT_STATE.selected_scope candidate_build_id disagrees with active candidate")
        analysis_contract = str(selected.get("analysis_contract", ""))
        if candidate_id not in analysis_contract:
            errors.append("CURRENT_STATE.selected_scope analysis_contract does not name the active candidate")
        if re.search(r"\bimplement\b.*\bsuccessor\b", analysis_contract, re.I):
            errors.append("CURRENT_STATE.selected_scope analysis_contract still asks to implement an already-built successor")
        irrelevant = "\n".join(str(x) for x in selected.get("currently_irrelevant_actions", []))
        if "later successor candidate is actually built" in irrelevant.lower():
            errors.append("CURRENT_STATE currently_irrelevant_actions still contains the pre-build runtime prohibition")

    topics = {str(t.get("id")): t for t in km.get("topics", []) if isinstance(t, dict) and t.get("id")}
    for tid, canonical in (
        ("accepted_baseline", "Knowledge/CURRENT_LIFECYCLE.md"),
        ("active_candidate_and_next_test", "Knowledge/CURRENT_LIFECYCLE.md"),
        ("pikmin_enemy_compatibility", "Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md"),
        ("roadmap_and_deferred_scopes", "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"),
    ):
        topic = topics.get(tid)
        if not topic:
            errors.append(f"knowledge map missing live topic: {tid}")
        elif topic.get("canonical") != canonical:
            errors.append(f"knowledge map topic {tid} canonical drift: {topic.get('canonical')!r}")
    active_topic = topics.get("active_candidate_and_next_test", {})
    stale_machine = [x for x in active_topic.get("machine_state", []) if "S1.42AG_REJECTED" in str(x)]
    if stale_machine:
        errors.append("active_candidate_and_next_test retains rejected S1.42AG machine-state routing")

    completed_profiles = [p for p in integrity.get("profiles", []) if isinstance(p, dict)]
    pending_profiles = [p for p in integrity.get("pending_profiles", []) if isinstance(p, dict)]
    completed_by_id = {str(p.get("build_id")): p for p in completed_profiles if p.get("build_id")}
    pending_by_id = {str(p.get("build_id")): p for p in pending_profiles if p.get("build_id")}

    accepted_entry = completed_by_id.get(accepted_id)
    if not accepted_entry:
        errors.append(f"artifact evidence completed profiles missing accepted build {accepted_id}")
    elif accepted_entry.get("profile_sha256") != accepted.get("sha256"):
        errors.append("artifact evidence accepted profile SHA disagrees with CURRENT_STATE")

    if runtime_pending and candidate_id:
        if candidate_id in completed_by_id:
            errors.append(f"active pending candidate {candidate_id} must not appear in completed profiles before runtime decision")
        pending_entry = pending_by_id.get(candidate_id)
        if not pending_entry:
            errors.append(f"artifact evidence pending_profiles missing active candidate {candidate_id}")
        else:
            if pending_entry.get("role") != "ACTIVE_RUNTIME_CANDIDATE_PENDING":
                errors.append(f"artifact evidence {candidate_id} is not marked ACTIVE_RUNTIME_CANDIDATE_PENDING")
            if pending_entry.get("runtime_evidence_required") is not False:
                errors.append(f"artifact evidence {candidate_id} must explicitly defer runtime evidence while pending")
            if pending_entry.get("profile") != candidate.get("profile") or pending_entry.get("profile_sha256") != candidate.get("sha256"):
                errors.append(f"artifact evidence {candidate_id} profile identity disagrees with CURRENT_STATE")
            canonical_sources = str(candidate.get("profile_sources", "")).rstrip("/")
            if str(pending_entry.get("profile_sources", "")).rstrip("/") != canonical_sources:
                errors.append(f"artifact evidence {candidate_id} profile_sources disagrees with CURRENT_STATE")

            fallback = Path(str(candidate.get("profile", ""))).stem.replace(" ", "_")
            fallback_rel = f"ProfileSources/{fallback}"
            if canonical_sources and fallback_rel != canonical_sources and (root / fallback_rel).exists():
                errors.append(f"duplicate filename-derived candidate snapshot exists: {fallback_rel}; canonical is {canonical_sources}")

    return errors


def main() -> int:
    errors = validate_live_state(ROOT)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("PASS: current/live authorities agree semantically with CURRENT_STATE and pending-candidate evidence")
    return 0


if __name__ == "__main__":
    sys.exit(main())
