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


def main() -> int:
    if not ACTIVE.exists():
        raise RuntimeError("RuntimeInbox/ACTIVE_BUILD.txt is missing")
    build_id = ACTIVE.read_text(encoding="utf-8").strip()
    if not build_id:
        raise RuntimeError("ACTIVE_BUILD.txt is empty")

    files = sorted(p for p in INBOX.iterdir() if p.is_file() and p.name != ".gitkeep")
    if not files:
        print("No runtime evidence waiting in RuntimeInbox/Current.")
        return 0

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

    for source in files:
        dest = raw_dir / source.name
        shutil.copy2(source, dest)
        record = {
            "name": source.name,
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

    for source in files:
        source.unlink()

    print(json.dumps(index, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
