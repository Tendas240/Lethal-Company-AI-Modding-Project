#!/usr/bin/env python3
"""Exact S1.42AK-BMDSFIX1 -> SHDIAG1 inactive review-build validator.

Validates only compiler/archive review bytes. Never publishes, indexes, imports,
arms runtime, or establishes gameplay proof.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path

import dnfile

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-SHDIAG1.json"
CURRENT_SPEC_PATH = ROOT / "BuildSpecs/current.json"
ACTIVE_BUILD_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
CURRENT_STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
PARENT_REL = "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
PARENT_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
PROFILE_REL = "Profiles/LC V1 S1.42AK-SHD1.r2z"
PROFILE_NAME = "LC V1 S1.42AK-SHD1"
OLD_PROFILE_NAME = "LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix"
DLL_MEMBER = "BepInEx/plugins/S142AKSHDiag1/S142AKSHDiag1.dll"
BMDS_DLL = "BepInEx/plugins/S142AKBMDSFix1/S142AKBMDSFix1.dll"
BMDS_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
NORMALIZER_DLL = "BepInEx/plugins/S142ABInteriorWeightNormalization/S142ABInteriorWeightNormalization.dll"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
BASELINE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_members(data: bytes) -> dict[str, bytes]:
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        require(archive.testzip() is None, "ZIP CRC failed")
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate ZIP members")
        for name in names:
            normalized = name.replace("\\", "/")
            require(not normalized.startswith("/") and ".." not in normalized.split("/"),
                    "Unsafe ZIP member path: " + name)
        return {name: archive.read(name) for name in names}


def validate_delta(parent: dict[str, bytes], built: dict[str, bytes], dll: bytes) -> dict:
    require(len(parent) == 337, "Parent archive must contain exactly 337 members")
    require(len(built) == 338, "Review archive must contain exactly 338 members")
    require(set(built) - set(parent) == {DLL_MEMBER}, "Unexpected added archive member(s)")
    require(not (set(parent) - set(built)), "Parent archive member removed")
    changed = [name for name in parent if parent[name] != built[name]]
    require(changed == ["export.r2x"], "Unexpected changed existing members: " + repr(changed))

    old = ("profileName: " + OLD_PROFILE_NAME).encode("utf-8")
    new = ("profileName: " + PROFILE_NAME).encode("utf-8")
    pattern = re.compile(rb"(?m)^" + re.escape(new) + rb"(?=\r?$)")
    reverted, count = pattern.subn(old, built["export.r2x"])
    require(count == 1 and reverted == parent["export.r2x"],
            "export.r2x drift exceeds exact profile identity metadata")
    require(b"LethalLevelLoaderUpdated" not in built["export.r2x"], "Forbidden LLL fork identity present")

    require(built[DLL_MEMBER] == dll, "Injected SHDIAG1 DLL differs from frozen compiled DLL")
    require(BMDS_DLL in parent and BMDS_DLL in built, "BMDSFIX1 DLL missing")
    require(sha256(parent[BMDS_DLL]) == sha256(built[BMDS_DLL]) == BMDS_DLL_SHA,
            "BMDSFIX1 DLL hash drift")
    require(parent[BMDS_DLL] == built[BMDS_DLL], "BMDSFIX1 DLL bytes changed")
    require(NORMALIZER_DLL in parent and NORMALIZER_DLL in built, "Accepted normalizer DLL missing")
    require(sha256(parent[NORMALIZER_DLL]) == sha256(built[NORMALIZER_DLL]) == NORMALIZER_SHA,
            "Accepted normalizer hash drift")
    require(parent[NORMALIZER_DLL] == built[NORMALIZER_DLL], "Accepted normalizer bytes changed")

    return {
        "parent_members": 337,
        "review_members": 338,
        "changed_existing_members": changed,
        "added_members": [DLL_MEMBER],
        "removed_members": [],
        "package_changes": 0,
        "config_changes": 0,
        "bmdsfix1_dll_sha256": BMDS_DLL_SHA,
        "normalizer_sha256": NORMALIZER_SHA,
    }


def negative_cases(parent: dict[str, bytes], built: dict[str, bytes], dll: bytes) -> list[str]:
    cases: list[str] = []
    mutations = {
        "config-drift": lambda b: b.__setitem__(
            "BepInEx/config/LethalLevelLoader.cfg",
            b["BepInEx/config/LethalLevelLoader.cfg"] + b"\n"),
        "bmdsfix1-replaced": lambda b: b.__setitem__(BMDS_DLL, b"wrong"),
        "normalizer-replaced": lambda b: b.__setitem__(NORMALIZER_DLL, b"wrong"),
        "member-removed": lambda b: b.pop(BMDS_DLL),
        "extra-plugin": lambda b: b.__setitem__("BepInEx/plugins/unauthorized.dll", b"wrong"),
        "export-drift": lambda b: b.__setitem__("export.r2x", b["export.r2x"] + b"\n# unauthorized\n"),
        "wrong-profile-identity": lambda b: b.__setitem__(
            "export.r2x", b["export.r2x"].replace(b"LC V1 S1.42AK-SHD1", b"LC V1 S1.42AK-LFD2")),
        "wrong-shdiag1-dll": lambda b: b.__setitem__(DLL_MEMBER, b"wrong"),
    }
    for name, mutate in mutations.items():
        altered = dict(built)
        mutate(altered)
        try:
            validate_delta(parent, altered, dll)
        except ValueError:
            cases.append(name)
        else:
            raise ValueError("Negative case unexpectedly accepted: " + name)
    return cases


def assembly_identity(dll: bytes) -> str:
    pe = dnfile.dnPE(data=dll)
    try:
        require(pe.net is not None, "Compiled SHDIAG1 DLL is not a managed assembly")
        rows = pe.net.mdtables.Assembly.rows
        require(len(rows) == 1, "Compiled SHDIAG1 DLL has missing/ambiguous Assembly table")
        return str(rows[0].Name)
    finally:
        pe.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--artifact-root", type=Path, default=ROOT / "review-output")
    args = parser.parse_args()

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    current_spec = json.loads(CURRENT_SPEC_PATH.read_text(encoding="utf-8"))
    current_state = json.loads(CURRENT_STATE_PATH.read_text(encoding="utf-8"))
    active_build = ACTIVE_BUILD_PATH.read_text(encoding="utf-8").strip()

    require(spec["enabled"] is True and spec["review_only"] is True, "SHDIAG1 review recipe activation drift")
    require(spec["build_id"] == "S1.42AK-SHDIAG1", "SHDIAG1 build ID drift")
    require(spec["base_profile"] == PARENT_REL and spec["base_sha256"] == PARENT_SHA, "Parent recipe drift")
    require(spec["output_profile"] == PROFILE_REL and spec["profile_name"] == PROFILE_NAME, "Review identity drift")
    require(spec["overwrite"] is False, "Review overwrite must remain false")
    for field in ("mod_state_changes", "mod_additions", "mod_removals", "config_patches", "file_injections"):
        require(spec[field] == [], "Unauthorized recipe field: " + field)

    require(current_spec["enabled"] is False, "BuildSpecs/current.json must remain disabled")
    require(current_spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS",
            "Live build controller ID drift")
    require(current_spec["base_profile"] == PARENT_REL and current_spec["base_sha256"] == PARENT_SHA,
            "Live build controller parent drift")
    require(current_spec["local_plugin_builds"] == [], "Live build controller must not arm SHDIAG1")
    require(active_build == "S1.42AK-BMDSFIX1", "Runtime ACTIVE_BUILD drift")
    require(current_state["accepted_baseline"]["build_id"] == "S1.42AK", "Accepted baseline ID drift")
    require(current_state["accepted_baseline"]["sha256"] == BASELINE_SHA, "Accepted baseline hash drift")
    require(current_state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "Active candidate ID drift")
    require(current_state["active_candidate"]["sha256"] == PARENT_SHA, "Active candidate profile hash drift")
    require(current_state["runtime_test_outstanding"] is True, "BMDSFIX1 regular runtime gate must remain outstanding")
    require(not (ROOT / "ProfileSources/S1.42AK-SHDIAG1").exists(),
            "Inactive review must not create a SHDIAG1 ProfileSources index")

    published = ROOT / PROFILE_REL
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", PROFILE_REL],
        cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    require(not published.exists() and tracked.returncode != 0,
            "SHDIAG1 review profile must remain uncommitted/unpublished")

    parent_bytes = (ROOT / PARENT_REL).read_bytes()
    require(sha256(parent_bytes) == PARENT_SHA, "Exact BMDSFIX1 parent SHA mismatch")
    profile_path = args.artifact_root / PROFILE_REL
    dll_path = args.artifact_root / "DLL/S142AKSHDiag1.dll"
    require(profile_path.is_file(), "Frozen SHDIAG1 review profile missing")
    require(dll_path.is_file(), "Frozen compiled SHDIAG1 DLL missing")
    profile_bytes = profile_path.read_bytes()
    dll = dll_path.read_bytes()

    parent = read_members(parent_bytes)
    built = read_members(profile_bytes)
    report = validate_delta(parent, built, dll)
    identity = assembly_identity(dll)
    require(identity == "S142AKSHDiag1", "Assembly identity drift: " + identity)

    result_path = args.artifact_root / "Evidence/BUILD_RESULT.json"
    require(result_path.is_file(), "Builder result evidence missing")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    require(result["build_id"] == "S1.42AK-SHDIAG1", "Builder result build ID drift")
    require(result["parent_sha256"] == PARENT_SHA, "Builder parent hash report drift")
    require(result["profile_sha256"] == sha256(profile_bytes), "Builder profile hash report drift")
    require(result["dll_sha256"] == sha256(dll), "Builder DLL hash report drift")
    require(result["profile_indexing"] is False and result["published"] is False and result["runtime_armed"] is False,
            "Builder inactive-scope report drift")

    report.update({
        "status": "PASS_INACTIVE_COMPILE_ARCHIVE_REVIEW_ONLY",
        "classification": "DIAGNOSTIC_ONLY_NEVER_ACCEPT",
        "assembly_name": identity,
        "parent_sha256": PARENT_SHA,
        "profile_sha256": sha256(profile_bytes),
        "dll_sha256": sha256(dll),
        "negative_cases": negative_cases(parent, built, dll) if args.self_test else [],
        "profile_indexing": False,
        "published": False,
        "runtime_armed": False,
        "runtime_proof": False,
        "actions_zip_rehash": "OUTSTANDING_AFTER_ARTIFACT_FREEZE",
        "qualification": "Compiler/archive validity only. No publication, ProfileSources index, Gale import, runtime activation, gameplay proof, or acceptance.",
    })
    evidence = args.artifact_root / "Evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "STATIC_VERIFICATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
