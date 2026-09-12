#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "BuildSpecs/S1.42AI_PLAN.md"
VERIFICATION = ROOT / "SourceEvidence/NativeSpawnOwners/20260912T200049Z-CrossAssemblyConsumers/VERIFICATION.json"
MARKER = "## Build, evidence and restoration gates"
HEADING = "## Cross-assembly spawn-API consumer review — 2026-09-12"

SECTION = """## Cross-assembly spawn-API consumer review — 2026-09-12

`SourceEvidence/NativeSpawnOwners/20260912T200049Z-CrossAssemblyConsumers/REVIEW.md` and `VERIFICATION.json` close the two named public/generic cross-assembly consumer gates against the exact S1.42AI installed assembly set. Successful Actions run `34715820639` scanned all 183 enabled package records plus all five embedded project DLLs, covering 224 managed DLLs, and preserved the aggregate in artifact `10304508813` (`sha256:733bb10b253372afe704c3c01e8c4852e9faf06c141c578d162db2e5cad55cd1`). Candidate assemblies were fully decompiled with pinned ILSpy 11.0.0.9375.

No external assembly directly calls a SnowyLib spawn API and no external SnowyLib spawn reflection-like candidate was found. Likewise, no external assembly calls `InteractiveTerminalAPI.Tools.SpawnMob` and no reflection-like candidate for that method was found. Four packages declare InteractiveTerminalAPI dependencies, but dependency metadata alone is not a call. The sole external raw candidate, exact Lategame Upgrades 3.14.1, resolves all three `SpawnMob` IL call sites to its already-reviewed own `MoreShipUpgrades.Misc.Util.Tools::SpawnMob`; it has zero calls to InteractiveTerminalAPI SpawnMob and zero SnowyLib spawn calls.

Therefore the SnowyLib and InteractiveTerminalAPI SpawnMob **cross-assembly consumer gates are CLOSED for the exact static S1.42AI installed assembly set**. This does not redefine either provider as safe to suppress broadly: both remain shared infrastructure, and future package/version/profile changes must reopen this installed-set conclusion. Arbitrary runtime-generated reflection strings are outside static proof; no static direct-call or reflection indicator was found in the captured set.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) close the exact BCMER forced/forced-side/additional/runtime-custom event execution gate; (2) preserve/verify the exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (3) select and statically validate the smallest host/client-safe interception points. No gameplay run, build trigger or controller transition is requested at this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT.

"""


def main() -> None:
    verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
    gates = verification["gates"]
    assert gates["snowylib_cross_assembly_consumer_gate_open"] is False
    assert gates["interactive_terminal_api_cross_assembly_consumer_gate_open"] is False
    assert gates["bcmer_forced_additional_runtime_custom_gate_open"] is True
    assert gates["shyguy_runtime_identity_source_to_dll_provenance_gate_open"] is True
    assert gates["final_host_client_safe_interception_selection_gate_open"] is True
    assert gates["diag1_build_authorized"] is False

    text = PLAN.read_text(encoding="utf-8")
    if HEADING in text:
        raise RuntimeError("Cross-consumer section already present")
    if text.count(MARKER) != 1:
        raise RuntimeError("Expected exactly one build-gate marker")
    text = text.replace(MARKER, SECTION + MARKER)
    PLAN.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
