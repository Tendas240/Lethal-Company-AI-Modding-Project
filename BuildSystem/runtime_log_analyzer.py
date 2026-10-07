#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

LOG_RE = re.compile(
    r"^\[(?P<timestamp>\d{2}:\d{2}:\d{2}(?:\.\d+)?)\]\s+"
    r"\[(?P<level>[^:\]]+?)(?::(?P<source>[^\]]*))?\]\s*(?P<message>.*)$"
)

GUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
HEX_RE = re.compile(r"\b0x[0-9A-Fa-f]+\b|\b[0-9A-Fa-f]{16,}\b")
FLOAT_RE = re.compile(r"(?<![A-Za-z0-9_.-])-?\d+\.\d+(?![A-Za-z0-9_.-])")
INT_RE = re.compile(r"(?<![A-Za-z0-9_.-])-?\d+(?![A-Za-z0-9_.-])")
WS_RE = re.compile(r"[ \t]+")

TEXT_SUFFIXES = {".log", ".txt", ".out", ".err", ".json", ".jsonl", ".cfg", ".ini"}
CHAT_READABLE_LIMIT = 8 * 1024 * 1024
CHAT_CHUNK_TARGET = 256 * 1024
SIGNATURE_CHUNK_TARGET = 512 * 1024
SAMPLE_LIMIT = 5000

