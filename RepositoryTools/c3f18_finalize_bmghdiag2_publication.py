#!/usr/bin/env python3
"""One-shot C3F18 canonicalizer for the exact-byte BMGHDIAG2 publication checkpoint.

The exact reviewed bytes are already materialized on the dedicated publication branch.
This transformer advances only the branch-local lifecycle/publication state, keeps every
live build/runtime controller inactive, and leaves main integration/runtime activation for
later bounded checkpoints.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
LIFECYCLE_PATH = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
MAP_PATH = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
PLAN_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md"
SOURCE_GATE_PATH = ROOT / "AnalysisTools/validate_s142ak_bmghdiag2_source.py"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
PUBLICATION_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
BUILD_RESULT_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/BUILD_RESULT.json"
PROFILE_PATH = ROOT / "Profiles/LC V1 S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic.r2z"
PROFILE_SOURCES = ROOT / "ProfileSources/S1.42AK-BMGHDIAG2"
FILE_INDEX_PATH = PROFILE_SOURCES / "FILE_INDEX.json"
HIDDEN_CONFIG_PATH = PROFILE_SOURCES / "BepInEx/config/.LCMaxSoundsFix.cfg"

BUILD_ID = "S1.42AK-BMGHDIAG2"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PROFILE_SHA = "56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2"
DLL_SHA = "51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
ARTIFACT_ZIP_SHA = "265ebfae87ad3c48a6dbb57d0b3dce81a4c4d1c2e4872357f970354974da7a62"
HIDDEN_CONFIG_SHA = "0093bae709cec57fd3f4f3bc5af22231b16944a666768e7ecf879430693f73a2"
REVIEW_RUN = 35990294162
REVIEW_ARTIFACT_ID = 10803912824
PUBLICATION_RUN = 35994918640
PUBLICATION_BRANCH = "c3f18-bmghdiag2-exact-publication"
PUBLISHED_PROFILE_COMMIT = "0482b9e24521a1490529e4d81a8a397b61413f11"
OLD_STATUS = "PHASE_C3F18_BMGHDIAG2_INACTIVE_REVIEW_BUILD_PASS_PUBLICATION_NEXT"
NEW_STATUS = "PHASE_C3F18_BMGHDIAG2_EXACT_PUBLICATION_PASS_INTEGRATION_NEXT"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected exactly one replacement target, found {count}")
    return text.replace(old, new, 1)


def replace_section(text: str, start_heading: str, end_heading: str, replacement: str, label: str) -> str:
    start = text.find(start_heading)
    require(start >= 0, f"{label}: missing start heading {start_heading!r}")
    end = text.find(end_heading, start + len(start_heading))
    require(end >= 0, f"{label}: missing end heading {end_heading!r}")
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
require(state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(state["accepted_baseline"]["sha256"] == BASE_SHA, "Accepted baseline SHA drift")
require(state["latest_built_artifact"]["build_id"] == "S1.42AK", "Latest normal artifact drift")
require(state["active_candidate"] is None, "Unexpected active candidate")
require(state["runtime_test_outstanding"] is False, "Runtime unexpectedly authorized")
require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Build controller drift")
require(ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip() == "S1.42AK", "Runtime pointer drift")

selected = state["selected_scope"]
require(selected["scope_id"] == "UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY", "Selected scope drift")
require(selected["status"] == OLD_STATUS, "Unexpected pre-publication lifecycle state")
review = selected.get("diagnostic_successor_review")
require(isinstance(review, dict) and review.get("build_id") == BUILD_ID, "BMGHDIAG2 review record missing")
require(review.get("published") is False and review.get("runtime_armed") is False, "Unexpected review publication/runtime state")
require(review.get("profile_sha256") == PROFILE_SHA and review.get("diagnostic_dll_sha256") == DLL_SHA, "Review identity drift")

require(PROFILE_PATH.is_file() and sha_file(PROFILE_PATH) == PROFILE_SHA, "Published profile identity mismatch")
require(PUBLICATION_PATH.is_file(), "Publication verification missing")
publication = PUBLICATION_PATH.read_text(encoding="utf-8")
for marker in (
    "EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH",
    f"**Review workflow run:** `{REVIEW_RUN}`",
    f"**Actions artifact ID:** `{REVIEW_ARTIFACT_ID}`",
    f"**Artifact ZIP SHA-256:** `{ARTIFACT_ZIP_SHA}`",
    f"published profile SHA-256: `{PROFILE_SHA}`",
    f"published `S142AKBMGHDiag2.dll` SHA-256: `{DLL_SHA}`",
    "zero package changes, zero config changes",
    "not merged to `main`",
):
    require(marker in publication, "Publication evidence drift or missing marker: " + marker)

require(BUILD_RESULT_PATH.is_file(), "Published BUILD_RESULT.json missing")
build_result = json.loads(BUILD_RESULT_PATH.read_text(encoding="utf-8"))
require(build_result["build_id"] == BUILD_ID, "BUILD_RESULT build id drift")
require(build_result["base_sha256"] == BASE_SHA and build_result["output_sha256"] == PROFILE_SHA, "BUILD_RESULT identity drift")
require(build_result["zip_members"] == 337 and build_result["snapshot"]["entries"] == 337, "BUILD_RESULT archive/snapshot count drift")
require(build_result["mod_state_changes"] == [] and build_result["mod_additions"] == [] and build_result["mod_removals"] == [], "BUILD_RESULT package drift")

require(FILE_INDEX_PATH.is_file(), "Reconstructed FILE_INDEX.json missing")
index = json.loads(FILE_INDEX_PATH.read_text(encoding="utf-8"))
require(len(index) == 337, "Reconstructed FILE_INDEX row count drift")
hidden_rows = [row for row in index if row.get("path") == "BepInEx/config/.LCMaxSoundsFix.cfg"]
require(len(hidden_rows) == 1, "Hidden LCMaxSoundsFix index row missing or duplicated")
require(hidden_rows[0].get("index") == 1 and hidden_rows[0].get("size") == 621 and hidden_rows[0].get("sha256") == HIDDEN_CONFIG_SHA and hidden_rows[0].get("text_snapshot") is True, "Hidden LCMaxSoundsFix index identity drift")
require(HIDDEN_CONFIG_PATH.is_file() and sha_file(HIDDEN_CONFIG_PATH) == HIDDEN_CONFIG_SHA, "Reconstructed hidden LCMaxSoundsFix snapshot identity drift")

state["updated"] = "2026-09-24"
selected["status"] = NEW_STATUS
selected["finding"] = (
    "S1.42AK-BMGHDIAG2 has passed source/static review, the separate inactive review build, and exact-byte publication on the dedicated working branch. "
    f"Publication workflow run {PUBLICATION_RUN} materialized the exact reviewed profile from review run {REVIEW_RUN} / artifact {REVIEW_ARTIFACT_ID} at commit {PUBLISHED_PROFILE_COMMIT}, preserving profile SHA-256 {PROFILE_SHA} and diagnostic DLL SHA-256 {DLL_SHA}. "
    "The 337-member archive contract was rechecked, ProfileSources was reconstructed from the reviewed .r2z with repository snapshot semantics, the 337-row FILE_INDEX remained data-identical, and the hidden BepInEx/config/.LCMaxSoundsFix.cfg snapshot is present at index 1 with its reviewed size/hash. "
    f"LLL remains {LLL_SHA}, the accepted normalizer remains {NORMALIZER_SHA}, and package/config drift is zero. The publication is not yet integrated into main and remains not runtime-armed/not accepted. Black Mesa x Greenhouse remains NOT_YET_PROVEN; S1.42AK, Black Mesa Dawn/native ownership, Greenhouse availability, accepted normalization and the B3 matrix remain unchanged."
)
selected["analysis_contract"] = (
    "Treat S1.42AK-BMGHDIAG2 as exact-byte published on the dedicated working branch from the pinned reviewed artifact, but not yet integrated into main, not runtime-armed and not accepted. "
    "The next bounded checkpoint is publication integration: open/review the working-branch PR, require exact-head CI to pass, and merge only the exact branch state into main while BuildSpecs/current.json remains disabled, RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK, active_candidate remains null and runtime_test_outstanding remains false. "
    "Only after main integration may a later separate atomic runtime-activation step arm these exact published bytes. Preserve S1.42AB InteriorWeightNormalization, Black Mesa ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions and the separate Black-Mesa/Pikmin routing scope."
)
next_action = (
    f"Integrate the exact-byte S1.42AK-BMGHDIAG2 publication from branch {PUBLICATION_BRANCH} via PR and exact-head CI, preserving profile SHA-256 {PROFILE_SHA}, diagnostic DLL SHA-256 {DLL_SHA}, the reconstructed 337-row ProfileSources snapshot and publication evidence. "
    "Keep BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false throughout integration. Do not Gale-import or arm gameplay/runtime; runtime activation remains a later separate atomic checkpoint after main integration."
)
selected["next_action"] = next_action
review.update({
    "status": "EXACT_BYTES_PUBLISHED_ON_WORKING_BRANCH_NOT_MAIN_INTEGRATED_NOT_ARMED_NOT_ACCEPTED",
    "profile": "Profiles/LC V1 S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic.r2z",
    "profile_sources": "ProfileSources/S1.42AK-BMGHDIAG2/",
    "file_index": "ProfileSources/S1.42AK-BMGHDIAG2/FILE_INDEX.json",
    "build_result": "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/BUILD_RESULT.json",
    "publication_evidence": "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md",
    "publication_branch": PUBLICATION_BRANCH,
    "publication_workflow_run": PUBLICATION_RUN,
    "published_profile_commit": PUBLISHED_PROFILE_COMMIT,
    "published": True,
    "main_integrated": False,
    "runtime_armed": False,
})
state["next_action"] = next_action
STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

plan = PLAN_PATH.read_text(encoding="utf-8")
plan = replace_once(
    plan,
    "**Status:** SOURCE STATIC PASS / INACTIVE REVIEW BUILD PASS / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  ",
    "**Status:** SOURCE STATIC PASS / INACTIVE REVIEW BUILD PASS / EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / NOT MAIN-INTEGRATED / NOT ARMED / NOT ACCEPTED  ",
    "plan publication status",
)
plan = replace_section(
    plan,
    "## Publication boundary",
    "## Runtime boundary",
    f"""## Exact-byte publication checkpoint

