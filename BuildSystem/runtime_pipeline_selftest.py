#!/usr/bin/env python3
from __future__ import annotations

import json
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


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="runtime-pipeline-selftest-") as td:
        tmp = Path(td)
        sample = tmp / "LogOutput.log"
        write_sample_log(sample)
        assert_analyzer(tmp, sample)
        assert_large_ingest_and_queries(tmp, sample)
        assert_prepare_helper(tmp, sample)
    print("runtime pipeline self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
