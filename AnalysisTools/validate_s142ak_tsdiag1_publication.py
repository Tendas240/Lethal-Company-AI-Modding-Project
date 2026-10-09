#!/usr/bin/env python3
"""Stage-aware fail-closed TSDIAG1 ORIGINAL-BYTE publication/index boundary."""
from __future__ import annotations
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BUILD = "S1.42AK-TSDIAG1"
PROFILE = "Profiles/LC V1 S1.42AK-TS1.r2z"
PARENT = "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
SNAPSHOT = "ProfileSources/S1.42AK-TSDIAG1"
ADDED = "BepInEx/plugins/S142AKTSDiag1/S142AKTSDiag1.dll"
HASH_PROFILE = "d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e"
HASH_DLL = "fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201"
HASH_PARENT = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
HASH_ZIP = "010b84c1ffaea1d5cda2e14cdb9580c049da2cd1790e929491e44d13e2c4f39f"


def require(ok, explanation):
    if not ok:
        raise RuntimeError("TSDIAG1 publication-stage fail closed: " + explanation)


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(value).hexdigest()



def check_derived_lineage(metadata, parent):
    """The immutable derivative never impersonates the original 915-byte report."""
    source = metadata["original_review_evidence"]
    require(metadata["metadata_kind"] == "DERIVED_RUNTIME_BUILD_RESULT" and
            metadata["classification"] == "DIAGNOSTIC_ONLY_NEVER_ACCEPT" and
            metadata["build_id"] == BUILD and metadata["base_build_id"] == "S1.42AK-BMDSFIX1" and
            metadata["base_profile"] == PARENT and metadata["base_sha256"] == HASH_PARENT and
            metadata["output_profile"] == PROFILE and metadata["output_sha256"] == HASH_PROFILE and
            metadata["profile_sha256"] == HASH_PROFILE and metadata["dll_sha256"] == HASH_DLL and
            metadata["authoritative_review_artifact_id"] == 11615262607 and
            metadata["authoritative_review_artifact_zip_sha256"] == HASH_ZIP and
            metadata["published"] is True and metadata["indexed"] is True and
            metadata["runtime_armed"] is False and metadata["runtime_proof"] is False,
            "DERIVED runtime metadata must retain exact immutable original lineage")
    require(source["artifact_id"] == 11615262607 and
            source["producer_head"] == "24105017a0d98ccc05b878c809f84f93f4e87e37" and
            source["outer_zip_sha256"] == HASH_ZIP and
            source["original_build_result_member"] == "Evidence/BUILD_RESULT.json" and
            source["original_build_result_size_bytes"] == 915 and
            source["original_build_result_sha256"] ==
            "9a34b7f1d7b5dd910913e1a39ed033de98f76d8542065f244e64e6f7f400235a" and
            source["original_build_result_status"] ==
            "COMPILE_INPUT_PRESENT_ARCHIVE_AWAITS_INDEPENDENT_VALIDATION" and
            source["original_stage_published"] is False and
            source["original_stage_indexed"] is False and
            source["original_stage_runtime_armed"] is False,
            "original 915-byte prevalidation report was altered/relabeled")
    require(parent["build_id"] == "S1.42AK-BMDSFIX1" and
            parent["output_profile"] == PARENT and parent["output_sha256"] == HASH_PARENT,
            "independent AUTO-parent routing and hash mismatch")


