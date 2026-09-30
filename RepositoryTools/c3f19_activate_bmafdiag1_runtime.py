#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BUILD_ID="S1.42AK-BMAFDIAG1"
PROFILE_NAME="LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic"
PROFILE="Profiles/LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic.r2z"
PROFILE_SHA="b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2"
DLL_SHA="c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1"
LLL_SHA="b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA="901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
BASE_ID="S1.42AK"
BASE_PROFILE="Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z"
BASE_SHA="b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
CANDIDATE_ID="S1.42AK-BMDSFIX1"
CANDIDATE_PROFILE="Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
CANDIDATE_SHA="3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
BUILD_PLAN="BuildSpecs/S1.42AK-BMAFDIAG1_PLAN.md"
BUILD_RESULT="BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC="BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
PUBLICATION="BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
PROFILE_SOURCES="ProfileSources/S1.42AK-BMAFDIAG1/"
FILE_INDEX=PROFILE_SOURCES+"FILE_INDEX.json"
PROFILE_INDEX=PROFILE_SOURCES+"PROFILE_INDEX_RESULT.json"
ACTIVATION="Current/211_S1.42AK_BMAFDIAG1_RUNTIME_ACTIVATION.md"

def req(c,m):
    if not c: raise RuntimeError(m)
def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))
def write(rel,obj):
    (ROOT/rel).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def sha(rel):
    h=hashlib.sha256()
    with (ROOT/rel).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

