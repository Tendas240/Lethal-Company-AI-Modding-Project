#!/usr/bin/env python3
"""Pure static exact-byte SCDIAG1 activation/routing validation. Never builds or runs the game."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
def j(p): return json.loads((ROOT / p).read_text(encoding="utf-8"))
def must(ok, why):
    if not ok: raise RuntimeError("SCDIAG1 activation refused: " + why)
def hash_bytes(b): return hashlib.sha256(b).hexdigest()
def h(p): return hash_bytes((ROOT / p).read_bytes())
s=j("Current/CURRENT_STATE.json")
p=s["selected_scope"]["phase_c"]
d=s["selected_scope"]["diagnostic_revision"]
r=j("BuildSpecs/S1.42AK-SCDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json")
review=j("BuildSpecs/S1.42AK-SCDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json")
idx=j("ProfileSources/S1.42AK-SCDIAG1/PROFILE_INDEX_RESULT.json")
members=j("ProfileSources/S1.42AK-SCDIAG1/FILE_INDEX.json")
mapping=j("Profiles/EXPECTED_HASHES.json")
build=j("BuildSpecs/current.json")
auto=j("Current/AUTO_BUILD_RESULT.json")
parent="Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
profile="Profiles/LC V1 S1.42AK-SCD1.r2z"
new="BepInEx/plugins/S142AKSCDiag1/S142AKSCDiag1.dll"
ph="6be6865a7fde205280439503680ac910401c20b997f757ffbedbddc963c704f4"
bh="3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
dh="2bd49852973c04c89dceea5b8dc9e75b051bc9a95c16850af08fb37dc3113131"
must(s["accepted_baseline"]["build_id"]=="S1.42AK", "accepted baseline drift")
must(s["active_candidate"]["build_id"]=="S1.42AK-BMDSFIX1" and
     s["active_candidate"]["status"]=="ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED",
     "BMDSFIX1 gameplay candidate drift")
must(s["runtime_test_outstanding"] is True, "outstanding independent passive test erased")
must(build["enabled"] is False and build["build_id"]=="IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
     "build controller not disabled/IDLE")
must(build["local_plugin_builds"]==[] and build["config_patches"]==[], "build controller changed")
must(s["controllers"]["runtime_active_build"]=="S1.42AK-SCDIAG1" and
     (ROOT/"RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip()=="S1.42AK-SCDIAG1",
     "runtime controller/attribution disagreement")
must(p["storage_complex_scdiag1_runtime_activation_checkpoint_authorized_conditional"] is True and
     p["storage_complex_scdiag1_runtime_armed"] is True and
     p["storage_complex_runtime_test_authorized"] is True and
     p["storage_complex_scdiag1_built"] is False, "forbidden stage or new build")
must(p["storage_complex_target_generation_status"]=="STILL_NO_TRUSTED_ACTUAL_GENERATION_PROOF",
     "unearned generation proof")
must(d["build_id"]==r["build_id"]=="S1.42AK-SCDIAG1" and
     d["status"]=="PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED" and
     d["classification"]==r["classification"]=="DIAGNOSTIC_ONLY_NEVER_ACCEPT" and
     d["runtime_armed"] is True, "diagnostic lifecycle mismatch")
must(d["profile"]==r["output_profile"]==profile and
     d["sha256"]==r["output_sha256"]==ph and
     d["base_profile"]==r["base_profile"]==parent and
     d["base_sha256"]==r["base_sha256"]==bh, "Gale direct routing hashes/path mismatch")
must(d["base_build_id"]==r["base_build_id"]==auto["build_id"]=="S1.42AK-BMDSFIX1" and
     auto["output_profile"]==parent and auto["output_sha256"]==bh, "Gale AUTO candidate anchor mismatch")
must(r["runtime_target_metadata"]["runtime_controller_target"]=="S1.42AK-SCDIAG1" and
     r["runtime_target_metadata"]["runtime_attempts_authorized"]==1 and
     r["runtime_target_metadata"]["runtime_target_moon"]=="Offense" and
     r["runtime_target_metadata"]["runtime_target_flow"]=="StorageComplex",
     "routing/attempt target widened")
must(review["artifact_id"]==r["authoritative_review_artifact_id"]==11581745624 and
     review["zip_sha256"]==r["authoritative_review_artifact_zip_sha256"]==
     "9971c22f162ef61177b57f2e350bba5289f5fa09dd78cff65ccd82fcadb0d730",
     "unfrozen Actions artifact reference")
must(review["independent_artifact_rehash_match"] is True and
     review["profile_sha256"]==ph and review["parent_sha256"]==bh and review["dll_sha256"]==dh,
     "frozen review hashes drift")
must(idx["sha256"]==ph and idx["build_id"]=="S1.42AK-SCDIAG1" and
     idx["build_id_resolution"]=="EXPECTED_HASHES" and idx["zip_members"]==338 and
     idx["snapshot"]["entries"]==338 and idx["snapshot"]["text_entries"]==331 and
     mapping[profile]["sha256"]==ph and mapping[profile]["build_id"]=="S1.42AK-SCDIAG1",
     "canonical mapping/index mismatch")
must(h(profile)==ph and h(parent)==bh, "published profile or parent byte hash mismatch")
must(len(members)==338 and len(set(x["path"] for x in members))==338 and
     sum(bool(x["text_snapshot"]) for x in members)==331,
     "full static index row count/uniqueness mismatch")
indexed={x["path"]:x for x in members}
must(indexed[new]["sha256"]==dh and indexed[new]["size"]==18944 and
     indexed["BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"]["sha256"]==
     "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06" and
     indexed["BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"]["sha256"]==
     "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92",
     "DLL/normalizer/BMDSFIX1 frozen hashes mismatch")
# LLL is a Gale/Thunderstore managed package, not a loose plugin member of
# the .r2z user-override archive. It must NOT be invented in FILE_INDEX.
# The exact runtime GUID/version/hash remain mandatory plugin arming guards.
must(not any(x["path"].lower().endswith("/lethallevelloader.dll") for x in members),
     "unexpected loose LLL DLL override in frozen diagnostic archive")
source=(ROOT/"Patches/S142AKSCDiag1/Plugin.cs").read_text(encoding="utf-8")
must(all(x in source for x in (
     "imabatby.lethallevelloader", "1.7.12",
     "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c",
     "tendas.lethalcompany.s142abinteriorweightnormalization",
     "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06")),
     "exact external LLL/normalizer arming identity missing")
with ZipFile(ROOT/profile) as z, ZipFile(ROOT/parent) as base:
    child={n:z.read(n) for n in z.namelist()}
    inherited={n:base.read(n) for n in base.namelist()}
    must(len(child)==338 and len(inherited)==337 and
         set(child)-set(inherited)=={new} and set(inherited)-set(child)==set(),
         "reviewed 337-to-338 archive delta drift")
    must(z.testzip() is None and base.testzip() is None, "ZIP CRC drift")
    must(hash_bytes(child[new])==dh, "archived diagnostic DLL mismatch")
    must(all(child[n]==v for n,v in inherited.items() if n!="export.r2x"),
         "inherited archive member changed")
    old=inherited["export.r2x"]
    old_head=old.splitlines(keepends=True)[0]
    child_head=child["export.r2x"].splitlines(keepends=True)[0]
    must(old_head.startswith(b"profileName: ") and
         child_head.startswith(b"profileName: LC V1 S1.42AK-SCD1") and
         old.replace(old_head,child_head,1)==child["export.r2x"],
         "export.r2x differs beyond exact profile identity")
    must(all(hash_bytes(v)==indexed[n]["sha256"] for n,v in child.items()),
         "archived member hash / static index mismatch")
must(d["target_moon"]=="Offense" and d["target_dungeon_name"]=="Storage Complex" and
     d["target_flow_asset"]=="StorageComplex" and d["target_rarity"]==100,
     "wrong exact target selector")
must(r["published"] is True and r["indexed"] is True and r["runtime_proof"] is False and
     r["changed_existing_members"]==["export.r2x"] and r["added_members"]==[new] and
     r["package_changes"]==r["config_changes"]==0,
     "unauthorized package/config/generation proof")
print("PASS: exact profile/parent/DLL/LLL/normalizer bytes, 337->338 delta, CRC, canonical indexing, disabled build, one-hop Gale runtime-only activation; no compilation")
