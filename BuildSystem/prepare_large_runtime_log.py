#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

PART_SIZE = 20 * 1024 * 1024


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a very large runtime log for the disposable runtime-large branch")
    parser.add_argument("log", type=Path)
    parser.add_argument("--output", type=Path, default=Path("RuntimeInbox/Large"))
    args = parser.parse_args()

    source = args.log.resolve()
    if not source.is_file():
        raise SystemExit(f"Input file not found: {source}")
    args.output.mkdir(parents=True, exist_ok=True)

    archive = args.output / f"{source.name}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=True) as z:
        z.write(source, arcname=source.name)

    archive_size = archive.stat().st_size
    archive_hash = sha256(archive)
    parts = []
    if archive_size > PART_SIZE:
        with archive.open("rb") as src:
            n = 1
            while True:
                data = src.read(PART_SIZE)
                if not data:
                    break
                part = args.output / f"{archive.name}.part{n:03d}"
                part.write_bytes(data)
                parts.append({"name": part.name, "size": part.stat().st_size, "sha256": sha256(part)})
                n += 1
        archive.unlink()
    else:
        parts.append({"name": archive.name, "size": archive_size, "sha256": archive_hash})

    manifest = {
        "schema_version": 1,
        "original_name": source.name,
        "original_size": source.stat().st_size,
        "original_sha256": sha256(source),
        "archive_name": f"{source.name}.zip",
        "archive_size": archive_size,
        "archive_sha256": archive_hash,
        "split_part_size": PART_SIZE,
        "upload_files": parts,
        "target_branch": "runtime-large",
        "target_directory": "RuntimeInbox/Large",
    }
    manifest_path = args.output / "UPLOAD_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
