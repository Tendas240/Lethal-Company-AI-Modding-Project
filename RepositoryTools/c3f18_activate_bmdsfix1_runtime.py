#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_ID = "S1.42AK-BMDSFIX1"
TITLE = "Black Mesa Deep Sewers Size Fix"
PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
DLL_REL = "ProfileSources/S1.42AK-BMDSFIX1/BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"
DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
BASE_ID = "S1.42AK"
BASE_PROFILE = "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
BUILD_RESULT = "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC_EVIDENCE = "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
PUBLICATION_EVIDENCE = "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
INTEGRATION_EVIDENCE = "BuildSpecs/S1.42AK-BMDSFIX1_BUILD_EVIDENCE/MAIN_INTEGRATION_CHECKPOINT.json"
BUILD_PLAN = "BuildSpecs/S1.42AK-BMDSFIX1_PLAN.md"
PROFILE_SOURCES = "ProfileSources/S1.42AK-BMDSFIX1/"
FILE_INDEX = "ProfileSources/S1.42AK-BMDSFIX1/FILE_INDEX.json"
ACTIVATION = "Current/174_S1.42AK_BMDSFIX1_RUNTIME_ACTIVATION.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, data) -> None:
    (ROOT / rel).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(rel: str) -> str:
    h = hashlib.sha256()
    with (ROOT / rel).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected exactly one replacement target, found {count}")
    return text.replace(old, new, 1)


def replace_regex(text: str, pattern: str, replacement: str, label: str, flags: int = re.S) -> str:
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    require(count == 1, f"{label}: expected exactly one regex target, found {count}")
    return new_text


