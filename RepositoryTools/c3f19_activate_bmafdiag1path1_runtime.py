#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BUILD = "S1.42AK-BMAFDIAG1PATH1"
PROFILE_NAME = "LC V1 S1.42AK-BMAFD1P1"
PROFILE = "Profiles/LC V1 S1.42AK-BMAFD1P1.r2z"
PROFILE_SHA = "423e2e5185c85c1a3ce7a100583717d3503cf7308a12a182f5f7f65dc501ff91"
PARENT = "S1.42AK-BMAFDIAG1"
PARENT_PROFILE = "Profiles/LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic.r2z"
PARENT_SHA = "b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2"
DLL_SHA = "c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1"
FOUNDRY_CFG_SHA = "c9f03e7839c70ce21fae37ff597085175de35a9c176b97aed40798401ce66c0e"
ACCEPTED = "S1.42AK"
ACCEPTED_PROFILE = "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z"
ACCEPTED_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
CANDIDATE = "S1.42AK-BMDSFIX1"
CANDIDATE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
ACTIVATION = "Current/218_S1.42AK_BMAFDIAG1PATH1_RUNTIME_ACTIVATION.md"
BUILD_RESULT = "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC = "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
PUBLICATION = "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
PROFILE_SOURCES = "ProfileSources/S1.42AK-BMAFDIAG1PATH1/"
FILE_INDEX = PROFILE_SOURCES + "FILE_INDEX.json"
PROFILE_INDEX = PROFILE_SOURCES + "PROFILE_INDEX_RESULT.json"
PARENT_STATUS = "PUBLISHED_DIAGNOSTIC_PRELOADER_PATH_LENGTH_BLOCKED_DO_NOT_RERUN_NOT_ACCEPTED"
ACTIVE_STATUS = "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED"
OLD_REV = "2026-10-01-import-uia-v2.4.4-runtime-path-budget-guard"
NEW_REV = "2026-10-01-import-uia-v2.4.5-one-hop-accepted-baseline-parent-chain"


