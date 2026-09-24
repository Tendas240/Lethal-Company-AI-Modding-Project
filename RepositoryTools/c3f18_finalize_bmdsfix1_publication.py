#!/usr/bin/env python3
"""One-shot C3F18 canonicalizer for the exact-byte BMDSFIX1 publication checkpoint.

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
PLAN_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_PLAN.md"
SOURCE_GATE_PATH = ROOT / "AnalysisTools/validate_s142ak_bmdsfix1_source.py"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
PUBLICATION_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
BUILD_RESULT_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
REVIEW_PATH = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.md"
PROFILE_PATH = ROOT / "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
PROFILE_SOURCES = ROOT / "ProfileSources/S1.42AK-BMDSFIX1"
FILE_INDEX_PATH = PROFILE_SOURCES / "FILE_INDEX.json"
HIDDEN_CONFIG_PATH = PROFILE_SOURCES / "BepInEx/config/.LCMaxSoundsFix.cfg"

BUILD_ID = "S1.42AK-BMDSFIX1"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
ARTIFACT_ZIP_SHA = "b22e14b07455f722202cfaaf915ee362786c1a05c090aff0939f5a61b9de5db1"
HIDDEN_CONFIG_SHA = "0093bae709cec57fd3f4f3bc5af22231b16944a666768e7ecf879430693f73a2"
REVIEW_RUN = 36014932493
REVIEW_ARTIFACT_ID = 10813908176
PUBLICATION_RUN = 36017880276
PUBLICATION_BRANCH = "c3f18-bmdsfix1-exact-publication"
PUBLISHED_PROFILE_COMMIT = "80057f75a253961449a4e92e27a16cbd83997f8a"
PUBLICATION_STAGING_HEAD = "cef6b8cdb4eb0add7daf2088c6748f63e1dcf58a"
OLD_STATUS = "PHASE_C3F18_BMGHDIAG2_RUNTIME_INCONCLUSIVE_BMDSFIX1_INACTIVE_REVIEW_BUILD_PASS_PUBLICATION_NEXT"
NEW_STATUS = "PHASE_C3F18_BMGHDIAG2_RUNTIME_INCONCLUSIVE_BMDSFIX1_EXACT_PUBLICATION_PASS_INTEGRATION_NEXT"


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
require(state["controllers"]["runtime_active_build"] == "S1.42AK", "Machine runtime controller drift")

selected = state["selected_scope"]
require(selected["scope_id"] == "UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY", "Selected scope drift")
require(selected["status"] == OLD_STATUS, "Unexpected pre-publication lifecycle state")
review = selected.get("bmdsfix1_review")
require(isinstance(review, dict) and review.get("build_id") == BUILD_ID, "BMDSFIX1 review record missing")
require(review.get("published") is False and review.get("runtime_armed") is False, "Unexpected review publication/runtime state")
require(review.get("review_run") == REVIEW_RUN and review.get("review_artifact_id") == REVIEW_ARTIFACT_ID, "Review provenance drift")
require(review.get("profile_sha256") == PROFILE_SHA and review.get("bmdsfix1_dll_sha256") == DLL_SHA, "Review identity drift")
require(review.get("review_artifact_zip_sha256") == ARTIFACT_ZIP_SHA, "Review artifact ZIP identity drift")

require(PROFILE_PATH.is_file() and sha_file(PROFILE_PATH) == PROFILE_SHA, "Published profile identity mismatch")
require(PUBLICATION_PATH.is_file(), "Publication verification missing")
publication = PUBLICATION_PATH.read_text(encoding="utf-8")
for marker in (
    "EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH",
    f"**Review workflow run:** `{REVIEW_RUN}`",
    f"**Actions artifact ID:** `{REVIEW_ARTIFACT_ID}`",
    f"**Artifact ZIP SHA-256:** `{ARTIFACT_ZIP_SHA}`",
    f"published profile SHA-256: `{PROFILE_SHA}`",
    f"published `S142AKBMDSFix1.dll` SHA-256: `{DLL_SHA}`",
    "zero package changes, zero config changes",
    "dedicated working branch",
):
    require(marker in publication, "Publication evidence drift or missing marker: " + marker)

require(BUILD_RESULT_PATH.is_file(), "Published BUILD_RESULT.json missing")
build_result = json.loads(BUILD_RESULT_PATH.read_text(encoding="utf-8"))
require(build_result["build_id"] == BUILD_ID, "BUILD_RESULT build id drift")
require(build_result["base_sha256"] == BASE_SHA and build_result["output_sha256"] == PROFILE_SHA, "BUILD_RESULT identity drift")
require(build_result["zip_members"] == 337 and build_result["snapshot"]["entries"] == 337, "BUILD_RESULT archive/snapshot count drift")
require(build_result["added_members"] == ["BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"], "BUILD_RESULT added-member drift")
require(build_result["changed_existing_members"] == ["export.r2x"], "BUILD_RESULT changed-member drift")
require(build_result["mod_state_changes"] == [] and build_result["mod_additions"] == [] and build_result["mod_removals"] == [], "BUILD_RESULT package drift")
require(STATIC_PATH.is_file(), "Persisted review static verification missing")
require(REVIEW_PATH.is_file(), "Persisted review checkpoint missing")

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
    "S1.42AK-BMDSFIX1 has passed its pair-scoped source/static gate, separate inactive review build, and exact-byte publication on the dedicated working branch. "
    f"Publication workflow run {PUBLICATION_RUN} materialized the exact reviewed profile from review run {REVIEW_RUN} / artifact {REVIEW_ARTIFACT_ID} at commit {PUBLISHED_PROFILE_COMMIT}, preserving profile SHA-256 {PROFILE_SHA} and BMDSFIX1 DLL SHA-256 {DLL_SHA}. "
    "All 337 archive members were rechecked; the only added member remains BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll, the only changed existing member remains export.r2x profile identity metadata, package/config drift is zero, and ProfileSources was reconstructed from the exact reviewed .r2z with a data-identical 337-row FILE_INDEX. "
    f"LLL remains {LLL_SHA} and the accepted normalizer remains {NORMALIZER_SHA}. The publication is not yet integrated into main and remains not runtime-armed/not accepted. The fix remains scoped only to Black Mesa x DeepSewersFlow; Black Mesa x Greenhouse remains NOT_YET_PROVEN under its separate successor-diagnostic task."
)
selected["analysis_contract"] = (
    "Treat S1.42AK-BMDSFIX1 as exact-byte published on the dedicated working branch from the pinned reviewed artifact, but not yet integrated into main, not runtime-armed and not accepted. "
    "The next bounded checkpoint is publication integration: make the existing BMDSFIX1 review/archive gate publication-aware without rebuilding the published profile, open/review the working-branch PR, require exact-head CI to pass, and merge only the exact branch state into main while BuildSpecs/current.json remains disabled, RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK, active_candidate remains null and runtime_test_outstanding remains false. "
    "Only after main integration and a new exact main gate may a later separate atomic runtime-activation step arm these exact published bytes. Preserve S1.42AB InteriorWeightNormalization, Dawn/native Black Mesa ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions, Black-Mesa/Pikmin routing and the separate Black Mesa x Greenhouse diagnostic scope."
)
next_action = (
    f"Integrate the exact-byte S1.42AK-BMDSFIX1 publication from branch {PUBLICATION_BRANCH} via a publication-aware PR and exact-head CI, preserving profile SHA-256 {PROFILE_SHA}, BMDSFIX1 DLL SHA-256 {DLL_SHA}, the reconstructed 337-row ProfileSources snapshot and publication evidence. "
    "Keep BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false throughout integration. Do not Gale-import, runtime-arm or accept BMDSFIX1; runtime activation remains a later separate atomic checkpoint after main integration and a new exact main gate. Black Mesa x Greenhouse successor-diagnostic repair remains separate."
)
selected["next_action"] = next_action
review.update({
    "status": "EXACT_BYTES_PUBLISHED_ON_WORKING_BRANCH_NOT_MAIN_INTEGRATED_NOT_ARMED_NOT_ACCEPTED",
    "profile": "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z",
    "profile_sources": "ProfileSources/S1.42AK-BMDSFIX1/",
    "file_index": "ProfileSources/S1.42AK-BMDSFIX1/FILE_INDEX.json",
    "build_result": "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/BUILD_RESULT.json",
    "publication_evidence": "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md",
    "publication_branch": PUBLICATION_BRANCH,
    "publication_workflow_run": PUBLICATION_RUN,
    "publication_staging_head": PUBLICATION_STAGING_HEAD,
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
    "**Status:** SOURCE/STATIC PASS / INACTIVE REVIEW BUILD PASS / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  ",
    "**Status:** SOURCE/STATIC PASS / INACTIVE REVIEW BUILD PASS / EXACT REVIEWED BYTES PUBLISHED ON WORKING BRANCH / NOT MAIN-INTEGRATED / NOT ARMED / NOT ACCEPTED  ",
    "plan publication status",
)
plan = replace_section(
    plan,
    "## Publication boundary",
    "## Runtime validation contract",
    f"""## Exact-byte publication checkpoint

