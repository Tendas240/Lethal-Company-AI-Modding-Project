#!/usr/bin/env python3
"""Repository-wide guard for the corrected S1.42AC raw runtime-log SHA provenance."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRATA_PATH = ROOT / "Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json"
INDEX_PATH = ROOT / "RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json"
AUTHORITATIVE = "fe4b4a20996d0b76d9f1bdd8551a233138a032c1321c417a56e1ac3948ae8067"
SUPERSEDED = "8626030f279243f9f3b8c04e07dfc7b11cb2d0d1359b8494f657a68aa1288bc0"
TEXT_SUFFIXES = {
    ".md", ".json", ".txt", ".py", ".ps1", ".yml", ".yaml", ".cs",
    ".cfg", ".toml", ".ini", ".xml", ".r2x", ".csv",
}
LOCAL_QUALIFIERS = (
    "supersed", "erratum", "incorrect", "wrong", "historical metadata",
    "historical sha", "old value", "old sha", "provenance correction",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    global FAILED
    FAILED = True


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot read JSON {path.relative_to(ROOT)}: {exc}")
        return {}


def validate_authority() -> set[str]:
    errata = load_json(ERRATA_PATH)
    if errata.get("authoritative_sha256") != AUTHORITATIVE:
        fail("errata authoritative_sha256 drift")
    if errata.get("superseded_sha256") != SUPERSEDED:
        fail("errata superseded_sha256 drift")
    if errata.get("authority") != "RuntimeEvidence/S1.42AC/20260904T181854Z/INDEX.json":
        fail("errata authority path drift")

    index = load_json(INDEX_PATH)
    entries = [x for x in index.get("files", []) if x.get("name") == "LogOutput.log"]
    if len(entries) != 1 or entries[0].get("sha256") != AUTHORITATIVE:
        fail("RuntimeEvidence INDEX does not expose the authoritative S1.42AC LogOutput.log SHA")
    for analysis in index.get("analysis", []):
        source_sha = analysis.get("stats", {}).get("source_sha256")
        if source_sha and source_sha != AUTHORITATIVE:
            fail(f"embedded runtime analysis source_sha256 drift: {source_sha}")

    allowed = set()
    for entry in errata.get("historical_document_errata", []):
        path = entry.get("path")
        classification = str(entry.get("classification", "")).upper()
        note = str(entry.get("note", "")).lower()
        if not path or not (ROOT / path).is_file():
            fail(f"errata references missing historical document: {path!r}")
            continue
        if "SUPERSEDED" not in classification or "supersed" not in note:
            fail(f"historical errata entry is not explicitly superseded: {path}")
            continue
        allowed.add(path)
    return allowed


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {
            "README", "LICENSE", "Dockerfile", "Makefile"
        }:
            continue
        yield path


def validate_occurrences(explicit_historical_errata: set[str]) -> None:
    occurrences = 0
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if SUPERSEDED not in text:
            continue
        rel = path.relative_to(ROOT).as_posix()
        start = 0
        while True:
            idx = text.find(SUPERSEDED, start)
            if idx < 0:
                break
            occurrences += 1
            window = text[max(0, idx - 700): min(len(text), idx + len(SUPERSEDED) + 700)].lower()
            locally_qualified = any(token in window for token in LOCAL_QUALIFIERS)
            explicitly_mapped = rel in explicit_historical_errata
            if not locally_qualified and not explicitly_mapped:
                fail(
                    f"unqualified superseded S1.42AC raw-log SHA occurrence in {rel}; "
                    "mark it locally as superseded/erratum or register the historical document in the canonical errata"
                )
            start = idx + len(SUPERSEDED)

    if occurrences == 0:
        fail("superseded SHA disappeared entirely; expected preserved historical/erratum provenance")
    else:
        print(f"qualified_superseded_sha_occurrences={occurrences}")


FAILED = False


def main() -> int:
    if not ERRATA_PATH.is_file():
        fail("missing Current/S1.42AC_RUNTIME_SHA_PROVENANCE_ERRATA.json")
        return 1
    if not INDEX_PATH.is_file():
        fail("missing authoritative S1.42AC RuntimeEvidence INDEX")
        return 1
    mapped = validate_authority()
    validate_occurrences(mapped)
    if FAILED:
        return 1
    print("PASS: S1.42AC runtime SHA provenance is repository-wide qualified and authoritative")
    return 0


if __name__ == "__main__":
    sys.exit(main())
