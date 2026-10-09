#!/usr/bin/env python3
"""Stage-aware fail-closed TSDIAG1 ORIGINAL-BYTE publication/index boundary."""
from __future__ import annotations
import hashlib
import json
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
            p["toy_store_tsdiag1_built"] is False and
            p["toy_store_tsdiag1_runtime_armed"] is False and
            p["toy_store_runtime_test_authorized"] is False, "publication/activation boundary")
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
            (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text().strip() == "S1.42AK-BMDSFIX1",
            "live build/runtime controller drift")
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
    print("PASS: TSDIAG1 stage-aware original-byte publication integrity / no unauthorized index or runtime")


if __name__ == "__main__":
    validate()
