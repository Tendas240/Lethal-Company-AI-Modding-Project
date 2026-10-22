#!/usr/bin/env python3
"""Versioned current Residual-18 Offense V2 proof guard. Historical Residual-21 guard is immutable."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
INDEX="RuntimeEvidence/S1.42AK/20261022T103937Z/INDEX.json"
RAW="RuntimeEvidence/S1.42AK/20261022T103937Z/raw/LogOutput.log"
RECEIPT="Current/S1.42AK_OFFENSE_RANDOM_BATCH_V2_INGEST_V1.json"
RECORD="Current/S1.42AK_OFFENSE_RANDOM_BATCH_V2_GENERATION_PROOF_RECONCILIATION.md"
SHA="969044ab459387c3a509134c4c56a10ae1736b46af9fc76d3ac8cf01c25ec07d"
SIZE=10906072
FLOWS=("SubSysFlow","Spelunk_MagmaFlow","LeadFactory")
REMAINING=("Level3Flow","Black Mesa","CrimsonKeep","GoldenHotel","MelanieMuseum","shatteredrooms")
CI=(".github/workflows/knowledge-architecture.yml",
    ".github/workflows/s142ak-tsdiag1-source-static.yml",
    ".github/workflows/s142ak-scdiag1-source-static.yml")
PROOFS=(
    ("SubSysFlow","Sub Systems",1,58143079,12142,12144,12338,12352,(12593,12594,12595,12596),12600,12601),
    ("Spelunk_MagmaFlow","Spelunkers Caverns (Magmatic)",7,1918422,52624,52626,52705,52714,(52932,52933,52934,52935),52939,52940),
    ("LeadFactory","Lead Factory",10,59160378,74022,74024,74111,74123,(74326,74327,74328,74329),74333,74334),
)

def check(condition,why):
    if not condition: raise ValueError("RESIDUAL18_FAIL_CLOSED: "+why)

def js(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))

def check_state(state,index,receipt,build,active):
    phase=state["selected_scope"]["phase_c"]
    check((phase["residual_no_trusted_actual_generation_proof"],phase["residual_viable_equal_100"],phase["residual_owner_hard_block"])==(18,6,12),"exact residual")
    check(phase["v2_offense_generation_proof_reconciliation"]==RECORD and phase["v2_offense_generation_proof_index"]==INDEX,"V2 evidence links")
    check(phase["v2_offense_generation_proof_log_sha256"]==SHA and phase["v2_offense_generation_proof_log_size_bytes"]==SIZE,"raw original identity")
    check(phase["v2_offense_generation_proof_status"]=="PASS_3_NATURAL_OFFENSE_BASIC_GENERATION_MATERIALIZATION_ONLY_P0_PARTIAL_P1_PRELIMINARY","narrow proof tier")
    check(phase["v2_offense_generation_proof_flows"]==list(FLOWS) and phase["v2_offense_remaining_viable_generation_gaps"]==list(REMAINING),"exact 3+6 cohort")
    check(phase["subsysflow_historical_restricted_exception_superseded_for_offense_basic_generation_only"] is True,"SubSysFlow exact scope")
    check(state["next_action"]==state["selected_scope"]["next_action"] and "RESIDUAL 18 = 6" in state["next_action"] and "NOT COMPLETED" in state["next_action"],"navigation mirrors")
    check(state["selected_scope"]["scope_id"]=="UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY","scope")
    check(state["accepted_baseline"]["build_id"]=="S1.42AK" and state["active_candidate"]["build_id"]=="S1.42AK-BMDSFIX1" and state["active_candidate"]["status"]=="ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED" and state["runtime_test_outstanding"] is True,"baseline/candidate")
    check(state["controllers"]["runtime_active_build"]==active=="S1.42AK-BMDSFIX1","runtime controller")
    check(state["controllers"]["build_enabled"] is False and state["controllers"]["build_id"]=="IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS" and build["enabled"] is False and build["build_id"]=="IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS" and build["output_profile"]=="Profiles/DO_NOT_BUILD.r2z" and build["mod_additions"]==[] and build["mod_removals"]==[] and build["config_patches"]==[],"build disabled")
    check(index["build_id"]=="S1.42AK" and index["attribution"]["mode"]=="COMPLETED_S1_42AK_OFFENSE_RANDOM_BATCH_V2_NOT_RUNTIME_ACTIVATION" and index["attribution"]["original_profile_bytes_independently_verified"] is False,"index build and P0")
    check(len(index["files"])==1 and index["files"][0]["name"]=="LogOutput.log" and index["files"][0]["size"]==SIZE and index["files"][0]["sha256"]==SHA,"index original bytes")
    check(index["retention"]["no_automatic_deletion"] is True and index["retention"]["raw_original"]=="PRESERVE_UNTIL_SEPARATE_P0_P6_AND_RETENTION_DECISION","retention")
    check(receipt["status"]=="CONSUMED" and receipt["receipt"]["raw_path"]==RAW and receipt["receipt"]["evidence_index"]==INDEX and receipt["receipt"]["sha256"]==SHA and receipt["receipt"]["size"]==SIZE and receipt["receipt"]["original_profile_bytes_independently_verified"] is False,"receipt provenance")

def check_lines(lines):
    check(len(lines)==112894,"original lines count")
    def at(n,substring):check(substring in lines[n-1],"line "+str(n)+" expected "+substring)
    for flow,label,day,seed,pool,history,dungeon,floor,entrances,completed,tile in PROOFS:
        at(pool,"Final effective viable pool for Offense:")
        at(pool,label+"(100)")
        at(history,"Created New Day History Log! PlanetName: Offense ,"+label)
        at(history,"Day: "+str(day))
        at(dungeon,"Dungeon has finished generating on this client after multiple frames")
        at(floor,"Players finished generating the new floor")
        for n in entrances:
            at(n,"PathfindingLib")
            at(n," connects to ")
        at(completed,"Generation has completed with seed "+str(seed)+".")
        at(tile,"Preparing tile information for "+flow+" took ")
        check(pool<history<dungeon<floor<entrances[0]<entrances[-1]<completed<tile,"ordered event chain "+flow)
        local=lines[history-1:tile]
        check(not any("[BMDSFIX1] APPLIED" in line for line in local),"unexpected BMDSFIX1 "+flow)
        check(not any("Dungeon generation failed" in line or "NoMatchingDoorwayPlacementResult" in line for line in local),"generation error "+flow)
    at(12154,"ElevatorMod.Patches.ElevatorStartRoom")
    at(12328,"Ladder1_Mesh")
    at(53414,"Array index (0) is out of bounds (size=0)")
    at(9053,"DungeonFlow: LeadFactory has a null socket")
    at(74099,"RuntimeNavMeshBuilder: Source mesh Grates")

def check_workflows():
    for path in CI:
        body=(ROOT/path).read_text(encoding="utf-8")
        check("python AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py --historical" in body,"immutable history invocation "+path)
        for mode in ("current","self-test"):
            check("python AnalysisTools/validate_s142ak_residual18_lifecycle_v1.py --"+mode in body,"v2 state adapter "+path)
            check("python AnalysisTools/validate_s142ak_residual21_lifecycle_v1.py --"+mode not in body,"stale current gate "+path)
    body=(ROOT/CI[0]).read_text(encoding="utf-8")
    check("fetch-depth: 0" in body and "'AnalysisTools/**'" in body and "'Current/**'" in body,"CI preserved")
    for workflow, modes in (
        (".github/workflows/knowledge-architecture.yml",
         ("--historical-cross-diagnostic", "--historical-cross-diagnostic-self-test")),
        (".github/workflows/s142ak-tsdiag1-publication-lifecycle.yml",
         ("--historical-cross-diagnostic", "--historical-cross-diagnostic-self-test",
          "--historical-publication", "--historical-publication-self-test")),
    ):
        content = (ROOT / workflow).read_text(encoding="utf-8")
        for mode in modes:
            expected = "python AnalysisTools/validate_s142ak_residual18_lifecycle_v1.py " + mode
            check(expected in [line.strip() for line in content.splitlines()],
                  "historical frozen adapter invocation: " + workflow + " " + mode)
        check("python AnalysisTools/validate_s142ak_cross_diagnostic_frozen_provenance.py" not in content and
              "python AnalysisTools/validate_s142ak_tsdiag1_publication.py" not in content,
              "no historical validator may run on true V2 state: " + workflow)
    publication = (ROOT / ".github/workflows/s142ak-tsdiag1-publication-lifecycle.yml").read_text(encoding="utf-8")
    check("'AnalysisTools/validate_s142ak_residual18_lifecycle_v1.py'" in publication,
          "publication trigger must include versioned adapter")

def load():
    return js("Current/CURRENT_STATE.json"),js(INDEX),js(RECEIPT),js("BuildSpecs/current.json"),(ROOT/"RuntimeInbox/ACTIVE_BUILD.txt").read_text().strip()

def verified_raw():
    raw=(ROOT/RAW).read_bytes()
    check(len(raw)==SIZE and hashlib.sha256(raw).hexdigest()==SHA,"exact original raw SHA/size")
    return raw.decode("utf-8").splitlines()

def current():
    check_state(*load())
    lines=verified_raw();check_lines(lines)
    record=(ROOT/RECORD).read_text(encoding="utf-8")
    for token in (SHA,"10,906,072","P0 PARTIAL","P1 PRELIMINARY","SubSysFlow","Spelunk_MagmaFlow","LeadFactory","Ladder1_Mesh","Array index (0) is out of bounds","null doorway socket","18 = 6","12 unchanged owner-hard-block"):
        check(token in record,"source record qualification "+token)
    check_workflows()
    print("PASS: original V2 natural Offense 3/3 basic generation, residual 18=6+12, immutable controllers")

def fail_if_passes(fn,label):
    try:fn()
    except (ValueError,IndexError,AssertionError,KeyError,TypeError):return
    raise AssertionError("negative mutation passed: "+label)

def self_test():
    st,idx,rec,build,active=load()
    check_state(st,idx,rec,build,active)
    for key,value in (("residual_no_trusted_actual_generation_proof",21),("residual_viable_equal_100",9),("residual_owner_hard_block",11),("v2_offense_generation_proof_log_sha256","0"*64),("v2_offense_generation_proof_flows",[]),("v2_offense_remaining_viable_generation_gaps",[]),("subsysflow_historical_restricted_exception_superseded_for_offense_basic_generation_only",False)):
        bad=copy.deepcopy(st);bad["selected_scope"]["phase_c"][key]=value
        fail_if_passes(lambda b=bad:check_state(b,idx,rec,build,active),"state "+key)
    bad=copy.deepcopy(idx);bad["files"][0]["sha256"]="0"*64
    fail_if_passes(lambda:check_state(st,bad,rec,build,active),"index")
    bad=copy.deepcopy(rec);bad["status"]="PENDING"
    fail_if_passes(lambda:check_state(st,idx,bad,build,active),"receipt")
    bad=copy.deepcopy(build);bad["enabled"]=True
    fail_if_passes(lambda:check_state(st,idx,rec,bad,active),"build")
    fail_if_passes(lambda:check_state(st,idx,rec,build,"S1.42AK-TSDIAG1"),"runtime controller")
    lines=verified_raw();check_lines(lines)
    for entry in PROOFS:
        flow=entry[0];n=entry[-1];bad=list(lines);bad[n-1]=bad[n-1].replace(flow,"MISSING_FLOW")
        fail_if_passes(lambda b=bad:check_lines(b),"flow "+flow)
    check_workflows()
    print("PASS: exact current-18 negative mutation regression and protected original bytes")


# The actual V2 proof is mandatory. Only the three historical counters are
# projected in process memory, never persisted to the repository or original log.
FROZEN_ORIGINAL_VALIDATORS = {
    "cross": (
        "AnalysisTools/validate_s142ak_cross_diagnostic_frozen_provenance.py",
        "67ed414709dca5abb63f5573d2185cb5f0f10c8f",
    ),
    "publication": (
        "AnalysisTools/validate_s142ak_tsdiag1_publication.py",
        "d61f3818e301d2cafbe77bc028b1e95a653dd27a",
    ),
}
RESIDUAL_KEYS = (
    "residual_no_trusted_actual_generation_proof",
    "residual_viable_equal_100",
    "residual_owner_hard_block",
)


def historical_frozen_adapter(which, negative=False):
    check(which in FROZEN_ORIGINAL_VALIDATORS, "unknown frozen validator")
    # Validate real V2 18/6/12, exact 10,906,072 raw bytes and SHA, three
    # independently attributed Offense flows, receipt, retention, controllers,
    # untouched source records and ALL real-state negative tests FIRST.
    current()
    self_test()
    for source, expected_sha in FROZEN_ORIGINAL_VALIDATORS.values():
        tree_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD:" + source], cwd=ROOT, text=True
        ).strip()
        disk_sha = subprocess.check_output(
            ["git", "hash-object", str(ROOT / source)], cwd=ROOT, text=True
        ).strip()
        check(tree_sha == disk_sha == expected_sha, "frozen validator byte drift: " + source)

    state, _index, _receipt, _build, _active = load()
    phase = state["selected_scope"]["phase_c"]
    check(tuple(phase[key] for key in RESIDUAL_KEYS) == (18, 6, 12),
          "real V2 proof must precede historical state projection")
    check(phase["toy_store_tsdiag1_runtime_evidence_reconciled"] is True and
          phase["toy_store_tsdiag1_runtime_attempt_consumed"] is True and
          phase["toy_store_tsdiag1_runtime_armed"] is False and
          phase["toy_store_runtime_test_authorized"] is False,
          "historical TSDIAG1 completed provenance not frozen")

    historical = copy.deepcopy(state)
    projected = historical["selected_scope"]["phase_c"]
    for key, value in zip(RESIDUAL_KEYS, (21, 9, 12)):
        projected[key] = value
    check(tuple(projected[key] for key in RESIDUAL_KEYS) == (21, 9, 12),
          "historical memory-only projection mismatch")
    historical_json = json.dumps(historical)
    source = FROZEN_ORIGINAL_VALIDATORS[which][0]
    real_read_text = Path.read_text
    state_path = ROOT / "Current/CURRENT_STATE.json"

    def in_memory_state_read(self, *args, **kwargs):
        if self == state_path:
            return historical_json
        return real_read_text(self, *args, **kwargs)

    original_argv = sys.argv[:]
    try:
        # Exact original Python entry point: no skipped assertions or caught
        # validator failures. The Path override applies to this ONE JSON path.
        with patch.object(Path, "read_text", in_memory_state_read):
            sys.argv = [str(ROOT / source)] + (["--self-test"] if negative else [])
            runpy.run_path(str(ROOT / source), run_name="__main__")
    finally:
        sys.argv = original_argv
    print("PASS: V2 fail-closed then byte-identical frozen " + which +
          (" negative self-tests" if negative else " original gate"))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--current",action="store_true")
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--historical-cross-diagnostic",action="store_true")
    parser.add_argument("--historical-cross-diagnostic-self-test",action="store_true")
    parser.add_argument("--historical-publication",action="store_true")
    parser.add_argument("--historical-publication-self-test",action="store_true")
    opts=parser.parse_args()
    if sum(vars(opts).values()) != 1:
        parser.error("choose exactly one fail-closed validation mode")
    if opts.current: current()
    if opts.self_test: self_test()
    if opts.historical_cross_diagnostic: historical_frozen_adapter("cross")
    if opts.historical_cross_diagnostic_self_test: historical_frozen_adapter("cross", negative=True)
    if opts.historical_publication: historical_frozen_adapter("publication")
    if opts.historical_publication_self_test: historical_frozen_adapter("publication", negative=True)
