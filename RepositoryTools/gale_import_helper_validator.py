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
V24_REVISION = "2026-09-05-import-uia-v2.4-export-read-fail-closed-materialization-proof"
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

    direct_reader = "[System.IO.StreamReader]::new($stream,[System.Text.Encoding]::UTF8,$true,4096)"
    if direct_reader not in zip_function:
        fail("v2.4 export reader does not use the direct four-argument StreamReader constructor")
    if "New-Object System.IO.StreamReader -ArgumentList" in zip_function:
        fail("legacy non-terminating StreamReader constructor path remains in v2.4 export reader")
    if "[string]::IsNullOrWhiteSpace($text)" not in zip_function or "refusing to derive dependency contracts" not in zip_function:
        fail("v2.4 export reader does not fail closed on empty/whitespace export text")

    required_materialization_tokens = (
        "[ValidateNotNullOrEmpty()][string]$ExpectedExportText",
        "BepInEx\\plugins\\loaforc-loaforcsSoundAPI\\**\\me.loaforc.soundapi.dll",
        "BepInEx\\plugins\\loaforc-loaforcsSoundAPI_LethalCompany\\**\\me.loaforc.soundapi.lethalcompany.dll",
        "$hits.Count -ne 1",
        "LethalCompany SoundAPI binding resolved without exactly two critical materialization contracts",
    )
    for token in required_materialization_tokens:
        if token not in materialization_functions:
            fail(f"v2.4 materialization contract missing token: {token}")

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

    for doc_name, doc in (("Knowledge/GALE_PROFILE_WORKFLOW.md", gale), ("Knowledge/CURRENT_LIFECYCLE.md", lifecycle)):
        if "RuntimeTools/ReplaceActiveGaleProfileV24.ps1" not in doc or V24_REVISION not in doc:
            fail(f"{doc_name} does not route the current Gale workflow to v2.4")

    print("PASS: Gale import helper v2.4 fail-closed regression contract validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
