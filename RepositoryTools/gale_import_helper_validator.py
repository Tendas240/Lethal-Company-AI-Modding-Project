#!/usr/bin/env python3
"""Regression guard for the canonical Gale import/materialization helper."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "RuntimeTools/ReplaceActiveGaleProfile.ps1"
V24 = ROOT / "RuntimeTools/ReplaceActiveGaleProfileV24.ps1"
GALE_KNOWLEDGE = ROOT / "Knowledge/GALE_PROFILE_WORKFLOW.md"
LIFECYCLE = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"

BASE_REVISION = "2026-09-05-import-uia-v2.2-materialization-proof"
V24_REVISION = "2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain"
BASE_SIGNATURE = f"$helperRevision='{BASE_REVISION}'"
V24_SIGNATURE = f"$helperRevision='{V24_REVISION}'"


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def extract_here_string(source: str, variable: str) -> str:
    match = re.search(rf"\${re.escape(variable)}=@'\r?\n(.*?)\r?\n'@", source, re.S)
    if not match:
        fail(f"could not extract PowerShell here-string ${variable}")
    return match.group(1)


def main() -> int:
    for path in (BASE, V24, GALE_KNOWLEDGE, LIFECYCLE):
        if not path.exists():
            fail(f"required file missing: {path.relative_to(ROOT)}")

    base = BASE.read_text(encoding="utf-8")
    wrapper = V24.read_text(encoding="utf-8")
    gale = GALE_KNOWLEDGE.read_text(encoding="utf-8")
    lifecycle = LIFECYCLE.read_text(encoding="utf-8")

    if base.count(BASE_SIGNATURE) != 1:
        fail("validated v2.2 base helper revision signature is missing or ambiguous")
    if BASE_REVISION not in wrapper or V24_REVISION not in wrapper:
        fail("v2.4 wrapper does not pin both its required base revision and own revision")

    zip_function = extract_here_string(wrapper, "newZipTextFunction")
    materialization_functions = extract_here_string(wrapper, "newMaterializationFunctions")
    target_resolution = extract_here_string(wrapper, "newTargetResolutionBlock")

    direct_reader = "[System.IO.StreamReader]::new($stream,[System.Text.Encoding]::UTF8,$true,4096)"
    if direct_reader not in zip_function:
        fail("v2.4 export reader does not use the direct four-argument StreamReader constructor")
    if "New-Object System.IO.StreamReader -ArgumentList" in zip_function:
        fail("legacy non-terminating StreamReader constructor path remains in v2.4 export reader")
    if "[string]::IsNullOrWhiteSpace($text)" not in zip_function or "refusing to derive dependency contracts" not in zip_function:
        fail("v2.4 export reader does not fail closed on empty/whitespace export text")

    required_materialization_tokens = (
        "[ValidateNotNullOrEmpty()][string]$ExpectedExportText",
        "$baseNamePattern='(?m)^\\s*-\\s*name:\\s*'+[regex]::Escape($basePackage)+'\\s*$'",
        "$lcNamePattern='(?m)^\\s*-\\s*name:\\s*'+[regex]::Escape($lcPackage)+'\\s*$'",
        "BepInEx\\plugins\\loaforc-loaforcsSoundAPI\\**\\me.loaforc.soundapi.dll",
        "BepInEx\\plugins\\loaforc-loaforcsSoundAPI_LethalCompany\\**\\me.loaforc.soundapi.lethalcompany.dll",
        "$hits.Count -ne 1",
        "LethalCompany SoundAPI binding resolved without exactly two critical materialization contracts",
    )
    for token in required_materialization_tokens:
        if token not in materialization_functions:
            fail(f"v2.4 materialization contract missing token: {token}")

    if "$ExpectedExportText.IndexOf($basePackage" in materialization_functions:
        fail("base SoundAPI drift detection uses an unsafe substring test; LC package name has the base name as a prefix")

    required_target_tokens = (
        "if(([string]$build.build_id) -eq $active)",
        "Current/CURRENT_STATE.json?cb=$cache",
        "$state.controllers.runtime_active_build",
        "$state.selected_scope.diagnostic_revision",
        "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
        "$diag.base_build_id",
        "$diag.base_profile",
        "$diag.base_sha256",
        "$diag.build_result",
        "function Get-RepositoryJson {",
        "$RepositoryPath -split '/'",
        "[Uri]::EscapeDataString($_)",
        "${encodedPath}?cb=$cache",
        "-ErrorAction Stop",
        "$diagBuild=Get-RepositoryJson -RepositoryPath ([string]$diag.build_result) -Label \"Diagnostic build_result\"",
        "$diagBuild.build_id",
        "$diagBuild.output_profile",
        "$diagBuild.output_sha256",
        "$diagBuild.profile_name",
        "$state.selected_scope.diagnostic_parent_revision",
        "PUBLISHED_DIAGNOSTIC_PARENT_RUNTIME_EVIDENCE_INGESTED_NOT_ACCEPTED",
        "if(([string]$diag.base_build_id) -eq ([string]$build.build_id))",
        "$parent.base_build_id",
        "$parent.base_profile",
        "$parent.base_sha256",
        "$parent.build_result",
        "Parent diagnostic build_result",
        "Diagnostic build_result profile/SHA disagree with CURRENT_STATE diagnostic_revision",
        "Diagnostic build_result base profile/SHA disagree with CURRENT_STATE diagnostic_revision",
    )
    for token in required_target_tokens:
        if token not in target_resolution:
            fail(f"v2.4 diagnostic runtime-target contract missing token: {token}")

    if "else {" not in target_resolution:
        fail("v2.4 target resolver has no explicit diagnostic-only mismatch branch")
    if "AUTO_BUILD_RESULT gehört zu" in target_resolution:
        fail("legacy unconditional ACTIVE_BUILD/AUTO_BUILD_RESULT mismatch abort remains in target resolver")
    if "[Uri]::EscapeUriString($RepositoryPath)" in target_resolution:
        fail("repository JSON path still uses EscapeUriString instead of segment-wise EscapeDataString")
    if "$encodedPath?cb=$cache" in target_resolution:
        fail("repository JSON URL leaves the path variable undelimited before '?cb'; PowerShell can parse '?' as part of the variable name")
    if 'main/${encodedPath}?cb=$cache' not in target_resolution:
        fail("repository JSON URL does not explicitly delimit the encoded path variable before '?cb'")
    if target_resolution.count("Get-RepositoryJson -RepositoryPath") != 2:
        fail("v2.4.2 target resolver must load exactly the active diagnostic and its one-hop parent build-result through the guarded repository JSON loader")

    zip_start = base.find("function Get-ZipEntryText {")
    materialization_start = base.find("function Get-RequiredCriticalMaterializationPaths {")
    wait_start = base.find("function Wait-ImportedProfileEvidence {")
    if zip_start < 0 or materialization_start <= zip_start or wait_start <= materialization_start:
        fail("v2.2 helper patch boundaries drifted")

    patched = (
        base[:zip_start]
        + zip_function
        + "\n\n"
        + materialization_functions
        + "\n\n"
        + base[wait_start:]
    ).replace(BASE_SIGNATURE, V24_SIGNATURE)

    if V24_SIGNATURE not in patched:
        fail("simulated v2.4 patch did not stamp the v2.4 revision")
    if "New-Object System.IO.StreamReader -ArgumentList" in patched:
        fail("simulated v2.4 helper still contains the defective StreamReader path")
    if patched.count("function Get-ZipEntryText {") != 1:
        fail("simulated v2.4 helper has an ambiguous Get-ZipEntryText definition")
    if patched.count("function Get-RequiredCriticalMaterializationPaths {") != 1:
        fail("simulated v2.4 helper has an ambiguous materialization-contract definition")

    target_marker = '$active=((Invoke-RestMethod -UseBasicParsing -Uri "https://raw.githubusercontent.com/$repo/main/RuntimeInbox/ACTIVE_BUILD.txt?cb=$cache" -Headers $headers).Trim())'
    profile_file_marker = "$profileFile=[IO.Path]::GetFileName($profilePath)"
    target_start = patched.find(target_marker)
    profile_file_start = patched.find(profile_file_marker, target_start)
    if target_start < 0 or profile_file_start <= target_start:
        fail("simulated v2.4 runtime-target patch boundaries drifted")
    patched = patched[:target_start] + target_resolution + "\n\n" + patched[profile_file_start:]

    if "AUTO_BUILD_RESULT gehört zu" in patched:
        fail("simulated v2.4 helper retains the legacy unconditional runtime-target mismatch abort")
    if patched.count("Current/CURRENT_STATE.json?cb=$cache") != 1:
        fail("simulated v2.4 helper does not contain exactly one CURRENT_STATE diagnostic resolver")
    if patched.count("PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED") != 1:
        fail("simulated v2.4 helper diagnostic status guard is missing or ambiguous")
    if "$encodedPath?cb=$cache" in patched:
        fail("simulated v2.4 helper contains the PowerShell '?'-variable interpolation regression")
    if patched.count("Get-RepositoryJson -RepositoryPath") != 2:
        fail("simulated v2.4.2 helper does not retain exactly two guarded diagnostic build-result loads")

    for doc_name, doc in (("Knowledge/GALE_PROFILE_WORKFLOW.md", gale), ("Knowledge/CURRENT_LIFECYCLE.md", lifecycle)):
        if "RuntimeTools/ReplaceActiveGaleProfileV24.ps1" not in doc or V24_REVISION not in doc:
            fail(f"{doc_name} does not route the current Gale workflow to the diagnostic-aware v2.4 revision")

    if "diagnostic_revision" not in gale or "diagnostic_parent_revision" not in gale or "AUTO_BUILD_RESULT" not in gale or "CURRENT_STATE" not in gale:
        fail("Gale workflow authority does not document the fail-closed diagnostic runtime-target/parent-chain exception")
    if "PowerShell" not in gale or "?cb" not in gale or "ErrorAction Stop" not in gale:
        fail("Gale workflow authority does not document the diagnostic build-result URL/fail-closed repair")

    print("PASS: Gale import helper v2.4.2 one-hop diagnostic-parent chain + fail-closed materialization regression contract validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
