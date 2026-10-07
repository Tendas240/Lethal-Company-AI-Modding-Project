#!/usr/bin/env python3
"""Validate externalized cold-history payloads and historical path recovery.

The legacy Archive/ and Logs/ payload trees are intentionally absent from current
HEAD after a positive deletion audit. Their exact bytes remain in primary Git
history and in the verified frozen recovery repository. This gate prevents the
payloads or unregistered direct references from silently returning.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
COLD_ROOTS = ("Archive", "Logs")
MANIFEST_REL = "Current/COLD_HISTORY_STORAGE.json"
EXPECTED_TREES = {
    "Archive": "0dd155347e3174d5bdef7b27922ff738a9a11f35",
    "Logs": "9e67fc1a098b869dab9ba86063f5c2396d69c03f",
}
EXPECTED_RECOVERY_REPOSITORY = "Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904"
EXPECTED_RECOVERY_COMMIT = "5dbd0e637a480d8591773e422bbca4b0654cad20"
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".py", ".ps1", ".yml", ".yaml", ".toml",
    ".ini", ".cfg", ".cs", ".xml", ".csv", ".tsv", ".bat", ".cmd",
    ".sh", ".gitattributes", ".gitignore",
}


def is_text_candidate(root: Path, path: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return False
    if ".git" in rel_parts:
        return False
    if any(cold in rel_parts for cold in COLD_ROOTS):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {"README", "LICENSE"}


def inventory_references(root: Path = ROOT) -> list[tuple[str, int, str]]:
    refs: list[tuple[str, int, str]] = []
    for path in root.rglob("*"):
        if not path.is_file() or not is_text_candidate(root, path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(root).as_posix()
        for number, line in enumerate(text.splitlines(), 1):
            if "Archive/" in line or "Logs/" in line:
                refs.append((rel, number, line.strip()))
    return refs


def load_manifest(root: Path, manifest_rel: str = MANIFEST_REL) -> tuple[dict[str, Any], list[str]]:
    path = root / manifest_rel
    if not path.is_file():
        return {}, [f"missing {manifest_rel}"]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except Exception as exc:
        return {}, [f"invalid cold-history manifest: {exc}"]


def validate_strict(
    root: Path = ROOT,
    manifest_rel: str = MANIFEST_REL,
    refs: list[tuple[str, int, str]] | None = None,
) -> list[str]:
    errors: list[str] = []
    manifest, load_errors = load_manifest(root, manifest_rel)
    if load_errors:
        return load_errors
    if refs is None:
        refs = inventory_references(root)

    if manifest.get("status") != "CURRENT_CANONICAL_COLD_HISTORY_STORAGE":
        errors.append("cold-history manifest status is not canonical/current")
    if manifest.get("history_rewrite") is not False:
        errors.append("manifest must state history_rewrite=false")
    if manifest.get("recovery_repository") != EXPECTED_RECOVERY_REPOSITORY:
        errors.append("recovery repository drift")
    if manifest.get("recovery_commit") != EXPECTED_RECOVERY_COMMIT:
        errors.append("recovery commit drift")
    mapping = str(manifest.get("path_mapping_rule", ""))
    if "same relative path" not in mapping or "Archive/" not in mapping or "Logs/" not in mapping:
        errors.append("manifest lacks deterministic same-relative-path recovery rule")

    allowed_files = set(map(str, manifest.get("allowed_primary_files", [])))
    wanted_allowed = {"Archive/README.md", "Logs/README.md"}
    if allowed_files != wanted_allowed:
        errors.append(f"allowed_primary_files drift: {sorted(allowed_files)}")

    trees = manifest.get("externalized_trees", {})
    for cold_root, sha in EXPECTED_TREES.items():
        entry = trees.get(cold_root, {}) if isinstance(trees, dict) else {}
        if entry.get("source_tree_sha") != sha or entry.get("backup_tree_sha") != sha:
            errors.append(f"{cold_root}: manifest does not preserve verified identical tree SHA {sha}")
        if entry.get("recovery_repository") != EXPECTED_RECOVERY_REPOSITORY:
            errors.append(f"{cold_root}: recovery repository drift")
        if entry.get("recovery_commit") != EXPECTED_RECOVERY_COMMIT:
            errors.append(f"{cold_root}: recovery commit drift")
        if entry.get("recovery_prefix") != cold_root + "/":
            errors.append(f"{cold_root}: recovery prefix drift")

        directory = root / cold_root
        if not directory.is_dir():
            errors.append(f"missing cold-history pointer directory: {cold_root}/")
            continue
        actual = {
            path.relative_to(root).as_posix()
            for path in directory.rglob("*") if path.is_file()
        }
        expected_here = {p for p in allowed_files if p.startswith(cold_root + "/")}
        for path in sorted(actual - expected_here):
            errors.append(f"unexpected payload remains in primary repository: {path}")
        for path in sorted(expected_here - actual):
            errors.append(f"required cold-history pointer missing: {path}")

        pointer_rel = str(entry.get("primary_pointer", ""))
        pointer = root / pointer_rel
        if pointer.is_file():
            text = pointer.read_text(encoding="utf-8", errors="replace")
            for needle in (sha, EXPECTED_RECOVERY_REPOSITORY, EXPECTED_RECOVERY_COMMIT, MANIFEST_REL):
                if needle not in text:
                    errors.append(f"{pointer_rel}: missing recovery proof fragment {needle}")

    allowed_ref_files = set(map(str, manifest.get("allowed_reference_files", [])))
    legacy_refs = set(map(str, manifest.get("legacy_reference_files", [])))
    infra_refs = set(map(str, manifest.get("infrastructure_reference_files", [])))
    if allowed_ref_files != legacy_refs | infra_refs:
        errors.append("allowed_reference_files must equal legacy_reference_files union infrastructure_reference_files")
    for rel in sorted(allowed_ref_files):
        if not (root / rel).is_file():
            errors.append(f"registered cold-history reference file missing: {rel}")
    for rel, line_no, line in refs:
        if rel not in allowed_ref_files:
            errors.append(f"unmigrated inbound cold-history reference: {rel}:{line_no}: {line}")

    migration_path = root / "Current/REPOSITORY_MIGRATION_MANIFEST.json"
    if not migration_path.is_file():
        errors.append("missing Current/REPOSITORY_MIGRATION_MANIFEST.json")
    else:
        try:
            migration = json.loads(migration_path.read_text(encoding="utf-8"))
            if migration.get("cold_history_manifest") != MANIFEST_REL:
                errors.append("migration manifest does not route to cold-history manifest")
            if migration.get("history_rewrite") is not False:
                errors.append("migration manifest must state history_rewrite=false")
        except Exception as exc:
            errors.append(f"invalid migration manifest: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", action="store_true", help="print references without enforcing externalization")
    args = parser.parse_args()
    refs = inventory_references(ROOT)
    print(f"cold-history inbound reference lines={len(refs)}")
    for rel, line_no, line in refs:
        print(f"REF {rel}:{line_no}: {line}")
    if args.inventory:
        return 0
    errors = validate_strict(ROOT, MANIFEST_REL, refs)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("PASS: cold-history payload is externalized with controlled recovery references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
