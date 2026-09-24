#!/usr/bin/env python3
"""One-shot C3F18 canonicalizer for the passed inactive BMGHDIAG2 review build.

This script is intentionally temporary. It updates repository-native lifecycle/evidence
from the already-completed review run, regenerates protected navigation, and leaves all
live build/runtime controllers inactive.
"""
from __future__ import annotations

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
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE"

BUILD_ID = "S1.42AK-BMGHDIAG2"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PROFILE_SHA = "56884f84bf90b1d8038b6aa1ee12de4548aedf76603134acbd5a91ad74233ef2"
DLL_SHA = "51de493e340a2e0c0422e9816b5c2f592113e12a71cf1be7081631b3c9520775"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
REVIEW_HEAD = "e45c695a5f75dd8e304f0434cd21bce3e0a30da3"
REVIEW_MERGE_REF = "569cbbb184a4f81085999a802c9a695ba3a9f3f2"
REVIEW_RUN = 35990294162
REVIEW_ARTIFACT_ID = 10803912824
REVIEW_ARTIFACT_ZIP_SHA = "265ebfae87ad3c48a6dbb57d0b3dce81a4c4d1c2e4872357f970354974da7a62"
REVIEW_ARTIFACT_NAME = "S1.42AK-BMGHDIAG2-review-569cbbb184a4f81085999a802c9a695ba3a9f3f2"
DIAGNOSTIC_DLL = "BepInEx/plugins/S142AKBMGHDiag2/S142AKBMGHDiag2.dll"
NEW_STATUS = "PHASE_C3F18_BMGHDIAG2_INACTIVE_REVIEW_BUILD_PASS_PUBLICATION_NEXT"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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
require(selected["status"] == "PHASE_C3F18_BMGHDIAG2_SOURCE_STATIC_PASS_INACTIVE_REVIEW_BUILD_NEXT", "Unexpected pre-finalization scope state")

