#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_ID = "S1.42AK-BMDSFIX1-DIAG1"
PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector.r2z"
PROFILE_SHA = "31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e"
DLL_SHA = "3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1"
DLL_ENTRY = "BepInEx/plugins/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.dll"
BASE_BUILD_ID = "S1.42AK-BMDSFIX1"
BASE_PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
BASE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
BMDSFIX1_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
BMDSFIX1_DLL_ENTRY = "BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"
ACTIVATION = "Current/180_S1.42AK_BMDSFIX1_DIAG1_RUNTIME_ACTIVATION.md"
BUILD_PLAN = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_PLAN.md"
BUILD_RESULT = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC_EVIDENCE = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
PUBLICATION_EVIDENCE = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
REVIEW_CHECKPOINT = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, data) -> None:
    (ROOT / rel).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(rel: str) -> str:
    h = hashlib.sha256()
    with (ROOT / rel).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected exactly one replacement target, found {count}")
    return text.replace(old, new, 1)


# Fail closed on the exact post-publication, pre-activation state.
state = load_json("Current/CURRENT_STATE.json")
require(state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(state["latest_built_artifact"]["build_id"] == BASE_BUILD_ID, "Latest artifact drift")
require(state["latest_built_artifact"]["sha256"] == BASE_SHA, "Latest artifact SHA drift")
require(isinstance(state.get("active_candidate"), dict), "BMDSFIX1 gameplay candidate is missing")
require(state["active_candidate"]["build_id"] == BASE_BUILD_ID, "Gameplay candidate drift")
require(state["active_candidate"]["sha256"] == BASE_SHA, "Gameplay candidate SHA drift")
require(state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED", "Gameplay candidate status drift")
require(state["runtime_test_outstanding"] is True, "Regular BMDSFIX1 runtime gate must remain outstanding")
require(state["selected_scope"]["candidate_build_id"] == BASE_BUILD_ID, "Selected-scope candidate drift")
require(state["selected_scope"]["bmdsfix1_target_status"] == "OUTSTANDING_BLACK_MESA_DEEP_SEWERS", "BMDSFIX1 target gate drift")
require(state["controllers"]["runtime_active_build"] == BASE_BUILD_ID, "Runtime controller was already redirected")
require((ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == BASE_BUILD_ID, "ACTIVE_BUILD drift")

current_spec = load_json("BuildSpecs/current.json")
require(current_spec["enabled"] is False, "Build controller must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Build controller identity drift")
require(current_spec["base_profile"] == BASE_PROFILE and current_spec["base_sha256"] == BASE_SHA, "Build controller parent guard drift")

auto_result = load_json("Current/AUTO_BUILD_RESULT.json")
require(auto_result["build_id"] == BASE_BUILD_ID, "AUTO_BUILD_RESULT is not BMDSFIX1")
require(auto_result["output_profile"] == BASE_PROFILE and auto_result["output_sha256"] == BASE_SHA, "AUTO_BUILD_RESULT BMDSFIX1 identity drift")

require(sha256_file(BASE_PROFILE) == BASE_SHA, "Exact BMDSFIX1 parent profile SHA mismatch")
require(sha256_file(PROFILE) == PROFILE_SHA, "Exact DIAG1 profile SHA mismatch")
build_result = load_json(BUILD_RESULT)
require(build_result["build_id"] == BUILD_ID, "DIAG1 build result ID drift")
require(build_result["base_profile"] == BASE_PROFILE and build_result["base_sha256"] == BASE_SHA, "DIAG1 build-result parent drift")
require(build_result["output_profile"] == PROFILE and build_result["output_sha256"] == PROFILE_SHA, "DIAG1 build-result output drift")
require(build_result["zip_members"] == 338, "DIAG1 archive member count drift")
require(build_result["changed_existing_members"] == ["export.r2x"], "DIAG1 changed-member contract drift")
require(build_result["added_members"] == [DLL_ENTRY], "DIAG1 added-member contract drift")
require(build_result.get("mod_state_changes") == [] and build_result.get("mod_additions") == [] and build_result.get("mod_removals") == [], "DIAG1 package/mod delta drift")

with zipfile.ZipFile(ROOT / PROFILE, "r") as archive:
    require(len(archive.infolist()) == 338, "DIAG1 materialized archive member count drift")
    require(DLL_ENTRY in archive.namelist(), "DIAG1 DLL missing from exact profile")
    require(BMDSFIX1_DLL_ENTRY in archive.namelist(), "Inherited BMDSFIX1 DLL missing from DIAG1 profile")
    require(hashlib.sha256(archive.read(DLL_ENTRY)).hexdigest() == DLL_SHA, "DIAG1 DLL SHA mismatch")
    require(hashlib.sha256(archive.read(BMDSFIX1_DLL_ENTRY)).hexdigest() == BMDSFIX1_DLL_SHA, "Inherited BMDSFIX1 DLL SHA mismatch")

expected_hashes = load_json("Profiles/EXPECTED_HASHES.json")
require(PROFILE in expected_hashes, "DIAG1 EXPECTED_HASHES mapping missing")
require(expected_hashes[PROFILE]["build_id"] == BUILD_ID and expected_hashes[PROFILE]["sha256"] == PROFILE_SHA, "DIAG1 EXPECTED_HASHES identity drift")

# The prior Greenhouse diagnostics are historical evidence only. The active diagnostic pointer
# is repointed to the independently versioned BMDSFIX1-DIAG1 overlay; their evidence records remain untouched.
scope = state["selected_scope"]
old_diag = scope.get("diagnostic_revision")
require(isinstance(old_diag, dict) and old_diag.get("build_id") == "S1.42AK-BMGHDIAG2", "Unexpected pre-activation diagnostic pointer")
require(old_diag.get("runtime_validation_status") == "RUNTIME_EVIDENCE_INGESTED_DIAGNOSTIC_REFUSED_BEFORE_ARMING_QUALIFICATION_INCONCLUSIVE_NOT_ACCEPTED", "Historical BMGHDIAG2 state drift")

scope["diagnostic_build_plan"] = BUILD_PLAN
scope["diagnostic_static_evidence"] = STATIC_EVIDENCE
scope["diagnostic_publication_evidence"] = PUBLICATION_EVIDENCE
scope["diagnostic_runtime_activation"] = ACTIVATION
scope["diagnostic_revision"] = {
    "build_id": BUILD_ID,
    "status": "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
    "base_build_id": BASE_BUILD_ID,
    "base_profile": BASE_PROFILE,
    "base_sha256": BASE_SHA,
    "build_plan": BUILD_PLAN,
    "static_evidence": STATIC_EVIDENCE,
    "review_checkpoint": REVIEW_CHECKPOINT,
    "review_pr": 154,
    "reviewed_head": "87154ea28b0167a6d4e435f04620978926565e85",
    "review_merge_ref": "476e69887030005d455b50a7c85ea8a6f11d5da6",
    "review_run": 36051334448,
    "review_artifact_id": 10830821692,
    "review_artifact_zip_sha256": "53787c9e943a297996f5cb0f81d6a9e783ad23abc4a7d642ab45b449ed6419d7",
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "bmdsfix1_dll_sha256": BMDSFIX1_DLL_SHA,
    "lll_sha256": "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
    "normalizer_sha256": "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
    "archive_members_verified": 338,
    "added_members": [DLL_ENTRY],
    "changed_existing_members": ["export.r2x"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "published": True,
    "runtime_armed": True,
    "profile": PROFILE,
    "profile_sources": "ProfileSources/S1.42AK-BMDSFIX1-DIAG1/",
    "file_index": "ProfileSources/S1.42AK-BMDSFIX1-DIAG1/FILE_INDEX.json",
    "build_result": BUILD_RESULT,
    "publication_evidence": PUBLICATION_EVIDENCE,
    "publication_branch": "c3f18-bmdsfix1-diag1-exact-publication",
    "publication_workflow_run": 36052888788,
    "published_profile_commit": "3a04ddcc361ff439aaf930633ccf492f7381ad82",
    "main_integrated": True,
    "integration_pr": 155,
    "main_integration_commit": "0b3f5347fd642855122ca8ef9ef61eaa7daf6845",
    "index_reconciliation": "Current/179_S1.42AK_BMDSFIX1_DIAG1_PROFILE_INDEX_MAPPING_RECONCILIATION.md",
    "activation_record": ACTIVATION,
    "runtime_role": "DIAGNOSTIC_ONLY_DETERMINISTIC_BLACK_MESA_DEEP_SEWERS_SELECTOR_SUPPORTING_EVIDENCE_NEVER_ACCEPT",
    "runtime_validation_status": "RUNTIME_TEST_OUTSTANDING_SUPPORTING_EVIDENCE_ONLY_NOT_ACCEPTED"
}
scope["status"] = "PHASE_C3F18_BMDSFIX1_DIAG1_RUNTIME_ACTIVE_SUPPORTING_EVIDENCE_OUTSTANDING"
scope["finding"] = (
    "Exact published and profile-index-reconciled S1.42AK-BMDSFIX1-DIAG1 bytes are now the active diagnostic runtime target solely to deterministically select Black Mesa x DeepSewersFlow and collect supporting target evidence. "
    "The diagnostic profile remains SHA-256 31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e with diagnostic DLL SHA-256 3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1 over the exact BMDSFIX1 parent 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0. "
    "S1.42AK-BMDSFIX1 remains the active gameplay candidate and remains not accepted; its regular exact-byte Black Mesa x DeepSewersFlow qualification is not waived or replaced by DIAG1. BuildSpecs/current.json remains disabled and no profile, DLL, config or package bytes are changed by activation."
)
scope["analysis_contract"] = (
    "Keep S1.42AK-BMDSFIX1 as the active gameplay candidate / not accepted and treat S1.42AK-BMDSFIX1-DIAG1 only as the active diagnostic runtime overlay for deterministic supporting Black Mesa x DeepSewersFlow evidence. "
    "Require [BMDSFIX1-DIAG1] ARMED without refusal, [BMDSFIX1-DIAG1] SELECTED Black Mesa / DeepSewersFlow with normalized rarity=100 and pool N->1, the inherited [BMDSFIX1] ARMED and target APPLIED multiplier ->1 markers, completed dungeon generation and normal landed gameplay without the prior persistent retry/Entering-the-atmosphere failure or a new severe target-attributable regression. "
    "Never accept DIAG1, never infer BMDSFIX1 acceptance from DIAG1 evidence, never waive the regular exact-byte BMDSFIX1 target gate, and do not mix the separate Black Mesa x Greenhouse/BMGHDIAG scope into this diagnostic."
)
scope["next_action"] = (
    "Import exact active S1.42AK-BMDSFIX1-DIAG1 through the canonical repository-driven Gale v2.4 launcher, run the bounded diagnostic on Black Mesa, and capture deterministic DeepSewersFlow selection plus inherited BMDSFIX1 application/generation/landing evidence. Then upload that run's exact BepInEx/LogOutput.log with the DIAG1 build-specific uploader. Treat the result as supporting diagnostic evidence only; the regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding until separately satisfied."
)
state["controllers"]["runtime_active_build"] = BUILD_ID
state["next_action"] = scope["next_action"]
write_json("Current/CURRENT_STATE.json", state)
(ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID + "\n", encoding="utf-8")

# Keep the gameplay candidate pending entry and add an independent active diagnostic pending entry.
integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
completed_ids = {x.get("build_id") for x in integrity.get("profiles", []) if isinstance(x, dict)}
pending_ids = {x.get("build_id") for x in integrity.get("pending_profiles", []) if isinstance(x, dict)}
require(BUILD_ID not in completed_ids and BUILD_ID not in pending_ids, "DIAG1 already registered as runtime evidence")
require(BASE_BUILD_ID in pending_ids, "BMDSFIX1 candidate pending evidence entry missing")
integrity["updated"] = "2026-09-24"
integrity["last_validated"] = "2026-09-24"
integrity["pending_profiles"].append({
    "build_id": BUILD_ID,
    "role": "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
    "profile": PROFILE,
    "profile_sha256": PROFILE_SHA,
    "profile_sources": "ProfileSources/S1.42AK-BMDSFIX1-DIAG1/",
    "file_index": "ProfileSources/S1.42AK-BMDSFIX1-DIAG1/FILE_INDEX.json",
    "export": "ProfileSources/S1.42AK-BMDSFIX1-DIAG1/export.r2x",
    "build_plan": BUILD_PLAN,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC_EVIDENCE,
    "publication_evidence": PUBLICATION_EVIDENCE,
    "activation_record": ACTIVATION,
    "diagnostic_dll_sha256": DLL_SHA,
    "inherited_bmdsfix1_dll_sha256": BMDSFIX1_DLL_SHA,
    "runtime_evidence_required": False,
    "partial_runtime_evidence_present": False,
    "note": "Exact published/indexed DIAG1 bytes are runtime-armed only as a deterministic Black Mesa x DeepSewersFlow selector over the still-unaccepted BMDSFIX1 gameplay candidate. Supporting diagnostic evidence cannot satisfy or waive regular exact-byte BMDSFIX1 qualification."
})
integrity.setdefault("verified_repository_api_observations", []).append(
    "S1.42AK-BMDSFIX1-DIAG1 exact profile SHA-256 31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e is runtime-armed solely as a supporting deterministic Deep Sewers diagnostic over exact BMDSFIX1; BMDSFIX1 remains the unaccepted gameplay candidate and its regular target gate remains outstanding."
)
write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

# Human artifact-integrity router.
path = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
text = path.read_text(encoding="utf-8")
old = "- **S1.42AK-BMDSFIX1** — active gameplay runtime candidate directly over accepted S1.42AK; profile SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`; BMDSFIX1 DLL SHA-256 `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`; runtime evidence outstanding; not accepted."
new = old + "\n- **S1.42AK-BMDSFIX1-DIAG1** — active diagnostic runtime target over exact BMDSFIX1; profile SHA-256 `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`; DIAG1 DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; supporting deterministic Deep Sewers evidence only; never a gameplay base or acceptance candidate."
text = replace_once(text, old, new, "artifact pending profiles")
old = "BMDSFIX1 exact reviewed bytes are published and main-integrated. Runtime activation changes only lifecycle/controller/evidence routing; no gameplay/config/package/profile/plugin bytes are regenerated or altered. The candidate is scoped only to Black Mesa x `DeepSewersFlow`. Black Mesa x Greenhouse remains separate and unproven."
new = "BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. `RuntimeInbox/ACTIVE_BUILD.txt` now points to exact DIAG1 solely for Gale target resolution and diagnostic evidence attribution; activation changes only lifecycle/controller/evidence routing and regenerates no gameplay/config/package/profile/plugin bytes. DIAG1 may supply supporting deterministic Black Mesa x `DeepSewersFlow` evidence but cannot qualify or accept BMDSFIX1. Black Mesa x Greenhouse remains separate and unproven."
text = replace_once(text, old, new, "artifact activation boundary")
path.write_text(text, encoding="utf-8")

# Current knowledge-map anchor.
path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
text = path.read_text(encoding="utf-8")
old = "`BuildSpecs/current.json` remains disabled while guarding the candidate, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task."
new = "`BuildSpecs/current.json` remains disabled while guarding the exact BMDSFIX1 candidate. The separately published/indexed `S1.42AK-BMDSFIX1-DIAG1` is now the active diagnostic runtime target and `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1` solely for Gale resolution/evidence attribution. BMDSFIX1 remains the active gameplay candidate / not accepted, its regular Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task."
text = replace_once(text, old, new, "knowledge-map DIAG1 activation")
path.write_text(text, encoding="utf-8")

# Current lifecycle router.
path = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
text = path.read_text(encoding="utf-8")
old_live = "- Active diagnostic runtime target: **none**.\n- Runtime test outstanding: **yes — remaining Black Mesa x DeepSewersFlow target qualification only**.\n- Preserved partial evidence: **Black Mesa x Substation non-target control PASS** at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/`.\n- Selected scope: **Universal Interior Viability / Equal Availability — BMDSFIX1 partial runtime evidence ingested; target evidence outstanding**.\n- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 candidate bytes.\n- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`.\n- S1.42AK remains the accepted rollback baseline; no Greenhouse diagnostic is armed."
new_live = "- Active diagnostic runtime target: **S1.42AK-BMDSFIX1-DIAG1 — diagnostic only / never accept**.\n- Runtime test outstanding: **yes — immediate DIAG1 supporting run is armed; regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived**.\n- Preserved partial evidence: **Black Mesa x Substation non-target control PASS** at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/`.\n- Selected scope: **Universal Interior Viability / Equal Availability — deterministic BMDSFIX1-DIAG1 supporting target evidence next; gameplay candidate unchanged**.\n- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 candidate bytes.\n- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1` for diagnostic target resolution/evidence attribution only.\n- S1.42AK remains the accepted rollback baseline; BMDSFIX1 remains the unaccepted gameplay candidate; Greenhouse/BMGHDIAG remains separate."
text = replace_once(text, old_live, new_live, "lifecycle live execution state")
old_next = "Keep exact active S1.42AK-BMDSFIX1 bytes unchanged and run only the remaining Black Mesa x DeepSewersFlow target gate: obtain a target selection showing [BMDSFIX1] ARMED and APPLIED with multiplier ->1, completed dungeon generation and normal landed gameplay without the prior persistent retry/Entering-the-atmosphere failure or a new severe target-attributable regression. Upload that run's exact BepInEx/LogOutput.log with the existing build-specific uploader. The already-ingested Black Mesa x Substation run is the preserved non-target control and does not need to be repeated solely for qualification."
new_next = "Import exact active S1.42AK-BMDSFIX1-DIAG1 through the canonical Gale v2.4 launcher and run the bounded Black Mesa diagnostic. Require `[BMDSFIX1-DIAG1] ARMED` without refusal, deterministic `[BMDSFIX1-DIAG1] SELECTED Black Mesa / DeepSewersFlow; normalized rarity=100; pool=<N>->1`, inherited `[BMDSFIX1] ARMED` and target `APPLIED ... ->1`, completed generation and normal landed gameplay without the prior persistent retry/Entering-the-atmosphere failure or a new severe target-attributable regression. Upload that run's exact `BepInEx/LogOutput.log` with the DIAG1 uploader. This is supporting diagnostic evidence only: BMDSFIX1 remains not accepted and its regular exact-byte Black Mesa x DeepSewersFlow qualification is not waived."
text = replace_once(text, old_next, new_next, "lifecycle next action")
old_perm = "The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. BMDSFIX1 now resolves through the normal active-candidate path because `Current/AUTO_BUILD_RESULT.json`, `CURRENT_STATE.latest_built_artifact`, `active_candidate` and `RuntimeInbox/ACTIVE_BUILD.txt` all bind the same exact `S1.42AK-BMDSFIX1` profile SHA. Runtime activation does not accept the candidate; only later runtime evidence and an explicit decision can do so."
new_perm = "The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. DIAG1 now resolves through the explicit direct-diagnostic path: `RuntimeInbox/ACTIVE_BUILD.txt` and `CURRENT_STATE.controllers.runtime_active_build` bind `selected_scope.diagnostic_revision`, whose exact parent is `Current/AUTO_BUILD_RESULT.json = S1.42AK-BMDSFIX1`. This diagnostic routing changes no BMDSFIX1 bytes, does not promote DIAG1, and cannot accept BMDSFIX1."
text = replace_once(text, old_perm, new_perm, "lifecycle Gale path")
path.write_text(text, encoding="utf-8")

# Roadmap live selected-scope routing. Greenhouse text is intentionally left untouched.
path = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
text = path.read_text(encoding="utf-8")
old = "Latest built artifact and active gameplay runtime candidate is **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`; `BuildSpecs/current.json` remains disabled while guarding the exact candidate; one bounded runtime test is outstanding."
new = "Latest built artifact and active gameplay runtime candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted. Exact `S1.42AK-BMDSFIX1-DIAG1` is now the active diagnostic runtime overlay, so `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1` solely for Gale resolution/evidence attribution; `BuildSpecs/current.json` remains disabled while guarding the exact BMDSFIX1 candidate. The diagnostic run is supporting evidence only and does not waive the regular BMDSFIX1 target gate."
text = replace_once(text, old, new, "roadmap current position")
text = replace_once(text, "**Universal Interior Viability / Equal Availability — SELECTED / BMDSFIX1 RUNTIME ACTIVE / EVIDENCE OUTSTANDING.**", "**Universal Interior Viability / Equal Availability — SELECTED / BMDSFIX1-DIAG1 SUPPORTING RUNTIME ACTIVE / GAMEPLAY QUALIFICATION STILL OUTSTANDING.**", "roadmap selected scope")
old = "Import exact active S1.42AK-BMDSFIX1 through the canonical repository-driven Gale v2.4 launcher. Run the bounded BMDSFIX1 runtime gate: obtain one Black Mesa x DeepSewersFlow generation showing [BMDSFIX1] ARMED and APPLIED with multiplier ->1, successful generation/landing without the prior persistent retry flood, and at least one non-target generation showing no BMDSFIX1 application or size mutation. Then upload that run's exact BepInEx/LogOutput.log with the build-specific one-line uploader. Do not alter profile/config/package/plugin bytes during the test."
new = "Import exact active S1.42AK-BMDSFIX1-DIAG1 through the canonical repository-driven Gale v2.4 launcher. Run one bounded Black Mesa diagnostic to obtain `[BMDSFIX1-DIAG1] ARMED`, deterministic DeepSewersFlow selection, inherited `[BMDSFIX1] APPLIED ... ->1`, completed generation and normal landing without the prior persistent retry failure or a new severe target-attributable regression, then upload that exact `BepInEx/LogOutput.log` with the DIAG1 uploader. Do not alter profile/config/package/plugin bytes. This diagnostic never becomes a gameplay build and does not satisfy or waive the separate regular exact-byte BMDSFIX1 qualification."
text = replace_once(text, old, new, "roadmap next action")
path.write_text(text, encoding="utf-8")

activation_text = r'''# S1.42AK-BMDSFIX1-DIAG1 Runtime Activation

**Date:** 2026-09-24  
**Status:** PUBLISHED / INDEXED / ACTIVE DIAGNOSTIC RUNTIME TARGET / SUPPORTING TEST OUTSTANDING / NEVER ACCEPT  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted  
**Diagnostic:** S1.42AK-BMDSFIX1-DIAG1  
**Diagnostic profile:** `Profiles/LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector.r2z`  
**Diagnostic profile SHA-256:** `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`  
**Diagnostic DLL SHA-256:** `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`  
**Exact BMDSFIX1 parent SHA-256:** `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`

## Activation decision

The already reviewed, exact-byte-published, main-integrated and profile-index-reconciled DIAG1 artifact is authorized as the active **diagnostic-only** runtime target for one bounded deterministic Black Mesa x `DeepSewersFlow` supporting-evidence run.

Activation changes only lifecycle/controller/evidence routing. It does not rebuild or alter the DIAG1 profile, either project DLL, any package, any config, or the exact BMDSFIX1 gameplay candidate. `BuildSpecs/current.json` remains disabled and pinned to exact BMDSFIX1.

S1.42AK-BMDSFIX1 remains `ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED`. DIAG1 is **NEVER ACCEPT** and cannot be promoted into gameplay lineage. A DIAG1 runtime cannot itself accept BMDSFIX1 and cannot waive or replace the regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification contract.

## Canonical direct-diagnostic chain

The Gale v2.4 direct-diagnostic resolver is intentionally used:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1`

-> `CURRENT_STATE.controllers.runtime_active_build`

-> `CURRENT_STATE.selected_scope.diagnostic_revision`

-> `BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json`

-> exact parent `Current/AUTO_BUILD_RESULT.json = S1.42AK-BMDSFIX1` / SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`.

No one-hop diagnostic parent is required because DIAG1 derives directly from the current exact BMDSFIX1 `AUTO_BUILD_RESULT`.

## Supporting runtime contract

Run the exact diagnostic on **Black Mesa**. The bounded supporting run should establish:

1. `[BMDSFIX1-DIAG1] ARMED` with no `REFUSED TO ARM` marker;
2. `[BMDSFIX1-DIAG1] SELECTED Black Mesa / DeepSewersFlow; normalized rarity=100; pool=<N>->1` with no `REFUSED selection` marker;
3. inherited `[BMDSFIX1] ARMED`;
4. target `[BMDSFIX1] APPLIED` with the Black Mesa / `DeepSewersFlow` multiplier reduced to `1`;
5. completed dungeon generation;
6. normal landed gameplay without the prior persistent retry / `Entering the atmosphere` failure or a new severe target-attributable regression.

This is deterministic **supporting diagnostic evidence**, not regular exact-byte BMDSFIX1 qualification, because the runtime profile additionally contains the DIAG1 selector DLL and DIAG1 profile identity.

The already-ingested Black Mesa x Substation BMDSFIX1 run remains the preserved non-target control. It need not be repeated solely for this diagnostic. Black Mesa x Greenhouse/BMGHDIAG remains a separate scope and is not part of this runtime gate.

## Exact Gale replacement/import one-liner

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

The launcher must resolve the direct diagnostic chain above, download the exact DIAG1 `.r2z`, verify SHA-256 `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`, and preserve the existing fail-closed Gale/materialization checks.

## Exact build-specific runtime-log uploader

After the diagnostic gameplay run is complete, run this single PowerShell line. It bootstraps/resolves `gh`, authenticates if required, verifies the exact DIAG1 local `LogOutput.log` by path/non-empty content/diagnostic marker, computes its SHA-256, and creates or replaces `RuntimeInbox/Current/LogOutput.log` on `main` without requiring a local repository clone.

```powershell
$ErrorActionPreference='Stop';$build='S1.42AK-BMDSFIX1-DIAG1';$log='C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $log -PathType Leaf)){throw "Expected runtime log not found: $log"};$bytes=[IO.File]::ReadAllBytes($log);if($bytes.Length -le 0){throw 'Runtime log is empty'};$text=[Text.Encoding]::UTF8.GetString($bytes);if($text.IndexOf('[BMDSFIX1-DIAG1]',[StringComparison]::Ordinal) -lt 0){throw 'Refusing upload: exact local LogOutput.log contains no [BMDSFIX1-DIAG1] marker'};$localSha=([BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($bytes))).Replace('-','').ToLowerInvariant();$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;$fallback=Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe';if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback};if(!$gh -and (Get-Command winget -ErrorAction SilentlyContinue)){winget install --id GitHub.cli -e --source winget --accept-source-agreements --accept-package-agreements | Out-Host;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback}};if(!$gh){throw 'GitHub CLI (gh) could not be resolved or bootstrapped'};& $gh auth status -h github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login -h github.com -w;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dest='RuntimeInbox/Current/LogOutput.log';$existing=$null;try{$existing=(& $gh api "repos/$repo/contents/$dest?ref=main" --jq '.sha' 2>$null)}catch{};$payload=@{message="Upload $build runtime log ($localSha)";content=[Convert]::ToBase64String($bytes);branch='main'};if($existing){$payload.sha=$existing};$json=$payload|ConvertTo-Json -Compress;$json|& $gh api --method PUT "repos/$repo/contents/$dest" --input -;if($LASTEXITCODE -ne 0){throw 'GitHub runtime-log upload failed'};Write-Host "Uploaded exact $build LogOutput.log SHA-256 $localSha" -ForegroundColor Green
```

The normal runtime-ingest workflow will attribute the uploaded evidence to `S1.42AK-BMDSFIX1-DIAG1` through `RuntimeInbox/ACTIVE_BUILD.txt`. If the diagnostic run has already completed and only upload remains, do not repeat gameplay solely for evidence submission.

## Preserved boundaries

- accepted gameplay baseline remains S1.42AK;
- active gameplay candidate remains exact S1.42AK-BMDSFIX1 / not accepted;
- regular BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived;
- exact BMDSFIX1 and DIAG1 profile/DLL bytes are unchanged;
- package/config changes are zero;
- `BuildSpecs/current.json` remains disabled and guards exact BMDSFIX1;
- Black Mesa x Greenhouse/BMGHDIAG remains separate;
- no universal interior override is authorized.

## Post-diagnostic boundary

After DIAG1 evidence is ingested and decided, runtime routing must return to the exact BMDSFIX1 gameplay candidate before any regular BMDSFIX1 qualification run. DIAG1 evidence may support the diagnosis of the target pair but never substitutes for that exact-byte gameplay gate.
'''
(ROOT / ACTIVATION).write_text(activation_text, encoding="utf-8")

print("PASS: staged exact BMDSFIX1-DIAG1 diagnostic runtime activation; gameplay candidate and all artifact bytes preserved")
