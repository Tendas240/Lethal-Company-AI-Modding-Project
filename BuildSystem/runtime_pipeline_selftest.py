#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import os
import importlib.util
import runtime_ingest as one_shot_ingest
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from runtime_log_analyzer import analyze_log

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*args: str) -> None:
    subprocess.run([PYTHON, *args], cwd=ROOT, check=True)


def write_sample_log(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "[12:00:00.000] [Info   :SelfTest] boot",
                "[12:00:01.000] [Info   :SelfTest] ADDING ENEMY #0. Flowerman;",
                "[12:00:02.000] [Warning:SelfTest] ordinary warning",
                "[12:00:03.000] [Error  :SelfTest] SyntheticException: expected self-test marker",
                "  at SelfTest.Frame()",
                "[12:00:04.000] [Info   :SelfTest] DeathPlayerJetpackBlast",
                "[12:00:05.000] [Info   :SelfTest] finished",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def assert_analyzer(tmp: Path, sample: Path) -> None:
    out = tmp / "analyzer"
    stats = analyze_log(sample, out, create_chat_chunks=True)
    assert stats["line_count"] == 7, stats
    markers = json.loads((out / "MARKERS.json").read_text(encoding="utf-8"))
    assert markers["adding_enemy"]["count"] == 1, markers["adding_enemy"]
    assert markers["jetpack_blast_death"]["count"] == 1, markers["jetpack_blast_death"]
    assert markers["work_state_no_task"]["count"] == 0
    assert markers["leader_null_following"]["count"] == 0
    chunk_manifest = json.loads((out / "CHAT_CHUNKS_MANIFEST.json").read_text(encoding="utf-8"))
    assert chunk_manifest["created"] is True
    assert chunk_manifest["chunks"], chunk_manifest
    assert (out / "SIGNATURES_MANIFEST.json").is_file()
    assert (out / "TOP_SIGNATURES.md").is_file()


def make_split_zip(inbox: Path, sample: Path) -> str:
    archive = inbox.parent / "LogOutput.log.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as z:
        z.write(sample, arcname="LogOutput.log")
    data = archive.read_bytes()
    # Deliberately tiny parts exercise the same reconstruction path as 20 MiB production parts.
    split_at = max(1, len(data) // 3)
    part_no = 1
    for offset in range(0, len(data), split_at):
        (inbox / f"LogOutput.log.zip.part{part_no:03d}").write_bytes(data[offset : offset + split_at])
        part_no += 1
    return archive.name


def assert_large_ingest_and_queries(tmp: Path, sample: Path) -> None:
    inbox = tmp / "large-inbox"
    inbox.mkdir()
    active = tmp / "ACTIVE_BUILD.txt"
    active.write_text("PIPELINE_SELFTEST\n", encoding="utf-8")
    source_name = make_split_zip(inbox, sample)

    output = tmp / "large-result"
    scratch = tmp / "large-scratch"
    run(
        "BuildSystem/runtime_large_ingest.py",
        "--inbox",
        str(inbox),
        "--active",
        str(active),
        "--output",
        str(output),
        "--scratch",
        str(scratch),
    )
    ready = (output / "RESULT_READY").read_text(encoding="utf-8").strip()
    evidence_rel = Path("RuntimeEvidence") / ready
    run_dir = output / evidence_rel
    index = json.loads((run_dir / "INDEX.json").read_text(encoding="utf-8"))
    assert index["build_id"] == "PIPELINE_SELFTEST"
    assert index["pipeline"] == "runtime_large_disposable_branch_v1"
    assert index["analysis"], index
    assert (scratch / "raw" / source_name).is_file()

    query_root = tmp / "query-output"
    request = {
        "enabled": True,
        "request_id": "pattern_test",
        "evidence_dir": str(evidence_rel).replace("\\", "/"),
        "source_file": source_name,
        "archive_member": "LogOutput.log",
        "mode": "pattern",
        "pattern": "ADDING ENEMY",
        "regex": False,
        "case_sensitive": True,
        "context_lines": 1,
        "max_matches": 10,
        "line_ranges": [],
    }
    request_path = tmp / "QUERY.json"
    request_path.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
    run("BuildSystem/runtime_log_query.py", str(request_path), str(scratch), str(query_root))
    pattern_result = query_root / evidence_rel / "analysis" / "queries" / "pattern_test.txt"
    pattern_text = pattern_result.read_text(encoding="utf-8")
    assert "ADDING ENEMY #0. Flowerman" in pattern_text, pattern_text
    assert "L00000002" in pattern_text, pattern_text

    request.update(
        {
            "request_id": "range_test",
            "mode": "line_ranges",
            "line_ranges": [{"start": 4, "end": 5}],
        }
    )
    request_path.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
    run("BuildSystem/runtime_log_query.py", str(request_path), str(scratch), str(query_root))
    range_result = query_root / evidence_rel / "analysis" / "queries" / "range_test.txt"
    range_text = range_result.read_text(encoding="utf-8")
    assert "L00000004" in range_text and "L00000005" in range_text, range_text
    assert "SyntheticException" in range_text, range_text


def assert_prepare_helper(tmp: Path, sample: Path) -> None:
    prep = tmp / "prepared"
    run("BuildSystem/prepare_large_runtime_log.py", str(sample), "--output", str(prep))
    manifest = json.loads((prep / "UPLOAD_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["original_name"] == sample.name
    assert manifest["original_size"] == sample.stat().st_size
    assert manifest["target_branch"] == "runtime-large"
    assert manifest["target_directory"] == "RuntimeInbox/Large"
    assert manifest["upload_files"], manifest



def assert_historical_one_shot(tmp: Path) -> None:
    """Synthetic-only tests; never access real user bytes or modify repository."""
    original_expected = one_shot_ingest.ONESHOT_EXPECTED
    original_cwd = Path.cwd()
    spec = importlib.util.spec_from_file_location(
        "one_shot_byte_validator", ROOT / "RepositoryTools/artifact_byte_integrity_validator.py"
    )
    validator = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(validator)

    def fixture(name: str):
        root = tmp / name
        (root / "RuntimeInbox/Current").mkdir(parents=True)
        (root / "Current").mkdir()
        (root / "BuildSpecs").mkdir()
        (root / "RuntimeEvidence").mkdir()
        data = (b"[12:00:01.000] [Info   :SelfTest] historical log line\n"
                b"[12:00:02.000] [Info   :SelfTest] second line\n")
        expected = dict(original_expected)
        expected.update(size=len(data), sha256=hashlib.sha256(data).hexdigest(), lines=2)
        state = {
            "accepted_baseline": {
                "build_id": expected["build_id"], "profile": expected["accepted_profile"],
                "sha256": expected["accepted_profile_sha256"], "status": "ACCEPTED_FULL_NORMAL_STACK"
            },
            "active_candidate": {
                "build_id": expected["runtime_active_build"],
                "status": "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED",
                "profile": "Profiles/SyntheticBMDS.r2z", "sha256": "a" * 64
            },
            "latest_built_artifact": {"build_id": expected["runtime_active_build"]},
            "controllers": {
                "runtime_active_build": expected["runtime_active_build"], "build_enabled": False,
                "build_id": "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS"
            }
        }
        buildspec = {
            "enabled": False, "build_id": "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
            "base_profile": "Profiles/SyntheticBMDS.r2z", "base_sha256": "a" * 64,
            "output_profile": "Profiles/DO_NOT_BUILD.r2z"
        }
        manifest = {
            "schema_version": 1, "status": "PENDING", "expected": expected, "receipt": None,
            "provenance": "PRIOR_CHAT_USER_ORIGINAL_LOG_PROFILE_BYTE_IDENTITY_P0_PARTIAL"
        }
        (root / "Current/CURRENT_STATE.json").write_text(json.dumps(state), encoding="utf-8")
        (root / "BuildSpecs/current.json").write_text(json.dumps(buildspec), encoding="utf-8")
        (root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json").write_text(
            json.dumps(manifest), encoding="utf-8")
        (root / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(
            expected["runtime_active_build"] + "\n", encoding="utf-8")
        (root / "RuntimeInbox/Current" / expected["inbox_filename"]).write_bytes(data)
        return root, expected, data

    def call(root: Path, expected: dict):
        os.chdir(root)
        one_shot_ingest.ONESHOT_EXPECTED = expected
        return one_shot_ingest.main()

    def refuse(root: Path, expected: dict):
        try:
            call(root, expected)
        except RuntimeError as exc:
            assert "ONESHOT_REFUSED" in str(exc), str(exc)
        else:
            raise AssertionError("One-shot negative test unexpectedly accepted input")
        assert not any((root / "RuntimeEvidence").rglob("INDEX.json")), "failed preflight wrote evidence"
        assert not any((root / "RuntimeEvidence").iterdir()), "failed preflight mutated evidence tree"

    def read_manifest(root: Path):
        return json.loads((root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json").read_text())

    try:
        root, expected, data = fixture("valid")
        errors = []
        validator.verify_one_shot_contract(root, errors, expected_override=expected)
        assert not errors, errors
        assert call(root, expected) == 0
        consumed = read_manifest(root)
        assert consumed["status"] == "CONSUMED"
        receipt = consumed["receipt"]
        assert receipt["build_id"] == "S1.42AK"
        assert receipt["runtime_active_build_at_ingest"] == "S1.42AK-BMDSFIX1"
        assert (root / receipt["raw_path"]).read_bytes() == data
        index = json.loads((root / receipt["evidence_index"]).read_text())
        assert index["files"][0]["name"] == "LogOutput.log"
        assert index["build_id"] == "S1.42AK"
        assert not (root / "RuntimeInbox/Current" / expected["inbox_filename"]).exists()
        errors = []
        validator.verify_one_shot_contract(root, errors, expected_override=expected)
        assert not errors, errors
        # The persisted contract blocks a second upload.
        (root / "RuntimeInbox/Current" / expected["inbox_filename"]).write_bytes(data)
        try:
            call(root, expected)
        except RuntimeError as exc:
            assert "ONESHOT_REFUSED" in str(exc)
        else:
            raise AssertionError("CONSUMED replay unexpectedly succeeded")
        # Even resetting PENDING is not enough: existing indexed SHA wins.
        reverted = dict(consumed, status="PENDING", receipt=None)
        (root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json").write_text(
            json.dumps(reverted), encoding="utf-8")
        try:
            call(root, expected)
        except RuntimeError as exc:
            assert "replay" in str(exc)
        else:
            raise AssertionError("INDEX replay guard failed")
        # Byte-integrity check must independently reject altered raw after consume.
        (root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json").write_text(
            json.dumps(consumed), encoding="utf-8")
        (root / receipt["raw_path"]).write_bytes(data + b"tamper")
        errors = []
        validator.verify_one_shot_contract(root, errors, expected_override=expected)
        assert any("raw original byte identity" in x for x in errors), errors

        root, expected, data = fixture("bad-hash")
        source = root / "RuntimeInbox/Current" / expected["inbox_filename"]
        changed = bytearray(data)
        changed[0] ^= 1  # Equal size, changed SHA-256: isolate the hash-only gate.
        assert len(changed) == expected["size"]
        assert hashlib.sha256(changed).hexdigest() != expected["sha256"]
        source.write_bytes(changed)
        contract_before = (root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json").read_bytes()
        refuse(root, expected)
        assert source.read_bytes() == changed, "failed preflight changed or consumed source"
        assert (root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json").read_bytes() == contract_before, "failed preflight changed contract"
        root, expected, data = fixture("wrong-size")
        other = dict(expected, size=len(data)+1)
        refuse(root, other)
        root, expected, data = fixture("wrong-controller")
        (root / "RuntimeInbox/ACTIVE_BUILD.txt").write_text("S1.42AK\n")
        refuse(root, expected)
        root, expected, data = fixture("wrong-profile")
        state_file = root / "Current/CURRENT_STATE.json"
        state = json.loads(state_file.read_text())
        state["accepted_baseline"]["sha256"] = "b" * 64
        state_file.write_text(json.dumps(state), encoding="utf-8")
        refuse(root, expected)
        root, expected, data = fixture("additional-inbox-file")
        (root / "RuntimeInbox/Current/other.txt").write_text("not allowed")
        refuse(root, expected)
        root, expected, data = fixture("bad-manifest")
        mpath = root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json"
        m = json.loads(mpath.read_text())
        m["expected"]["build_id"] = "S1.42AK-BMDSFIX1"
        mpath.write_text(json.dumps(m))
        refuse(root, expected)
        root, expected, data = fixture("already-consumed")
        mpath = root / "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json"
        m = json.loads(mpath.read_text())
        m["status"] = "CONSUMED"
        mpath.write_text(json.dumps(m))
        refuse(root, expected)
        root, expected, data = fixture("misnamed-original")
        (root / "RuntimeInbox/Current" / expected["inbox_filename"]).rename(
            root / "RuntimeInbox/Current/LogOutput.log")
        refuse(root, expected)
        root, expected, data = fixture("unrelated-normal-upload")
        (root / "RuntimeInbox/Current" / expected["inbox_filename"]).rename(
            root / "RuntimeInbox/Current/LogOutput.log")
        (root / "RuntimeInbox/Current/LogOutput.log").write_bytes(b"unrelated historical ordinary file\n")
        assert call(root, expected) == 0
        ids = list((root / "RuntimeEvidence/S1.42AK-BMDSFIX1").glob("*/INDEX.json"))
        assert len(ids) == 1
        assert json.loads(ids[0].read_text())["build_id"] == "S1.42AK-BMDSFIX1"
    finally:
        one_shot_ingest.ONESHOT_EXPECTED = original_expected
        os.chdir(original_cwd)

def main() -> int:
    with tempfile.TemporaryDirectory(prefix="runtime-pipeline-selftest-") as td:
        tmp = Path(td)
        sample = tmp / "LogOutput.log"
        write_sample_log(sample)
        assert_analyzer(tmp, sample)
        assert_large_ingest_and_queries(tmp, sample)
        assert_prepare_helper(tmp, sample)
        assert_historical_one_shot(tmp)
    print("runtime pipeline self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
