#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "Current/CURRENT_STATE.json"
ACTIVE = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
FINDING = ROOT / "Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md"
EVIDENCE_DIR = "RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/"
EVIDENCE_INDEX = EVIDENCE_DIR + "INDEX.json"
LOG_SHA = "4f3dae931364cefc4b297c8c316502e96d32b27431467a5607ce69ed6d6e69ef"


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"required replacement anchor missing: {label}")
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, replacement: str, label: str) -> str:
    pattern = re.escape(start) + r".*?(?=" + re.escape(end) + r")"
    out, n = re.subn(pattern, replacement.rstrip() + "\n\n", text, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError(f"required section replacement failed: {label} ({n})")
    return out


# Fail closed against an unexpected live state.
s = json.loads(STATE.read_text(encoding="utf-8"))
assert s["accepted_baseline"]["build_id"] == "S1.42AK"
assert s["active_candidate"] is None
assert s["runtime_test_outstanding"] is True
scope = s["selected_scope"]
assert scope["scope_id"] == "UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY"
diag = scope["diagnostic_revision"]
assert diag["build_id"] == "S1.42AK-BMGHDIAG1"
assert diag["status"] == "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED"
assert s["controllers"]["runtime_active_build"] == "S1.42AK-BMGHDIAG1"
assert ACTIVE.read_text(encoding="utf-8").strip() == "S1.42AK-BMGHDIAG1"
assert (ROOT / EVIDENCE_INDEX).is_file(), "ingested BMGHDIAG1 runtime index missing"
idx = json.loads((ROOT / EVIDENCE_INDEX).read_text(encoding="utf-8"))
assert idx["build_id"] == "S1.42AK-BMGHDIAG1"
assert idx["files"][0]["sha256"] == LOG_SHA

s["runtime_test_outstanding"] = False
scope["status"] = "PHASE_C3F17_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REPAIR_ANALYSIS_REQUIRED"
scope["finding"] = (
    "The first exact published S1.42AK-BMGHDIAG1 runtime attempt is ingested at "
    f"{EVIDENCE_DIR}. The diagnostic loaded but failed closed before arming with "
    "[BMGHDIAG1] REFUSED TO ARM because it could not hash the loaded Assembly-CSharp.dll, so normal dungeon selection was preserved. "
    "The normal Black Mesa LLL pool nevertheless proves Greenhouse / GreenhouseFlow viable at effective rarity 100 under accepted S1.42AB normalization; "
    "the actual selected interior was Decrepit store. The user's main-entrance and two-fire-exit traversals therefore qualify Decrepit store only, not Greenhouse. "
    "Black Mesa x Greenhouse remains NOT_YET_PROVEN. S1.42AK, Black Mesa Dawn/native ownership, Greenhouse availability, accepted normalization and the B3 matrix remain unchanged."
)
scope["analysis_contract"] = (
    "Preserve the ingested BMGHDIAG1 refusal evidence and do not repeat the same published bytes. Repository-native analysis must determine why "
    "ValidateAssemblyHash/ResolveObservationContract could not hash the loaded Assembly-CSharp.dll despite the static installed-V81 hash contract, then define the minimal fail-closed successor diagnostic revision if justified. "
    "Do not alter accepted S1.42AK, S1.42AB InteriorWeightNormalization, Black Mesa ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions or the separate Black-Mesa/Pikmin routing scope. "
    "No gameplay run is authorized until a corrected diagnostic is separately reviewed, published and armed."
)
next_action = (
    "Analyze the ingested S1.42AK-BMGHDIAG1 startup refusal repository-native: trace ValidateAssemblyHash and ResolveObservationContract against the exact installed-V81/runtime assembly-loading evidence, "
    "determine the minimal provenance-safe fix, and prepare a separately versioned successor diagnostic only if the root cause is established. Do not rerun the refused BMGHDIAG1 bytes and do not arm gameplay yet."
)
scope["next_action"] = next_action
scope["diagnostic_runtime_finding"] = "Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md"
diag["status"] = "RUNTIME_FAILED_DIAGNOSTIC_REPAIR_REQUIRED_NOT_ACCEPTED"
diag["runtime_validation_status"] = "RUNTIME_EVIDENCE_INGESTED_DIAGNOSTIC_REFUSED_BEFORE_ARMING_QUALIFICATION_INCONCLUSIVE_NOT_ACCEPTED"
diag["runtime_evidence"] = EVIDENCE_DIR
diag["runtime_index"] = EVIDENCE_INDEX
diag["runtime_log_sha256"] = LOG_SHA
diag["runtime_decision"] = "Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md"
s["next_action"] = next_action
s["controllers"]["runtime_active_build"] = "S1.42AK"
STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
ACTIVE.write_text("S1.42AK\n", encoding="utf-8")

FINDING.write_text("""# S1.42AK-BMGHDIAG1 Runtime Inconclusive — Diagnostic Startup Refusal

**Date:** 2026-09-23  
**Status:** DIAGNOSTIC RUNTIME EVIDENCE INGESTED / STARTUP REFUSAL / BLACK MESA x GREENHOUSE QUALIFICATION INCONCLUSIVE / NOT ACCEPTANCE AUTHORITY  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Diagnostic:** S1.42AK-BMGHDIAG1 — failed diagnostic evidence only, never a gameplay base  
**Runtime evidence:** `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`  
**Runtime log SHA-256:** `4f3dae931364cefc4b297c8c316502e96d32b27431467a5607ce69ed6d6e69ef`  
**Runtime log size:** 1,780,500 bytes

## Runtime result

The exact published BMGHDIAG1 plugin loaded, but its startup contract failed closed before installing/arming the targeted selection and entrance-observation behavior:

`[BMGHDIAG1] REFUSED TO ARM; normal behavior preserved: System.InvalidOperationException: Cannot hash loaded assembly: Assembly-CSharp.dll`

The recorded stack reaches `S142AKBMGHDiag1.Plugin.ValidateAssemblyHash`, `ResolveObservationContract`, and `Awake`. Because the diagnostic deliberately preserves normal behavior on refusal, this run contains no valid BMGHDIAG1 deterministic Greenhouse-selection claim and cannot satisfy the activation contract in `Current/170_S1.42AK_BMGHDIAG1_RUNTIME_ACTIVATION.md`.

## What the run still proves

Normal LethalLevelLoader matching on Black Mesa returned `Greenhouse (100)` as viable. The accepted S1.42AB normalizer then retained Greenhouse at final effective rarity `100` in the Black Mesa viable pool. This is direct runtime availability/weight evidence for Greenhouse on Black Mesa; it is not generation/traversal proof for the pair.

Because BMGHDIAG1 had already refused to arm, normal selection chose **Decrepit store**. The user reported successful normal main-entrance entry/exit and successful in/out traversal through two distinct fire exits. Those observations are useful Decrepit-store-on-Black-Mesa traversal evidence but cannot be attributed to Greenhouse.

## Qualification decision

**Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.** The run is inconclusive because the diagnostic refused before target selection, not because Greenhouse exhibited a demonstrated generation or traversal incompatibility.

Do not repeat the exact BMGHDIAG1 bytes: the same startup guard is already known to refuse. Return runtime-evidence attribution to accepted S1.42AK and clear the outstanding-runtime-test flag while the diagnostic itself is repaired.

## Exact next action

Analyze the diagnostic startup failure repository-native. Trace the `ValidateAssemblyHash` / `ResolveObservationContract` implementation against the exact installed-V81 and runtime assembly-loading evidence and establish why the loaded `Assembly-CSharp.dll` could not be hashed. Only after that root cause is established may a minimal, separately versioned, fail-closed successor diagnostic be designed, reviewed, published and armed for another Black Mesa x Greenhouse run.

The runtime evidence does **not** justify silently removing the assembly provenance gate, broadening the hook contract, or substituting an unverified assembly identity mechanism.

## Preserved boundaries

- accepted/latest gameplay baseline remains exact S1.42AK;
- accepted S1.42AB InteriorWeightNormalization remains unchanged;
- Black Mesa remains Dawn/native-owned and is not duplicate-registered;
- Greenhouse availability remains unchanged;
- the B3 30x53 matrix remains unchanged by this evidence-sync decision;
- Shatteredrooms x Experimentation/Embrion remain untouched;
- Black Mesa/Pikmin routing remains a separate scope;
- no universal interior override or gameplay successor is armed.
""", encoding="utf-8")

# Canonical lifecycle topic.
p = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
t = p.read_text(encoding="utf-8")
t = must_replace(t,
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->",
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->",
    "lifecycle live state")
t = must_replace(t,
    "`Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`  ",
    "`Current/168_S1.42AK_UNIVERSAL_INTERIOR_PHASE_C1_EXISTING_RUNTIME_COMPATIBILITY_TRIAGE.md`, `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`, `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`  ",
    "lifecycle evidence list")
old_start = "## Active targeted runtime diagnostic — Black Mesa x Greenhouse"
old_end = "## Live execution state"
replacement = """## BMGHDIAG1 runtime attempt — inconclusive diagnostic refusal

The first exact published `S1.42AK-BMGHDIAG1` Black Mesa run is ingested at `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`. The plugin loaded but emitted `[BMGHDIAG1] REFUSED TO ARM` because `ValidateAssemblyHash` could not hash the loaded `Assembly-CSharp.dll`; its fail-closed contract preserved normal dungeon selection.

The same run nevertheless proves that normal LethalLevelLoader matching on Black Mesa includes `Greenhouse (100)` and that accepted S1.42AB normalization leaves Greenhouse at effective rarity 100. The actual normal selection was `Decrepit store`. The user's successful main-entrance and two distinct fire-exit in/out traversals therefore apply to Decrepit store, not Greenhouse.

Black Mesa x Greenhouse remains `NOT_YET_PROVEN`; this is diagnostic-tool failure evidence, not a demonstrated Greenhouse incompatibility. Decision authority: `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`. Do not rerun the same BMGHDIAG1 bytes. No diagnostic runtime target is currently armed while the assembly-hash failure is analyzed."""
t = replace_section(t, old_start, old_end, replacement, "lifecycle BMG section")
# Replace the live-state bullets up to the next heading.
t = replace_section(t, "## Live execution state", "## Exact next project action", """## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK**.
- Active gameplay candidate: **none**.
- Active diagnostic runtime target: **none**.
- Runtime test outstanding: **no**.
- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F17 BMGHDIAG1 refusal root-cause/fix analysis**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.
- No gameplay successor or universal override is armed.""", "lifecycle live execution")
t = replace_section(t, "## Exact next project action", "## Permanent Gale workflow", """## Exact next project action

Analyze the ingested BMGHDIAG1 startup refusal repository-native: trace `ValidateAssemblyHash` and `ResolveObservationContract` against the exact installed-V81/runtime assembly-loading evidence, determine the minimal provenance-safe fix, and prepare a separately versioned successor diagnostic only if the root cause is established. Do not rerun the refused BMGHDIAG1 bytes and do not arm gameplay yet.""", "lifecycle next action")
t = must_replace(t,
    "The active BMGHDIAG1 target uses its fail-closed direct-diagnostic path over exact accepted/latest S1.42AK; no diagnostic-parent hop is required.",
    "No diagnostic is currently runtime-armed. Any later corrected BMGH diagnostic must be separately published and armed through the same fail-closed repository authority chain before another gameplay run.",
    "lifecycle Gale note")
p.write_text(t, encoding="utf-8")

# Interior/LLL topic status.
p = ROOT / "Knowledge/INTERIORS_AND_LLL.md"
t = p.read_text(encoding="utf-8")
t = replace_section(t,
    "## Active C3F17 targeted Black Mesa x Greenhouse runtime qualification",
    "## Selected universal viability / equal availability investigation",
    """## C3F17 Black Mesa x Greenhouse qualification status

The first exact published `S1.42AK-BMGHDIAG1` runtime attempt is ingested at `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/` but is **not** a successful pair qualification. The diagnostic plugin refused before arming because its installed-V81 observation provenance gate could not hash the loaded `Assembly-CSharp.dll`; fail-closed behavior preserved normal dungeon selection.

The normal Black Mesa LLL matching report in that same run includes `Greenhouse (100)`, and accepted S1.42AB normalization retains `Greenhouse(100)` in the final effective viable pool. This directly proves current Black Mesa availability and equal effective weighting for Greenhouse. It does not prove Greenhouse generation, entrance topology or player traversal because normal selection chose `Decrepit store` after the diagnostic refusal.

The user's successful main-entrance and two distinct fire-exit round trips therefore qualify Decrepit store traversal only. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`. Canonical decision: `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`.

No runtime test is currently armed. The next step is source/root-cause analysis of `ValidateAssemblyHash` / `ResolveObservationContract` and, only if justified, a separately versioned minimal diagnostic repair. Do not rerun the refused BMGHDIAG1 bytes, change Greenhouse availability, duplicate-register Black Mesa, alter S1.42AB normalization, modify the B3 matrix, or open the separate Black-Mesa/Pikmin routing scope.""",
    "interiors C3F17 section")
p.write_text(t, encoding="utf-8")

# Human Knowledge Map lifecycle anchor.
p = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
t = p.read_text(encoding="utf-8")
t = must_replace(t,
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->",
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->",
    "knowledge map live state")
t = must_replace(t,
    "No gameplay candidate or successor build is armed. Exact published `S1.42AK-BMGHDIAG1` is the active diagnostic-only runtime target for the bounded Black Mesa x Greenhouse C3F17 qualification; `BuildSpecs/current.json` remains disabled and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG1`. The B3 matrix remains unchanged until this runtime evidence is ingested and interpreted.",
    "No gameplay candidate or successor build is armed. The first exact `S1.42AK-BMGHDIAG1` Black Mesa run is now ingested, but the diagnostic refused before arming because it could not hash the loaded `Assembly-CSharp.dll`; normal selection then chose Decrepit store. The same normal LLL pool proves Greenhouse viable on Black Mesa at final effective rarity 100, but Black Mesa x Greenhouse remains `NOT_YET_PROVEN` because no targeted generation/traversal occurred. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no runtime test is currently armed, and the next action is repository-native diagnostic root-cause/fix analysis. The B3 matrix remains unchanged.",
    "knowledge map lifecycle anchor")
p.write_text(t, encoding="utf-8")

# Artifact/evidence machine index: move BMGHDIAG1 from pending to completed failed-diagnostic evidence.
p = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.json"
a = json.loads(p.read_text(encoding="utf-8"))
pending = a.get("pending_profiles", [])
matches = [x for x in pending if x.get("build_id") == "S1.42AK-BMGHDIAG1"]
if len(matches) != 1:
    raise RuntimeError(f"expected one pending BMGHDIAG1 entry, found {len(matches)}")
entry = matches[0]
a["pending_profiles"] = [x for x in pending if x is not entry]
entry["role"] = "RUNTIME_FAILED_DIAGNOSTIC_REPAIR_REQUIRED"
entry["runtime_evidence"] = EVIDENCE_DIR
entry["runtime_index"] = EVIDENCE_INDEX
entry["runtime_log_sha256"] = LOG_SHA
entry["decision"] = "Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md"
entry["note"] = "Published Black Mesa x Greenhouse diagnostic refused before arming because the loaded Assembly-CSharp.dll could not be hashed. Normal Black Mesa LLL evidence still proves Greenhouse viable/effective-100; actual selection was Decrepit store. Repair analysis required; not a gameplay base."
entry.pop("runtime_evidence_required", None)
entry.pop("partial_runtime_evidence_present", None)
a.setdefault("profiles", []).append(entry)

def rewrite_strings(v):
    if isinstance(v, list):
        return [rewrite_strings(x) for x in v]
    if isinstance(v, dict):
        return {k: rewrite_strings(x) for k, x in v.items()}
    if isinstance(v, str) and v == "S1.42AK-BMGHDIAG1 is repository-published at SHA-256 7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90 with readable ProfileSources/FILE_INDEX evidence and is tracked only as an active pending diagnostic until an explicit runtime decision.":
        return "S1.42AK-BMGHDIAG1 runtime evidence is RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/ with raw LogOutput.log SHA-256 4f3dae931364cefc4b297c8c316502e96d32b27431467a5607ce69ed6d6e69ef; Current/171 records the fail-closed startup refusal and required diagnostic repair analysis."
    return v
a = rewrite_strings(a)
a["updated"] = "2026-09-23"
p.write_text(json.dumps(a, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Artifact/evidence human mirror.
p = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
t = p.read_text(encoding="utf-8")
t = must_replace(t,
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->",
    "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->",
    "artifact live state")
old = """## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.
- **S1.42AK-BMGHDIAG1** — active runtime diagnostic pending for Black Mesa x Greenhouse; profile `Profiles/LC V1 S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic.r2z`, SHA-256 `7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90`, readable snapshot `ProfileSources/S1.42AK-BMGHDIAG1/`.

`S1.42AK-BMGHDIAG1` is the active diagnostic runtime target; there is no active gameplay candidate. It remains pending/unaccepted until an explicit runtime decision.
"""
new = """## Completed failed diagnostic evidence: S1.42AK-BMGHDIAG1

Profile: `Profiles/LC V1 S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic.r2z`  
SHA-256: `7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90`  
Readable snapshot: `ProfileSources/S1.42AK-BMGHDIAG1/`  
Runtime evidence: `RuntimeEvidence/S1.42AK-BMGHDIAG1/20260923T165840Z/`  
Runtime log SHA-256: `4f3dae931364cefc4b297c8c316502e96d32b27431467a5607ce69ed6d6e69ef`  
Decision: `Current/171_S1.42AK_BMGHDIAG1_RUNTIME_INCONCLUSIVE_DIAGNOSTIC_REFUSAL.md`

The diagnostic refused before arming because the loaded `Assembly-CSharp.dll` could not be hashed. Normal Black Mesa LLL evidence still proves Greenhouse viable at effective rarity 100, but actual selection was Decrepit store; Black Mesa x Greenhouse therefore remains unqualified and the diagnostic requires repair analysis. It is not runtime-active and is never a gameplay base.

## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.
"""
t = must_replace(t, old, new, "artifact BMG status")
p.write_text(t, encoding="utf-8")

# Regenerate protected current-navigation mirrors from machine state.
subprocess.check_call([sys.executable, str(ROOT / "RepositoryTools/render_current_navigation.py")])
subprocess.check_call([sys.executable, str(ROOT / "RepositoryTools/render_current_navigation.py"), "--check"])
subprocess.check_call([sys.executable, str(ROOT / "RepositoryTools/current_state_semantic_validator.py")])

# Narrow postconditions.
s2 = json.loads(STATE.read_text(encoding="utf-8"))
assert s2["runtime_test_outstanding"] is False
assert s2["controllers"]["runtime_active_build"] == "S1.42AK"
assert s2["selected_scope"]["diagnostic_revision"]["runtime_log_sha256"] == LOG_SHA
assert ACTIVE.read_text(encoding="utf-8").strip() == "S1.42AK"
print("PASS: C3F17 BMGHDIAG1 inconclusive runtime handover sync prepared")
