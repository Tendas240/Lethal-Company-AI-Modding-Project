#!/usr/bin/env python3
"""Validate the repository knowledge architecture and atomic current-state invariants.

Standard-library only so GitHub Actions can run it on every relevant change.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def exists(path: str) -> bool:
    clean = path.rstrip("/")
    if not clean:
        return False
    if "*" in clean:
        return bool(list(ROOT.glob(clean)))
    return (ROOT / clean).exists()


def load_json(path: str) -> Any:
    p = ROOT / path
    if not p.is_file():
        fail(f"missing JSON: {path}")
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path}: {exc}")
        return {}


def require_path(path: str, context: str) -> None:
    if not exists(path):
        fail(f"missing path referenced by {context}: {path}")


def validate_required_artifacts(req: dict[str, Any]) -> None:
    explicit = [
        "OVERHAUL_START_HERE_ChatGPT.txt",
        "Current/104_REPOSITORY_OVERHAUL_INFORMATION_ARCHITECTURE_PLAN.md",
        "Current/105_REPOSITORY_OVERHAUL_EXECUTION_PLAYBOOK.md",
        "Current/PRE_OVERHAUL_BACKUP_MANIFEST.json",
        "Current/PROJECT_KNOWLEDGE_MAP.md",
        "Current/PROJECT_KNOWLEDGE_MAP.json",
        "Current/BUILD_LINEAGE.md",
        "Current/BUILD_LINEAGE.json",
        "Current/CURRENT_STATE.json",
        "Current/DOCUMENT_AUTHORITY.md",
        "Current/DOCUMENT_AUTHORITY.json",
        "Current/REPOSITORY_MIGRATION_MANIFEST.md",
        "Current/REPOSITORY_MIGRATION_MANIFEST.json",
        "RepositoryTools/knowledge_architecture_validator.py",
        "RepositoryTools/answerability_cases.json",
        "RepositoryTools/answerability_regression.py",
        ".github/workflows/knowledge-architecture.yml",
    ]
    for path in explicit:
        require_path(path, "required artifact set")


def validate_backup(req: dict[str, Any]) -> None:
    manifest = load_json("Current/PRE_OVERHAUL_BACKUP_MANIFEST.json")
    required = req.get("pre_overhaul_backup_gate", {}).get("manifest_required_fields", [])
    for key in required:
        if key not in manifest:
            fail(f"backup manifest missing field: {key}")
    result = str(manifest.get("verification_result", "")).upper()
    if "PASS" not in result:
        fail(f"backup verification is not PASS: {result!r}")
    if manifest.get("frozen_source_commit_sha") != "5dbd0e637a480d8591773e422bbca4b0654cad20":
        fail("backup manifest frozen source commit drift")


def validate_knowledge_map(req: dict[str, Any]) -> None:
    km = load_json("Current/PROJECT_KNOWLEDGE_MAP.json")
    topics = km.get("topics", [])
    ids = [t.get("id") for t in topics]
    if len(ids) != len(set(ids)):
        fail("knowledge-map topic ids are not unique")

    mandatory = set(req.get("mandatory_topics", []))
    missing = sorted(mandatory - set(ids))
    if missing:
        fail("mandatory topics missing from knowledge map: " + ", ".join(missing))

    topic_ids = set(ids)
    canonical_paths: set[str] = set()
    for topic in topics:
        tid = topic.get("id", "<missing-id>")
        canonical = topic.get("canonical")
        if not canonical:
            fail(f"topic {tid} has no canonical target")
        else:
            require_path(canonical, f"topic {tid}.canonical")
            canonical_paths.add(canonical)

        for field in ("machine_state", "evidence", "config_paths", "code_paths", "historical_sources"):
            for path in topic.get(field, []):
                require_path(path, f"topic {tid}.{field}")
        for related in topic.get("related_topics", []):
            if related not in topic_ids:
                fail(f"topic {tid} links unknown related topic: {related}")

    for p in sorted((ROOT / "Knowledge").glob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        if rel not in canonical_paths:
            fail(f"orphan Knowledge canonical document: {rel}")

    bootstrap = km.get("bootstrap", [])
    if len(bootstrap) > 5:
        fail(f"knowledge-map bootstrap fanout too large: {len(bootstrap)}")
    for path in bootstrap:
        require_path(path, "knowledge-map bootstrap")


def validate_current_state() -> None:
    state = load_json("Current/CURRENT_STATE.json")
    buildspec = load_json("BuildSpecs/current.json")
    lineage = load_json("Current/BUILD_LINEAGE.json")
    auto = load_json("Current/AUTO_BUILD_RESULT.json")

    accepted = state.get("accepted_baseline", {})
    latest = state.get("latest_built_artifact", {})
    candidate = state.get("active_candidate")
    controllers = state.get("controllers", {})

    # The accepted baseline remains a deliberately frozen gameplay authority until
    # an explicit later runtime decision promotes a successor.
    if accepted.get("build_id") != "S1.42AC":
        fail("atomic state accepted baseline is not S1.42AC")
    if accepted.get("sha256") != "0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9":
        fail("atomic state S1.42AC SHA drift")
    if accepted.get("status") != "ACCEPTED_FULL_NORMAL_STACK":
        fail("atomic state S1.42AC is not accepted full normal stack")

    active_build_path = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
    if not active_build_path.is_file():
        fail("RuntimeInbox/ACTIVE_BUILD.txt missing")
        active_build = ""
    else:
        active_build = active_build_path.read_text(encoding="utf-8").strip()

    lineage_builds = [b for b in lineage.get("builds", []) if isinstance(b, dict)]
    lineage_by_id = {b.get("id"): b for b in lineage_builds if b.get("id")}
    lineage_ids = set(lineage_by_id)

    if active_build and active_build not in lineage_ids:
        fail(f"ACTIVE_BUILD references unknown build lineage id: {active_build!r}")
    if controllers.get("runtime_active_build") != active_build:
        fail("CURRENT_STATE controller runtime_active_build mismatch")

    candidate_id = candidate.get("build_id") if isinstance(candidate, dict) else None
    if candidate_id:
        if state.get("runtime_test_outstanding") is not True:
            fail("active candidate requires runtime_test_outstanding=true")
        if latest.get("build_id") != candidate_id:
            fail("active candidate must be the latest built artifact")
        if active_build != candidate_id:
            fail("ACTIVE_BUILD must identify the active runtime candidate")
        if lineage.get("active_candidate_build_id") != candidate_id:
            fail("BUILD_LINEAGE active candidate mismatch")
        if candidate_id not in lineage_ids:
            fail("active candidate is missing from BUILD_LINEAGE")
        if candidate.get("profile") != latest.get("profile") or candidate.get("sha256") != latest.get("sha256"):
            fail("active candidate identity disagrees with latest built artifact")
    else:
        if state.get("runtime_test_outstanding") is not False:
            fail("runtime_test_outstanding must be false when no active candidate exists")
        if lineage.get("active_candidate_build_id") is not None:
            fail("BUILD_LINEAGE active candidate must be null when CURRENT_STATE has none")

    # The current build controller must be disabled between atomic build operations.
    # Its guard may point at the active candidate while runtime validation is open;
    # otherwise it guards the accepted baseline.
    if buildspec.get("enabled") is not False:
        fail("BuildSpecs/current.json must remain disabled outside an atomic build operation")
    guard = candidate if candidate_id else accepted
    if buildspec.get("base_profile") != guard.get("profile"):
        fail("BuildSpecs base_profile does not match the current guarded artifact")
    if buildspec.get("base_sha256") != guard.get("sha256"):
        fail("BuildSpecs base_sha256 does not match the current guarded artifact")
    if controllers.get("build_id") != buildspec.get("build_id"):
        fail("CURRENT_STATE controller build_id mismatch")
    if controllers.get("build_enabled") != buildspec.get("enabled"):
        fail("CURRENT_STATE controller build_enabled mismatch")
    if controllers.get("build_base_profile") != buildspec.get("base_profile"):
        fail("CURRENT_STATE controller build_base_profile mismatch")
    if controllers.get("build_base_sha256") != buildspec.get("base_sha256"):
        fail("CURRENT_STATE controller build_base_sha256 mismatch")

    if lineage.get("current_accepted_build_id") != accepted.get("build_id"):
        fail("BUILD_LINEAGE current accepted build mismatch")
    if lineage.get("latest_built_artifact_id") != latest.get("build_id"):
        fail("BUILD_LINEAGE latest built artifact mismatch")

    accepted_lineage = lineage_by_id.get(accepted.get("build_id"), {})
    if accepted_lineage.get("sha256") != accepted.get("sha256"):
        fail("accepted CURRENT_STATE SHA disagrees with BUILD_LINEAGE")
    if accepted_lineage.get("decision_record") != accepted.get("acceptance"):
        fail("accepted CURRENT_STATE acceptance disagrees with BUILD_LINEAGE decision record")
    if accepted_lineage.get("safe_as_gameplay_base") is not True:
        fail("accepted BUILD_LINEAGE entry is not marked safe_as_gameplay_base")

    # AUTO_BUILD_RESULT is immutable provenance for the latest actual profile build.
    if auto.get("build_id") != latest.get("build_id"):
        fail("AUTO_BUILD_RESULT does not describe latest built artifact")
    if auto.get("output_sha256") != latest.get("sha256"):
        fail("AUTO_BUILD_RESULT latest artifact SHA mismatch")
    latest_lineage = lineage_by_id.get(latest.get("build_id"), {})
    parent_id = latest_lineage.get("parent")
    parent = lineage_by_id.get(parent_id, {}) if parent_id else {}
    if parent_id and auto.get("base_sha256") != parent.get("sha256"):
        fail("AUTO_BUILD_RESULT base SHA disagrees with latest artifact lineage parent")

    for key in ("profile", "acceptance", "project_status", "runtime_evidence", "profile_sources", "file_index"):
        value = accepted.get(key)
        if value:
            require_path(value, f"CURRENT_STATE.accepted_baseline.{key}")
    for key in ("profile", "acceptance", "candidate_record", "project_status", "original_rejection", "corrected_analysis", "runtime_evidence", "profile_sources", "file_index", "build_plan"):
        value = latest.get(key)
        if value:
            require_path(value, f"CURRENT_STATE.latest_built_artifact.{key}")
    if isinstance(candidate, dict):
        for key in ("profile", "candidate_record", "project_status", "runtime_evidence"):
            value = candidate.get(key)
            if value:
                require_path(value, f"CURRENT_STATE.active_candidate.{key}")


def validate_profile_sources() -> None:
    for build in ("S1.42AB", "S1.42AC", "S1.42AD"):
        require_path(f"ProfileSources/{build}/FILE_INDEX.json", f"{build} readable snapshot")
        require_path(f"ProfileSources/{build}/export.r2x", f"{build} readable snapshot")


def runtime_log_sha256_from_index(path: str, context: str) -> str | None:
    data = load_json(path)
    files = [entry for entry in data.get("files", []) if entry.get("name") == "LogOutput.log"]
    if len(files) != 1:
        fail(f"{context}: expected exactly one LogOutput.log entry in {path}, found {len(files)}")
        return None
    sha = files[0].get("sha256")
    if not sha:
        fail(f"{context}: LogOutput.log entry has no sha256 in {path}")
        return None

    for analysis in data.get("analysis", []):
        stats = analysis.get("stats", {})
        source_sha = stats.get("source_sha256")
        if source_sha and source_sha != sha:
            fail(f"{context}: runtime INDEX file sha256 {sha} disagrees with embedded analysis source_sha256 {source_sha}")
    return sha


def validate_runtime_evidence_provenance() -> None:
    integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
    runtime_by_build: dict[str, str] = {}

    for profile in integrity.get("profiles", []):
        build_id = profile.get("build_id", "<missing-build-id>")
        index_path = profile.get("runtime_index")
        declared_sha = profile.get("runtime_log_sha256")
        if not index_path:
            fail(f"artifact evidence {build_id} has no runtime_index")
            continue
        require_path(index_path, f"artifact evidence {build_id}.runtime_index")
        actual_sha = runtime_log_sha256_from_index(index_path, f"artifact evidence {build_id}")
        if actual_sha is None:
            continue
        runtime_by_build[str(build_id)] = actual_sha
        if declared_sha != actual_sha:
            fail(f"artifact evidence {build_id} runtime_log_sha256 mismatch: {declared_sha!r} != {actual_sha!r}")

    # Preserve and validate the original rejected-state provenance independently of
    # the later explicit acceptance. The current artifact index intentionally points
    # S1.42AC at the fresh acceptance run, so resolve rejection-era bytes directly.
    status = load_json("Current/Projektstatus_S1.42AC_REJECTED.json")
    historical_accepted = status.get("accepted_baseline", {})
    rejected = status.get("rejected_candidate", {})

    ab_sha = runtime_by_build.get("S1.42AB")
    if ab_sha and historical_accepted.get("raw_log_sha256") != ab_sha:
        fail("S1.42AB historical project-status raw_log_sha256 disagrees with authoritative RuntimeEvidence INDEX")

    old_index = "RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json"
    require_path(old_index, "S1.42AC historical rejection runtime index")
    old_ac_sha = runtime_log_sha256_from_index(old_index, "S1.42AC historical rejection")
    if not old_ac_sha:
        fail("S1.42AC historical authoritative runtime-log SHA could not be resolved")
        return
    if rejected.get("raw_log_sha256") != old_ac_sha:
        fail("S1.42AC historical rejected project-status raw_log_sha256 disagrees with rejection-era RuntimeEvidence INDEX")

    provenance = rejected.get("raw_log_sha256_provenance", {})
    if provenance.get("authority") != old_index:
        fail("S1.42AC raw-log provenance authority does not point to the canonical historical RuntimeEvidence INDEX")
    if provenance.get("authoritative_sha256") != old_ac_sha:
        fail("S1.42AC historical provenance authoritative_sha256 disagrees with RuntimeEvidence INDEX")
    superseded = provenance.get("superseded_recorded_sha256")
    if not superseded or superseded == old_ac_sha:
        fail("S1.42AC provenance must retain a distinct superseded historical SHA-256 value")

    rejection_path = ROOT / "Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md"
    if not rejection_path.is_file():
        fail("missing S1.42AC rejection record for provenance erratum validation")
        return
    rejection_text = rejection_path.read_text(encoding="utf-8", errors="replace")
    lowered = rejection_text.lower()
    if old_ac_sha not in rejection_text:
        fail("S1.42AC rejection record does not contain authoritative rejection-era raw-log SHA-256")
    if str(superseded) not in rejection_text:
        fail("S1.42AC rejection record does not preserve the superseded historical SHA-256")
    if "provenance erratum" not in lowered or "supersed" not in lowered:
        fail("S1.42AC rejection record lacks an explicit provenance erratum/supersession marker")

    accepted_status = load_json("Current/Projektstatus_S1.42AC_ACCEPTED.json")
    accepted_runtime = accepted_status.get("runtime_acceptance", {})
    fresh_index = "RuntimeEvidence/S1.42AC/20260904T235720Z/INDEX.json"
    require_path(fresh_index, "S1.42AC corrected acceptance runtime index")
    fresh_sha = runtime_log_sha256_from_index(fresh_index, "S1.42AC corrected acceptance")
    if fresh_sha and accepted_runtime.get("raw_log_sha256") != fresh_sha:
        fail("S1.42AC accepted project-status raw_log_sha256 disagrees with fresh RuntimeEvidence INDEX")
    if fresh_sha and runtime_by_build.get("S1.42AC") != fresh_sha:
        fail("Current artifact evidence index does not point S1.42AC at the fresh accepted runtime bytes")
    if accepted_runtime.get("static_equal_eventtype_probability_gate") is not True:
        fail("S1.42AC accepted project status does not assert the corrected static EventType probability gate")


def validate_lineage() -> None:
    data = load_json("Current/BUILD_LINEAGE.json")
    builds = data.get("builds", [])
    ids = {b.get("id") for b in builds}
    if None in ids:
        fail("BUILD_LINEAGE contains build with missing id")
    for b in builds:
        bid = b.get("id")
        for field in ("parent", "supersedes", "superseded_by"):
            target = b.get(field)
            if target and target not in ids:
                fail(f"BUILD_LINEAGE {bid}.{field} points to unknown build {target}")
        for field in ("profile", "build_plan", "candidate_record", "decision_record", "runtime_evidence", "historical_rejection", "historical_runtime_evidence", "post_decision_analysis"):
            path = b.get(field)
            if path:
                require_path(path, f"BUILD_LINEAGE {bid}.{field}")


def validate_authority_and_migration() -> None:
    auth = load_json("Current/DOCUMENT_AUTHORITY.json")
    historical = {x.get("path") for x in auth.get("historical_or_superseded", [])}
    for required in ("Current/02_TECHNICAL_BASELINE.md", "Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md"):
        if required not in historical:
            fail(f"known stale-current document not explicitly classified: {required}")

    migration = load_json("Current/REPOSITORY_MIGRATION_MANIFEST.json")
    for entry in migration.get("redirects_and_supersessions", []):
        require_path(entry.get("legacy", ""), "migration legacy path")
        for target in entry.get("current_targets", []):
            require_path(target, f"migration target for {entry.get('legacy')}")
    if migration.get("deleted_paths"):
        warn("migration manifest contains deletions; ensure unique-fact audit is documented")


def validate_bootstrap() -> None:
    required_routes = [
        "Current/00_CURRENT_STATE.md",
        "Current/PROJECT_KNOWLEDGE_MAP.md",
        "Current/CURRENT_STATE.json",
    ]
    for path in ("README.md", "START_HERE_ChatGPT_Masterprompt.txt", "Current/01_HANDOVER_CORE.md"):
        require_path(path, "bootstrap")
        text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
        for route in required_routes[:2]:
            if route not in text:
                fail(f"bootstrap {path} does not route to {route}")
        if "overhaul" in path.lower() and "not executed" in text.lower():
            fail(f"canonical bootstrap still says overhaul not executed: {path}")
    start_lines = (ROOT / "START_HERE_ChatGPT_Masterprompt.txt").read_text(encoding="utf-8").splitlines()
    if len(start_lines) > 180:
        fail(f"START_HERE is not compact routing bootstrap ({len(start_lines)} lines > 180)")


def validate_overhaul_completion_metadata() -> None:
    req = load_json("Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json")
    status = str(req.get("status", "")).upper()
    if "VALIDATED" not in status or not any(token in status for token in ("EXECUTED", "COMPLETE", "IMPLEMENTED")):
        fail(f"requirements status does not declare completed execution: {req.get('status')!r}")
    execution = load_json("Current/OVERHAUL_EXECUTION_STATE.json")
    if execution.get("last_completed_phase") != 11:
        fail("OVERHAUL_EXECUTION_STATE last_completed_phase is not 11")
    if str(execution.get("status", "")).upper() not in {"COMPLETE_VALIDATED", "OVERHAUL_COMPLETE_VALIDATED"}:
        fail("OVERHAUL_EXECUTION_STATE status is not complete/validated")


def main() -> int:
    req = load_json("Current/REPOSITORY_KNOWLEDGE_ARCHITECTURE_REQUIREMENTS.json")
    validate_required_artifacts(req)
    validate_backup(req)
    validate_knowledge_map(req)
    validate_current_state()
    validate_profile_sources()
    validate_runtime_evidence_provenance()
    validate_lineage()
    validate_authority_and_migration()
    validate_bootstrap()
    validate_overhaul_completion_metadata()
    print("Repository knowledge architecture validation")
    print(f"errors={len(ERRORS)} warnings={len(WARNINGS)}")
    for message in WARNINGS:
        print(f"WARNING: {message}")
    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
