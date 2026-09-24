#!/usr/bin/env python3
"""One-shot canonicalizer for the passed inactive S1.42AK-BMDSFIX1 review build.

This script is intentionally temporary. It persists exact review evidence and advances
only the repository lifecycle to the exact-byte publication checkpoint while leaving
all live build/runtime controllers inactive.
"""
from __future__ import annotations

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
EVIDENCE_DIR = ROOT / "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE"

BUILD_ID = "S1.42AK-BMDSFIX1"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
REVIEW_HEAD = "79922a13b3543552dac67bff3d49384c129d4260"
REVIEW_MERGE_REF = "7dbe71ba9ec504a387c5750f4f4c479dceffa95c"
REVIEW_RUN = 36014932493
REVIEW_ARTIFACT_ID = 10813908176
REVIEW_ARTIFACT_ZIP_SHA = "b22e14b07455f722202cfaaf915ee362786c1a05c090aff0939f5a61b9de5db1"
REVIEW_ARTIFACT_NAME = "S1.42AK-BMDSFIX1-review-7dbe71ba9ec504a387c5750f4f4c479dceffa95c"
FIX_DLL = "BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"
NEW_STATUS = "PHASE_C3F18_BMGHDIAG2_RUNTIME_INCONCLUSIVE_BMDSFIX1_INACTIVE_REVIEW_BUILD_PASS_PUBLICATION_NEXT"
OLD_STATUS = "PHASE_C3F18_BMGHDIAG2_RUNTIME_INCONCLUSIVE_BMDSFIX1_SOURCE_INTEGRATED_REVIEW_BUILD_NEXT"


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
require(selected["status"] == OLD_STATUS, "Unexpected pre-finalization scope state")