The exact reviewed Actions artifact has now been materialized without rebuilding. Publication workflow run `{PUBLICATION_RUN}` on `{PUBLICATION_BRANCH}` produced commit `{PUBLISHED_PROFILE_COMMIT}` and persisted `BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`.

Publication re-confirmed:

- review run `{REVIEW_RUN}` / artifact `{REVIEW_ARTIFACT_ID}` / artifact ZIP SHA-256 `{ARTIFACT_ZIP_SHA}`;
- exact published profile SHA-256 `{PROFILE_SHA}`;
- exact published diagnostic DLL SHA-256 `{DLL_SHA}`;
- 337 archive members and the exact one-DLL plus `export.r2x` identity-only delta;
- zero package/config changes;
- LLL SHA-256 `{LLL_SHA}` and accepted normalizer SHA-256 `{NORMALIZER_SHA}` unchanged;
- readable `ProfileSources/S1.42AK-BMGHDIAG2/` reconstructed from the exact reviewed `.r2z` using repository snapshot semantics;
- reconstructed `FILE_INDEX.json` data-identical to the reviewed 337-row index;
- hidden `BepInEx/config/.LCMaxSoundsFix.cfg` present at index 1, 621 bytes, SHA-256 `{HIDDEN_CONFIG_SHA}`.

