#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GAMEPLAY_BUILD_ID = "S1.42AK-BMDSFIX1"
GAMEPLAY_PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
GAMEPLAY_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
BMDSFIX1_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
BMDSFIX1_DLL_ENTRY = "BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"

PARENT_BUILD_ID = "S1.42AK-BMDSFIX1-DIAG1"
PARENT_PROFILE = "Profiles/LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector.r2z"
PARENT_SHA = "31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e"
PARENT_BUILD_RESULT = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json"

BUILD_ID = "S1.42AK-BMDSFIX1-DIAG1PATH1"
PROFILE_NAME = "LC V1 S1.42AK-D1P1"
PROFILE = "Profiles/LC V1 S1.42AK-D1P1.r2z"
PROFILE_SHA = "0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6"
DIAG_DLL_SHA = "3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1"
DIAG_DLL_ENTRY = "BepInEx/plugins/S142AKBMDSFix1Diag1/S142AKBMDSFix1Diag1.dll"
BUILD_SPEC = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1.json"
BUILD_RESULT = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC_EVIDENCE = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
PUBLICATION_EVIDENCE = "BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
PROFILE_INDEX_RESULT = "ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json"
PROFILE_SOURCES = "ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/"
FILE_INDEX = "ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/FILE_INDEX.json"
REVIEW_CHECKPOINT = "Current/182_S1.42AK_BMDSFIX1_DIAG1PATH1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md"
PUBLICATION_CHECKPOINT = "Current/184_S1.42AK_BMDSFIX1_DIAG1PATH1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md"
ACTIVATION = "Current/185_S1.42AK_BMDSFIX1_DIAG1PATH1_RUNTIME_ACTIVATION.md"

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

