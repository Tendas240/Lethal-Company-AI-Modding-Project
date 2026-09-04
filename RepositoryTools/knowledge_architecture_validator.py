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
    # Directory references in project metadata conventionally end with '/'.
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
                # Evidence glob descriptions such as Current/Projektstatus_*.json are allowed.
                require_path(path, f"topic {tid}.{field}")
        for related in topic.get("related_topics", []):
            if related not in topic_ids:
                fail(f"topic {tid} links unknown related topic: {related}")

    # Every semantic Knowledge document should be routable from the map.
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
    controllers = state.get("controllers", {})

    if accepted.get("build_id") != "S1.42AB":
        fail("atomic state accepted baseline is not S1.42AB")
    if accepted.get("sha256") != "3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca":
        fail("atomic state S1.42AB SHA drift")
    if latest.get("build_id") != "S1.42AC":
        fail("atomic state latest built artifact is not S1.42AC")
    if state.get("active_candidate") is not None:
        fail("active candidate must be null while no successor is armed")
    if state.get("runtime_test_outstanding") is not False:
        fail("runtime_test_outstanding must be false")

    active_build_path = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
    if not active_build_path.is_file():
        fail("RuntimeInbox/ACTIVE_BUILD.txt missing")
        active_build = ""
    else:
        active_build = active_build_path.read_text(encoding="utf-8").strip()
    if active_build != accepted.get("build_id"):
        fail(f"ACTIVE_BUILD mismatch: {active_build!r} != {accepted.get('build_id')!r}")
    if controllers.get("runtime_active_build") != active_build:
        fail("CURRENT_STATE controller runtime_active_build mismatch")

    if buildspec.get("enabled") is not False:
        fail("BuildSpecs/current.json must remain disabled")
    if buildspec.get("base_profile") != accepted.get("profile"):
        fail("BuildSpecs base_profile does not match accepted baseline")
    if buildspec.get("base_sha256") != accepted.get("sha256"):
        fail("BuildSpecs base_sha256 does not match accepted baseline")
    if controllers.get("build_id") != buildspec.get("build_id"):
        fail("CURRENT_STATE controller build_id mismatch")
    if controllers.get("build_enabled") != buildspec.get("enabled"):
        fail("CURRENT_STATE controller build_enabled mismatch")

    if lineage.get("current_accepted_build_id") != accepted.get("build_id"):
        fail("BUILD_LINEAGE current accepted build mismatch")
    if lineage.get("active_candidate_build_id") is not None:
        fail("BUILD_LINEAGE active candidate must be null")
    if lineage.get("latest_built_artifact_id") != latest.get("build_id"):
        fail("BUILD_LINEAGE latest built artifact mismatch")

    # AUTO_BUILD_RESULT is historical latest-build output, not the active controller.
    if auto.get("build_id") != latest.get("build_id"):
        fail("AUTO_BUILD_RESULT does not describe latest built artifact")
    if auto.get("output_sha256") != latest.get("sha256"):
        fail("AUTO_BUILD_RESULT latest artifact SHA mismatch")
    if auto.get("base_sha256") != accepted.get("sha256"):
        fail("AUTO_BUILD_RESULT base SHA no longer matches accepted baseline lineage")

    for key in ("profile", "acceptance", "project_status", "runtime_evidence", "profile_sources", "file_index"):
        if key in accepted:
            require_path(accepted[key], f"CURRENT_STATE.accepted_baseline.{key}")
    for key in ("profile", "project_status", "original_rejection", "corrected_analysis", "runtime_evidence", "profile_sources", "file_index"):
        if key in latest:
            require_path(latest[key], f"CURRENT_STATE.latest_built_artifact.{key}")


def validate_profile_sources() -> None:
    for build in ("S1.42AB", "S1.42AC"):
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

    status = load_json("Current/Projektstatus_S1.42AC_REJECTED.json")
    accepted = status.get("accepted_baseline", {})
    rejected = status.get("rejected_candidate", {})

    ab_sha = runtime_by_build.get("S1.42AB")
    if ab_sha and accepted.get("raw_log_sha256") != ab_sha:
        fail("S1.42AB project-status raw_log_sha256 disagrees with authoritative RuntimeEvidence INDEX")

    ac_sha = runtime_by_build.get("S1.42AC")
    if not ac_sha:
        fail("S1.42AC authoritative runtime-log SHA could not be resolved from artifact evidence")
        return
    if rejected.get("raw_log_sha256") != ac_sha:
        fail("S1.42AC project-status raw_log_sha256 disagrees with authoritative RuntimeEvidence INDEX")

    provenance = rejected.get("raw_log_sha256_provenance", {})
    expected_index = "RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json"
    if provenance.get("authority") != expected_index:
        fail("S1.42AC raw-log provenance authority does not point to the canonical RuntimeEvidence INDEX")
    if provenance.get("authoritative_sha256") != ac_sha:
        fail("S1.42AC provenance authoritative_sha256 disagrees with RuntimeEvidence INDEX")
    superseded = provenance.get("superseded_recorded_sha256")
    if not superseded or superseded == ac_sha:
        fail("S1.42AC provenance must retain a distinct superseded historical SHA-256 value")

    rejection_path = ROOT / "Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md"
    if not rejection_path.is_file():
        fail("missing S1.42AC rejection record for provenance erratum validation")
        return
    rejection_text = rejection_path.read_text(encoding="utf-8", errors="replace")
    lowered = rejection_text.lower()
    if ac_sha not in rejection_text:
        fail("S1.42AC rejection record does not contain authoritative raw-log SHA-256")
    if str(superseded) not in rejection_text:
        fail("S1.42AC rejection record does not preserve the superseded historical SHA-256")
    if "provenance erratum" not in lowered or "supersed" not in lowered:
        fail("S1.42AC rejection record lacks an explicit provenance erratum/supersession marker")


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
        for field in ("profile", "build_plan", "candidate_record", "decision_record", "runtime_evidence"):
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