def check_lifecycle_route(state, p, metadata, parent, active, activation_text=None):
    check_derived_lineage(metadata, parent)
    controls = state["controllers"]
    demand_build = read_json("BuildSpecs/current.json")
    require(demand_build["enabled"] is False and
            demand_build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
            "build controller must stay disabled/IDLE")
    runtime_flags = (
        p["toy_store_tsdiag1_runtime_armed"],
        p["toy_store_runtime_test_authorized"],
        p["toy_store_tsdiag1_runtime_activation_checkpoint_executed"],
    )
    new_stage = active == BUILD or controls["runtime_active_build"] == BUILD or any(runtime_flags)
    if not new_stage:
        require(runtime_flags == (False, False, False) and
                active == controls["runtime_active_build"] == "S1.42AK-BMDSFIX1" and
                state["selected_scope"]["diagnostic_revision"]["build_id"] == "S1.42AK-SCDIAG1" and
                state["selected_scope"]["diagnostic_revision"]["runtime_armed"] is False,
                "inactive-original publication stage altered or mixed with active diagnostic")
        return "INACTIVE_ORIGINAL_PUBLICATION_INDEXED"

    require(runtime_flags == (True, True, True),
            "no partially armed/test-authorized diagnostic lifecycle")
    require(p["toy_store_tsdiag1_runtime_activation_authorization_pr"] == 405 and
            p["toy_store_tsdiag1_runtime_activation_authorization_main_commit"] ==
            "46096717993039e3b7b2b7cb8579fc4bcec9151c" and
            p["toy_store_tsdiag1_runtime_activation_authorization_main_knowledge_architecture_run"] ==
            37960835253 and p["toy_store_tsdiag1_profile_indexed"] is True,
            "independently integrated runtime-activation decision/index missing")
    diag = state["selected_scope"]["diagnostic_revision"]
    require(active == controls["runtime_active_build"] == diag["build_id"] == BUILD and
            diag["status"] == "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED" and
            diag["classification"] == "DIAGNOSTIC_ONLY_NEVER_ACCEPT" and
            diag["runtime_armed"] is True and
            diag["base_build_id"] == "S1.42AK-BMDSFIX1" and
            diag["base_profile"] == PARENT and diag["base_sha256"] == HASH_PARENT and
            diag["profile"] == PROFILE and diag["sha256"] == HASH_PROFILE and
            diag["build_result"] == "BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json",
            "diagnostic/runtime controller or original-byte routing inconsistent")
    record = p.get("toy_store_tsdiag1_runtime_activation")
    require(isinstance(record, str) and
            re.fullmatch(r"Current/[0-9]+_S1\.42AK_TSDIAG1_RUNTIME_ACTIVATION\.md", record) is not None,
            "distinct versioned activation record is missing")
    if activation_text is None:
        activation_path = ROOT / record
        require(activation_path.is_file(), "activation record not actually committed")
        activation_text = activation_path.read_text(encoding="utf-8")
    for token in (BUILD, PROFILE, HASH_PROFILE, HASH_DLL, HASH_PARENT,
                  "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
                  "DIAGNOSTIC_ONLY_NEVER_ACCEPT"):
        require(token in activation_text, "explicit activation record lacks exact token: " + token)
    return "EXACT_ORIGINAL_DIAGNOSTIC_RUNTIME_AUTHORIZED"


