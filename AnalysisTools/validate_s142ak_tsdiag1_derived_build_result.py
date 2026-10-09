#!/usr/bin/env python3
"""Fail-closed ORIGINAL-ANCHORED TSDIAG1 runtime metadata checks; no build actions."""
import argparse
import copy
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
META = "BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json"
REVIEW = "BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json"
PUB = "BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
INDEX = "ProfileSources/S1.42AK-TSDIAG1/PROFILE_INDEX_RESULT.json"
FILES = "ProfileSources/S1.42AK-TSDIAG1/FILE_INDEX.json"
PARENT = "Current/AUTO_BUILD_RESULT.json"
HASHES = "Profiles/EXPECTED_HASHES.json"
PREFLIGHT = "Current/376_S1.42AK_TSDIAG1_FROZEN_ORIGINAL_PROVENANCE_AND_CI_STAGE_PREFLIGHT.md"
STATE = "Current/CURRENT_STATE.json"
ACTIVE = "RuntimeInbox/ACTIVE_BUILD.txt"
ORIGINAL_STATUS = "COMPILE_INPUT_PRESENT_ARCHIVE_AWAITS_INDEPENDENT_VALIDATION"
ORIGINAL_SHA = "9a34b7f1d7b5dd910913e1a39ed033de98f76d8542065f244e64e6f7f400235a"
PROFILE_SHA = "d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e"
DLL_SHA = "fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201"
ZIP_SHA = "010b84c1ffaea1d5cda2e14cdb9580c049da2cd1790e929491e44d13e2c4f39f"
PARENT_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def demand(condition, reason):
    if not condition:
        raise ValueError(reason)

def equal(actual, expected, label):
    demand(type(actual) is type(expected) and actual == expected, f"{label}: unexpected identity/value")