The exact reviewed Actions artifact has now been materialized without rebuilding. Publication workflow run `{PUBLICATION_RUN}` on `{PUBLICATION_BRANCH}` used staging head `{PUBLICATION_STAGING_HEAD}` and produced publication commit `{PUBLISHED_PROFILE_COMMIT}` with persisted `BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`.

Publication re-confirmed:

- review run `{REVIEW_RUN}` / artifact `{REVIEW_ARTIFACT_ID}` / artifact ZIP SHA-256 `{ARTIFACT_ZIP_SHA}`;
- exact published profile SHA-256 `{PROFILE_SHA}`;
- exact published BMDSFIX1 DLL SHA-256 `{DLL_SHA}`;
- 337 archive members and the exact one-DLL plus `export.r2x` identity-only delta;
- zero package/config changes and no removed members;
- LLL SHA-256 `{LLL_SHA}` and accepted normalizer SHA-256 `{NORMALIZER_SHA}` unchanged;
- readable `ProfileSources/S1.42AK-BMDSFIX1/` reconstructed from the exact reviewed `.r2z` using repository snapshot semantics;
- reconstructed `FILE_INDEX.json` data-identical to the reviewed 337-row index;
- hidden `BepInEx/config/.LCMaxSoundsFix.cfg` present at index 1, 621 bytes, SHA-256 `{HIDDEN_CONFIG_SHA}`.

