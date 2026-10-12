#!/usr/bin/env python3
"""CKDIAG1 fail-closed, source-ABSENT checkpoint guard. This is NOT source approval."""
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ("s1.42ak-ckdiag1", "s142akckdiag1",
          "tendas.lethalcompany.s142akckdiag1", "lc v1 s1.42ak-ckd1",
          "[ckdiag1]")
PARENT = "LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
EXPECTED_PARENT_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
NORMALIZER_PATH = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
RECORD = "Current/402_S1.42AK_PHASE_C_CKDIAG1_SOURCE_GATES_BLOCKED_CHECKPOINT.md"
FINDINGS = "SourceEvidence/UniversalInteriorViability/CKDIAG1BlockedSourcePreflight/FINDINGS.md"

def require(ok, why):
    if not ok:
        raise RuntimeError("CKDIAG1 BLOCKED checkpoint guard: " + why)

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def sha(data):
    return hashlib.sha256(data).hexdigest()

def collides(value):
    lower = value.casefold()
    return any(token in lower for token in TOKENS)

def inspect_archives():
    archives = sorted((ROOT / "Profiles").glob("*.r2z"))
    require(archives, "no original archives")
    hits = []
    unindexed = []
    for archive in archives:
        with zipfile.ZipFile(archive) as z:
            members = [entry for entry in z.infolist() if not entry.is_dir()]
            names = [entry.filename for entry in members]
            require(len(names) == len(set(name.casefold() for name in names)),
                    "case-insensitive member alias in " + archive.name)
            for entry in members:
                if collides(entry.filename):
                    hits.append(archive.name + "::" + entry.filename)
                # Inspect source-config/profile metadata and raw local DLL bytes, not external packages.
                if entry.filename.lower().endswith((".r2x", ".cfg", ".dll", ".json")):
                    data = z.read(entry.filename)
                    low = data.lower()
                    if any(token.encode("utf-8") in low for token in TOKENS):
                        hits.append(archive.name + "::" + entry.filename + " [embedded]")
                    if any(token.encode("utf-16le") in low for token in TOKENS):
                        hits.append(archive.name + "::" + entry.filename + " [utf16]")
            if archive.name == PARENT:
                require(sha(archive.read_bytes()) == EXPECTED_PARENT_SHA,
                        "original parent bytes SHA-256 drift")
                index = json.loads(read("ProfileSources/S1.42AK-BMDSFIX1/FILE_INDEX.json"))
                items = {x["path"]: x for x in index}
                require(len(items) == len(index) and set(items) == set(names),
                        "parent index / archive member mismatch")
                for entry in members:
                    b = z.read(entry)
                    meta = items[entry.filename]
                    require(sha(b) == meta["sha256"] and len(b) == meta["size"],
                            "parent file-index content hash drift: " + entry.filename)
                require(items[NORMALIZER_PATH]["sha256"] == NORMALIZER_SHA,
                        "original normalizer indexed DLL hash drift")
    require(len(archives) >= 75, "profile archive inventory shrank")
    require(not hits, "reserved identity collision: " + str(hits[:5]))
    return len(archives)

def main():
    state = json.loads(read("Current/CURRENT_STATE.json"))
    phase = state["selected_scope"]["phase_c"]
    build = json.loads(read("BuildSpecs/current.json"))
    require(state["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline drift")
    require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1" and
            state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED",
            "active candidate drift")
    require(phase["crimson_keep_source_implementation_authorized"] is True and
            phase["crimson_keep_runtime_test_authorized"] is False,
            "conditional source authorization/lifecycle drift")
    require(phase["residual_no_trusted_actual_generation_proof"] == 21 and
            phase["residual_viable_equal_100"] == 9 and
            phase["residual_owner_hard_block"] == 12, "phase C residual drift")
    require(not build["enabled"] and
            build["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
            "build controller active")
    require(read("RuntimeInbox/ACTIVE_BUILD.txt").strip() == "S1.42AK-BMDSFIX1",
            "runtime evidence routing drift")
    require(not (ROOT / "Patches/S142AKCKDiag1").exists(),
            "unsafe selector source staged under a blocked checkpoint")
    require(not (ROOT / ".github/workflows/s142ak-ckdiag1-source-static.yml").exists(),
            "source validation workflow would misrepresent blocked state")
    require("BLOCKED / REFUSED" in read(RECORD) and
            "NO SOURCE IMPLEMENTATION" in read(FINDINGS),
            "blocked authorization statement missing")
    indexes = sorted((ROOT / "ProfileSources").glob("*/FILE_INDEX.json"))
    require(len(indexes) >= 66, "indexed inventory shrank")
    for path in indexes:
        entries = json.loads(path.read_text(encoding="utf-8"))
        require(not any(collides(e["path"]) for e in entries),
                "indexed member collision: " + str(path))
    count = inspect_archives()
    print(json.dumps({
        "checkpoint": "CKDIAG1_BLOCKED_REFUSED_SOURCE_ABSENT",
        "profile_archives_inspected": count,
        "file_indexes_inspected": len(indexes),
        "parent_sha256": EXPECTED_PARENT_SHA,
        "source_compiled": False, "patch_installed": False,
        "runtime_authorized": False, "collision_preflight": "PASS_NOT_SOURCE_AUTHORITY",
        "unresolved": ["effective Harmony execution order", "unambiguous server caller",
                       "runtime owner/asset reference provenance",
                       "atomic isolated return-list mutation semantics",
                       "exact packaged LLL/normalizer dependency identity at future runtime"]
    }, indent=2))

if __name__ == "__main__":
    main()
