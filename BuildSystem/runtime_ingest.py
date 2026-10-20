#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from runtime_log_analyzer import analyze_log, is_text_candidate

INBOX = Path("RuntimeInbox/Current")
ACTIVE = Path("RuntimeInbox/ACTIVE_BUILD.txt")
EVIDENCE = Path("RuntimeEvidence")
PERSIST_EXTRACTED_LIMIT = 16 * 1024 * 1024

ONESHOT_CONTRACT = Path("Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json")
ONESHOT_STATE = Path("Current/CURRENT_STATE.json")
ONESHOT_BUILDSPEC = Path("BuildSpecs/current.json")
ONESHOT_EXPECTED = {
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



def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(archive: Path, target: Path) -> list[dict]:
    extracted: list[dict] = []
    with zipfile.ZipFile(archive, "r") as z:
        for info in z.infolist():
            rel = PurePosixPath(info.filename)
            if rel.is_absolute() or ".." in rel.parts:
                raise RuntimeError(f"Unsafe archive member: {info.filename}")
            dest = target / rel
            if info.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info, "r") as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted.append({
                "path": str(rel),
                "size": dest.stat().st_size,
                "sha256": sha256(dest),
                "persisted": True,
            })
    return extracted


def analyze_candidate(path: Path, analysis_root: Path, label: str) -> dict | None:
    if not is_text_candidate(path):
        return None
    out = analysis_root / label
    stats = analyze_log(path, out, create_chat_chunks=True)
    return {
        "source": str(path),
        "analysis": str(out),
        "stats": stats,
    }



def require_one_shot(source: Path, active: str, files: list[Path]) -> dict:
    """Fail-closed before any evidence write; never promotes or activates a profile."""
    expected = ONESHOT_EXPECTED
    if len(files) != 1 or files[0] != source:
        raise RuntimeError("ONESHOT_REFUSED: reserved upload must be the sole inbox evidence")
    if source.is_symlink() or not source.is_file() or source.name != expected["inbox_filename"]:
        raise RuntimeError("ONESHOT_REFUSED: wrong source type or reserved name")
    if source.stat().st_size != expected["size"] or sha256(source) != expected["sha256"]:
        raise RuntimeError("ONESHOT_REFUSED: original log size/SHA-256 mismatch")
    if active != expected["runtime_active_build"]:
        raise RuntimeError("ONESHOT_REFUSED: runtime controller changed; no fallback")
    if not ONESHOT_CONTRACT.is_file():
        raise RuntimeError("ONESHOT_REFUSED: versioned contract missing")
    contract = json.loads(ONESHOT_CONTRACT.read_text(encoding="utf-8"))
    if (set(contract) != {"schema_version", "status", "expected", "receipt", "provenance"}
            or type(contract["schema_version"]) is not int or contract["schema_version"] != 1
            or contract["status"] != "PENDING" or contract["receipt"] is not None
            or contract["expected"] != expected
            or contract["provenance"] != "PRIOR_CHAT_USER_ORIGINAL_LOG_PROFILE_BYTE_IDENTITY_P0_PARTIAL"):
        raise RuntimeError("ONESHOT_REFUSED: contract mismatch or already consumed")
    state = json.loads(ONESHOT_STATE.read_text(encoding="utf-8"))
    accepted = state.get("accepted_baseline", {})
    candidate = state.get("active_candidate", {})
    latest = state.get("latest_built_artifact", {})
    controllers = state.get("controllers", {})
    buildspec = json.loads(ONESHOT_BUILDSPEC.read_text(encoding="utf-8"))
    if not (accepted.get("build_id") == expected["build_id"]
            and accepted.get("profile") == expected["accepted_profile"]
            and accepted.get("sha256") == expected["accepted_profile_sha256"]
            and accepted.get("status") == "ACCEPTED_FULL_NORMAL_STACK"
            and candidate.get("build_id") == expected["runtime_active_build"]
            and candidate.get("status") == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
            and latest.get("build_id") == candidate.get("build_id")
            and controllers.get("runtime_active_build") == active
            and controllers.get("build_enabled") is False
            and buildspec.get("enabled") is False
            and buildspec.get("build_id") == controllers.get("build_id")
            and buildspec.get("base_profile") == candidate.get("profile")
            and buildspec.get("base_sha256") == candidate.get("sha256")
            and buildspec.get("output_profile") == "Profiles/DO_NOT_BUILD.r2z"):
        raise RuntimeError("ONESHOT_REFUSED: state/profile/controller drift")
    target = EVIDENCE / expected["build_id"]
    if target.exists():
        for index_path in sorted(target.glob("*/INDEX.json")):
            index = json.loads(index_path.read_text(encoding="utf-8"))
            if (index.get("attribution", {}).get("contract_id") == expected["contract_id"]
                    or any(e.get("sha256") == expected["sha256"] for e in index.get("files", []))):
                raise RuntimeError("ONESHOT_REFUSED: already indexed; replay")
    return contract