These exact bytes are published only on the dedicated working branch at this checkpoint. They are not yet integrated into `main`, not Gale-imported, not runtime-armed and not accepted.

## Integration boundary

The next bounded action is to make the existing BMDSFIX1 review/archive gate publication-aware, then perform PR/exact-head-CI/main integration of this exact working-branch publication without rebuilding or replacing the pinned bytes. All live controllers must remain inactive throughout integration. Runtime activation remains a later separate atomic lifecycle step after the publication is visible on `main` and a new exact `main` gate succeeds.
""",
    "plan publication section",
)
PLAN_PATH.write_text(plan, encoding="utf-8")

source_gate = SOURCE_GATE_PATH.read_text(encoding="utf-8")
source_gate = replace_once(
    source_gate,
    '"status": "SOURCE_STATIC_CONTRACT_PASS_NOT_PUBLISHED_NOT_ARMED",',
    '"status": "SOURCE_STATIC_CONTRACT_PASS_PUBLISHED_WORKING_BRANCH_NOT_ARMED",',
    "source-gate report status",
)
source_gate = replace_once(
    source_gate,
    '"qualification": "Source, compile and pure policy only; no profile build, controller mutation, runtime arming or acceptance."',
    '"qualification": "Source, compile and pure policy only. Exact reviewed bytes may already be branch-published, but this source gate itself never builds a profile, mutates controllers, arms runtime or grants acceptance."',
    "source-gate qualification",
)
SOURCE_GATE_PATH.write_text(source_gate, encoding="utf-8")

map_text = MAP_PATH.read_text(encoding="utf-8")
old_map = (
    "The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation has now passed both source/static integration and a separate inactive review build. PR #149 reviewed head `79922a13b3543552dac67bff3d49384c129d4260` / review run `36014932493` produced Actions artifact `10813908176` with profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0` and BMDSFIX1 DLL SHA-256 `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`. The exact archive delta is one new BMDSFIX1 DLL plus profile identity metadata only, with zero package/config changes and byte-identical accepted normalizer. BMDSFIX1 is **not published and not runtime-armed**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no active candidate exists and no runtime test is outstanding. The next action is a separate exact-byte publication checkpoint; Gale import/gameplay remains later. The B3 matrix, ownership boundaries and Black Mesa x Greenhouse successor-diagnostic task remain unchanged."
)
new_map = (
    f"The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation has now passed source/static integration, a separate inactive review build, and exact-byte publication on `{PUBLICATION_BRANCH}`. Review PR #149 / run `{REVIEW_RUN}` / artifact `{REVIEW_ARTIFACT_ID}` is preserved at profile SHA-256 `{PROFILE_SHA}` and BMDSFIX1 DLL SHA-256 `{DLL_SHA}`; publication run `{PUBLICATION_RUN}` materialized those exact bytes at commit `{PUBLISHED_PROFILE_COMMIT}`. The 337-member archive delta remains one BMDSFIX1 DLL plus profile identity metadata only, with zero package/config changes and byte-identical accepted normalizer. BMDSFIX1 is **published on the working branch but not main-integrated and not runtime-armed**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no active candidate exists and no runtime test is outstanding. The next action is publication-aware PR/exact-head-CI/main integration; Gale import/gameplay remains later. The B3 matrix, ownership boundaries and Black Mesa x Greenhouse successor-diagnostic task remain unchanged."
)
map_text = replace_once(map_text, old_map, new_map, "knowledge-map BMDSFIX1 lifecycle paragraph")
MAP_PATH.write_text(map_text, encoding="utf-8")

lifecycle = LIFECYCLE_PATH.read_text(encoding="utf-8")
old_heading = "## BMDSFIX1 inactive review build — pass"
new_section = f"""## BMDSFIX1 exact-byte publication — pass / integration next