state["updated"] = "2026-09-24"
selected["status"] = NEW_STATUS
selected["finding"] = (
    "S1.42AK-BMDSFIX1 has passed its pair-scoped source/static gate and a separate inactive review build directly from exact accepted S1.42AK. "
    f"Review PR #149 head {REVIEW_HEAD} produced review run {REVIEW_RUN}; artifact {REVIEW_ARTIFACT_ID} has ZIP SHA-256 {REVIEW_ARTIFACT_ZIP_SHA}. "
    f"The review profile SHA-256 is {PROFILE_SHA} and the compiled/injected BMDSFIX1 DLL SHA-256 is {DLL_SHA}. "
    f"All 337 archive members were verified: the only added member is {FIX_DLL}, the only changed existing member is export.r2x profile identity metadata, there are zero package/config changes, LLL remains {LLL_SHA}, and the accepted S1.42AB normalizer remains byte-identical at {NORMALIZER_SHA}. "
    "These bytes are review-only and are not repository-published or runtime-armed. The fix remains scoped only to Black Mesa x DeepSewersFlow and does not alter accepted normalization, Black Mesa ownership, Greenhouse availability, the B3 matrix, or the separate Black Mesa x Greenhouse diagnostic task."
)
selected["analysis_contract"] = (
    "Treat S1.42AK-BMDSFIX1 as source/static-verified and inactive-review-build-verified, but not published, not runtime-armed and not accepted. "
    f"The next bounded checkpoint may publish only the exact reviewed bytes from review run {REVIEW_RUN} / artifact {REVIEW_ARTIFACT_ID}, with profile SHA-256 {PROFILE_SHA} and BMDSFIX1 DLL SHA-256 {DLL_SHA}. "
    "That publication checkpoint must re-verify the exact archive delta and readable ProfileSources evidence while keeping BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false. "
    "Runtime activation must remain a later separate atomic step. Preserve S1.42AB InteriorWeightNormalization, Dawn/native Black Mesa ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions and the separate Black-Mesa/Pikmin routing and Black Mesa x Greenhouse diagnostic scopes."
)
next_action = (
    f"Publish the exact reviewed S1.42AK-BMDSFIX1 bytes from review run {REVIEW_RUN} / artifact {REVIEW_ARTIFACT_ID}, pinning profile SHA-256 {PROFILE_SHA} and BMDSFIX1 DLL SHA-256 {DLL_SHA}, and verify the published archive/ProfileSources against the passed review-build delta. "
    "Keep BuildSpecs/current.json disabled, RuntimeInbox/ACTIVE_BUILD.txt at S1.42AK, active_candidate null and runtime_test_outstanding=false. Do not Gale-import, runtime-arm or accept BMDSFIX1 in the publication checkpoint. Black Mesa x Greenhouse successor-diagnostic repair remains separate."
)
selected["next_action"] = next_action
selected["bmdsfix1_review"] = {
    "build_id": BUILD_ID,
    "status": "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED_NOT_ACCEPTED",
    "base_build_id": "S1.42AK",
    "base_profile": "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z",
    "base_sha256": BASE_SHA,
    "build_spec": "BuildSpecs/S1.42AK-BMDSFIX1.json",
    "build_plan": "BuildSpecs/S1.42AK-BMDSFIX1_PLAN.md",
    "static_evidence": "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/STATIC_VERIFICATION.json",
    "review_checkpoint": "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.md",
    "source_pr": 146,
    "review_pr": 149,
    "reviewed_head": REVIEW_HEAD,
    "review_merge_ref": REVIEW_MERGE_REF,
    "review_run": REVIEW_RUN,
    "review_artifact_id": REVIEW_ARTIFACT_ID,
    "review_artifact_name": REVIEW_ARTIFACT_NAME,
    "review_artifact_zip_sha256": REVIEW_ARTIFACT_ZIP_SHA,
    "profile_sha256": PROFILE_SHA,
    "bmdsfix1_dll_sha256": DLL_SHA,
    "lll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "added_members": [FIX_DLL],
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
    "bmdsfix1_dll_sha256": DLL_SHA,
    "lll_dll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "added_members": [FIX_DLL],
    "changed_existing_members": ["export.r2x"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "runtime_armed": False,
    "qualification": "Persisted from successful PR #149 inactive CI review build. The reviewed profile remains an Actions artifact only; BuildSpecs/current.json and RuntimeInbox/ACTIVE_BUILD.txt remain unchanged and no runtime test is authorized.",
}
(EVIDENCE_DIR / "STATIC_VERIFICATION.json").write_text(json.dumps(static_report, indent=2) + "\n", encoding="utf-8")

review_record = {
    "status": "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED",
    "build_id": BUILD_ID,
    "review_pr": 149,
    "reviewed_head": REVIEW_HEAD,
    "review_merge_ref": REVIEW_MERGE_REF,
    "review_run": REVIEW_RUN,
    "review_artifact_id": REVIEW_ARTIFACT_ID,
    "review_artifact_name": REVIEW_ARTIFACT_NAME,
    "review_artifact_zip_sha256": REVIEW_ARTIFACT_ZIP_SHA,
    "profile_sha256": PROFILE_SHA,
    "bmdsfix1_dll_sha256": DLL_SHA,
    "base_sha256": BASE_SHA,
    "lll_dll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "added_members": [FIX_DLL],
    "changed_existing_members": ["export.r2x"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "published": False,
    "runtime_armed": False,
    "runtime_test_outstanding": False,
}
(EVIDENCE_DIR / "REVIEW_BUILD_CHECKPOINT.json").write_text(json.dumps(review_record, indent=2) + "\n", encoding="utf-8")

(EVIDENCE_DIR / "REVIEW_BUILD_CHECKPOINT.md").write_text(f"""# S1.42AK-BMDSFIX1 inactive review-build checkpoint

**Status:** PASS / REVIEW ARTIFACT ONLY / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  
**Date:** 2026-09-24  
**Review PR:** #149  
**Reviewed head:** `{REVIEW_HEAD}`  
**PR merge ref used by Actions:** `{REVIEW_MERGE_REF}`  
**Review workflow run:** `{REVIEW_RUN}`  
**Actions artifact ID:** `{REVIEW_ARTIFACT_ID}`  
**Artifact name:** `{REVIEW_ARTIFACT_NAME}`  
**Artifact ZIP SHA-256:** `{REVIEW_ARTIFACT_ZIP_SHA}`

## Exact reviewed bytes

- exact parent S1.42AK SHA-256: `{BASE_SHA}`;
- review profile SHA-256: `{PROFILE_SHA}`;
- compiled/injected `S142AKBMDSFix1.dll` SHA-256: `{DLL_SHA}`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `{LLL_SHA}`;
- accepted S1.42AB normalizer SHA-256: `{NORMALIZER_SHA}`.

The build compiled with zero warnings and zero errors. The injected BMDSFIX1 DLL was byte-identical to the compiled DLL.

## Exact archive delta

All 337 archive members were checked against the generated `FILE_INDEX.json`.

- added: `{FIX_DLL}` only;
- changed existing: `export.r2x` only, and only permitted profile identity metadata differs after normalization;
- removed: none;
- package changes: 0;
- config changes: 0;
- accepted normalizer: byte-identical.

## Lifecycle boundary

This checkpoint records only an ephemeral Actions review artifact. No BMDSFIX1 `.r2z` or `ProfileSources/S1.42AK-BMDSFIX1/` has been published to `main`. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK`, `active_candidate` remains null and `runtime_test_outstanding` remains false.

The next permitted bounded action is a separate exact-byte publication checkpoint that materializes **these exact reviewed bytes** and revalidates their identity without arming runtime. Gale import/gameplay remains forbidden until a later explicit activation step.
""", encoding="utf-8")

plan = PLAN_PATH.read_text(encoding="utf-8")
plan = replace_once(
    plan,
    "**Status:** SOURCE IMPLEMENTATION / STATIC REVIEW ONLY / NOT BUILT / NOT ARMED / NOT ACCEPTED  ",
    "**Status:** SOURCE/STATIC PASS / INACTIVE REVIEW BUILD PASS / NOT PUBLISHED / NOT ARMED / NOT ACCEPTED  ",
    "plan status",
)
plan = replace_section(
    plan,
    "## Future build/review gate",
    "## Runtime validation contract",
    f"""## Inactive review-build checkpoint

PR #149 head `{REVIEW_HEAD}` completed the separately authorized inactive review build. `S1.42AK BMDSFIX1 inactive review build and archive-delta gate` run `{REVIEW_RUN}` passed the pair-policy tests, source contract, fresh LLL provenance, compilation/build, exact archive validation and artifact upload.

Exact review identity:

- Actions artifact ID `{REVIEW_ARTIFACT_ID}` / `{REVIEW_ARTIFACT_NAME}`;
- artifact ZIP SHA-256 `{REVIEW_ARTIFACT_ZIP_SHA}`;
- review profile SHA-256 `{PROFILE_SHA}`;
- BMDSFIX1 DLL SHA-256 `{DLL_SHA}`;
- 337 archive members verified;
- only `{FIX_DLL}` added;
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
    '"status": "SOURCE_STATIC_CONTRACT_PASS_NOT_BUILT_NOT_ARMED",',
    '"status": "SOURCE_STATIC_CONTRACT_PASS_NOT_PUBLISHED_NOT_ARMED",',
    "source gate report status",
)
SOURCE_GATE_PATH.write_text(source_gate, encoding="utf-8")

lifecycle = LIFECYCLE_PATH.read_text(encoding="utf-8")
lifecycle = replace_section(
    lifecycle,
    "## BMDSFIX1 source/static repair — integrated, not built",
    "## Live execution state",
    f"""## BMDSFIX1 inactive review build — pass

The pair-scoped Deep Sewers mitigation `S1.42AK-BMDSFIX1` remains the exact one-postfix repair integrated through source PR #146. It clamps only Black Mesa x `DeepSewersFlow` values above 1.0 to 1.0 and preserves LLL/DunGen ownership, accepted S1.42AB normalization, Greenhouse availability and all non-target pairings.

A separate inactive review build has now also passed. PR #149 exact reviewed head `{REVIEW_HEAD}` produced review run `{REVIEW_RUN}` / Actions artifact `{REVIEW_ARTIFACT_ID}`. The review profile SHA-256 is `{PROFILE_SHA}` and the compiled/injected BMDSFIX1 DLL SHA-256 is `{DLL_SHA}`. All 337 archive members were verified: exactly one BMDSFIX1 DLL was added, only `export.r2x` profile identity metadata changed, package/config changes are zero, LLL remains `{LLL_SHA}`, and the accepted normalizer remains byte-identical at `{NORMALIZER_SHA}`. Persisted evidence: `BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.md`.

BMDSFIX1 is **review-built but not published, not runtime-armed and not accepted**. The review artifact is not a gameplay target. Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task.
""",
    "lifecycle BMDSFIX1 section",
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
- Selected scope: **Universal Interior Viability / Equal Availability — BMGHDIAG2 remains inconclusive; BMDSFIX1 inactive review build passed; exact publication checkpoint next**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`.
- No BMDSFIX1 profile or universal override is armed; S1.42AK remains accepted/latest.
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
km = replace_section(
    km,
    "**Universal Interior Viability / Equal Availability is the selected scope.**",
    "## Authority rule",
    f"""**Universal Interior Viability / Equal Availability is the selected scope.** Phases A through C2 remain complete with the fixed 30×53 matrix unchanged at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`.

Both exact Black Mesa x Greenhouse diagnostic attempts remain completed failed diagnostic evidence. BMGHDIAG2 is ingested at `RuntimeEvidence/S1.42AK-BMGHDIAG2/20260924T124542Z/` and refused before arming on `EntranceTeleport manifest module identity mismatch`, so Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation has now passed both source/static integration and a separate inactive review build. PR #149 reviewed head `{REVIEW_HEAD}` / review run `{REVIEW_RUN}` produced Actions artifact `{REVIEW_ARTIFACT_ID}` with profile SHA-256 `{PROFILE_SHA}` and BMDSFIX1 DLL SHA-256 `{DLL_SHA}`. The exact archive delta is one new BMDSFIX1 DLL plus profile identity metadata only, with zero package/config changes and byte-identical accepted normalizer. BMDSFIX1 is **not published and not runtime-armed**. `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`, no active candidate exists and no runtime test is outstanding. The next action is a separate exact-byte publication checkpoint; Gale import/gameplay remains later. The B3 matrix, ownership boundaries and Black Mesa x Greenhouse successor-diagnostic task remain unchanged.
""",
    "knowledge map selected scope",
)
MAP_PATH.write_text(km, encoding="utf-8")

print(json.dumps({
    "status": NEW_STATUS,
    "review_run": REVIEW_RUN,
    "review_artifact_id": REVIEW_ARTIFACT_ID,
    "profile_sha256": PROFILE_SHA,
    "bmdsfix1_dll_sha256": DLL_SHA,
    "runtime_armed": False,
}, indent=2))
