#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BUILD_ID = "S1.42AK-BMGHDIAG3"
PROFILE_NAME = "LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic"
PROFILE = f"Profiles/{PROFILE_NAME}.r2z"
PROFILE_SHA = "7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace"
DLL_SHA = "d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
BASE_ID = "S1.42AK"
BASE_PROFILE = "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
CANDIDATE_ID = "S1.42AK-BMDSFIX1"
CANDIDATE_PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
CANDIDATE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
ACTIVATION = "Current/198_S1.42AK_BMGHDIAG3_RUNTIME_ACTIVATION.md"
BUILD_PLAN = "BuildSpecs/S1.42AK-BMGHDIAG3_PLAN.md"
BUILD_RESULT = "BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC = "BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
PUBLICATION = "BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
PROFILE_SOURCES = "ProfileSources/S1.42AK-BMGHDIAG3/"
FILE_INDEX = PROFILE_SOURCES + "FILE_INDEX.json"
PROFILE_INDEX = PROFILE_SOURCES + "PROFILE_INDEX_RESULT.json"
GALE_OLD_REV = "2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain"
GALE_NEW_REV = "2026-09-28-import-uia-v2.4.3-accepted-baseline-direct-diagnostic-chain"


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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    (ROOT / rel).write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Fail closed on exact pre-activation authority and byte identity.
# ---------------------------------------------------------------------------
state = load_json("Current/CURRENT_STATE.json")
require(state["accepted_baseline"]["build_id"] == BASE_ID, "Accepted baseline ID drift")
require(state["accepted_baseline"]["profile"] == BASE_PROFILE, "Accepted baseline profile drift")
require(state["accepted_baseline"]["sha256"] == BASE_SHA, "Accepted baseline SHA drift")
require(state["latest_built_artifact"]["build_id"] == CANDIDATE_ID, "Latest built artifact drift")
require(state["latest_built_artifact"]["profile"] == CANDIDATE_PROFILE, "Latest built profile drift")
require(state["latest_built_artifact"]["sha256"] == CANDIDATE_SHA, "Latest built SHA drift")
require(state["active_candidate"]["build_id"] == CANDIDATE_ID, "Active gameplay candidate drift")
require(state["active_candidate"]["sha256"] == CANDIDATE_SHA, "Active gameplay candidate SHA drift")
require(state["runtime_test_outstanding"] is True, "BMDSFIX1 passive runtime gate must remain outstanding")
require(state["controllers"]["runtime_active_build"] == CANDIDATE_ID, "Pre-activation runtime controller drift")
require((ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == CANDIDATE_ID, "ACTIVE_BUILD drift")
current = load_json("BuildSpecs/current.json")
require(current["enabled"] is False, "BuildSpecs/current.json must remain disabled")
require(current["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Build controller ID drift")
require(current["base_profile"] == CANDIDATE_PROFILE and current["base_sha256"] == CANDIDATE_SHA, "Build controller base drift")
auto = load_json("Current/AUTO_BUILD_RESULT.json")
require(auto["build_id"] == CANDIDATE_ID, "AUTO_BUILD_RESULT must remain BMDSFIX1")
require(auto["output_profile"] == CANDIDATE_PROFILE and auto["output_sha256"] == CANDIDATE_SHA, "AUTO_BUILD_RESULT identity drift")

scope = state["selected_scope"]
require("BMGHDIAG3_PROFILE_INDEX_RECONCILED_RUNTIME_ACTIVATION_NEXT" in scope["status"], "Unexpected lifecycle phase")
old_diag = copy.deepcopy(scope["diagnostic_revision"])
require(old_diag["build_id"] == "S1.42AK-BMDSFIX1-DIAG1PATH1", "Expected reconciled DIAG1PATH1 diagnostic_revision before Greenhouse activation")
require(old_diag.get("runtime_armed") is False, "DIAG1PATH1 must not still be runtime-armed")

require(sha256_file(PROFILE) == PROFILE_SHA, "Published BMGHDIAG3 profile SHA mismatch")
build = load_json(BUILD_RESULT)
require(build["build_id"] == BUILD_ID, "BMGHDIAG3 build-result ID drift")
require(build["profile_name"] == PROFILE_NAME, "BMGHDIAG3 profile name drift")
require(build["output_profile"] == PROFILE and build["output_sha256"] == PROFILE_SHA, "BMGHDIAG3 output identity drift")
require(build["base_profile"] == BASE_PROFILE and build["base_sha256"] == BASE_SHA, "BMGHDIAG3 base identity drift")
require(build["zip_members"] == 337, "BMGHDIAG3 archive member count drift")
require(build["changed_existing_members"] == ["export.r2x"], "BMGHDIAG3 changed member set drift")
require(build["added_members"] == ["BepInEx/plugins/S142AKBMGHDiag3/S142AKBMGHDiag3.dll"], "BMGHDIAG3 added member set drift")

indexed = load_json(PROFILE_INDEX)
require(indexed["build_id"] == BUILD_ID, "BMGHDIAG3 profile-index build ID drift")
require(indexed["profile_path"] == PROFILE and indexed["sha256"] == PROFILE_SHA, "BMGHDIAG3 profile-index identity drift")
require(indexed["zip_members"] == 337 and indexed["build_id_resolution"] == "EXPECTED_HASHES", "BMGHDIAG3 profile-index contract drift")

expected = load_json("Profiles/EXPECTED_HASHES.json")
entry = expected.get(PROFILE)
require(entry is not None, "BMGHDIAG3 expected-hash mapping missing")
require(entry["build_id"] == BUILD_ID and entry["sha256"] == PROFILE_SHA, "BMGHDIAG3 expected-hash mapping drift")
require("not runtime-armed by indexing" in entry["note"], "BMGHDIAG3 expected-hash note no longer describes indexed/inactive pre-state")

# ---------------------------------------------------------------------------
# Canonical state transition: active diagnostic over accepted S1.42AK while
# retaining BMDSFIX1 as the separate unaccepted gameplay candidate.
# ---------------------------------------------------------------------------
diag = {
    "build_id": BUILD_ID,
    "status": "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
    "classification": "DIAGNOSTIC_ONLY_NEVER_ACCEPT",
    "base_build_id": BASE_ID,
    "base_profile": BASE_PROFILE,
    "base_sha256": BASE_SHA,
    "profile_name": PROFILE_NAME,
    "profile": PROFILE,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "profile_index_result": PROFILE_INDEX,
    "profile_sha256": PROFILE_SHA,
    "sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "lll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "changed_existing_members": ["export.r2x"],
    "added_members": ["BepInEx/plugins/S142AKBMGHDiag3/S142AKBMGHDiag3.dll"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "build_plan": BUILD_PLAN,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC,
    "publication_evidence": PUBLICATION,
    "source_reconciliation": "Current/194_S1.42AK_BMGHDIAG3_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md",
    "review_checkpoint": "Current/195_S1.42AK_BMGHDIAG3_INACTIVE_REVIEW_BUILD_CHECKPOINT.md",
    "publication_checkpoint": "Current/196_S1.42AK_BMGHDIAG3_EXACT_BYTE_PUBLICATION_CHECKPOINT.md",
    "profile_index_reconciliation": "Current/197_S1.42AK_BMGHDIAG3_PROFILE_INDEX_RECONCILIATION.md",
    "published": True,
    "indexed": True,
    "runtime_armed": True,
    "activation_record": ACTIVATION,
    "runtime_role": "DIAGNOSTIC_ONLY_BLACK_MESA_GREENHOUSE_FORCE_SELECTION_AND_READ_ONLY_ENTRANCE_OBSERVATION_NEVER_ACCEPT",
    "runtime_validation_status": "RUNTIME_TEST_OUTSTANDING_NEVER_ACCEPT",
}
scope["diagnostic_revision"] = diag
scope["diagnostic_build_plan"] = BUILD_PLAN
scope["diagnostic_static_evidence"] = STATIC
scope["diagnostic_publication_evidence"] = PUBLICATION
scope["diagnostic_runtime_activation"] = ACTIVATION
scope["status"] = "PHASE_C3F18_BMDSFIX1_TARGET_QUALIFICATION_PASSIVE_OUTSTANDING_BMGHDIAG3_RUNTIME_ACTIVE_TEST_OUTSTANDING"
scope["finding"] = (
    "S1.42AK-BMGHDIAG3 exact reviewed bytes are published, canonically indexed and now runtime-armed solely as the bounded Black Mesa x Greenhouse diagnostic target. "
    "The active diagnostic profile remains SHA-256 7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace and its DLL remains SHA-256 d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352. "
    "It derives directly from exact accepted S1.42AK, not from BMDSFIX1 or either failed BMGHDIAG predecessor. "
    "S1.42AK-BMDSFIX1 remains the separate active gameplay candidate / not accepted, and its regular exact-byte Black Mesa x DeepSewersFlow qualification remains outstanding, unwaived and passive. "
    "BuildSpecs/current.json remains disabled and pinned to BMDSFIX1. RuntimeInbox/ACTIVE_BUILD.txt now identifies BMGHDIAG3 only for exact Gale target resolution and runtime-evidence attribution. "
    "Black Mesa x Greenhouse remains NOT_YET_PROVEN until this exact diagnostic runtime evidence is ingested and decided."
)
scope["analysis_contract"] = (
    "Treat S1.42AK-BMGHDIAG3 as the active diagnostic runtime target only and NEVER ACCEPT it as gameplay. Preserve exact profile/DLL identities, accepted S1.42AK, the separate unaccepted BMDSFIX1 gameplay candidate, "
    "the passive/unwaived BMDSFIX1 Black Mesa x DeepSewersFlow gate, accepted S1.42AB normalization, Black Mesa Dawn/native ownership, Greenhouse availability, the B3 matrix, Shatteredrooms exclusions and the separate Black-Mesa/Pikmin routing scope. "
    "Do not rebuild or mutate the diagnostic profile/DLL/package/config bytes. The runtime gate must establish BMGHDIAG3 arming, exact Black Mesa Greenhouse selection, generation/topology/traversal evidence and absence of invalidating REFUSED/TOPOLOGY_INCONCLUSIVE markers before any Greenhouse compatibility conclusion."
)
next_action = (
    "Import the exact active S1.42AK-BMGHDIAG3 profile through the canonical repository-driven Gale v2.4 launcher, run one bounded Black Mesa x Greenhouse diagnostic, exercise the main entrance and alternate entrance IDs 1, 2 and 3 in both directions where practical, then upload that run's exact BepInEx/LogOutput.log with the BMGHDIAG3 build-specific one-line uploader. "
    "Do not alter profile/config/package/plugin/gameplay bytes during the test. Treat the result as diagnostic-only / NEVER ACCEPT; do not accept BMDSFIX1 or waive its passive Black Mesa x DeepSewersFlow gate."
)
scope["next_action"] = next_action
phase_c = scope.get("phase_c")
require(isinstance(phase_c, dict), "selected_scope.phase_c missing")
phase_c["bmgdiag3_review_runtime_armed"] = True
phase_c["bmgdiag3_runtime_activation"] = ACTIVATION
phase_c["bmgdiag3_runtime_activation_status"] = "ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_TEST_OUTSTANDING_NEVER_ACCEPT"
phase_c["black_mesa_greenhouse_status"] = "NOT_YET_PROVEN"
state["updated"] = "2026-09-28"
state["runtime_test_outstanding"] = True
state["controllers"]["runtime_active_build"] = BUILD_ID
state["next_action"] = next_action
write_json("Current/CURRENT_STATE.json", state)
(ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID + "\n", encoding="utf-8")

# EXPECTED_HASHES keeps exact bytes but changes the lifecycle note only.
entry["note"] = (
    "Diagnostic-only active runtime target directly over accepted S1.42AK; exact reviewed bytes are published/indexed and the canonical readable snapshot is ProfileSources/S1.42AK-BMGHDIAG3/. "
    "NEVER ACCEPT and never use as a gameplay base; runtime activation authorizes only bounded Black Mesa x Greenhouse diagnostic evidence collection."
)
write_json("Profiles/EXPECTED_HASHES.json", expected)

# Artifact/evidence index: add the active diagnostic without disturbing BMDSFIX1.
integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
require(not any(x.get("build_id") == BUILD_ID for x in integrity.get("profiles", [])), "BMGHDIAG3 unexpectedly already completed")
require(not any(x.get("build_id") == BUILD_ID for x in integrity.get("pending_profiles", [])), "BMGHDIAG3 unexpectedly already pending")
integrity["updated"] = "2026-09-28"
integrity["last_validated"] = "2026-09-28"
integrity["pending_profiles"].append({
    "build_id": BUILD_ID,
    "role": "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
    "profile": PROFILE,
    "profile_sha256": PROFILE_SHA,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "export": PROFILE_SOURCES + "export.r2x",
    "build_plan": BUILD_PLAN,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC,
    "publication_evidence": PUBLICATION,
    "activation_record": ACTIVATION,
    "diagnostic_dll_sha256": DLL_SHA,
    "runtime_evidence_required": False,
    "partial_runtime_evidence_present": False,
    "note": "Exact published/indexed BMGHDIAG3 bytes are runtime-armed solely for bounded Black Mesa x Greenhouse diagnostic qualification. Diagnostic only / NEVER ACCEPT; BMDSFIX1 and its passive Deep Sewers gate are unchanged."
})
integrity.setdefault("verified_repository_api_observations", []).append(
    "S1.42AK-BMGHDIAG3 exact published/indexed profile SHA-256 7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace is runtime-armed only as a direct diagnostic over accepted S1.42AK; it remains NEVER ACCEPT and Black Mesa x Greenhouse remains NOT_YET_PROVEN pending runtime evidence."
)
write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

# Human evidence index.
path = "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
text = read(path)
text = replace_once(text, "**Last-Validated:** 2026-09-25", "**Last-Validated:** 2026-09-28", "artifact integrity date")
old = "- **S1.42AK-BMDSFIX1-DIAG1PATH1** — active diagnostic runtime/evidence target using short identity `LC V1 S1.42AK-D1P1`; profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; inherited DIAG1 selector DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; supporting deterministic Deep Sewers evidence only; never a gameplay base or acceptance candidate."
new = (
    "- **S1.42AK-BMDSFIX1-DIAG1PATH1** — completed supporting diagnostic evidence using short identity `LC V1 S1.42AK-D1P1`; profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; inherited DIAG1 selector DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; not runtime-active and never a gameplay base or acceptance candidate.\n"
    "- **S1.42AK-BMGHDIAG3** — active diagnostic runtime/evidence target directly over accepted S1.42AK; profile SHA-256 `7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace`; diagnostic DLL SHA-256 `d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352`; Black Mesa x Greenhouse evidence outstanding; **NEVER ACCEPT**."
)
text = replace_once(text, old, new, "artifact pending diagnostic list")
old_para = "BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. `RuntimeInbox/ACTIVE_BUILD.txt` now points to exact DIAG1PATH1 solely for Gale target resolution and diagnostic evidence attribution; blocked long-name DIAG1 is retained only as the one-hop parent and must not be rerun. Activation changes only lifecycle/controller/evidence routing and regenerates no gameplay/config/package/profile/plugin bytes. DIAG1PATH1 may supply supporting deterministic Black Mesa x `DeepSewersFlow` evidence but cannot qualify or accept BMDSFIX1. Black Mesa x Greenhouse remains separate and unproven."
new_para = (
    "BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. `RuntimeInbox/ACTIVE_BUILD.txt` now points to exact BMGHDIAG3 solely for Gale target resolution and diagnostic evidence attribution. "
    "DIAG1PATH1 remains completed supporting Deep Sewers evidence and is not runtime-active. BMGHDIAG3 activation changes only lifecycle/controller/evidence routing plus the minimal Gale authority guard needed to resolve a direct diagnostic against accepted S1.42AK while `AUTO_BUILD_RESULT` remains the separate BMDSFIX1 candidate. "
    "No gameplay/config/package/profile/plugin bytes are rebuilt or mutated. BMGHDIAG3 is NEVER ACCEPT, BMDSFIX1 remains not accepted with its passive Deep Sewers gate unwaived, and Black Mesa x Greenhouse remains unproven until runtime evidence is decided."
)
text = replace_once(text, old_para, new_para, "artifact active routing paragraph")
write(path, text)

# Human project router: replace only the stale direct runtime-routing paragraph and date.
path = "Current/PROJECT_KNOWLEDGE_MAP.md"
text = read(path)
text = replace_once(text, "**Last-Validated:** 2026-09-25", "**Last-Validated:** 2026-09-28", "knowledge map date")
old = "DIAG1PATH1 remains diagnostic support only / **NEVER ACCEPT** and cannot qualify BMDSFIX1 because the deterministic selector DLL was present. Runtime/evidence routing is exact `S1.42AK-BMDSFIX1`; DIAG1PATH1 is not runtime-armed. The regular exact-byte gameplay Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived, and no further non-target control is required solely for that gate. The long-name DIAG1 remains preloader-blocked historical provenance and must not be rerun. Black Mesa x Greenhouse/BMGHDIAG remains separate."
new = (
    "DIAG1PATH1 remains diagnostic support only / **NEVER ACCEPT** and cannot qualify BMDSFIX1 because the deterministic selector DLL was present. The regular exact-byte gameplay Black Mesa x `DeepSewersFlow` qualification remains outstanding, unwaived and passive; dedicated blind rerolls remain disallowed. "
    "The exact published/indexed `S1.42AK-BMGHDIAG3` successor is now the active diagnostic runtime/evidence target directly over accepted S1.42AK, with `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG3`. It is **NEVER ACCEPT** and does not replace or accept BMDSFIX1. "
    "Black Mesa x Greenhouse remains `NOT_YET_PROVEN` pending this exact diagnostic run. Activation authority: `Current/198_S1.42AK_BMGHDIAG3_RUNTIME_ACTIVATION.md`."
)
text = replace_once(text, old, new, "knowledge map active routing")
write(path, text)

# Roadmap: reconcile selected runtime overlay without changing scope.
path = "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
text = read(path)
text = replace_once(text, "**Last-Validated:** 2026-09-25", "**Last-Validated:** 2026-09-28", "roadmap date")
old = "Latest built artifact and active gameplay runtime candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted. Exact short-identity `S1.42AK-BMDSFIX1-DIAG1PATH1` is now the active diagnostic runtime/evidence overlay, so `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1PATH1` solely for Gale resolution/evidence attribution; blocked long-name DIAG1 is retained only as its one-hop parent and must not be rerun. `BuildSpecs/current.json` remains disabled while guarding the exact BMDSFIX1 candidate. The diagnostic run is supporting evidence only and does not waive the regular BMDSFIX1 target gate."
new = (
    "Latest built artifact and active gameplay runtime candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted and its exact regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding. "
    "Exact published/indexed `S1.42AK-BMGHDIAG3` is now the active diagnostic runtime/evidence overlay directly over accepted S1.42AK, so `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG3` solely for Gale resolution/evidence attribution. `BuildSpecs/current.json` remains disabled while guarding exact BMDSFIX1. "
    "BMGHDIAG3 is diagnostic only / NEVER ACCEPT and cannot accept BMDSFIX1 or waive the regular Deep Sewers target gate."
)
text = replace_once(text, old, new, "roadmap current position")
text = replace_once(
    text,
    "**Universal Interior Viability / Equal Availability — SELECTED / BMDSFIX1-DIAG1PATH1 SUPPORTING RUNTIME ACTIVE / GAMEPLAY QUALIFICATION STILL OUTSTANDING.**",
    "**Universal Interior Viability / Equal Availability — SELECTED / BMGHDIAG3 GREENHOUSE DIAGNOSTIC RUNTIME ACTIVE / BMDSFIX1 GAMEPLAY QUALIFICATION STILL PASSIVE OUTSTANDING.**",
    "roadmap selected scope status",
)
old = "After this activation is integrated and exact-head validated, import exact active S1.42AK-BMDSFIX1-DIAG1PATH1 through the canonical repository-driven Gale v2.4 launcher. Run one bounded Black Mesa diagnostic to obtain inherited `[BMDSFIX1-DIAG1] ARMED`, deterministic DeepSewersFlow selection, inherited `[BMDSFIX1] APPLIED ... ->1`, completed generation and normal landing without the prior persistent retry failure or a new severe target-attributable regression, then upload that exact `BepInEx/LogOutput.log` with the DIAG1PATH1 uploader. Do not alter profile/config/package/plugin bytes. This diagnostic never becomes a gameplay build and does not satisfy or waive the separate regular exact-byte BMDSFIX1 qualification."
new = (
    "After this repository activation is integrated and exact-head validated, import exact active S1.42AK-BMGHDIAG3 through the canonical repository-driven Gale v2.4 launcher. Run one bounded Black Mesa x Greenhouse diagnostic, establish `[BMGHDIAG3] ARMED`, exact Greenhouse selection, completed generation and topology/traversal evidence, then upload that exact `BepInEx/LogOutput.log` with the BMGHDIAG3 uploader. "
    "Do not alter profile/config/package/plugin/gameplay bytes. This diagnostic is NEVER ACCEPT and does not satisfy, waive or alter the separate regular exact-byte BMDSFIX1 Deep Sewers qualification."
)
text = replace_once(text, old, new, "roadmap next action")
text = replace_once(
    text,
    "- Black Mesa x Greenhouse successor-diagnostic repair after BMGHDIAG2 identity refusal.",
    "- Black Mesa x Greenhouse BMGHDIAG3 runtime evidence and decision (currently selected diagnostic gate, not a gameplay acceptance path).",
    "roadmap Greenhouse item",
)
write(path, text)

# Lifecycle: mark the profile-index paragraph as superseded by activation and update Gale helper revision.
path = "Knowledge/CURRENT_LIFECYCLE.md"
text = read(path)
text = text.replace(GALE_OLD_REV, GALE_NEW_REV)
old = (
    "BMGHDIAG3 is therefore canonically indexed and exact-head CI-green. It remains not Gale-imported and not runtime-armed. No gameplay/config/package/profile/plugin byte changed during indexing; `BuildSpecs/current.json` remains disabled, `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`, BMDSFIX1 remains not accepted with its passive target gate unchanged, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.\n\n"
    "The next bounded Greenhouse gate is a separate **BMGHDIAG3 runtime-activation checkpoint** for these already-published and indexed exact bytes."
)
new = (
    "BMGHDIAG3 is therefore canonically indexed and exact-head CI-green. That inactive index state is now superseded by `Current/198_S1.42AK_BMGHDIAG3_RUNTIME_ACTIVATION.md`: the exact same profile/DLL bytes are runtime-armed solely as a diagnostic target, with `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG3`. "
    "`BuildSpecs/current.json` remains disabled and `Current/AUTO_BUILD_RESULT.json` remains exact BMDSFIX1; the canonical Gale v2.4.3 resolver now fail-closed permits this direct diagnostic to bind to the exact `CURRENT_STATE.accepted_baseline` S1.42AK identity while preserving the separate BMDSFIX1 candidate. "
    "BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**, BMDSFIX1 remains not accepted with its passive target gate unchanged, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN` until runtime evidence is ingested and decided.\n\n"
    "The next bounded Greenhouse gate is the exact BMGHDIAG3 runtime test and evidence upload; no gameplay acceptance is implied by activation."
)
text = replace_once(text, old, new, "lifecycle BMGHDIAG3 activation")
write(path, text)

# Gale v2.4.3: preserve all existing checks while adding one exact accepted-baseline
# direct-diagnostic authority branch. AUTO_BUILD_RESULT is not rewritten.
path = "RuntimeTools/ReplaceActiveGaleProfileV24.ps1"
text = read(path)
text = replace_once(text, GALE_OLD_REV, GALE_NEW_REV, "Gale wrapper revision")
old = '''    if(([string]$diag.base_build_id) -eq ([string]$build.build_id)){
        if(([string]$diag.base_profile) -ne ([string]$build.output_profile) -or ([string]$diag.base_sha256).ToLowerInvariant() -ne ([string]$build.output_sha256).ToLowerInvariant()){throw "Direct diagnostic runtime target '$active' base profile/SHA disagree with AUTO_BUILD_RESULT"}
    }
    else {
'''
new = '''    if(([string]$diag.base_build_id) -eq ([string]$build.build_id)){
        if(([string]$diag.base_profile) -ne ([string]$build.output_profile) -or ([string]$diag.base_sha256).ToLowerInvariant() -ne ([string]$build.output_sha256).ToLowerInvariant()){throw "Direct diagnostic runtime target '$active' base profile/SHA disagree with AUTO_BUILD_RESULT"}
    }
    elseif(([string]$diag.base_build_id) -eq ([string]$state.accepted_baseline.build_id)){
        if(([string]$diag.base_profile) -ne ([string]$state.accepted_baseline.profile) -or ([string]$diag.base_sha256).ToLowerInvariant() -ne ([string]$state.accepted_baseline.sha256).ToLowerInvariant()){throw "Direct accepted-baseline diagnostic runtime target '$active' base profile/SHA disagree with CURRENT_STATE.accepted_baseline"}
    }
    else {
'''
text = replace_once(text, old, new, "Gale accepted-baseline branch")
text = replace_once(
    text,
    'Write-Host "Expliziter diagnostischer Runtime-Target wurde über CURRENT_STATE + one-hop parent chain + build_result fail-closed verifiziert." -ForegroundColor DarkGray',
    'Write-Host "Expliziter diagnostischer Runtime-Target wurde über CURRENT_STATE + direct AUTO/accepted-baseline/one-hop parent chain + build_result fail-closed verifiziert." -ForegroundColor DarkGray',
    "Gale resolver status message",
)
write(path, text)

# Permanent Gale regression validator.
path = "RepositoryTools/gale_import_helper_validator.py"
text = read(path)
text = replace_once(text, GALE_OLD_REV, GALE_NEW_REV, "Gale validator revision")
needle = '        "if(([string]$diag.base_build_id) -eq ([string]$build.build_id))",\n'
addition = (
    needle
    + '        "$state.accepted_baseline",\n'
    + '        "elseif(([string]$diag.base_build_id) -eq ([string]$state.accepted_baseline.build_id))",\n'
    + '        "$state.accepted_baseline.profile",\n'
    + '        "$state.accepted_baseline.sha256",\n'
    + '        "Direct accepted-baseline diagnostic runtime target",\n'
)
text = replace_once(text, needle, addition, "Gale validator accepted baseline tokens")
text = replace_once(
    text,
    'print("PASS: Gale import helper v2.4.2 one-hop diagnostic-parent chain + fail-closed materialization regression contract validated")',
    'print("PASS: Gale import helper v2.4.3 direct AUTO/accepted-baseline + one-hop diagnostic-parent chain + fail-closed materialization regression contract validated")',
    "Gale validator PASS",
)
write(path, text)

# Canonical Gale workflow documentation.
path = "Knowledge/GALE_PROFILE_WORKFLOW.md"
text = read(path)
text = replace_once(
    text,
    "**Last-Hardened:** 2026-09-18 (`2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`; adds a fail-closed explicit one-hop diagnostic-parent chain for DIAG2 while preserving the previously validated local UI/import path)",
    "**Last-Hardened:** 2026-09-28 (`2026-09-28-import-uia-v2.4.3-accepted-baseline-direct-diagnostic-chain`; adds a fail-closed direct accepted-baseline diagnostic anchor while preserving the direct AUTO and explicit one-hop parent paths plus the validated local UI/import path)",
    "Gale workflow hardened line",
)
old = '''Before presenting it, `RuntimeInbox/ACTIVE_BUILD.txt` must resolve fail-closed through one of three explicitly bounded repository-authorized shapes:

1. **normal built-artifact path:** `ACTIVE_BUILD == Current/AUTO_BUILD_RESULT.json.build_id`;
2. **direct diagnostic path:** the active `selected_scope.diagnostic_revision` is explicitly authorized, its own build-result matches its output/base identity, and its base binds directly to `AUTO_BUILD_RESULT`; this remains valid when `AUTO_BUILD_RESULT` is the accepted/latest baseline and there is intentionally no gameplay `active_candidate`; or
3. **one-hop diagnostic-parent path:** the active `diagnostic_revision` is explicitly authorized, its base identity matches exactly one `selected_scope.diagnostic_parent_revision`, that parent has the exact parent status `PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED`, the parent's own build-result matches it, and the parent itself binds directly to `AUTO_BUILD_RESULT`.

The third shape is deliberately **not recursive**. It authorizes the exact balanced -> DIAG1 -> DIAG2 chain without allowing an arbitrary diagnostic lineage. No other `ACTIVE_BUILD` / `AUTO_BUILD_RESULT` mismatch is permitted. Diagnostic resolution changes only repository target selection; it does not promote a diagnostic artifact, replace the balanced candidate or weaken download/import integrity checks.
'''
new = '''Before presenting it, `RuntimeInbox/ACTIVE_BUILD.txt` must resolve fail-closed through one of four explicitly bounded repository-authorized shapes:

1. **normal built-artifact path:** `ACTIVE_BUILD == Current/AUTO_BUILD_RESULT.json.build_id`;
2. **direct AUTO diagnostic path:** the active `selected_scope.diagnostic_revision` is explicitly authorized, its own build-result matches its output/base identity, and its base binds directly to `AUTO_BUILD_RESULT`;
3. **direct accepted-baseline diagnostic path:** the same active diagnostic/build-result/controller checks pass, and its base build ID/profile/SHA bind exactly to `CURRENT_STATE.accepted_baseline`; this permits a diagnostic built directly from the accepted baseline even while `AUTO_BUILD_RESULT` legitimately points at a separate active gameplay candidate; or
4. **one-hop diagnostic-parent path:** the active `diagnostic_revision` is explicitly authorized, its base identity matches exactly one `selected_scope.diagnostic_parent_revision`, that parent has the exact parent status `PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED`, the parent's own build-result matches it, and the parent itself binds directly to `AUTO_BUILD_RESULT`.

The one-hop shape is deliberately **not recursive**, and the accepted-baseline path is not a generic fallback: build ID, profile path and SHA-256 must all match the canonical accepted baseline exactly. No other `ACTIVE_BUILD` / `AUTO_BUILD_RESULT` mismatch is permitted. Diagnostic resolution changes only repository target selection; it does not promote a diagnostic artifact, replace the gameplay candidate or weaken download/import integrity checks.
'''
text = replace_once(text, old, new, "Gale workflow authority shapes")
text = replace_once(
    text,
    "- a direct diagnostic must bind to the current `AUTO_BUILD_RESULT`; a second-generation diagnostic must bind to exactly one explicit `selected_scope.diagnostic_parent_revision`, whose own build-result and base identity bind directly to `AUTO_BUILD_RESULT`;",
    "- a direct diagnostic must bind either to the current `AUTO_BUILD_RESULT` or exactly to `CURRENT_STATE.accepted_baseline` by build ID/profile/SHA; a second-generation diagnostic must bind to exactly one explicit `selected_scope.diagnostic_parent_revision`, whose own build-result and base identity bind directly to `AUTO_BUILD_RESULT`;",
    "Gale workflow v24 direct bullet",
)
insert_marker = "The permanent repository regression gate is `RepositoryTools/gale_import_helper_validator.py`, run by `.github/workflows/knowledge-architecture.yml`."
section = '''## v2.4.3 exact accepted-baseline direct diagnostic anchor

BMGHDIAG3 is intentionally built directly from exact accepted S1.42AK while `Current/AUTO_BUILD_RESULT.json` correctly remains the separate S1.42AK-BMDSFIX1 gameplay candidate. Rewriting `AUTO_BUILD_RESULT` merely to import the diagnostic would corrupt build authority, while treating accepted S1.42AK as a fake diagnostic parent would misrepresent lineage.

Revision `2026-09-28-import-uia-v2.4.3-accepted-baseline-direct-diagnostic-chain` adds exactly one fail-closed authority edge: after the active controller, diagnostic status and diagnostic build-result have already matched, a direct diagnostic may bind to `CURRENT_STATE.accepted_baseline` only when its `base_build_id`, `base_profile` and `base_sha256` all match that accepted baseline exactly. The existing direct-`AUTO_BUILD_RESULT` and explicit one-hop diagnostic-parent paths remain unchanged. No recursive or arbitrary fallback is introduced.

'''
text = replace_once(text, insert_marker, section + insert_marker, "Gale v2.4.3 documentation")
text = replace_once(
    text,
    "- diagnostic mismatches require exact controller + active diagnostic revision + status + build-result agreement; a non-direct diagnostic additionally requires the exact one-hop `diagnostic_parent_revision` contract above; no generic or recursive fallback exists;",
    "- diagnostic mismatches require exact controller + active diagnostic revision + status + build-result agreement; a direct diagnostic base must match either exact `AUTO_BUILD_RESULT` or exact `CURRENT_STATE.accepted_baseline` identity, while a non-direct diagnostic additionally requires the exact one-hop `diagnostic_parent_revision` contract above; no generic or recursive fallback exists;",
    "Gale fail-closed requirement",
)
write(path, text)

# Activation record includes the exact future commands, but repository integration
# is still required before the user is instructed to run them.
uploader = r'''$ErrorActionPreference='Stop';$build='S1.42AK-BMGHDIAG3';$log='C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $log -PathType Leaf)){throw "Expected runtime log not found: $log"};$bytes=[IO.File]::ReadAllBytes($log);if($bytes.Length -le 0){throw 'Runtime log is empty'};$text=[Text.Encoding]::UTF8.GetString($bytes);if($text.IndexOf('[BMGHDIAG3]',[StringComparison]::Ordinal) -lt 0){throw 'Refusing upload: exact local LogOutput.log contains no [BMGHDIAG3] marker'};$localSha=([BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($bytes))).Replace('-','').ToLowerInvariant();$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;$fallback=Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe';if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback};if(!$gh -and (Get-Command winget -ErrorAction SilentlyContinue)){winget install --id GitHub.cli -e --source winget --accept-source-agreements --accept-package-agreements | Out-Host;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback}};if(!$gh){throw 'GitHub CLI (gh) could not be resolved or bootstrapped'};& $gh auth status -h github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login -h github.com -w;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dest='RuntimeInbox/Current/LogOutput.log';$existing=$null;try{$existing=(& $gh api "repos/$repo/contents/$dest?ref=main" --jq '.sha' 2>$null)}catch{};$payload=@{message="Upload $build runtime log ($localSha)";content=[Convert]::ToBase64String($bytes);branch='main'};if($existing){$payload.sha=$existing};$json=$payload|ConvertTo-Json -Compress;$tmp=[IO.Path]::GetTempFileName();try{[IO.File]::WriteAllText($tmp,$json,[Text.UTF8Encoding]::new($false));& $gh api --method PUT "repos/$repo/contents/$dest" --input $tmp;if($LASTEXITCODE -ne 0){throw 'Runtime log upload failed'}}finally{Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue};Write-Host "Uploaded $build LogOutput.log SHA-256 $localSha" -ForegroundColor Green'''

activation = f'''# S1.42AK-BMGHDIAG3 Runtime Activation

**Date:** 2026-09-28
**Status:** PUBLISHED / INDEXED / ACTIVE DIAGNOSTIC RUNTIME TARGET / TEST OUTSTANDING / NEVER ACCEPT
**Accepted gameplay baseline:** S1.42AK — unchanged
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted / passive Deep Sewers gate unchanged
**Diagnostic:** S1.42AK-BMGHDIAG3
**Diagnostic profile:** `{PROFILE}`
**Diagnostic profile SHA-256:** `{PROFILE_SHA}`
**Diagnostic DLL SHA-256:** `{DLL_SHA}`
**Direct diagnostic base:** accepted S1.42AK / `{BASE_SHA}`

## Activation decision

The exact reviewed, exact-byte-published and canonically indexed BMGHDIAG3 artifact is authorized as the active runtime/evidence target for one bounded Black Mesa x Greenhouse diagnostic run after this activation is integrated and exact-head CI-green.

This is an authority/routing transition only. It does not rebuild or mutate the profile, diagnostic DLL, package/config/gameplay bytes, accepted S1.42AK, or the separate BMDSFIX1 gameplay candidate. `BuildSpecs/current.json` remains disabled and pinned to exact BMDSFIX1. `Current/AUTO_BUILD_RESULT.json` also remains exact BMDSFIX1; it is not rewritten to impersonate the accepted diagnostic base.

BMGHDIAG3 is **DIAGNOSTIC ONLY / NEVER ACCEPT**. Runtime activation cannot accept BMGHDIAG3, cannot accept BMDSFIX1, cannot waive or replace BMDSFIX1's passive regular Black Mesa x `DeepSewersFlow` qualification, and cannot mark Black Mesa x Greenhouse proven before runtime evidence exists.

## Exact runtime authority chain

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG3` resolves through:

1. `CURRENT_STATE.controllers.runtime_active_build`;
2. `CURRENT_STATE.selected_scope.diagnostic_revision`;
3. `{BUILD_RESULT}`;
4. exact BMGHDIAG3 output identity `{PROFILE_SHA}`;
5. exact direct base identity `CURRENT_STATE.accepted_baseline = S1.42AK` / `{BASE_SHA}`.

The canonical Gale v2.4.3 resolver adds only this explicit accepted-baseline direct-diagnostic edge. The pre-existing direct-`AUTO_BUILD_RESULT` and one-hop diagnostic-parent paths remain intact. No generic or recursive fallback exists.

## Preserved byte/provenance gates

- profile SHA-256: `{PROFILE_SHA}`;
- diagnostic DLL SHA-256: `{DLL_SHA}`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `{LLL_SHA}`;
- accepted S1.42AB normalizer SHA-256: `{NORMALIZER_SHA}`;
- archive members: 337;
- changed existing archive member: `export.r2x` only;
- added archive member: `BepInEx/plugins/S142AKBMGHDiag3/S142AKBMGHDiag3.dll` only;
- package/config drift: zero;
- `ProfileSources/S1.42AK-BMGHDIAG3/PROFILE_INDEX_RESULT.json`: exact profile/index identity, `EXPECTED_HASHES` resolution.

BMGHDIAG3's source repair remains exactly the removal of the disproven `ManifestModule.Name == "Assembly-CSharp.dll"` runtime equality. Non-null runtime-module presence and all remaining physical provenance, runtime structure, dependency, exact LLL selection, after-normalizer ordering, Greenhouse identity/rarity and read-only topology/traversal contracts remain.

## Runtime qualification contract

Run the exact diagnostic on **Black Mesa**. A sufficient run must establish all of the following:

1. `[BMGHDIAG3] ARMED` appears without startup refusal;
2. `[BMGHDIAG3] SELECTED Black Mesa Greenhouse / GreenhouseFlow; normalized rarity=100; pool=<N>->1` appears;
3. DunGen completes without exhausted retries or fatal generation abort;
4. `[BMGHDIAG3] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4` appears;
5. the player normally enters and exits through the main entrance;
6. alternate IDs 1, 2 and 3 are directly traversed by the player; bidirectional use should be obtained where practical;
7. no severe clipping or inaccessible required entrance geometry is observed at exercised endpoints;
8. no new severe/persistent target-attributable routing or NavMesh failure is present;
9. no `[BMGHDIAG3] REFUSED` or `TOPOLOGY_INCONCLUSIVE` marker invalidates the run.

Successful native teleport alone must not be overclaimed as visual geometry proof. The separate Black-Mesa/Pikmin routing-recovery scope remains closed during this diagnostic.

## Exact Gale replacement/import one-liner

Use only after this activation commit is integrated on `main` and exact-head CI is green:

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

The launcher must verify the exact active controller/diagnostic/build-result/accepted-baseline chain and the exact downloaded profile SHA before Gale import. Follow its numeric old-profile selection and explicit `y` deletion confirmation; do not manually substitute another profile.

## Exact build-specific runtime-log uploader

After the bounded gameplay run is complete, use this single line. It verifies the exact Gale-local BMGHDIAG3 log path, non-empty content and `[BMGHDIAG3]` marker, computes SHA-256, bootstraps/authenticates `gh` when needed, and creates or replaces `RuntimeInbox/Current/LogOutput.log` on `main` without a local repository clone.

```powershell
{uploader}
```

## Evidence attribution and rollback

Runtime evidence must be uploaded while `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMGHDIAG3`. Runtime-active status never promotes the diagnostic. BMGHDIAG3 is NEVER ACCEPT.

The separate BMDSFIX1 gameplay candidate remains preserved exactly and its regular Deep Sewers gate remains passive/outstanding. After the Greenhouse diagnostic decision, runtime/evidence routing must be explicitly reconciled rather than inferred from this activation record.
'''
write(ACTIVATION, activation)

print("PASS: staged exact BMGHDIAG3 runtime activation + fail-closed Gale accepted-baseline direct-diagnostic authority repair")
