#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
text = path.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one target, found {count}")
    text = text.replace(old, new, 1)

replace_once(
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->",
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->",
    "live marker",
)
replace_once("**Last-Validated:** 2026-09-23", "**Last-Validated:** 2026-09-24", "validation date")
replace_once(
    "There is no active gameplay candidate or armed successor build. Exact published `S1.42AK-BMGHDIAG1` is the active diagnostic-only runtime target and one runtime test is outstanding. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG1`; `BuildSpecs/current.json` remains disabled.",
    "There is no active gameplay candidate or gameplay successor. Exact reviewed/main-integrated `S1.42AK-BMGHDIAG2` is the active diagnostic-only runtime target and one bounded runtime test is outstanding. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG2`; `BuildSpecs/current.json` remains disabled; accepted/latest normal baseline remains S1.42AK.",
    "current position",
)
replace_once(
    "**Universal Interior Viability / Equal Availability — SELECTED / PHASE C3F17 TARGETED RUNTIME QUALIFICATION OUTSTANDING.**",
    "**Universal Interior Viability / Equal Availability — SELECTED / PHASE C3F18 BMGHDIAG2 TARGETED RUNTIME QUALIFICATION OUTSTANDING.**",
    "selected scope heading",
)
replace_once(
    "Phases A through C3F17 static analysis preserve the authoritative 30x53 B3 matrix while narrowing Black Mesa x Greenhouse to a targeted runtime proof boundary. `S1.42AK-BMGHDIAG1` is armed only for that pair; no universal override or gameplay successor is armed.",
    "Phases A through C3F18 preserve the authoritative 30x53 B3 matrix while narrowing Black Mesa x Greenhouse to a targeted runtime proof boundary. BMGHDIAG1 remains failed startup-refusal evidence; exact `S1.42AK-BMGHDIAG2` is armed only for that pair. No universal override or gameplay successor is armed, and the matrix remains unchanged until runtime evidence is ingested and decided.",
    "selected scope paragraph",
)
path.write_text(text, encoding="utf-8")
print("PASS: roadmap reflects active BMGHDIAG2 diagnostic without scope expansion")
