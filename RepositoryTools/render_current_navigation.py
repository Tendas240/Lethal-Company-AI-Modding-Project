#!/usr/bin/env python3
"""Render compact current navigation from Current/CURRENT_STATE.json.

Use `python RepositoryTools/render_current_navigation.py --check` in CI.
Without --check the script rewrites the generated navigation files.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "Current/CURRENT_STATE.json"


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def render_readme(s: dict) -> str:
    a = s["accepted_baseline"]
    l = s["latest_built_artifact"]
    o = s["overhaul"]
    return f"""# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for **Lethal Company V81**.

## Fast takeover

Read, in order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/PROJECT_KNOWLEDGE_MAP.md`

Then open only the topic/evidence needed for the user's question. Do not read the entire historical repository by default.

Machine-readable live state: `Current/CURRENT_STATE.json`.

## Current state

Accepted baseline: **{a['build_id']} — {a['title']}**  
Profile: `{a['profile']}`  
SHA-256: `{a['sha256']}`

Latest built artifact: **{l['build_id']} — {l['title']} — formally rejected/not promoted**  
SHA-256: `{l['sha256']}`

Active candidate: **none**. Runtime test outstanding: **no**. Build successor armed: **no**.

Exact next action: {s['next_action']}

## Semantic navigation

- Topic router: `Current/PROJECT_KNOWLEDGE_MAP.md` / `.json`
- Build history: `Current/BUILD_LINEAGE.md` / `.json`
- Authority/history classification: `Current/DOCUMENT_AUTHORITY.md` / `.json`
- Artifact/runtime-evidence integrity: `Current/ARTIFACT_EVIDENCE_INTEGRITY.md` / `.json`
- Deferred work: `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
- Patch safety: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Historical handovers, candidate notes and runtime decisions are preserved as evidence, but they do not override the current state/topic authority graph.

## Repository overhaul

Status: **{o['status']}**.  
Verified pre-overhaul recovery repository: `{o['pre_overhaul_backup']}` at frozen source commit `{o['frozen_source_commit']}`.  
Manifest: `{o['backup_manifest']}`.

No local repository clone or local profile build should be required from the user while repository-native artifacts and automation are sufficient.
"""


def render_start(s: dict) -> str:
    a = s["accepted_baseline"]
    l = s["latest_built_artifact"]
    c = s["controllers"]
    return f"""======================================================================
CURRENT CANONICAL TAKEOVER — GENERATED FROM Current/CURRENT_STATE.json
======================================================================

Repository: https://github.com/{s['repository']}
Game: {s['game']}
Repository is the Source of Truth.

READ FIRST:
1. Current/00_CURRENT_STATE.md
2. Current/PROJECT_KNOWLEDGE_MAP.md
3. Current/01_HANDOVER_CORE.md

Then route the user's question through Current/PROJECT_KNOWLEDGE_MAP.md and read only the relevant Knowledge topic plus linked evidence/config/code.
Use Current/DOCUMENT_AUTHORITY.md when old files contain stale "current" wording.
Use Current/BUILD_LINEAGE.md for "which build introduced/rejected this?" questions.

ACCEPTED BASELINE
- {a['build_id']} — {a['title']}
- profile: {a['profile']}
- SHA-256: {a['sha256']}
- acceptance: {a['acceptance']}

LATEST BUILT ARTIFACT
- {l['build_id']} — {l['title']}
- status: FORMALLY REJECTED / NOT PROMOTED
- SHA-256: {l['sha256']}
- corrected BCMER analysis: {l['corrected_analysis']}

CURRENT EXECUTION STATE
- active candidate: NONE
- runtime test outstanding: NO
- successor armed: NO
- BuildSpecs/current.json enabled: {str(c['build_enabled']).lower()}
- build controller id: {c['build_id']}
- RuntimeInbox/ACTIVE_BUILD.txt: {c['runtime_active_build']}

EXACT NEXT ACTION
{s['next_action']}

RUNTIME-TEST UX RULE
Whenever a future runtime test is outstanding, the same response that explains the test MUST include the exact build-specific one-line PowerShell log uploader. There is no uploader to run now because no runtime test is pending.

PERMANENT POLICY ROUTES
- BCMER: Knowledge/BCMER.md
- Interiors/LLL: Knowledge/INTERIORS_AND_LLL.md
- Enemy spawn baseline: Knowledge/ENEMY_SPAWN_BASELINE.md
- Pikmin/enemy compatibility: Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md
- Jetpack: Knowledge/JETPACK.md
- CodeRebirth/item tuning: Knowledge/CODEREBIRTH.md and Knowledge/ITEM_TUNING.md
- Monitor-only errors: Knowledge/MONITOR_ONLY_ERRORS.md
- Black Mesa/Pikmin routing: Knowledge/BLACK_MESA_PIKMIN_ROUTING.md
- Roadmap: Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md
- Patch safety: Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md

