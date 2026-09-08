#!/usr/bin/env python3
"""Inventory and validate externalized cold-history payloads.

The legacy Archive/ and Logs/ trees are historical payloads. This validator can
first inventory inbound path references and, once a cold-storage manifest is
present, enforce that only pointer files remain in the primary repository.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLD_ROOTS = ("Archive", "Logs")
MANIFEST = ROOT / "Current/COLD_HISTORY_STORAGE.json"
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".py", ".ps1", ".yml", ".yaml", ".toml",
    ".ini", ".cfg", ".cs", ".xml", ".csv", ".tsv", ".bat", ".cmd",
    ".sh", ".gitattributes", ".gitignore",
}


def is_text_candidate(path: Path) -> bool:
    if ".git" in path.parts:
        return False
    if any(root in path.parts for root in COLD_ROOTS):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {"README", "LICENSE"}


def inventory_references() -> list[tuple[str, int, str]]:
    refs: list[tuple[str, int, str]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not is_text_candidate(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(ROOT).as_posix()
        for number, line in enumerate(text.splitlines(), 1):
            if "Archive/" in line or "Logs/" in line:
                refs.append((rel, number, line.strip()))
    return refs


def validate_strict(refs: list[tuple[str, int, str]]) -> list[str]:
    errors: list[str] = []
    if not MANIFEST.is_file():
        return ["missing Current/COLD_HISTORY_STORAGE.json"]
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid cold-history manifest: {exc}"]

    allowed_files = set(manifest.get("allowed_primary_files", []))
    for root in COLD_ROOTS:
        directory = ROOT / root
        if not directory.is_dir():
            errors.append(f"missing cold-history pointer directory: {root}/")
            continue
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in directory.rglob("*") if path.is_file()
        }
        unexpected = sorted(actual - allowed_files)
        missing = sorted({p for p in allowed_files if p.startswith(root + "/")} - actual)
        for path in unexpected:
            errors.append(f"unexpected payload remains in primary repository: {path}")
        for path in missing:
            errors.append(f"required cold-history pointer missing: {path}")

    allowed_ref_files = set(manifest.get("allowed_reference_files", []))
    for rel, line_no, line in refs:
        if rel not in allowed_ref_files:
            errors.append(f"unmigrated inbound cold-history reference: {rel}:{line_no}: {line}")

    expected = {
        "Archive": "0dd155347e3174d5bdef7b27922ff738a9a11f35",
        "Logs": "9e67fc1a098b869dab9ba86063f5c2396d69c03f",
    }
    trees = manifest.get("externalized_trees", {})
    for root, sha in expected.items():
        entry = trees.get(root, {})
        if entry.get("source_tree_sha") != sha or entry.get("backup_tree_sha") != sha:
            errors.append(f"{root}: manifest does not preserve verified identical tree SHA {sha}")
        if not entry.get("recovery_repository") or not entry.get("recovery_commit"):
            errors.append(f"{root}: recovery repository/commit missing from manifest")

    if manifest.get("history_rewrite") is not False:
        errors.append("manifest must state history_rewrite=false")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", action="store_true")
    args = parser.parse_args()
    refs = inventory_references()
    print(f"cold-history inbound reference lines={len(refs)}")
    for rel, line_no, line in refs:
        print(f"REF {rel}:{line_no}: {line}")
    if args.inventory:
        return 0
    errors = validate_strict(refs)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("PASS: cold-history payload is externalized with controlled references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
