#!/usr/bin/env python3
"""Recompute current critical profile/runtime SHA-256 values from repository bytes.

Completed profile decisions live under `profiles`. Runtime-pending candidates live under
`pending_profiles`: their profile bytes and readable snapshot are mandatory before runtime.
A pending candidate may also carry indexed partial runtime evidence before its final explicit
acceptance/rejection decision; when present, those runtime bytes are verified here as well.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTEGRITY_PATH = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.json"
PENDING_ROLE = "ACTIVE_RUNTIME_CANDIDATE_PENDING"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require_readable_profile_artifacts(entry: dict[str, Any], build_id: str, errors: list[str]) -> None:
    sources_rel = entry.get("profile_sources")
    if not sources_rel or not (ROOT / str(sources_rel)).is_dir():
        errors.append(f"{build_id}: readable profile snapshot missing: {sources_rel}")

    file_index_rel = entry.get("file_index")
    if not file_index_rel or not (ROOT / str(file_index_rel)).is_file():
        errors.append(f"{build_id}: readable FILE_INDEX missing: {file_index_rel}")

    export_rel = entry.get("export")
    if export_rel and not (ROOT / str(export_rel)).is_file():
        errors.append(f"{build_id}: readable export missing: {export_rel}")

    for field in ("candidate_record", "project_status", "acceptance", "rejection", "build_plan", "runtime_partial_record"):
        rel = entry.get(field)
        if rel and not (ROOT / str(rel)).exists():
            errors.append(f"{build_id}: referenced {field} missing: {rel}")


def verify_profile(entry: dict[str, Any], errors: list[str]) -> bool:
    build_id = str(entry.get("build_id", "<missing-build-id>"))
    profile_rel = entry.get("profile")
    expected_profile_sha = entry.get("profile_sha256")
    if not profile_rel or not expected_profile_sha:
        errors.append(f"{build_id}: profile path/SHA missing from artifact evidence index")
        return False
    profile_path = ROOT / str(profile_rel)
    if not profile_path.is_file():
        errors.append(f"{build_id}: profile bytes missing: {profile_rel}")
        return False
    actual = sha256_file(profile_path)
    if actual != str(expected_profile_sha).lower():
        errors.append(f"{build_id}: profile byte SHA mismatch: {actual} != {expected_profile_sha}")
        return False
    require_readable_profile_artifacts(entry, build_id, errors)
    return True


def verify_runtime(entry: dict[str, Any], errors: list[str]) -> bool:
    build_id = str(entry.get("build_id", "<missing-build-id>"))
    index_rel = entry.get("runtime_index")
    expected_log_sha = entry.get("runtime_log_sha256")
    if not index_rel or not expected_log_sha:
        errors.append(f"{build_id}: runtime index/log SHA missing from artifact evidence entry")
        return False

    index_path = ROOT / str(index_rel)
    if not index_path.is_file():
        errors.append(f"{build_id}: runtime index missing: {index_rel}")
        return False

    index = load_json(index_path)
    log_entries = [x for x in index.get("files", []) if x.get("name") == "LogOutput.log"]
    if len(log_entries) != 1:
        errors.append(f"{build_id}: expected exactly one LogOutput.log in {index_rel}")
        return False

    indexed_sha = log_entries[0].get("sha256")
    if indexed_sha != expected_log_sha:
        errors.append(f"{build_id}: artifact index/runtime INDEX SHA mismatch: {expected_log_sha} != {indexed_sha}")

    sources = [a.get("source") for a in index.get("analysis", []) if a.get("source")]
    log_source = next((s for s in sources if str(s).endswith("/raw/LogOutput.log")), None)
    if log_source is None:
        log_source = (Path(str(index_rel)).parent / "raw" / "LogOutput.log").as_posix()
    log_path = ROOT / str(log_source)
    if not log_path.is_file():
        errors.append(f"{build_id}: raw runtime log bytes missing: {log_source}")
        return False

    actual_log_sha = sha256_file(log_path)
    if actual_log_sha != expected_log_sha:
        errors.append(f"{build_id}: raw runtime-log byte SHA mismatch: {actual_log_sha} != {expected_log_sha}")
    expected_size = log_entries[0].get("size")
    if isinstance(expected_size, int) and log_path.stat().st_size != expected_size:
        errors.append(f"{build_id}: raw runtime-log byte size mismatch: {log_path.stat().st_size} != {expected_size}")
    for analysis in index.get("analysis", []):
        source_sha = analysis.get("stats", {}).get("source_sha256")
        if source_sha and source_sha != actual_log_sha:
            errors.append(f"{build_id}: embedded analysis source_sha256 disagrees with raw bytes")
    return True


def main() -> int:
    errors: list[str] = []
    if not INTEGRITY_PATH.is_file():
        print("ERROR: missing Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
        return 1

    integrity = load_json(INTEGRITY_PATH)
    completed = [x for x in integrity.get("profiles", []) if isinstance(x, dict)]
    pending = [x for x in integrity.get("pending_profiles", []) if isinstance(x, dict)]
    completed_profiles_checked = 0
    completed_logs_checked = 0
    pending_profiles_checked = 0
    pending_partial_logs_checked = 0

    for entry in completed:
        if verify_profile(entry, errors):
            completed_profiles_checked += 1
        if verify_runtime(entry, errors):
            completed_logs_checked += 1

    for entry in pending:
        build_id = str(entry.get("build_id", "<missing-build-id>"))
        if entry.get("role") != PENDING_ROLE:
            errors.append(f"{build_id}: pending_profiles entry must use role {PENDING_ROLE}")
        if entry.get("runtime_evidence_required") is not False:
            errors.append(f"{build_id}: pending candidate must explicitly set runtime_evidence_required=false until final runtime decision")

        index_present = bool(entry.get("runtime_index"))
        sha_present = bool(entry.get("runtime_log_sha256"))
        partial_declared = entry.get("partial_runtime_evidence_present") is True
        if index_present != sha_present:
            errors.append(f"{build_id}: pending partial runtime evidence must declare both runtime_index and runtime_log_sha256")
        elif index_present:
            if not partial_declared:
                errors.append(f"{build_id}: pending runtime evidence requires partial_runtime_evidence_present=true")
            if verify_runtime(entry, errors):
                pending_partial_logs_checked += 1
        elif partial_declared:
            errors.append(f"{build_id}: partial_runtime_evidence_present=true but runtime_index/runtime_log_sha256 are missing")

        if verify_profile(entry, errors):
            pending_profiles_checked += 1

    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print(
        "PASS: actual bytes verified for "
        f"{completed_profiles_checked} completed profiles/{completed_logs_checked} completed runtime logs, "
        f"{pending_profiles_checked} pending runtime candidate profile(s), and "
        f"{pending_partial_logs_checked} pending partial runtime log(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
