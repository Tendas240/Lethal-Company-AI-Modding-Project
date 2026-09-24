#!/usr/bin/env python3
"""Canonicalize the completed C3F18 BMGHDIAG2 PR/main integration without arming runtime."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
LIFECYCLE_PATH = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
MAP_PATH = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
PLAN_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md"
SOURCE_GATE_PATH = ROOT / "AnalysisTools/validate_s142ak_bmghdiag2_source.py"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
PROFILE_PATH = ROOT / "Profiles/LC V1 S1.42AK-BMGHDIAG2 Black Mesa Greenhouse Diagnostic.r2z"
INDEX_PATH = ROOT / "ProfileSources/S1.42AK-BMGHDIAG2/FILE_INDEX.json"
PUBLICATION_PATH = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
INTEGRATION_MD = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/MAIN_INTEGRATION_CHECKPOINT.md"
INTEGRATION_JSON = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/MAIN_INTEGRATION_CHECKPOINT.json"

BUILD_ID = "S1.42AK-BMGHDIAG2"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PROFILE_SHA = "56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2"
DLL_SHA = "51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
PR = 144
PR_HEAD = "984feb61d9a23296ec111f377639c090cf4f952b"
MAIN_MERGE = "1dc18d5a37b5560d282174e11460672b508382ba"
KA_RUN = 35996531577
SOURCE_RUN = 35996531589
ARCHIVE_RUN = 35996531593
PUBLICATION_RUN = 35994918640
REVIEW_RUN = 35990294162
REVIEW_ARTIFACT = 10803912824
OLD_STATUS = "PHASE_C3F18_BMGHDIAG2_EXACT_PUBLICATION_PASS_INTEGRATION_NEXT"
NEW_STATUS = "PHASE_C3F18_BMGHDIAG2_MAIN_INTEGRATION_PASS_RUNTIME_ACTIVATION_NEXT"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected one target, found {count}")
    return text.replace(old, new, 1)


def replace_section(text: str, start_heading: str, end_heading: str, replacement: str, label: str) -> str:
    start = text.find(start_heading)
    require(start >= 0, f"{label}: missing start heading {start_heading!r}")
    end = text.find(end_heading, start + len(start_heading))
    require(end >= 0, f"{label}: missing end heading {end_heading!r}")
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


require(subprocess.run(["git", "merge-base", "--is-ancestor", MAIN_MERGE, "HEAD"], cwd=ROOT).returncode == 0,
        "Expected PR #144 main merge commit is not an ancestor of HEAD")
state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
current = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
require(state["accepted_baseline"]["build_id"] == "S1.42AK" and state["accepted_baseline"]["sha256"] == BASE_SHA, "Accepted baseline drift")
require(state["latest_built_artifact"]["build_id"] == "S1.42AK", "Latest normal artifact drift")
require(state["active_candidate"] is None and state["runtime_test_outstanding"] is False, "Runtime lifecycle unexpectedly armed")
require(current["enabled"] is False and current["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Build controller drift")
require(ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip() == "S1.42AK", "Runtime pointer drift")
selected = state["selected_scope"]
require(selected["status"] == OLD_STATUS, "Unexpected pre-integration lifecycle status")
review = selected["diagnostic_successor_review"]
require(review["build_id"] == BUILD_ID and review["published"] is True and review["main_integrated"] is False and review["runtime_armed"] is False,
        "Unexpected pre-integration BMGHDIAG2 record")
require(PROFILE_PATH.is_file() and sha_file(PROFILE_PATH) == PROFILE_SHA, "Main-integrated profile SHA drift")
require(PUBLICATION_PATH.is_file(), "Publication evidence missing on main")
index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
require(len(index) == 337, "ProfileSources FILE_INDEX row-count drift")
dll_rows = [r for r in index if r.get("path") == "BepInEx/plugins/S142AKBMGHDiag2/S142AKBMGHDiag2.dll"]
require(len(dll_rows) == 1 and dll_rows[0].get("sha256") == DLL_SHA, "Diagnostic DLL index identity drift")

state["updated"] = "2026-09-24"
selected["status"] = NEW_STATUS
selected["finding"] = (
    f"S1.42AK-BMGHDIAG2 exact reviewed bytes are now integrated into main by PR #{PR}, exact head {PR_HEAD}, merge commit {MAIN_MERGE}. "
    f"Exact-head CI passed Knowledge Architecture run {KA_RUN}, source/pure-static run {SOURCE_RUN}, and publication-aware archive run {ARCHIVE_RUN}; the archive gate used published-validation mode and skipped both rebuild and artifact upload. "
    f"The main-integrated profile remains SHA-256 {PROFILE_SHA}, diagnostic DLL SHA-256 {DLL_SHA}, with the same 337-member archive/index contract, zero package/config drift, LLL {LLL_SHA}, and accepted normalizer {NORMALIZER_SHA}. "
    "All live controllers remain inactive: BuildSpecs/current.json is disabled, RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK, active_candidate is null and runtime_test_outstanding is false. Black Mesa x Greenhouse remains NOT_YET_PROVEN until a later explicit diagnostic runtime run."
)
selected["analysis_contract"] = (
    "Treat S1.42AK-BMGHDIAG2 as exact-byte published and integrated into main, but not runtime-armed and not accepted. "
    f"Any runtime activation must target only profile SHA-256 {PROFILE_SHA} / diagnostic DLL SHA-256 {DLL_SHA} directly over accepted S1.42AK and must be a separate atomic lifecycle/controller transition. "
    "Until that later step, keep BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false. Preserve S1.42AB InteriorWeightNormalization, Black Mesa ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions and the separate Black-Mesa/Pikmin routing scope."
)
next_action = (
    f"Prepare a separate atomic runtime-activation checkpoint for the exact main-integrated S1.42AK-BMGHDIAG2 profile SHA-256 {PROFILE_SHA} / diagnostic DLL SHA-256 {DLL_SHA}. "
    "That later activation may point RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK-BMGHDIAG2 and set runtime_test_outstanding=true only while preserving accepted/latest normal baseline S1.42AK and keeping BuildSpecs/current.json disabled. "
    "Do not change gameplay/config/package bytes. The activation response must provide the repository-derived Gale import command and exact build-specific one-line PowerShell runtime-log uploader."
)
selected["next_action"] = next_action
review.update({
    "status": "EXACT_BYTES_MAIN_INTEGRATED_NOT_ARMED_NOT_ACCEPTED",
    "integration_pr": PR,
    "integration_pr_head": PR_HEAD,
    "main_integration_commit": MAIN_MERGE,
    "integration_knowledge_architecture_run": KA_RUN,
    "integration_source_static_run": SOURCE_RUN,
    "integration_archive_gate_run": ARCHIVE_RUN,
    "integration_checkpoint": "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/MAIN_INTEGRATION_CHECKPOINT.md",
    "main_integrated": True,
    "runtime_armed": False,
})
state["next_action"] = next_action
STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

checkpoint = {
    "status": "MAIN_INTEGRATION_PASS_NOT_RUNTIME_ARMED_NOT_ACCEPTED",
    "build_id": BUILD_ID,
    "integration_pr": PR,
    "integration_pr_head": PR_HEAD,
    "main_merge_commit": MAIN_MERGE,
    "knowledge_architecture_run": KA_RUN,
    "source_static_run": SOURCE_RUN,
    "published_archive_gate_run": ARCHIVE_RUN,
    "review_run": REVIEW_RUN,
    "review_artifact_id": REVIEW_ARTIFACT,
    "publication_run": PUBLICATION_RUN,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "archive_members_verified": 337,
    "rebuild_during_integration": False,
    "artifact_upload_during_integration": False,
    "runtime_armed": False,
    "runtime_test_outstanding": False,
}
INTEGRATION_JSON.write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")
INTEGRATION_MD.write_text(f"""# S1.42AK-BMGHDIAG2 main-integration checkpoint

