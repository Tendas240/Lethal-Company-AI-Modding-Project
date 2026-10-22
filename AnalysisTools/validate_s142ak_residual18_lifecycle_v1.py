#!/usr/bin/env python3
"""Versioned current Residual-18 Offense V2 proof guard. Historical Residual-21 guard is immutable."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

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

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--current",action="store_true");parser.add_argument("--self-test",action="store_true")
    opts=parser.parse_args()
    if not(opts.current or opts.self_test):parser.error("choose --current or --self-test")
    if opts.current:current()
    if opts.self_test:self_test()