The pair-scoped Deep Sewers mitigation `S1.42AK-BMDSFIX1` remains the exact one-postfix repair integrated through source PR #146. It clamps only Black Mesa x `DeepSewersFlow` values above 1.0 to 1.0 and preserves LLL/DunGen ownership, accepted S1.42AB normalization, Greenhouse availability and all non-target pairings.

The separate inactive review build remains pinned to PR #149 reviewed head `79922a13b3543552dac67bff3d49384c129d4260`, review run `{REVIEW_RUN}` and Actions artifact `{REVIEW_ARTIFACT_ID}` / ZIP SHA-256 `{ARTIFACT_ZIP_SHA}`. The exact reviewed profile SHA-256 is `{PROFILE_SHA}` and the compiled/injected BMDSFIX1 DLL SHA-256 is `{DLL_SHA}`.

Exact-byte publication is now complete on `{PUBLICATION_BRANCH}`. Publication workflow run `{PUBLICATION_RUN}` used staging head `{PUBLICATION_STAGING_HEAD}` and produced publication commit `{PUBLISHED_PROFILE_COMMIT}` without rebuilding the profile or DLL. Persisted evidence is `BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`.

Publication reverified all 337 archive members: exactly one BMDSFIX1 DLL was added, only `export.r2x` profile identity metadata changed, package/config changes are zero, LLL remains `{LLL_SHA}`, and the accepted normalizer remains byte-identical at `{NORMALIZER_SHA}`. `ProfileSources/S1.42AK-BMDSFIX1/` was reconstructed from the exact reviewed `.r2z`; its 337-row `FILE_INDEX.json` remains data-identical to review evidence, including hidden `.LCMaxSoundsFix.cfg` snapshot identity.

BMDSFIX1 is therefore **exact-byte published on the dedicated working branch, but not yet integrated into `main`, not runtime-armed and not accepted**. The next bounded checkpoint is publication-aware PR/exact-head-CI/main integration of these same bytes. Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task.
"""
lifecycle = replace_section(lifecycle, old_heading, "## Live execution state", new_section, "lifecycle BMDSFIX1 section")
lifecycle = replace_once(
    lifecycle,
    "- Selected scope: **Universal Interior Viability / Equal Availability — BMGHDIAG2 remains inconclusive; BMDSFIX1 inactive review build passed; exact publication checkpoint next**.",
    "- Selected scope: **Universal Interior Viability / Equal Availability — BMGHDIAG2 remains inconclusive; BMDSFIX1 exact-byte publication passed on working branch; integration next**.",
    "lifecycle live selected-scope line",
)
old_next = (
    "Publish the exact reviewed S1.42AK-BMDSFIX1 bytes from review run 36014932493 / artifact 10813908176, pinning profile SHA-256 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0 and BMDSFIX1 DLL SHA-256 f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92, and verify the published archive/ProfileSources against the passed review-build delta. Keep BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false. Do not Gale-import, runtime-arm or accept BMDSFIX1 in the publication checkpoint. Black Mesa x Greenhouse successor-diagnostic repair remains separate."
)
lifecycle = replace_once(lifecycle, old_next, next_action, "lifecycle exact next action")
LIFECYCLE_PATH.write_text(lifecycle, encoding="utf-8")

print(json.dumps({
    "status": NEW_STATUS,
    "build_id": BUILD_ID,
    "publication_branch": PUBLICATION_BRANCH,
    "publication_workflow_run": PUBLICATION_RUN,
    "published_profile_commit": PUBLISHED_PROFILE_COMMIT,
    "profile_sha256": PROFILE_SHA,
    "bmdsfix1_dll_sha256": DLL_SHA,
    "archive_members_verified": 337,
    "main_integrated": False,
    "runtime_armed": False,
    "active_candidate": state["active_candidate"],
    "runtime_test_outstanding": state["runtime_test_outstanding"],
    "runtime_active_build": state["controllers"]["runtime_active_build"],
}, indent=2))