state = load_json("Current/CURRENT_STATE.json")
require(state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline drift")
require(state["latest_built_artifact"]["build_id"] == GAMEPLAY_BUILD_ID, "Latest artifact drift")
require(state["latest_built_artifact"]["sha256"] == GAMEPLAY_SHA, "Latest artifact SHA drift")
require(state["active_candidate"]["build_id"] == GAMEPLAY_BUILD_ID, "Gameplay candidate drift")
require(state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED", "Gameplay candidate status drift")
require(state["active_candidate"]["sha256"] == GAMEPLAY_SHA, "Gameplay candidate SHA drift")
require(state["runtime_test_outstanding"] is True, "Regular BMDSFIX1 runtime gate must remain outstanding")
require(state["selected_scope"]["candidate_build_id"] == GAMEPLAY_BUILD_ID, "Selected-scope candidate drift")
require(state["selected_scope"]["phase_c"]["bmdsfix1_target_status"] == "OUTSTANDING_BLACK_MESA_DEEP_SEWERS", "BMDSFIX1 target gate drift")
require(state["selected_scope"]["status"] == "PHASE_C3F18_DIAG1_PRELOADER_BLOCKED_DIAG1PATH1_PUBLISHED_INDEXED_ACTIVATION_OUTSTANDING", "Selected-scope activation boundary drift")
require(state["controllers"]["runtime_active_build"] == PARENT_BUILD_ID, "Runtime controller was already redirected")
require((ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == PARENT_BUILD_ID, "ACTIVE_BUILD drift")

current_spec = load_json("BuildSpecs/current.json")
require(current_spec["enabled"] is False, "Build controller must remain disabled")
require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "Build controller identity drift")
require(current_spec["base_profile"] == GAMEPLAY_PROFILE and current_spec["base_sha256"] == GAMEPLAY_SHA, "Build controller gameplay guard drift")

auto_result = load_json("Current/AUTO_BUILD_RESULT.json")
require(auto_result["build_id"] == GAMEPLAY_BUILD_ID, "AUTO_BUILD_RESULT is not BMDSFIX1")
require(auto_result["output_profile"] == GAMEPLAY_PROFILE and auto_result["output_sha256"] == GAMEPLAY_SHA, "AUTO_BUILD_RESULT gameplay identity drift")

scope = state["selected_scope"]
parent = scope.get("diagnostic_revision")
require(isinstance(parent, dict) and parent.get("build_id") == PARENT_BUILD_ID, "Long-name DIAG1 parent pointer drift")
require(parent.get("status") == "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED", "Long-name DIAG1 parent status drift")
require(parent.get("profile") == PARENT_PROFILE and parent.get("sha256") == PARENT_SHA, "Long-name DIAG1 parent identity drift")
require(parent.get("runtime_validation_status") == "PRELOADER_BLOCKED_BEFORE_DIAGNOSTIC_EXECUTION_DO_NOT_RERUN_DIAG1PATH1_PUBLISHED_INDEXED_ACTIVATION_OUTSTANDING", "Long-name DIAG1 preloader-block state drift")

successor = scope.get("diagnostic_successor_revision")
require(isinstance(successor, dict) and successor.get("build_id") == BUILD_ID, "DIAG1PATH1 successor metadata missing")
require(successor.get("status") == "PUBLISHED_INDEXED_NOT_ARMED", "DIAG1PATH1 successor status drift")
require(successor.get("classification") == "DIAGNOSTIC_SUPPORT_ONLY_NEVER_ACCEPT", "DIAG1PATH1 classification drift")
require(successor.get("base_build_id") == PARENT_BUILD_ID, "DIAG1PATH1 parent build drift")
require(successor.get("base_profile") == PARENT_PROFILE and successor.get("base_sha256") == PARENT_SHA, "DIAG1PATH1 parent identity drift")
require(successor.get("output_profile") == PROFILE and successor.get("profile_sha256") == PROFILE_SHA, "DIAG1PATH1 output identity drift")
require(successor.get("indexed") is True and successor.get("runtime_armed") is False, "DIAG1PATH1 index/arming boundary drift")
require(successor.get("profile_index_result") == PROFILE_INDEX_RESULT, "DIAG1PATH1 profile-index pointer drift")

require(sha256_file(GAMEPLAY_PROFILE) == GAMEPLAY_SHA, "Exact BMDSFIX1 gameplay profile SHA mismatch")
require(sha256_file(PARENT_PROFILE) == PARENT_SHA, "Exact long-name DIAG1 parent profile SHA mismatch")
require(sha256_file(PROFILE) == PROFILE_SHA, "Exact DIAG1PATH1 profile SHA mismatch")

build_result = load_json(BUILD_RESULT)
require(build_result["build_id"] == BUILD_ID, "DIAG1PATH1 build result ID drift")
require(build_result["base_profile"] == PARENT_PROFILE and build_result["base_sha256"] == PARENT_SHA, "DIAG1PATH1 build-result parent drift")
require(build_result["output_profile"] == PROFILE and build_result["output_sha256"] == PROFILE_SHA, "DIAG1PATH1 build-result output drift")
require(build_result["zip_members"] == 338, "DIAG1PATH1 archive member count drift")
require(build_result["changed_existing_members"] == ["export.r2x"], "DIAG1PATH1 changed-member contract drift")
require(build_result["added_members"] == [] and build_result["mod_state_changes"] == [] and build_result["mod_additions"] == [] and build_result["mod_removals"] == [], "DIAG1PATH1 identity-only delta drift")

index_result = load_json(PROFILE_INDEX_RESULT)
require(index_result["build_id"] == BUILD_ID, "DIAG1PATH1 profile-index build ID drift")
require(index_result["profile_path"] == PROFILE and index_result["sha256"] == PROFILE_SHA, "DIAG1PATH1 profile-index identity drift")
require(index_result["profile_name"] == PROFILE_NAME and index_result["zip_members"] == 338, "DIAG1PATH1 profile-index metadata drift")
require(index_result["build_id_resolution"] == "EXPECTED_HASHES", "DIAG1PATH1 profile-index resolution drift")

expected_hashes = load_json("Profiles/EXPECTED_HASHES.json")
require(PROFILE in expected_hashes, "DIAG1PATH1 EXPECTED_HASHES mapping missing")
require(expected_hashes[PROFILE]["build_id"] == BUILD_ID and expected_hashes[PROFILE]["sha256"] == PROFILE_SHA, "DIAG1PATH1 EXPECTED_HASHES identity drift")

with zipfile.ZipFile(ROOT / PROFILE, "r") as archive:
    require(len(archive.infolist()) == 338, "DIAG1PATH1 materialized archive member count drift")
    require(DIAG_DLL_ENTRY in archive.namelist(), "Inherited DIAG1 selector DLL missing from DIAG1PATH1")
    require(BMDSFIX1_DLL_ENTRY in archive.namelist(), "Inherited BMDSFIX1 DLL missing from DIAG1PATH1")
    require(hashlib.sha256(archive.read(DIAG_DLL_ENTRY)).hexdigest() == DIAG_DLL_SHA, "Inherited DIAG1 selector DLL SHA mismatch")
    require(hashlib.sha256(archive.read(BMDSFIX1_DLL_ENTRY)).hexdigest() == BMDSFIX1_DLL_SHA, "Inherited BMDSFIX1 DLL SHA mismatch")

parent_revision = copy.deepcopy(parent)
parent_revision["status"] = "PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED"
parent_revision["runtime_armed"] = False
parent_revision["runtime_role"] = "PRELOADER_BLOCKED_DIAGNOSTIC_PARENT_DO_NOT_RERUN_NEVER_ACCEPT"
parent_revision["runtime_validation_status"] = "PRELOADER_BLOCKED_BEFORE_DIAGNOSTIC_EXECUTION_DO_NOT_RERUN_PARENT_OF_DIAG1PATH1"
scope["diagnostic_parent_revision"] = parent_revision

active_diag = copy.deepcopy(successor)
active_diag["status"] = "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED"
active_diag["runtime_armed"] = True
active_diag["profile"] = PROFILE
active_diag["sha256"] = PROFILE_SHA
active_diag["build_spec"] = BUILD_SPEC
active_diag["build_result"] = BUILD_RESULT
active_diag["static_evidence"] = STATIC_EVIDENCE
active_diag["publication_evidence"] = PUBLICATION_EVIDENCE
active_diag["activation_record"] = ACTIVATION
active_diag["runtime_role"] = "DIAGNOSTIC_SUPPORT_ONLY_DETERMINISTIC_BLACK_MESA_DEEP_SEWERS_SELECTOR_IDENTITY_SHORTENED_NEVER_ACCEPT"
active_diag["runtime_validation_status"] = "RUNTIME_TEST_OUTSTANDING_SUPPORTING_EVIDENCE_ONLY_NOT_ACCEPTED"
scope["diagnostic_revision"] = active_diag
scope["diagnostic_successor_revision"] = copy.deepcopy(active_diag)
scope["diagnostic_runtime_activation"] = ACTIVATION
scope["diagnostic_static_evidence"] = STATIC_EVIDENCE
scope["diagnostic_publication_evidence"] = PUBLICATION_EVIDENCE

scope["status"] = "PHASE_C3F18_DIAG1PATH1_RUNTIME_ACTIVE_SUPPORTING_EVIDENCE_OUTSTANDING"
scope["finding"] = (
    "Exact published/indexed S1.42AK-BMDSFIX1-DIAG1PATH1 is now the active diagnostic-only runtime/evidence target using the short Gale profile identity "
    "LC V1 S1.42AK-D1P1, SHA-256 0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6. "
    "It is byte-identical to the blocked long-name DIAG1 diagnostic except export.r2x profileName metadata, with 338 members and unchanged DIAG1 selector, BMDSFIX1 and normalizer DLL hashes. "
    "The long-name S1.42AK-BMDSFIX1-DIAG1 is retained only as the explicit one-hop diagnostic parent and must not be rerun. "
    "S1.42AK-BMDSFIX1 remains the active gameplay candidate / not accepted, and its regular exact-byte Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived."
)
scope["analysis_contract"] = (
    "Treat S1.42AK-BMDSFIX1-DIAG1PATH1 only as an active diagnostic-support runtime overlay for deterministic Black Mesa x DeepSewersFlow evidence. "
    "Require the inherited [BMDSFIX1-DIAG1] ARMED and SELECTED markers, inherited [BMDSFIX1] ARMED and target APPLIED multiplier ->1 markers, completed generation and normal landed gameplay without the prior persistent retry/Entering-the-atmosphere failure or a new severe target-attributable regression. "
    "Never accept DIAG1PATH1, never infer BMDSFIX1 acceptance from this diagnostic, never rerun the blocked long-name DIAG1, never waive the regular exact-byte BMDSFIX1 target gate, and keep Black Mesa x Greenhouse/BMGHDIAG separate."
)
scope["next_action"] = (
    "After this activation is integrated and exact-head CI validated, import exact active S1.42AK-BMDSFIX1-DIAG1PATH1 through the canonical repository-driven Gale v2.4 launcher, run one bounded Black Mesa diagnostic, and upload its exact BepInEx/LogOutput.log with the DIAG1PATH1 build-specific uploader. "
    "Treat the result as supporting diagnostic evidence only; the regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding until separately satisfied."
)
state["controllers"]["runtime_active_build"] = BUILD_ID
state["next_action"] = scope["next_action"]
write_json("Current/CURRENT_STATE.json", state)
(ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID + "\n", encoding="utf-8")

integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
pending = integrity.get("pending_profiles", [])
by_id = {x.get("build_id"): x for x in pending if isinstance(x, dict)}
require(GAMEPLAY_BUILD_ID in by_id, "BMDSFIX1 pending evidence entry missing")
require(PARENT_BUILD_ID in by_id, "DIAG1 pending evidence entry missing")
require(BUILD_ID not in by_id, "DIAG1PATH1 already registered as pending evidence")
require(by_id[PARENT_BUILD_ID].get("role") == "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING", "DIAG1 pending role drift")
by_id[PARENT_BUILD_ID]["activation_record"] = "Current/180_S1.42AK_BMDSFIX1_DIAG1_RUNTIME_ACTIVATION.md"
by_id[PARENT_BUILD_ID]["note"] = (
    "Exact long-name DIAG1 bytes remain preserved but are preloader-blocked by the observed 260/262-character Gale-local nested paths and must not be rerun. "
    "They are retained only as the explicit one-hop diagnostic parent for the short-identity DIAG1PATH1 successor."
)
pending.append({
    "build_id": BUILD_ID,
    "role": "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
    "profile": PROFILE,
    "profile_sha256": PROFILE_SHA,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "export": PROFILE_SOURCES + "export.r2x",
    "build_spec": BUILD_SPEC,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC_EVIDENCE,
    "publication_evidence": PUBLICATION_EVIDENCE,
    "activation_record": ACTIVATION,
    "diagnostic_dll_sha256": DIAG_DLL_SHA,
    "inherited_bmdsfix1_dll_sha256": BMDSFIX1_DLL_SHA,
    "runtime_evidence_required": False,
    "partial_runtime_evidence_present": False,
    "note": (
        "Exact published/indexed DIAG1PATH1 bytes are runtime-armed only as the short-identity deterministic Black Mesa x DeepSewersFlow selector over the still-unaccepted BMDSFIX1 gameplay candidate. "
        "Supporting diagnostic evidence cannot satisfy or waive regular exact-byte BMDSFIX1 qualification."
    )
})
integrity["updated"] = "2026-09-25"
integrity["last_validated"] = "2026-09-25"
observations = integrity.get("verified_repository_api_observations", [])
old_obs = "S1.42AK-BMDSFIX1-DIAG1 exact profile SHA-256 31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e is runtime-armed solely as a supporting deterministic Deep Sewers diagnostic over exact BMDSFIX1; BMDSFIX1 remains the unaccepted gameplay candidate and its regular target gate remains outstanding."
require(old_obs in observations, "DIAG1 integrity observation drift")
observations[observations.index(old_obs)] = (
    "S1.42AK-BMDSFIX1-DIAG1 exact profile SHA-256 31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e is preserved as the preloader-blocked one-hop diagnostic parent and must not be rerun."
)
observations.append(
    "S1.42AK-BMDSFIX1-DIAG1PATH1 exact profile SHA-256 0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6 is the active diagnostic-only runtime/evidence target; it differs from DIAG1 only by export.r2x profile identity and cannot accept or waive BMDSFIX1."
)
write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

path = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
text = path.read_text(encoding="utf-8")
text = replace_once(text, "**Last-Validated:** 2026-09-24", "**Last-Validated:** 2026-09-25", "artifact-integrity validation date")
text = replace_once(
    text,
    "- **S1.42AK-BMDSFIX1-DIAG1** — active diagnostic runtime target over exact BMDSFIX1; profile SHA-256 `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`; DIAG1 DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; supporting deterministic Deep Sewers evidence only; never a gameplay base or acceptance candidate.",
    "- **S1.42AK-BMDSFIX1-DIAG1** — preserved preloader-blocked diagnostic parent; profile SHA-256 `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`; DIAG1 DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; must not be rerun and is not the active runtime/evidence target.\n- **S1.42AK-BMDSFIX1-DIAG1PATH1** — active diagnostic runtime/evidence target using short identity `LC V1 S1.42AK-D1P1`; profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; inherited DIAG1 selector DLL SHA-256 `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`; supporting deterministic Deep Sewers evidence only; never a gameplay base or acceptance candidate.",
    "artifact-integrity pending diagnostics",
)
text = replace_once(
    text,
    "BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. `RuntimeInbox/ACTIVE_BUILD.txt` now points to exact DIAG1 solely for Gale target resolution and diagnostic evidence attribution; activation changes only lifecycle/controller/evidence routing and regenerates no gameplay/config/package/profile/plugin bytes. DIAG1 may supply supporting deterministic Black Mesa x `DeepSewersFlow` evidence but cannot qualify or accept BMDSFIX1. Black Mesa x Greenhouse remains separate and unproven.",
    "BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. `RuntimeInbox/ACTIVE_BUILD.txt` now points to exact DIAG1PATH1 solely for Gale target resolution and diagnostic evidence attribution; blocked long-name DIAG1 is retained only as the one-hop parent and must not be rerun. Activation changes only lifecycle/controller/evidence routing and regenerates no gameplay/config/package/profile/plugin bytes. DIAG1PATH1 may supply supporting deterministic Black Mesa x `DeepSewersFlow` evidence but cannot qualify or accept BMDSFIX1. Black Mesa x Greenhouse remains separate and unproven.",
    "artifact-integrity routing paragraph",
)
path.write_text(text, encoding="utf-8")

path = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
text = path.read_text(encoding="utf-8")
text = replace_once(
    text,
    "The separately versioned `S1.42AK-BMDSFIX1-DIAG1PATH1` identity-only successor is now exact-byte published and canonically indexed. Publication authority is `Current/184_S1.42AK_BMDSFIX1_DIAG1PATH1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md`; exact profile `Profiles/LC V1 S1.42AK-D1P1.r2z` remains SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, with only the reviewed `export.r2x` profile-identity delta relative to long-name DIAG1 and all protected DLL/package/config bytes unchanged. Canonical indexing is recorded by `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`: build ID `S1.42AK-BMDSFIX1-DIAG1PATH1`, profile identity `LC V1 S1.42AK-D1P1`, 338 archive members, resolution through `EXPECTED_HASHES`. DIAG1PATH1 remains **not runtime-armed / diagnostic support only / never accept**.",
    "The separately versioned `S1.42AK-BMDSFIX1-DIAG1PATH1` identity-only successor is exact-byte published, canonically indexed and now explicitly runtime-armed as the active **diagnostic-support-only** target. Activation authority is `Current/185_S1.42AK_BMDSFIX1_DIAG1PATH1_RUNTIME_ACTIVATION.md`; exact profile `Profiles/LC V1 S1.42AK-D1P1.r2z` remains SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, with only the reviewed `export.r2x` profile-identity delta relative to long-name DIAG1 and all protected DLL/package/config bytes unchanged. Canonical indexing remains `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`: build ID `S1.42AK-BMDSFIX1-DIAG1PATH1`, profile identity `LC V1 S1.42AK-D1P1`, 338 archive members, resolution through `EXPECTED_HASHES`. The long-name DIAG1 is retained only as the preloader-blocked one-hop diagnostic parent and must not be rerun. DIAG1PATH1 is **diagnostic support only / never acceptable as gameplay**.",
    "lifecycle PATH1 activation paragraph",
)
old_live = """- Runtime/evidence pointer: **S1.42AK-BMDSFIX1-DIAG1**, but the long-name profile is **preloader-blocked and must not be rerun**.
- Diagnostic successor: **S1.42AK-BMDSFIX1-DIAG1PATH1 — published / indexed / not armed / diagnostic support only / never accept**.
- Runtime test outstanding: **yes — regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived; DIAG1PATH1 is published/indexed but no DIAG1PATH1 runtime is authorized before a separate explicit activation checkpoint**."""
new_live = """- Runtime/evidence pointer: **S1.42AK-BMDSFIX1-DIAG1PATH1 — active diagnostic-support-only target / never accept**.
- Diagnostic parent: **S1.42AK-BMDSFIX1-DIAG1 — preloader-blocked one-hop parent / must not be rerun**.
- Runtime test outstanding: **yes — one bounded DIAG1PATH1 supporting diagnostic run is now authorized after exact-head activation validation; regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived**."""
text = replace_once(text, old_live, new_live, "lifecycle live-state bullets")
text = replace_once(
    text,
    "- Selected scope: **Universal Interior Viability / Equal Availability — DIAG1PATH1 publication/indexing complete; explicit runtime activation is the next bounded gate; gameplay candidate unchanged**.",
    "- Selected scope: **Universal Interior Viability / Equal Availability — DIAG1PATH1 runtime/evidence activation complete on this branch; exact-head integration validation remains required before import/run; gameplay candidate unchanged**.",
    "lifecycle selected-scope bullet",
)
text = replace_once(
    text,
    "- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1` remains unchanged until a later explicit successor activation; it is runtime/evidence routing, not acceptance authority.",
    "- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1PATH1` is runtime/evidence routing only and is not acceptance authority.",
    "lifecycle active-build bullet",
)
old_next = """Perform a separate explicit `S1.42AK-BMDSFIX1-DIAG1PATH1` runtime-activation checkpoint. The activation may change runtime/evidence routing only after re-verifying the exact published/indexed profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; it must not rebuild or alter profile, DLL, package, config or gameplay bytes and cannot accept DIAG1PATH1 or BMDSFIX1. Do **not** import or run DIAG1PATH1 before that activation checkpoint is integrated and validated. The regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived."""
new_next = """After this DIAG1PATH1 runtime/evidence activation is integrated and exact-head validated, import exact `S1.42AK-BMDSFIX1-DIAG1PATH1` through the canonical Gale v2.4 helper and run one bounded Black Mesa supporting diagnostic. Require inherited `[BMDSFIX1-DIAG1] ARMED` / deterministic DeepSewersFlow selection plus inherited `[BMDSFIX1] ARMED` / target `APPLIED ... ->1`, completed generation and normal landed gameplay without the prior persistent retry/`Entering the atmosphere` failure or a new severe target-attributable regression. Upload that exact run's `BepInEx/LogOutput.log` with the build-specific DIAG1PATH1 uploader. DIAG1PATH1 remains never-accept diagnostic support; the regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived."""
text = replace_once(text, old_next, new_next, "lifecycle next action")
text = replace_once(
    text,
    "`RuntimeInbox/ACTIVE_BUILD.txt` still points to `S1.42AK-BMDSFIX1-DIAG1`, so invoking the helper now would still resolve the preloader-blocked long-name diagnostic and remains **not authorized**. DIAG1PATH1 is now published and indexed, but the runtime pointer must change only in the separate explicit activation checkpoint. After that checkpoint is integrated and exact-head validated, the repository-driven helper must resolve the exact DIAG1PATH1 bytes.",
    "`RuntimeInbox/ACTIVE_BUILD.txt` now points to `S1.42AK-BMDSFIX1-DIAG1PATH1`. The Gale v2.4 one-hop diagnostic-parent resolver must therefore resolve exact profile `Profiles/LC V1 S1.42AK-D1P1.r2z` / SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6` through `CURRENT_STATE.selected_scope.diagnostic_revision`, with blocked DIAG1 retained only as `diagnostic_parent_revision`. Import remains unauthorized until this activation is integrated and exact-head validated.",
    "lifecycle Gale paragraph",
)
path.write_text(text, encoding="utf-8")

path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
text = path.read_text(encoding="utf-8")
old_map = "The published/indexed `S1.42AK-BMDSFIX1-DIAG1` still occupies the runtime/evidence pointer, but two consecutive launches are documented as preloader-blocked before diagnostic execution and the long-name profile must not be rerun. Its identity-only successor `S1.42AK-BMDSFIX1-DIAG1PATH1` is now exact-byte published and canonically indexed: profile `Profiles/LC V1 S1.42AK-D1P1.r2z`, SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, canonical index result `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`, 338 archive members, `EXPECTED_HASHES` resolution. It remains not runtime-armed, diagnostic support only and never acceptable as gameplay. The immediate repository task is a separate explicit DIAG1PATH1 runtime-activation checkpoint; do not import or run it before that gate is integrated and validated. BMDSFIX1 remains not accepted, its regular qualification remains outstanding and unwaived, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse/BMGHDIAG remains separate."
new_map = "The preloader-blocked long-name `S1.42AK-BMDSFIX1-DIAG1` is now retained only as the explicit one-hop diagnostic parent and must not be rerun. Its identity-only successor `S1.42AK-BMDSFIX1-DIAG1PATH1` is exact-byte published, canonically indexed and explicitly activated as the runtime/evidence diagnostic target: profile `Profiles/LC V1 S1.42AK-D1P1.r2z`, SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, canonical index result `ProfileSources/S1.42AK-BMDSFIX1-DIAG1PATH1/PROFILE_INDEX_RESULT.json`, 338 archive members, `EXPECTED_HASHES` resolution. It remains diagnostic support only and never acceptable as gameplay. Do not import or run it until this activation is integrated and exact-head validated. BMDSFIX1 remains not accepted, its regular qualification remains outstanding and unwaived, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse/BMGHDIAG remains separate."
text = replace_once(text, old_map, new_map, "knowledge-map PATH1 activation")
path.write_text(text, encoding="utf-8")

path = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
text = path.read_text(encoding="utf-8")
text = replace_once(
    text,
    "Latest built artifact and active gameplay runtime candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted. Exact `S1.42AK-BMDSFIX1-DIAG1` is now the active diagnostic runtime overlay, so `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1` solely for Gale resolution/evidence attribution; `BuildSpecs/current.json` remains disabled while guarding the exact BMDSFIX1 candidate. The diagnostic run is supporting evidence only and does not waive the regular BMDSFIX1 target gate.",
    "Latest built artifact and active gameplay runtime candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`. It is not accepted. Exact short-identity `S1.42AK-BMDSFIX1-DIAG1PATH1` is now the active diagnostic runtime/evidence overlay, so `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1PATH1` solely for Gale resolution/evidence attribution; blocked long-name DIAG1 is retained only as its one-hop parent and must not be rerun. `BuildSpecs/current.json` remains disabled while guarding the exact BMDSFIX1 candidate. The diagnostic run is supporting evidence only and does not waive the regular BMDSFIX1 target gate.",
    "roadmap current position",
)
text = replace_once(
    text,
    "**Universal Interior Viability / Equal Availability — SELECTED / BMDSFIX1-DIAG1 SUPPORTING RUNTIME ACTIVE / GAMEPLAY QUALIFICATION STILL OUTSTANDING.**",
    "**Universal Interior Viability / Equal Availability — SELECTED / BMDSFIX1-DIAG1PATH1 SUPPORTING RUNTIME ACTIVE / GAMEPLAY QUALIFICATION STILL OUTSTANDING.**",
    "roadmap selected scope",
)
text = replace_once(
    text,
    "Import exact active S1.42AK-BMDSFIX1-DIAG1 through the canonical repository-driven Gale v2.4 launcher. Run one bounded Black Mesa diagnostic to obtain `[BMDSFIX1-DIAG1] ARMED`, deterministic DeepSewersFlow selection, inherited `[BMDSFIX1] APPLIED ... ->1`, completed generation and normal landing without the prior persistent retry failure or a new severe target-attributable regression, then upload that exact `BepInEx/LogOutput.log` with the DIAG1 uploader. Do not alter profile/config/package/plugin bytes. This diagnostic never becomes a gameplay build and does not satisfy or waive the separate regular exact-byte BMDSFIX1 qualification.",
    "After this activation is integrated and exact-head validated, import exact active S1.42AK-BMDSFIX1-DIAG1PATH1 through the canonical repository-driven Gale v2.4 launcher. Run one bounded Black Mesa diagnostic to obtain inherited `[BMDSFIX1-DIAG1] ARMED`, deterministic DeepSewersFlow selection, inherited `[BMDSFIX1] APPLIED ... ->1`, completed generation and normal landing without the prior persistent retry failure or a new severe target-attributable regression, then upload that exact `BepInEx/LogOutput.log` with the DIAG1PATH1 uploader. Do not alter profile/config/package/plugin bytes. This diagnostic never becomes a gameplay build and does not satisfy or waive the separate regular exact-byte BMDSFIX1 qualification.",
    "roadmap next action",
)
text = text.replace("**Last-Validated:** 2026-09-24", "**Last-Validated:** 2026-09-25", 1)
path.write_text(text, encoding="utf-8")

activation_text = r"""# S1.42AK-BMDSFIX1-DIAG1PATH1 Runtime Activation

**Date:** 2026-09-25  
**Status:** PUBLISHED / INDEXED / ACTIVE DIAGNOSTIC RUNTIME TARGET / SUPPORTING TEST OUTSTANDING / NEVER ACCEPT  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted  
**Diagnostic:** S1.42AK-BMDSFIX1-DIAG1PATH1  
**Diagnostic profile:** `Profiles/LC V1 S1.42AK-D1P1.r2z`  
**Diagnostic profile identity:** `LC V1 S1.42AK-D1P1`  
**Diagnostic profile SHA-256:** `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`  
**Inherited DIAG1 selector DLL SHA-256:** `3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1`  
**Inherited BMDSFIX1 DLL SHA-256:** `f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92`

## Activation decision

The already reviewed, exact-byte-published and canonically profile-indexed `S1.42AK-BMDSFIX1-DIAG1PATH1` identity-only successor is authorized as the active **diagnostic-support-only** runtime/evidence target for one bounded deterministic Black Mesa x `DeepSewersFlow` run after this activation is integrated and exact-head validated.

Activation changes lifecycle/controller/evidence routing only. It does not rebuild or alter the PATH1 profile, the inherited DIAG1 selector DLL, the BMDSFIX1 gameplay DLL, any package, any config, or the exact BMDSFIX1 gameplay candidate. `BuildSpecs/current.json` remains disabled and pinned to exact BMDSFIX1.

S1.42AK-BMDSFIX1 remains `ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED`. DIAG1PATH1 is **NEVER ACCEPT** and cannot be promoted into gameplay lineage. A DIAG1PATH1 runtime cannot itself accept BMDSFIX1 and cannot waive or replace the regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification contract.

The long-name `S1.42AK-BMDSFIX1-DIAG1` is preloader-blocked, must not be rerun, and is retained only as the explicit one-hop diagnostic parent needed to prove PATH1 provenance.

## Canonical one-hop diagnostic chain

The Gale v2.4 one-hop diagnostic resolver is intentionally used:

`RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1PATH1`

-> `CURRENT_STATE.controllers.runtime_active_build`

-> `CURRENT_STATE.selected_scope.diagnostic_revision`

-> `BuildSpecs/S1.42AK-BMDSFIX1-DIAG1PATH1_BUILD_EVIDENCE/BUILD_RESULT.json`

-> `CURRENT_STATE.selected_scope.diagnostic_parent_revision = S1.42AK-BMDSFIX1-DIAG1`

-> `BuildSpecs/S1.42AK-BMDSFIX1-DIAG1_BUILD_EVIDENCE/BUILD_RESULT.json`

-> exact gameplay parent `Current/AUTO_BUILD_RESULT.json = S1.42AK-BMDSFIX1` / SHA-256 `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`.

The PATH1 archive remains 338 members and differs from the published long-name DIAG1 archive only in `export.r2x` profile identity metadata. DIAG1 selector, BMDSFIX1 and accepted normalizer DLL bytes remain unchanged.

## Supporting runtime contract

Run the exact PATH1 diagnostic on **Black Mesa**. The bounded supporting run should establish:

1. inherited `[BMDSFIX1-DIAG1] ARMED` with no `REFUSED TO ARM` marker;
2. inherited `[BMDSFIX1-DIAG1] SELECTED Black Mesa / DeepSewersFlow; normalized rarity=100; pool=<N>->1` with no `REFUSED selection` marker;
3. inherited `[BMDSFIX1] ARMED`;
4. target `[BMDSFIX1] APPLIED` with Black Mesa / `DeepSewersFlow` multiplier reduced to `1`;
5. completed dungeon generation;
6. normal landed gameplay without the prior persistent retry / `Entering the atmosphere` failure or a new severe target-attributable regression.

This is deterministic **supporting diagnostic evidence**, not regular exact-byte BMDSFIX1 qualification, because the runtime profile additionally contains the DIAG1 selector DLL and PATH1 profile identity.

The already-ingested Black Mesa x Substation BMDSFIX1 run remains the preserved non-target control. It need not be repeated solely for this diagnostic. Black Mesa x Greenhouse/BMGHDIAG remains a separate scope and is not part of this runtime gate.

## Exact Gale replacement/import one-liner

```powershell
$u='https://raw.githubusercontent.com/Tendas240/Lethal-Company-AI-Modding-Project/main/RuntimeTools/ReplaceActiveGaleProfileV24.ps1?cb='+[DateTime]::UtcNow.Ticks;iex (iwr -UseBasicParsing $u).Content
```

After this activation is integrated and exact-head validated, the launcher must resolve the one-hop diagnostic chain above, download exact `Profiles/LC V1 S1.42AK-D1P1.r2z`, verify SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, and preserve the existing fail-closed Gale/materialization checks.

## Exact build-specific runtime-log uploader

After the diagnostic gameplay run is complete, run this single PowerShell line:

```powershell
$ErrorActionPreference='Stop';$build='S1.42AK-BMDSFIX1-DIAG1PATH1';$log=Join-Path $env:APPDATA 'com.kesomannen.gale\lethal-company\profiles\LC V1 S1.42AK-D1P1\BepInEx\LogOutput.log';if(!(Test-Path -LiteralPath $log -PathType Leaf)){throw "Expected runtime log not found: $log"};$bytes=[IO.File]::ReadAllBytes($log);if($bytes.Length -le 0){throw 'Runtime log is empty'};$text=[Text.Encoding]::UTF8.GetString($bytes);if($text.IndexOf('[BMDSFIX1-DIAG1]',[StringComparison]::Ordinal) -lt 0){throw 'Refusing upload: exact local LogOutput.log contains no [BMDSFIX1-DIAG1] marker'};$localSha=([BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash($bytes))).Replace('-','').ToLowerInvariant();$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;$fallback=Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe';if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback};if(!$gh -and (Get-Command winget -ErrorAction SilentlyContinue)){winget install --id GitHub.cli -e --source winget --accept-source-agreements --accept-package-agreements | Out-Host;$gh=(Get-Command gh -ErrorAction SilentlyContinue).Source;if(!$gh -and (Test-Path -LiteralPath $fallback)){$gh=$fallback}};if(!$gh){throw 'GitHub CLI (gh) could not be resolved or bootstrapped'};& $gh auth status -h github.com *> $null;if($LASTEXITCODE -ne 0){& $gh auth login -h github.com -w;if($LASTEXITCODE -ne 0){throw 'GitHub authentication failed'}};$repo='Tendas240/Lethal-Company-AI-Modding-Project';$dest='RuntimeInbox/Current/LogOutput.log';$existing=$null;try{$existing=(& $gh api "repos/$repo/contents/$dest?ref=main" --jq '.sha' 2>$null)}catch{};$payload=@{message="Upload $build runtime log ($localSha)";content=[Convert]::ToBase64String($bytes);branch='main'};if($existing){$payload.sha=$existing};$json=$payload|ConvertTo-Json -Compress;$json|& $gh api --method PUT "repos/$repo/contents/$dest" --input -;if($LASTEXITCODE -ne 0){throw 'GitHub runtime-log upload failed'};Write-Host "Uploaded exact $build LogOutput.log SHA-256 $localSha" -ForegroundColor Green
```

The normal runtime-ingest workflow attributes uploaded evidence through `RuntimeInbox/ACTIVE_BUILD.txt`. If gameplay has already completed and only upload remains, do not repeat gameplay solely for evidence submission.

## Preserved boundaries

- accepted gameplay baseline remains S1.42AK;
- active gameplay candidate remains exact S1.42AK-BMDSFIX1 / not accepted;
- regular BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived;
- exact BMDSFIX1, DIAG1 selector and DIAG1PATH1 profile bytes are unchanged;
- package/config changes are zero;
- `BuildSpecs/current.json` remains disabled and guards exact BMDSFIX1;
- blocked long-name DIAG1 must not be rerun;
- Black Mesa x Greenhouse/BMGHDIAG remains separate;
- no universal interior override is authorized.

## Post-diagnostic boundary

After PATH1 evidence is ingested and decided, runtime routing must return to the exact BMDSFIX1 gameplay candidate before any regular BMDSFIX1 qualification run. DIAG1PATH1 evidence may support the diagnosis of the target pair but never substitutes for that exact-byte gameplay gate.
"""
(ROOT / ACTIVATION).write_text(activation_text, encoding="utf-8")

print("PASS: staged exact BMDSFIX1-DIAG1PATH1 diagnostic runtime activation; gameplay candidate and all artifact bytes preserved")
