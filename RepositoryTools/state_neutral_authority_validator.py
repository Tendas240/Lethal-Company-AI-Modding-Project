#!/usr/bin/env python3
"""Keep architecture/governance topic documents free of volatile live lifecycle snapshots."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_NEUTRAL_DOCS = (
    "Knowledge/REPOSITORY_OVERHAUL.md",
)
REQUIRED_ROUTING_FRAGMENTS = (
    "Current/CURRENT_STATE.json",
    "Knowledge/CURRENT_LIFECYCLE.md",
    ".github/workflows/knowledge-architecture.yml",
    "Current/VALIDATOR_COVERAGE.json",
)
FORBIDDEN_PATTERNS = (
    (r"<!--\s*LIVE_STATE:", "live-state marker"),
    (r"(?im)^##\s+Current gameplay handoff\s*$", "current gameplay handoff section"),
    (r"(?im)^\s*Accepted gameplay baseline remains\b", "duplicated accepted-baseline declaration"),
    (r"(?im)^\s*Latest built artifact\s*:", "duplicated latest-artifact declaration"),
    (r"(?im)^\s*Active candidate\s*:", "duplicated active-candidate declaration"),
    (r"(?im)^\s*Runtime test outstanding\s*:", "duplicated runtime-pending declaration"),
    (r"(?im)^\s*No runtime test is outstanding\b", "duplicated runtime-pending declaration"),
    (r"(?im)^The permanent CI now runs:\s*$", "duplicated permanent-CI gate inventory"),
)


def validate_text(rel: str, text: str) -> list[str]:
    errors: list[str] = []
    for fragment in REQUIRED_ROUTING_FRAGMENTS:
        if fragment not in text:
            errors.append(f"{rel}: missing state-neutral routing fragment {fragment!r}")
    for pattern, label in FORBIDDEN_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"{rel}: forbidden {label}; route volatile truth to its canonical authority")
    return errors


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in STATE_NEUTRAL_DOCS:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing state-neutral authority document: {rel}")
            continue
        errors.extend(validate_text(rel, path.read_text(encoding="utf-8", errors="replace")))
    return errors


def self_test() -> int:
    good = """# Repository overhaul\nCurrent lifecycle: Current/CURRENT_STATE.json and Knowledge/CURRENT_LIFECYCLE.md.\nCI: .github/workflows/knowledge-architecture.yml with coverage in Current/VALIDATOR_COVERAGE.json.\n"""
    bad = good + """\n## Current gameplay handoff\nAccepted gameplay baseline remains **S1.TEST**.\nNo runtime test is outstanding.\n"""
    good_errors = validate_text("good.md", good)
    bad_errors = validate_text("bad.md", bad)
    if good_errors:
        print("ERROR: valid state-neutral fixture failed:", good_errors)
        return 1
    if len(bad_errors) < 3:
        print("ERROR: stale live-state fixture did not fail strongly enough:", bad_errors)
        return 1
    print("PASS: state-neutral authority validator negative fixture rejected duplicated live lifecycle state")
    return 0


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return self_test()
    errors = validate_repository(ROOT)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("PASS: architecture/governance topic documents remain state-neutral and route volatile truth to canonical authorities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
