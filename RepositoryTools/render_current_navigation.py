#!/usr/bin/env python3
"""Render protected current navigation from Current/CURRENT_STATE.json."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
MARKER_MD = "<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->"
MARKER_TEXT = "GENERATED — DO NOT MANUALLY EDIT. Update Current/CURRENT_STATE.json and run RepositoryTools/render_current_navigation.py."


def load_state():
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def status_text(value):
    return str(value).replace("_", " ")


def policy_path(s):
    return s["canonical_navigation"]["segmented_execution_policy"]


def active_candidate_id(s):
    candidate = s.get("active_candidate")
    return candidate.get("build_id", "none") if isinstance(candidate, dict) else "none"


def yes_no(value):
    return "yes" if bool(value) else "no"


def runtime_note(s):
    if s.get("runtime_test_outstanding"):
        return (
            f"A runtime test is pending for {active_candidate_id(s)}. "
            "`RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build."
        )
    return (
        "No new runtime test is pending. A completed run may still require its build-specific PowerShell uploader before evidence ingestion; "
        "`RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build."
    )


def render_readme(s):
    h = s["canonical_navigation"]["handover_preparation_prompt"]
    p = policy_path(s)
    return f"""{MARKER_MD}
# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and repository-native build/handover workspace for **{s['game']}**.

## Fast takeover

Read, in order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `{p}`
3. `Current/CURRENT_STATE.json`
4. `Current/PROJECT_KNOWLEDGE_MAP.md`

Then route the request through the Knowledge Map and open only the canonical topic/evidence needed for that task. Do not read historical handovers or the full repository by default.

Human-readable live-state mirror: `Current/00_CURRENT_STATE.md`.

Current-chat handover procedure: `{h}`. Every project task, including handover work, remains continuation-gated by `{p}`.

No local repository clone or local profile build should be required from the user while repository-native infrastructure is sufficient.
"""


def render_start(s):
    h = s["canonical_navigation"]["handover_preparation_prompt"]
    p = policy_path(s)
    return f"""======================================================================
CURRENT CANONICAL TAKEOVER — GENERATED FROM Current/CURRENT_STATE.json
======================================================================
{MARKER_TEXT}

Repository: https://github.com/{s['repository']}
Game: {s['game']}
Repository is the Source of Truth.

READ FIRST:
1. {p}
2. Current/CURRENT_STATE.json
3. Current/PROJECT_KNOWLEDGE_MAP.md

SEGMENTED EXECUTION RULE
For every project request that requires work, follow {p}. Execute only the current segment, report Completed / Findings / Remaining / Next segment, then STOP and wait for the user's explicit continuation signal before beginning the next non-final segment. A genuinely short atomic task may be Segment 1/1. Never split an atomic change so the repository/controllers are knowingly left inconsistent.

ROUTING RULE
Use Current/CURRENT_STATE.json for volatile live project state. Route the user's question through Current/PROJECT_KNOWLEDGE_MAP.md and read only the registered canonical topic plus linked evidence/config/code needed for the task. Human-readable live-state mirror: Current/00_CURRENT_STATE.md; it is optional when the machine state already answers the task. Use Current/DOCUMENT_AUTHORITY.md only when current-vs-history precedence is actually in question. Use Current/BUILD_LINEAGE.md only for build-history questions.

HANDOVER SIGNAL
When the user explicitly requests transfer to a new ChatGPT chat, execute {h} under the same segmented-execution policy. Verify then-current main/CI/controllers and generate a fresh compact new-chat prompt from repository authority instead of reusing stale conversation memory.

RUNTIME-TEST UX RULE
Whenever a future runtime test is outstanding, the response that explains the test MUST include the repository-driven Gale replacement/import one-liner when required and the exact build-specific self-contained PowerShell one-line runtime-log uploader. A completed run may still require its build-specific uploader even when no new runtime test is outstanding; do not ask the user to rerun solely because evidence upload is pending.

HISTORY RULE
Historical decisions remain evidence but never override Current/CURRENT_STATE.json or the canonical topic graph merely because an old file says "current".

