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
HISTORICAL_DOTNET_SDK = "8.0.424"
PINNED_ILSPY = "11.0.0.9375"

SOURCE_REL = "Patches/S139CompatibilityFixes/Plugin.cs"
CSPROJ_REL = "Patches/S139CompatibilityFixes/S139CompatibilityFixes.csproj"
HISTORICAL_HELPER_REL = "RepositoryTools/_temporary_build_s142ah.py"
HISTORICAL_WORKFLOW_REL = ".github/workflows/atomic-build-s142ah-v8-final.yml"
PROFILE_BUILDER_REL = "BuildSystem/profile_builder.py"
BUILT_DLL_REL = "Patches/S139CompatibilityFixes/bin/Release/netstandard2.1/S139CompatibilityFixes.dll"

AH_PROFILE_REL = "Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z"
AH_PROFILE_SHA256 = "06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e"
AI_PROFILE_REL = "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
AI_PROFILE_SHA256 = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
DLL_MEMBER = "BepInEx/plugins/Tendas-S139CompatibilityFixes/S139CompatibilityFixes.dll"
RUNTIME_DLL_SHA256 = "bf86f338dba1428327088f0aaa2af8d9816f647c3b3c12214a5fc52db8e34573"
SOURCE_SHA256 = "2b8a326383ea5f39a69f7b370836180509dc5a34ec0c1b98dbe0734f4f87707d"
CSPROJ_SHA256 = "c51a47a8eb502df7a787c2a08ed90962e284fa68e4557c8bc022bc56e68dd39b"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(args: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True)


def require_success(proc: subprocess.CompletedProcess[str], label: str) -> str:
    if proc.returncode != 0:
        raise RuntimeError(
            f"{label} failed with exit code {proc.returncode}\n"
            f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout


def git_show(commit: str, path: str) -> bytes:
    proc = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"git show failed for {commit}:{path}: "
            f"{proc.stderr.decode('utf-8', errors='replace')}"
        )
    return proc.stdout


def require_hash(label: str, data: bytes, expected: str) -> str:
    actual = sha_bytes(data)
    if actual != expected:
        raise RuntimeError(f"{label} SHA-256 mismatch: expected {expected}, got {actual}")
    return actual


def extract_member(profile_path: Path, expected_profile_sha: str, destination: Path) -> dict:
    actual_profile_sha = sha_file(profile_path)
    if actual_profile_sha != expected_profile_sha:
        raise RuntimeError(
            f"{profile_path} SHA-256 mismatch: expected {expected_profile_sha}, got {actual_profile_sha}"
        )
    with zipfile.ZipFile(profile_path, "r") as archive:
        matches = [i for i in archive.infolist() if i.filename == DLL_MEMBER]
        if len(matches) != 1:
            raise RuntimeError(f"{profile_path}: expected one {DLL_MEMBER}, found {len(matches)}")
        data = archive.read(matches[0])
    dll_sha = require_hash(f"{profile_path}:{DLL_MEMBER}", data, RUNTIME_DLL_SHA256)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return {
        "profile": str(profile_path.relative_to(ROOT)).replace("\\", "/"),
        "profile_sha256": actual_profile_sha,
        "dll_member": DLL_MEMBER,
        "dll_sha256": dll_sha,
        "dll_size": len(data),
    }


def decompile(ilspy: Path, assembly: Path, *, il: bool) -> tuple[str, str]:
    cmd = [str(ilspy)]
    if il:
        cmd.append("--ilcode")
    cmd.append(str(assembly))
    proc = run(cmd)
    text = require_success(proc, f"ILSpy {'IL' if il else 'C#'} decompile for {assembly.name}")
    return text.replace("\r\n", "\n").replace("\r", "\n"), proc.stderr


