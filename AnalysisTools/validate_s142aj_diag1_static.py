#!/usr/bin/env python3
"""Exact AJ -> DIAG1 archive delta gate. Does not arm or promote any runtime."""
import hashlib, json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def sha(b): return hashlib.sha256(b).hexdigest()
def members(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        if len(names)!=len(set(names)): raise RuntimeError("Duplicate archive members")
        return {n:z.read(n) for n in names}
def require(ok, message):
    if not ok: raise RuntimeError(message)

spec=json.loads((ROOT/"BuildSpecs/S1.42AJ-DIAG1.json").read_text())
base=ROOT/spec["base_profile"]
require(sha(base.read_bytes())=="7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba", "AJ base SHA mismatch")
for field in ("mod_state_changes","mod_additions","mod_removals","config_patches","file_injections"):
    require(spec[field]==[], "Unauthorized "+field)
require(len(spec["local_plugin_builds"])==1,"Exactly one local plugin required")
original=members(base)
output=ROOT/spec["output_profile"]
built=members(output)
dll="BepInEx/plugins/S142AJDiag1OfficeSelection/S142AJDiag1OfficeSelection.dll"
require(set(built)-set(original)=={dll}, "Added member mismatch")
require(set(original)-set(built)==set(), "Removed members")
changed=[n for n in original if original[n]!=built[n]]
require(changed==["export.r2x"], "Unexpected changed members: "+repr(changed))
def stable_export(data):
    text=data.decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n")
    require(len(re.findall(r"(?m)^profileName:.*$",text))==1,"Profile name count")
    return re.sub(r"(?m)^profileName:.*$","profileName: <identity>",text).rstrip("\n")
require(stable_export(original["export.r2x"])==stable_export(built["export.r2x"]), "Package/export drift")
require("LethalLevelLoaderUpdated" not in built["export.r2x"].decode(), "Forbidden LLL fork")
normalizer="BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
require(sha(built[normalizer])=="901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06", "Normalizer drift")
compiled=ROOT/spec["local_plugin_builds"][0]["built_file"]
require(compiled.read_bytes()==built[dll], "Injected DLL differs from compiled DLL")
result=json.loads((ROOT/spec["result_json"]).read_text())
require(result["build_id"]=="S1.42AJ-DIAG1" and result["output_sha256"]==sha(output.read_bytes()),"Build result binding")
require(result["added_members"]==[dll] and result["changed_existing_members"]==["export.r2x"],"Builder delta mismatch")
report={"status":"STATIC_PASS_NOT_RUNTIME_READY","build_id":"S1.42AJ-DIAG1",
        "base_sha256":sha(base.read_bytes()),"output_sha256":sha(output.read_bytes()),
        "diagnostic_dll_sha256":sha(built[dll]),"normalizer_sha256":sha(built[normalizer]),
        "changed_existing_members":changed,"added_members":[dll],
        "qualification":"Build and archive validation only. Runtime caller identification, ordering, generation and gameplay remain unproven."}
dest=ROOT/"BuildSpecs/S1.42AJ-DIAG1_BUILD_EVIDENCE"
dest.mkdir(exist_ok=True)
(dest/"STATIC_VERIFICATION.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