Do not require the user to make a local clone/build while repository-native infrastructure is sufficient.
"""


def render_current(s):
    a, l, c = s["accepted_baseline"], s["latest_built_artifact"], s["controllers"]
    p = policy_path(s)
    hist = f"\nHistorical rejection: `{l['original_rejection']}`  \n" if l.get("original_rejection") else ""
    corr = f"Corrected source-path analysis: `{l['corrected_analysis']}`  \n" if l.get("corrected_analysis") else ""
    acc = f"Acceptance: `{l['acceptance']}`  \n" if l.get("acceptance") else ""
    cand = f"Candidate record: `{l['candidate_record']}`  \n" if l.get("candidate_record") else ""
    return f"""{MARKER_MD}
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** {s['updated']}  
**Game:** {s['game']}

## Project execution policy

Every ChatGPT chat performing project work must follow `{p}`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**{a['build_id']} — {a['title']} — {status_text(a['status'])}**

Profile: `{a['profile']}`  
SHA-256: `{a['sha256']}`  
Acceptance: `{a['acceptance']}`  
Runtime evidence: `{a['runtime_evidence']}`

## Latest built artifact

**{l['build_id']} — {l['title']} — {status_text(l['status'])}**

Profile: `{l['profile']}`  
SHA-256: `{l['sha256']}`  
{acc}{cand}{hist}{corr}
A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **{active_candidate_id(s)}**
- Runtime test outstanding: **{yes_no(s.get('runtime_test_outstanding'))}**
- Successor armed: **{yes_no(c.get('build_enabled'))}**
- `BuildSpecs/current.json`: {'enabled' if c['build_enabled'] else 'disabled'} (`{c['build_id']}`)
- Guarded build base: `{c['build_base_profile']}` / `{c['build_base_sha256']}`
- `RuntimeInbox/ACTIVE_BUILD.txt = {c['runtime_active_build']}`

## Exact next action

{s['next_action']}

{runtime_note(s)}

## Where current truth lives

Use `{p}` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **{s['overhaul']['status']}**.  
Verified recovery repository: `{s['overhaul']['pre_overhaul_backup']}`.  
Frozen source commit: `{s['overhaul']['frozen_source_commit']}`.
"""


def render_handover(s):
    h = s["canonical_navigation"]["handover_preparation_prompt"]
    p = policy_path(s)
    return f"""{MARKER_MD}
# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Project execution policy:** `{p}`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Current-chat handover procedure:** `{h}`  
**Last-Validated:** {s['updated']}

## Fresh-session procedure

1. Read `{p}` and follow it for every project task.
2. Read `Current/CURRENT_STATE.json`.
3. Read `Current/PROJECT_KNOWLEDGE_MAP.md`.
4. Route the request to the registered canonical topic and open only linked evidence/config/code that is actually needed.

For non-trivial work, execute one bounded segment per assistant turn, report the checkpoint, stop, and wait for explicit user continuation before the next segment. Short atomic work may be Segment 1/1; never create a knowingly inconsistent checkpoint.

Use `Current/DOCUMENT_AUTHORITY.md` only when old/current wording conflicts, and `Current/BUILD_LINEAGE.md` only for build-history questions. Human-readable state is available in `Current/00_CURRENT_STATE.md` but does not need to be reread when `Current/CURRENT_STATE.json` already answers the task.

## Future handover signal

When the user later requests transfer to another ChatGPT chat, execute `{h}` under `{p}`. Verify then-current repository/CI/controller reality and generate the compact new-chat prompt from current authority; do not reuse an old static handover snapshot.

## Runtime-test UX

Whenever a runtime test is outstanding, the test instructions must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific one-line PowerShell log uploader. If a completed run still needs ingestion, provide the uploader for the runtime-active build without requiring another test run.

Do not require a local repository clone or local profile build while repository-native infrastructure is sufficient.
"""


def generated(s):
    return {
        "README.md": render_readme(s),
        "START_HERE_ChatGPT_Masterprompt.txt": render_start(s),
        "Current/00_CURRENT_STATE.md": render_current(s),
        "Current/01_HANDOVER_CORE.md": render_handover(s),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    s = load_state()
    mismatches = []
    for rel, content in generated(s).items():
        path = ROOT / rel
        if args.check:
            actual = path.read_text(encoding="utf-8") if path.exists() else ""
            if actual != content:
                mismatches.append(rel)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print("rendered", rel)
    if mismatches:
        for rel in mismatches:
            print("OUT-OF-DATE:", rel)
        return 1
    if args.check:
        print("PASS: generated current navigation matches Current/CURRENT_STATE.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
