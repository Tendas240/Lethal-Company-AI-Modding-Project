#!/usr/bin/env python3
"""Repository-wide integrity linting for known-bad values, authority and generated artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_REL = "Current/INTEGRITY_ERRATA_REGISTRY.json"
TEXT_SUFFIXES = {
    ".md", ".json", ".txt", ".py", ".ps1", ".yml", ".yaml", ".cs",
    ".cfg", ".toml", ".ini", ".xml", ".r2x", ".csv",
}
DEFAULT_QUALIFIERS = (
    "supersed", "erratum", "incorrect", "wrong", "historical metadata",
    "historical sha", "old value", "old sha", "provenance correction",
    "do not use", "not authoritative", "not current", "qualification",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"README", "LICENSE", "Dockerfile", "Makefile"}:
            yield path


def scan_known_bad_values(root: Path, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    registry_rel = str(registry.get("registry_path", REGISTRY_REL))
    files: list[tuple[str, str]] = []
    for path in iter_text_files(root):
        try:
            files.append((path.relative_to(root).as_posix(), path.read_text(encoding="utf-8")))
        except (UnicodeDecodeError, OSError):
            pass

    for item in registry.get("known_bad_values", []):
        value = str(item.get("value", ""))
        bad_id = str(item.get("id", "<missing-id>"))
        if not value:
            errors.append(f"{bad_id}: empty known-bad value")
            continue
        allowed = set(item.get("allowed_historical_paths", []))
        qualifiers = tuple(str(x).lower() for x in item.get("local_qualifiers", DEFAULT_QUALIFIERS))
        occurrences = 0
        for rel, text in files:
            start = 0
            while True:
                idx = text.find(value, start)
                if idx < 0:
                    break
                occurrences += 1
                window = text[max(0, idx - 700): min(len(text), idx + len(value) + 700)].lower()
                qualified = rel == registry_rel or rel in allowed or any(q in window for q in qualifiers)
                if not qualified:
                    errors.append(f"{bad_id}: forbidden unqualified occurrence in {rel}")
                start = idx + len(value)
        if occurrences == 0:
            errors.append(f"{bad_id}: known-bad value vanished entirely; registry must preserve provenance")
    return errors


def authority_errors(root: Path, authority: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    seen: dict[tuple[str, str], str] = {}
    for entry in authority.get("canonical", []):
        path = str(entry.get("path", ""))
        level = str(entry.get("authority", ""))
        if not path or not (root / path).exists():
            errors.append(f"authority entry points to missing path: {path!r}")
        for claim in entry.get("canonical_for", []):
            key = (level, str(claim))
            previous = seen.get(key)
            if previous and previous != path:
                errors.append(f"duplicate current authority for {key}: {previous} and {path}")
            else:
                seen[key] = path
    return errors


def orphan_topic_errors(root: Path, knowledge_map: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    canonical = {str(t.get("canonical")) for t in knowledge_map.get("topics", []) if t.get("canonical")}
    knowledge_dir = root / "Knowledge"
    if knowledge_dir.is_dir():
        for path in knowledge_dir.glob("*.md"):
            rel = path.relative_to(root).as_posix()
            if rel not in canonical:
                errors.append(f"orphan Knowledge canonical document: {rel}")
    return errors


def generated_marker_errors(root: Path, registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for entry in registry.get("generated_artifacts", []):
        rel = str(entry.get("path", ""))
        marker = str(entry.get("required_marker", ""))
        path = root / rel
        if not path.is_file():
            errors.append(f"generated artifact missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if marker and marker not in text[:1200]:
            errors.append(f"generated artifact lacks required protection marker: {rel}")
    return errors


def main() -> int:
    registry_path = ROOT / REGISTRY_REL
    if not registry_path.is_file():
        print(f"ERROR: missing {REGISTRY_REL}")
        return 1
    registry = load_json(registry_path)
    errors: list[str] = []
    errors.extend(scan_known_bad_values(ROOT, registry))

    authority_path = ROOT / "Current/DOCUMENT_AUTHORITY.json"
    if not authority_path.is_file():
        errors.append("missing Current/DOCUMENT_AUTHORITY.json")
    else:
        errors.extend(authority_errors(ROOT, load_json(authority_path)))

    map_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.json"
    if not map_path.is_file():
        errors.append("missing Current/PROJECT_KNOWLEDGE_MAP.json")
    else:
        errors.extend(orphan_topic_errors(ROOT, load_json(map_path)))

    errors.extend(generated_marker_errors(ROOT, registry))
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("PASS: repository-wide integrity guard found no unqualified known-bad values, authority collisions, orphan topics, or generated-file marker drift")
    return 0


if __name__ == "__main__":
    sys.exit(main())
