#!/usr/bin/env python3
"""Versioned, fail-closed historical-source / current Residual-21 CI lifecycle.

Never rewrites frozen source validators, produces profile bytes, or authorizes runtime.
The archived validators execute in an authentic detached Git worktree; the current
phase is checked independently against the original Toy Store evidence and PR #429.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = "b45a1753353dd3cf6a84c2f9c4091aeb74f3b791"
FROZEN = {
    "AnalysisTools/validate_s142ak_tsdiag1_source.py": "601a9c814deabcc21e32351f72dbdcfba7969db7",
    "AnalysisTools/validate_s142ak_scdiag1_source.py": "8606dd816185a6b0872d6e2288d133c29db8312c",
}
IMMUTABLE_FROM_ARCHIVE = (
    "Patches/S142AKTSDiag1",
    "Patches/S142AKSCDiag1",
    "SourceEvidence/UniversalInteriorViability/TSDIAG1SourceStatic",
    "SourceEvidence/UniversalInteriorViability/SCDIAG1SourceStatic",
    "BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json",
    "BuildSpecs/S1.42AK-SCDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json",
    "BuildSystem/tsdiag1_review_build.py",
    "BuildSystem/scdiag1_review_build.py",
    "AnalysisTools/validate_s142ak_tsdiag1_build.py",
    "AnalysisTools/validate_s142ak_scdiag1_build.py",
    "AnalysisTools/validate_s142ak_scdiag1_activation.py",
)
TS_INDEX = "RuntimeEvidence/S1.42AK-TSDIAG1/20261011T231328Z/INDEX.json"
LOG_SHA = "d964ea75b357a50bc942480576899ef00f1bc1cb984597afd2c4eaf7c06b9155"
TS_PROOF = "PASS_DIAGNOSTIC_GENERATED_ACTUAL_GENERATION_AND_MATERIALIZATION_NATURAL_SELECTION_UNPROVEN"
SCD_LOG_SHA = "39dfe45721befd6e256a341497100534c45d37868de14dc29ba6a58c08ce207e"
ADAPTER = "AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py"
SOURCE_WORKFLOWS = (
    ".github/workflows/s142ak-tsdiag1-source-static.yml",
    ".github/workflows/s142ak-scdiag1-source-static.yml",
)
BUILD_WORKFLOWS = (
    ".github/workflows/s142ak-tsdiag1-build-static.yml",
    ".github/workflows/s142ak-scdiag1-build-static.yml",
)
KNOWLEDGE = ".github/workflows/knowledge-architecture.yml"
TS_HEAD = "f4d1714b7113d1383b2178dca05a426212885c6b"
TS_MERGE = "e5c5fabbe6f60caa24e3a63b4e282c6594a4bd7f"


def demand(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError("RESIDUAL21_LIFECYCLE_V1_FAIL_CLOSED: " + why)


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def git_blob(revision: str, path: str) -> str:
    return git("rev-parse", revision + ":" + path)


def json_file(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check_frozen(found: dict[str, str], archived: dict[str, str]) -> None:
    for path, sha in FROZEN.items():
        demand(archived[path] == sha, "historical source blob: " + path)
        demand(found[path] == sha, "current source blob changed: " + path)
    for path in IMMUTABLE_FROM_ARCHIVE:
        demand(found[path] == archived[path], "original source/review drift: " + path)


def check_historical_state(state: dict, active: str, build: dict) -> None:
    p = state["selected_scope"]["phase_c"]
    demand((p["residual_no_trusted_actual_generation_proof"],
            p["residual_viable_equal_100"], p["residual_owner_hard_block"]) ==
           (22, 10, 12), "archive is not the pre-Toy-Store 22=10+12 phase")
    demand(p["toy_store_tsdiag1_runtime_armed"] is False and
           p["toy_store_runtime_test_authorized"] is False and
           p["toy_store_tsdiag1_built"] is False and
           p["toy_store_tsdiag1_review_build_pass"] is True and
           p["toy_store_tsdiag1_source_static_validated"] is True,
           "historical Toy Store source/review stage changed")
    demand(p["storage_complex_scdiag1_runtime_armed"] is False and
           p["storage_complex_runtime_test_authorized"] is False and
           p["storage_complex_scdiag1_runtime_attempts_consumed"] == 1 and
           p["storage_complex_scdiag1_runtime_log_sha256"] == SCD_LOG_SHA,
           "historical completed Storage Complex phase changed")
    demand(state["accepted_baseline"]["build_id"] == "S1.42AK" and
           state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1" and
           state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED" and
           state["runtime_test_outstanding"] is True and
           state["controllers"]["runtime_active_build"] == active == "S1.42AK-BMDSFIX1" and
           build["enabled"] is False and
           build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS" and
           build["output_profile"] == "Profiles/DO_NOT_BUILD.r2z",
           "historical baseline/controller boundary changed")


def check_current(state: dict, index: dict, build: dict, active: str) -> None:
    p = state["selected_scope"]["phase_c"]
    expect = {
        "residual_no_trusted_actual_generation_proof": 21,
        "residual_viable_equal_100": 9,
        "residual_owner_hard_block": 12,
        "toy_store_generation_proof_status": TS_PROOF,
        "toy_store_tsdiag1_runtime_evidence_reconciled": True,
        "toy_store_tsdiag1_runtime_attempt_consumed": True,
        "toy_store_tsdiag1_runtime_armed": False,
        "toy_store_runtime_test_authorized": False,
        "toy_store_tsdiag1_built": False,
        "toy_store_tsdiag1_runtime_reconciliation": "Current/393_S1.42AK_TSDIAG1_TOY_STORE_RUNTIME_EVIDENCE_RECONCILIATION.md",
        "toy_store_tsdiag1_runtime_evidence": "RuntimeEvidence/S1.42AK-TSDIAG1/20261011T231328Z/",
        "toy_store_tsdiag1_runtime_index": TS_INDEX,
        "toy_store_tsdiag1_runtime_log_sha256": LOG_SHA,
        "toy_store_tsdiag1_runtime_reconciliation_pr": 429,
        "toy_store_tsdiag1_runtime_reconciliation_pr_final_head": TS_HEAD,
        "toy_store_tsdiag1_runtime_reconciliation_main_commit": TS_MERGE,
        "toy_store_tsdiag1_runtime_reconciliation_main_knowledge_architecture_push_run": 38184195902,
        "storage_complex_scdiag1_runtime_armed": False,
        "storage_complex_runtime_test_authorized": False,
        "storage_complex_scdiag1_runtime_attempts_consumed": 1,
        "storage_complex_scdiag1_runtime_log_sha256": SCD_LOG_SHA,
    }
    for name, value in expect.items():
        demand(type(p[name]) is type(value) and p[name] == value,
               "current lifecycle/provenance mismatch: " + name)
    files = index["files"]
    demand(index["build_id"] == "S1.42AK-TSDIAG1" and
           len(files) == 1 and files[0]["name"] == "LogOutput.log" and
           files[0]["size"] == 1537121 and files[0]["sha256"] == LOG_SHA,
           "original Toy Store INDEX provenance mismatch")
    demand(state["selected_scope"]["scope_id"] == "UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY" and
           state["accepted_baseline"]["build_id"] == "S1.42AK" and
           state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1" and
           state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED" and
           state["runtime_test_outstanding"] is True, "accepted/passive runtime boundary changed")
    demand(state["controllers"]["runtime_active_build"] == active == "S1.42AK-BMDSFIX1" and
           state["controllers"]["build_enabled"] is False and
           state["controllers"]["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS" and
           build["enabled"] is False and
           build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS" and
           build["output_profile"] == "Profiles/DO_NOT_BUILD.r2z" and
           build["local_plugin_builds"] == [] and
           build["config_patches"] == [] and
           build["mod_additions"] == [] and
           build["mod_removals"] == [], "current build/runtime controllers changed")
    demand(state["next_action"] == state["selected_scope"]["next_action"],
           "current next-action mirrors disagree")
    demand(p["storage_complex_target_generation_status"] ==
           "PASS_DIAGNOSTIC_GENERATED_STORAGECOMPLEX_GENERATION_MATERIALIZATION_PROOF_NATURAL_SELECTION_NOT_PROVEN" and
           p["storage_complex_scdiag1_runtime_status"] ==
           "RUNTIME_COMPLETE_PASS_DIAGNOSTIC_GENERATION_MATERIALIZATION_PROOF_NEVER_ACCEPT" and
           state["selected_scope"]["diagnostic_revision"]["runtime_armed"] is False,
           "SCDIAG1 completed-proof/diagnostic disarm drift")


def check_authoritative_documents(record393: str, record394: str) -> None:
    demand(all(v in record393 for v in ("22 → 21", "ToystoreFlow",
           "one actual diagnostic-generated", LOG_SHA)),
           "393 Toy Store diagnostic-generation original reconciliation drift")
    demand(all(v in record394 for v in ("[PR #429]", TS_HEAD, TS_MERGE,
           "38184195902", "21 = 9 viable/equal-100 + 12 owner-hard-block")),
           "394 integrated Toy Store provenance drift")


def check_workflows(bodies: dict[str, str]) -> None:
    for path, name in zip(SOURCE_WORKFLOWS, ("tsdiag1", "scdiag1")):
        body = bodies[path]
        demand("ref: " + "$" + "{{ github.event.pull_request.head.sha }}" in body and
               "fetch-depth: 0" in body and
               ("Patches/S142AK" + ("TSDiag1" if name == "tsdiag1" else "SCDiag1")) in body and
               "Knowledge/INTERIORS_AND_LLL.md" in body and
               ADAPTER in body and
               "python " + ADAPTER + " --historical" in body and
               "python " + ADAPTER + " --current" in body and
               "python " + ADAPTER + " --self-test" in body and
               "dotnet run --project" in body and
               "dotnet build" in body and
               "      - 'Current/CURRENT_STATE.json'" not in body,
               "source static/legacy+current/compilation path weakened: " + path)
    for path in BUILD_WORKFLOWS:
        body = bodies[path]
        demand("if: steps.frozen.outputs.exists != 'true'" in body and
               "Refuse repeat review build" in body and
               "git', 'diff', '--exit-code'" in body and
               "review_build" in body and
               ADAPTER in body and
               "unreviewed completed-runtime source validator drift" in body
               if path.endswith("scdiag1-build-static.yml") else
               "if: steps.frozen.outputs.exists != 'true'" in body and
               "Refuse repeat review build" in body and
               "git', 'diff', '--exit-code'" in body and
               "Unexpected source-validator drift" in body and ADAPTER in body,
               "frozen review guard disabled: " + path)
    body = bodies[KNOWLEDGE]
    demand("python AnalysisTools/validate_s142ak_cross_diagnostic_frozen_provenance.py" in body and
           "python AnalysisTools/validate_s142ak_cross_diagnostic_frozen_provenance.py --self-test" in body and
           "python " + ADAPTER + " --historical" in body and
           "python " + ADAPTER + " --current" in body and
           "python " + ADAPTER + " --self-test" in body and
           "fetch-depth: 0" in body and
           "'AnalysisTools/**'" in body and "'Current/**'" in body,
           "independent knowledge architecture or negative tests weakened")


def verify_objects() -> tuple[dict[str, str], dict[str, str]]:
    demand(subprocess.run(["git", "merge-base", "--is-ancestor", ARCHIVE, "HEAD"],
                          cwd=ROOT, check=False).returncode == 0,
           "historical fixture commit is not an ancestor of HEAD")
    found = {}
    archived = {}
    for path in (*FROZEN, *IMMUTABLE_FROM_ARCHIVE):
        found[path] = git_blob("HEAD", path)
        archived[path] = git_blob(ARCHIVE, path)
    check_frozen(found, archived)
    demand(git_blob("HEAD", TS_INDEX) == "860f16b80b357147e2f070757156bcf4733e6624",
           "original INDEX Git blob identity changed")
    demand(git_blob("HEAD", "Current/393_S1.42AK_TSDIAG1_TOY_STORE_RUNTIME_EVIDENCE_RECONCILIATION.md")
           == "94e2d8d0a5aa80320e46eebacba5c58802694643",
           "393 original reconciliation blob changed")
    demand(git_blob("HEAD", "Current/394_S1.42AK_TSDIAG1_POST_429_RUNTIME_EVIDENCE_HANDOVER_AUTHORITY_RECONCILIATION.md")
           == "6223a5ba8aed3b2b1c6f751b1972abff1087c133",
           "394 integration reconciliation blob changed")
    git_blob("HEAD", "RuntimeEvidence/S1.42AK-TSDIAG1/20261011T231328Z/raw/LogOutput.log")
    return found, archived


def verify_historical(run_originals: bool) -> None:
    found, archived = verify_objects()
    archived_state = json.loads(git("show", ARCHIVE + ":Current/CURRENT_STATE.json"))
    archived_build = json.loads(git("show", ARCHIVE + ":BuildSpecs/current.json"))
    archived_active = git("show", ARCHIVE + ":RuntimeInbox/ACTIVE_BUILD.txt")
    check_historical_state(archived_state, archived_active, archived_build)
    if not run_originals:
        return
    with tempfile.TemporaryDirectory(prefix="residual21-legacy-") as directory:
        target = Path(directory) / "original"
        subprocess.run(["git", "worktree", "add", "--detach", str(target), ARCHIVE],
                       cwd=ROOT, check=True)
        try:
            for path in FROZEN:
                completed = subprocess.run([sys.executable, str(target / path)],
                                           cwd=target, check=False)
                demand(completed.returncode == 0,
                       "authentic historical source validator failed: " + path)
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(target)],
                           cwd=ROOT, check=True)
    print("PASS: BOTH original frozen source validators actually executed on authentic 22=10+12 snapshot")


def verify_current() -> None:
    verify_objects()
    state = json_file("Current/CURRENT_STATE.json")
    index = json_file(TS_INDEX)
    build = json_file("BuildSpecs/current.json")
    active = (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()
    check_current(state, index, build, active)
    check_authoritative_documents(
        (ROOT / "Current/393_S1.42AK_TSDIAG1_TOY_STORE_RUNTIME_EVIDENCE_RECONCILIATION.md").read_text(encoding="utf-8"),
        (ROOT / "Current/394_S1.42AK_TSDIAG1_POST_429_RUNTIME_EVIDENCE_HANDOVER_AUTHORITY_RECONCILIATION.md").read_text(encoding="utf-8"))
    check_workflows({path: (ROOT / path).read_text(encoding="utf-8")
                     for path in (*SOURCE_WORKFLOWS, *BUILD_WORKFLOWS, KNOWLEDGE)})
    print("PASS: current 21=9+12 checked independently against immutable Toy Store provenance and controllers")


def expect_reject(fn, label: str) -> None:
    try:
        fn()
    except (RuntimeError, KeyError, TypeError, ValueError, AssertionError):
        return
    raise AssertionError("negative mutation unexpectedly PASSED: " + label)


def negative_tests() -> None:
    verify_objects()
    state = json_file("Current/CURRENT_STATE.json")
    index = json_file(TS_INDEX)
    build = json_file("BuildSpecs/current.json")
    active = (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()
    check_current(state, index, build, active)
    current = state["selected_scope"]["phase_c"]
    mutations = {
        "residual_no_trusted_actual_generation_proof": 22,
        "residual_viable_equal_100": 10,
        "residual_owner_hard_block": 11,
        "toy_store_generation_proof_status": "UNPROVEN",
        "toy_store_tsdiag1_runtime_evidence_reconciled": False,
        "toy_store_tsdiag1_runtime_attempt_consumed": False,
        "toy_store_tsdiag1_runtime_armed": True,
        "toy_store_runtime_test_authorized": True,
        "toy_store_tsdiag1_runtime_log_sha256": "0" * 64,
        "toy_store_tsdiag1_runtime_index": "MUTATED",
        "toy_store_tsdiag1_runtime_reconciliation": "MUTATED",
        "toy_store_tsdiag1_runtime_reconciliation_pr": 0,
        "toy_store_tsdiag1_runtime_reconciliation_pr_final_head": "0" * 40,
        "toy_store_tsdiag1_runtime_reconciliation_main_commit": "0" * 40,
        "toy_store_tsdiag1_runtime_reconciliation_main_knowledge_architecture_push_run": 0,
        "storage_complex_scdiag1_runtime_armed": True,
        "storage_complex_scdiag1_runtime_attempts_consumed": 0,
    }
    for key, value in mutations.items():
        bad = copy.deepcopy(state)
        bad["selected_scope"]["phase_c"][key] = value
        expect_reject(lambda b=bad: check_current(b, index, build, active), "state " + key)
    for key, value in (("build_id", "INVALID"), ("files", [])):
        bad = copy.deepcopy(index)
        bad[key] = value
        expect_reject(lambda b=bad: check_current(state, b, build, active), "index " + key)
    for key, value in (("size", 1), ("sha256", "0" * 64), ("name", "wrong.log")):
        bad = copy.deepcopy(index)
        bad["files"][0][key] = value
        expect_reject(lambda b=bad: check_current(state, b, build, active), "log " + key)
    for key in ("enabled", "build_id", "output_profile"):
        bad = copy.deepcopy(build)
        bad[key] = True if key == "enabled" else "UNAUTHORIZED"
        expect_reject(lambda b=bad: check_current(state, index, b, active), "controller " + key)
    expect_reject(lambda: check_current(state, index, build, "S1.42AK-TSDIAG1"),
                  "runtime rearm")
    historical = json.loads(git("show", ARCHIVE + ":Current/CURRENT_STATE.json"))
    arch_build = json.loads(git("show", ARCHIVE + ":BuildSpecs/current.json"))
    arch_active = git("show", ARCHIVE + ":RuntimeInbox/ACTIVE_BUILD.txt")
    for key, value in (("residual_no_trusted_actual_generation_proof", 21),
                       ("residual_viable_equal_100", 9),
                       ("residual_owner_hard_block", 11),
                       ("toy_store_tsdiag1_runtime_armed", True)):
        bad = copy.deepcopy(historical)
        bad["selected_scope"]["phase_c"][key] = value
        expect_reject(lambda b=bad: check_historical_state(b, arch_active, arch_build),
                      "historical " + key)
    found = {path: git_blob("HEAD", path) for path in (*FROZEN, *IMMUTABLE_FROM_ARCHIVE)}
    archived = {path: git_blob(ARCHIVE, path) for path in (*FROZEN, *IMMUTABLE_FROM_ARCHIVE)}
    for path in (*FROZEN, *IMMUTABLE_FROM_ARCHIVE):
        bad = dict(found)
        bad[path] = "0" * 40
        expect_reject(lambda b=bad: check_frozen(b, archived), "frozen Git pin " + path)
    bodies = {path: (ROOT / path).read_text(encoding="utf-8")
              for path in (*SOURCE_WORKFLOWS, *BUILD_WORKFLOWS, KNOWLEDGE)}
    check_workflows(bodies)
    for path in bodies:
        bad = dict(bodies)
        if path in SOURCE_WORKFLOWS:
            bad[path] = bodies[path].replace("python " + ADAPTER + " --historical", "")
        elif path in BUILD_WORKFLOWS:
            bad[path] = bodies[path].replace("if: steps.frozen.outputs.exists != 'true'", "")
        else:
            bad[path] = bodies[path].replace("python " + ADAPTER + " --self-test", "")
        expect_reject(lambda b=bad: check_workflows(b), "workflow " + path)
    original393 = (ROOT / "Current/393_S1.42AK_TSDIAG1_TOY_STORE_RUNTIME_EVIDENCE_RECONCILIATION.md").read_text(encoding="utf-8")
    original394 = (ROOT / "Current/394_S1.42AK_TSDIAG1_POST_429_RUNTIME_EVIDENCE_HANDOVER_AUTHORITY_RECONCILIATION.md").read_text(encoding="utf-8")
    expect_reject(lambda: check_authoritative_documents(original393.replace(LOG_SHA, "0" * 64), original394),
                  "original 393 reconciliation")
    expect_reject(lambda: check_authoritative_documents(original393, original394.replace(TS_MERGE, "0" * 40)),
                  "original 394 integration")
    print("PASS: synthetic negative mutations of historical/current provenance, hashes, state, controllers and mandatory CI routing")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--historical", action="store_true")
    parser.add_argument("--current", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.historical:
        verify_historical(run_originals=True)
    if args.current:
        verify_current()
    if args.self_test:
        negative_tests()
    if not (args.historical or args.current or args.self_test):
        verify_historical(run_originals=True)
        verify_current()
        negative_tests()


if __name__ == "__main__":
    main()
