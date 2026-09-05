#!/usr/bin/env python3
"""Render protected current navigation from Current/CURRENT_STATE.json."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
MARKER_MD = "<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->"
MARKER_TEXT = "GENERATED — DO NOT MANUALLY EDIT. Update Current/CURRENT_STATE.json and run RepositoryTools/render_current_navigation.py."

def load_state(): return json.loads(STATE_PATH.read_text(encoding="utf-8"))
def status_text(value): return str(value).replace("_", " ")
def opt_line(obj, key, label):
    value=obj.get(key)
    return f"- {label}: {value}\n" if value else ""

def render_readme(s):
    a,l,o=s["accepted_baseline"],s["latest_built_artifact"],s["overhaul"]
    h=s["canonical_navigation"]["handover_preparation_prompt"]
    return f"""{MARKER_MD}
# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for **Lethal Company V81**.

## Fast takeover

Read, in order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/00_CURRENT_STATE.md`
3. `Current/PROJECT_KNOWLEDGE_MAP.md`

Then open only the topic/evidence needed for the user's question. Do not read the entire historical repository by default.

Machine-readable live state: `Current/CURRENT_STATE.json`.

Current-chat handover procedure: `{h}`. When the user requests transfer to a new ChatGPT chat, the active chat must execute that procedure and generate a fresh new-chat prompt from current repository authority.

## Current state

Accepted baseline: **{a['build_id']} — {a['title']}**  
Profile: `{a['profile']}`  
SHA-256: `{a['sha256']}`

Latest built artifact: **{l['build_id']} — {l['title']} — {status_text(l['status'])}**  
SHA-256: `{l['sha256']}`

Active candidate: **none**. Runtime test outstanding: **no**. Build successor armed: **no**.

Exact next action: {s['next_action']}

## Semantic navigation

- Topic router: `Current/PROJECT_KNOWLEDGE_MAP.md` / `.json`
- Chat handover procedure: `{h}`
- Build history: `Current/BUILD_LINEAGE.md` / `.json`
- Authority/history classification: `Current/DOCUMENT_AUTHORITY.md` / `.json`
- Artifact/runtime-evidence integrity: `Current/ARTIFACT_EVIDENCE_INTEGRITY.md` / `.json`
- Deferred work: `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
- Patch safety: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Historical handovers, candidate notes, rejection records and runtime decisions are preserved as evidence, but they do not override the current state/topic authority graph or a later explicit acceptance decision.

## Repository overhaul

Status: **{o['status']}**.  
Verified pre-overhaul recovery repository: `{o['pre_overhaul_backup']}` at frozen source commit `{o['frozen_source_commit']}`.  
Manifest: `{o['backup_manifest']}`.

No local repository clone or local profile build should be required from the user while repository-native artifacts and automation are sufficient.
"""

def render_start(s):
    a,l,c=s["accepted_baseline"],s["latest_built_artifact"],s["controllers"]
    h=s["canonical_navigation"]["handover_preparation_prompt"]
    latest_details=(opt_line(l,"acceptance","acceptance")+opt_line(l,"original_rejection","historical rejection")+opt_line(l,"corrected_analysis","corrected BCMER analysis")).rstrip()
    return f"""======================================================================
CURRENT CANONICAL TAKEOVER — GENERATED FROM Current/CURRENT_STATE.json
======================================================================
{MARKER_TEXT}

Repository: https://github.com/{s['repository']}
Game: {s['game']}
Repository is the Source of Truth.

READ FIRST:
1. Current/00_CURRENT_STATE.md
2. Current/PROJECT_KNOWLEDGE_MAP.md
3. Current/01_HANDOVER_CORE.md

Then route the user's question through Current/PROJECT_KNOWLEDGE_MAP.md and read only the relevant Knowledge topic plus linked evidence/config/code.
Use Current/DOCUMENT_AUTHORITY.md when old files contain stale "current" wording.
Use Current/BUILD_LINEAGE.md for "which build introduced/rejected/accepted this?" questions.

HANDOVER SIGNAL
When the user explicitly requests transfer to a new ChatGPT chat, execute {h}. Verify the then-current main/CI/controllers first and generate a fresh new-chat start prompt from repository authority instead of reusing stale conversation memory.

ACCEPTED BASELINE
- {a['build_id']} — {a['title']}
- status: {status_text(a['status'])}
- profile: {a['profile']}
- SHA-256: {a['sha256']}
- acceptance: {a['acceptance']}

LATEST BUILT ARTIFACT
- {l['build_id']} — {l['title']}
- status: {status_text(l['status'])}
- SHA-256: {l['sha256']}
{latest_details}

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
Whenever a future runtime test is outstanding, the same response that explains the test MUST include the repository-driven Gale replacement/import one-liner when required and the exact build-specific self-contained PowerShell one-line runtime-log uploader. A completed run may still require its build-specific uploader even when no new runtime test is outstanding; do not ask the user to rerun solely because evidence upload is pending.

PERMANENT POLICY ROUTES
- Chat handover: {h}
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
Do not delete or reinterpret history to match current truth. Historical decisions remain evidence. A later explicit decision may supersede a historical lifecycle verdict while preserving the original record and its observations. Current/CURRENT_STATE.json plus the build-specific current decision record determine live status.