**Status:** PASS / EXACT REVIEWED BYTES ON MAIN / NOT RUNTIME ARMED / NOT ACCEPTED
**Date:** 2026-09-24
**Integration PR:** #{PR}
**Exact PR head:** `{PR_HEAD}`
**Main merge commit:** `{MAIN_MERGE}`

## Exact-head CI

- Knowledge Architecture: run `{KA_RUN}` — PASS;
- BMGHDIAG2 source/pure-static gate: run `{SOURCE_RUN}` — PASS;
- BMGHDIAG2 publication-aware archive gate: run `{ARCHIVE_RUN}` — PASS.

The archive gate detected published-validation mode. It skipped both `profile_builder.py` and Actions artifact upload, then validated the already-published exact bytes and readable snapshot.

## Main-integrated identities

- profile SHA-256: `{PROFILE_SHA}`;
- diagnostic DLL SHA-256: `{DLL_SHA}`;
- archive/index members: 337;
- LethalLevelLoader 1.7.12 DLL SHA-256: `{LLL_SHA}`;
- accepted S1.42AB normalizer SHA-256: `{NORMALIZER_SHA}`;
- package/config drift: zero.

## Lifecycle boundary

This checkpoint integrates publication only. S1.42AK remains the accepted/latest normal baseline. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`, `active_candidate` remains null and `runtime_test_outstanding` remains false. BMGHDIAG2 is not Gale-imported, not runtime-armed and not accepted.

The next permitted action is a separate atomic runtime-activation checkpoint for these exact main-integrated bytes.
""", encoding="utf-8")

plan = PLAN_PATH.read_text(encoding="utf-8")
plan = replace_once(
    plan,
    "**Status:** SOURCE STATIC PASS / INACTIVE REVIEW BUILD PASS / EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / NOT MAIN-INTEGRATED / NOT ARMED / NOT ACCEPTED  ",
    "**Status:** SOURCE STATIC PASS / INACTIVE REVIEW BUILD PASS / EXACT REVIEWED BYTES MAIN-INTEGRATED / NOT ARMED / NOT ACCEPTED",
    "plan status",
)
plan = replace_section(
    plan,
    "## Integration boundary",
    "## Runtime boundary",
    f"""## Main-integration checkpoint

PR #{PR} exact head `{PR_HEAD}` merged the exact-byte publication to `main` at `{MAIN_MERGE}` after all required exact-head gates passed:

- Knowledge Architecture run `{KA_RUN}`;
- BMGHDIAG2 source/pure-static run `{SOURCE_RUN}`;
- publication-aware archive-delta run `{ARCHIVE_RUN}`.

The archive gate ran in published-validation mode and skipped both rebuild and artifact upload. The exact main profile/DLL hashes remain `{PROFILE_SHA}` / `{DLL_SHA}`, with 337 indexed archive members, zero package/config drift, unchanged LLL/normalizer and all live controllers inactive.

BMGHDIAG2 is now repository-published on `main`, but is still not Gale-imported, not runtime-armed and not accepted. Runtime activation is the next separately bounded atomic checkpoint.
""",
    "plan integration section",
)
PLAN_PATH.write_text(plan, encoding="utf-8")

source_gate = SOURCE_GATE_PATH.read_text(encoding="utf-8")
source_gate = replace_once(
    source_gate,
    'require("EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH" in plan and "NOT ARMED" in plan, "Human plan publication/runtime boundary drift")',
    'require("EXACT REVIEWED BYTES" in plan and "NOT ARMED" in plan, "Human plan publication/runtime boundary drift")',
    "source gate plan boundary",
)
source_gate = replace_once(source_gate, '"status": "SOURCE_STATIC_CONTRACT_PASS_PUBLISHED_WORKING_BRANCH_NOT_ARMED",', '"status": "SOURCE_STATIC_CONTRACT_PASS_PUBLISHED_NOT_ARMED",', "source status")
source_gate = replace_once(
    source_gate,
    '"qualification": "Source/compile/pure-policy validation only. Exact reviewed bytes may already be branch-published, but this source gate itself never builds, publishes, arms lifecycle or authorizes runtime."',
    '"qualification": "Source/compile/pure-policy validation only. Exact reviewed bytes may already be repository-published, but this source gate itself never builds, publishes, arms lifecycle or authorizes runtime."',
    "source qualification",
)
SOURCE_GATE_PATH.write_text(source_gate, encoding="utf-8")

lifecycle = LIFECYCLE_PATH.read_text(encoding="utf-8")
lifecycle = replace_section(
    lifecycle,
    "## BMGHDIAG2 exact-byte publication — working-branch pass",
    "## Live execution state",
    f"""## BMGHDIAG2 exact-byte publication — main integration pass

C3F18's provenance-safe `S1.42AK-BMGHDIAG2` successor has passed source/static review, the separate inactive review build, exact-byte publication, and main integration. PR #{PR} exact head `{PR_HEAD}` merged at `{MAIN_MERGE}` after Knowledge Architecture run `{KA_RUN}`, source/pure-static run `{SOURCE_RUN}`, and publication-aware archive run `{ARCHIVE_RUN}` all passed.

The integration archive gate selected published-validation mode: no profile rebuild and no Actions artifact upload occurred. The exact main-integrated profile SHA-256 remains `{PROFILE_SHA}` and diagnostic DLL SHA-256 remains `{DLL_SHA}`. The 337-member archive/index contract, zero package/config drift, LLL `{LLL_SHA}`, accepted normalizer `{NORMALIZER_SHA}`, and reconstructed readable ProfileSources snapshot remain unchanged. Integration evidence: `BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/MAIN_INTEGRATION_CHECKPOINT.md`.

BMGHDIAG2 is **published on main but not runtime-armed and not accepted**. Black Mesa x Greenhouse remains `NOT_YET_PROVEN` until a later explicit diagnostic runtime run.
""",
    "lifecycle BMGHDIAG2 section",
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
- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F18 BMGHDIAG2 exact bytes integrated on main; separate runtime activation next**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.
- No gameplay successor or universal override is armed.
""",
    "lifecycle live state",
)
lifecycle = replace_section(lifecycle, "## Exact next project action", "## Permanent Gale workflow", f"""## Exact next project action

{next_action}
""", "lifecycle next action")
lifecycle = lifecycle.replace(
    "BMGHDIAG2 is exact-byte published on the dedicated working branch but remains non-runtime until publication integration and a later explicit atomic activation step; only that later activation may authorize another gameplay run.",
    "BMGHDIAG2 exact bytes are integrated on main but remain non-runtime until a later explicit atomic activation step; only that later activation may authorize another gameplay run.",
)
LIFECYCLE_PATH.write_text(lifecycle, encoding="utf-8")

km = MAP_PATH.read_text(encoding="utf-8")
km = replace_section(
    km,
    "**Universal Interior Viability / Equal Availability is the selected scope.**",
    "## Authority rule",
    f"""**Universal Interior Viability / Equal Availability is the selected scope.** Phases A through C2 remain complete with the fixed 30×53 matrix unchanged at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`. The first exact `S1.42AK-BMGHDIAG1` Black Mesa run remains ingested as fail-closed diagnostic refusal evidence; Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

