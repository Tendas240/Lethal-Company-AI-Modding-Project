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

ONE_SHOT_REL = "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json"
# Independently pinned constants: a modified manifest must not redefine evidence truth.
ONE_SHOT_EXPECTED = {
    "contract_id": "S1.42AK-OFFENSE-MINESHAFT-20261020-V1",
    "build_id": "S1.42AK",
    "inbox_filename": "S1.42AK_OFFENSE_20261020_LogOutput.log",
    "raw_filename": "LogOutput.log",
    "size": 3173316,
    "sha256": "7c7b02af7891b97b48078432ca8bf8d26d051a533cc15810d012950c44fac6c9",
    "accepted_profile": "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z",
    "accepted_profile_sha256": "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee",
    "runtime_active_build": "S1.42AK-BMDSFIX1",
    "moon": "Offense",
    "flow": "Level3Flow",
    "seed": 43291983,
    "lines": 31886
}


V2_REL = "Current/S1.42AK_OFFENSE_RANDOM_BATCH_V2_INGEST_V1.json"
# Independently pinned, NOT imported from the ingest script or mutable contract.
V2_EXPECTED = {
    "contract_id": "S1.42AK-OFFENSE-RANDOM-BATCH-20261021-V2",
    "build_id": "S1.42AK",
    "inbox_filename": "S1.42AK_OFFENSE_RANDOM_BATCH_20261021_LogOutput.log",
    "raw_filename": "LogOutput.log",
    "size": 10906072,
    "sha256": "969044ab459387c3a509134c4c56a10ae1736b46af9fc76d3ac8cf01c25ec07d",
    "accepted_profile": "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z",
    "accepted_profile_sha256": "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee",
    "runtime_active_build": "S1.42AK-BMDSFIX1",
    "moon": "Offense",
}
V2_PROVENANCE = "USER_ATTESTED_S1_42AK_PROFILE_CONTINUITY_NOT_INDEPENDENT_BYTES"
V2_RETENTION = {
    "raw_original": "PRESERVE_UNTIL_SEPARATE_P0_P6_AND_RETENTION_DECISION",
    "public_upload_requires_separate_user_approval": True,
    "no_automatic_deletion": True,
}
V2_MODE = "COMPLETED_S1_42AK_OFFENSE_RANDOM_BATCH_V2_NOT_RUNTIME_ACTIVATION"