MARKERS = {
    "work_state_no_task": "Work state with no task assigned!",
    "leader_null_following": "Leader is null when following",
    "compatibility_fixes_error": "[Error  :S1.39 Compatibility Fixes]",
    "fatal_marker": "[Fatal",
    "exception": "Exception",
    "null_reference_exception": "NullReferenceException",
    "missing_reference_exception": "MissingReferenceException",
    "stack_overflow_exception": "StackOverflowException",
    "out_of_memory_exception": "OutOfMemoryException",
    "networkobjectreference_unspawned": "NetworkObjectReference can only be created from spawned NetworkObjects",
    "pikmin_notice_zone": "PikminNoticeZone.OnTriggerStay",
    "adding_enemy": "ADDING ENEMY",
    "enemy_isolation": "EnemyIsolation",
    "player_died": "A player died.",
    "jetpack_blast_death": "DeathPlayerJetpackBlast",
    "harmony_error": "Error while running static void",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_event_text(text: str) -> str:
    text = GUID_RE.sub("<guid>", text)
    text = HEX_RE.sub("<hex>", text)
    text = FLOAT_RE.sub("<float>", text)
    text = INT_RE.sub("<int>", text)
    text = WS_RE.sub(" ", text)
    return text.strip()


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return cleaned or "log"


def is_text_candidate(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name.lower().endswith("logoutput.log")


class SignatureStore:
    def __init__(self, db_path: Path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute(
            """
            CREATE TABLE signatures (
                signature_hash TEXT PRIMARY KEY,
                level TEXT NOT NULL,
                source TEXT NOT NULL,
                normalized TEXT NOT NULL,
                count INTEGER NOT NULL,
                first_line INTEGER NOT NULL,
                last_line INTEGER NOT NULL,
                first_timestamp TEXT,
                last_timestamp TEXT,
                first_sample TEXT NOT NULL,
                last_sample TEXT NOT NULL
            )
            """
        )
        self.pending = 0

    def add(
        self,
        signature_hash: str,
        level: str,
        source: str,
        normalized: str,
        start_line: int,
        end_line: int,
        timestamp: str | None,
        sample: str,
    ) -> None:
        sample = sample[:SAMPLE_LIMIT]
        self.conn.execute(
            """
            INSERT INTO signatures (
                signature_hash, level, source, normalized, count,
                first_line, last_line, first_timestamp, last_timestamp,
                first_sample, last_sample
            ) VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(signature_hash) DO UPDATE SET
                count = count + 1,
                last_line = excluded.last_line,
                last_timestamp = COALESCE(excluded.last_timestamp, signatures.last_timestamp),
                last_sample = excluded.last_sample
            """,
            (
                signature_hash,
                level,
                source,
                normalized,
                start_line,
                end_line,
                timestamp,
                timestamp,
                sample,
                sample,
            ),
        )
        self.pending += 1
        if self.pending >= 5000:
            self.conn.commit()
            self.pending = 0

    def finish(self) -> None:
        self.conn.commit()

    def unique_count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) FROM signatures").fetchone()
        return int(row[0])

    def iter_sorted(self):
        cur = self.conn.execute(
            """
            SELECT signature_hash, level, source, normalized, count,
                   first_line, last_line, first_timestamp, last_timestamp,
                   first_sample, last_sample
            FROM signatures
            ORDER BY count DESC, first_line ASC
            """
        )
        columns = [d[0] for d in cur.description]
        for row in cur:
            yield dict(zip(columns, row))

    def close(self) -> None:
        self.conn.close()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export_signature_chunks(store: SignatureStore, output_dir: Path) -> dict:
    sig_dir = output_dir / "signatures"
    sig_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    chunk_no = 1
    current_path = sig_dir / f"signatures_{chunk_no:04d}.jsonl"
    current = current_path.open("w", encoding="utf-8")
    current_bytes = 0
    current_records = 0
    total_records = 0
    first_rank = 1

    try:
        for record in store.iter_sorted():
            line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
            encoded_len = len(line.encode("utf-8"))
            if current_records and current_bytes + encoded_len > SIGNATURE_CHUNK_TARGET:
                current.close()
                manifest.append({
                    "file": str(current_path.relative_to(output_dir)),
                    "records": current_records,
                    "rank_start": first_rank,
                    "rank_end": total_records,
                    "size": current_path.stat().st_size,
                    "sha256": sha256_file(current_path),
                })
                chunk_no += 1
                first_rank = total_records + 1
                current_path = sig_dir / f"signatures_{chunk_no:04d}.jsonl"
                current = current_path.open("w", encoding="utf-8")
                current_bytes = 0
                current_records = 0
            current.write(line)
            current_bytes += encoded_len
            current_records += 1
            total_records += 1
    finally:
        if not current.closed:
            current.close()

    if current_records:
        manifest.append({
            "file": str(current_path.relative_to(output_dir)),
            "records": current_records,
            "rank_start": first_rank,
            "rank_end": total_records,
            "size": current_path.stat().st_size,
            "sha256": sha256_file(current_path),
        })
    elif current_path.exists():
        current_path.unlink()

    result = {"total_signatures": total_records, "chunks": manifest}
    write_json(output_dir / "SIGNATURES_MANIFEST.json", result)
    return result


def write_top_markdown(store: SignatureStore, output_dir: Path, limit: int = 100) -> None:
    lines = [
        "# Top normalized runtime signatures",
        "",
        "Every log event was processed. Dynamic GUID/hex/numeric values are normalized for aggregation.",
        "Full normalized signature coverage is stored in `signatures/` and indexed by `SIGNATURES_MANIFEST.json`.",
        "",
        "| Count | Level | Source | Lines | Normalized event |",
        "|---:|---|---|---:|---|",
    ]
    for i, rec in enumerate(store.iter_sorted()):
        if i >= limit:
            break
        normalized = str(rec["normalized"]).replace("|", "\\|").replace("\n", " ↩ ")
        if len(normalized) > 240:
            normalized = normalized[:237] + "..."
        source = str(rec["source"]).replace("|", "\\|")
        lines.append(
            f"| {rec['count']} | {rec['level']} | {source} | {rec['first_line']}-{rec['last_line']} | {normalized} |"
        )
    (output_dir / "TOP_SIGNATURES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def analyze_log(path: Path, output_dir: Path, *, create_chat_chunks: bool = True) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = output_dir / ".signatures.sqlite"
    store = SignatureStore(db_path)

    severity_counts = Counter()
    source_counts = Counter()
    marker_counts = Counter({k: 0 for k in MARKERS})
    marker_first = {}
    marker_last = {}
    timeline = defaultdict(Counter)
    parse = Counter()

    size = path.stat().st_size
    allow_chunks = create_chat_chunks and size <= CHAT_READABLE_LIMIT
    chunks_dir = output_dir / "chat_chunks"
    chunk_file = None
    chunk_path = None
    chunk_bytes = 0
    chunk_no = 0
    chunk_start_line = 1
    chunk_manifest = []

    current_event = None
    line_no = 0
    first_timestamp = None
    last_timestamp = None
    h = hashlib.sha256()

    def close_chunk(end_line: int) -> None:
        nonlocal chunk_file, chunk_path, chunk_bytes, chunk_start_line
        if chunk_file is None or chunk_path is None:
            return
        chunk_file.close()
        final_path = chunks_dir / f"chunk_{len(chunk_manifest)+1:04d}_L{chunk_start_line:08d}-L{end_line:08d}.log"
        chunk_path.rename(final_path)
        chunk_manifest.append({
            "file": str(final_path.relative_to(output_dir)),
            "line_start": chunk_start_line,
            "line_end": end_line,
            "size": final_path.stat().st_size,
            "sha256": sha256_file(final_path),
        })
        chunk_file = None
        chunk_path = None
        chunk_bytes = 0
        chunk_start_line = end_line + 1

    def add_marker(key: str, event) -> None:
        marker_counts[key] += 1
        if key not in marker_first:
            marker_first[key] = {
                "line": event["start_line"],
                "timestamp": event["timestamp"],
                "sample": event["raw"][:SAMPLE_LIMIT],
            }
        marker_last[key] = {
            "line": event["start_line"],
            "timestamp": event["timestamp"],
            "sample": event["raw"][:SAMPLE_LIMIT],
        }

    def flush_event(event) -> None:
        if event is None:
            return
        level = event["level"] or "UNPARSED"
        source = event["source"] or ""
        raw = event["raw"]
        normalized = normalize_event_text(event["normalized_input"])
        signature_hash = hashlib.sha256(
            f"{level}\0{source}\0{normalized}".encode("utf-8", errors="replace")
        ).hexdigest()
        store.add(
            signature_hash,
            level,
            source,
            normalized,
            event["start_line"],
            event["end_line"],
            event["timestamp"],
            raw,
        )
        severity_counts[level] += 1
        source_counts[source or "<none>"] += 1
        if event["timestamp"]:
            minute = event["timestamp"][:5]
            timeline[minute][level] += 1
        for key, needle in MARKERS.items():
            if needle in raw:
                add_marker(key, event)

    try:
        if allow_chunks:
            chunks_dir.mkdir(parents=True, exist_ok=True)

        with path.open("rb") as f:
            for raw_line in f:
                line_no += 1
                h.update(raw_line)
                if allow_chunks:
                    if chunk_file is None:
                        chunk_no += 1
                        chunk_path = chunks_dir / f".chunk_{chunk_no:04d}.tmp"
                        chunk_file = chunk_path.open("wb")
                    chunk_file.write(raw_line)
                    chunk_bytes += len(raw_line)
                    if chunk_bytes >= CHAT_CHUNK_TARGET:
                        close_chunk(line_no)

                line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                m = LOG_RE.match(line)
                if m:
                    flush_event(current_event)
                    timestamp = m.group("timestamp")
                    first_timestamp = first_timestamp or timestamp
                    last_timestamp = timestamp
                    current_event = {
                        "timestamp": timestamp,
                        "level": m.group("level").strip(),
                        "source": (m.group("source") or "").strip(),
                        "start_line": line_no,
                        "end_line": line_no,
                        "raw": line,
                        "normalized_input": m.group("message"),
                    }
                    parse["parsed_header_lines"] += 1
                else:
                    parse["continuation_or_unparsed_lines"] += 1
                    if current_event is None:
                        current_event = {
                            "timestamp": None,
                            "level": "UNPARSED",
                            "source": "",
                            "start_line": line_no,
                            "end_line": line_no,
                            "raw": line,
                            "normalized_input": line,
                        }
                    else:
                        current_event["end_line"] = line_no
                        current_event["raw"] += "\n" + line
                        current_event["normalized_input"] += "\n" + line
        flush_event(current_event)
        if allow_chunks and chunk_file is not None:
            close_chunk(line_no)
        store.finish()

        sig_manifest = export_signature_chunks(store, output_dir)
        write_top_markdown(store, output_dir)

        markers = {}
        for key, needle in MARKERS.items():
            markers[key] = {
                "needle": needle,
                "count": marker_counts[key],
                "first": marker_first.get(key),
                "last": marker_last.get(key),
            }
        write_json(output_dir / "MARKERS.json", markers)
        write_json(
            output_dir / "SOURCE_COUNTS.json",
            [{"source": k, "count": v} for k, v in source_counts.most_common()],
        )
        write_json(
            output_dir / "TIMELINE_BY_MINUTE.json",
            [
                {"minute": minute, "levels": dict(counts)}
                for minute, counts in sorted(timeline.items())
            ],
        )

        chunk_info = {
            "created": allow_chunks,
            "source_size_limit_bytes": CHAT_READABLE_LIMIT,
            "target_chunk_bytes": CHAT_CHUNK_TARGET,
            "chunks": chunk_manifest,
        }
        write_json(output_dir / "CHAT_CHUNKS_MANIFEST.json", chunk_info)

        stats = {
            "schema_version": 1,
            "source_file": path.name,
            "source_size_bytes": size,
            "source_sha256": h.hexdigest(),
            "line_count": line_no,
            "event_count": sum(severity_counts.values()),
            "unique_normalized_signatures": store.unique_count(),
            "first_timestamp": first_timestamp,
            "last_timestamp": last_timestamp,
            "severity_counts": dict(severity_counts),
            "parse_counts": dict(parse),
            "chat_readable_chunks_created": allow_chunks,
            "signature_chunk_count": len(sig_manifest["chunks"]),
        }
        write_json(output_dir / "STATS.json", stats)

        readme = f"""# Runtime log analysis\n\nSource: `{path.name}`  \nSHA-256: `{h.hexdigest()}`  \nSize: {size} bytes  \nLines: {line_no}  \nEvents: {stats['event_count']}  \nUnique normalized signatures: {stats['unique_normalized_signatures']}\n\nThis analysis is streaming and covers every source line. `signatures/` contains normalized event signatures with exact counts plus first/last samples and line positions. `MARKERS.json` contains project-critical regression markers. `TIMELINE_BY_MINUTE.json` and `SOURCE_COUNTS.json` provide distribution checks.\n\nChat-readable lossless raw chunks are {'present' if allow_chunks else 'not generated because the source exceeds the configured main-branch duplication threshold'}.\n"""
        (output_dir / "README.md").write_text(readme, encoding="utf-8")
        return stats
    finally:
        store.close()
        if db_path.exists():
            db_path.unlink()
        wal = Path(str(db_path) + "-wal")
        shm = Path(str(db_path) + "-shm")
        if wal.exists():
            wal.unlink()
        if shm.exists():
            shm.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Streaming Lethal Company runtime log analyzer")
    parser.add_argument("log", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--no-chat-chunks", action="store_true")
    args = parser.parse_args()
    if not args.log.is_file():
        raise SystemExit(f"Log file not found: {args.log}")
    stats = analyze_log(args.log, args.output, create_chat_chunks=not args.no_chat_chunks)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