# Exact pre-activation proof boundary.
state = load_json("Current/CURRENT_STATE.json")
require(state["accepted_baseline"]["build_id"] == BASE_ID, "Accepted baseline drift")
require(state["accepted_baseline"]["sha256"] == BASE_SHA, "Accepted baseline SHA drift")
require(state["latest_built_artifact"]["build_id"] == BASE_ID, "Latest normal artifact drift")
require(state["active_candidate"] is None, "Active candidate must be null before BMDSFIX1 activation")
require(state["runtime_test_outstanding"] is False, "Runtime test already outstanding")
require(state["selected_scope"]["status"] == "PHASE_C3F18_BMGHDIAG2_RUNTIME_INCONCLUSIVE_BMDSFIX1_MAIN_INTEGRATION_PASS_RUNTIME_ACTIVATION_NEXT", "Unexpected selected-scope phase")
require(state["controllers"]["runtime_active_build"] == BASE_ID, "Runtime controller drift")
require((ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == BASE_ID, "ACTIVE_BUILD drift")

current_spec = load_json("BuildSpecs/current.json")
require(current_spec["enabled"] is False, "Build controller must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Unexpected disabled build-controller identity")
require(current_spec["base_profile"] == BASE_PROFILE and current_spec["base_sha256"] == BASE_SHA, "Pre-activation build guard drift")

integration = load_json(INTEGRATION_EVIDENCE)
require(integration["status"] == "MAIN_INTEGRATION_PASS_NOT_RUNTIME_ARMED_NOT_ACCEPTED", "Integration checkpoint status drift")
require(integration["build_id"] == BUILD_ID, "Integration checkpoint build ID drift")
require(integration["profile_sha256"] == PROFILE_SHA, "Integration checkpoint profile SHA drift")
require(integration["bmdsfix1_dll_sha256"] == DLL_SHA, "Integration checkpoint DLL SHA drift")
require(integration["runtime_armed"] is False and integration["runtime_test_outstanding"] is False, "Integration checkpoint already runtime-armed")

build_result = load_json(BUILD_RESULT)
require(build_result["build_id"] == BUILD_ID, "BMDSFIX1 build-result ID drift")
require(build_result["profile_name"] == "LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix", "BMDSFIX1 profile-name drift")
require(build_result["base_profile"] == BASE_PROFILE and build_result["base_sha256"] == BASE_SHA, "BMDSFIX1 parent drift")
require(build_result["output_profile"] == PROFILE and build_result["output_sha256"] == PROFILE_SHA, "BMDSFIX1 output identity drift")
require(build_result["zip_members"] == 337, "BMDSFIX1 archive-member count drift")
require(build_result["changed_existing_members"] == ["export.r2x"], "BMDSFIX1 changed-member contract drift")
require(build_result["added_members"] == ["BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"], "BMDSFIX1 added-member contract drift")
require(sha256_file(PROFILE) == PROFILE_SHA, "Main-integrated BMDSFIX1 profile SHA mismatch")
require(sha256_file(DLL_REL) == DLL_SHA, "Main-integrated BMDSFIX1 DLL SHA mismatch")

review = state["selected_scope"]["bmdsfix1_review"]
require(review["build_id"] == BUILD_ID, "CURRENT_STATE BMDSFIX1 record ID drift")
require(review["status"] == "EXACT_BYTES_MAIN_INTEGRATED_NOT_ARMED_NOT_ACCEPTED", "CURRENT_STATE BMDSFIX1 pre-activation status drift")
require(review["profile"] == PROFILE and review["profile_sha256"] == PROFILE_SHA, "CURRENT_STATE BMDSFIX1 profile identity drift")
require(review["bmdsfix1_dll_sha256"] == DLL_SHA, "CURRENT_STATE BMDSFIX1 DLL identity drift")
require(review["main_integrated"] is True and review["runtime_armed"] is False, "CURRENT_STATE BMDSFIX1 integration/arming drift")

# Promote exact published BMDSFIX1 bytes to the normal active runtime-candidate path.
candidate = {
    "build_id": BUILD_ID,
    "title": TITLE,
    "status": "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED",
    "profile": PROFILE,
    "sha256": PROFILE_SHA,
    "candidate_record": ACTIVATION,
    "build_plan": BUILD_PLAN,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC_EVIDENCE,
    "publication_evidence": PUBLICATION_EVIDENCE,
    "parent": BASE_ID,
    "review_run": 36014932493,
    "review_artifact_id": 10813908176,
    "publication_workflow_run": 36017880276,
    "published_profile_commit": "80057f75a253961449a4e92e27a16cbd83997f8a",
    "main_integration_commit": "21138185f1ab377660b61120f1d07733d4180672"
}
state["latest_built_artifact"] = copy.deepcopy(candidate)
state["active_candidate"] = copy.deepcopy(candidate)
state["runtime_test_outstanding"] = True
scope = state["selected_scope"]
scope["status"] = "PHASE_C3F18_BMDSFIX1_RUNTIME_ACTIVE_TEST_OUTSTANDING"
scope["candidate_build_id"] = BUILD_ID
scope["finding"] = (
    "S1.42AK-BMDSFIX1 exact reviewed/published/main-integrated bytes are now the active gameplay runtime candidate for the bounded Black Mesa x DeepSewersFlow mitigation gate. "
    "The active profile remains SHA-256 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0 with BMDSFIX1 DLL SHA-256 f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92 and 337 members. "
    "Accepted baseline remains S1.42AK; BMDSFIX1 is latest/active but not accepted. BuildSpecs/current.json remains disabled and now guards the exact active-candidate profile. RuntimeInbox/ACTIVE_BUILD.txt identifies S1.42AK-BMDSFIX1 for canonical Gale target resolution and runtime-evidence attribution. "
    "The fix scope remains only Black Mesa x DeepSewersFlow. Black Mesa x Greenhouse remains NOT_YET_PROVEN under its separate successor-diagnostic task."
)
scope["analysis_contract"] = (
    "Treat S1.42AK-BMDSFIX1 as the active runtime candidate but not accepted. Preserve exact profile SHA-256 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0 and BMDSFIX1 DLL SHA-256 f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92. "
    "Runtime qualification must prove [BMDSFIX1] ARMED without refusal, Black Mesa x DeepSewersFlow application to multiplier 1, completed dungeon generation and landed gameplay without the prior persistent retry/atmosphere failure, plus at least one non-target generation with no unintended BMDSFIX1 application. "
    "Do not change gameplay/config/package/profile/plugin bytes, do not alter S1.42AB normalization or Dawn/native Black Mesa ownership, and keep Black Mesa x Greenhouse separate."
)
scope["next_action"] = (
    "Import exact active S1.42AK-BMDSFIX1 through the canonical repository-driven Gale v2.4 launcher. Run the bounded BMDSFIX1 runtime gate: obtain one Black Mesa x DeepSewersFlow generation showing [BMDSFIX1] ARMED and APPLIED with multiplier ->1, successful generation/landing without the prior persistent retry flood, and at least one non-target generation showing no BMDSFIX1 application or size mutation. Then upload that run's exact BepInEx/LogOutput.log with the build-specific one-line uploader. Do not alter profile/config/package/plugin bytes during the test."
)
review = copy.deepcopy(review)
review["status"] = "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
review["runtime_armed"] = True
review["activation_record"] = ACTIVATION
review["runtime_validation_status"] = "RUNTIME_TEST_OUTSTANDING_NOT_ACCEPTED"
scope["bmdsfix1_review"] = review
scope["bmdsfix1_runtime_activation"] = ACTIVATION
state["next_action"] = scope["next_action"]
state["controllers"]["runtime_active_build"] = BUILD_ID
state["controllers"]["build_base_profile"] = PROFILE
state["controllers"]["build_base_sha256"] = PROFILE_SHA
write_json("Current/CURRENT_STATE.json", state)

# Normal runtime-candidate resolver contract: current AUTO_BUILD_RESULT must describe latest active gameplay candidate.
write_json("Current/AUTO_BUILD_RESULT.json", build_result)
auto_md = f"""# Automated profile build result - {BUILD_ID}\n\n- Profile: {build_result['profile_name']}\n- Base: {build_result['base_profile']}\n- Base SHA-256: {build_result['base_sha256']}\n- Output: {build_result['output_profile']}\n- Output SHA-256: {build_result['output_sha256']}\n- ZIP members: {build_result['zip_members']}\n- Text snapshot: {build_result['snapshot_dir']} ({build_result['snapshot']['text_entries']} readable files)\n\n## Changed existing members\n\n- export.r2x\n\n## Added members\n\n- BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll\n"""
(ROOT / "Current/AUTO_BUILD_RESULT.md").write_text(auto_md, encoding="utf-8")

# Build controller stays disabled but guards the active candidate, as required by atomic-state validation.
current_spec["base_profile"] = PROFILE
current_spec["base_sha256"] = PROFILE_SHA
write_json("BuildSpecs/current.json", current_spec)
(ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID + "\n", encoding="utf-8")

# Register exact profile for Gale/integrity checks.
expected = load_json("Profiles/EXPECTED_HASHES.json")
require(PROFILE not in expected, "BMDSFIX1 expected-hash entry already exists unexpectedly")
expected[PROFILE] = {
    "build_id": BUILD_ID,
    "sha256": PROFILE_SHA,
    "note": "Active runtime gameplay candidate directly over accepted S1.42AK; canonical readable snapshot is ProfileSources/S1.42AK-BMDSFIX1/. Not accepted until explicit runtime decision."
}
write_json("Profiles/EXPECTED_HASHES.json", expected)

# Pending artifact-evidence candidate.
integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
require(not any(x.get("build_id") == BUILD_ID for x in integrity.get("profiles", [])), "BMDSFIX1 unexpectedly already completed in artifact evidence")
require(not any(x.get("build_id") == BUILD_ID for x in integrity.get("pending_profiles", [])), "BMDSFIX1 unexpectedly already pending in artifact evidence")
integrity["updated"] = "2026-09-24"
integrity["last_validated"] = "2026-09-24"
integrity["pending_profiles"].append({
    "build_id": BUILD_ID,
    "role": "ACTIVE_RUNTIME_CANDIDATE_PENDING",
    "profile": PROFILE,
    "profile_sha256": PROFILE_SHA,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "export": "ProfileSources/S1.42AK-BMDSFIX1/export.r2x",
    "candidate_record": ACTIVATION,
    "build_plan": BUILD_PLAN,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC_EVIDENCE,
    "publication_evidence": PUBLICATION_EVIDENCE,
    "bmdsfix1_dll_sha256": DLL_SHA,
    "runtime_evidence_required": False,
    "partial_runtime_evidence_present": False,
    "note": "Exact reviewed/published/main-integrated BMDSFIX1 bytes are the active gameplay runtime candidate solely for Black Mesa x DeepSewersFlow qualification; accepted baseline remains S1.42AK."
})
integrity.setdefault("verified_repository_api_observations", []).append(
    "S1.42AK-BMDSFIX1 exact profile SHA-256 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0 is runtime-armed as the active gameplay candidate; BMDSFIX1 DLL SHA-256 f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92 remains exact and acceptance is pending runtime evidence."
)
write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

# Build lineage: accepted stays S1.42AK; BMDSFIX1 becomes latest + active candidate.
lineage = load_json("Current/BUILD_LINEAGE.json")
require(lineage["current_accepted_build_id"] == BASE_ID, "Lineage accepted baseline drift")
require(lineage["active_candidate_build_id"] is None, "Lineage already has active candidate")
require(lineage["latest_built_artifact_id"] == BASE_ID, "Lineage latest artifact drift")
require(not any(x.get("id") == BUILD_ID for x in lineage["builds"]), "BMDSFIX1 lineage entry already exists")
lineage["date"] = "2026-09-24"
lineage["active_candidate_build_id"] = BUILD_ID
lineage["latest_built_artifact_id"] = BUILD_ID
lineage["builds"].append({
    "id": BUILD_ID,
    "title": TITLE,
    "status": "active-runtime-candidate-not-accepted",
    "parent": BASE_ID,
    "profile": PROFILE,
    "sha256": PROFILE_SHA,
    "build_plan": BUILD_PLAN,
    "candidate_record": ACTIVATION,
    "decision_record": ACTIVATION,
    "workflow_run": 36014932493,
    "build_commit": "7dbe71ba9ec504a387c5750f4f4c479dceffa95c",
    "static_evidence": STATIC_EVIDENCE,
    "safe_as_gameplay_base": False,
    "principal_feature": "pair-scoped Black Mesa x DeepSewersFlow generation-size clamp to 1.0 over exact accepted S1.42AK; runtime qualification outstanding",
    "publication_evidence": PUBLICATION_EVIDENCE,
    "activation_record": ACTIVATION
})
lineage.setdefault("feature_index", {})["Black_Mesa_DeepSewers_pair_scoped_size_clamp_runtime_candidate"] = BUILD_ID
lineage.setdefault("lineage_invariants", []).append(
    "S1.42AK-BMDSFIX1 is built directly from exact accepted S1.42AK and changes only the added S142AKBMDSFix1.dll plus export identity metadata. It is the active runtime candidate solely for Black Mesa x DeepSewersFlow qualification and is not safe as a gameplay base until an explicit runtime decision accepts it. Black Mesa x Greenhouse remains a separate diagnostic scope."
)
write_json("Current/BUILD_LINEAGE.json", lineage)

# Human build-lineage mirror.
path = ROOT / "Current/BUILD_LINEAGE.md"
text = path.read_text(encoding="utf-8")
text = text.replace("**Last-Validated:** 2026-09-17", "**Last-Validated:** 2026-09-24", 1)
text = replace_regex(text, r"## Current lineage head\n.*?(?=\n## Meaningful build history)", """## Current lineage head

- **Accepted gameplay baseline:** S1.42AK — LC Office Camera Enemy Balance — **ACCEPTED FULL NORMAL STACK**.
- **Latest built artifact / active candidate:** S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix — **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED**.
- **Accepted predecessor / rollback provenance:** S1.42AI — BCMER ShyGuy Interior-Only Event Correction.
- **Balanced parent:** S1.42AJ — LC Office V81 Integration — not accepted; exact parent of S1.42AK.
- **Completed LC Office diagnostic evidence:** S1.42AJ-DIAG1 / S1.42AJ-DIAG2 — diagnostic-only, not gameplay accepted.
- **Current action:** run the bounded BMDSFIX1 Black Mesa x DeepSewersFlow runtime gate plus one non-target generation, then ingest the exact runtime log. S1.42AK remains accepted until an explicit decision.

For live lifecycle state use `Knowledge/CURRENT_LIFECYCLE.md`. This file is the build-history router; use the linked build-specific evidence for exact forensic detail.
""", "build-lineage current head")
text = replace_once(text, "| S1.42AK | **ACCEPTED FULL NORMAL STACK** | Accepted balanced LC Office camera/enemy integration; full-normal Offense gate passed with limited hostile-indoor coverage explicitly preserved. |", "| S1.42AK | **ACCEPTED FULL NORMAL STACK** | Accepted balanced LC Office camera/enemy integration; full-normal Offense gate passed with limited hostile-indoor coverage explicitly preserved. |\n| S1.42AK-BMDSFIX1 | **ACTIVE RUNTIME CANDIDATE / NOT ACCEPTED** | Exact pair-scoped Black Mesa x DeepSewersFlow size clamp over accepted S1.42AK; exact reviewed/published bytes are active for runtime qualification only. |", "build-lineage table row")
insert = f"""### S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix

- Parent: exact accepted S1.42AK.
- Profile: `{PROFILE}`
- SHA-256: `{PROFILE_SHA}`
- BMDSFIX1 DLL SHA-256: `{DLL_SHA}`
- Plan: `{BUILD_PLAN}`
- Build result: `{BUILD_RESULT}`
- Publication evidence: `{PUBLICATION_EVIDENCE}`
- Activation: `{ACTIVATION}`
- Status: **active runtime candidate / not accepted**.
- Scope: only Black Mesa x `DeepSewersFlow`; no Greenhouse, universal availability, package or config change.

"""
text = replace_once(text, "### S1.42C — enemy-spawn restore baseline", insert + "### S1.42C — enemy-spawn restore baseline", "build-lineage detailed candidate section")
path.write_text(text, encoding="utf-8")

# Human artifact integrity mirror.
path = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->", "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->", "artifact-integrity live marker")
text = replace_regex(text, r"## Pending / deferred unaccepted profiles\n.*?(?=\n## Completed diagnostic evidence: S1\.42AI-DIAG1R3)", f"""## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.
- **S1.42AK-BMDSFIX1** — active gameplay runtime candidate directly over accepted S1.42AK; profile SHA-256 `{PROFILE_SHA}`; BMDSFIX1 DLL SHA-256 `{DLL_SHA}`; runtime evidence outstanding; not accepted.

BMDSFIX1 exact reviewed bytes are published and main-integrated. Runtime activation changes only lifecycle/controller/evidence routing; no gameplay/config/package/profile/plugin bytes are regenerated or altered. The candidate is scoped only to Black Mesa x `DeepSewersFlow`. Black Mesa x Greenhouse remains separate and unproven.
""", "artifact-integrity pending section")
path.write_text(text, encoding="utf-8")

# Knowledge-map live anchor.
path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->", "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->", "knowledge-map live marker")
text = replace_regex(text, r"The separate pair-scoped `S1\.42AK-BMDSFIX1`.*?(?=\n\n## Authority rule)", f"""The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation has passed source/static integration, inactive review build, exact-byte publication and main integration, and is now the **active gameplay runtime candidate / not accepted**. Exact profile SHA-256 is `{PROFILE_SHA}` and BMDSFIX1 DLL SHA-256 is `{DLL_SHA}`; the 337-member archive/index, zero package/config drift, LLL/normalizer identities and readable ProfileSources snapshot remain unchanged. `BuildSpecs/current.json` remains disabled while guarding the candidate, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`, and one bounded runtime test is outstanding. Accepted baseline remains S1.42AK. The runtime gate is limited to Black Mesa x `DeepSewersFlow` plus a non-target control generation. Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task. Activation authority: `{ACTIVATION}`.""", "knowledge-map BMDSFIX1 anchor")
path.write_text(text, encoding="utf-8")

# Current lifecycle router.
path = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->", "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->", "lifecycle live marker")
text = replace_regex(text, r"## BMDSFIX1 exact-byte publication — main integration pass\n.*?(?=\n## Live execution state)", f"""## BMDSFIX1 exact-byte publication — runtime activation

The pair-scoped Deep Sewers mitigation `S1.42AK-BMDSFIX1` has passed source/static review, inactive review build, exact-byte publication and main integration. Its exact main-integrated profile SHA-256 remains `{PROFILE_SHA}` and BMDSFIX1 DLL SHA-256 remains `{DLL_SHA}` with 337 members, zero package/config drift, unchanged LLL/normalizer identities and readable `ProfileSources/S1.42AK-BMDSFIX1/`.

The exact published bytes are now runtime-armed as the active gameplay candidate under `{ACTIVATION}`. Accepted baseline remains S1.42AK; BMDSFIX1 is latest/active but not accepted. The runtime gate is scoped only to Black Mesa x `DeepSewersFlow`, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task.
""", "lifecycle BMDSFIX1 section")
text = replace_regex(text, r"## Live execution state\n.*?(?=\n## Exact next project action)", f"""## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK-BMDSFIX1 — active runtime candidate / not accepted**.
- Active gameplay candidate: **S1.42AK-BMDSFIX1**.
- Active diagnostic runtime target: **none**.
- Runtime test outstanding: **yes — bounded BMDSFIX1 qualification**.
- Selected scope: **Universal Interior Viability / Equal Availability — BMDSFIX1 runtime active; evidence outstanding**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 candidate bytes.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`.
- S1.42AK remains the accepted rollback baseline; no Greenhouse diagnostic is armed.
""", "lifecycle live state")
text = replace_regex(text, r"## Exact next project action\n.*?(?=\n## Permanent Gale workflow)", f"""## Exact next project action

{scope['next_action']}
""", "lifecycle next action")
text = replace_regex(text, r"## Permanent Gale workflow\n.*\Z", f"""## Permanent Gale workflow

The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. BMDSFIX1 now resolves through the normal active-candidate path because `Current/AUTO_BUILD_RESULT.json`, `CURRENT_STATE.latest_built_artifact`, `active_candidate` and `RuntimeInbox/ACTIVE_BUILD.txt` all bind the same exact `{BUILD_ID}` profile SHA. Runtime activation does not accept the candidate; only later runtime evidence and an explicit decision can do so.
""", "lifecycle Gale section")
path.write_text(text, encoding="utf-8")

# Roadmap live block.
path = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->", "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->", "roadmap live marker")
text = replace_regex(text, r"## Current position\n.*?(?=\n## Completed LC Office scrap scope)", f"""## Current position

Accepted gameplay baseline remains **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**, SHA-256 `{BASE_SHA}`.

Latest built artifact and active gameplay runtime candidate is **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `{PROFILE_SHA}`. It is not accepted. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`; `BuildSpecs/current.json` remains disabled while guarding the exact candidate; one bounded runtime test is outstanding.

Exact BMGHDIAG2 runtime evidence remains completed and inconclusive because the diagnostic refused before arming with `EntranceTeleport manifest module identity mismatch`. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`; identical BMGHDIAG2 bytes must not be rerun as though they could qualify the pair.

## Selected scope

**Universal Interior Viability / Equal Availability — SELECTED / BMDSFIX1 RUNTIME ACTIVE / EVIDENCE OUTSTANDING.**

The authoritative 30x53 B3 matrix and accepted S1.42AB post-viability normalizer remain unchanged. BMDSFIX1 addresses only the separately observed Black Mesa x Deep Sewers 4.875 generation-size pressure. Exact reviewed/published/main-integrated bytes are active without any package/config/profile/plugin rebuild or mutation.

Plan: `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`.

## Exact next selected-scope action

{scope['next_action']}
""", "roadmap current block")
path.write_text(text, encoding="utf-8")

# Interior topic: close stale BMGHDIAG2-active wording and expose only current BMDSFIX1 gate.
path = ROOT / "Knowledge/INTERIORS_AND_LLL.md"
text = path.read_text(encoding="utf-8")
text = replace_regex(text, r"That startup-provenance root cause has since been repaired by separately versioned `S1\.42AK-BMGHDIAG2`.*?Activation authority: `Current/172_S1\.42AK_BMGHDIAG2_RUNTIME_ACTIVATION\.md`\.", f"""The separately versioned `S1.42AK-BMGHDIAG2` attempt is now completed failed diagnostic evidence: it refused before arming on `EntranceTeleport manifest module identity mismatch`, so Black Mesa x Greenhouse remains `NOT_YET_PROVEN` and those exact bytes must not be rerun as if they can qualify the pair. The same normal-fallback run separately exposed Black Mesa x Deep Sewers generation pressure at multiplier 4.875.

The exact pair-scoped `S1.42AK-BMDSFIX1` mitigation is now the active gameplay runtime candidate, profile SHA-256 `{PROFILE_SHA}`, BMDSFIX1 DLL SHA-256 `{DLL_SHA}`. Its only behavior change is Black Mesa x `DeepSewersFlow` clamping an LLL-calculated multiplier greater than 1 to exactly 1.0. The runtime gate must prove arming/application, successful generation and landing without the previous persistent retry/atmosphere failure, plus a non-target generation with no unintended application. Activation authority: `{ACTIVATION}`.""", "interiors current C3F18 paragraph")
path.write_text(text, encoding="utf-8")

# Activation record itself contains both mandatory ready-to-test one-liners.
gale = "$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content"
uploader = "$ErrorActionPreference='Stop';$build='S1.42AK-BMDSFIX1';$log=Join-Path $env:APPDATA 'com.kesomannen.gale\\lethal-company\\profiles\\LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix\\BepInEx\\LogOutput.log';if(!(Test-Path -LiteralPath $log -PathType Leaf)){throw \"Expected runtime log not found: $log\"};$bytes=[IO.File]::ReadAllBytes($log);if($bytes.Length -le 0){throw 'Runtime log is empty'};$text=[Text.Encoding]::UTF8.GetString($bytes);if($text.IndexOf('[BMDSFIX1]',[StringComparison]::Ordinal) -lt 0){throw 'Refusing upload: exact local LogOutput.log contains no [BMDSFIX1] marker'};$localSha=([BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($bytes))).Replace('-','').ToLowerInvariant();$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;$fallback=Join-Path $env:ProgramFiles 'GitHub CLI\\gh.exe';if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback};if(!$gh -and (Get-Command winget -ErrorAction SilentlyContinue)){winget install --id GitHub.cli -e --source winget --accept-source-agreements --accept-package-agreements | Out-Host;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback}};if(!$gh){throw 'GitHub CLI (gh) could not be resolved or bootstrapped'};& $gh auth status -h github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login -h github.com -w;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dest='RuntimeInbox/Current/LogOutput.log';$existing=$null;try{$existing=(& $gh api \"repos/$repo/contents/$dest?ref=main\" --jq '.sha' 2>$null)}catch{};$payload=@{message=\"Upload $build runtime log ($localSha)\";content=[Convert]::ToBase64String($bytes);branch='main'};if($existing){$payload.sha=$existing};$json=$payload|ConvertTo-Json -Compress;$json|& $gh api --method PUT \"repos/$repo/contents/$dest\" --input -;if($LASTEXITCODE -ne 0){throw 'GitHub runtime-log upload failed'};Write-Host \"Uploaded exact $build LogOutput.log SHA-256 $localSha\" -ForegroundColor Green"
activation = f"""# S1.42AK-BMDSFIX1 Runtime Activation

**Date:** 2026-09-24
**Status:** PUBLISHED ON MAIN / ACTIVE GAMEPLAY RUNTIME CANDIDATE / TEST OUTSTANDING / NOT ACCEPTED
**Accepted gameplay baseline:** S1.42AK — unchanged
**Candidate:** S1.42AK-BMDSFIX1 — {TITLE}
**Candidate profile:** `{PROFILE}`
**Candidate SHA-256:** `{PROFILE_SHA}`
**BMDSFIX1 DLL SHA-256:** `{DLL_SHA}`
**Exact parent:** accepted S1.42AK / `{BASE_SHA}`
**Main integration:** PR #150 / exact head `24713dfc93a24f5e65ae5f223d3ea9c164da785e` / merge `21138185f1ab377660b61120f1d07733d4180672`

## Activation decision

The exact reviewed, exact-byte-published and main-integrated BMDSFIX1 artifact is authorized as the active gameplay runtime-evidence candidate for the bounded Black Mesa x `DeepSewersFlow` generation-size mitigation gate. S1.42AK remains the accepted rollback baseline. BMDSFIX1 is latest/active but is not accepted until a later explicit runtime decision.

No gameplay, config, package, profile or plugin bytes are created or changed by this activation. `BuildSpecs/current.json` remains disabled and guards the exact active candidate. `RuntimeInbox/ACTIVE_BUILD.txt`, `Current/AUTO_BUILD_RESULT.json`, `CURRENT_STATE.latest_built_artifact` and `active_candidate` all bind the exact same BMDSFIX1 profile, so the canonical Gale launcher resolves through its normal active-build path.

## Exact runtime identities

- profile SHA-256: `{PROFILE_SHA}`;
- BMDSFIX1 DLL SHA-256: `{DLL_SHA}`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c`;
- accepted S1.42AB normalizer SHA-256: `901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06`;
- archive/index members: 337;
- package/config drift: zero.

## Runtime qualification contract

A sufficient run must establish all of the following:

1. `[BMDSFIX1] ARMED` appears without `[BMDSFIX1] REFUSED TO ARM`;
2. Black Mesa selects `DeepSewersFlow`;
3. `[BMDSFIX1] APPLIED Black Mesa / DeepSewersFlow multiplier=...->1` appears;
4. LLL/DunGen completes generation and `Players finished generating the new floor` appears;
5. the prior persistent `Entering the atmosphere` state clears and normal landed gameplay begins;
6. no persistent retry flood equivalent to the failing 4.875 run remains;
7. at least one non-target generation demonstrates no BMDSFIX1 application marker and no unintended size mutation;
8. no new severe target-attributable generation, entrance, routing or NavMesh regression appears.

This does not qualify Black Mesa x Greenhouse. That remains a separate `NOT_YET_PROVEN` successor-diagnostic scope.

## Exact Gale replacement/import one-liner

```powershell
{gale}
```

The launcher must resolve `{BUILD_ID}` through the normal `ACTIVE_BUILD == AUTO_BUILD_RESULT.build_id` path and verify the exact downloaded profile SHA before Gale import. Follow its numeric old-profile selection and explicit `y` deletion confirmation; do not manually substitute another profile.

## Exact build-specific runtime-log uploader

After the gameplay run is complete, run this single PowerShell line. It resolves/bootstrap `gh`, authenticates if required, verifies the exact local BMDSFIX1 `LogOutput.log` by path/non-empty content/marker, computes SHA-256, and creates or replaces `RuntimeInbox/Current/LogOutput.log` on `main` without a local repository clone.

```powershell
{uploader}
```

The normal runtime-ingest workflow then attributes the evidence to BMDSFIX1 through `RuntimeInbox/ACTIVE_BUILD.txt`. If gameplay has already completed and only upload remains, do not repeat gameplay solely for evidence submission.

## Preserved boundaries

- accepted baseline remains S1.42AK;
- S1.42AB InteriorWeightNormalization remains unchanged;
- Black Mesa remains Dawn/native-owned and is not duplicate-registered;
- Greenhouse availability and classification remain unchanged;
- the 30x53 B3 matrix remains unchanged until evidence justifies reclassification;
- Shatteredrooms x Experimentation/Embrion remain untouched;
- no universal interior override or Black-Mesa/Pikmin routing repair is authorized.

## Evidence attribution and rollback

Runtime evidence must be uploaded while `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD_ID}`. Runtime-active status never promotes or accepts the candidate. Rollback remains exact accepted S1.42AK through the same canonical Gale replacement workflow after the BMDSFIX1 gate is decided.
"""
(ROOT / ACTIVATION).write_text(activation, encoding="utf-8")

print("PASS: prepared exact BMDSFIX1 active runtime-candidate lifecycle state without changing gameplay/config/package/profile/plugin bytes")