PENDING_ROLES = {
    "ACTIVE_RUNTIME_CANDIDATE_PENDING",
    "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
    "DEFERRED_FULL_NORMAL_RUNTIME_GATE_NOT_WAIVED",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized_sha256(value: Any) -> str:
    """Canonicalize textual SHA metadata before comparison."""
    text = str(value).strip().lower()
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        return ""
    return text


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
    expected_profile_sha = normalized_sha256(entry.get("profile_sha256"))
    if not profile_rel or not expected_profile_sha:
        errors.append(f"{build_id}: profile path/SHA missing or malformed in artifact evidence index")
        return False
    profile_path = ROOT / str(profile_rel)
    if not profile_path.is_file():
        errors.append(f"{build_id}: profile bytes missing: {profile_rel}")
        return False
    actual = sha256_file(profile_path)
    if actual != expected_profile_sha:
        errors.append(f"{build_id}: profile byte SHA mismatch: {actual} != {expected_profile_sha}")
        return False
    require_readable_profile_artifacts(entry, build_id, errors)
    return True


def resolve_runtime_log(index_rel: Any) -> tuple[dict[str, Any] | None, Path | None]:
    if not index_rel:
        return None, None
    index_path = ROOT / str(index_rel)
    if not index_path.is_file():
        return None, None
    index = load_json(index_path)
    sources = [a.get("source") for a in index.get("analysis", []) if a.get("source")]
    log_source = next((s for s in sources if str(s).endswith("/raw/LogOutput.log")), None)
    if log_source is None:
        log_source = (Path(str(index_rel)).parent / "raw" / "LogOutput.log").as_posix()
    log_path = ROOT / str(log_source)
    return index, log_path if log_path.is_file() else None


def verify_runtime(entry: dict[str, Any], errors: list[str]) -> bool:
    build_id = str(entry.get("build_id", "<missing-build-id>"))
    index_rel = entry.get("runtime_index")
    expected_log_sha_raw = entry.get("runtime_log_sha256")
    expected_log_sha = normalized_sha256(expected_log_sha_raw)
    if not index_rel or not expected_log_sha:
        raw_text = str(expected_log_sha_raw)
        codepoints = " ".join(f"U+{ord(ch):04X}" for ch in raw_text)
        diagnostic = ""
        _, diagnostic_log_path = resolve_runtime_log(index_rel)
        if diagnostic_log_path is not None:
            actual_raw_sha = sha256_file(diagnostic_log_path)
            actual_codepoints = " ".join(f"{i}:{ord(ch):02X}" for i, ch in enumerate(actual_raw_sha))
            diagnostic = (
                f" actual_raw_sha256={actual_raw_sha} actual_len={len(actual_raw_sha)}"
                f" actual_codepoints={actual_codepoints}"
            )
        errors.append(
            f"{build_id}: runtime index/log SHA missing or malformed in artifact evidence entry; "
            f"raw={expected_log_sha_raw!r} len={len(raw_text)} codepoints={codepoints}{diagnostic}"
        )
        return False

    index, log_path = resolve_runtime_log(index_rel)
    if index is None:
        errors.append(f"{build_id}: runtime index missing: {index_rel}")
        return False

    log_entries = [x for x in index.get("files", []) if x.get("name") == "LogOutput.log"]
    if len(log_entries) != 1:
        errors.append(f"{build_id}: expected exactly one LogOutput.log in {index_rel}")
        return False

    indexed_sha = normalized_sha256(log_entries[0].get("sha256"))
    if not indexed_sha:
        errors.append(f"{build_id}: runtime INDEX contains malformed LogOutput.log SHA")
    elif indexed_sha != expected_log_sha:
        errors.append(f"{build_id}: artifact index/runtime INDEX SHA mismatch: {expected_log_sha} != {indexed_sha}")

    if log_path is None:
        errors.append(f"{build_id}: raw runtime log bytes missing for {index_rel}")
        return False

    actual_log_sha = sha256_file(log_path)
    if actual_log_sha != expected_log_sha:
        errors.append(f"{build_id}: raw runtime-log byte SHA mismatch: {actual_log_sha} != {expected_log_sha}")
    expected_size = log_entries[0].get("size")
    if isinstance(expected_size, int) and log_path.stat().st_size != expected_size:
        errors.append(f"{build_id}: raw runtime-log byte size mismatch: {log_path.stat().st_size} != {expected_size}")
    for analysis in index.get("analysis", []):
        source_sha_raw = analysis.get("stats", {}).get("source_sha256")
        if source_sha_raw:
            source_sha = normalized_sha256(source_sha_raw)
            if not source_sha:
                errors.append(f"{build_id}: embedded analysis source_sha256 is malformed")
            elif source_sha != actual_log_sha:
                errors.append(f"{build_id}: embedded analysis source_sha256 disagrees with raw bytes")
    return True



def verify_one_shot_contract(root: Path, errors: list[str], *,
                             expected_override: dict[str, Any] | None = None) -> None:
    """Validate the complete one-time receipt and original bytes independently."""
    expected = ONE_SHOT_EXPECTED if expected_override is None else expected_override
    path = root / ONE_SHOT_REL
    if not path.is_file():
        errors.append("S1.42AK one-shot: versioned contract missing")
        return
    try:
        contract = load_json(path)
    except (OSError, ValueError) as exc:
        errors.append(f"S1.42AK one-shot: invalid contract JSON: {exc}")
        return
    if (set(contract) != {"schema_version", "status", "expected", "receipt", "provenance"}
            or type(contract["schema_version"]) is not int or contract["schema_version"] != 1
            or contract["expected"] != expected
            or contract["provenance"] != "PRIOR_CHAT_USER_ORIGINAL_LOG_PROFILE_BYTE_IDENTITY_P0_PARTIAL"):
        errors.append("S1.42AK one-shot: altered contract schema/expected provenance")
        return
    status = contract.get("status")
    receipt = contract.get("receipt")
    if status == "PENDING":
        if receipt is not None:
            errors.append("S1.42AK one-shot: PENDING must not contain a receipt")
        return
    if status != "CONSUMED" or not isinstance(receipt, dict):
        errors.append("S1.42AK one-shot: invalid consumption status/receipt")
        return

    stamp = receipt.get("ingested_utc")
    if (not isinstance(stamp, str) or len(stamp) != 16
            or stamp[8] != "T" or stamp[-1] != "Z"
            or not stamp[:8].isdigit() or not stamp[9:-1].isdigit()):
        errors.append("S1.42AK one-shot: unsafe/malformed ingest stamp")
        return
    directory = Path("RuntimeEvidence") / expected["build_id"] / stamp
    index_rel = (directory / "INDEX.json").as_posix()
    raw_rel = (directory / "raw" / expected["raw_filename"]).as_posix()
    required = {
        "contract_id": expected["contract_id"],
        "ingested_utc": stamp,
        "evidence_index": index_rel,
        "raw_path": raw_rel,
        "sha256": expected["sha256"],
        "size": expected["size"],
        "build_id": expected["build_id"],
        "source_inbox_name": expected["inbox_filename"],
        "runtime_active_build_at_ingest": expected["runtime_active_build"],
        "original_profile_bytes_independently_verified": False,
    }
    if receipt != required:
        errors.append("S1.42AK one-shot: consumed receipt drift")
        return
    index_path, raw_path = root / index_rel, root / raw_rel
    if not index_path.is_file() or not raw_path.is_file() or raw_path.is_symlink():
        errors.append("S1.42AK one-shot: original raw evidence or index absent")
        return
    try:
        index = load_json(index_path)
    except (OSError, ValueError) as exc:
        errors.append(f"S1.42AK one-shot: invalid evidence INDEX: {exc}")
        return
    attribution = {
        "mode": "COMPLETED_S1_42AK_ONE_SHOT_NOT_RUNTIME_ACTIVATION",
        "contract_id": expected["contract_id"],
        "source_inbox_name": expected["inbox_filename"],
        "runtime_active_build_at_ingest": expected["runtime_active_build"],
        "original_profile_bytes_independently_verified": False,
    }
    files = index.get("files", [])
    if (index.get("build_id") != expected["build_id"]
            or index.get("ingested_utc") != stamp
            or index.get("attribution") != attribution
            or not isinstance(files, list) or len(files) != 1
            or files[0].get("name") != expected["raw_filename"]
            or files[0].get("sha256") != expected["sha256"]
            or files[0].get("size") != expected["size"]):
        errors.append("S1.42AK one-shot: INDEX attribution/byte metadata drift")
    if raw_path.stat().st_size != expected["size"] or sha256_file(raw_path) != expected["sha256"]:
        errors.append("S1.42AK one-shot: raw original byte identity mismatch")
    analysis = index.get("analysis", [])
    if not isinstance(analysis, list) or len(analysis) != 1 or (
            analysis[0].get("stats", {}).get("source_sha256") != expected["sha256"]
            or analysis[0].get("stats", {}).get("line_count") != expected["lines"]):
        errors.append("S1.42AK one-shot: analysis SHA/line-count disagreement")
    for rel in ("STATS.json", "MARKERS.json", "CHAT_CHUNKS_MANIFEST.json"):
        analyzed = directory / "analysis" / "raw__S1.42AK_OFFENSE_20261020_LogOutput" / rel
        if not (root / analyzed).is_file():
            errors.append(f"S1.42AK one-shot: missing analysis {analyzed}")



def verify_v2_contract(root: Path, errors: list[str], *,
                       expected_override: dict[str, Any] | None = None) -> None:
    expected = V2_EXPECTED if expected_override is None else expected_override
    path = root / V2_REL
    if not path.is_file():
        errors.append("S1.42AK V2: versioned contract missing")
        return
    try:
        contract = load_json(path)
    except (OSError, ValueError) as exc:
        errors.append(f"S1.42AK V2: invalid contract JSON: {exc}")
        return
    if (set(contract) != {"schema_version", "status", "expected", "receipt", "provenance", "retention"}
            or type(contract["schema_version"]) is not int or contract["schema_version"] != 1
            or contract["expected"] != expected or contract["provenance"] != V2_PROVENANCE
            or contract["retention"] != V2_RETENTION):
        errors.append("S1.42AK V2: contract/identity/retention drift")
        return
    status, receipt = contract.get("status"), contract.get("receipt")
    if status == "PENDING":
        if receipt is not None:
            errors.append("S1.42AK V2: PENDING must have no receipt")
        return
    if status != "CONSUMED" or not isinstance(receipt, dict):
        errors.append("S1.42AK V2: invalid status/consumption receipt")
        return
    stamp = receipt.get("ingested_utc")
    if (not isinstance(stamp, str) or len(stamp) != 16 or stamp[8] != "T"
            or stamp[-1] != "Z" or not stamp[:8].isdigit() or not stamp[9:-1].isdigit()):
        errors.append("S1.42AK V2: unsafe ingest timestamp")
        return
    directory = Path("RuntimeEvidence") / expected["build_id"] / stamp
    index_rel = (directory / "INDEX.json").as_posix()
    raw_rel = (directory / "raw" / expected["raw_filename"]).as_posix()
    required = {
        "contract_id": expected["contract_id"],
        "ingested_utc": stamp,
        "evidence_index": index_rel,
        "raw_path": raw_rel,
        "sha256": expected["sha256"],
        "size": expected["size"],
        "build_id": expected["build_id"],
        "source_inbox_name": expected["inbox_filename"],
        "runtime_active_build_at_ingest": expected["runtime_active_build"],
        "original_profile_bytes_independently_verified": False,
    }
    if receipt != required:
        errors.append("S1.42AK V2: consumed receipt drift")
        return
    index_path, raw_path = root / index_rel, root / raw_rel
    if not index_path.is_file() or not raw_path.is_file() or raw_path.is_symlink():
        errors.append("S1.42AK V2: original raw/INDEX missing")
        return
    try:
        index = load_json(index_path)
    except (OSError, ValueError) as exc:
        errors.append(f"S1.42AK V2: invalid INDEX: {exc}")
        return
    attribution = {
        "mode": V2_MODE,
        "contract_id": expected["contract_id"],
        "source_inbox_name": expected["inbox_filename"],
        "runtime_active_build_at_ingest": expected["runtime_active_build"],
        "original_profile_bytes_independently_verified": False,
    }
    indexed_files = index.get("files", [])
    retention = index.get("retention", {})
    if (index.get("build_id") != expected["build_id"] or index.get("ingested_utc") != stamp
            or index.get("attribution") != attribution
            or not isinstance(indexed_files, list) or len(indexed_files) != 1
            or indexed_files[0].get("name") != expected["raw_filename"]
            or indexed_files[0].get("sha256") != expected["sha256"]
            or indexed_files[0].get("size") != expected["size"]
            or retention.get("raw_and_extracted_are_disposable_after_acceptance") is not False
            or retention.get("raw_original") != V2_RETENTION["raw_original"]
            or retention.get("no_automatic_deletion") is not True):
        errors.append("S1.42AK V2: INDEX/attribution/retention drift")
    if raw_path.stat().st_size != expected["size"] or sha256_file(raw_path) != expected["sha256"]:
        errors.append("S1.42AK V2: raw original byte mismatch")
    analysis = index.get("analysis", [])
    if (not isinstance(analysis, list) or len(analysis) != 1
            or analysis[0].get("stats", {}).get("source_sha256") != expected["sha256"]
            or analysis[0].get("stats", {}).get("source_size_bytes") != expected["size"]):
        errors.append("S1.42AK V2: analyzer/INDEX SHA or size disagreement")
    analysis_dir = directory / "analysis" / ("raw__" + Path(expected["inbox_filename"]).stem)
    for name in ("STATS.json", "MARKERS.json", "CHAT_CHUNKS_MANIFEST.json"):
        if not (root / analysis_dir / name).is_file():
            errors.append(f"S1.42AK V2: missing analysis artifact {analysis_dir / name}")


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
        if entry.get("role") not in PENDING_ROLES:
            errors.append(
                f"{build_id}: pending_profiles entry role {entry.get('role')!r} is not one of "
                f"{sorted(PENDING_ROLES)}"
            )
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

    verify_one_shot_contract(ROOT, errors)
    verify_v2_contract(ROOT, errors)

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
