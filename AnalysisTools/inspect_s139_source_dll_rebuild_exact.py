#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREBUILD_COMMIT = "af415c8d6fdb69b0b7c88102e714764f3dc24b57"
BUILD_COMMIT = "fdb6b94e34144f860f6ac6eb2fd5bdbdd7797ef5"
BUILD_RUN_ID = 34141360051
HISTORICAL_SDK = "8.0.424"
ILSPY_VERSION = "11.0.0.9375"

SOURCE = "Patches/S139CompatibilityFixes/Plugin.cs"
CSPROJ = "Patches/S139CompatibilityFixes/S139CompatibilityFixes.csproj"
BUILT_DLL = "Patches/S139CompatibilityFixes/bin/Release/netstandard2.1/S139CompatibilityFixes.dll"
HELPER = "RepositoryTools/_temporary_build_s142ah.py"
PROFILE_BUILDER = "BuildSystem/profile_builder.py"
WORKFLOW = ".github/workflows/atomic-build-s142ah-v8-final.yml"
DLL_MEMBER = "BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll"

SOURCE_SHA = "2b8a326383ea5f39a69f7b370836180509dc5a34ec0c1b98dbe0734f4f87707d"
CSPROJ_SHA = "c51a47a8eb502df7a787c2a08ed90962e284fa68e4557c8bc022bc56e68dd39b"
RUNTIME_DLL_SHA = "bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573"
AH_PROFILE = "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z"
AH_PROFILE_SHA = "06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e"
AI_PROFILE = "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
AI_PROFILE_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def ok(proc: subprocess.CompletedProcess[str], label: str) -> str:
    if proc.returncode != 0:
        raise RuntimeError(f"{label} failed ({proc.returncode})\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout


def show(commit: str, path: str) -> bytes:
    proc = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


def assert_sha(label: str, data: bytes, expected: str) -> None:
    actual = sha(data)
    if actual != expected:
        raise RuntimeError(f"{label}: expected {expected}, got {actual}")


def extract_profile_dll(profile_rel: str, profile_sha: str, target: Path) -> dict:
    profile = ROOT / profile_rel
    actual_profile_sha = file_sha(profile)
    if actual_profile_sha != profile_sha:
        raise RuntimeError(f"{profile_rel}: expected profile {profile_sha}, got {actual_profile_sha}")
    with zipfile.ZipFile(profile) as zf:
        hits = [x for x in zf.infolist() if x.filename == DLL_MEMBER]
        if len(hits) != 1:
            raise RuntimeError(f"{profile_rel}: expected exactly one {DLL_MEMBER}, got {len(hits)}")
        data = zf.read(hits[0])
    assert_sha(f"{profile_rel}:{DLL_MEMBER}", data, RUNTIME_DLL_SHA)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {"profile": profile_rel, "profile_sha256": actual_profile_sha, "dll_sha256": sha(data), "dll_size": len(data)}


def decompile(ilspy: Path, dll: Path, il: bool) -> str:
    cmd = [str(ilspy)] + (["--ilcode"] if il else []) + [str(dll)]
    return ok(run(cmd), f"ILSpy {'IL' if il else 'C#'} {dll.name}").replace("\r\n", "\n").replace("\r", "\n")


def summary(out: Path, v: dict) -> None:
    c = v.get("comparison", {})
    text = f"""# S139CompatibilityFixes Source-to-DLL Exact Rebuild Review

- Status: `{v.get('status')}`
- Historical successful build run: `{BUILD_RUN_ID}`
- Historical pre-build head: `{PREBUILD_COMMIT}`
- Historical build commit: `{BUILD_COMMIT}`
- Historical SDK: `{HISTORICAL_SDK}`
- Runtime DLL SHA-256: `{RUNTIME_DLL_SHA}`
- Rebuilt DLL SHA-256: `{c.get('rebuilt_sha256', '<unavailable>')}`
- Byte-identical: `{c.get('byte_identical', False)}`
- Full C# identical: `{c.get('csharp_identical', False)}`
- Full IL identical: `{c.get('il_identical', False)}`

The rebuild runs from a detached worktree at the exact historical pre-build commit. A temporary untracked `global.json` selects the exact SDK observed in the successful historical Actions run; it is an environment selector only and is removed with the worktree.

This is read-only analysis evidence. It does not authorize DIAG1 implementation, a profile build, controller changes, or runtime testing.
"""
    if v.get("error"):
        text += f"\n## Error\n\n```text\n{v['error']}\n```\n"
    (out / "SUMMARY.md").write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", required=True, type=Path)
    ap.add_argument("--ilspy", required=True, type=Path)
    ns = ap.parse_args()
    out = ns.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    ilspy = ns.ilspy.resolve() if ns.ilspy.is_absolute() else (ROOT / ns.ilspy).resolve()
    worktree = out.parent / "s139-historical-prebuild-worktree"

    v: dict = {
        "schema_version": 3,
        "purpose": "S1.42AI-DIAG1 project-local S139 source-to-runtime-DLL exact rebuild review",
        "status": "RUNNING",
        "historical_build": {
            "workflow_run": BUILD_RUN_ID,
            "prebuild_commit": PREBUILD_COMMIT,
            "build_commit": BUILD_COMMIT,
            "observed_runner": "Ubuntu 24.04.4 / image 20260831.293.1",
            "observed_dotnet_sdk": HISTORICAL_SDK,
            "observed_python": "3.12.14",
            "configuration": "Release",
            "project": CSPROJ,
            "built_file": BUILT_DLL,
        },
        "expected": {
            "source_sha256": SOURCE_SHA,
            "csproj_sha256": CSPROJ_SHA,
            "runtime_dll_sha256": RUNTIME_DLL_SHA,
            "s142ah_profile_sha256": AH_PROFILE_SHA,
            "s142ai_profile_sha256": AI_PROFILE_SHA,
            "ilspy_version": ILSPY_VERSION,
        },
    }
    rc = 1
    try:
        v["analysis_head"] = ok(run(["git", "rev-parse", "HEAD"]), "analysis HEAD").strip()
        v["github_run_id"] = os.environ.get("GITHUB_RUN_ID")

        current_source = (ROOT / SOURCE).read_bytes()
        pre_source = show(PREBUILD_COMMIT, SOURCE)
        built_source = show(BUILD_COMMIT, SOURCE)
        current_proj = (ROOT / CSPROJ).read_bytes()
        pre_proj = show(PREBUILD_COMMIT, CSPROJ)
        built_proj = show(BUILD_COMMIT, CSPROJ)
        for label, data, expected in [
            ("current source", current_source, SOURCE_SHA), ("prebuild source", pre_source, SOURCE_SHA),
            ("build source", built_source, SOURCE_SHA), ("current csproj", current_proj, CSPROJ_SHA),
            ("prebuild csproj", pre_proj, CSPROJ_SHA), ("build csproj", built_proj, CSPROJ_SHA),
        ]:
            assert_sha(label, data, expected)
        if not current_source == pre_source == built_source:
            raise RuntimeError("Plugin.cs lineage is not byte-identical")
        if not current_proj == pre_proj == built_proj:
            raise RuntimeError("csproj lineage is not byte-identical")
        v["source_lineage"] = {
            "source_sha256": SOURCE_SHA, "csproj_sha256": CSPROJ_SHA,
            "source_bytes_identical_current_prebuild_build": True,
            "csproj_bytes_identical_current_prebuild_build": True,
        }

        helper = show(PREBUILD_COMMIT, HELPER).decode("utf-8")
        builder = show(PREBUILD_COMMIT, PROFILE_BUILDER).decode("utf-8")
        workflow = show(PREBUILD_COMMIT, WORKFLOW).decode("utf-8")
        for marker in [
            '"project": "Patches/S139CompatibilityFixes/S139CompatibilityFixes.csproj"',
            '"configuration": "Release"',
            '"built_file": "Patches/S139CompatibilityFixes/bin/Release/netstandard2.1/S139CompatibilityFixes.dll"',
            '"archive_path": DLL_ARCHIVE_PATH',
        ]:
            if marker not in helper:
                raise RuntimeError(f"historical helper marker missing: {marker}")
        if 'subprocess.run(["dotnet", "build", str(project), "-c", config], check=True)' not in builder:
            raise RuntimeError("historical profile builder exact dotnet build contract missing")
        for marker in ['runs-on: ubuntu-latest', 'dotnet-version: "8.0.x"', 'python-version: "3.12"']:
            if marker not in workflow:
                raise RuntimeError(f"historical workflow marker missing: {marker}")
        v["historical_contract"] = {
            "helper_sha256": sha(helper.encode()), "profile_builder_sha256": sha(builder.encode()),
            "workflow_sha256": sha(workflow.encode()), "exact_release_build_contract": True,
        }

        ref = out / "reference"
        rebuilt = out / "rebuilt"
        ah_dll = ref / "S1.42AH" / "S139CompatibilityFixes.dll"
        ai_dll = ref / "S1.42AI" / "S139CompatibilityFixes.dll"
        v["profiles"] = {
            "S1.42AH": extract_profile_dll(AH_PROFILE, AH_PROFILE_SHA, ah_dll),
            "S1.42AI": extract_profile_dll(AI_PROFILE, AI_PROFILE_SHA, ai_dll),
        }
        if ah_dll.read_bytes() != ai_dll.read_bytes():
            raise RuntimeError("S1.42AH and S1.42AI embedded project DLLs differ")

        (out / "HOST_DOTNET_SDKS.txt").write_text(ok(run(["dotnet", "--list-sdks"]), "dotnet --list-sdks"), encoding="utf-8")
        if worktree.exists():
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, capture_output=True)
            shutil.rmtree(worktree, ignore_errors=True)
        ok(run(["git", "worktree", "add", "--detach", str(worktree), PREBUILD_COMMIT]), "historical worktree add")
        head = ok(run(["git", "rev-parse", "HEAD"], worktree), "historical worktree HEAD").strip()
        if head != PREBUILD_COMMIT:
            raise RuntimeError(f"historical worktree expected {PREBUILD_COMMIT}, got {head}")
        v["historical_worktree_head"] = head

        selector = {"sdk": {"version": HISTORICAL_SDK, "rollForward": "disable", "allowPrerelease": False}}
        selector_path = worktree / "global.json"
        if selector_path.exists():
            raise RuntimeError("historical pre-build commit unexpectedly already contains global.json")
        selector_bytes = (json.dumps(selector, indent=2) + "\n").encode()
        selector_path.write_bytes(selector_bytes)
        v["temporary_sdk_selector"] = {"sha256": sha(selector_bytes), "tracked": False}
        selected = ok(run(["dotnet", "--version"], worktree), "selected historical SDK").strip()
        v["selected_historical_sdk"] = selected
        if selected != HISTORICAL_SDK:
            raise RuntimeError(f"SDK selector expected {HISTORICAL_SDK}, got {selected}")
        (out / "DOTNET_INFO.txt").write_text(ok(run(["dotnet", "--info"], worktree), "historical dotnet --info"), encoding="utf-8")

        for d in [worktree / "Patches/S139CompatibilityFixes/bin", worktree / "Patches/S139CompatibilityFixes/obj"]:
            shutil.rmtree(d, ignore_errors=True)
        build = run(["dotnet", "build", CSPROJ, "-c", "Release"], worktree)
        (out / "BUILD_STDOUT.txt").write_text(build.stdout, encoding="utf-8")
        (out / "BUILD_STDERR.txt").write_text(build.stderr, encoding="utf-8")
        ok(build, "historical-head exact Release rebuild")
        built = worktree / BUILT_DLL
        if not built.exists():
            raise RuntimeError(f"rebuilt DLL missing: {built}")
        rebuilt_dll = rebuilt / "S139CompatibilityFixes.dll"
        rebuilt_dll.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built, rebuilt_dll)

        version = ok(run([str(ilspy), "--version"]), "ILSpy version").strip()
        (out / "ILSPY_VERSION.txt").write_text(version + "\n", encoding="utf-8")
        if ILSPY_VERSION not in version:
            raise RuntimeError(f"expected ILSpy {ILSPY_VERSION}, got {version}")
        runtime_cs = decompile(ilspy, ai_dll, False)
        rebuilt_cs = decompile(ilspy, rebuilt_dll, False)
        runtime_il = decompile(ilspy, ai_dll, True)
        rebuilt_il = decompile(ilspy, rebuilt_dll, True)
        (ref / "S1.42AI" / "FULL_CSHARP.txt").write_text(runtime_cs, encoding="utf-8")
        (ref / "S1.42AI" / "FULL_IL.txt").write_text(runtime_il, encoding="utf-8")
        (rebuilt / "FULL_CSHARP.txt").write_text(rebuilt_cs, encoding="utf-8")
        (rebuilt / "FULL_IL.txt").write_text(rebuilt_il, encoding="utf-8")

        runtime_bytes = ai_dll.read_bytes()
        rebuilt_bytes = rebuilt_dll.read_bytes()
        v["comparison"] = {
            "runtime_sha256": sha(runtime_bytes), "runtime_size": len(runtime_bytes),
            "rebuilt_sha256": sha(rebuilt_bytes), "rebuilt_size": len(rebuilt_bytes),
            "byte_identical": runtime_bytes == rebuilt_bytes,
            "runtime_csharp_sha256": sha(runtime_cs.encode()), "rebuilt_csharp_sha256": sha(rebuilt_cs.encode()),
            "csharp_identical": runtime_cs == rebuilt_cs,
            "runtime_il_sha256": sha(runtime_il.encode()), "rebuilt_il_sha256": sha(rebuilt_il.encode()),
            "il_identical": runtime_il == rebuilt_il,
        }
        if runtime_bytes != rebuilt_bytes:
            v["status"] = "FAIL_HISTORICAL_HEAD_REBUILD_NOT_BYTE_IDENTICAL"
            v["source_to_dll_provenance"] = "OPEN_REVIEW_REQUIRED"
            rc = 2
        else:
            v["status"] = "PASS_BYTE_IDENTICAL_HISTORICAL_HEAD_REBUILD"
            v["source_to_dll_provenance"] = "CLOSED_EXACT_BYTE_REBUILD"
            rc = 0
    except Exception as exc:
        v["status"] = "FAIL_ANALYSIS_ERROR"
        v["source_to_dll_provenance"] = "OPEN_ANALYSIS_ERROR"
        v["error"] = f"{type(exc).__name__}: {exc}"
        rc = 1
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "worktree", "prune"], cwd=ROOT, capture_output=True)
        shutil.rmtree(worktree, ignore_errors=True)
        (out / "VERIFICATION.json").write_text(json.dumps(v, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary(out, v)

    print(json.dumps({"status": v["status"], "source_to_dll_provenance": v.get("source_to_dll_provenance"), "comparison": v.get("comparison")}, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
