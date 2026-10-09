#!/usr/bin/env python3
"""Independent state-neutral freeze of completed SCDIAG1/FXDIAG1 source and proof.

Executed by permanent Knowledge Architecture and TSDIAG1 publication lifecycle,
including on CURRENT_STATE-only PRs. Never invokes historical source compilers.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PINNED_GIT_OBJECTS = {
    "Patches/S142AKSCDiag1": "eccdb2d456aa71a847503724a21b465c54a16de2",
    "Patches/S142AKFXDiag1": "ed5f43c98eb862c87f1a2dca74865c4108f5768e",
    "SourceEvidence/UniversalInteriorViability/SCDIAG1SourceStatic": "46e7786b27621a1f86449586407a889bf5088978",
    "SourceEvidence/UniversalInteriorViability/FXDIAG1SourceStatic": "4d2bcb25529cab4d3175a5b0eafc258d982fe713",
    "AnalysisTools/validate_s142ak_scdiag1_source.py": "8606dd816185a6b0872d6e2288d133c29db8312c",
    "AnalysisTools/validate_s142ak_fxdiag1_source.py": "062f3ce79b00b657dcb49ff4b536ddb5c7bfa812",
    "Current/343_S1.42AK_PHASE_C_STORAGE_COMPLEX_SCDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md": "6649346f0b3e2d1487b0f2d3733f09e3c59bfb7f",
    "Current/328_S1.42AK_PHASE_C_FRACTURED_COMPLEX_FXDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md": "e73f7b84d21675abe935520cb4ffc81c1c121a39",
}
SOURCE_WORKFLOWS = {
    ".github/workflows/s142ak-scdiag1-source-static.yml": (
        "Patches/S142AKSCDiag1/**",
        "AnalysisTools/validate_s142ak_scdiag1_source.py",
        "SourceEvidence/UniversalInteriorViability/SCDIAG1SourceStatic/**",
        "Current/343_S1.42AK_PHASE_C_STORAGE_COMPLEX_SCDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md",
    ),
    ".github/workflows/s142ak-fxdiag1-source-static.yml": (
        "Patches/S142AKFXDiag1/**",
        "AnalysisTools/validate_s142ak_fxdiag1_source.py",
        "SourceEvidence/UniversalInteriorViability/FXDIAG1SourceStatic/**",
        "Current/328_S1.42AK_PHASE_C_FRACTURED_COMPLEX_FXDIAG1_SOURCE_STATIC_IMPLEMENTATION_CHECKPOINT.md",
    ),
}
SCD_LOG = "39dfe45721befd6e256a341497100534c45d37868de14dc29ba6a58c08ce207e"
FXD_LOG = "748bed34edc8a4cb68cc9ff0c9b1d7ba6380aa85a3e3a8719bdabc0492e7e801"


def demand(ok: bool, reason: str) -> None:
    if not ok:
        raise RuntimeError("cross-diagnostic frozen-source/proof boundary: " + reason)


def check_pins(found: dict[str, str]) -> None:
    for path, sha in PINNED_GIT_OBJECTS.items():
        demand(found.get(path) == sha, "frozen Git tree/blob drift: " + path)


def check_workflows(workflows: dict[str, str]) -> None:
    for path, required in SOURCE_WORKFLOWS.items():
        body = workflows[path]
        demand("'Current/CURRENT_STATE.json'" not in body, "volatile source trigger: " + path)
        for token in (*required, path):
            demand("'" + token + "'" in body, "missing source path trigger: " + token)
        demand("ref: \${{ github.event.pull_request.head.sha }}" in body,
               "source checkout not exact PR head: " + path)
        demand("dotnet run --project" in body and "dotnet build" in body and
               "python AnalysisTools/validate_s142ak_" in body,
               "source tests/compile/validator were disabled: " + path)


def check_closed_proof(state: dict) -> None:
    p = state["selected_scope"]["phase_c"]
    demand(state["accepted_baseline"]["build_id"] == "S1.42AK" and
           state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1" and
           state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED" and
           state["runtime_test_outstanding"] is True, "gameplay baseline/passive gate changed")
    demand(p["residual_no_trusted_actual_generation_proof"] == 22 and
           p["residual_viable_equal_100"] == 10 and
           p["residual_owner_hard_block"] == 12, "residual proof count changed")
    demand(p["storage_complex_scdiag1_source_static_validated"] is True and
           p["storage_complex_scdiag1_source_pr_final_head"] ==
           "973b8648644bcfc9fb42ff4943b3ca38b5d82a5e" and
           p["storage_complex_scdiag1_source_static_run"] == 37843419333 and
           p["storage_complex_scdiag1_source_main_knowledge_architecture_run"] == 37845920307,
           "SCDIAG1 validated source lineage changed")
    demand(p["storage_complex_scdiag1_runtime_armed"] is False and
           p["storage_complex_runtime_test_authorized"] is False and
           p["storage_complex_scdiag1_runtime_test_authorized"] is False and
           p["storage_complex_scdiag1_runtime_attempts_consumed"] == 1 and
           p["storage_complex_scdiag1_runtime_log_sha256"] == SCD_LOG and
           p["storage_complex_scdiag1_runtime_pathfinding_logical_connections"] == 4 and
           p["storage_complex_scdiag1_runtime_proof_status"] ==
           "PASS_DIAGNOSTIC_GENERATED_STORAGE_COMPLEX_STORAGECOMPLEX_GENERATION_MATERIALIZATION",
           "SCDIAG1 completed proof/rearm drift")
    demand(p["fractured_complex_fxdiag1_source_static_validated"] is True and
           p["fractured_complex_fxdiag1_source_pr_final_head"] ==
           "8003dcde3291a91c0e8cbcce7bd8bfe8082232a5" and
           p["fractured_complex_fxdiag1_source_main_knowledge_architecture_run"] == 37792853298,
           "FXDIAG1 validated source lineage changed")
    demand(p["fractured_complex_fxdiag1_runtime_armed"] is False and
           p["fractured_complex_fxdiag1_runtime_authorized"] is False and
           p["fractured_complex_fxdiag1_runtime_test_authorized"] is False and
           p["fractured_complex_fxdiag1_runtime_attempts_consumed"] == 1 and
           p["fractured_complex_fxdiag1_runtime_log_sha256"] == FXD_LOG and
           p["fractured_complex_fxdiag1_runtime_pathfinding_logical_connections"] == 4 and
           p["fractured_complex_fxdiag1_runtime_proof_status"] ==
           "PASS_DIAGNOSTIC_GENERATED_FRACTURED_COMPLEX_FRACTUREDCOMPLEXFLOW_GENERATION_MATERIALIZATION",
           "FXDIAG1 completed proof/rearm drift")
    # In particular: DO NOT bind this frozen proof to the mutable active pointer
    # or selected_scope.diagnostic_revision. Later, independently authorized TS
    # routing must not recompile either completed historical selector.


def self_test(state: dict, workflows: dict[str, str]) -> None:
    check_pins(dict(PINNED_GIT_OBJECTS))
    for path in PINNED_GIT_OBJECTS:
        bad = dict(PINNED_GIT_OBJECTS)
        bad[path] = "0" * 40
        expect_reject(lambda: check_pins(bad), "pin mutation " + path)
    check_workflows(workflows)
    for path in SOURCE_WORKFLOWS:
        bad = dict(workflows)
        bad[path] = bad[path].replace("dotnet build", "dotnet skip")
        expect_reject(lambda: check_workflows(bad), "source compiler removed")
        bad[path] = workflows[path].replace("  pull_request:", "  pull_request:\n    paths:\n      - 'Current/CURRENT_STATE.json'")
        expect_reject(lambda: check_workflows(bad), "volatile trigger restored")
    check_closed_proof(state)
    for key in ("storage_complex_scdiag1_runtime_attempts_consumed",
                "fractured_complex_fxdiag1_runtime_attempts_consumed",
                "storage_complex_scdiag1_runtime_armed",
                "fractured_complex_fxdiag1_runtime_armed",
                "storage_complex_scdiag1_runtime_log_sha256",
                "fractured_complex_fxdiag1_runtime_log_sha256",
                "storage_complex_scdiag1_source_static_run",
                "fractured_complex_fxdiag1_source_pr_final_head"):
        bad = copy.deepcopy(state)
        bad["selected_scope"]["phase_c"][key] = True if key.endswith("runtime_armed") else "MUTATED"
        expect_reject(lambda: check_closed_proof(bad), "closed proof mutation " + key)
    # Synthetic newer TS target: no historical pointer or diagnostic-revision dependency.
    allowed = copy.deepcopy(state)
    allowed["controllers"]["runtime_active_build"] = "S1.42AK-TSDIAG1"
    allowed["selected_scope"]["diagnostic_revision"] = {"build_id": "S1.42AK-TSDIAG1"}
    check_closed_proof(allowed)
    print("PASS: frozen-source Git pins, source path triggers and independent completed-proof negative mutations")


def expect_reject(fn, description: str) -> None:
    try:
        fn()
    except (RuntimeError, KeyError, TypeError, AssertionError):
        return
    raise AssertionError("failed negative test: " + description)


def main() -> None:
    found = {}
    for path in PINNED_GIT_OBJECTS:
        found[path] = subprocess.check_output(
            ["git", "rev-parse", "HEAD:" + path], cwd=ROOT, text=True
        ).strip()
    workflows = {path: (ROOT / path).read_text(encoding="utf-8")
                 for path in SOURCE_WORKFLOWS}
    state = json.loads((ROOT / "Current/CURRENT_STATE.json").read_text(encoding="utf-8"))
    check_pins(found)
    check_workflows(workflows)
    check_closed_proof(state)
    if "--self-test" in sys.argv[1:]:
        self_test(state, workflows)
    else:
        print("PASS: frozen SCDIAG1/FXDIAG1 source, evidence and completed proof independently pinned")


if __name__ == "__main__":
    main()
