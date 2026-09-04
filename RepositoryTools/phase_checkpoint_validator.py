#!/usr/bin/env python3
"""Validate immutable, monotonic checkpoints for future multi-phase repository operations."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "Current/MULTIPHASE_CHECKPOINT_POLICY.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_ok(root: Path, *args: str) -> bool:
    return subprocess.run(["git", *args], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def git_lines(root: Path, *args: str) -> list[str]:
    proc = subprocess.run(["git", *args], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def validate_checkpoint_set(root: Path, policy: dict[str, Any], check_git: bool = True) -> list[str]:
    errors: list[str] = []
    checkpoint_root = root / str(policy.get("checkpoint_root", "ExecutionCheckpoints"))
    if not checkpoint_root.exists():
        return errors
    required = list(policy.get("required_fields", []))
    for process_dir in sorted(p for p in checkpoint_root.iterdir() if p.is_dir()):
        records: dict[int, tuple[Path, dict[str, Any]]] = {}
        for path in sorted(process_dir.glob("phase_*.json")):
            try:
                data = load_json(path)
            except Exception as exc:
                errors.append(f"{path.relative_to(root)}: invalid JSON: {exc}")
                continue
            for field in required:
                if field not in data:
                    errors.append(f"{path.relative_to(root)}: missing field {field}")
            phase = data.get("phase")
            if not isinstance(phase, int):
                errors.append(f"{path.relative_to(root)}: phase must be integer")
                continue
            if phase in records:
                errors.append(f"{process_dir.relative_to(root)}: duplicate phase {phase}")
            records[phase] = (path, data)

        if not records:
            continue
        phases = sorted(records)
        first_allowed = int(policy.get("first_phase", 0))
        if phases[0] != first_allowed:
            errors.append(f"{process_dir.relative_to(root)}: first checkpoint is phase {phases[0]}, expected {first_allowed}")
        for phase in phases:
            path, data = records[phase]
            if phase > first_allowed:
                if phase - 1 not in records:
                    errors.append(f"{path.relative_to(root)}: phase {phase} exists without phase {phase - 1} PASS checkpoint")
                    continue
                prev_path, prev = records[phase - 1]
                if str(prev.get("status", "")).upper() != "PASS":
                    errors.append(f"{path.relative_to(root)}: predecessor phase {phase - 1} is not PASS")
                expected_prev = prev_path.relative_to(root).as_posix()
                if data.get("predecessor_checkpoint") != expected_prev:
                    errors.append(f"{path.relative_to(root)}: predecessor_checkpoint must be {expected_prev}")

            if str(data.get("status", "")).upper() == "PASS":
                completion = str(data.get("completion_commit", ""))
                if check_git and completion and completion not in {"PENDING", "TBD"}:
                    if not git_ok(root, "cat-file", "-e", f"{completion}^{{commit}}"):
                        errors.append(f"{path.relative_to(root)}: completion_commit does not exist: {completion}")
                    for artifact in data.get("produced_artifacts", []):
                        if not git_ok(root, "cat-file", "-e", f"{completion}:{artifact}"):
                            errors.append(f"{path.relative_to(root)}: completion commit does not contain produced artifact {artifact}")

            if check_git:
                history = git_lines(root, "log", "--format=%H", "--", path.relative_to(root).as_posix())
                if len(history) > 1:
                    errors.append(f"{path.relative_to(root)}: checkpoint was modified after creation; checkpoints are immutable")
    return errors


def main() -> int:
    if not POLICY_PATH.is_file():
        print("ERROR: missing Current/MULTIPHASE_CHECKPOINT_POLICY.json")
        return 1
    policy = load_json(POLICY_PATH)
    errors = validate_checkpoint_set(ROOT, policy, check_git=True)
    for error in errors:
        print("ERROR:", error)
    if errors:
        return 1
    print("PASS: future multi-phase checkpoints are absent or monotonic, immutable and commit-backed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
