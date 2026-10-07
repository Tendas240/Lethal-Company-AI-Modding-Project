#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PROFILE = ROOT / "Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z"
PROFILE = Path(os.environ["DIAG1_MATERIALIZED_PROFILE"]).resolve()
STATIC = Path(os.environ["DIAG1_STATIC_OUT"]).resolve() / "STATIC_VALIDATION.json"
OUT = Path(os.environ["DIAG1_MATERIALIZED_APPLICABILITY_OUT"]).resolve()
EXPECTED_BASE_SHA = "d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2"
EXPECTED_GUID = "kite.ZelevatorCode"
EXPECTED_ASSEMBLY = "kite.ZelevatorCode"
EXPECTED_TYPE = "ElevatorMod.Patches.EndlessElevator"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized_export(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        text = z.read("export.r2x").decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    hits = [line for line in text.split("\n") if re.match(r"^\s*profileName\s*:", line)]
    if len(hits) != 1:
        raise RuntimeError(f"Expected exactly one profileName in {path}, found {len(hits)}")
    return re.sub(r"(?m)^(\s*)profileName\s*:.*$", r"\1profileName: <NORMALIZED>", text)


def main() -> int:
    if sha256_file(BASE_PROFILE) != EXPECTED_BASE_SHA:
        raise RuntimeError("S1.42AI base profile SHA mismatch")
    static = json.loads(STATIC.read_text(encoding="utf-8"))
    if static.get("status") != "PASS_PREBUILD_STATIC_GATE":
        raise RuntimeError(f"Static gate is not green: {static.get('status')}")
    contract = static.get("checks", {}).get("endless_elevator_applicability", {})
    expected = {
        "applicability": "NOT_APPLICABLE_DEPENDENCY_ABSENT",
        "dependency_guid": EXPECTED_GUID,
        "provider_assembly": EXPECTED_ASSEMBLY,
        "provider_type": EXPECTED_TYPE,
        "required_when_dependency_present": True,
        "missing_or_drifted_target_when_applicable": "FAIL_CLOSED",
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            raise RuntimeError(f"Materialized applicability contract drift for {key}: {contract.get(key)!r} != {value!r}")
    if normalized_export(PROFILE) != normalized_export(BASE_PROFILE):
        raise RuntimeError("Materialized profile package/export set differs from exact S1.42AI applicability-bound base")
    report = {
        "status": "PASS_MATERIALIZED_ENDLESS_ELEVATOR_APPLICABILITY",
        "materialized_profile": str(PROFILE),
        "materialized_profile_sha256": sha256_file(PROFILE),
        "base_profile_sha256": EXPECTED_BASE_SHA,
        "applicability": contract["applicability"],
        "dependency_guid": EXPECTED_GUID,
        "provider_assembly": EXPECTED_ASSEMBLY,
        "provider_type": EXPECTED_TYPE,
        "required_when_dependency_present": True,
        "missing_or_drifted_target_when_applicable": "FAIL_CLOSED",
        "package_set_equals_bound_base": True,
        "static_gate_status": static["status"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
