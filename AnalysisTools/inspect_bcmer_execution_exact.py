#!/usr/bin/env python3
"""Exact BCMER 1.71.0 event-execution capture for S1.42AI-DIAG1 patch-safety review."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "bcmer-execution-exact-output"
WORK = Path(os.environ["RUNNER_TEMP"]) / "s142ai-bcmer-execution-exact"
OUT.mkdir(exist_ok=True)
WORK.mkdir(exist_ok=True)

CANONICAL_MAIN = "15cd35a62a995b1895634d40a661a880aa6f087d"
PACKAGE = "SoftDiamond-BrutalCompanyMinusExtraReborn"
VERSION = "1.71.0"
URL = f"https://gcdn.thunderstore.io/live/repository/packages/{PACKAGE}-{VERSION}.zip"
ZIP_SHA256 = "fa3d7727eef5ff023291caa7b0a306194b3a3826b8361af5bc42c7a6b58b1534"
MEMBER = "BrutalCompanyMinus.dll"
DLL_SHA256 = "c344d3fdddd1f4ac32c80d3ec24eee54810c4cfd91a13594d88579fa23bbf148"
ILSPY_VERSION = "11.0.0.9375"
MAX_PACKAGE_BYTES = 256 * 1024 * 1024
MAX_OUTPUT_BYTES = 192 * 1024 * 1024
ALLOWED_DELTA = {
    "AnalysisTools/inspect_bcmer_execution_exact.py",
    ".github/workflows/bcmer-execution-exact-review.yml",
}

TOKENS = (
    "forcedEvents",
    "sideEvents",
    "customEvents",
    "EventsToSpawnWith",
    "EventsToRemove",
    "ApplyEvents",
    ".Execute()",
    "GetEvent(",
    "AddEventIfOnly",
    "Register",
    "CustomEvent",
    "API",
    "ChooseEvents",
    "disabledEvents",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr[-3000:]))
    return p.stdout.strip()


def verify_analysis_branch_delta() -> None:
    p = subprocess.run(
        ["git", "merge-base", "--is-ancestor", CANONICAL_MAIN, "HEAD"],
        cwd=ROOT, text=True, capture_output=True, timeout=60,
    )
    if p.returncode:
        raise RuntimeError("Canonical main is not an ancestor of analysis HEAD")
    changed = [x for x in git("diff", "--name-only", CANONICAL_MAIN + "..HEAD").splitlines() if x]
    unexpected = sorted(set(changed) - ALLOWED_DELTA)
    if unexpected:
        raise RuntimeError("Unexpected analysis-branch delta: " + ", ".join(unexpected))


def run(args: list[str]) -> bytes:
    p = subprocess.run(args, capture_output=True, timeout=420)
    if p.returncode:
        raise RuntimeError(
            f"{args[0]} failed ({p.returncode}): "
            + p.stderr.decode("utf-8", errors="replace")[-5000:]
        )
    if len(p.stdout) > MAX_OUTPUT_BYTES:
        raise RuntimeError(f"Decompiler output exceeded {MAX_OUTPUT_BYTES} bytes")
    return p.stdout


def download(url: str, path: Path) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "s142ai-bcmer-execution-exact/1"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read(MAX_PACKAGE_BYTES + 1)
    if len(data) > MAX_PACKAGE_BYTES:
        raise RuntimeError("Bounded package download exceeded 256 MiB")
    path.write_bytes(data)
    return data


def contexts(text: str, tokens: tuple[str, ...], radius: int = 5) -> str:
    lines = text.splitlines()
    chosen: set[int] = set()
    for i, line in enumerate(lines):
        if any(token in line for token in tokens):
            lo = max(0, i - radius)
            hi = min(len(lines), i + radius + 1)
            chosen.update(range(lo, hi))
    out: list[str] = []
    last = -2
    for i in sorted(chosen):
        if i != last + 1:
            out.append("\n---\n")
        out.append(f"{i + 1}: {lines[i]}")
        last = i
    return "\n".join(out) + "\n"


verify_analysis_branch_delta()
zip_path = WORK / f"{PACKAGE}-{VERSION}.zip"
package_bytes = download(URL, zip_path)
actual_zip = sha256(package_bytes)
if actual_zip != ZIP_SHA256:
    raise RuntimeError(f"ZIP SHA mismatch: {actual_zip}")

with zipfile.ZipFile(zip_path) as archive:
    if MEMBER not in archive.namelist():
        raise RuntimeError(f"Exact DLL member missing: {MEMBER}")
    dll_bytes = archive.read(MEMBER)
actual_dll = sha256(dll_bytes)
if actual_dll != DLL_SHA256:
    raise RuntimeError(f"DLL SHA mismatch: {actual_dll}")

dll_path = WORK / MEMBER
dll_path.write_bytes(dll_bytes)
source = run(["ilspycmd", str(dll_path)])
il = run(["ilspycmd", "-il", str(dll_path)])
source_text = source.decode("utf-8", errors="replace")
il_text = il.decode("utf-8", errors="replace")

required_markers = (
    "class EventManager",
    "class MEvent",
    "forcedEvents",
    "customEvents",
    "EventsToSpawnWith",
    "ApplyEvents",
    "ChooseEvents",
)
missing = [m for m in required_markers if m not in source_text]
if missing:
    raise RuntimeError("Required BCMER execution markers missing from full decompile: " + ", ".join(missing))

source_name = "BrutalCompanyMinus-1.71.0.cs"
il_name = "BrutalCompanyMinus-1.71.0.il"
focus_name = "EXECUTION_CONTEXTS.txt"
(OUT / source_name).write_bytes(source)
(OUT / il_name).write_bytes(il)
(OUT / focus_name).write_text(contexts(source_text, TOKENS, radius=7), encoding="utf-8")

patterns = {
    "forcedEvents": r"\bforcedEvents\b",
    "sideEvents": r"\bsideEvents\b",
    "customEvents": r"\bcustomEvents\b",
    "disabledEvents": r"\bdisabledEvents\b",
    "EventsToSpawnWith": r"\bEventsToSpawnWith\b",
    "ApplyEvents": r"\bApplyEvents\b",
    "Execute_call_syntax": r"\.Execute\s*\(\s*\)",
    "GetEvent": r"\bGetEvent\s*\(",
    "ChooseEvents": r"\bChooseEvents\s*\(",
    "AddEventIfOnly": r"\bAddEventIfOnly\s*\(",
    "public_API_type": r"class\s+API\b",
}
counts = {name: len(re.findall(pattern, source_text)) for name, pattern in patterns.items()}

verification = {
    "schema_version": 1,
    "purpose": "Exact full-assembly BCMER 1.71.0 event-execution review for S1.42AI-DIAG1 forced/forced-side/additional/runtime-custom coverage",
    "canonical_main": CANONICAL_MAIN,
    "repository_commit": os.environ.get("GITHUB_SHA"),
    "package": PACKAGE,
    "version": VERSION,
    "package_url": URL,
    "package_zip_sha256": actual_zip,
    "member": MEMBER,
    "dll_sha256": actual_dll,
    "decompiler": {"tool": "ilspycmd", "version": ILSPY_VERSION},
    "source_sha256": sha256(source),
    "source_bytes": len(source),
    "source_lines": len(source_text.splitlines()),
    "il_sha256": sha256(il),
    "il_bytes": len(il),
    "il_lines": len(il_text.splitlines()),
    "source_occurrences": counts,
    "required_markers_present": True,
    "outputs": [source_name, il_name, focus_name],
    "qualification": "Complete exact package/DLL C# and IL capture for BCMER 1.71.0 only. This artifact is evidence for method/call-site/state-contract review; it does not itself authorize DIAG1 implementation, build, controller transition, Gale import or gameplay testing.",
}
(OUT / "VERIFICATION.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
print(json.dumps(verification, indent=2))
