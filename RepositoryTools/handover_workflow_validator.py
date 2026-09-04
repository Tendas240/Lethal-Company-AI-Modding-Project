#!/usr/bin/env python3
"""Validate the persistent current-chat -> new-chat handover workflow."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOVER = "Current/HANDOVER_PREPARATION_PROMPT.md"
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load_json(rel: str) -> dict:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing JSON: {rel}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {rel}: {exc}")
        return {}


def main() -> int:
    handover_path = ROOT / HANDOVER
    if not handover_path.is_file():
        fail(f"missing canonical handover prompt: {HANDOVER}")
        prompt = ""
    else:
        prompt = handover_path.read_text(encoding="utf-8", errors="replace")

    state = load_json("Current/CURRENT_STATE.json")
    navigation = state.get("canonical_navigation", {})
    if navigation.get("handover_preparation_prompt") != HANDOVER:
        fail("CURRENT_STATE canonical_navigation.handover_preparation_prompt does not point to canonical handover prompt")

    for rel in ("README.md", "START_HERE_ChatGPT_Masterprompt.txt", "Current/01_HANDOVER_CORE.md"):
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing bootstrap file: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if HANDOVER not in text:
            fail(f"bootstrap file does not expose canonical handover prompt: {rel}")

    km = load_json("Current/PROJECT_KNOWLEDGE_MAP.json")
    handover_topics = [t for t in km.get("topics", []) if t.get("id") == "chat_handover"]
    if len(handover_topics) != 1:
        fail(f"expected exactly one chat_handover topic, found {len(handover_topics)}")
    elif handover_topics[0].get("canonical") != HANDOVER:
        fail("chat_handover topic does not route to canonical handover prompt")

    km_human = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
    if not km_human.is_file():
        fail("missing human Project Knowledge Map")
    else:
        text = km_human.read_text(encoding="utf-8", errors="replace")
        if "chat_handover" not in text or HANDOVER not in text:
            fail("human Project Knowledge Map does not expose chat_handover route")

    authority = load_json("Current/DOCUMENT_AUTHORITY.json")
    authority_entries = [x for x in authority.get("canonical", []) if x.get("path") == HANDOVER]
    if len(authority_entries) != 1:
        fail(f"expected exactly one canonical authority entry for handover prompt, found {len(authority_entries)}")
    else:
        entry = authority_entries[0]
        if entry.get("authority") != "CURRENT_HANDOVER_WORKFLOW":
            fail("handover prompt authority class is not CURRENT_HANDOVER_WORKFLOW")
        canonical_for = set(entry.get("canonical_for", []))
        required = {"chat_handover_preparation", "fresh_new_chat_prompt_generation"}
        if not required.issubset(canonical_for):
            fail("handover prompt authority entry is missing required canonical_for claims")

    cases = load_json("RepositoryTools/answerability_cases.json")
    route_cases = [c for c in cases.get("cases", []) if c.get("id") == "chat-handover"]
    if len(route_cases) != 1:
        fail(f"expected exactly one chat-handover routing regression case, found {len(route_cases)}")
    else:
        case = route_cases[0]
        if case.get("expected_topic") != "chat_handover" or case.get("expected_canonical") != HANDOVER:
            fail("chat-handover routing regression case targets the wrong topic/canonical source")

    required_prompt_fragments = [
        "PART 1 — HANDOVER COMPLETION",
        "PART 2 — READY-TO-COPY START PROMPT FOR THE NEW CHAT",
        "Current/CURRENT_STATE.json",
        "Current/PROJECT_KNOWLEDGE_MAP.md",
        "Current/INTEGRITY_ERRATA_REGISTRY.json",
        "Knowledge/BUILD_AND_RUNTIME_PIPELINE.md",
        "exact build-specific self-contained PowerShell one-line runtime-log uploader",
        "completed runtime log",
        "runtime-active/evidence-attribution",
        "full-repository audit by default",
        "when the user later signals another handover",
    ]
    lowered = prompt.lower()
    for fragment in required_prompt_fragments:
        if fragment.lower() not in lowered:
            fail(f"handover prompt missing required contract fragment: {fragment}")

    if "hard-coding the current accepted build" not in lowered:
        fail("handover prompt does not explicitly prohibit hard-coded current-state snapshots")

    print("Persistent ChatGPT handover workflow validation")
    print(f"errors={len(ERRORS)}")
    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
