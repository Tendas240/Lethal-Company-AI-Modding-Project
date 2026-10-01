#!/usr/bin/env python3
"""Fail-closed project guard for Gale/Windows runtime path budgets."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PureWindowsPath

ROOT = Path(__file__).resolve().parents[1]
REFERENCE_PROFILE_ROOT = PureWindowsPath(
    r"C:\Users\Milan\AppData\Roaming\com.kesomannen.gale\lethal-company\profiles"
)
SAFE_RUNTIME_PATH_CHARS = 255

CRITICAL_RUNTIME_PATHS = (
    (
        "LC Office V81 preloader",
        PureWindowsPath(
            r"BepInEx\patchers\MonkeySolutions-LC_Office_v81_Unofficial_Compatibility_Fix"
            r"\LCOfficeV81Preloader\LCOfficeV81Preloader.dll"
        ),
    ),
    (
        "loaforcsSoundAPI LethalCompany binding",
        PureWindowsPath(
            r"BepInEx\plugins\loaforc-loaforcsSoundAPI_LethalCompany"
            r"\loaforcsSoundAPI_LethalCompany\me.loaforc.soundapi.lethalcompany.dll"
        ),
    ),
)

LEGACY_BLOCKED_IDENTITIES = {
    "S1.42AK-BMDSFIX1-DIAG1": "LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector",
    "S1.42AK-BMAFDIAG1": "LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic",
}


def projections(profile_name: str, profile_root: PureWindowsPath = REFERENCE_PROFILE_ROOT):
    target = profile_root / profile_name
    return [
        (label, str(target / rel), len(str(target / rel)))
        for label, rel in CRITICAL_RUNTIME_PATHS
    ]


def violations(profile_name: str, profile_root: PureWindowsPath = REFERENCE_PROFILE_ROOT):
    return [row for row in projections(profile_name, profile_root) if row[2] > SAFE_RUNTIME_PATH_CHARS]


def load_spec(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_spec(path: Path, *, preserve_exact_legacy_record: bool) -> list[str]:
    spec = load_spec(path)
    profile_name = str(spec.get("profile_name", "")).strip()
    build_id = str(spec.get("build_id", "")).strip()
    if not profile_name:
        return [f"{path}: missing profile_name"]

    bad = violations(profile_name)
    if not bad:
        longest = max(projections(profile_name), key=lambda x: x[2])
        print(
            f"PASS: {path} build_id={build_id or '<none>'} "
            f"max_projected_runtime_path={longest[2]}/{SAFE_RUNTIME_PATH_CHARS}"
        )
        return []

    if preserve_exact_legacy_record and LEGACY_BLOCKED_IDENTITIES.get(build_id) == profile_name:
        lengths = ",".join(str(x[2]) for x in bad)
        print(
            f"PRESERVED LEGACY BLOCK: {path} build_id={build_id} "
            f"over_budget_lengths={lengths}; exact historical spec may remain but must not be rebuilt"
        )
        return []

    errors = []
    for label, full_path, length in bad:
        errors.append(
            f"{path}: projected Gale runtime path exceeds safe project budget "
            f"({length}>{SAFE_RUNTIME_PATH_CHARS}) for {label}: {full_path}"
        )
    return errors


def self_test() -> None:
    known = {
        "LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic": (260, 262),
        "LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector": (260, 262),
        "LC V1 S1.42AK-D1P1": (215, 217),
        "LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic": (253, 255),
    }
    for name, expected in known.items():
        actual = tuple(x[2] for x in projections(name))
        if actual != expected:
            raise AssertionError(f"{name}: expected {expected}, got {actual}")
    if not violations("LC V1 S1.42AK-BMAFDIAG1 Black Mesa Abandoned Foundry Diagnostic"):
        raise AssertionError("BMAFDIAG1 long identity must be rejected")
    if violations("LC V1 S1.42AK-D1P1"):
        raise AssertionError("short DIAG1PATH1 identity must pass")
    if violations("LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic"):
        raise AssertionError("known successful 255-character boundary identity must remain permitted")
    print("PASS: Gale runtime path-length guard self-test")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", type=Path, help="Validate one build spec fail-closed; legacy exceptions are not allowed.")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        if args.spec is None:
            return 0

    if args.spec is not None:
        paths = [args.spec]
        preserve_legacy = False
    else:
        paths = sorted((ROOT / "BuildSpecs").glob("*.json"))
        preserve_legacy = True

    errors: list[str] = []
    for path in paths:
        errors.extend(validate_spec(path, preserve_exact_legacy_record=preserve_legacy))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: Gale runtime path-length budget validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