C3F18's separately versioned `S1.42AK-BMGHDIAG2` provenance repair has passed source/static review, inactive review build, exact-byte publication, and main integration. PR #{PR} exact head `{PR_HEAD}` merged at `{MAIN_MERGE}` after exact-head Knowledge Architecture `{KA_RUN}`, source/pure-static `{SOURCE_RUN}`, and publication-aware archive `{ARCHIVE_RUN}` all passed. The main-integrated profile SHA-256 is `{PROFILE_SHA}` and diagnostic DLL SHA-256 is `{DLL_SHA}`; the 337-member archive/index, zero package/config drift, LLL/normalizer identities and readable ProfileSources snapshot remain unchanged. BMGHDIAG2 is **on main but not runtime-armed**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no active candidate exists and no runtime test is outstanding. The next action is a separate atomic runtime-activation checkpoint; no gameplay run is yet authorized. The B3 matrix and permanent ownership/scope boundaries remain unchanged.
""",
    "knowledge map selected scope",
)
MAP_PATH.write_text(km, encoding="utf-8")

print(json.dumps({
    "status": NEW_STATUS,
    "integration_pr": PR,
    "main_merge_commit": MAIN_MERGE,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "runtime_armed": False,
    "runtime_test_outstanding": False,
}, indent=2))