HISTORY RULE
Do not delete or reinterpret history to match current truth. Historical decisions remain evidence. Current/109 supersedes only the old BCMER per-event-weight interpretation behind the S1.42AC rejection; S1.42AC remains formally rejected/not promoted until an explicit later decision changes that status.

REPOSITORY OVERHAUL
Architecture status: {s['overhaul']['status']}
Recovery repository: {s['overhaul']['pre_overhaul_backup']}
Frozen source commit: {s['overhaul']['frozen_source_commit']}

Do not require the user to make a local clone/build while repository-native infrastructure is sufficient.
"""


def render_current(s: dict) -> str:
    a = s["accepted_baseline"]
    l = s["latest_built_artifact"]
    c = s["controllers"]
    return f"""# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** {s['updated']}  
**Game:** {s['game']}

## Accepted baseline

**{a['build_id']} — {a['title']} — ACCEPTED FULL NORMAL STACK**

Profile: `{a['profile']}`  
SHA-256: `{a['sha256']}`  
Acceptance: `{a['acceptance']}`  
Runtime evidence: `{a['runtime_evidence']}`

## Latest built artifact

**{l['build_id']} — {l['title']} — FORMALLY REJECTED / NOT PROMOTED**

Profile: `{l['profile']}`  
SHA-256: `{l['sha256']}`  
Original rejection: `{l['original_rejection']}`  
Corrected source-path analysis: `{l['corrected_analysis']}`

The old S1.42AC equality gate misread BCMER's logged values as aggregate EventType weights. `Current/109` proves they are per-event weights normalized by enabled event count. The equal 12.5 scales are therefore the correct static EventType-probability model; this technical correction does not silently promote the rejected artifact.

## Live execution state

- Active candidate: **none**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`{c['build_id']}`)
- Guarded build base: accepted {a['build_id']} / `{c['build_base_sha256']}`
- `RuntimeInbox/ACTIVE_BUILD.txt = {c['runtime_active_build']}`

## Exact next action

{s['next_action']}

No PowerShell uploader is required now because no runtime test is pending.

## Where current truth lives

Use `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **{s['overhaul']['status']}**.  
Verified recovery repository: `{s['overhaul']['pre_overhaul_backup']}`.  
Frozen source commit: `{s['overhaul']['frozen_source_commit']}`.
"""


def render_handover(s: dict) -> str:
    a = s["accepted_baseline"]
    l = s["latest_built_artifact"]
    return f"""# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Last-Validated:** {s['updated']}

## Fresh-session procedure

1. Read `Current/00_CURRENT_STATE.md`.
2. Read `Current/PROJECT_KNOWLEDGE_MAP.md`.
3. Route the user's question to the registered semantic topic.
4. Open linked config/code/runtime/history only when needed.
5. Use `Current/BUILD_LINEAGE.md` for build-history questions and `Current/DOCUMENT_AUTHORITY.md` when an older file says "current".

Do not require a local repository clone or local profile build while repository-native artifacts and automation are sufficient.

## Current anchors

Accepted: **{a['build_id']} — {a['title']}**, SHA-256 `{a['sha256']}`.  
Latest built: **{l['build_id']} — {l['title']}**, SHA-256 `{l['sha256']}`, formally rejected/not promoted.  
Active candidate: **none**. Runtime test: **none pending**. Successor: **not armed**.

Exact next action: {s['next_action']}

## Mandatory runtime-test UX

Whenever a future runtime test becomes outstanding, the response that explains what to test must include the exact build-specific one-line PowerShell log uploader in the same response.

## Historical authority warning

Old final handovers, audits, candidate notes, `Current/02_TECHNICAL_BASELINE.md`, and the old progress blocks in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are retained history. They do not override the new current-state/topic graph. See `Current/DOCUMENT_AUTHORITY.md` and `Current/REPOSITORY_MIGRATION_MANIFEST.md`.

## Recovery

Verified pre-overhaul repository: `{s['overhaul']['pre_overhaul_backup']}`  
Frozen source commit: `{s['overhaul']['frozen_source_commit']}`  
Manifest: `{s['overhaul']['backup_manifest']}`
"""


def generated(s: dict) -> dict[str, str]:
    return {
        "README.md": render_readme(s),
        "START_HERE_ChatGPT_Masterprompt.txt": render_start(s),
        "Current/00_CURRENT_STATE.md": render_current(s),
        "Current/01_HANDOVER_CORE.md": render_handover(s),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    state = load_state()
    mismatches = []
    for rel, content in generated(state).items():
        p = ROOT / rel
        if args.check:
            actual = p.read_text(encoding="utf-8") if p.exists() else ""
            if actual != content:
                mismatches.append(rel)
        else:
            p.write_text(content, encoding="utf-8")
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
