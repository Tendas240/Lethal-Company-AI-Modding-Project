#!/usr/bin/env python3
"""Construct the authorized S1.42AK-TWDIAG1 inactive review artifact only.

This builder never publishes, indexes, arms runtime, or changes live controllers.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAIN = "b240d621951e80b904dc0e5bbb4435e4d064d9cf"
SPEC_PATH = ROOT / "BuildSpecs/S1.42AK-TWDIAG1.json"
PARENT_REL = "Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z"
PARENT_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
PROFILE_REL = "Profiles/LC V1 S1.42AK-TWD1.r2z"
PROFILE_NAME = "LC V1 S1.42AK-TWD1"
OLD_PROFILE_NAME = "LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix"
DLL_MEMBER = "BepInEx/plugins/S142AKTWDiag1/S142AKTWDiag1.dll"
COMPILED_REL = "Patches/S142AKTWDiag1/bin/Release/netstandard2.1/S142AKTWDiag1.dll"
OUT = ROOT / "review-output"
EVIDENCE = OUT / "Evidence"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def main() -> None:
    require(not OUT.exists(), "review-output already exists; refuse overwrite")
    require(not (ROOT / PROFILE_REL).exists(), "TWDIAG1 review profile already exists in repository checkout")
    tracked = git("ls-files", "--error-unmatch", "--", PROFILE_REL)
    require(tracked.returncode != 0, "TWDIAG1 review profile is tracked; inactive review must remain ephemeral")
    require(not (ROOT / "ProfileSources/S1.42AK-TWDIAG1").exists(),
            "ProfileSources/S1.42AK-TWDIAG1 must not exist during inactive review")

    fetch = git("fetch", "--no-tags", "--depth=1", "origin", SOURCE_MAIN)
    require(fetch.returncode == 0, "Cannot fetch exact source-main authority: " + fetch.stdout)
    source_diff = git(
        "diff", "--exit-code", SOURCE_MAIN, "HEAD", "--",
        "Patches/S142AKTWDiag1",
        "AnalysisTools/validate_s142ak_twdiag1_source.py",
        ".github/workflows/s142ak-twdiag1-source-static.yml",
        "SourceEvidence/UniversalInteriorViability/TWDIAG1SourceStatic/FINDINGS.md",
    )
    require(source_diff.returncode == 0,
            "Main-integrated TWDIAG1 source/static inputs drifted in review branch:\n" + source_diff.stdout)

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    expected = {
        "enabled": True,
        "review_only": True,
        "build_id": "S1.42AK-TWDIAG1",
        "base_profile": PARENT_REL,
        "base_sha256": PARENT_SHA,
        "output_profile": PROFILE_REL,
        "profile_name": PROFILE_NAME,
        "overwrite": False,
        "mod_state_changes": [],
        "mod_additions": [],
        "mod_removals": [],
        "config_patches": [],
        "file_injections": [],
        "local_plugin_builds": [{
            "project": "Patches/S142AKTWDiag1/S142AKTWDiag1.csproj",
            "configuration": "Release",
            "built_file": COMPILED_REL,
            "archive_path": DLL_MEMBER,
        }],
        "text_assertions": [{"path": "export.r2x", "not_contains": "LethalLevelLoaderUpdated"}],
        "result_json": "BuildSpecs/S1.42AK-TWDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json",
        "result_md": "BuildSpecs/S1.42AK-TWDIAG1_BUILD_EVIDENCE/BUILD_RESULT.md",
    }
    require(spec == expected, "Frozen TWDIAG1 review recipe drift")

    parent_path = ROOT / PARENT_REL
    compiled_path = ROOT / COMPILED_REL
    require(parent_path.is_file(), "Exact BMDSFIX1 parent profile missing")
    parent_bytes = parent_path.read_bytes()
    require(sha256(parent_bytes) == PARENT_SHA, "Exact BMDSFIX1 parent SHA-256 mismatch")
    require(compiled_path.is_file(), "Compiled TWDIAG1 DLL missing")
    dll_bytes = compiled_path.read_bytes()

    EVIDENCE.mkdir(parents=True)
    output_path = OUT / PROFILE_REL
    output_path.parent.mkdir(parents=True)

    with zipfile.ZipFile(parent_path, "r") as src:
        infos = src.infolist()
        names = [info.filename for info in infos]
        require(len(names) == len(set(names)) == 337, "Parent archive member count/uniqueness drift")
        require(DLL_MEMBER not in names, "TWDIAG1 DLL unexpectedly already exists in parent")
        require("export.r2x" in names, "Parent export.r2x missing")

        export = src.read("export.r2x")
        old = ("profileName: " + OLD_PROFILE_NAME).encode("utf-8")
        new = ("profileName: " + PROFILE_NAME).encode("utf-8")
        lines = export.splitlines(keepends=True)
        hits = [i for i, line in enumerate(lines) if line.rstrip(b"\r\n") == old]
        require(len(hits) == 1, "Parent profileName identity is not uniquely exact")
        i = hits[0]
        lines[i] = new + lines[i][len(old):]
        changed_export = b"".join(lines)

        with zipfile.ZipFile(output_path, "x") as dst:
            for info in infos:
                data = changed_export if info.filename == "export.r2x" else src.read(info.filename)
                dst.writestr(info, data)
            new_info = zipfile.ZipInfo(DLL_MEMBER, date_time=(1980, 1, 1, 0, 0, 0))
            new_info.create_system = 0
            dst.writestr(new_info, dll_bytes, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    (OUT / "DLL").mkdir()
    shutil.copyfile(compiled_path, OUT / "DLL/S142AKTWDiag1.dll")

    with zipfile.ZipFile(output_path, "r") as built:
        require(built.testzip() is None, "Generated TWDIAG1 profile ZIP CRC failure")
        require(len(built.namelist()) == 338, "Generated review profile must have exactly 338 members")

    report = {
        "status": "COMPILE_INPUT_PRESENT_ARCHIVE_AWAITS_INDEPENDENT_VALIDATION",
        "build_id": "S1.42AK-TWDIAG1",
        "classification": "DIAGNOSTIC_ONLY_NEVER_ACCEPT",
        "source_main_commit": SOURCE_MAIN,
        "build_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "parent_profile": PARENT_REL,
        "parent_sha256": PARENT_SHA,
        "review_profile": PROFILE_REL,
        "profile_sha256": sha256(output_path.read_bytes()),
        "dll_member": DLL_MEMBER,
        "dll_sha256": sha256(dll_bytes),
        "parent_members": 337,
        "review_members": 338,
        "profile_indexing": False,
        "published": False,
        "runtime_armed": False,
        "runtime_proof": False,
    }
    (EVIDENCE / "BUILD_RESULT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