def write_summary(output_dir: Path, verification: dict) -> None:
    c = verification.get("comparison", {})
    lines = [
        "# S139CompatibilityFixes Source-to-DLL Exact Rebuild Review",
        "",
        f"- Status: `{verification.get('status', 'UNKNOWN')}`",
        f"- Analysis head: `{verification.get('analysis_head', '<unknown>')}`",
        f"- Historical successful build run: `{BUILD_RUN_ID}`",
        f"- Historical pre-build head: `{PREBUILD_COMMIT}`",
        f"- Historical build commit: `{BUILD_COMMIT}`",
        f"- Historical SDK: `{HISTORICAL_DOTNET_SDK}`",
        f"- Runtime DLL SHA-256: `{RUNTIME_DLL_SHA256}`",
        f"- Rebuilt DLL SHA-256: `{c.get('rebuilt_sha256', '<unavailable>')}`",
        f"- Byte-identical: `{c.get('byte_identical', False)}`",
        f"- Full C# decompile identical: `{c.get('csharp_identical', False)}`",
        f"- Full IL decompile identical: `{c.get('il_identical', False)}`",
        "",
        "The rebuild is executed from a detached worktree at the exact historical pre-build commit, not from the analysis branch head. This prevents current Git revision metadata from contaminating the comparison.",
        "",
        "This is read-only analysis evidence. It does not authorize DIAG1 implementation, profile build, controller changes, or runtime testing.",
        "",
    ]
    if verification.get("error"):
        lines.extend(["## Error", "", "```text", verification["error"], "```", ""])
    (output_dir / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--ilspy", required=True, type=Path)
    args = parser.parse_args()

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    ilspy = (ROOT / args.ilspy).resolve() if not args.ilspy.is_absolute() else args.ilspy.resolve()
    worktree = output_dir.parent / "s139-historical-prebuild-worktree"

    verification: dict = {
        "schema_version": 2,
        "purpose": "S1.42AI-DIAG1 project-local S139 source-to-runtime-DLL exact rebuild review",
        "status": "RUNNING",
        "historical_build": {
            "workflow_run": BUILD_RUN_ID,
            "prebuild_commit": PREBUILD_COMMIT,
            "build_commit": BUILD_COMMIT,
            "toolchain": {
                "runner": "ubuntu-latest",
                "historical_runner_image": "ubuntu-24.04 / 20260831.293.1",
                "dotnet_sdk": HISTORICAL_DOTNET_SDK,
                "python": "3.12.14",
                "configuration": "Release",
                "project": CSPROJ_REL,
                "built_file": BUILT_DLL_REL,
            },
        },
        "expected": {
            "source_sha256": SOURCE_SHA256,
            "csproj_sha256": CSPROJ_SHA256,
            "runtime_dll_sha256": RUNTIME_DLL_SHA256,
            "s142ah_profile_sha256": AH_PROFILE_SHA256,
            "s142ai_profile_sha256": AI_PROFILE_SHA256,
            "ilspy_version": PINNED_ILSPY,
        },
    }

    try:
        analysis_head = require_success(run(["git", "rev-parse", "HEAD"]), "git rev-parse HEAD").strip()
        verification["analysis_head"] = analysis_head
        verification["github_run_id"] = os.environ.get("GITHUB_RUN_ID")
        verification["github_run_attempt"] = os.environ.get("GITHUB_RUN_ATTEMPT")

        current_source = (ROOT / SOURCE_REL).read_bytes()
        current_csproj = (ROOT / CSPROJ_REL).read_bytes()
        prebuild_source = git_show(PREBUILD_COMMIT, SOURCE_REL)
        build_source = git_show(BUILD_COMMIT, SOURCE_REL)
        prebuild_csproj = git_show(PREBUILD_COMMIT, CSPROJ_REL)
        build_csproj = git_show(BUILD_COMMIT, CSPROJ_REL)
        for label, data, expected in [
            ("current source", current_source, SOURCE_SHA256),
            ("pre-build source", prebuild_source, SOURCE_SHA256),
            ("build-commit source", build_source, SOURCE_SHA256),
            ("current csproj", current_csproj, CSPROJ_SHA256),
            ("pre-build csproj", prebuild_csproj, CSPROJ_SHA256),
            ("build-commit csproj", build_csproj, CSPROJ_SHA256),
        ]:
            require_hash(label, data, expected)
        if not (current_source == prebuild_source == build_source):
            raise RuntimeError("Plugin.cs bytes differ across current/pre-build/build-commit lineage")
        if not (current_csproj == prebuild_csproj == build_csproj):
            raise RuntimeError("S139CompatibilityFixes.csproj bytes differ across current/pre-build/build-commit lineage")

        helper = git_show(PREBUILD_COMMIT, HISTORICAL_HELPER_REL).decode("utf-8")
        builder = git_show(PREBUILD_COMMIT, PROFILE_BUILDER_REL).decode("utf-8")
        workflow = git_show(PREBUILD_COMMIT, HISTORICAL_WORKFLOW_REL).decode("utf-8")
        required_helper = [
            '"project": "Patches/S139CompatibilityFixes/S139CompatibilityFixes.csproj"',
            '"configuration": "Release"',
            '"built_file": "Patches/S139CompatibilityFixes/bin/Release/netstandard2.1/S139CompatibilityFixes.dll"',
            '"archive_path": DLL_ARCHIVE_PATH',
        ]
        missing = [m for m in required_helper if m not in helper]
        if missing:
            raise RuntimeError(f"Historical helper contract markers missing: {missing}")
        exact_builder = 'subprocess.run(["dotnet", "build", str(project), "-c", config], check=True)'
        if exact_builder not in builder:
            raise RuntimeError("Historical profile builder does not prove exact dotnet build <project> -c <config> path")
        for marker in ['runs-on: ubuntu-latest', 'dotnet-version: "8.0.x"', 'python-version: "3.12"']:
            if marker not in workflow:
                raise RuntimeError(f"Historical workflow toolchain marker missing: {marker}")

        verification["source_lineage"] = {
            "current_source_sha256": sha_bytes(current_source),
            "prebuild_source_sha256": sha_bytes(prebuild_source),
            "build_commit_source_sha256": sha_bytes(build_source),
            "current_csproj_sha256": sha_bytes(current_csproj),
            "prebuild_csproj_sha256": sha_bytes(prebuild_csproj),
            "build_commit_csproj_sha256": sha_bytes(build_csproj),
            "source_bytes_identical": current_source == prebuild_source == build_source,
            "csproj_bytes_identical": current_csproj == prebuild_csproj == build_csproj,
            "historical_helper_sha256": sha_bytes(helper.encode("utf-8")),
            "historical_profile_builder_sha256": sha_bytes(builder.encode("utf-8")),
            "historical_workflow_sha256": sha_bytes(workflow.encode("utf-8")),
        }

        reference_dir = output_dir / "reference"
        rebuilt_dir = output_dir / "rebuilt"
        ah_ref = reference_dir / "S1.42AH" / "S139CompatibilityFixes.dll"
        ai_ref = reference_dir / "S1.42AI" / "S139CompatibilityFixes.dll"
        verification["profiles"] = {
            "S1.42AH": extract_member(ROOT / AH_PROFILE_REL, AH_PROFILE_SHA256, ah_ref),
            "S1.42AI": extract_member(ROOT / AI_PROFILE_REL, AI_PROFILE_SHA256, ai_ref),
        }
        if ah_ref.read_bytes() != ai_ref.read_bytes():
            raise RuntimeError("S1.42AH and S1.42AI embedded compatibility DLL bytes differ")

        current_sdk = require_success(run(["dotnet", "--version"]), "dotnet --version").strip()
        verification["active_dotnet_sdk"] = current_sdk
        if current_sdk != HISTORICAL_DOTNET_SDK:
            raise RuntimeError(
                f"SDK mismatch: historical run used {HISTORICAL_DOTNET_SDK}; analysis environment resolved {current_sdk}"
            )
        (output_dir / "DOTNET_INFO.txt").write_text(
            require_success(run(["dotnet", "--info"]), "dotnet --info"), encoding="utf-8"
        )

        if worktree.exists():
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, capture_output=True)
            if worktree.exists():
                shutil.rmtree(worktree)
        require_success(
            run(["git", "worktree", "add", "--detach", str(worktree), PREBUILD_COMMIT]),
            "create detached historical worktree",
        )
        worktree_head = require_success(run(["git", "rev-parse", "HEAD"], cwd=worktree), "historical worktree HEAD").strip()
        if worktree_head != PREBUILD_COMMIT:
            raise RuntimeError(f"Historical worktree head mismatch: expected {PREBUILD_COMMIT}, got {worktree_head}")
        verification["historical_worktree_head"] = worktree_head

        worktree_sdk = require_success(run(["dotnet", "--version"], cwd=worktree), "historical worktree dotnet --version").strip()
        if worktree_sdk != HISTORICAL_DOTNET_SDK:
            raise RuntimeError(f"Historical worktree SDK mismatch: expected {HISTORICAL_DOTNET_SDK}, got {worktree_sdk}")

        for d in (worktree / "Patches/S139CompatibilityFixes/bin", worktree / "Patches/S139CompatibilityFixes/obj"):
            if d.exists():
                shutil.rmtree(d)
        build_proc = run(["dotnet", "build", CSPROJ_REL, "-c", "Release"], cwd=worktree)
        (output_dir / "BUILD_STDOUT.txt").write_text(build_proc.stdout, encoding="utf-8")
        (output_dir / "BUILD_STDERR.txt").write_text(build_proc.stderr, encoding="utf-8")
        require_success(build_proc, "exact historical-head S139 Release rebuild")

        built_dll = worktree / BUILT_DLL_REL
        if not built_dll.exists():
            raise RuntimeError(f"Expected rebuilt DLL missing: {built_dll}")
        rebuilt_copy = rebuilt_dir / "S139CompatibilityFixes.dll"
        rebuilt_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(built_dll, rebuilt_copy)

        ilspy_version = require_success(run([str(ilspy), "--version"]), "ilspycmd --version").strip()
        (output_dir / "ILSPY_VERSION.txt").write_text(ilspy_version + "\n", encoding="utf-8")
        if PINNED_ILSPY not in ilspy_version:
            raise RuntimeError(f"Unexpected ILSpy version: expected {PINNED_ILSPY}, got {ilspy_version!r}")

        runtime_csharp, runtime_csharp_err = decompile(ilspy, ai_ref, il=False)
        rebuilt_csharp, rebuilt_csharp_err = decompile(ilspy, rebuilt_copy, il=False)
        runtime_il, runtime_il_err = decompile(ilspy, ai_ref, il=True)
        rebuilt_il, rebuilt_il_err = decompile(ilspy, rebuilt_copy, il=True)
        (reference_dir / "S1.42AI" / "FULL_CSHARP.txt").write_text(runtime_csharp, encoding="utf-8")
        (rebuilt_dir / "FULL_CSHARP.txt").write_text(rebuilt_csharp, encoding="utf-8")
        (reference_dir / "S1.42AI" / "FULL_IL.txt").write_text(runtime_il, encoding="utf-8")
        (rebuilt_dir / "FULL_IL.txt").write_text(rebuilt_il, encoding="utf-8")
        (reference_dir / "S1.42AI" / "ILSPY_STDERR.txt").write_text(
            runtime_csharp_err + "\n--- IL ---\n" + runtime_il_err, encoding="utf-8"
        )
        (rebuilt_dir / "ILSPY_STDERR.txt").write_text(
            rebuilt_csharp_err + "\n--- IL ---\n" + rebuilt_il_err, encoding="utf-8"
        )

        runtime_bytes = ai_ref.read_bytes()
        rebuilt_bytes = rebuilt_copy.read_bytes()
        verification["comparison"] = {
            "runtime_sha256": sha_bytes(runtime_bytes),
            "runtime_size": len(runtime_bytes),
            "rebuilt_sha256": sha_bytes(rebuilt_bytes),
            "rebuilt_size": len(rebuilt_bytes),
            "byte_identical": runtime_bytes == rebuilt_bytes,
            "runtime_csharp_sha256": sha_bytes(runtime_csharp.encode("utf-8")),
            "rebuilt_csharp_sha256": sha_bytes(rebuilt_csharp.encode("utf-8")),
            "csharp_identical": runtime_csharp == rebuilt_csharp,
            "runtime_il_sha256": sha_bytes(runtime_il.encode("utf-8")),
            "rebuilt_il_sha256": sha_bytes(rebuilt_il.encode("utf-8")),
            "il_identical": runtime_il == rebuilt_il,
        }

        if runtime_bytes == rebuilt_bytes:
            verification["status"] = "PASS_BYTE_IDENTICAL_HISTORICAL_HEAD_REBUILD"
            verification["source_to_dll_provenance"] = "CLOSED_EXACT_BYTE_REBUILD"
            rc = 0
        else:
            verification["status"] = "FAIL_HISTORICAL_HEAD_REBUILD_NOT_BYTE_IDENTICAL"
            verification["source_to_dll_provenance"] = "OPEN_REVIEW_REQUIRED"
            rc = 2

    except Exception as exc:
        verification["status"] = "FAIL_ANALYSIS_ERROR"
        verification["source_to_dll_provenance"] = "OPEN_ANALYSIS_ERROR"
        verification["error"] = f"{type(exc).__name__}: {exc}"
        rc = 1
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, capture_output=True)
        subprocess.run(["git", "worktree", "prune"], cwd=ROOT, capture_output=True)
        if worktree.exists():
            shutil.rmtree(worktree, ignore_errors=True)
        (output_dir / "VERIFICATION.json").write_text(
            json.dumps(verification, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        write_summary(output_dir, verification)

    print(json.dumps({
        "status": verification["status"],
        "source_to_dll_provenance": verification.get("source_to_dll_provenance"),
        "comparison": verification.get("comparison"),
        "verification": str(output_dir / "VERIFICATION.json"),
    }, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
