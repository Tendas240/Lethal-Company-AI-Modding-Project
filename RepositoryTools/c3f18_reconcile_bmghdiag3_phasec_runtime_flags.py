#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "Current/CURRENT_STATE.json"

state = json.loads(STATE.read_text(encoding="utf-8"))
scope = state["selected_scope"]
phase_c = scope["phase_c"]
diag = scope["diagnostic_revision"]

assert diag["build_id"] == "S1.42AK-BMGHDIAG3"
assert diag["runtime_armed"] is False
assert diag["runtime_result"] == "PASS_BLACK_MESA_GREENHOUSE_RUNTIME_COMPATIBILITY"
assert phase_c["black_mesa_greenhouse_status"] == "PASS_RUNTIME_COMPATIBLE_BLACK_MESA_GREENHOUSE_DIAGNOSTIC_ONLY"
assert phase_c["bmgdiag3_review_runtime_armed"] is True
assert phase_c["bmgdiag3_runtime_activation_status"] == "ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_TEST_OUTSTANDING_NEVER_ACCEPT"

phase_c["bmgdiag3_review_runtime_armed"] = False
phase_c["bmgdiag3_runtime_activation_status"] = "COMPLETED_DIAGNOSTIC_RUNTIME_COMPATIBILITY_PASS_NEVER_ACCEPT_NOT_ACTIVE"

for key, expected in (
    ("bmgdiag3_review_runtime_armed", False),
    ("bmgdiag3_runtime_activation_status", "COMPLETED_DIAGNOSTIC_RUNTIME_COMPATIBILITY_PASS_NEVER_ACCEPT_NOT_ACTIVE"),
):
    if key in scope:
        assert scope[key] == expected
        del scope[key]

STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("Reconciled BMGHDIAG3 phase-C runtime activation flags.")
