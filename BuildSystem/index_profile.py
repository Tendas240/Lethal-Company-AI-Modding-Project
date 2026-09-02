#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from profile_builder import decode, read_zip, sha_file, snapshot

REGISTRY = Path("Profiles/EXPECTED_HASHES.json")


def main(paths: list[str]) -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}

    if not paths:
        print("No profile paths supplied.")
        return 0

    for raw in paths:
        path = Path(raw)
        if not path.exists():
            raise RuntimeError(f"Profile path does not exist: {path}")

        meta = registry.get(path.as_posix())
        actual_hash = sha_file(path)
        if meta:
            expected = meta["sha256"].lower()
            if actual_hash != expected:
                raise RuntimeError(
                    f"SHA-256 mismatch for {path}: expected {expected}, got {actual_hash}"
                )
            build_id = meta["build_id"]
        else:
            build_id = path.stem.replace(" ", "_")

        entries = read_zip(path)
        exports = [e for e in entries if e.name == "export.r2x"]
        if len(exports) != 1:
            raise RuntimeError(f"{path}: export.r2x count is {len(exports)}, expected 1")

        export_text = decode(exports[0].data)
        m = re.search(r"(?m)^\s*profileName\s*:\s*(.+?)\s*$", export_text)
        if not m:
            raise RuntimeError(f"{path}: profileName not found")
        profile_name = m.group(1).strip().strip('"').strip("'")

        snap_dir = Path("ProfileSources") / build_id
        snap_info = snapshot(entries, snap_dir)
        result = {
            "build_id": build_id,
            "profile_path": path.as_posix(),
            "profile_name": profile_name,
            "sha256": actual_hash,
            "zip_members": len(entries),
            "snapshot": snap_info,
        }
        (snap_dir / "PROFILE_INDEX_RESULT.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
