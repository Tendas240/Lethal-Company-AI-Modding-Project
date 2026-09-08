#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from profile_builder import decode, read_zip, sha_file, snapshot

REGISTRY = Path("Profiles/EXPECTED_HASHES.json")
LINEAGE = Path("Current/BUILD_LINEAGE.json")


def resolve_build(path: Path, actual_hash: str, registry: dict, lineage: dict) -> str:
    rel = path.as_posix()
    meta = registry.get(rel)
    if meta:
        expected = str(meta["sha256"]).lower()
        if actual_hash != expected:
            raise RuntimeError(f"SHA-256 mismatch for {path}: expected {expected}, got {actual_hash}")
        return str(meta["build_id"])

    matches = [
        b for b in lineage.get("builds", [])
        if isinstance(b, dict) and b.get("profile") == rel and b.get("id")
    ]
    if len(matches) > 1:
        raise RuntimeError(f"Multiple BUILD_LINEAGE entries claim profile {path}")
    if len(matches) == 1:
        entry = matches[0]
        expected = entry.get("sha256")
        if expected and actual_hash != str(expected).lower():
            raise RuntimeError(
                f"SHA-256 mismatch for lineage profile {path}: expected {expected}, got {actual_hash}"
            )
        return str(entry["id"])

    if rel.startswith("Profiles/"):
        raise RuntimeError(
            f"Current profile {path} has no canonical build mapping in Profiles/EXPECTED_HASHES.json "
            "or Current/BUILD_LINEAGE.json; refusing filename-derived snapshot directory"
        )

    # Retained legacy references are not part of the current build lineage and may
    # continue using a deterministic filename-derived identifier under their own
    # References/LegacyProfiles/.../Extracted snapshot location.
    return path.stem.replace(" ", "_")


def main(paths: list[str]) -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    lineage = json.loads(LINEAGE.read_text(encoding="utf-8")) if LINEAGE.exists() else {"builds": []}

    if not paths:
        print("No profile paths supplied.")
        return 0

    for raw in paths:
        path = Path(raw)
        if not path.exists():
            raise RuntimeError(f"Profile path does not exist: {path}")

        actual_hash = sha_file(path)
        build_id = resolve_build(path, actual_hash, registry, lineage)

        entries = read_zip(path)
        exports = [e for e in entries if e.name == "export.r2x"]
        if len(exports) != 1:
            raise RuntimeError(f"{path}: export.r2x count is {len(exports)}, expected 1")

        export_text = decode(exports[0].data)
        m = re.search(r"(?m)^\s*profileName\s*:\s*(.+?)\s*$", export_text)
        if not m:
            raise RuntimeError(f"{path}: profileName not found")
        profile_name = m.group(1).strip().strip('"').strip("'")

        if path.as_posix().startswith("References/LegacyProfiles/"):
            snap_dir = path.parent / "Extracted"
        else:
            snap_dir = Path("ProfileSources") / build_id

        snap_info = snapshot(entries, snap_dir)
        result = {
            "build_id": build_id,
            "profile_path": path.as_posix(),
            "profile_name": profile_name,
            "sha256": actual_hash,
            "zip_members": len(entries),
            "snapshot_dir": snap_dir.as_posix(),
            "snapshot": snap_info,
            "build_id_resolution": "EXPECTED_HASHES" if path.as_posix() in registry else (
                "BUILD_LINEAGE" if path.as_posix().startswith("Profiles/") else "LEGACY_FILENAME"
            ),
        }
        (snap_dir / "PROFILE_INDEX_RESULT.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