def refuse_misattributed_original(files: list[Path]) -> None:
    """Never route these exact original bytes to the active BMDSFIX1 namespace."""
    for source in files:
        if source.stat().st_size == ONESHOT_EXPECTED["size"] and sha256(source) == ONESHOT_EXPECTED["sha256"]:
            raise RuntimeError("ONESHOT_REFUSED: exact original requires reserved inbox filename")


def consume_one_shot(contract: dict, run_dir: Path, stamp: str, active: str) -> None:
    expected = ONESHOT_EXPECTED
    contract["status"] = "CONSUMED"
    contract["receipt"] = {
        "contract_id": expected["contract_id"],
        "ingested_utc": stamp,
        "evidence_index": (run_dir / "INDEX.json").as_posix(),
        "raw_path": (run_dir / "raw" / expected["raw_filename"]).as_posix(),
        "sha256": expected["sha256"],
        "size": expected["size"],
        "build_id": expected["build_id"],
        "source_inbox_name": expected["inbox_filename"],
        "runtime_active_build_at_ingest": active,
        "original_profile_bytes_independently_verified": False,
    }
    # Workflow commits receipt + INDEX + raw + inbox deletion as one Git commit.
    ONESHOT_CONTRACT.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main() -> int:
    if not ACTIVE.exists():
        raise RuntimeError("RuntimeInbox/ACTIVE_BUILD.txt is missing")
    build_id = ACTIVE.read_text(encoding="utf-8").strip()
    if not build_id:
        raise RuntimeError("ACTIVE_BUILD.txt is empty")

    files = sorted(p for p in INBOX.iterdir() if p.name != ".gitkeep")
    if not files:
        print("No runtime evidence waiting in RuntimeInbox/Current.")
        return 0
    if any(p.is_symlink() or not p.is_file() for p in files):
        raise RuntimeError("Runtime inbox contains unsupported file type")
    one_shot = any(p.name == ONESHOT_EXPECTED["inbox_filename"] for p in files)
    contract = require_one_shot(next(p for p in files if p.name == ONESHOT_EXPECTED["inbox_filename"]), build_id, files) if one_shot else None
    if one_shot:
        build_id = ONESHOT_EXPECTED["build_id"]
    else:
        refuse_misattributed_original(files)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = EVIDENCE / build_id / stamp
    raw_dir = run_dir / "raw"
    extracted_dir = run_dir / "extracted"
    analysis_dir = run_dir / "analysis"
    raw_dir.mkdir(parents=True, exist_ok=False)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    index = {
        "schema_version": 2,
        "build_id": build_id,
        "ingested_utc": stamp,
        "pipeline": "runtime_ingest_v2_streaming_analysis",
        "files": [],
        "analysis": [],
        "retention": {
            "raw_and_extracted_are_disposable_after_acceptance": True,
            "keep_before_deletion": [
                "INDEX.json",
                "analysis/STATS.json equivalents",
                "analysis/MARKERS.json equivalents",
                "analysis/signature index",
                "canonical runtime acceptance documentation",
                "SHA-256 values needed for provenance",
            ],
        },
    }

    if one_shot:
        index["attribution"] = {
            "mode": "COMPLETED_S1_42AK_ONE_SHOT_NOT_RUNTIME_ACTIVATION",
            "contract_id": ONESHOT_EXPECTED["contract_id"],
            "source_inbox_name": ONESHOT_EXPECTED["inbox_filename"],
            "runtime_active_build_at_ingest": ONESHOT_EXPECTED["runtime_active_build"],
            "original_profile_bytes_independently_verified": False,
        }
    for source in files:
        dest = raw_dir / (ONESHOT_EXPECTED["raw_filename"] if one_shot else source.name)
        shutil.copy2(source, dest)
        record = {
            "name": dest.name,
            "size": dest.stat().st_size,
            "sha256": sha256(dest),
            "extracted": [],
        }

        direct = analyze_candidate(dest, analysis_dir, f"raw__{source.stem}")
        if direct:
            index["analysis"].append(direct)

        if source.suffix.lower() in {".zip", ".r2z"}:
            target = extracted_dir / source.stem
            target.mkdir(parents=True, exist_ok=True)
            record["extracted"] = safe_extract(dest, target)
            for item in record["extracted"]:
                member = target / item["path"]
                label = "archive__" + source.stem + "__" + item["path"].replace("/", "__").replace("\\", "__")
                analyzed = analyze_candidate(member, analysis_dir, label)
                if analyzed:
                    index["analysis"].append(analyzed)
                if member.stat().st_size > PERSIST_EXTRACTED_LIMIT:
                    member.unlink()
                    item["persisted"] = False
                    item["retention_note"] = (
                        "Expanded member exceeded 16 MiB and was intentionally not committed; "
                        "analysis is complete and the compressed raw archive remains available until evidence cleanup."
                    )

        index["files"].append(record)

    (run_dir / "INDEX.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if one_shot:
        consume_one_shot(contract, run_dir, stamp, ONESHOT_EXPECTED["runtime_active_build"])
    for source in files:
        source.unlink()

    print(json.dumps(index, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
