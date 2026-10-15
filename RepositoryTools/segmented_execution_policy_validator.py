#!/usr/bin/env python3
"""Validate the project-wide ChatGPT segmented-execution contract."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = "Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md"
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


def require_fragments(rel: str, fragments: list[str]) -> None:
    path = ROOT / rel
    if not path.is_file():
        fail(f"missing required file: {rel}")
        return
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    for fragment in fragments:
        if fragment.lower() not in text:
            fail(f"{rel} missing segmented-execution contract fragment: {fragment}")


def main() -> int:
    policy_path = ROOT / POLICY
    if not policy_path.is_file():
        fail(f"missing canonical segmented execution policy: {POLICY}")
        policy_text = ""
    else:
        policy_text = policy_path.read_text(encoding="utf-8", errors="replace")

    policy_required = [
        "CURRENT / CANONICAL PROJECT-WIDE CHATGPT EXECUTION POLICY",
        "For every user request that requires ChatGPT to perform project work",
        "at most two consecutive bounded segments",
        "within an existing authorization only",
        "Never cross an authorization boundary automatically",
        "Before entering the second segment, reassess scope",
        "approximately four minutes",
        "six project execution segments",
        "does not automatically create",
        "At the end of each assistant response",
        "Completed:",
        "Findings:",
        "Remaining:",
        "Next segment:",
        "Mandatory dual visualizations",
        "Weiter – Segment N+1:",
        "Message Delivery timed out",
        "connection interrupted. waiting for the complete answer",
        "Do not rely on ChatGPT Memory",
        "Every generated new-chat start prompt must explicitly instruct the new chat to read and follow this policy",
    ]
    lowered = policy_text.lower()
    for fragment in policy_required:
        if fragment.lower() not in lowered:
            fail(f"segmented execution policy missing required contract fragment: {fragment}")

    state = load_json("Current/CURRENT_STATE.json")
    navigation = state.get("canonical_navigation", {})
    if navigation.get("segmented_execution_policy") != POLICY:
        fail("CURRENT_STATE canonical_navigation.segmented_execution_policy does not point to canonical policy")

    bootstrap_files = [
        "README.md",
        "START_HERE_ChatGPT_Masterprompt.txt",
        "Current/00_CURRENT_STATE.md",
        "Current/01_HANDOVER_CORE.md",
    ]
    for rel in bootstrap_files:
        require_fragments(rel, [POLICY])

    require_fragments(
        "START_HERE_ChatGPT_Masterprompt.txt",
        [
            "SEGMENTED EXECUTION RULE",
            "up to two bounded segments may run in the same assistant response",
            "then STOP and wait for the user's next message",
            "Segment 1/1",
        ],
    )
    require_fragments(
        "Current/01_HANDOVER_CORE.md",
        [
            "at most two segments may run in one assistant response",
            "explicit user continuation",
        ],
    )

    require_fragments(
        "Current/PROJECT_KNOWLEDGE_MAP.md",
        [
            POLICY,
            "chatgpt_segmented_execution",
            "Before performing project work",
        ],
    )

    authority = load_json("Current/DOCUMENT_AUTHORITY.json")
    entries = [x for x in authority.get("canonical", []) if isinstance(x, dict) and x.get("path") == POLICY]
    if len(entries) != 1:
        fail(f"expected exactly one canonical authority entry for segmented policy, found {len(entries)}")
    else:
        entry = entries[0]
        if entry.get("authority") != "CURRENT_CHATGPT_EXECUTION_POLICY":
            fail("segmented policy authority class is not CURRENT_CHATGPT_EXECUTION_POLICY")
        required = {"chatgpt_segmented_execution", "project_task_segmentation", "continuation_gate"}
        if not required.issubset(set(entry.get("canonical_for", []))):
            fail("segmented policy authority entry is missing required canonical_for claims")

    require_fragments(
        "Current/DOCUMENT_AUTHORITY.md",
        [POLICY, "bounded segment", "explicit user continuation"],
    )

    require_fragments(
        "Current/HANDOVER_PREPARATION_PROMPT.md",
        [
            POLICY,
            "Mandatory segmented execution",
            "Up to two already-authorized handover preparation segments",
            "stop and wait for the user's explicit continuation signal",
            "instruct the new chat to read `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` before performing project work",
        ],
    )

    # Reject legacy unconditional one-segment-per-turn instructions in the
    # current bootstrap/handover authorities, while retaining a hard response stop.
    legacy_statements = {
        "START_HERE_ChatGPT_Masterprompt.txt": [
            "Execute only the current segment, report Completed",
        ],
        "Current/01_HANDOVER_CORE.md": [
            "one bounded segment per assistant turn",
        ],
        "Current/HANDOVER_PREPARATION_PROMPT.md": [
            "execute one bounded segment, report Completed",
        ],
    }
    for rel, phrases in legacy_statements.items():
        path = ROOT / rel
        if path.is_file():
            content = path.read_text(encoding="utf-8", errors="replace").lower()
            for phrase in phrases:
                if phrase.lower() in content:
                    fail(f"stale unconditional stop rule remains in {rel}: {phrase}")

    print("Segmented ChatGPT execution policy validation")
    print(f"errors={len(ERRORS)}")
    for message in ERRORS:
        print(f"ERROR: {message}")
    if ERRORS:
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
