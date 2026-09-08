#!/usr/bin/env python3
"""Negative tests proving that integrity validators fail on representative bad fixtures."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import current_state_semantic_validator as cssv
import phase_checkpoint_validator as pcv
import repository_integrity_guard as rig

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "Current/INTEGRITY_ERRATA_REGISTRY.json"
BAD = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["known_bad_values"][0]["value"]


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_unqualified_bad_sha_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "bad.md").write_text(f"runtime sha {BAD}\n", encoding="utf-8")
        registry = {"registry_path": "Current/INTEGRITY_ERRATA_REGISTRY.json", "known_bad_values": [{"id": "bad", "value": BAD}]}
        errors = rig.scan_known_bad_values(root, registry)
        assert_true(bool(errors), "unqualified known-bad SHA must fail")


def test_registered_historical_bad_sha_passes() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "old.md").write_text(f"runtime sha {BAD}\n", encoding="utf-8")
        registry = {"registry_path": "Current/INTEGRITY_ERRATA_REGISTRY.json", "known_bad_values": [{"id": "bad", "value": BAD, "allowed_historical_paths": ["old.md"]}]}
        errors = rig.scan_known_bad_values(root, registry)
        assert_true(not errors, f"registered historical SHA should pass: {errors}")


def test_duplicate_current_authority_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "a.json").write_text("{}", encoding="utf-8")
        (root / "b.json").write_text("{}", encoding="utf-8")
        authority = {"canonical": [
            {"path": "a.json", "authority": "GLOBAL_CURRENT_MACHINE", "canonical_for": ["accepted_baseline"]},
            {"path": "b.json", "authority": "GLOBAL_CURRENT_MACHINE", "canonical_for": ["accepted_baseline"]},
        ]}
        errors = rig.authority_errors(root, authority)
        assert_true(bool(errors), "duplicate current authority must fail")


def test_orphan_topic_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "Knowledge").mkdir()
        (root / "Knowledge" / "ROUTED.md").write_text("ok", encoding="utf-8")
        (root / "Knowledge" / "ORPHAN.md").write_text("bad", encoding="utf-8")
        km = {"topics": [{"canonical": "Knowledge/ROUTED.md"}]}
        errors = rig.orphan_topic_errors(root, km)
        assert_true(bool(errors), "orphan Knowledge topic must fail")


def test_phase_without_predecessor_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        path = root / "ExecutionCheckpoints" / "demo" / "phase_05.json"
        write_json(path, {
            "phase": 5, "status": "PASS", "start_commit": "x", "completion_commit": "y",
            "required_inputs": [], "produced_artifacts": [], "validation_result": "PASS",
            "next_phase": 6, "timestamp": "2026-09-05T00:00:00Z", "predecessor_checkpoint": "missing",
        })
        policy = {"checkpoint_root": "ExecutionCheckpoints", "first_phase": 0, "required_fields": ["phase", "status"]}
        errors = pcv.validate_checkpoint_set(root, policy, check_git=False)
        assert_true(bool(errors), "phase 5 without phase 4 checkpoint must fail")


def test_stale_live_runtime_instruction_fails() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        state = {
            "accepted_baseline": {"build_id": "S1.A", "sha256": "a"},
            "latest_built_artifact": {"build_id": "S1.B", "sha256": "b"},
            "active_candidate": {
                "build_id": "S1.B", "sha256": "b", "profile": "Profiles/S1.B.r2z",
                "profile_sources": "ProfileSources/S1.B/"
            },
            "runtime_test_outstanding": True,
            "selected_scope": {
                "candidate_build_id": "S1.B",
                "analysis_contract": "Run S1.B runtime validation.",
                "currently_irrelevant_actions": []
            }
        }
        write_json(root / "Current/CURRENT_STATE.json", state)
        write_json(root / "Current/PROJECT_KNOWLEDGE_MAP.json", {"topics": [
            {"id": "accepted_baseline", "canonical": "Knowledge/CURRENT_LIFECYCLE.md"},
            {"id": "active_candidate_and_next_test", "canonical": "Knowledge/CURRENT_LIFECYCLE.md", "machine_state": []},
            {"id": "pikmin_enemy_compatibility", "canonical": "Knowledge/PIKMIN_ENEMY_COMPATIBILITY.md"},
            {"id": "roadmap_and_deferred_scopes", "canonical": "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"},
        ]})
        write_json(root / "Current/ARTIFACT_EVIDENCE_INTEGRITY.json", {
            "profiles": [{"build_id": "S1.A", "profile_sha256": "a"}],
            "pending_profiles": [
                {"build_id": "S1.B", "role": "ACTIVE_RUNTIME_CANDIDATE_PENDING", "runtime_evidence_required": False,
                 "profile": "Profiles/S1.B.r2z", "profile_sha256": "b", "profile_sources": "ProfileSources/S1.B/"}
            ]
        })
        marker = cssv.expected_marker(state)
        for rel in cssv.LIVE_DOCS:
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            body = f"{marker}\nAccepted S1.A. Latest S1.B. Candidate S1.B. Runtime test outstanding: yes.\n"
            if rel == "Knowledge/CURRENT_LIFECYCLE.md":
                body += "No runtime test is currently pending.\n"
            path.write_text(body, encoding="utf-8")
        errors = cssv.validate_live_state(root)
        assert_true(any("stale runtime-pending contradiction" in x for x in errors), "stale live runtime instruction must fail")


def main() -> int:
    tests = [
        test_unqualified_bad_sha_fails,
        test_registered_historical_bad_sha_passes,
        test_duplicate_current_authority_fails,
        test_orphan_topic_fails,
        test_phase_without_predecessor_fails,
        test_stale_live_runtime_instruction_fails,
    ]
    for test in tests:
        test()
        print("PASS:", test.__name__)
    print(f"PASS: {len(tests)} negative validator fixtures behaved as required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