These exact bytes are published only on the dedicated working branch at this checkpoint. They are not yet integrated into `main`, not Gale-imported, not runtime-armed and not accepted.

## Integration boundary

The next bounded action is PR/exact-head-CI/main integration of the exact working-branch publication. All live controllers must remain inactive throughout integration. Runtime activation remains a later separate atomic lifecycle step after the publication is visible on `main`.
""",
    "plan publication section",
)
PLAN_PATH.write_text(plan, encoding="utf-8")

source_gate = SOURCE_GATE_PATH.read_text(encoding="utf-8")
source_gate = replace_once(
    source_gate,
    'require("NOT PUBLISHED" in plan and "NOT ARMED" in plan, "Human plan publication/runtime boundary drift")',
    'require("EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH" in plan and "NOT ARMED" in plan, "Human plan publication/runtime boundary drift")',
    "source gate publication boundary",
)
source_gate = replace_once(
    source_gate,
    '"status": "SOURCE_STATIC_CONTRACT_PASS_NOT_PUBLISHED_NOT_ARMED",',
    '"status": "SOURCE_STATIC_CONTRACT_PASS_PUBLISHED_WORKING_BRANCH_NOT_ARMED",',
    "source gate report status",
)
source_gate = replace_once(
    source_gate,
    '"qualification": "Source/compile/pure-policy validation only. A separate inactive review-build spec may exist, but this source gate never builds, publishes, arms lifecycle or authorizes runtime."',
    '"qualification": "Source/compile/pure-policy validation only. Exact reviewed bytes may already be branch-published, but this source gate itself never builds, publishes, arms lifecycle or authorizes runtime."',
    "source gate qualification",
)
SOURCE_GATE_PATH.write_text(source_gate, encoding="utf-8")

lifecycle = LIFECYCLE_PATH.read_text(encoding="utf-8")
lifecycle = replace_section(
    lifecycle,
    "## BMGHDIAG2 inactive review build — pass",
    "## Live execution state",
    f"""## BMGHDIAG2 exact-byte publication — working-branch pass

