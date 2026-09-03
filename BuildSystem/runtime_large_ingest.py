#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from runtime_log_analyzer import analyze_log, is_text_candidate

PART_RE = re.compile(r"^(?P<base>.+\.zip)\.part(?P<num>\d{3})$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def reconstruct_inputs(inbox: Path, temp: Path) -> tuple[list[Path], list[dict]]:
    files = sorted(p for p in inbox.iterdir() if p.is_file() and p.name not in {".gitkeep", "README.md", "UPLOAD_MANIFEST.json"})
    groups: dict[str, list[tuple[int, Path]]] = {}
    standalone: list[Path] = []
    input_records: list[dict] = []
    for p in files:
        m = PART_RE.match(p.name)
        if m:
            groups.setdefault(m.group("base"), []).append((int(m.group("num")), p))
        else:
            standalone.append(p)

    logical = []
    for p in standalone:
        target = temp / p.name
        shutil.copy2(p, target)
        logical.append(target)
        input_records.append({"name": p.name, "size": p.stat().st_size, "sha256": sha256(p), "kind": "standalone"})

    for base, parts in groups.items():
        parts.sort()
        expected = list(range(1, len(parts) + 1))
        actual = [n for n, _ in parts]
        if actual != expected:
            raise RuntimeError(f"Split archive {base} has non-contiguous parts: {actual}")
        target = temp / base
        h = hashlib.sha256()
        size = 0
        with target.open("wb") as dst:
            for n, p in parts:
                with p.open("rb") as src:
                    for chunk in iter(lambda: src.read(1024 * 1024), b""):
                        dst.write(chunk)
                        h.update(chunk)
                        size += len(chunk)
                input_records.append({"name": p.name, "size": p.stat().st_size, "sha256": sha256(p), "kind": "split_part", "logical_archive": base, "part": n})
        logical.append(target)
        input_records.append({"name": base, "size": size, "sha256": h.hexdigest(), "kind": "reconstructed_archive"})
    return logical, input_records


def safe_extract(archive: Path, target: Path) -> list[Path]:
    out = []
    with zipfile.ZipFile(archive, "r") as z:
        for info in z.infolist():
            rel = PurePosixPath(info.filename)
            if rel.is_absolute() or ".." in rel.parts:
                raise RuntimeError(f"Unsafe archive member: {info.filename}")
            if info.is_dir():
                continue
            dest = target / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst)
            out.append(dest)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze disposable very-large runtime logs without committing raw data to main")
    parser.add_argument("--inbox", type=Path, default=Path("RuntimeInbox/Large"))
    parser.add_argument("--active", type=Path, default=Path("RuntimeInbox/ACTIVE_BUILD.txt"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()

    build_id = args.active.read_text(encoding="utf-8").strip()
    if not build_id:
        raise RuntimeError("ACTIVE_BUILD.txt is empty")
    args.output.mkdir(parents=True, exist_ok=True)
    args.scratch.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="runtime-large-") as td:
        temp = Path(td)
        logical, input_records = reconstruct_inputs(args.inbox, temp)
        if not logical:
            print("No large runtime input found.")
            return 0

        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        run_dir = args.output / "RuntimeEvidence" / build_id / stamp
        analysis_root = run_dir / "analysis"
        analysis_root.mkdir(parents=True)
        scratch_raw = args.scratch / "raw"
        scratch_raw.mkdir(parents=True, exist_ok=True)

        index = {
            "schema_version": 1,
            "build_id": build_id,
            "ingested_utc": stamp,
            "pipeline": "runtime_large_disposable_branch_v1",
            "inputs": input_records,
            "logical_sources": [],
            "analysis": [],
            "raw_retention": {
                "main_branch": "never committed by this pipeline",
                "source_branch": "runtime-large force-reset after successful ingest",
                "workflow_artifact": "14 days",
                "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
                "artifact_name": f"runtime-large-raw-{os.environ.get('GITHUB_RUN_ID', 'local')}",
                "canonical_compact_analysis": "retained until superseded/obsolete per project evidence policy",
            },
        }

        for source in logical:
            shutil.copy2(source, scratch_raw / source.name)
            logical_record = {"name": source.name, "size": source.stat().st_size, "sha256": sha256(source), "members": []}
            candidates = []
            if source.suffix.lower() == ".zip":
                extract_root = temp / (source.stem + "_extracted")
                extract_root.mkdir()
                members = safe_extract(source, extract_root)
                for member in members:
                    logical_record["members"].append({
                        "path": str(member.relative_to(extract_root)),
                        "size": member.stat().st_size,
                        "sha256": sha256(member),
                        "text_analyzed": is_text_candidate(member),
                    })
                    if is_text_candidate(member):
                        candidates.append(member)
            elif is_text_candidate(source):
                candidates.append(source)

            for candidate in candidates:
                label = source.stem + "__" + candidate.name
                out = analysis_root / label
                stats = analyze_log(candidate, out, create_chat_chunks=False)
                index["analysis"].append({"source": candidate.name, "path": str(out.relative_to(run_dir)), "stats": stats})
            index["logical_sources"].append(logical_record)

        (run_dir / "INDEX.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (args.output / "RESULT_READY").write_text(f"{build_id}/{stamp}\n", encoding="utf-8")
        print(json.dumps(index, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
