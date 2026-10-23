#!/usr/bin/env python3
"""Versioned fail-closed Residual-17 Mineshaft/Level3Flow Offense proof.

The exact integrated Residual-18 lifecycle/negative/frozen gates run in a
detached, full-history worktree at the immutable 18=6+12 main commit.
No old validator, raw evidence, owner gate, or controller is rewritten.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE18 = "1b56e567cda265b46d12e6806cc2fe7f4f83f2de"
BASE21 = "a5ae21ce9bad57a908ff5c3983d6c4e091d24e5b"
OLD = "AnalysisTools/validate_s142ak_residual18_lifecycle_v1.py"
RECORD = "Current/S1.42AK_MINESHAFT_LEVEL3FLOW_RESIDUAL17_BASIC_GENERATION_CANONIZATION_V1.md"
V1_RAW = "RuntimeEvidence/S1.42AK/20261020T213936Z/raw/LogOutput.log"
V1_INDEX = "RuntimeEvidence/S1.42AK/20261020T213936Z/INDEX.json"
V1_RECEIPT = "Current/S1.42AK_OFFENSE_MINESHAFT_ONE_SHOT_INGEST_V1.json"
V1_SHA = "7c7b02af7891b97b48078432ca8bf8d26d051a533cc15810d012950c44fac6c9"
V1_SIZE = 3173316
V2_SHA = "969044ab459387c3a509134c4c56a10ae1736b46af9fc76d3ac8cf01c25ec07d"
V2_REMAINING = ["Black Mesa", "CrimsonKeep", "GoldenHotel", "MelanieMuseum", "shatteredrooms"]
STATUS = "PASS_OFFENSE_BASIC_GENERATION_MATERIALIZATION_ONLY_P0_PARTIAL_P1_PRELIMINARY"
PINS = {
    OLD: "fb9aba2ae629b5e5182c7f25ead933ee89ef3a52",
    "AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py": "66f946de347b98931b6037057458ebfb416ebcf9",
    "AnalysisTools/validate_s142ak_cross_diagnostic_frozen_provenance.py": "67ed414709dca5abb63f5573d2185cb5f0f10c8f",
    "AnalysisTools/validate_s142ak_tsdiag1_publication.py": "d61f3818e301d2cafbe77bc028b1e95a653dd27a",
    V1_RAW: "993d692861a0ea3f295d6c6aaec7730460ce0cb5",
    V1_INDEX: "e78c430ad78373ca47a115c7c40f6d3e63a66013",
    V1_RECEIPT: "7b616a1be911d41840434774d562e325c46914f9",
    "Current/S1.42AK_MINESHAFT_LEVEL3FLOW_GENERATION_EVIDENCE_RECONCILIATION_V1.md": "ea5d165ab27011c5fb0edcf659c6095cbfbf0b2c",
    "Current/S1.42AK_MINESHAFT_USER_PROFILE_CONTINUITY_ATTESTATION_20261021.md": "e1a3bee796254f41f115532a1fb83c51399b89a6",
    "RuntimeEvidence/S1.42AK/20261022T103937Z/raw/LogOutput.log": "6cdaaf5ecf699297eae24566a82f3528d661ed3c",
    "RuntimeEvidence/S1.42AK/20261022T103937Z/INDEX.json": "4f200e98b46568124a7b5b1b680225833c61269c",
    "Current/S1.42AK_OFFENSE_RANDOM_BATCH_V2_INGEST_V1.json": "1f9636aa9f96e59179d1bd62a33a86c35a650eb8",
    "Current/S1.42AK_OFFENSE_RANDOM_BATCH_V2_GENERATION_PROOF_RECONCILIATION.md": "49bd321d685da9770fcb4b2368fb1bae3358c3e2",
    "BuildSpecs/current.json": "598bd4d374ca6560cf73e81dc128f067f335c2c4",
    "RuntimeInbox/ACTIVE_BUILD.txt": "a1e2869d9f78e7dee9098a6dba39c63d0a81817c",
}
CI_MODES = {
    ".github/workflows/knowledge-architecture.yml": (
        "historical-cross-diagnostic", "historical-cross-diagnostic-self-test", "current", "self-test"),
    ".github/workflows/s142ak-tsdiag1-source-static.yml": ("current", "self-test"),
    ".github/workflows/s142ak-scdiag1-source-static.yml": ("current", "self-test"),
    ".github/workflows/s142ak-tsdiag1-publication-lifecycle.yml": (
        "historical-cross-diagnostic", "historical-cross-diagnostic-self-test",
        "historical-publication", "historical-publication-self-test"),
}
EDGE_LINES = {
    12787: ("EntranceTeleportA (EntranceTeleport) (248)",
            "EntranceTeleportA(Clone) (EntranceTeleport) (312)"),
    12788: ("EntranceTeleportB (EntranceTeleport) (249)",
            "EntranceTeleportB(Clone) (EntranceTeleport) (308)"),
    12789: ("EntranceTeleportB(Clone) (EntranceTeleport) (308)",
            "EntranceTeleportB (EntranceTeleport) (249)"),
    12790: ("EntranceTeleportA(Clone) (EntranceTeleport) (312)",
            "EntranceTeleportA (EntranceTeleport) (248)"),
}
ERRORS = ("[BMDSFIX1] APPLIED", "Dungeon generation failed",
          "NoMatchingDoorwayPlacementResult")


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError("RESIDUAL17_FAIL_CLOSED: " + reason)


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def check_pins() -> None:
    require(subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE18, "HEAD"], cwd=ROOT,
        check=False).returncode == 0, "18 main not ancestor")
    for path, pinned in PINS.items():
        require(git("rev-parse", "HEAD:" + path) == pinned, "HEAD Git-object drift " + path)
        require(git("hash-object", str(ROOT / path)) == pinned, "working bytes drift " + path)
    require(git("rev-parse", BASE18 + ":" + OLD) == PINS[OLD],
            "authentic 18 baseline adapter mismatch")


def verify_raw_bytes(raw: bytes) -> None:
    require(len(raw) == V1_SIZE and hashlib.sha256(raw).hexdigest() == V1_SHA,
            "original Mineshaft raw size / SHA-256")


def check_lines(lines: list[str]) -> None:
    require(len(lines) == 31886, "original V1 line count")

    def at(n: int, *needles: str) -> None:
        require(all(token in lines[n - 1] for token in needles), "log line " + str(n))

    for n in (12241, 12260):
        at(n, "Final effective viable pool for Offense:")
        require(re.search(r"(?:^|, )Mineshaft\(100\)(?:,|$)", lines[n - 1]) is not None,
                "exact standalone Mineshaft rarity 100, not Expanded Mineshaft: " + str(n))
    at(12262, "Created New Day History Log!", "PlanetName: Offense ,Mineshaft",
       "Day: 1")
    at(12527, "Dungeon has finished generating on this client after multiple frames")
    at(12537, "Players finished generating the new floor")
    edge_pattern = re.compile(r"PathfindingLib\] (.+? \(EntranceTeleport\) \(\d+\)) connects to "
                              r"(.+? \(EntranceTeleport\) \(\d+\))")
    found = []
    for n, expected in EDGE_LINES.items():
        match = edge_pattern.search(lines[n - 1])
        require(match is not None and match.groups() == expected, "entrance " + str(n))
        found.append(match.groups())
    require(len(set(found)) == 4 and all((dst, src) in found for src, dst in found),
            "two exact bidirectional entrance pairs")
    at(12794, "CullFactory", "Generation has completed with seed 43291983.")
    at(12795, "CullFactory", "Preparing tile information for Level3Flow took ")
    require(12241 < 12260 < 12262 < 12527 < 12537 < 12787 < 12790 < 12794 < 12795,
            "event chronology")
    local = lines[12262 - 1:12795]
    require(not any(token in line for line in local for token in ERRORS),
            "local generation negative controls")


def check_state(state: dict, index: dict, receipt: dict, build: dict, active: str) -> None:
    scope = state["selected_scope"]
    p = scope["phase_c"]
    require(scope["scope_id"] == "UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY"
            and scope["status"] == "PHASE_C_RESIDUAL_17_S142AK_MINESHAFT_V1_BASIC_GENERATION_PROOF_RECONCILED",
            "scope/status")
    require((p["residual_no_trusted_actual_generation_proof"],
             p["residual_viable_equal_100"], p["residual_owner_hard_block"]) == (17, 5, 12),
            "exact residual 17=5+12")
    require(p["v2_offense_generation_proof_flows"] == [
        "SubSysFlow", "Spelunk_MagmaFlow", "LeadFactory"]
        and p["v2_offense_remaining_viable_generation_gaps"] == V2_REMAINING
        and p["v2_offense_generation_proof_log_sha256"] == V2_SHA
        and p["v2_offense_generation_proof_log_size_bytes"] == 10906072
        and p["v2_offense_generation_proof_status"] ==
        "PASS_3_NATURAL_OFFENSE_BASIC_GENERATION_MATERIALIZATION_ONLY_P0_PARTIAL_P1_PRELIMINARY"
        and p["subsysflow_historical_restricted_exception_superseded_for_offense_basic_generation_only"] is True,
        "untouched three V2 proofs and reduced gap list")
    require(p["mineshaft_offense_generation_proof_status"] == STATUS
            and p["mineshaft_offense_generation_proof_reconciliation"] == RECORD
            and p["mineshaft_offense_generation_proof_index"] == V1_INDEX
            and p["mineshaft_offense_generation_proof_log_sha256"] == V1_SHA
            and p["mineshaft_offense_generation_proof_log_size_bytes"] == V1_SIZE
            and p["mineshaft_offense_generation_proof_flow"] == "Level3Flow"
            and p["mineshaft_offense_generation_proof_profile_byte_independently_verified"] is False,
            "Mineshaft narrow proof fields")
    require(state["next_action"] == scope["next_action"]
            and "RESIDUAL 17 = 5" in state["next_action"]
            and "NOT COMPLETED" in state["next_action"]
            and "P0 PARTIAL / P1 PRELIMINARY" in state["next_action"]
            and "12 UNCHANGED OWNER" in state["next_action"],
            "navigation mirrors and proof limits")
    require(state["accepted_baseline"]["build_id"] == "S1.42AK"
            and state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1"
            and state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
            and state["runtime_test_outstanding"] is True
            and state["controllers"]["runtime_active_build"] == active == "S1.42AK-BMDSFIX1"
            and state["controllers"]["build_enabled"] is False
            and build["enabled"] is False
            and build["build_id"] == state["controllers"]["build_id"] ==
            "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS"
            and build["output_profile"] == "Profiles/DO_NOT_BUILD.r2z"
            and build["mod_additions"] == build["mod_removals"] == build["config_patches"] == [],
            "accepted/runtime/build controllers")
    require(index["build_id"] == "S1.42AK"
            and index["attribution"]["mode"] == "COMPLETED_S1_42AK_ONE_SHOT_NOT_RUNTIME_ACTIVATION"
            and index["attribution"]["original_profile_bytes_independently_verified"] is False
            and len(index["files"]) == 1
            and index["files"][0]["name"] == "LogOutput.log"
            and index["files"][0]["sha256"] == V1_SHA
            and index["files"][0]["size"] == V1_SIZE
            and index["analysis"][0]["stats"]["line_count"] == 31886,
            "V1 original INDEX")
    require(receipt["status"] == "CONSUMED"
            and receipt["receipt"]["raw_path"] == V1_RAW
            and receipt["receipt"]["evidence_index"] == V1_INDEX
            and receipt["receipt"]["size"] == V1_SIZE
            and receipt["receipt"]["sha256"] == V1_SHA
            and receipt["receipt"]["original_profile_bytes_independently_verified"] is False,
            "V1 receipt/provenance")
    require(p["v2_offense_generation_proof_index"] ==
            "RuntimeEvidence/S1.42AK/20261022T103937Z/INDEX.json",
            "V2 original index link")


def check_workflow_contents(contents: dict[str, str]) -> None:
    for path, modes in CI_MODES.items():
        body = contents[path]
        commands = [line.strip().removeprefix("run: ").strip()
                    for line in body.splitlines()]
        for mode in modes:
            cmd = "python AnalysisTools/validate_s142ak_residual17_lifecycle_v1.py --" + mode
            require(cmd in commands, "new fail-closed workflow invocation " + path + " " + mode)
        require("python AnalysisTools/validate_s142ak_residual18_lifecycle_v1.py" not in body,
                "current workflow may not execute 18 directly " + path)
    for path in list(CI_MODES)[:3]:
        require("python AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py --historical"
                in contents[path], "real residual-21 historical invocation " + path)
    require("fetch-depth: 0" in contents[".github/workflows/knowledge-architecture.yml"]
            and "'AnalysisTools/**'" in contents[".github/workflows/knowledge-architecture.yml"]
            and "'Current/**'" in contents[".github/workflows/knowledge-architecture.yml"],
            "full-history and source triggers")
    require("'AnalysisTools/validate_s142ak_residual17_lifecycle_v1.py'"
            in contents[".github/workflows/s142ak-tsdiag1-publication-lifecycle.yml"],
            "publication new adapter trigger")
    require("fetch-depth: 0" in contents[".github/workflows/s142ak-tsdiag1-publication-lifecycle.yml"],
            "historical publication CI needs complete Git objects")
    for path in (".github/workflows/s142ak-tsdiag1-source-static.yml",
                 ".github/workflows/s142ak-scdiag1-source-static.yml"):
        require("'AnalysisTools/validate_s142ak_residual17_lifecycle_v1.py'" in contents[path],
                "source CI new adapter trigger " + path)


def check_current() -> tuple[dict, dict, dict, dict, str, list[str]]:
    check_pins()
    state, index, receipt = load_json("Current/CURRENT_STATE.json"), load_json(V1_INDEX), load_json(V1_RECEIPT)
    build = load_json("BuildSpecs/current.json")
    active = (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()
    check_state(state, index, receipt, build, active)
    raw = (ROOT / V1_RAW).read_bytes()
    verify_raw_bytes(raw)
    lines = raw.decode("utf-8").splitlines()
    check_lines(lines)
    record = (ROOT / RECORD).read_text(encoding="utf-8")
    for token in (V1_SHA, "3,173,316", "31,886", "12787", "12790", "12527",
                  "43291983", "Level3Flow", "P0 PARTIAL", "P1 PRELIMINARY",
                  "17 = 5 + 12", "PRESERVE_UNTIL_SEPARATE_P0_P6_AND_RETENTION_DECISION",
                  "TRUSTED_PROOF_NOT_YET_CANONIZED"):
        require(token in record, "canonical record missing qualification " + token)
    contents = {path: (ROOT / path).read_text(encoding="utf-8") for path in CI_MODES}
    check_workflow_contents(contents)
    return state, index, receipt, build, active, lines


def reject(callback, label: str) -> None:
    try:
        callback()
    except (ValueError, IndexError, AssertionError, KeyError, TypeError):
        return
    raise AssertionError("negative mutation unexpectedly passed: " + label)


def self_test() -> None:
    state, index, receipt, build, active, lines = check_current()
    for key, bad_value in (
        ("residual_no_trusted_actual_generation_proof", 18),
        ("residual_viable_equal_100", 6),
        ("residual_owner_hard_block", 11),
        ("v2_offense_generation_proof_flows", []),
        ("v2_offense_remaining_viable_generation_gaps", ["Level3Flow"] + V2_REMAINING),
        ("mineshaft_offense_generation_proof_log_sha256", "0" * 64),
        ("mineshaft_offense_generation_proof_status", "UNPROVEN"),
        ("mineshaft_offense_generation_proof_profile_byte_independently_verified", True),
    ):
        bad = copy.deepcopy(state)
        bad["selected_scope"]["phase_c"][key] = bad_value
        reject(lambda b=bad: check_state(b, index, receipt, build, active),
               "machine " + key)
    bad = copy.deepcopy(state)
    bad["next_action"] = "MUTATED"
    reject(lambda: check_state(bad, index, receipt, build, active), "navigation")
    bad = copy.deepcopy(index)
    bad["files"][0]["sha256"] = "0" * 64
    reject(lambda: check_state(state, bad, receipt, build, active), "V1 INDEX hash")
    bad = copy.deepcopy(receipt)
    bad["status"] = "PENDING"
    reject(lambda: check_state(state, index, bad, build, active), "V1 receipt status")
    bad = copy.deepcopy(build)
    bad["enabled"] = True
    reject(lambda: check_state(state, index, receipt, bad, active), "build activation")
    reject(lambda: check_state(state, index, receipt, build, "S1.42AK-TSDIAG1"),
           "runtime activation")
    raw = (ROOT / V1_RAW).read_bytes()
    reject(lambda: verify_raw_bytes(raw[:-1]), "V1 truncation")
    mutated = bytearray(raw)
    mutated[123] ^= 1
    reject(lambda: verify_raw_bytes(bytes(mutated)), "V1 raw byte corruption")
    for n, before, after in (
        (12241, ", Mineshaft(100)", ", Mineshaft(0)"),
        (12260, ", Mineshaft(100)", ", Mineshaft(0)"),
        (12262, "PlanetName: Offense", "PlanetName: Black Mesa"),
        (12262, "Day: 1", "Day: 2"),
        (12527, "Dungeon has finished generating", "Dungeon has NOT finished generating"),
        (12537, "Players finished generating", "Players never finished generating"),
        (12787, "EntranceTeleportA(Clone)", "EntranceTeleportB(Clone)"),
        (12789, "EntranceTeleportB(Clone)", "EntranceTeleportA(Clone)"),
        (12794, "43291983", "0"),
        (12795, "Level3Flow", "WrongFlow"),
    ):
        altered = list(lines)
        require(before in altered[n - 1], "negative fixture initial token " + str(n))
        altered[n - 1] = altered[n - 1].replace(before, after, 1)
        reject(lambda a=altered: check_lines(a), "V1 event mutation " + str(n))
    for token in ERRORS:
        altered = list(lines)
        altered[12530 - 1] = token
        reject(lambda a=altered: check_lines(a), "negative generation " + token)
    contents = {path: (ROOT / path).read_text(encoding="utf-8") for path in CI_MODES}
    for path, modes in CI_MODES.items():
        changed = dict(contents)
        changed[path] = changed[path].replace(
            "python AnalysisTools/validate_s142ak_residual17_lifecycle_v1.py --" + modes[0],
            "echo SKIPPED", 1)
        reject(lambda b=changed: check_workflow_contents(b), "CI route " + path)
    print("PASS: Residual-17 original-byte, event, state, workflow negative mutations")


def historical_18(*modes: str) -> None:
    check_current()
    with tempfile.TemporaryDirectory(prefix="mineshaft-residual18-original-") as tmp:
        checkout = Path(tmp) / "historical"
        subprocess.run(["git", "worktree", "add", "--detach", str(checkout), BASE18],
                       cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout,
                                            text=True).strip() == BASE18,
                    "historical checkout not exact Residual-18 main")
            for mode in modes:
                result = subprocess.run(
                    [sys.executable, str(checkout / OLD), "--" + mode],
                    cwd=checkout, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    check=False)
                require(result.returncode == 0, "original Residual-18 --" + mode +
                        " failed: " + result.stdout[-3000:])
                print("PASS: authentic original Residual-18 --" + mode)
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(checkout)],
                           cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def historical_21_negatives() -> None:
    """Execute the original Residual-21 CURRENT and negative self-tests on real historic 21=9+12."""
    check_current()
    require(git("rev-parse", BASE21 + ":AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py") ==
            PINS["AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py"],
            "historical 21 exact validator blob")
    with tempfile.TemporaryDirectory(prefix="mineshaft-residual21-original-") as tmp:
        checkout = Path(tmp) / "historical"
        subprocess.run(["git", "worktree", "add", "--detach", str(checkout), BASE21],
                       cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            require(subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout,
                                            text=True).strip() == BASE21,
                    "historical residual-21 checkout mismatch")
            for mode in ("current", "self-test"):
                result = subprocess.run(
                    [sys.executable, str(checkout / "AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py"), "--" + mode],
                    cwd=checkout, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    check=False)
                require(result.returncode == 0, "authentic Residual-21 --" + mode +
                        " failed: " + result.stdout[-3000:])
                print("PASS: authentic original Residual-21 --" + mode)
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(checkout)],
                           cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> None:
    parser = argparse.ArgumentParser()
    for opt in ("current", "self-test", "historical-cross-diagnostic",
                "historical-cross-diagnostic-self-test", "historical-publication",
                "historical-publication-self-test"):
        parser.add_argument("--" + opt, action="store_true")
    args = parser.parse_args()
    modes = [name for name, active in vars(args).items() if active]
    if len(modes) != 1:
        parser.error("choose one exact fail-closed validation mode")
    mode = modes[0].replace("_", "-")
    if mode == "current":
        check_current()
        historical_18("current")
        print("PASS: current 17=5+12 with independently executed historical V2 original")
    elif mode == "self-test":
        self_test()
        historical_18("self-test")
        historical_21_negatives()
    else:
        historical_18(mode)


if __name__ == "__main__":
    main()
