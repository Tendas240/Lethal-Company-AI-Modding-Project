from pathlib import Path
import copy
import json
import re

ROOT = Path(__file__).resolve().parents[1]
AI = "S1.42AI"
R3 = "S1.42AI-DIAG1R3"
MARKER = "<!-- LIVE_STATE: accepted=S1.42AH latest=S1.42AI candidate=S1.42AI runtime_test_outstanding=true -->"


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def dump(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write(rel, text):
    (ROOT / rel).write_text(text.rstrip() + "\n", encoding="utf-8")


state = load("Current/CURRENT_STATE.json")
assert state["active_candidate"]["build_id"] == AI
assert state["latest_built_artifact"]["build_id"] == R3
latest = copy.deepcopy(state["active_candidate"])
latest["status"] = "BUILD_PASS_STATIC_DELTA_VERIFIED_FULL_NORMAL_RUNTIME_ACTIVE_AFTER_DIAG1R3_PASS_NOT_ACCEPTED"
state["latest_built_artifact"] = latest
dump("Current/CURRENT_STATE.json", state)

lineage = load("Current/BUILD_LINEAGE.json")
assert lineage["active_candidate_build_id"] == AI
lineage["latest_built_artifact_id"] = AI
dump("Current/BUILD_LINEAGE.json", lineage)

# Replace live markers first.
for rel in (
    "Knowledge/CURRENT_LIFECYCLE.md",
    "Current/PROJECT_KNOWLEDGE_MAP.md",
    "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md",
    "Current/ARTIFACT_EVIDENCE_INTEGRITY.md",
):
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    text, n = re.subn(r"^<!-- LIVE_STATE:.*?-->$", MARKER, text, count=1, flags=re.M)
    assert n == 1, rel
    write(rel, text)

# Lifecycle: R3 is completed evidence; S1.42AI is both live latest and active.
p = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
text = p.read_text(encoding="utf-8")
text = text.replace("## Latest built artifact / completed diagnostic", "## Completed diagnostic evidence", 1)
text = text.replace("- Latest built artifact: **S1.42AI-DIAG1R3** (completed diagnostic evidence).\n- Active runtime candidate: **S1.42AI**.", "- Completed diagnostic evidence: **S1.42AI-DIAG1R3**.\n- Latest built artifact and active runtime candidate: **S1.42AI**.", 1)
write(p.relative_to(ROOT), text)

# Knowledge-map lifecycle anchor: do not call completed R3 the live latest artifact.
p = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
text = p.read_text(encoding="utf-8")
text = text.replace("Latest built artifact: **S1.42AI-DIAG1R3 — completed diagnostic runtime pass / not gameplay accepted**.", "Completed diagnostic evidence: **S1.42AI-DIAG1R3 — diagnostic runtime pass / not gameplay accepted**.", 1)
text = text.replace("Active full-normal runtime candidate: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — NOT ACCEPTED**.", "Latest built artifact and active full-normal runtime candidate: **S1.42AI — BCMER ShyGuy Interior-Only Event Correction — NOT ACCEPTED**.", 1)
write(p.relative_to(ROOT), text)

# Roadmap and evidence index wording.
p = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
text = p.read_text(encoding="utf-8")
text = text.replace("Accepted gameplay baseline: **S1.42AH**. Latest built artifact: **S1.42AI-DIAG1R3**, now completed diagnostic-pass evidence rather than an active candidate. Its exterior-visibility condition remains explicitly not exercised because no exterior ShyGuy occurred. Active full-normal runtime candidate: **S1.42AI**,", "Accepted gameplay baseline: **S1.42AH**. Completed diagnostic evidence: **S1.42AI-DIAG1R3**, with exterior visibility explicitly not exercised because no exterior ShyGuy occurred. Latest built artifact and active full-normal runtime candidate: **S1.42AI**,")
write(p.relative_to(ROOT), text)

p = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
text = p.read_text(encoding="utf-8")
text = text.replace("## Latest built artifact / completed diagnostic: S1.42AI-DIAG1R3", "## Completed diagnostic evidence: S1.42AI-DIAG1R3", 1)
text = text.replace("## Active full-normal runtime candidate: S1.42AI", "## Latest built artifact / active full-normal runtime candidate: S1.42AI", 1)
write(p.relative_to(ROOT), text)

p = ROOT / "Current/BUILD_LINEAGE.md"
text = p.read_text(encoding="utf-8")
text = text.replace("- **Latest built artifact:** S1.42AI-DIAG1R3 — completed diagnostic runtime pass / not gameplay accepted.\n- **Active candidate:** S1.42AI — full-normal BCMER ShyGuy Interior-Only Event Correction / not accepted.", "- **Completed diagnostic evidence:** S1.42AI-DIAG1R3 — runtime diagnostic pass / not gameplay accepted.\n- **Latest built artifact / active candidate:** S1.42AI — full-normal BCMER ShyGuy Interior-Only Event Correction / not accepted.", 1)
write(p.relative_to(ROOT), text)

print("PASS: normalized live latest/active identity to S1.42AI while retaining R3 as completed evidence")