REPOSITORY OVERHAUL
Architecture status: {s['overhaul']['status']}
Recovery repository: {s['overhaul']['pre_overhaul_backup']}
Frozen source commit: {s['overhaul']['frozen_source_commit']}

Do not require the user to make a local clone/build while repository-native infrastructure is sufficient.
"""

def render_current(s):
    a,l,c=s["accepted_baseline"],s["latest_built_artifact"],s["controllers"]
    hist=""
    if l.get("original_rejection"):
        hist=f"\nHistorical rejection: `{l['original_rejection']}`  \n"
    corr=""
    if l.get("corrected_analysis"):
        corr=f"Corrected source-path analysis: `{l['corrected_analysis']}`  \n"
    acc=""
    if l.get("acceptance"):
        acc=f"Acceptance: `{l['acceptance']}`  \n"
    return f"""{MARKER_MD}
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** {s['updated']}  
**Game:** {s['game']}

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
{acc}{hist}{corr}
A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **none**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`{c['build_id']}`)
- Guarded build base: accepted {a['build_id']} / `{c['build_base_sha256']}`
- `RuntimeInbox/ACTIVE_BUILD.txt = {c['runtime_active_build']}`

## Exact next action

{s['next_action']}

No new runtime test is pending. A completed run may still require its build-specific PowerShell uploader before evidence ingestion; `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **{s['overhaul']['status']}**.  
Verified recovery repository: `{s['overhaul']['pre_overhaul_backup']}`.  
Frozen source commit: `{s['overhaul']['frozen_source_commit']}`.
"""

def render_handover(s):
    a,l=s["accepted_baseline"],s["latest_built_artifact"]
    h=s["canonical_navigation"]["handover_preparation_prompt"]
    return f"""{MARKER_MD}
# 01 — Handover Core

**Status:** CURRENT TAKEOVER ROUTER  
**Machine state:** `Current/CURRENT_STATE.json`  
**Topic router:** `Current/PROJECT_KNOWLEDGE_MAP.md`  
**Authority registry:** `Current/DOCUMENT_AUTHORITY.md`  
**Current-chat handover procedure:** `{h}`  
**Last-Validated:** {s['updated']}

## Fresh-session procedure

1. Read `Current/00_CURRENT_STATE.md`.
2. Read `Current/PROJECT_KNOWLEDGE_MAP.md`.
3. Route the user's question to the registered semantic topic.
4. Open linked config/code/runtime/history only when needed.
5. Use `Current/BUILD_LINEAGE.md` for build-history questions and `Current/DOCUMENT_AUTHORITY.md` when an older file says "current".

Do not require a local repository clone or local profile build while repository-native artifacts and automation are sufficient.

## Future handover signal

When the user later requests transfer to another ChatGPT chat, execute `{h}`. That procedure verifies the then-current repository/CI/controller state and generates the new chat's start prompt from current authority; do not reuse an old static handover snapshot.

## Current anchors

Accepted: **{a['build_id']} — {a['title']}**, SHA-256 `{a['sha256']}`.  
Latest built: **{l['build_id']} — {l['title']}**, SHA-256 `{l['sha256']}`, status **{status_text(l['status'])}**.  
Active candidate: **none**. Runtime test: **none pending**. Successor: **not armed**.

Exact next action: {s['next_action']}

## Mandatory runtime-test UX

Whenever a future runtime test becomes outstanding, the response that explains what to test must include the repository-driven Gale replacement/import one-liner when required and the exact build-specific one-line PowerShell log uploader in the same response. If a run is already complete but its log is not yet ingested, provide the uploader for the runtime-active build without requiring another test run.

## Historical authority warning

Old final handovers, audits, candidate notes, rejection records, `Current/02_TECHNICAL_BASELINE.md`, and the old progress blocks in `Current/07_FUTURE_ROADMAP_BCMER_INTERIORS.md` are retained history. They do not override the current-state/topic graph or a later explicit acceptance decision. See `Current/DOCUMENT_AUTHORITY.md` and `Current/REPOSITORY_MIGRATION_MANIFEST.md`.

## Recovery

Verified pre-overhaul repository: `{s['overhaul']['pre_overhaul_backup']}`  
Frozen source commit: `{s['overhaul']['frozen_source_commit']}`  
Manifest: `{s['overhaul']['backup_manifest']}`
"""

def generated(s):
    return {"README.md":render_readme(s),"START_HERE_ChatGPT_Masterprompt.txt":render_start(s),"Current/00_CURRENT_STATE.md":render_current(s),"Current/01_HANDOVER_CORE.md":render_handover(s)}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--check",action="store_true"); args=p.parse_args(); s=load_state(); mismatches=[]
    for rel,content in generated(s).items():
        path=ROOT/rel
        if args.check:
            actual=path.read_text(encoding="utf-8") if path.exists() else ""
            if actual!=content: mismatches.append(rel)
        else:
            path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content,encoding="utf-8"); print("rendered",rel)
    if mismatches:
        for rel in mismatches: print("OUT-OF-DATE:",rel)
        return 1
    if args.check: print("PASS: generated current navigation matches Current/CURRENT_STATE.json")
    return 0
if __name__=="__main__": sys.exit(main())
