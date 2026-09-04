#!/usr/bin/env python3
"""Recompute current critical artifact/runtime SHA-256 values from repository bytes."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTEGRITY_PATH = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    if not INTEGRITY_PATH.is_file():
        print("ERROR: missing Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
        return 1

    integrity = load_json(INTEGRITY_PATH)
    checked_profiles = 0
    checked_logs = 0

    for entry in integrity.get("profiles", []):
        build_id = str(entry.get("build_id", "<missing-build-id>"))
        profile_rel = entry.get("profile")
        expected_profile_sha = entry.get("profile_sha256")
        if not profile_rel or not expected_profile_sha:
            errors.append(f"{build_id}: profile path/SHA missing from artifact evidence index")
        else:
            profile_path = ROOT / profile_rel
            if not profile_path.is_file():
                errors.append(f"{build_id}: profile bytes missing: {profile_rel}")
            else:
                actual = sha256_file(profile_path)
                checked_profiles += 1
                if actual != expected_profile_sha:
                    errors.append(f"{build_id}: profile byte SHA mismatch: {actual} != {expected_profile_sha}")

        index_rel = entry.get("runtime_index")
        expected_log_sha = entry.get("runtime_log_sha256")
        if not index_rel or not expected_log_sha:
            errors.append(f"{build_id}: runtime index/log SHA missing from artifact evidence index")
            continue
        index_path = ROOT / index_rel
        if not index_path.is_file():
            errors.append(f"{build_id}: runtime index missing: {index_rel}")
            continue
        index = load_json(index_path)
        log_entries = [x for x in index.get("files", []) if x.get("name") == "LogOutput.log"]
        if len(log_entries) != 1:
            errors.append(f"{build_id}: expected exactly one LogOutput.log in {index_rel}")
            continue
        indexed_sha = log_entries[0].get("sha256")
        if indexed_sha != expected_log_sha:
            errors.append(f"{build_id}: artifact index/runtime INDEX SHA mismatch: {expected_log_sha} != {indexed_sha}")

        sources = [a.get("source") for a in index.get("analysis", []) if a.get("source")]
        log_source = next((s for s in sources if str(s).endswith("/raw/LogOutput.log")), None)
        if log_source is None:
            log_source = (Path(index_rel).parent / "raw" / "LogOutput.log").as_posix()
        log_path = ROOT / str(log_source)
        if not log_path.is_file():
            errors.append(f"{build_id}: raw runtime log bytes missing: {log_source}")
            continue
        actual_log_sha = sha256_file(log_path)
        checked_logs += 1
        if actual_log_sha != expected_log_sha:
            errors.append(f"{build_id}: raw runtime-log byte SHA mismatch: {actual_log_sha} != {expected_log_sha}")
        expected_size = log_entries[0].get("size")
        if isinstance(expected_size, int) and log_path.stat().st_size != expected_size:
            errors.append(f"{build_id}: raw runtime-log byte size mismatch: {log_path.stat().st_size} != {expected_size}")
        for analysis in index.get("analysis", []):
            source_sha = analysis.get("stats", {}).get("source_sha256")
            if source_sha and source_sha != actual_log_sha:
                errors.append(f"{build_id}: embedded analysis source_sha256 disagrees with raw bytes")

    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print(f"PASS: actual bytes verified for {checked_profiles} profiles and {checked_logs} runtime logs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
