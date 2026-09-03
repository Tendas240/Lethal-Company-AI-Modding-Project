#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import deque
from pathlib import Path, PurePosixPath


def safe_member(name: str) -> PurePosixPath:
    rel = PurePosixPath(name)
    if rel.is_absolute() or ".." in rel.parts:
        raise RuntimeError(f"Unsafe archive member: {name}")
    return rel


def choose_source(root: Path, source_file: str | None) -> Path:
    files = sorted(p for p in root.rglob("*") if p.is_file())
    if source_file:
        matches = [p for p in files if p.name == source_file or str(p.relative_to(root)) == source_file]
        if len(matches) != 1:
            raise RuntimeError(f"Expected exactly one source_file match for {source_file!r}, got {len(matches)}")
        return matches[0]
    candidates = [p for p in files if p.suffix.lower() in {".zip", ".log", ".txt"}]
    if len(candidates) != 1:
        raise RuntimeError("source_file is required when artifact contains multiple candidate files")
    return candidates[0]


def iter_text_lines(source: Path, member: str | None):
    if source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source, "r") as z:
            members = [i for i in z.infolist() if not i.is_dir()]
            if member:
                info = z.getinfo(str(safe_member(member)))
            else:
                text = [i for i in members if Path(i.filename).suffix.lower() in {".log", ".txt", ".out", ".err"}]
                if len(text) != 1:
                    raise RuntimeError("archive_member is required when ZIP does not contain exactly one text log")
                info = text[0]
            with z.open(info, "r") as f:
                for n, raw in enumerate(f, 1):
                    yield n, raw.decode("utf-8", errors="replace").rstrip("\r\n"), info.filename
    else:
        with source.open("rb") as f:
            for n, raw in enumerate(f, 1):
                yield n, raw.decode("utf-8", errors="replace").rstrip("\r\n"), source.name


def line_ranges_query(source: Path, member: str | None, ranges: list[dict]) -> tuple[list[str], dict]:
    normalized = []
    for r in ranges:
        start = int(r["start"])
        end = int(r["end"])
        if start < 1 or end < start:
            raise RuntimeError(f"Invalid line range: {r}")
        normalized.append((start, end))
    normalized.sort()
    out = []
    total_lines = 0
    selected = 0
    used_member = None
    idx = 0
    for n, line, member_name in iter_text_lines(source, member):
        total_lines = n
        used_member = member_name
        while idx < len(normalized) and n > normalized[idx][1]:
            idx += 1
        if idx >= len(normalized):
            continue
        start, end = normalized[idx]
        if start <= n <= end:
            out.append(f"L{n:08d}: {line}")
            selected += 1
    return out, {"mode": "line_ranges", "ranges": normalized, "selected_lines": selected, "source_line_count": total_lines, "archive_member": used_member}


def pattern_query(source: Path, member: str | None, request: dict) -> tuple[list[str], dict]:
    pattern = str(request["pattern"])
    use_regex = bool(request.get("regex", False))
    case_sensitive = bool(request.get("case_sensitive", False))
    context = max(0, int(request.get("context_lines", 3)))
    max_matches = max(1, int(request.get("max_matches", 1000)))
    flags = 0 if case_sensitive else re.IGNORECASE
    rx = re.compile(pattern, flags) if use_regex else None
    needle = pattern if case_sensitive else pattern.lower()

    before = deque(maxlen=context)
    out = []
    matches = 0
    total_lines = 0
    used_member = None
    after_remaining = 0
    emitted_until = 0

    def is_match(line: str) -> bool:
        if rx:
            return rx.search(line) is not None
        hay = line if case_sensitive else line.lower()
        return needle in hay

    for n, line, member_name in iter_text_lines(source, member):
        total_lines = n
        used_member = member_name
        matched = is_match(line)
        if matched and matches < max_matches:
            matches += 1
            start_separator = f"--- match {matches} at line {n} ---"
            out.append(start_separator)
            for bn, bline in before:
                if bn > emitted_until:
                    out.append(f"L{bn:08d}: {bline}")
            if n > emitted_until:
                out.append(f"L{n:08d}: {line}")
            emitted_until = max(emitted_until, n)
            after_remaining = context
        elif after_remaining > 0:
            if n > emitted_until:
                out.append(f"L{n:08d}: {line}")
                emitted_until = n
            after_remaining -= 1
        before.append((n, line))

    return out, {
        "mode": "pattern",
        "pattern": pattern,
        "regex": use_regex,
        "case_sensitive": case_sensitive,
        "context_lines": context,
        "max_matches": max_matches,
        "matches_returned": matches,
        "source_line_count": total_lines,
        "archive_member": used_member,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract targeted evidence from a temporary large-runtime artifact")
    parser.add_argument("request", type=Path)
    parser.add_argument("artifact_root", type=Path)
    parser.add_argument("output_root", type=Path)
    args = parser.parse_args()

    request = json.loads(args.request.read_text(encoding="utf-8"))
    if not request.get("enabled", False):
        print("Query disabled.")
        return 0
    request_id = str(request["request_id"])
    evidence_dir = Path(str(request["evidence_dir"]))
    if evidence_dir.is_absolute() or ".." in evidence_dir.parts:
        raise RuntimeError("evidence_dir must be a safe repository-relative path")

    source = choose_source(args.artifact_root, request.get("source_file"))
    member = request.get("archive_member")
    mode = request.get("mode", "pattern")
    if mode == "line_ranges":
        lines, result = line_ranges_query(source, member, list(request.get("line_ranges", [])))
    elif mode == "pattern":
        lines, result = pattern_query(source, member, request)
    else:
        raise RuntimeError(f"Unsupported query mode: {mode}")

    target = args.output_root / evidence_dir / "analysis" / "queries"
    target.mkdir(parents=True, exist_ok=True)
    text_path = target / f"{request_id}.txt"
    meta_path = target / f"{request_id}.json"
    text_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    result.update({
        "request_id": request_id,
        "source_file": str(source.relative_to(args.artifact_root)),
        "result_text": str(text_path),
    })
    meta_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
