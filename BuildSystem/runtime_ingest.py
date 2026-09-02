#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

INBOX = Path("RuntimeInbox/Current")
ACTIVE = Path("RuntimeInbox/ACTIVE_BUILD.txt")
EVIDENCE = Path("RuntimeEvidence")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_extract(archive: Path, target: Path) -> list[str]:
    extracted = []
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
            extracted.append(str(rel))
    return extracted


def main() -> int:
    if not ACTIVE.exists():
        raise RuntimeError("RuntimeInbox/ACTIVE_BUILD.txt is missing")
    build_id = ACTIVE.read_text(encoding="utf-8").strip()
    if not build_id:
        raise RuntimeError("ACTIVE_BUILD.txt is empty")

    files = sorted(
        p for p in INBOX.iterdir()
        if p.is_file() and p.name != ".gitkeep"
    )
    if not files:
        print("No runtime evidence waiting in RuntimeInbox/Current.")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = EVIDENCE / build_id / stamp
    raw_dir = run_dir / "raw"
    extracted_dir = run_dir / "extracted"
    raw_dir.mkdir(parents=True, exist_ok=False)

    index = {
        "build_id": build_id,
        "ingested_utc": stamp,
        "files": [],
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

        if source.suffix.lower() in {".zip", ".r2z"}:
            target = extracted_dir / source.stem
            target.mkdir(parents=True, exist_ok=True)
            record["extracted"] = safe_extract(dest, target)

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