def check(d, r, ix, hashes, auto, entries, state, pub, preflight, active, profile_digest):
    equal(d["schema_version"], 1, "schema_version")
    equal(d["metadata_kind"], "DERIVED_RUNTIME_BUILD_RESULT", "metadata_kind")
    equal(d["status"], "DERIVED_RUNTIME_METADATA_ORIGINAL_FROZEN_REVIEW_PUBLISHED_INDEXED_NO_REBUILD", "derived status")
    equal(d["classification"], "DIAGNOSTIC_ONLY_NEVER_ACCEPT", "classification")
    demand("DERIVED" in d["provenance"] and "unchanged" in d["provenance"] and "No recompilation" in d["provenance"], "explicit derivation/no-rebuild statement")
    equal(d["build_id"], r["build_id"], "build_id")
    equal(r["build_id"], "S1.42AK-TSDIAG1", "immutable review build ID")
    equal(r["status"], "PASS_INACTIVE_REVIEW_BUILD_INDEPENDENTLY_REHASHED", "independent review status")
    equal(r["classification"], d["classification"], "review classification")
    demand(r["independent_artifact_rehash_match"] is True and r["review_zip_crc_pass"] is True and r["unique_members"] is True, "original review validation")
    for field in ("source_main_commit", "build_head", "parent_profile", "parent_sha256",
                  "review_profile", "profile_sha256", "dll_member", "dll_sha256",
                  "parent_members", "review_members", "profile_name"):
        equal(d[field], r[field], "review " + field)
    equal(r["build_head"], "24105017a0d98ccc05b878c809f84f93f4e87e37", "producer head")
    equal(r["source_main_commit"], "4056ccdfd2ec42b9b3378a438d4f996f8d78e828", "source main")
    equal(r["artifact_id"], 11615262607, "sole original artifact ID")
    equal(r["build_workflow_run"], 37929246619, "sole original run")
    equal(r["build_workflow_run_number"], 2, "sole original run number")
    equal(r["zip_sha256"], ZIP_SHA, "original artifact ZIP digest")
    equal(r["parent_sha256"], PARENT_SHA, "original parent SHA")
    equal(r["profile_sha256"], PROFILE_SHA, "review profile SHA")
    equal(r["dll_sha256"], DLL_SHA, "review DLL SHA")
    equal(r["review_members"], 338, "review members")
    o = d["original_review_evidence"]
    expected_original = {
        "artifact_id": r["artifact_id"], "producer_run_id": r["build_workflow_run"],
        "producer_run_number": r["build_workflow_run_number"], "producer_head": r["build_head"],
        "outer_zip_sha256": r["zip_sha256"], "original_build_result_member": "Evidence/BUILD_RESULT.json",
        "original_build_result_size_bytes": 915, "original_build_result_sha256": ORIGINAL_SHA,
        "original_build_result_status": ORIGINAL_STATUS,
        "independent_review_status": r["status"],
        "original_stage_published": False, "original_stage_indexed": False,
        "original_stage_runtime_armed": False
    }
    equal(o, expected_original, "complete original prevalidation stage attestation")
    demand(ORIGINAL_SHA in preflight and ORIGINAL_STATUS in preflight and
           ZIP_SHA in preflight and "915 bytes" in preflight, "independent raw-original provenance missing")
    equal(d["authoritative_review_artifact_id"], r["artifact_id"], "artifact alias")
    equal(d["authoritative_review_artifact_zip_sha256"], r["zip_sha256"], "artifact ZIP alias")
    equal(d["base_build_id"], auto["build_id"], "Gale direct parent build")
    equal(auto["build_id"], "S1.42AK-BMDSFIX1", "immutable parent build")
    equal(auto["output_sha256"], PARENT_SHA, "parent AUTO_BUILD_RESULT output SHA")
    equal(auto["zip_members"], 337, "parent member count")
    for field, expected in (
        ("base_profile", auto["output_profile"]), ("base_sha256", auto["output_sha256"]),
        ("output_profile", r["review_profile"]), ("output_sha256", r["profile_sha256"]),
    ):
        equal(d[field], expected, "Gale " + field)
    equal(d["parent_profile"], d["base_profile"], "original parent/derived base path")
    equal(d["parent_sha256"], d["base_sha256"], "original parent/derived base sha")
    equal(d["review_profile"], d["output_profile"], "original review/derived output path")
    equal(d["profile_sha256"], d["output_sha256"], "original review/derived output sha")
    equal(d["profile_name"], ix["profile_name"], "published profile name")
    equal(ix["build_id"], d["build_id"], "index build ID")
    equal(ix["profile_path"], d["output_profile"], "index path")
    equal(ix["sha256"], d["output_sha256"], "index SHA")
    equal(ix["zip_members"], d["zip_members"], "index member count")
    equal(ix["build_id_resolution"], "EXPECTED_HASHES", "index resolver")
    equal(hashes[d["output_profile"]]["build_id"], d["build_id"], "expected hash build")
    equal(hashes[d["output_profile"]]["sha256"], d["output_sha256"], "expected hash SHA")
    equal(profile_digest, PROFILE_SHA, "actual repository profile digest")
    demand(PROFILE_SHA in pub and ZIP_SHA in pub and DLL_SHA in pub
           and PARENT_SHA in pub, "exact-byte publication attestation")
    equal(d["snapshot_dir"], ix["snapshot_dir"], "canonical snapshot")
    equal(d["snapshot"], ix["snapshot"], "canonical snapshot counts")
    equal(d["zip_members"], 338, "archive member count")
    equal(len(entries), 338, "canonical file entries")
    equal(entries[-1]["path"], d["dll_member"], "last DLL path")
    equal(entries[-1]["sha256"], d["dll_sha256"], "original DLL from canonical index")
    equal(entries[-1]["size"], 18944, "DLL size")
    equal(d["changed_existing_members"], ["export.r2x"], "changed members")
    equal(d["added_members"], [d["dll_member"]], "sole added DLL")
    equal(d["removed_members"], [], "no removals")
    equal(d["package_changes"], 0, "package changes")
    equal(d["config_changes"], 0, "config changes")
    for field, expected in (("published", True), ("indexed", True),
                            ("runtime_armed", False), ("runtime_proof", False)):
        equal(d[field], expected, field)
    equal(d["lineage_sources"], {
        "original_provenance": PREFLIGHT, "review_checkpoint": REVIEW,
        "exact_byte_publication": PUB, "canonical_hashes": HASHES,
        "canonical_index": INDEX, "canonical_file_index": FILES,
        "parent_auto_build_result": PARENT
    }, "fixed lineage source paths")
    equal(state["controllers"]["runtime_active_build"], "S1.42AK-BMDSFIX1", "current controller")
    equal(active, "S1.42AK-BMDSFIX1", "ACTIVE_BUILD.txt")
    equal(state["selected_scope"]["phase_c"]["toy_store_tsdiag1_runtime_armed"], False, "runtime remains inactive")
    equal(state["selected_scope"]["phase_c"]["toy_store_runtime_test_authorized"], False, "test not authorized")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    d, r, ix, hashes, auto, entries, state = map(load, (META, REVIEW, INDEX, HASHES, PARENT, FILES, STATE))
    pub = (ROOT / PUB).read_text(encoding="utf-8")
    preflight = (ROOT / PREFLIGHT).read_text(encoding="utf-8")
    active = (ROOT / ACTIVE).read_text(encoding="utf-8").strip()
    digest = hashlib.sha256((ROOT / d["output_profile"]).read_bytes()).hexdigest()
    base = (d, r, ix, hashes, auto, entries, state, pub, preflight, active, digest)
    check(*base)
    failures = 0
    if args.self_test:
        cases = [
            (0, ("metadata_kind",), "ORIGINAL"),
            (0, ("status",), ORIGINAL_STATUS),
            (0, ("original_review_evidence", "artifact_id"), 11615262608),
            (0, ("original_review_evidence", "original_build_result_sha256"), "0"*64),
            (0, ("original_review_evidence", "original_build_result_status"), "PASS"),
            (0, ("original_review_evidence", "original_stage_published"), True),
            (0, ("base_profile",), "Profiles/other.r2z"),
            (0, ("base_sha256",), "0"*64),
            (0, ("output_sha256",), "0"*64),
            (0, ("dll_sha256",), "0"*64),
            (0, ("authoritative_review_artifact_id",), 0),
            (0, ("published",), False),
            (0, ("indexed",), False),
            (0, ("runtime_armed",), True),
            (1, ("artifact_id",), 9),
            (2, ("sha256",), "0"*64),
            (3, (d["output_profile"], "sha256"), "0"*64),
            (4, ("output_sha256",), "0"*64),
            (5, ("__LAST_DLL__", "sha256"), "0"*64),
            (6, ("controllers", "runtime_active_build"), "S1.42AK-TSDIAG1"),
        ]
        for objindex, path, value in cases:
            payload = [copy.deepcopy(v) for v in base]
            cur = payload[objindex]
            if path[0] == "__LAST_DLL__":
                cur[-1][path[1]] = value
            else:
                for p in path[:-1]:
                    cur = cur[p]
                cur[path[-1]] = value
            try:
                check(*payload)
            except (ValueError, KeyError, TypeError):
                failures += 1
            else:
                raise AssertionError(f"Negative provenance mutation was accepted: {path}")
        assert failures == len(cases)
    print(json.dumps({"status": "DERIVED_TSDIAG1_ORIGINAL_LINEAGE_PASS",
                      "original_prevalidation_not_relabelled": True,
                      "negative_mutations_rejected": failures, "runtime_armed": False,
                      "build_reconstructed": False}, indent=2))

if __name__ == "__main__":
    main()