def route_self_test(state, metadata, parent):
    """Pure synthetic mutations: NEVER edit current runtime controllers on disk."""
    p = state["selected_scope"]["phase_c"]
    active = "S1.42AK-BMDSFIX1"
    proof = read_json("BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json")
    assert check_lifecycle_route(state, p, metadata, parent, active) == "INACTIVE_ORIGINAL_PUBLICATION_INDEXED"
    def rejects(s, m, a, note, text=None):
        try:
            check_lifecycle_route(s, s["selected_scope"]["phase_c"], m, parent, a, text)
        except (RuntimeError, KeyError, TypeError):
            return
        raise AssertionError("negative mutation unexpectedly accepted: " + note)
    for key in ("toy_store_tsdiag1_runtime_armed", "toy_store_runtime_test_authorized",
                "toy_store_tsdiag1_runtime_activation_checkpoint_executed"):
        bad = copy.deepcopy(state)
        bad["selected_scope"]["phase_c"][key] = True
        rejects(bad, metadata, active, "unauthorized " + key)
    for key in ("metadata_kind", "base_sha256", "output_sha256", "dll_sha256",
                "authoritative_review_artifact_id", "published", "indexed", "runtime_armed"):
        bad = copy.deepcopy(metadata)
        bad[key] = "MUTATED"
        rejects(state, bad, active, "DERIVED " + key)
    for key in ("original_build_result_size_bytes", "original_build_result_sha256",
                "original_build_result_status", "producer_head", "original_stage_runtime_armed"):
        bad = copy.deepcopy(metadata)
        bad["original_review_evidence"][key] = "MUTATED"
        rejects(state, bad, active, "original prevalidation " + key)
    bad = copy.deepcopy(state)
    bad["controllers"]["runtime_active_build"] = BUILD
    rejects(bad, metadata, active, "mixed controller")
    bad = copy.deepcopy(state)
    bad["selected_scope"]["diagnostic_revision"] = {"build_id": BUILD}
    rejects(bad, metadata, active, "wrong dormant diagnostic")
    # Fully synthetic consistent activation branch, with exact published bytes.
    armed = copy.deepcopy(state)
    ap = armed["selected_scope"]["phase_c"]
    ap["toy_store_tsdiag1_runtime_armed"] = True
    ap["toy_store_runtime_test_authorized"] = True
    ap["toy_store_tsdiag1_runtime_activation_checkpoint_executed"] = True
    ap["toy_store_tsdiag1_runtime_activation"] = "Current/999_S1.42AK_TSDIAG1_RUNTIME_ACTIVATION.md"
    armed["controllers"]["runtime_active_build"] = BUILD
    armed["selected_scope"]["diagnostic_revision"] = {
        "build_id": BUILD, "status": "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
        "classification": "DIAGNOSTIC_ONLY_NEVER_ACCEPT", "runtime_armed": True,
        "base_build_id": "S1.42AK-BMDSFIX1", "base_profile": PARENT,
        "base_sha256": HASH_PARENT, "profile": PROFILE, "sha256": HASH_PROFILE,
        "build_result": "BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json",
    }
    doc = " ".join((BUILD, PROFILE, HASH_PROFILE, HASH_DLL, HASH_PARENT,
                    "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
                    "DIAGNOSTIC_ONLY_NEVER_ACCEPT"))
    assert check_lifecycle_route(armed, ap, metadata, parent, BUILD, doc) == "EXACT_ORIGINAL_DIAGNOSTIC_RUNTIME_AUTHORIZED"
    for mutate in ("wrong status", "mixed controller", "missing record", "wrong class",
                   "wrong parent", "unauthorized test"):
        bad = copy.deepcopy(armed)
        bp = bad["selected_scope"]["phase_c"]
        d = bad["selected_scope"]["diagnostic_revision"]
        if mutate == "wrong status":
            d["status"] = "ACCEPTED"
        elif mutate == "mixed controller":
            bad["controllers"]["runtime_active_build"] = "S1.42AK-BMDSFIX1"
        elif mutate == "missing record":
            bp["toy_store_tsdiag1_runtime_activation"] = "Current/UNKNOWN.md"
        elif mutate == "wrong class":
            d["classification"] = "ACCEPTED"
        elif mutate == "wrong parent":
            d["base_sha256"] = "0" * 64
        else:
            bp["toy_store_runtime_test_authorized"] = False
        rejects(bad, metadata, BUILD, "active " + mutate, doc)
    print("PASS: 24 synthetic negative mutations; inactive and exactly coherent activation-stage fixtures")