C3F18's provenance-safe `S1.42AK-BMGHDIAG2` successor has passed source/static review and the separate inactive review build. The exact reviewed bytes from run `{REVIEW_RUN}` / artifact `{REVIEW_ARTIFACT_ID}` have now also been published byte-for-byte on the dedicated working branch by publication run `{PUBLICATION_RUN}` at commit `{PUBLISHED_PROFILE_COMMIT}`. No profile or diagnostic DLL rebuild occurred.

The published profile SHA-256 is `{PROFILE_SHA}` and the diagnostic DLL SHA-256 is `{DLL_SHA}`. The 337-member archive contract remains exact: one new BMGHDIAG2 DLL, `export.r2x` identity metadata only, zero package/config changes, LLL `{LLL_SHA}`, and accepted normalizer `{NORMALIZER_SHA}`. `ProfileSources/S1.42AK-BMGHDIAG2/` was reconstructed from the exact reviewed `.r2z`; its 337-row FILE_INDEX matches review evidence and includes the previously artifact-upload-omitted hidden `.LCMaxSoundsFix.cfg` at index 1 with the reviewed 621-byte / `{HIDDEN_CONFIG_SHA}` identity. Publication evidence: `BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`.

BMGHDIAG2 is **exact-byte published on the working branch, but not yet integrated into main, not runtime-armed and not accepted**. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.
""",
    "lifecycle publication section",
)
lifecycle = replace_section(
    lifecycle,
    "## Live execution state",
    "## Exact next project action",
    """## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built/published normal artifact: **S1.42AK**.
- Active gameplay candidate: **none**.
- Active diagnostic runtime target: **none**.
- Runtime test outstanding: **no**.
- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F18 BMGHDIAG2 exact-byte publication passed on working branch; PR/CI/main integration next**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.
- No gameplay successor or universal override is armed.
""",
    "lifecycle live state",
)
lifecycle = replace_section(
    lifecycle,
    "## Exact next project action",
    "## Permanent Gale workflow",
    f"""## Exact next project action

{next_action}
""",
    "lifecycle next action",
)
lifecycle = replace_once(
    lifecycle,
    "No diagnostic is currently runtime-armed. BMGHDIAG2 remains source/static-only until a later review build, publication, and explicit atomic activation step; only that later activation may authorize another gameplay run.",
    "No diagnostic is currently runtime-armed. BMGHDIAG2 is exact-byte published on the dedicated working branch but remains non-runtime until publication integration and a later explicit atomic activation step; only that later activation may authorize another gameplay run.",
    "lifecycle Gale boundary",
)
LIFECYCLE_PATH.write_text(lifecycle, encoding="utf-8")

km = MAP_PATH.read_text(encoding="utf-8")
km = replace_section(
    km,
    "**Universal Interior Viability / Equal Availability is the selected scope.**",
    "## Authority rule",
    f"""**Universal Interior Viability / Equal Availability is the selected scope.** Phases A through C2 remain complete with the fixed 30×53 matrix unchanged at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`. The first exact `S1.42AK-BMGHDIAG1` Black Mesa run remains ingested as fail-closed diagnostic refusal evidence; Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

C3F18's separately versioned `S1.42AK-BMGHDIAG2` provenance repair has passed source/static review, a separate inactive review build, and exact-byte publication on the dedicated working branch. Publication run `{PUBLICATION_RUN}` materialized only review run `{REVIEW_RUN}` / artifact `{REVIEW_ARTIFACT_ID}` bytes at commit `{PUBLISHED_PROFILE_COMMIT}`: profile SHA-256 `{PROFILE_SHA}`, diagnostic DLL SHA-256 `{DLL_SHA}`, exact 337-member archive delta, zero package/config changes, unchanged LLL/normalizer, and a reconstructed 337-row readable ProfileSources snapshot including hidden `.LCMaxSoundsFix.cfg`. BMGHDIAG2 is **not yet integrated into main and not runtime-armed**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no active candidate exists and no runtime test is outstanding. The next action is PR/exact-head-CI/main integration of these exact publication bytes; Gale import/gameplay remains a later separate activation checkpoint. The B3 matrix and permanent ownership/scope boundaries remain unchanged.
""",
    "knowledge map publication state",
)
MAP_PATH.write_text(km, encoding="utf-8")

print(json.dumps({
    "status": NEW_STATUS,
    "publication_run": PUBLICATION_RUN,
    "published_profile_commit": PUBLISHED_PROFILE_COMMIT,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "published_on_working_branch": True,
    "main_integrated": False,
    "runtime_armed": False,
}, indent=2))