state["updated"] = "2026-09-24"
selected["status"] = NEW_STATUS
selected["finding"] = (
    "S1.42AK-BMGHDIAG2 has passed both the provenance-safe source/static gate and a separate inactive review build from exact accepted S1.42AK. "
    f"Review PR #142 head {REVIEW_HEAD} produced run {REVIEW_RUN}; artifact {REVIEW_ARTIFACT_ID} has ZIP SHA-256 {REVIEW_ARTIFACT_ZIP_SHA}. "
    f"The review profile SHA-256 is {PROFILE_SHA} and the compiled/injected diagnostic DLL SHA-256 is {DLL_SHA}. "
    f"All 337 archive members were verified: the only added member is {DIAGNOSTIC_DLL}, the only changed existing member is export.r2x identity metadata, there are zero package/config changes, LLL remains {LLL_SHA}, and the accepted normalizer remains byte-identical at {NORMALIZER_SHA}. "
    "These bytes are review-only and are not repository-published or runtime-armed. Black Mesa x Greenhouse remains NOT_YET_PROVEN; S1.42AK, Black Mesa Dawn/native ownership, Greenhouse availability, accepted normalization and the B3 matrix remain unchanged."
)
selected["analysis_contract"] = (
    "Treat S1.42AK-BMGHDIAG2 as source/static-verified and inactive-review-build-verified, but not published, not runtime-armed and not accepted. "
    f"The next bounded checkpoint may publish only the exact reviewed bytes from review run {REVIEW_RUN} / artifact {REVIEW_ARTIFACT_ID}, with profile SHA-256 {PROFILE_SHA} and diagnostic DLL SHA-256 {DLL_SHA}. "
    "That publication checkpoint must re-verify the exact archive delta and readable ProfileSources evidence while keeping BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false. Runtime activation must remain a later separate atomic step. Preserve S1.42AB InteriorWeightNormalization, Black Mesa ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions and the separate Black-Mesa/Pikmin routing scope."
)
next_action = (
    f"Publish the exact reviewed S1.42AK-BMGHDIAG2 bytes from review run {REVIEW_RUN} / artifact {REVIEW_ARTIFACT_ID}, pinning profile SHA-256 {PROFILE_SHA} and diagnostic DLL SHA-256 {DLL_SHA}, and verify the published archive/ProfileSources against the passed review-build delta. "
    "Keep BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false. Do not Gale-import or arm gameplay/runtime in the publication checkpoint."
)
selected["next_action"] = next_action
selected["diagnostic_successor_review"] = {
    "build_id": BUILD_ID,
    "status": "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED_NOT_ACCEPTED",
    "base_build_id": "S1.42AK",
    "base_profile": "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z",
    "base_sha256": BASE_SHA,
    "build_spec": "BuildSpecs/S1.42AK-BMGHDIAG2.json",
    "build_plan": "BuildSpecs/S1.42AK-BMGHDIAG2_PLAN.md",
    "static_evidence": "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/STATIC_VERIFICATION.json",
    "review_checkpoint": "BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.md",
    "source_pr": 141,
    "review_pr": 142,
    "reviewed_head": REVIEW_HEAD,
    "review_merge_ref": REVIEW_MERGE_REF,
    "review_run": REVIEW_RUN,
    "review_artifact_id": REVIEW_ARTIFACT_ID,
    "review_artifact_name": REVIEW_ARTIFACT_NAME,
    "review_artifact_zip_sha256": REVIEW_ARTIFACT_ZIP_SHA,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "lll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "added_members": [DIAGNOSTIC_DLL],
    "changed_existing_members": ["export.r2x"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "published": False,
    "runtime_armed": False,
}
state["next_action"] = next_action
STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
static_report = {
    "status": "STATIC_BUILD_PASS_REVIEW_ARTIFACT_NOT_ARMED",
    "build_id": BUILD_ID,
    "base_sha256": BASE_SHA,
    "output_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "lll_dll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "added_members": [DIAGNOSTIC_DLL],
    "changed_existing_members": ["export.r2x"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "runtime_armed": False,
    "qualification": "Persisted from successful PR #142 inactive CI review build. The reviewed profile remains an Actions artifact only; BuildSpecs/current.json and RuntimeInbox/ACTIVE_BUILD.txt remain unchanged and no runtime test is authorized."
}
(EVIDENCE_DIR / "STATIC_VERIFICATION.json").write_text(json.dumps(static_report, indent=2) + "\n", encoding="utf-8")
review_record = {
    "status": "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED",
    "build_id": BUILD_ID,
    "review_pr": 142,
    "reviewed_head": REVIEW_HEAD,
    "review_merge_ref": REVIEW_MERGE_REF,
    "review_run": REVIEW_RUN,
    "review_artifact_id": REVIEW_ARTIFACT_ID,
    "review_artifact_name": REVIEW_ARTIFACT_NAME,
    "review_artifact_zip_sha256": REVIEW_ARTIFACT_ZIP_SHA,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "base_sha256": BASE_SHA,
    "lll_dll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "added_members": [DIAGNOSTIC_DLL],
    "changed_existing_members": ["export.r2x"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "published": False,
    "runtime_armed": False,
    "runtime_test_outstanding": False,
}
(EVIDENCE_DIR / "REVIEW_BUILD_CHECKPOINT.json").write_text(json.dumps(review_record, indent=2) + "\n", encoding="utf-8")
(EVIDENCE_DIR / "REVIEW_BUILD_CHECKPOINT.md").write_text(f"""# S1.42AK-BMGHDIAG2 inactive review-build checkpoint

**Status:** PASS / REVIEW ARTIFACT ONLY / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  
**Date:** 2026-09-24  
**Review PR:** #142  
**Reviewed head:** `{REVIEW_HEAD}`  
**PR merge ref used by Actions:** `{REVIEW_MERGE_REF}`  
**Review workflow run:** `{REVIEW_RUN}`  
**Actions artifact ID:** `{REVIEW_ARTIFACT_ID}`  
**Artifact name:** `{REVIEW_ARTIFACT_NAME}`  
**Artifact ZIP SHA-256:** `{REVIEW_ARTIFACT_ZIP_SHA}`

## Exact reviewed bytes

- exact parent S1.42AK SHA-256: `{BASE_SHA}`;
- review profile SHA-256: `{PROFILE_SHA}`;
- compiled/injected `S142AKBMGHDiag2.dll` SHA-256: `{DLL_SHA}`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `{LLL_SHA}`;
- accepted S1.42AB normalizer SHA-256: `{NORMALIZER_SHA}`.

The build compiled with zero warnings and zero errors. The injected diagnostic DLL was byte-identical to the compiled DLL.

## Exact archive delta

All 337 archive members were checked against the generated `FILE_INDEX.json`.

- added: `{DIAGNOSTIC_DLL}` only;
- changed existing: `export.r2x` only, and only permitted profile identity metadata differs after normalization;
- removed: none;
- package changes: 0;
- config changes: 0;
- accepted normalizer: byte-identical.

## Lifecycle boundary

This checkpoint records only an ephemeral Actions review artifact. No BMGHDIAG2 `.r2z` or `ProfileSources/S1.42AK-BMGHDIAG2/` has been published to `main`. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`, `active_candidate` remains null and `runtime_test_outstanding` remains false.

The next permitted bounded action is a separate publication checkpoint that materializes **these exact reviewed bytes** and revalidates their identity without arming runtime. Gale import/gameplay remains forbidden until a later explicit activation step.
""", encoding="utf-8")

plan = PLAN_PATH.read_text(encoding="utf-8")
plan = replace_once(
    plan,
    "**Status:** SOURCE STATIC PASS / NOT BUILT / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  ",
    "**Status:** SOURCE STATIC PASS / INACTIVE REVIEW BUILD PASS / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  ",
    "plan status",
)
plan = replace_section(
    plan,
    "## Review-build boundary",
    "## Runtime boundary",
    f"""## Inactive review-build checkpoint

PR #142 head `{REVIEW_HEAD}` completed the separately authorized inactive review build. `S1.42AK BMGHDIAG2 inactive review build and archive-delta gate` run `{REVIEW_RUN}` passed all policy tests, the source gate, fresh LLL provenance, compilation/build, exact archive validation and artifact upload.

Exact review identity:

- Actions artifact ID `{REVIEW_ARTIFACT_ID}` / `{REVIEW_ARTIFACT_NAME}`;
- artifact ZIP SHA-256 `{REVIEW_ARTIFACT_ZIP_SHA}`;
- review profile SHA-256 `{PROFILE_SHA}`;
- diagnostic DLL SHA-256 `{DLL_SHA}`;
- 337 archive members verified;
- only `{DIAGNOSTIC_DLL}` added;
- only `export.r2x` changed, limited to profile identity metadata;
- zero package/config changes;
- accepted normalizer byte-identical at `{NORMALIZER_SHA}`.

The reviewed profile remains an ephemeral Actions artifact. It is not repository-published, not Gale-imported, not runtime-armed and not accepted.

## Publication boundary

The next permitted bounded action is a separate publication checkpoint that publishes only the exact reviewed bytes above, persists the readable `ProfileSources` snapshot and publication verification, and rechecks the same archive/hash contract while all live controllers remain inactive. Publication success still does not authorize gameplay; runtime activation remains a later separate atomic step.
""",
    "plan review-build section",
)
PLAN_PATH.write_text(plan, encoding="utf-8")

source_gate = SOURCE_GATE_PATH.read_text(encoding="utf-8")
source_gate = replace_once(
    source_gate,
    'require("NOT BUILT" in plan and "NOT ARMED" in plan, "Human plan runtime/build boundary drift")',
    'require("NOT PUBLISHED" in plan and "NOT ARMED" in plan, "Human plan publication/runtime boundary drift")',
    "source gate plan boundary",
)
source_gate = replace_once(
    source_gate,
    '"status": "SOURCE_STATIC_CONTRACT_PASS_NOT_BUILT_NOT_ARMED",',
    '"status": "SOURCE_STATIC_CONTRACT_PASS_NOT_PUBLISHED_NOT_ARMED",',
    "source gate report status",
)
SOURCE_GATE_PATH.write_text(source_gate, encoding="utf-8")

lifecycle = LIFECYCLE_PATH.read_text(encoding="utf-8")
lifecycle = replace_once(lifecycle, "**Last-Validated:** 2026-09-23", "**Last-Validated:** 2026-09-24", "lifecycle date")
lifecycle = replace_section(
    lifecycle,
    "## BMGHDIAG2 provenance repair — source/static pass",
    "## Live execution state",
    f"""## BMGHDIAG2 inactive review build — pass

C3F18 first established and source/static-verified the provenance-safe `S1.42AK-BMGHDIAG2` successor: the physical installed V81 `Assembly-CSharp.dll` is hashed through BepInEx `Paths.ManagedPath`, while the loaded `EntranceTeleport` assembly/type/method contract is checked structurally. The selection and read-only observation Harmony surfaces remain unchanged from the reviewed successor design.

A separate inactive review build has now also passed. PR #142 exact head `{REVIEW_HEAD}` produced review run `{REVIEW_RUN}` / Actions artifact `{REVIEW_ARTIFACT_ID}`. The review profile SHA-256 is `{PROFILE_SHA}` and the compiled/injected BMGHDIAG2 DLL SHA-256 is `{DLL_SHA}`. All 337 archive members were verified: exactly one diagnostic DLL was added, only `export.r2x` identity metadata changed, package/config changes are zero, LLL remains `{LLL_SHA}`, and the accepted normalizer remains byte-identical at `{NORMALIZER_SHA}`. Persisted evidence: `BuildSpecs/S1.42AK-BMGHDIAG2_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.md`.

BMGHDIAG2 is **review-built but not published, not runtime-armed and not accepted**. The review artifact is not a gameplay target. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.
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
- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F18 BMGHDIAG2 inactive review build passed; exact publication checkpoint next**.
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
LIFECYCLE_PATH.write_text(lifecycle, encoding="utf-8")

km = MAP_PATH.read_text(encoding="utf-8")
km = replace_once(km, "**Last-Validated:** 2026-09-23", "**Last-Validated:** 2026-09-24", "knowledge map date")
km = replace_section(
    km,
    "**Universal Interior Viability / Equal Availability is the selected scope.**",
    "## Authority rule",
    f"""**Universal Interior Viability / Equal Availability is the selected scope.** Phases A through C2 remain complete with the fixed 30×53 matrix unchanged at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`. The first exact `S1.42AK-BMGHDIAG1` Black Mesa run remains ingested as fail-closed diagnostic refusal evidence; Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

C3F18's separately versioned `S1.42AK-BMGHDIAG2` provenance repair has now passed both source/static review and a separate inactive review build. PR #142 head `{REVIEW_HEAD}` / review run `{REVIEW_RUN}` produced Actions artifact `{REVIEW_ARTIFACT_ID}` with profile SHA-256 `{PROFILE_SHA}` and diagnostic DLL SHA-256 `{DLL_SHA}`. The exact archive delta is one new BMGHDIAG2 DLL plus profile identity metadata only, with zero package/config changes and byte-identical accepted normalizer. BMGHDIAG2 is **not published and not runtime-armed**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no active candidate exists and no runtime test is outstanding. The next action is a separate exact-byte publication checkpoint; Gale import/gameplay remains later. The B3 matrix and permanent ownership/scope boundaries remain unchanged.
""",
    "knowledge map selected scope",
)
MAP_PATH.write_text(km, encoding="utf-8")

print(json.dumps({
    "status": NEW_STATUS,
    "review_run": REVIEW_RUN,
    "review_artifact_id": REVIEW_ARTIFACT_ID,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "runtime_armed": False,
}, indent=2))