state=load("Current/CURRENT_STATE.json")
req(state["selected_scope"]["status"]=="PHASE_C3_BMAFDIAG1_PROFILE_INDEX_COMPLETE_RUNTIME_ACTIVATION_NEXT_BMDSFIX1_TARGET_PASSIVE_OUTSTANDING","pre-activation lifecycle drift")
req(state["accepted_baseline"]["build_id"]==BASE_ID and state["accepted_baseline"]["profile"]==BASE_PROFILE and state["accepted_baseline"]["sha256"]==BASE_SHA,"accepted baseline drift")
req(state["active_candidate"]["build_id"]==CANDIDATE_ID and state["active_candidate"]["sha256"]==CANDIDATE_SHA,"candidate drift")
req(state["latest_built_artifact"]["build_id"]==CANDIDATE_ID and state["latest_built_artifact"]["sha256"]==CANDIDATE_SHA,"latest artifact drift")
req(state["controllers"]["runtime_active_build"]==CANDIDATE_ID,"runtime controller pre-state drift")
req((ROOT/"RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()==CANDIDATE_ID,"ACTIVE_BUILD pre-state drift")
req(state["runtime_test_outstanding"] is True,"BMDS passive gate must stay outstanding")

current=load("BuildSpecs/current.json")
req(current["enabled"] is False and current["build_id"]=="IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS","build controller drift")
req(current["base_profile"]==CANDIDATE_PROFILE and current["base_sha256"]==CANDIDATE_SHA,"build controller base drift")
auto=load("Current/AUTO_BUILD_RESULT.json")
req(auto["build_id"]==CANDIDATE_ID and auto["output_sha256"]==CANDIDATE_SHA,"AUTO_BUILD_RESULT drift")

old=state["selected_scope"].get("diagnostic_revision",{})
req(old.get("build_id")=="S1.42AK-BMGHDIAG3" and old.get("runtime_armed") is False,"completed BMGHDIAG3 diagnostic revision drift")
req(old.get("runtime_validation_status")=="RUNTIME_COMPATIBILITY_PASS_NEVER_ACCEPT","BMGHDIAG3 completion status drift")

req(sha(PROFILE)==PROFILE_SHA,"published BMAFDIAG1 profile SHA mismatch")
review=load("BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json")
req(review["review_artifact_id"]==11106178288 and review["profile_sha256"]==PROFILE_SHA and review["diagnostic_dll_sha256"]==DLL_SHA,"review authority drift")
req(review["archive_members_verified"]==337 and review["config_changes"]==1 and review["package_changes"]==0,"review archive/config drift")

build=load(BUILD_RESULT)
req(build["build_id"]==BUILD_ID and build["profile_name"]==PROFILE_NAME,"build-result identity drift")
req(build["base_profile"]==BASE_PROFILE and build["base_sha256"]==BASE_SHA,"build-result base drift")
req(build["output_profile"]==PROFILE and build["output_sha256"]==PROFILE_SHA,"build-result output drift")
req(build["zip_members"]==337,"build-result member count drift")
req(build["changed_existing_members"]==["BepInEx/config/LethalLevelLoader.cfg","export.r2x"],"build-result changed members drift")
req(build["added_members"]==["BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll"],"build-result added member drift")

static=load(STATIC)
req(static["output_sha256"]==PROFILE_SHA and static["diagnostic_dll_sha256"]==DLL_SHA,"static verification identity drift")
req(static["published"] is True and static["indexed"] is True and static["runtime_armed"] is False,"static verification lifecycle drift")
req(static["foundry_manual_level_names_delta"]=="Black Mesa:100" and static["foundry_owner_values_preserved"] is True,"Foundry config authority drift")

idx=load(PROFILE_INDEX)
req(idx["build_id"]==BUILD_ID and idx["profile_path"]==PROFILE and idx["sha256"]==PROFILE_SHA,"profile index identity drift")
req(idx["zip_members"]==337 and idx["snapshot"]["entries"]==337 and idx["snapshot"]["text_entries"]==331 and idx["build_id_resolution"]=="EXPECTED_HASHES","profile index contract drift")

expected=load("Profiles/EXPECTED_HASHES.json")
entry=expected.get(PROFILE)
req(entry is not None and entry["build_id"]==BUILD_ID and entry["sha256"]==PROFILE_SHA,"EXPECTED_HASHES drift")
req("not runtime-armed by indexing" in entry["note"],"EXPECTED_HASHES pre-state note drift")

diag={
 "build_id":BUILD_ID,
 "status":"PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
 "classification":"DIAGNOSTIC_ONLY_NEVER_ACCEPT",
 "base_build_id":BASE_ID,
 "base_profile":BASE_PROFILE,
 "base_sha256":BASE_SHA,
 "profile_name":PROFILE_NAME,
 "profile":PROFILE,
 "profile_sources":PROFILE_SOURCES,
 "file_index":FILE_INDEX,
 "profile_index_result":PROFILE_INDEX,
 "profile_sha256":PROFILE_SHA,
 "sha256":PROFILE_SHA,
 "diagnostic_dll_sha256":DLL_SHA,
 "lll_sha256":LLL_SHA,
 "normalizer_sha256":NORMALIZER_SHA,
 "archive_members_verified":337,
 "changed_existing_members":["BepInEx/config/LethalLevelLoader.cfg","export.r2x"],
 "added_members":["BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll"],
 "removed_members":[],
 "package_changes":0,
 "config_changes":1,
 "build_plan":BUILD_PLAN,
 "build_result":BUILD_RESULT,
 "static_evidence":STATIC,
 "publication_evidence":PUBLICATION,
 "source_reconciliation":"Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md",
 "review_checkpoint":"Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md",
 "publication_checkpoint":"Current/209_S1.42AK_BMAFDIAG1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md",
 "profile_index_reconciliation":"Current/210_S1.42AK_BMAFDIAG1_PROFILE_INDEX_RECONCILIATION.md",
 "published":True,
 "indexed":True,
 "runtime_armed":True,
 "activation_record":ACTIVATION,
 "runtime_role":"DIAGNOSTIC_ONLY_BLACK_MESA_ABANDONED_FOUNDRY_FORCE_SELECTION_AND_READ_ONLY_ENTRANCE_OBSERVATION_NEVER_ACCEPT",
 "runtime_validation_status":"RUNTIME_TEST_OUTSTANDING_NEVER_ACCEPT"
}

scope=state["selected_scope"]
scope["diagnostic_revision"]=diag
scope["diagnostic_build_plan"]=BUILD_PLAN
scope["diagnostic_static_evidence"]=STATIC
scope["diagnostic_publication_evidence"]=PUBLICATION
scope["diagnostic_runtime_activation"]=ACTIVATION
scope["status"]="PHASE_C3_BMAFDIAG1_RUNTIME_ACTIVE_TEST_OUTSTANDING_BMDSFIX1_TARGET_PASSIVE_OUTSTANDING"
scope["finding"]="Exact S1.42AK-BMAFDIAG1 reviewed bytes are published, canonically indexed and now runtime-armed solely as the bounded Black Mesa x Abandoned Foundry diagnostic target. The active diagnostic profile remains SHA-256 "+PROFILE_SHA+" and its DLL remains SHA-256 "+DLL_SHA+". It derives directly from exact accepted S1.42AK. The owner-default Abandoned Foundry LLL content-configuration delta is already frozen in those exact bytes: Enable Content Configuration=true plus exactly Black Mesa:100 while all other owner values remain preserved. S1.42AK-BMDSFIX1 remains the separate active gameplay candidate / not accepted and its regular Black Mesa x DeepSewersFlow gate remains outstanding, unwaived and passive. BuildSpecs/current.json and AUTO_BUILD_RESULT remain BMDSFIX1; RuntimeInbox/ACTIVE_BUILD.txt now identifies BMAFDIAG1 only for exact Gale target resolution and runtime-evidence attribution. Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN until runtime evidence is ingested and decided."
scope["analysis_contract"]="Treat S1.42AK-BMAFDIAG1 as the active diagnostic runtime target only and NEVER ACCEPT it as gameplay. Preserve exact profile/DLL identities, accepted S1.42AK, the separate unaccepted S1.42AK-BMDSFIX1 gameplay candidate, the passive/unwaived BMDSFIX1 Black Mesa x DeepSewersFlow gate, accepted S1.42AB normalization, the exact owner-default Foundry availability delta, historical Phase-B3, the Oxyde ordinary-generation exception, Shatteredrooms exclusions and the separate Black Mesa/Pikmin routing closure. Do not rebuild or mutate the diagnostic profile/DLL/package/config bytes. The runtime gate must establish BMAFDIAG1 arming, pre-reduction viable exact FoundryFlow at normalized rarity 100, exact singleton selection, completed generation, IDs 0..3 topology/traversal evidence and no invalidating REFUSED/TOPOLOGY_INCONCLUSIVE/TRAVERSAL_INCONCLUSIVE/OBSERVER_INCONCLUSIVE marker before any pair-compatibility conclusion."
next_action="Import the exact active S1.42AK-BMAFDIAG1 profile through the canonical repository-driven Gale v2.4.3 launcher, run one bounded Black Mesa x Abandoned Foundry diagnostic, exercise the main entrance and alternate entrance IDs 1, 2 and 3 in both directions where practical, then upload that run's exact BepInEx/LogOutput.log with the BMAFDIAG1 build-specific standalone PowerShell uploader. Do not alter profile/config/package/plugin/gameplay bytes during the test. Treat the result as diagnostic-only / NEVER ACCEPT; do not accept BMDSFIX1 or waive its passive Black Mesa x DeepSewersFlow gate."
scope["next_action"]=next_action

pc=scope["phase_c"]
pc["bmafdiag1_source_static_status"]="SOURCE_STATIC_PASS_MAIN_INTEGRATED_REVIEW_BUILD_PASS_EXACT_BYTES_PUBLISHED_INDEXED_RUNTIME_ACTIVE_TEST_OUTSTANDING"
pc["black_mesa_abandoned_foundry_status"]="NOT_YET_PROVEN_RUNTIME_DIAGNOSTIC_ACTIVE_TEST_OUTSTANDING"
pc["bmafdiag1_review_status"]="INACTIVE_REVIEW_BUILD_PASS_EXACT_BYTES_PUBLISHED_INDEXED_RUNTIME_ACTIVE_TEST_OUTSTANDING"
pc["bmafdiag1_review_published"]=True
pc["bmafdiag1_review_runtime_armed"]=True
pc["bmafdiag1_publication_checkpoint"]="Current/209_S1.42AK_BMAFDIAG1_EXACT_BYTE_PUBLICATION_CHECKPOINT.md"
pc["bmafdiag1_publication_evidence"]=PUBLICATION
pc["bmafdiag1_publication_status"]="EXACT_BYTE_PUBLISHED_MAIN_INTEGRATED_INDEXED_RUNTIME_ACTIVE_TEST_OUTSTANDING"
pc["bmafdiag1_publication_transport_run"]=36746508778
pc["bmafdiag1_published_profile_commit"]="85bd206a978e7b4bb244e2346590df7d19e6aa24"
pc["bmafdiag1_publication_integration_pr"]=201
pc["bmafdiag1_publication_pr_head"]="3dea5e96ea7a4826f106967c0660c830c589f733"
pc["bmafdiag1_publication_pr_knowledge_architecture_run"]=36747088770
pc["bmafdiag1_publication_main_integration_commit"]="7dc653a68603db87ee70c8c2d29f6b48175eecd5"
pc["bmafdiag1_publication_main_knowledge_architecture_run"]=36747792210
pc["bmafdiag1_profile_index_reconciliation"]="Current/210_S1.42AK_BMAFDIAG1_PROFILE_INDEX_RECONCILIATION.md"
pc["bmafdiag1_profile_indexed"]=True
pc["bmafdiag1_profile_index_result"]=PROFILE_INDEX
pc["bmafdiag1_profile_index_mapping_pr"]=202
pc["bmafdiag1_profile_index_mapping_head"]="f37d60aed62eb349d50bca987a1f0fbbca5ab62e"
pc["bmafdiag1_profile_index_mapping_merge_commit"]="1b65fe1e5656fc6905139268e9fc227c60d5148e"
pc["bmafdiag1_profile_index_workflow_run"]=36775289721
pc["bmafdiag1_profile_index_commit"]="d7688604c3917ea96fb6597ae5dfc718e5fd0f15"
pc["bmafdiag1_profile_index_exact_head_validation_run"]=36775324389
pc["bmafdiag1_runtime_activation"]=ACTIVATION
pc["bmafdiag1_runtime_activation_status"]="ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_TEST_OUTSTANDING_NEVER_ACCEPT"

state["updated"]="2026-09-30"
state["runtime_test_outstanding"]=True
state["controllers"]["runtime_active_build"]=BUILD_ID
state["next_action"]=next_action
write("Current/CURRENT_STATE.json",state)
(ROOT/"RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID+"\n",encoding="utf-8")

entry["note"]="Diagnostic-only active runtime target directly over accepted S1.42AK; exact reviewed bytes are published/indexed and the canonical readable snapshot is ProfileSources/S1.42AK-BMAFDIAG1/. NEVER ACCEPT and never use as a gameplay base; runtime activation authorizes only bounded Black Mesa x Abandoned Foundry diagnostic evidence collection."
write("Profiles/EXPECTED_HASHES.json",expected)

integrity=load("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
req(not any(x.get("build_id")==BUILD_ID for x in integrity.get("profiles",[])),"BMAFDIAG1 unexpectedly completed")
req(not any(x.get("build_id")==BUILD_ID for x in integrity.get("pending_profiles",[])),"BMAFDIAG1 unexpectedly pending")
integrity["updated"]="2026-09-30"
integrity["last_validated"]="2026-09-30"
integrity["pending_profiles"].append({
 "build_id":BUILD_ID,
 "role":"ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
 "profile":PROFILE,
 "profile_sha256":PROFILE_SHA,
 "profile_sources":PROFILE_SOURCES,
 "file_index":FILE_INDEX,
 "export":PROFILE_SOURCES+"export.r2x",
 "build_plan":BUILD_PLAN,
 "build_result":BUILD_RESULT,
 "static_evidence":STATIC,
 "publication_evidence":PUBLICATION,
 "activation_record":ACTIVATION,
 "diagnostic_dll_sha256":DLL_SHA,
 "runtime_evidence_required":False,
 "partial_runtime_evidence_present":False,
 "note":"Exact published/indexed BMAFDIAG1 bytes are runtime-armed solely for bounded Black Mesa x Abandoned Foundry diagnostic qualification. Diagnostic only / NEVER ACCEPT; BMDSFIX1 and its passive Deep Sewers gate are unchanged."
})
integrity.setdefault("verified_repository_api_observations",[]).append("S1.42AK-BMAFDIAG1 exact published/indexed profile SHA-256 "+PROFILE_SHA+" is runtime-armed only as a direct diagnostic over accepted S1.42AK; it remains NEVER ACCEPT and Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN pending runtime evidence.")
write("Current/ARTIFACT_EVIDENCE_INTEGRITY.json",integrity)
print("PASS: staged exact BMAFDIAG1 runtime authority transition")
