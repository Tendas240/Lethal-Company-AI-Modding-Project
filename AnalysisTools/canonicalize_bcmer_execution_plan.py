#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "BuildSpecs/S1.42AI_PLAN.md"
VERIFICATION = ROOT / "SourceEvidence/ShyGuyIsolation/20260912T202218Z-BCMERExecutionExact/VERIFICATION.json"
MARKER = "## Build, evidence and restoration gates"
HEADING = "## Exact BCMER event-execution gate closure — 2026-09-12"

SECTION = """## Exact BCMER event-execution gate closure — 2026-09-12

`SourceEvidence/ShyGuyIsolation/20260912T202218Z-BCMERExecutionExact/REVIEW.md` and `VERIFICATION.json` close the remaining BCMER forced / forced-side / additional / runtime-custom event-execution uncertainty for the exact static S1.42AI stack. Full-assembly run `34716488701` re-fetched exact BCMER 1.71.0, preserved complete C#/IL in artifact `10304724235` (`sha256:35ca8ec171fc40f8d9b0c9d2a9f1af3ad062f54c56c63a22e1424012c20cc116`), and proves exactly three direct `MEvent.Execute()` call sites: normal/additional execution through `ApplyEvents`, direct forced-event execution in `ModifyLevel`, and direct forced `EventsToSpawnWith` execution through `MEvent.GetEvent(...).Execute()`.

Disabled events are removed from the active `EventManager.events` list during config initialization. `API.ForceEvents`, heat forcing, terminal `MEVENT`, internal/public name resolution, and `MEvent.GetEvent` all resolve through that active list. Custom JSON events are loaded only when `Enable Custom Events?` is true; the complete assembly contains one `Directory.GetFiles(customEventsFolder)` load site, zero `FileSystemWatcher` occurrences, and no later custom-event reload path. The planned diagnostic also requires ShyGuy `Events To Spawn With` empty, custom events disabled, heat forcing disabled/empty, one normal draw and no bonus draws.

Installed-set consumer run `34716828573` scanned all 183 enabled packages plus five embedded project DLLs, covering 224 managed DLLs, and preserved aggregate artifact `10303989823` (`sha256:74303c27f635690df1178e30be7430c0146510cd3187ce42465b15f101fe4b3d`). BCMER itself is the only raw candidate. External callers of `API.ForceEvents`, `API.RegenerateEvents`, `MEvent.Execute`, `MEvent.GetEvent`, and `GeneralCustomEvent` construction are all zero; external static reflection-like BCMER execution candidates are zero. Arbitrary runtime-generated reflection remains outside static proof, with no static indicator found in the exact installed set.

Therefore the **forced / forced-side / additional / runtime-custom BCMER Execution Gate is CLOSED for the exact static S1.42AI stack under the planned DIAG1 configuration**, and **no dedicated BCMER event-execution Harmony patch is required for S1.42AI-DIAG1**. Do not broadly patch or skip `MEvent.Execute()`, `EventManager.ModifyLevel()`, or the BCMER selection/execution lifecycle; those broader surfaces remain prohibited by `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md` and would add unnecessary regression risk.

Patch safety remains **PARTIAL / NOT_BUILD_READY**. Remaining bounded work is now: (1) preserve/verify exact Shy Guy runtime identity and project source-to-DLL provenance required by the final narrow prevention design; then (2) select and statically validate the smallest host/client-safe enemy-spawn interception points across the already reviewed owner paths. No gameplay run, DIAG1 implementation/build, Gale import, build-controller transition or runtime-controller transition is authorized by this checkpoint. S1.42AI-DIAG1 remains NOT_BUILT.

"""


def main() -> None:
    verification = json.loads(VERIFICATION.read_text(encoding="utf-8"))
    gates = verification["gates"]
    assert gates["bcmer_forced_forced_side_additional_runtime_custom_execution_gate_open"] is False
    assert gates["dedicated_bcmer_event_execution_patch_required"] is False
    assert gates["broad_mevent_execute_patch_allowed"] is False
    assert gates["broad_eventmanager_modifylevel_skip_allowed"] is False
    assert gates["broad_bcmer_selection_execution_lifecycle_patch_allowed"] is False
    assert gates["shyguy_runtime_identity_source_to_dll_provenance_gate_open"] is True
    assert gates["final_host_client_safe_interception_selection_gate_open"] is True
    assert gates["patch_safety_build_ready"] is False
    assert gates["diag1_build_authorized"] is False

    text = PLAN.read_text(encoding="utf-8")
    if HEADING in text:
        raise RuntimeError("BCMER execution closure section already present")
    if text.count(MARKER) != 1:
        raise RuntimeError("Expected exactly one build-gate marker")
    text = text.replace(MARKER, SECTION + MARKER)
    PLAN.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
