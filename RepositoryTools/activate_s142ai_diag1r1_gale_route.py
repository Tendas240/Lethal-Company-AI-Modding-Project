#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
text = path.read_text(encoding="utf-8")
anchor = "Use `AnalysisEvidence/S1.42AI-DIAG1R1/MINIMAL_GUARD_CONTRACT.md` for the exact guard boundary and `Current/146_S1.42AI-DIAG1R1_BUILD_CANDIDATE_OWNER_TYPE_RESOLUTION_REPAIR.md` for the ready-to-test commands.\n"
section = """

## Canonical Gale workflow

Import the active R1 candidate only through `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`, using the canonical helper revision `2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof`. The candidate record supplies the repository-driven one-line launcher together with the exact R1 runtime-log uploader; these commands are paired and must not be substituted by an older Gale helper.
"""
if "RuntimeTools/ReplaceActiveGaleProfileV24.ps1" in text or "2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof" in text:
    raise RuntimeError("CURRENT_LIFECYCLE already contains a partial/previous Gale v2.4 route; refusing ambiguous patch")
if text.count(anchor) != 1:
    raise RuntimeError(f"Expected exactly one R1 runtime-contract anchor, found {text.count(anchor)}")
text = text.replace(anchor, anchor + section, 1)
path.write_text(text, encoding="utf-8")
print("PASS: staged canonical Gale v2.4 lifecycle route")
