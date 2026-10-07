#!/usr/bin/env python3
"""Exact DIAG1 -> DIAG2 one-variable camera config archive gate. Does not arm runtime."""
import configparser
import hashlib
import json
import zipfile
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "BuildSpecs/S1.42AJ-DIAG2.json"
EXPECTED_BASE_SHA = "4e6d7219deff356c5969a40bd75433987bf96baf60be68ae3928578faabf2832"
CONFIG = "BepInEx/config/Piggy.LCOffice.cfg"
DIAG_DLL = "BepInEx/plugins/S142AJDiag1OfficeSelection/S142AJDiag1OfficeSelection.dll"
DIAG_DLL_SHA = "9a477c18e5b8cf38922fa755b6bab101babc2f987e858567172b9be9c2c05fad"
NORMALIZER = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
PRESERVED_PROFILE_NAME = "LC V1 S1.42AJ-DIAG1 LC Office Diagnostic"

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def members(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError("Duplicate archive members")
        return {name: z.read(name) for name in names}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

spec = json.loads(SPEC.read_text(encoding="utf-8"))
require(spec["build_id"] == "S1.42AJ-DIAG2", "Build ID mismatch")
require(spec["base_profile"] == "Profiles/LC V1 S1.42AJ-DIAG1 LC Office Diagnostic.r2z", "Base profile mismatch")
require(spec["base_sha256"] == EXPECTED_BASE_SHA, "Spec base SHA mismatch")
require(spec["profile_name"] == PRESERVED_PROFILE_NAME, "Internal profile name must stay byte-stable with DIAG1")
for field in ("mod_state_changes", "mod_additions", "mod_removals", "file_injections", "local_plugin_builds"):
    require(spec[field] == [], "Unauthorized " + field)
require(spec["config_patches"] == [{
    "path": CONFIG,
    "section": "General",
    "key": "Camera Frame Speed",
    "value": "0",
}], "DIAG2 must contain exactly the one camera-frame-speed config patch")

base = ROOT / spec["base_profile"]
require(sha(base.read_bytes()) == EXPECTED_BASE_SHA, "DIAG1 base SHA mismatch")
original = members(base)
require(CONFIG not in original, "DIAG1 unexpectedly already contains LC Office config")

output = ROOT / spec["output_profile"]
built = members(output)
require(set(original) - set(built) == set(), "Archive members removed")
require(set(built) - set(original) == {CONFIG}, "Added member mismatch")
changed = [name for name in original if original[name] != built[name]]
require(changed == [], "Existing DIAG1 member drift: " + repr(changed))
require(built["export.r2x"] == original["export.r2x"], "export.r2x drift")
require(sha(built[DIAG_DLL]) == DIAG_DLL_SHA, "DIAG1 force-selection DLL drift")
require(sha(built[NORMALIZER]) == NORMALIZER_SHA, "Interior normalizer drift")

cfg_text = built[CONFIG].decode("utf-8-sig")
parser = configparser.ConfigParser(strict=True)
parser.optionxform = str
parser.read_file(StringIO(cfg_text))
require(parser.sections() == ["General"], "LC Office config must contain only [General]")
require(list(parser["General"].keys()) == ["Camera Frame Speed"], "LC Office config contains an unrelated key")
require(parser["General"]["Camera Frame Speed"].strip() == "0", "Camera Frame Speed is not 0")

result = json.loads((ROOT / spec["result_json"]).read_text(encoding="utf-8"))
require(result["build_id"] == "S1.42AJ-DIAG2", "Build-result ID mismatch")
require(result["base_sha256"] == EXPECTED_BASE_SHA, "Build-result base SHA mismatch")
require(result["output_sha256"] == sha(output.read_bytes()), "Build-result output SHA mismatch")
require(result["changed_existing_members"] == [], "Builder reports changed existing members")
require(result["added_members"] == [CONFIG], "Builder reports unexpected added members")

report = {
    "status": "STATIC_PASS_NOT_RUNTIME_READY",
    "build_id": "S1.42AJ-DIAG2",
    "base_build_id": "S1.42AJ-DIAG1",
    "base_sha256": EXPECTED_BASE_SHA,
    "output_sha256": sha(output.read_bytes()),
    "changed_existing_members": [],
    "added_members": [CONFIG],
    "camera_frame_speed": 0,
    "diagnostic_dll_sha256": sha(built[DIAG_DLL]),
    "normalizer_sha256": sha(built[NORMALIZER]),
    "qualification": "Exact one-variable archive proof only. Not published, not armed, and no performance causality inferred.",
}
dest = ROOT / "BuildSpecs/S1.42AJ-DIAG2_BUILD_EVIDENCE"
dest.mkdir(exist_ok=True)
(dest / "STATIC_VERIFICATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