def req(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write(rel: str, obj) -> None:
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def file_sha(rel: str) -> str:
    h = hashlib.sha256()
    with (ROOT / rel).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    req(count == 1, f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, replacement: str, label: str) -> str:
    a = text.find(start)
    req(a >= 0, f"{label}: start anchor missing")
    b = text.find(end, a + len(start))
    req(b > a, f"{label}: end anchor missing")
    return text[:a] + replacement + text[b:]


# ---- Exact preconditions -------------------------------------------------
state = load("Current/CURRENT_STATE.json")
scope = state["selected_scope"]
req(scope["status"] == "PHASE_C3_BMAFDIAG1PATH1_INDEXED_RUNTIME_ACTIVATION_REQUIRED_BMDSFIX1_TARGET_PASSIVE_OUTSTANDING", "lifecycle pre-state drift")
req(state["accepted_baseline"]["build_id"] == ACCEPTED and state["accepted_baseline"]["profile"] == ACCEPTED_PROFILE and state["accepted_baseline"]["sha256"] == ACCEPTED_SHA, "accepted baseline drift")
req(state["active_candidate"]["build_id"] == CANDIDATE and state["active_candidate"]["sha256"] == CANDIDATE_SHA, "gameplay candidate drift")
req(state["latest_built_artifact"]["build_id"] == CANDIDATE and state["latest_built_artifact"]["sha256"] == CANDIDATE_SHA, "latest artifact drift")
req(state["controllers"]["runtime_active_build"] == CANDIDATE, "runtime controller pre-state drift")
req((ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == CANDIDATE, "ACTIVE_BUILD pre-state drift")
req(state["runtime_test_outstanding"] is True, "BMDSFIX1 passive runtime gate must remain outstanding")

current = load("BuildSpecs/current.json")
req(current["enabled"] is False and current["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "build controller drift")
req(current["base_sha256"] == CANDIDATE_SHA, "build controller guard drift")
auto = load("Current/AUTO_BUILD_RESULT.json")
req(auto["build_id"] == CANDIDATE and auto["output_sha256"] == CANDIDATE_SHA, "AUTO_BUILD_RESULT drift")

parent = copy.deepcopy(scope["diagnostic_revision"])
req(parent["build_id"] == PARENT and parent["status"] == PARENT_STATUS, "blocked BMAFDIAG1 parent authority drift")
req(parent["profile"] == PARENT_PROFILE and parent["sha256"] == PARENT_SHA, "blocked BMAFDIAG1 parent identity drift")
req(parent["base_build_id"] == ACCEPTED and parent["base_profile"] == ACCEPTED_PROFILE and parent["base_sha256"] == ACCEPTED_SHA, "blocked BMAFDIAG1 accepted-base anchor drift")
req(parent["diagnostic_dll_sha256"] == DLL_SHA and parent["runtime_armed"] is False, "blocked parent DLL/runtime state drift")

successor = copy.deepcopy(scope["diagnostic_successor_revision"])
req(successor["build_id"] == BUILD, "PATH1 successor build ID drift")
req(successor["status"] == "PUBLISHED_INDEXED_NOT_GALE_IMPORTED_NOT_RUNTIME_ARMED", "PATH1 successor pre-state drift")
req(successor["profile"] == PROFILE and successor["sha256"] == PROFILE_SHA, "PATH1 successor identity drift")
req(successor["base_build_id"] == PARENT and successor["base_profile"] == PARENT_PROFILE and successor["base_sha256"] == PARENT_SHA, "PATH1 parent identity drift")
req(successor["diagnostic_dll_sha256"] == DLL_SHA and successor["foundry_lll_config_sha256"] == FOUNDRY_CFG_SHA, "PATH1 inherited byte identity drift")
req(successor["projected_successor_path_lengths"] == [219, 221] and successor["path_length_budget"] == 255, "PATH1 runtime path-length budget drift")
req(successor["published"] is True and successor["indexed"] is True and successor["runtime_armed"] is False, "PATH1 lifecycle pre-state drift")
req(file_sha(PROFILE) == PROFILE_SHA, "PATH1 published profile SHA mismatch")

idx = load(PROFILE_INDEX)
req(idx["build_id"] == BUILD and idx["profile_path"] == PROFILE and idx["sha256"] == PROFILE_SHA, "PATH1 profile-index identity drift")
req(idx["zip_members"] == 337 and idx["snapshot"]["entries"] == 337 and idx["snapshot"]["text_entries"] == 331 and idx["build_id_resolution"] == "EXPECTED_HASHES", "PATH1 profile-index contract drift")

build = load(BUILD_RESULT)
req(build["build_id"] == BUILD and build["profile_name"] == PROFILE_NAME, "PATH1 build-result identity drift")
req(build["base_profile"] == PARENT_PROFILE and build["base_sha256"] == PARENT_SHA, "PATH1 build-result parent drift")
req(build["output_profile"] == PROFILE and build["output_sha256"] == PROFILE_SHA, "PATH1 build-result output drift")
req(build["zip_members"] == 337 and build["changed_existing_members"] == ["export.r2x"] and build["added_members"] == [], "PATH1 build-result delta drift")

static = load(STATIC)
req(static["output_sha256"] == PROFILE_SHA and static["diagnostic_dll_sha256"] == DLL_SHA and static["foundry_lll_config_sha256"] == FOUNDRY_CFG_SHA, "PATH1 static byte authority drift")
req(static["projected_runtime_path_lengths"] == [219, 221] and static["path_length_budget"] == 255, "PATH1 static path budget drift")

# ---- Canonical machine-state activation ---------------------------------
active = copy.deepcopy(successor)
active.update({
    "status": ACTIVE_STATUS,
    "classification": "DIAGNOSTIC_ONLY_NEVER_ACCEPT",
    "profile_name": PROFILE_NAME,
    "profile": PROFILE,
    "output_profile": PROFILE,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "profile_index_result": PROFILE_INDEX,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC,
    "publication_evidence": PUBLICATION,
    "published": True,
    "indexed": True,
    "runtime_armed": True,
    "next_gate": "RUNTIME_DIAGNOSTIC_TEST",
    "activation_record": ACTIVATION,
    "runtime_role": "DIAGNOSTIC_ONLY_BLACK_MESA_ABANDONED_FOUNDRY_FORCE_SELECTION_AND_READ_ONLY_ENTRANCE_OBSERVATION_NEVER_ACCEPT",
    "runtime_validation_status": "RUNTIME_TEST_OUTSTANDING_NEVER_ACCEPT",
})

scope["diagnostic_parent_revision"] = parent
scope["diagnostic_revision"] = active
scope["diagnostic_successor_revision"] = copy.deepcopy(active)
scope["diagnostic_runtime_activation"] = ACTIVATION
scope["bmafdiag1path1_runtime_activation"] = ACTIVATION
scope["status"] = "PHASE_C3_BMAFDIAG1PATH1_RUNTIME_ACTIVE_TEST_OUTSTANDING_BMDSFIX1_TARGET_PASSIVE_OUTSTANDING"
scope["finding"] = (
    "Exact S1.42AK-BMAFDIAG1PATH1 reviewed bytes are published, canonically indexed and now runtime-armed solely as the bounded Black Mesa x Abandoned Foundry diagnostic target. "
    "The active short profile remains SHA-256 " + PROFILE_SHA + " and inherits the exact BMAFDIAG1 diagnostic DLL SHA-256 " + DLL_SHA + " and Foundry LLL config SHA-256 " + FOUNDRY_CFG_SHA + ". "
    "Its explicit one-hop diagnostic parent is the preloader-blocked long-name S1.42AK-BMAFDIAG1 identity, which remains DO_NOT_RERUN and binds exactly to accepted S1.42AK. "
    "S1.42AK-BMDSFIX1 remains the separate active gameplay candidate / NOT ACCEPTED and its regular Black Mesa x DeepSewersFlow qualification remains passive, outstanding and unwaived. "
    "BuildSpecs/current.json and AUTO_BUILD_RESULT remain exact BMDSFIX1; RuntimeInbox/ACTIVE_BUILD.txt identifies BMAFDIAG1PATH1 only for fail-closed Gale target resolution and runtime-evidence attribution. "
    "Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN until runtime evidence is ingested and decided."
)
scope["analysis_contract"] = (
    "Treat exact active S1.42AK-BMAFDIAG1PATH1 profile SHA-256 " + PROFILE_SHA + " and canonical PROFILE_INDEX_RESULT.json as immutable runtime inputs. "
    "The one-hop parent S1.42AK-BMAFDIAG1 remains preloader-blocked and DO_NOT_RERUN; it exists only as exact provenance anchored to accepted S1.42AK. "
    "Preserve DIAGNOSTIC ONLY / NEVER ACCEPT, accepted S1.42AK, separate S1.42AK-BMDSFIX1 / NOT ACCEPTED, its passive/unwaived DeepSewersFlow gate, accepted normalizer behavior, and all profile/DLL/config/package/gameplay bytes. "
    "A runtime qualification requires BMAFDIAG1 arming, pre-reduction viable exact FoundryFlow at normalized rarity 100, singleton selection, completed generation, IDs 0..3 topology/traversal evidence and no invalidating REFUSED/TOPOLOGY_INCONCLUSIVE/TRAVERSAL_INCONCLUSIVE/OBSERVER_INCONCLUSIVE marker."
)
next_action = (
    "Import the exact active S1.42AK-BMAFDIAG1PATH1 profile through the canonical repository-driven Gale v2.4.5 launcher, run one bounded Black Mesa x Abandoned Foundry diagnostic, exercise the main entrance and alternate entrance IDs 1, 2 and 3 in both directions where practical, then upload that run's exact BepInEx/LogOutput.log with the BMAFDIAG1PATH1 build-specific standalone PowerShell uploader. "
    "Do not alter profile/config/package/plugin/gameplay bytes during the test. Treat the result as diagnostic-only / NEVER ACCEPT; do not accept BMDSFIX1 or waive its passive Black Mesa x DeepSewersFlow gate."
)
scope["next_action"] = next_action

pc = scope["phase_c"]
pc["black_mesa_abandoned_foundry_status"] = "NOT_YET_PROVEN_BMAFDIAG1PATH1_RUNTIME_ACTIVE_TEST_OUTSTANDING"
pc["bmafdiag1path1_source_static_status"] = "SOURCE_STATIC_PASS_MAIN_INTEGRATED_REVIEW_PASS_EXACT_BYTES_PUBLISHED_INDEXED_RUNTIME_ACTIVE_TEST_OUTSTANDING"
pc["bmafdiag1path1_review_status"] = "INACTIVE_REVIEW_BUILD_PASS_EXACT_BYTES_PUBLISHED_INDEXED_RUNTIME_ACTIVE_TEST_OUTSTANDING"
pc["bmafdiag1path1_publication_status"] = "EXACT_BYTES_PUBLISHED_INDEXED_RUNTIME_ACTIVE_TEST_OUTSTANDING"
pc["bmafdiag1path1_profile_index_reconciliation"] = "Current/217_S1.42AK_BMAFDIAG1PATH1_PROFILE_INDEX_RECONCILIATION.md"
pc["bmafdiag1path1_profile_indexed"] = True
pc["bmafdiag1path1_profile_index_result"] = PROFILE_INDEX
pc["bmafdiag1path1_profile_index_run"] = 36902278452
pc["bmafdiag1path1_profile_index_commit"] = "e9e9b6f4b11c007f2325f72da15d8be8977fc9b0"
pc["bmafdiag1path1_runtime_activation"] = ACTIVATION
pc["bmafdiag1path1_runtime_activation_status"] = "ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_TEST_OUTSTANDING_NEVER_ACCEPT"

state["updated"] = "2026-10-01"
state["controllers"]["runtime_active_build"] = BUILD
state["runtime_test_outstanding"] = True
state["next_action"] = next_action
write("Current/CURRENT_STATE.json", state)
(ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD + "\n", encoding="utf-8")

# ---- Artifact-evidence routing ------------------------------------------
integrity = load("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
integrity["updated"] = "2026-10-01"
integrity["last_validated"] = "2026-10-01"
pending = integrity["pending_profiles"]
parent_entry = next((x for x in pending if x.get("build_id") == PARENT), None)
req(parent_entry is not None, "artifact-integrity BMAFDIAG1 parent entry missing")
parent_entry["note"] = "Exact long-name BMAFDIAG1 bytes remain published/indexed but are preloader-blocked by the observed 260/262-character Gale-local nested paths and must not be rerun. They are retained only as the explicit one-hop diagnostic parent for active BMAFDIAG1PATH1 and remain DIAGNOSTIC ONLY / NEVER ACCEPT."
req(not any(x.get("build_id") == BUILD for x in pending), "BMAFDIAG1PATH1 artifact-integrity entry already exists")
pending.append({
    "build_id": BUILD,
    "role": "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
    "profile": PROFILE,
    "profile_sha256": PROFILE_SHA,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "export": PROFILE_SOURCES + "export.r2x",
    "build_plan": "BuildSpecs/S1.42AK-BMAFDIAG1PATH1_PLAN.md",
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC,
    "publication_evidence": PUBLICATION,
    "activation_record": ACTIVATION,
    "diagnostic_dll_sha256": DLL_SHA,
    "runtime_evidence_required": False,
    "partial_runtime_evidence_present": False,
    "note": "Exact published/indexed short-identity BMAFDIAG1PATH1 bytes are runtime-armed solely for bounded Black Mesa x Abandoned Foundry diagnostic qualification through the explicit blocked-parent -> accepted-S1.42AK provenance chain. DIAGNOSTIC ONLY / NEVER ACCEPT; BMDSFIX1 and its passive Deep Sewers gate are unchanged."
})
integrity.setdefault("verified_repository_api_observations", []).append(
    "S1.42AK-BMAFDIAG1PATH1 exact published/indexed profile SHA-256 " + PROFILE_SHA + " is runtime-armed only as a one-hop diagnostic over blocked BMAFDIAG1 anchored exactly to accepted S1.42AK; the long parent remains DO_NOT_RERUN and Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN pending runtime evidence."
)
write("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

# ---- Gale resolver: add only blocked-parent -> accepted-baseline edge ----
gale_path = ROOT / "RuntimeTools/ReplaceActiveGaleProfileV24.ps1"
gale = gale_path.read_text(encoding="utf-8")
gale = replace_once(gale, OLD_REV, NEW_REV, "Gale current revision")
old_parent_block = """    else {
        $parent=$state.selected_scope.diagnostic_parent_revision
        if($null -eq $parent -or ([string]$parent.build_id) -ne ([string]$diag.base_build_id)){throw "Diagnostic runtime target '$active' parent '$($diag.base_build_id)' is not the explicit CURRENT_STATE diagnostic_parent_revision"}
        if(([string]$parent.status) -ne 'PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED'){throw "Diagnostic parent '$($parent.build_id)' has no authorized parent status: '$($parent.status)'"}
        if(([string]$diag.base_profile) -ne ([string]$parent.profile) -or ([string]$diag.base_sha256).ToLowerInvariant() -ne ([string]$parent.sha256).ToLowerInvariant()){throw "Diagnostic runtime target '$active' base profile/SHA disagree with diagnostic parent"}
        if(([string]$parent.base_build_id) -ne ([string]$build.build_id)){throw "Diagnostic parent '$($parent.build_id)' is not anchored directly to AUTO_BUILD_RESULT '$($build.build_id)'"}
        if(([string]$parent.base_profile) -ne ([string]$build.output_profile) -or ([string]$parent.base_sha256).ToLowerInvariant() -ne ([string]$build.output_sha256).ToLowerInvariant()){throw "Diagnostic parent '$($parent.build_id)' base profile/SHA disagree with AUTO_BUILD_RESULT"}
        $parentBuild=Get-RepositoryJson -RepositoryPath ([string]$parent.build_result) -Label "Parent diagnostic build_result"
        if(([string]$parentBuild.build_id) -ne ([string]$parent.build_id)){throw "Parent diagnostic build_result build ID mismatch"}
        if(([string]$parentBuild.output_profile) -ne ([string]$parent.profile) -or ([string]$parentBuild.output_sha256).ToLowerInvariant() -ne ([string]$parent.sha256).ToLowerInvariant()){throw "Parent diagnostic build_result profile/SHA disagree with CURRENT_STATE diagnostic_parent_revision"}
        if(([string]$parentBuild.base_profile) -ne ([string]$parent.base_profile) -or ([string]$parentBuild.base_sha256).ToLowerInvariant() -ne ([string]$parent.base_sha256).ToLowerInvariant()){throw "Parent diagnostic build_result base profile/SHA disagree with CURRENT_STATE diagnostic_parent_revision"}
    }
"""
new_parent_block = """    else {
        $parent=$state.selected_scope.diagnostic_parent_revision
        if($null -eq $parent -or ([string]$parent.build_id) -ne ([string]$diag.base_build_id)){throw "Diagnostic runtime target '$active' parent '$($diag.base_build_id)' is not the explicit CURRENT_STATE diagnostic_parent_revision"}
        if(([string]$diag.base_profile) -ne ([string]$parent.profile) -or ([string]$diag.base_sha256).ToLowerInvariant() -ne ([string]$parent.sha256).ToLowerInvariant()){throw "Diagnostic runtime target '$active' base profile/SHA disagree with diagnostic parent"}
        $parentAnchoredToAuto=([string]$parent.status) -eq 'PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED'
        $parentAnchoredToAccepted=([string]$parent.status) -eq 'PUBLISHED_DIAGNOSTIC_PRELOADER_PATH_LENGTH_BLOCKED_DO_NOT_RERUN_NOT_ACCEPTED'
        if(!$parentAnchoredToAuto -and !$parentAnchoredToAccepted){throw "Diagnostic parent '$($parent.build_id)' has no authorized parent status: '$($parent.status)'"}
        $parentBuild=Get-RepositoryJson -RepositoryPath ([string]$parent.build_result) -Label "Parent diagnostic build_result"
        if(([string]$parentBuild.build_id) -ne ([string]$parent.build_id)){throw "Parent diagnostic build_result build ID mismatch"}
        if(([string]$parentBuild.output_profile) -ne ([string]$parent.profile) -or ([string]$parentBuild.output_sha256).ToLowerInvariant() -ne ([string]$parent.sha256).ToLowerInvariant()){throw "Parent diagnostic build_result profile/SHA disagree with CURRENT_STATE diagnostic_parent_revision"}
        if(([string]$parentBuild.base_profile) -ne ([string]$parent.base_profile) -or ([string]$parentBuild.base_sha256).ToLowerInvariant() -ne ([string]$parent.base_sha256).ToLowerInvariant()){throw "Parent diagnostic build_result base profile/SHA disagree with CURRENT_STATE diagnostic_parent_revision"}
        if($parentAnchoredToAuto){
            if(([string]$parent.base_build_id) -ne ([string]$build.build_id)){throw "Diagnostic parent '$($parent.build_id)' is not anchored directly to AUTO_BUILD_RESULT '$($build.build_id)'"}
            if(([string]$parent.base_profile) -ne ([string]$build.output_profile) -or ([string]$parent.base_sha256).ToLowerInvariant() -ne ([string]$build.output_sha256).ToLowerInvariant()){throw "Diagnostic parent '$($parent.build_id)' base profile/SHA disagree with AUTO_BUILD_RESULT"}
        }
        else {
            if(([string]$parent.base_build_id) -ne ([string]$state.accepted_baseline.build_id)){throw "Blocked diagnostic parent '$($parent.build_id)' is not anchored directly to CURRENT_STATE.accepted_baseline '$($state.accepted_baseline.build_id)'"}
            if(([string]$parent.base_profile) -ne ([string]$state.accepted_baseline.profile) -or ([string]$parent.base_sha256).ToLowerInvariant() -ne ([string]$state.accepted_baseline.sha256).ToLowerInvariant()){throw "Blocked diagnostic parent '$($parent.build_id)' base profile/SHA disagree with CURRENT_STATE.accepted_baseline"}
        }
    }
"""
gale = replace_once(gale, old_parent_block, new_parent_block, "Gale one-hop parent resolver")
gale = gale.replace(
    "direct AUTO/accepted-baseline/one-hop parent chain + build_result fail-closed",
    "direct AUTO/accepted-baseline/one-hop parent-to-AUTO-or-accepted-baseline chain + build_result fail-closed",
)
gale = gale.replace(
    "Launching canonical Gale importer with v2.4.4 fail-closed runtime path-budget, accepted-baseline/direct/one-hop diagnostic chain, export-read and recursive materialization contract...",
    "Launching canonical Gale importer with v2.4.5 fail-closed runtime path-budget, direct diagnostics and one-hop parent-to-AUTO-or-accepted-baseline chain, export-read and recursive materialization contract...",
)
gale_path.write_text(gale, encoding="utf-8")

# ---- Permanent validators ------------------------------------------------
def patch_state_validator(rel: str, accepted_name: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    start = text.find("    diagnostic_one_hop = bool(")
    req(start >= 0, f"{rel}: diagnostic_one_hop start missing")
    end_token = "    diagnostic_is_runtime_target = diagnostic_direct_candidate or diagnostic_direct_accepted or diagnostic_one_hop"
    end = text.find(end_token, start)
    req(end > start, f"{rel}: diagnostic_is_runtime_target anchor missing")
    end += len(end_token)
    av = accepted_name
    replacement = f"""    diagnostic_one_hop_candidate = bool(
        diagnostic_common
        and candidate_id
        and diagnostic.get("base_build_id") != candidate_id
        and parent_id == diagnostic.get("base_build_id")
        and parent_diagnostic.get("status") == "PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED"
        and diagnostic.get("base_profile") == parent_diagnostic.get("profile")
        and diagnostic.get("base_sha256") == parent_diagnostic.get("sha256")
        and parent_diagnostic.get("base_build_id") == candidate_id
        and parent_diagnostic.get("base_profile") == candidate.get("profile")
        and parent_diagnostic.get("base_sha256") == candidate.get("sha256")
        and parent_diagnostic.get("build_result")
        and parent_diagnostic.get("publication_evidence")
    )
    diagnostic_one_hop_accepted = bool(
        diagnostic_common
        and candidate_id
        and diagnostic.get("base_build_id") != candidate_id
        and parent_id == diagnostic.get("base_build_id")
        and parent_diagnostic.get("status") == "PUBLISHED_DIAGNOSTIC_PRELOADER_PATH_LENGTH_BLOCKED_DO_NOT_RERUN_NOT_ACCEPTED"
        and diagnostic.get("base_profile") == parent_diagnostic.get("profile")
        and diagnostic.get("base_sha256") == parent_diagnostic.get("sha256")
        and parent_diagnostic.get("base_build_id") == {av}.get("build_id")
        and parent_diagnostic.get("base_profile") == {av}.get("profile")
        and parent_diagnostic.get("base_sha256") == {av}.get("sha256")
        and parent_diagnostic.get("build_result")
        and parent_diagnostic.get("publication_evidence")
    )
    diagnostic_one_hop = diagnostic_one_hop_candidate or diagnostic_one_hop_accepted
    diagnostic_is_runtime_target = diagnostic_direct_candidate or diagnostic_direct_accepted or diagnostic_one_hop"""
    text = text[:start] + replacement + text[end:]
    path.write_text(text, encoding="utf-8")

patch_state_validator("RepositoryTools/knowledge_architecture_validator.py", "accepted")
patch_state_validator("RepositoryTools/overhaul_contract_validator.py", "a")

validator_path = ROOT / "RepositoryTools/gale_import_helper_validator.py"
validator = validator_path.read_text(encoding="utf-8")
validator = replace_once(validator, f'V24_REVISION = "{OLD_REV}"', f'V24_REVISION = "{NEW_REV}"', "Gale validator revision")
needle = '        "PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED",\n'
validator = replace_once(
    validator,
    needle,
    needle
    + '        "PUBLISHED_DIAGNOSTIC_PRELOADER_PATH_LENGTH_BLOCKED_DO_NOT_RERUN_NOT_ACCEPTED",\n'
    + '        "$parentAnchoredToAuto",\n'
    + '        "$parentAnchoredToAccepted",\n'
    + '        "Blocked diagnostic parent",\n',
    "Gale validator accepted-parent tokens",
)
validator = validator.replace(
    "PASS: Gale import helper v2.4.4 runtime path-budget + direct AUTO/accepted-baseline + one-hop diagnostic-parent chain + fail-closed materialization regression contract validated",
    "PASS: Gale import helper v2.4.5 runtime path-budget + direct AUTO/accepted-baseline + one-hop parent-to-AUTO-or-accepted-baseline chain + fail-closed materialization regression contract validated",
)
validator_path.write_text(validator, encoding="utf-8")

# ---- Human authorities ---------------------------------------------------
gk_path = ROOT / "Knowledge/GALE_PROFILE_WORKFLOW.md"
gk = gk_path.read_text(encoding="utf-8")
old_harden = f"**Last-Hardened:** 2026-10-01 (@@BT@@{OLD_REV}@@BT@@; adds a fail-closed local Gale runtime path-length budget before destructive replacement while preserving the direct AUTO, accepted-baseline and explicit one-hop diagnostic paths plus the validated UI/import path)"
new_harden = f"**Last-Hardened:** 2026-10-01 (@@BT@@{NEW_REV}@@BT@@; preserves the runtime path-length budget and adds only an exact one-hop blocked-diagnostic-parent -> accepted-baseline authority edge for BMAFDIAG1PATH1)"
gk = replace_once(gk, old_harden, new_harden, "Gale workflow Last-Hardened")
old_shape = "4. **one-hop diagnostic-parent path:** the active @@BT@@diagnostic_revision@@BT@@ is explicitly authorized, its base identity matches exactly one @@BT@@selected_scope.diagnostic_parent_revision@@BT@@, that parent has the exact parent status @@BT@@PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED@@BT@@, the parent's own build-result matches it, and the parent itself binds directly to @@BT@@AUTO_BUILD_RESULT@@BT@@."
new_shape = "4. **one-hop diagnostic-parent path:** the active @@BT@@diagnostic_revision@@BT@@ is explicitly authorized and its base identity matches exactly one @@BT@@selected_scope.diagnostic_parent_revision@@BT@@ whose own build-result matches it. The parent must then use exactly one reviewed anchor: status @@BT@@PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED@@BT@@ with a direct exact bind to @@BT@@AUTO_BUILD_RESULT@@BT@@, or status @@BT@@PUBLISHED_DIAGNOSTIC_PRELOADER_PATH_LENGTH_BLOCKED_DO_NOT_RERUN_NOT_ACCEPTED@@BT@@ with a direct exact build/profile/SHA bind to @@BT@@CURRENT_STATE.accepted_baseline@@BT@@."
gk = replace_once(gk, old_shape, new_shape, "Gale workflow one-hop shape")
gk = replace_once(
    gk,
    "The one-hop shape is deliberately **not recursive**, and the accepted-baseline path is not a generic fallback: build ID, profile path and SHA-256 must all match the canonical accepted baseline exactly.",
    "The one-hop shape is deliberately **not recursive**, and neither accepted-baseline edge is a generic fallback: build ID, profile path and SHA-256 must all match the canonical accepted baseline exactly, and the one-hop accepted-baseline edge additionally requires the exact preloader-blocked / DO_NOT_RERUN parent status.",
    "Gale workflow no-recursion paragraph",
)
gk = replace_once(
    gk,
    "a second-generation diagnostic must bind to exactly one explicit @@BT@@selected_scope.diagnostic_parent_revision@@BT@@, whose own build-result and base identity bind directly to @@BT@@AUTO_BUILD_RESULT@@BT@@;",
    "a second-generation diagnostic must bind to exactly one explicit @@BT@@selected_scope.diagnostic_parent_revision@@BT@@ whose own build-result matches; that parent must bind either directly to @@BT@@AUTO_BUILD_RESULT@@BT@@ under the completed-parent status or exactly to @@BT@@CURRENT_STATE.accepted_baseline@@BT@@ under the preloader-blocked / DO_NOT_RERUN status;",
    "Gale workflow v2.4 summary",
)
insert = """## v2.4.5 exact one-hop blocked-parent -> accepted-baseline anchor

@@BT@@S1.42AK-BMAFDIAG1PATH1@@BT@@ is an identity-only successor of exact long-name @@BT@@S1.42AK-BMAFDIAG1@@BT@@. The parent is intentionally preserved as preloader-blocked / @@BT@@DO_NOT_RERUN@@BT@@ and itself derives directly from accepted @@BT@@S1.42AK@@BT@@, while @@BT@@AUTO_BUILD_RESULT@@BT@@ correctly remains the separate @@BT@@S1.42AK-BMDSFIX1@@BT@@ gameplay candidate.

Revision @@BT@@2026-10-01-import-uia-v2.4.5-one-hop-accepted-baseline-parent-chain@@BT@@ adds exactly that missing authority edge. After the active diagnostic, its build-result and its exact parent identity have all matched, the one-hop parent may bind to @@BT@@CURRENT_STATE.accepted_baseline@@BT@@ only when the parent status is exactly @@BT@@PUBLISHED_DIAGNOSTIC_PRELOADER_PATH_LENGTH_BLOCKED_DO_NOT_RERUN_NOT_ACCEPTED@@BT@@ and its base build ID, profile path and SHA-256 all equal the accepted baseline. The existing direct-AUTO, direct accepted-baseline and completed-parent -> AUTO paths remain unchanged. No recursive, arbitrary-length or generic fallback is introduced.

"""
gk = replace_once(gk, "## Critical package-root contract", insert + "## Critical package-root contract", "Gale workflow v2.4.5 section")
gk_path.write_text(gk, encoding="utf-8")

life_path = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
life = life_path.read_text(encoding="utf-8")
life = life.replace("Current/217_S1.42AK_BMAFDIAG1PATH1_PROFILE_INDEX_RECONCILIATION.md@@BT@@, @@BT@@ProfileSources/S1.42AK-BMAFDIAG1PATH1/PROFILE_INDEX_RESULT.json", "Current/217_S1.42AK_BMAFDIAG1PATH1_PROFILE_INDEX_RECONCILIATION.md@@BT@@, @@BT@@Current/218_S1.42AK_BMAFDIAG1PATH1_RUNTIME_ACTIVATION.md@@BT@@, @@BT@@ProfileSources/S1.42AK-BMAFDIAG1PATH1/PROFILE_INDEX_RESULT.json")
tail = f"""## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact / active gameplay candidate: **S1.42AK-BMDSFIX1 — not accepted**.
- Runtime/evidence pointer: **S1.42AK-BMAFDIAG1PATH1 — active diagnostic target / DIAGNOSTIC ONLY / NEVER ACCEPT**; this is evidence routing, not gameplay acceptance.
- BMAFDIAG1: **published + indexed / preloader path-length blocked / long identity DO NOT RERUN / explicit one-hop parent only**.
- BMAFDIAG1PATH1: **published + canonically indexed + runtime-armed / exact profile SHA-256 {PROFILE_SHA} / projected critical paths 219 and 221 <= 255 / not Gale-imported yet / bounded Black Mesa x Abandoned Foundry test outstanding / DIAGNOSTIC ONLY / NEVER ACCEPT**.
- Black Mesa x Abandoned Foundry remains @@BT@@NOT_YET_PROVEN@@BT@@ until runtime evidence is ingested and decided.
- BMGHDIAG3 remains completed Black Mesa x Greenhouse runtime-compatibility PASS / DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active.
- BMDSFIX1 regular Black Mesa x @@BT@@DeepSewersFlow@@BT@@ gameplay qualification remains **passive / outstanding / unwaived**.
- @@BT@@BuildSpecs/current.json@@BT@@ remains disabled at @@BT@@IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS@@BT@@.
- @@BT@@Current/AUTO_BUILD_RESULT.json@@BT@@ remains exact @@BT@@S1.42AK-BMDSFIX1@@BT@@.
- The historical Phase-B3 matrix, Oxyde ordinary-generation exception, Shatteredrooms exclusions and separate Black Mesa/Pikmin routing closure remain unchanged.

## Exact next project action

{next_action}

No gameplay run is authorized from branch-only state. The commands in @@BT@@Current/218_S1.42AK_BMAFDIAG1PATH1_RUNTIME_ACTIVATION.md@@BT@@ become executable test instructions only after this activation is integrated to @@BT@@main@@BT@@ and the permanent exact-head Knowledge Architecture gate is green.

## Permanent Gale workflow

The canonical Gale helper remains @@BT@@RuntimeTools/ReplaceActiveGaleProfileV24.ps1@@BT@@, now revision @@BT@@{NEW_REV}@@BT@@. It preserves the runtime path-length guard plus the existing direct AUTO/direct accepted-baseline/completed-parent -> AUTO paths, and adds only the explicit preloader-blocked parent -> accepted-baseline one-hop shape required by BMAFDIAG1PATH1. No recursive or generic diagnostic fallback exists.

@@BT@@RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMAFDIAG1PATH1@@BT@@ now resolves through the active diagnostic build-result, explicit blocked BMAFDIAG1 parent and exact accepted S1.42AK identity. @@BT@@AUTO_BUILD_RESULT@@BT@@ and @@BT@@BuildSpecs/current.json@@BT@@ remain BMDSFIX1 authorities.
"""
life = replace_between(life, "## Live execution state", "__NO_END__", tail, "unused") if False else life[:life.find("## Live execution state")] + tail
req("## Live execution state" in tail, "lifecycle tail construction failed")
life_path.write_text(life, encoding="utf-8")

map_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
km = map_path.read_text(encoding="utf-8")
start = km.find("The separately versioned identity-only successor **S1.42AK-BMAFDIAG1PATH1**")
end = km.find("## Authority rule", start)
req(start >= 0 and end > start, "PROJECT_KNOWLEDGE_MAP PATH1 current-anchor bounds missing")
replacement = f"""The separately versioned identity-only successor **S1.42AK-BMAFDIAG1PATH1** is now published, canonically indexed and explicitly runtime-armed as the bounded Black Mesa x Abandoned Foundry diagnostic target under @@BT@@Current/218_S1.42AK_BMAFDIAG1PATH1_RUNTIME_ACTIVATION.md@@BT@@. Exact profile @@BT@@Profiles/LC V1 S1.42AK-BMAFD1P1.r2z@@BT@@ remains SHA-256 @@BT@@{PROFILE_SHA}@@BT@@; inherited BMAFDIAG1 DLL SHA-256 remains @@BT@@{DLL_SHA}@@BT@@ and Foundry LLL config SHA-256 remains @@BT@@{FOUNDRY_CFG_SHA}@@BT@@. The long-name BMAFDIAG1 identity remains preloader-blocked / **DO NOT RERUN** and is retained only as the exact one-hop parent anchored to accepted S1.42AK. The canonical Gale resolver is revision @@BT@@{NEW_REV}@@BT@@ and permits only this exact blocked-parent -> accepted-baseline edge in addition to its existing fail-closed paths. No profile/DLL/config/package/gameplay bytes were rebuilt or changed by activation.

BMGHDIAG3 remains completed Black Mesa x Greenhouse runtime-compatibility PASS evidence / **DIAGNOSTIC ONLY / NEVER ACCEPT** and is not runtime-active. S1.42AK-BMDSFIX1 remains the separate active gameplay candidate / **NOT ACCEPTED**; its regular exact-byte Black Mesa x @@BT@@DeepSewersFlow@@BT@@ qualification remains passive, outstanding and unwaived. @@BT@@BuildSpecs/current.json@@BT@@ and @@BT@@AUTO_BUILD_RESULT@@BT@@ remain BMDSFIX1 authorities. Black Mesa x Abandoned Foundry remains @@BT@@NOT_YET_PROVEN@@BT@@ until the PATH1 runtime evidence is ingested and decided.

Exact next action: {next_action} No gameplay run is authorized until the activation PR is integrated and permanent exact-head @@BT@@main@@BT@@ Knowledge Architecture is green.

"""
km = km[:start] + replacement + km[end:]
map_path.write_text(km, encoding="utf-8")

road_path = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
road = road_path.read_text(encoding="utf-8")
road = road.replace("**Last-Validated:** 2026-09-29", "**Last-Validated:** 2026-10-01", 1)
a = road.find("## Current position")
b = road.find("## Selected scope", a)
req(a >= 0 and b > a, "roadmap current-position bounds missing")
current_position = f"""## Current position

Accepted gameplay baseline remains **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**, SHA-256 @@BT@@{ACCEPTED_SHA}@@BT@@.

Latest built artifact and active gameplay candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 @@BT@@{CANDIDATE_SHA}@@BT@@. It is not accepted and its exact regular Black Mesa x @@BT@@DeepSewersFlow@@BT@@ gate remains passive/outstanding/unwaived.

The long-name BMAFDIAG1 Black Mesa x Abandoned Foundry diagnostic remains preloader-blocked at the proven 260/262-character critical paths and is **DO_NOT_RERUN**. Its exact short-identity successor **S1.42AK-BMAFDIAG1PATH1** is published, indexed and runtime-armed only for the bounded diagnostic: profile SHA-256 @@BT@@{PROFILE_SHA}@@BT@@, projected critical paths 219/221, inherited diagnostic DLL/config bytes unchanged. @@BT@@RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMAFDIAG1PATH1@@BT@@ solely for Gale resolution/evidence attribution; @@BT@@BuildSpecs/current.json@@BT@@ remains disabled and @@BT@@AUTO_BUILD_RESULT@@BT@@ remains BMDSFIX1. Black Mesa x Abandoned Foundry remains @@BT@@NOT_YET_PROVEN@@BT@@ pending runtime evidence.

"""
road = road[:a] + current_position + road[b:]
c = road.find("## Exact next selected-scope action")
d = road.find("## Completed LC Office scrap scope", c)
req(c >= 0 and d > c, "roadmap next-action bounds missing")
road_next = f"""## Exact next selected-scope action

{next_action}

The PATH1 runtime remains diagnostic-only and cannot accept BMDSFIX1, waive the regular DeepSewersFlow gate, or authorize a universal availability override. The historical Phase-B3 matrix, Oxyde ordinary-generation exception, Shatteredrooms exclusions and Black Mesa/Pikmin routing closure remain unchanged.

"""
road = road[:c] + road_next + road[d:]
road_path.write_text(road, encoding="utf-8")

integrity_md_path = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
imd = integrity_md_path.read_text(encoding="utf-8")
old_bullet = "- **S1.42AK-BMAFDIAG1** — active diagnostic runtime/evidence target directly over accepted S1.42AK after activation integration; profile SHA-256 @@BT@@b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2@@BT@@; diagnostic DLL SHA-256 @@BT@@c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1@@BT@@; exact Black Mesa x Abandoned Foundry evidence outstanding; **DIAGNOSTIC ONLY / NEVER ACCEPT**."
new_bullets = f"""- **S1.42AK-BMAFDIAG1** — preserved preloader-blocked diagnostic parent; profile SHA-256 @@BT@@{PARENT_SHA}@@BT@@; exact 260/262-character critical-path block; **DO NOT RERUN / DIAGNOSTIC ONLY / NEVER ACCEPT**.
- **S1.42AK-BMAFDIAG1PATH1** — active diagnostic runtime/evidence target through the explicit blocked-parent -> accepted-S1.42AK one-hop chain; profile SHA-256 @@BT@@{PROFILE_SHA}@@BT@@; inherited diagnostic DLL SHA-256 @@BT@@{DLL_SHA}@@BT@@; exact Black Mesa x Abandoned Foundry evidence outstanding; **DIAGNOSTIC ONLY / NEVER ACCEPT**."""
imd = replace_once(imd, old_bullet, new_bullets, "artifact integrity BMAF bullets")
old_para = "BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. After the BMAFDIAG1 activation is integrated, runtime/evidence routing points to exact @@BT@@S1.42AK-BMAFDIAG1@@BT@@ solely for bounded diagnostic target resolution and attribution. @@BT@@BuildSpecs/current.json@@BT@@ remains disabled and @@BT@@Current/AUTO_BUILD_RESULT.json@@BT@@ remains BMDSFIX1. BMGHDIAG3 stays completed historical diagnostic PASS evidence. BMAFDIAG1 is NEVER ACCEPT, Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN pending runtime evidence, and the separate BMDSFIX1 Deep Sewers target gate remains passive/outstanding/unwaived."
new_para = "BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. Runtime/evidence routing now points to exact @@BT@@S1.42AK-BMAFDIAG1PATH1@@BT@@ solely for bounded diagnostic target resolution and attribution through blocked BMAFDIAG1 -> accepted S1.42AK. @@BT@@BuildSpecs/current.json@@BT@@ remains disabled and @@BT@@Current/AUTO_BUILD_RESULT.json@@BT@@ remains BMDSFIX1. BMGHDIAG3 stays completed historical diagnostic PASS evidence. Both BMAF diagnostics are NEVER ACCEPT; the long identity is DO_NOT_RERUN, Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN pending PATH1 runtime evidence, and the separate BMDSFIX1 Deep Sewers target gate remains passive/outstanding/unwaived."
imd = replace_once(imd, old_para, new_para, "artifact integrity BMAF routing paragraph")
integrity_md_path.write_text(imd, encoding="utf-8")

# ---- Durable activation record ------------------------------------------
activation = f"""# S1.42AK-BMAFDIAG1PATH1 Runtime Activation

**Date:** 2026-10-01  
**Status:** PUBLISHED / INDEXED / ACTIVE DIAGNOSTIC RUNTIME TARGET / TEST OUTSTANDING / NEVER ACCEPT  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted / passive Deep Sewers gate unchanged  
**Diagnostic:** S1.42AK-BMAFDIAG1PATH1  
**Diagnostic profile:** @@BT@@{PROFILE}@@BT@@  
**Diagnostic profile identity:** @@BT@@{PROFILE_NAME}@@BT@@  
**Diagnostic profile SHA-256:** @@BT@@{PROFILE_SHA}@@BT@@  
**Inherited BMAFDIAG1 DLL SHA-256:** @@BT@@{DLL_SHA}@@BT@@  
**Inherited Foundry LLL config SHA-256:** @@BT@@{FOUNDRY_CFG_SHA}@@BT@@  
**Explicit diagnostic parent:** S1.42AK-BMAFDIAG1 / preloader-blocked / DO_NOT_RERUN

## Activation decision

The exact reviewed, exact-byte-published and canonically indexed BMAFDIAG1PATH1 identity-only successor is authorized as the active runtime/evidence target for one bounded Black Mesa x Abandoned Foundry diagnostic run after this activation is integrated to @@BT@@main@@BT@@ and permanent exact-head Knowledge Architecture is green.

This is an authority/routing transition plus the minimum fail-closed Gale resolver extension required by the real provenance chain. It does not rebuild or mutate the PATH1 profile, inherited BMAFDIAG1 DLL, Foundry LLL config, package/gameplay bytes, accepted S1.42AK or the separate BMDSFIX1 gameplay candidate. @@BT@@BuildSpecs/current.json@@BT@@ remains disabled and @@BT@@Current/AUTO_BUILD_RESULT.json@@BT@@ remains exact BMDSFIX1.

BMAFDIAG1PATH1 is **DIAGNOSTIC ONLY / NEVER ACCEPT**. Runtime activation cannot accept it, cannot accept BMDSFIX1, cannot waive or replace BMDSFIX1's passive regular Black Mesa x @@BT@@DeepSewersFlow@@BT@@ qualification, and cannot mark Black Mesa x Abandoned Foundry proven before runtime evidence exists. Long-name BMAFDIAG1 remains **DO NOT RERUN**.

## Exact runtime authority chain

@@BT@@RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMAFDIAG1PATH1@@BT@@ resolves fail-closed through:

1. @@BT@@CURRENT_STATE.controllers.runtime_active_build@@BT@@;
2. active @@BT@@CURRENT_STATE.selected_scope.diagnostic_revision@@BT@@ = exact BMAFDIAG1PATH1;
3. @@BT@@{BUILD_RESULT}@@BT@@ and exact output SHA @@BT@@{PROFILE_SHA}@@BT@@;
4. explicit @@BT@@CURRENT_STATE.selected_scope.diagnostic_parent_revision@@BT@@ = blocked long-name BMAFDIAG1;
5. the parent's exact build-result/profile SHA @@BT@@{PARENT_SHA}@@BT@@;
6. exact parent base identity = @@BT@@CURRENT_STATE.accepted_baseline@@BT@@ S1.42AK / @@BT@@{ACCEPTED_SHA}@@BT@@.

Canonical Gale revision @@BT@@{NEW_REV}@@BT@@ adds only the explicit one-hop parent -> accepted-baseline edge. That edge requires the exact parent status @@BT@@{PARENT_STATUS}@@BT@@ plus exact accepted build ID/profile/SHA agreement. Existing direct-AUTO, direct accepted-baseline and completed-parent -> AUTO paths remain intact. There is no recursive or generic fallback.

## Preserved byte/provenance gates

- PATH1 profile SHA-256: @@BT@@{PROFILE_SHA}@@BT@@;
- inherited diagnostic DLL SHA-256: @@BT@@{DLL_SHA}@@BT@@;
- inherited Foundry LLL config SHA-256: @@BT@@{FOUNDRY_CFG_SHA}@@BT@@;
- archive members: 337;
- relative to exact published BMAFDIAG1 parent, changed existing member: @@BT@@export.r2x@@BT@@ only;
- added/removed members: zero;
- package changes: zero;
- config changes in PATH1: zero;
- local plugin builds: zero;
- projected critical Gale runtime paths: 219 and 221 characters, both <= project budget 255;
- canonical index: @@BT@@{PROFILE_INDEX}@@BT@@ / @@BT@@EXPECTED_HASHES@@BT@@ resolution.

## Runtime qualification contract

Run the exact PATH1 diagnostic on **Black Mesa**. A sufficient run must establish:

1. @@BT@@[BMAFDIAG1] ARMED@@BT@@ without startup refusal;
2. @@BT@@[BMAFDIAG1] SELECTED Black Mesa Abandoned Foundry / FoundryFlow; pre-reduction viable wrapper confirmed; normalized rarity=100; pool=<N>->1@@BT@@;
3. DunGen completes without exhausted retries or fatal generation abort;
4. @@BT@@[BMAFDIAG1] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4@@BT@@;
5. the player normally enters and exits through the main entrance;
6. alternate IDs 1, 2 and 3 are directly traversed; bidirectional use should be obtained where practical;
7. no severe clipping or inaccessible required entrance geometry is observed at exercised endpoints;
8. no new severe/persistent target-attributable routing or NavMesh failure is present;
9. no @@BT@@[BMAFDIAG1] REFUSED@@BT@@, @@BT@@TOPOLOGY_INCONCLUSIVE@@BT@@, @@BT@@TRAVERSAL_INCONCLUSIVE@@BT@@ or @@BT@@OBSERVER_INCONCLUSIVE@@BT@@ marker invalidates the run.

Successful native teleport alone must not be overclaimed as visual geometry proof. The separate Black-Mesa/Pikmin routing-recovery scope remains closed during this diagnostic.

## Exact Gale replacement/import one-liner

Use only after this activation is integrated on @@BT@@main@@BT@@ and exact-head CI is green:

@@BT@@@@BT@@@@BT@@powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
@@BT@@@@BT@@@@BT@@

The launcher must resolve the exact chain above, download @@BT@@{PROFILE}@@BT@@, verify SHA-256 @@BT@@{PROFILE_SHA}@@BT@@ and pass the local 255-character path guard before destructive replacement. Follow its numeric old-profile selection and explicit @@BT@@y@@BT@@ deletion confirmation; do not manually substitute another profile.

## Exact build-specific runtime-log uploader

After the bounded gameplay run is complete, use this single line:

@@BT@@@@BT@@@@BT@@powershell
$ErrorActionPreference='Stop';$build='{BUILD}';$log=Join-Path $env:APPDATA 'com.kesomannen.gale\lethal-company\profiles\{PROFILE_NAME}\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $log -PathType Leaf)){{throw "Expected runtime log not found: $log"}};$bytes=[IO.File]::ReadAllBytes($log);if($bytes.Length -le 0){{throw 'Runtime log is empty'}};$text=[Text.Encoding]::UTF8.GetString($bytes);if($text.IndexOf('[BMAFDIAG1]',[StringComparison]::Ordinal) -lt 0){{throw 'Refusing upload: exact local LogOutput.log contains no [BMAFDIAG1] marker'}};$localSha=([BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($bytes))).Replace('-','').ToLowerInvariant();$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;$fallback=Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe';if(!$gh -and (Test-Path -LiteralPath $fallback)){{$gh=$fallback}};if(!$gh -and (Get-Command winget -ErrorAction SilentlyContinue)){{winget install --id GitHub.cli -e --source winget --accept-source-agreements --accept-package-agreements | Out-Host;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh -and (Test-Path -LiteralPath $fallback)){{$gh=$fallback}}}};if(!$gh){{throw 'GitHub CLI (gh) could not be resolved or bootstrapped'}};& $gh auth status -h github.com *> $null;if($LASTEXITCODE -ne 0){{& $gh auth login -h github.com -w;if($LASTEXITCODE -ne 0){{throw 'GitHub authentication failed'}}}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dest='RuntimeInbox/Current/LogOutput.log';$existing=$null;try{{$existing=(& $gh api "repos/$repo/contents/$dest?ref=main" --jq '.sha' 2>$null)}}catch{{}};$payload=@{{message="Upload $build runtime log ($localSha)";content=[Convert]::ToBase64String($bytes);branch='main'}};if($existing){{$payload.sha=$existing}};$json=$payload|ConvertTo-Json -Compress;$tmp=[IO.Path]::GetTempFileName();try{{[IO.File]::WriteAllText($tmp,$json,[Text.UTF8Encoding]::new($false));& $gh api --method PUT "repos/$repo/contents/$dest" --input $tmp;if($LASTEXITCODE -ne 0){{throw 'Runtime log upload failed'}}}}finally{{Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue}};Write-Host "Uploaded $build LogOutput.log SHA-256 $localSha" -ForegroundColor Green
@@BT@@@@BT@@@@BT@@

Runtime evidence must be uploaded while @@BT@@RuntimeInbox/ACTIVE_BUILD.txt = {BUILD}@@BT@@. If gameplay is already complete and only upload remains, do not repeat gameplay solely for evidence submission.

## Preserved boundaries and post-diagnostic routing

Accepted S1.42AK and exact BMDSFIX1 gameplay bytes remain unchanged. BMDSFIX1 stays **NOT ACCEPTED** and its regular Deep Sewers target gate remains passive/outstanding/unwaived. Long-name BMAFDIAG1 stays **DO NOT RERUN**. After the PATH1 evidence is ingested and decided, runtime/evidence routing must be explicitly reconciled rather than inferred from this activation record.
"""
(ROOT / ACTIVATION).write_text(activation, encoding="utf-8")

# Replace placeholders used to keep this transformer source delimiter-safe.
for rel in [
    "Knowledge/GALE_PROFILE_WORKFLOW.md",
    "Knowledge/CURRENT_LIFECYCLE.md",
    "Current/PROJECT_KNOWLEDGE_MAP.md",
    "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md",
    "Current/ARTIFACT_EVIDENCE_INTEGRITY.md",
    ACTIVATION,
]:
    p = ROOT / rel
    p.write_text(p.read_text(encoding="utf-8").replace("@@BT@@", chr(96)), encoding="utf-8")

print("PASS: staged exact BMAFDIAG1PATH1 runtime activation with one-hop blocked-parent -> accepted-baseline Gale authority; protected artifact bytes untouched")