def validate():
    state = read_json("Current/CURRENT_STATE.json")
    p = state["selected_scope"]["phase_c"]
    proof = read_json("BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json")
    require(state["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline changed")
    require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1" and
            state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED" and
            state["runtime_test_outstanding"] is True, "unwaived BMDSFIX1 passive gate")
    require(p["residual_no_trusted_actual_generation_proof"] == 22 and
            p["residual_viable_equal_100"] == 10 and
            p["residual_owner_hard_block"] == 12, "residual changed")
    require(p["toy_store_tsdiag1_publication_authorized"] is True and
            p["toy_store_tsdiag1_publication_completed"] is True and
            p["toy_store_tsdiag1_built"] is False, "original publication boundary")
    require(p["toy_store_tsdiag1_publication_profile"] == PROFILE and
            p["toy_store_tsdiag1_publication_profile_sha256"] == HASH_PROFILE and
            p["toy_store_tsdiag1_publication_pr"] == 399 and
            p["toy_store_tsdiag1_publication_final_pr_head"] == "2c0eb2aa5b1a71fca4f16d302ad2ca6d5ee52223" and
            p["toy_store_tsdiag1_publication_main_integration_commit"] ==
            "f2f3f5e3dd330befeef8187640a40157c6470b5c" and
            p["toy_store_tsdiag1_publication_main_knowledge_architecture_run"] == 37943625924 and
            p["toy_store_tsdiag1_publication_profile_index_fail_closed_run"] == 37943625888,
            "exact original publication integration provenance")
    require(p["toy_store_tsdiag1_publication_original_artifact_id"] == 11615262607 and
            p["toy_store_tsdiag1_publication_original_artifact_zip_sha256"] == HASH_ZIP and
            proof["artifact_id"] == 11615262607 and
            proof["build_head"] == "24105017a0d98ccc05b878c809f84f93f4e87e37" and
            proof["zip_sha256"] == HASH_ZIP and
            proof["profile_sha256"] == HASH_PROFILE and
            proof["dll_sha256"] == HASH_DLL and
            proof["parent_sha256"] == HASH_PARENT and
            proof["classification"] == "DIAGNOSTIC_ONLY_NEVER_ACCEPT",
            "frozen independent review evidence")
    build = read_json("BuildSpecs/current.json")
    require(build["enabled"] is False and
            build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS" and
            state["controllers"]["build_enabled"] is False,
            "live build controller drift")
    derived = read_json("BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json")
    parent_auto = read_json("Current/AUTO_BUILD_RESULT.json")
    active = (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()
    route = check_lifecycle_route(state, p, derived, parent_auto, active)
    if "--self-test" in sys.argv[1:]:
        route_self_test(state, derived, parent_auto)
    require(not (ROOT / ".github/workflows/one-shot-tsdiag1-publication.yml").exists(),
            "one-shot transport workflow must not persist")
    profile_data = (ROOT / PROFILE).read_bytes()
    parent_data = (ROOT / PARENT).read_bytes()
    require(digest(profile_data) == HASH_PROFILE, "published profile bytes differ from frozen original")
    require(digest(parent_data) == HASH_PARENT, "parent archive changed")
    with zipfile.ZipFile(ROOT / PROFILE) as z, zipfile.ZipFile(ROOT / PARENT) as par:
        require(z.testzip() is None and par.testzip() is None, "ZIP CRC failure")
        names, inherited = z.namelist(), par.namelist()
        require(len(names) == 338 and len(set(names)) == 338 and
                len(inherited) == 337 and len(set(inherited)) == 337 and
                names[:337] == inherited and names[337:] == [ADDED],
                "expected 337-to-338 member identity/order")
        for path in inherited:
            if path != "export.r2x":
                require(z.read(path) == par.read(path), "unexpected inherited member drift: " + path)
        original = par.read("export.r2x")
        old = b"profileName: LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix"
        new = b"profileName: LC V1 S1.42AK-TS1"
        require(original.count(old) == 1 and
                z.read("export.r2x") == original.replace(old, new, 1),
                "only export profile-name change allowed")
        require(digest(z.read(ADDED)) == HASH_DLL, "DLL original SHA mismatch")
        require(digest(z.read("BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll")) ==
                "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92",
                "BMDSFIX1 inherited DLL mismatch")
        require(digest(z.read("BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll")) ==
                "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
                "normalizer inherited DLL mismatch")
        rows = read_json(SNAPSHOT + "/FILE_INDEX.json")
        require(len(rows) == 338 and sum(bool(row["text_snapshot"]) for row in rows) == 331,
                "deterministic static snapshot count")
        for i, (member, rec) in enumerate(zip(names, rows)):
            require(rec["index"] == i and rec["path"] == member and
                    rec["sha256"] == digest(z.read(member)) and
                    rec["size"] == len(z.read(member)),
                    "deterministic static snapshot member drift: " + member)

    registry = read_json("Profiles/EXPECTED_HASHES.json")
    canonical = registry.get(PROFILE)
    if canonical is not None:
        require(canonical.get("build_id") == BUILD and
                canonical.get("sha256") == HASH_PROFILE,
                "future canonical mapping cannot change frozen identity")
    result_file = ROOT / SNAPSHOT / "PROFILE_INDEX_RESULT.json"
    if p["toy_store_tsdiag1_profile_indexed"]:
        require(canonical is not None and result_file.exists(),
                "indexed state requires independently produced canonical mapping/result")
        result = read_json(SNAPSHOT + "/PROFILE_INDEX_RESULT.json")
        require(result.get("sha256") == HASH_PROFILE, "canonical index SHA mismatch")
    else:
        require(not result_file.exists(), "unindexed stage must not claim canonical index result")
    print("PASS: TSDIAG1 original-byte publication/index integrity and fail-closed " + route)


if __name__ == "__main__":
    validate()
