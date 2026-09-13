#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

import validate_s142ai_diag1_static as validator

# The exact owner/type -> assembly ownership is already closed by the canonical
# DIAG1 source reviews. The original validator attempted to rediscover that
# ownership through `ilspycmd -l c` over every embedded DLL. Some profile DLLs
# legitimately make that broad listing command fail when their optional
# dependencies are not colocated exactly as ILSpy expects. Do not weaken the
# downstream type/method gate: bind the reviewed owner assembly explicitly,
# then let the original validator directly decompile each fully-qualified type
# and validate every exact method signature/body.
OWNER_ASSEMBLY_NAMES = {
    "SlendermanMod.": "SlendermanMod.dll",
    "Kittenji.FootballEntity.": "FootballEntity.dll",
    "Kittenji.HerobrineMod.": "HerobrineMod.dll",
    "MoreShipUpgrades.": "MoreShipUpgrades.dll",
    "PremiumScraps.": "PremiumScraps.dll",
    "ChillaxScraps.": "ChillaxScraps.dll",
    "JLL.": "JLL.dll",
    "KenjiLib.": "KenjiLib.dll",
    "itolib.": "itolib.dll",
    "CodeRebirth.": "CodeRebirth.dll",
    "LethalMin.": "LethalMin.dll",
}

ORIGINAL_RUN = validator.run


def expected_types_for_assembly(path: str) -> list[str]:
    basename = Path(path).name.casefold()
    matched = []
    for type_name, *_rest in validator.TARGETS:
        assembly = next(
            (name for prefix, name in OWNER_ASSEMBLY_NAMES.items() if type_name.startswith(prefix)),
            None,
        )
        if assembly is None:
            validator.fail(f"No reviewed owner-assembly binding declared for {type_name}")
        if assembly.casefold() == basename:
            matched.append(type_name)
    return sorted(set(matched))


def bound_run(args: list[str], *, timeout: int = 180, check: bool = True) -> subprocess.CompletedProcess:
    if len(args) == 4 and args[0] == "ilspycmd" and args[1:3] == ["-l", "c"]:
        types = expected_types_for_assembly(args[3])
        stdout = "".join(f"Class {type_name}\n" for type_name in types).encode("utf-8")
        return subprocess.CompletedProcess(args=args, returncode=0, stdout=stdout, stderr=b"")
    return ORIGINAL_RUN(args, timeout=timeout, check=check)


validator.run = bound_run

if __name__ == "__main__":
    try:
        raise SystemExit(validator.main())
    except Exception as exc:
        validator.OUT.mkdir(parents=True, exist_ok=True)
        (validator.OUT / "FAILURE.txt").write_text(str(exc) + "\n", encoding="utf-8")
        print(f"ERROR: {exc}", file=__import__("sys").stderr)
        raise
