#!/usr/bin/env python3
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "Current/CURRENT_STATE.json"
LIFECYCLE = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
MAP = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
RECON = ROOT / "Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md"

NEXT = (
    "Prepare and execute a separately bounded inactive review-build checkpoint for S1.42AK-BMAFDIAG1 from the exact source/static bytes integrated by PR #198, deriving any review profile directly from exact accepted S1.42AK. The review build may compile/test the successor and materialize the repository-proven Abandoned Foundry owner-default LLL content-configuration section with Enable Content Configuration = true plus exactly Black Mesa:100 appended to the preserved Manual Level Names mapping. It must prove the archive/config delta fail-closed and must not publish bytes, modify/import Gale, runtime-arm BMAFDIAG1, start gameplay, alter S1.42AB normalization, duplicate-register Foundry, change unrelated pairings/size rules, or change BMDSFIX1 acceptance."
)

RECON_TEXT = """# S1.42AK-BMAFDIAG1 Source/Static Integration Reconciliation

**Date:** 2026-09-30
**Status:** SOURCE/STATIC PASS / MAIN-INTEGRATED / NOT BUILT / NOT PUBLISHED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / BLACK MESA x ABANDONED FOUNDRY NOT YET PROVEN
**Accepted gameplay baseline:** S1.42AK — unchanged
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted / separate passive target gate

## Decision

The separately versioned `S1.42AK-BMAFDIAG1` Black Mesa x Abandoned Foundry diagnostic has completed its bounded repository-native source/static design-and-implementation checkpoint and is integrated on `main`.

This decision is deliberately limited to source/static validity. It does **not** claim that a BMAFDIAG1 DLL has been compiled, that a review/Gale profile has been built, that the Foundry LLL content-configuration delta has been materialized into an artifact, that any bytes have been published/imported, or that a runtime test is authorized.

## Exact approved source contract

BMAFDIAG1 is a separately versioned diagnostic successor using the proven BMGHDIAG3 provenance/runtime-identity/topology architecture as source-contract precedent while targeting exact `Abandoned Foundry` / `FoundryFlow` on exact `Black Mesa`.

The diagnostic plugin itself does not create availability. Before any singleton reduction it must prove that LLL already returned exactly one `Abandoned Foundry` wrapper whose `DungeonFlow` asset is `FoundryFlow` and whose post-normalizer rarity is exactly `100`. Missing/duplicate/wrong-identity/wrong-rarity/unknown-caller conditions fail closed and preserve normal behavior.

Any later review profile must derive directly from exact accepted `S1.42AK`, never from BMGHDIAG3 or BMDSFIX1. The only authorized later availability semantic delta is the repository-proven owner-supported LLL content-configuration path: materialize the historical owner-default `[Custom Dungeon:  Abandoned Foundry]` section, set `Enable Content Configuration = true`, and append exactly `Black Mesa:100` to the existing owner Manual Level Names mapping while preserving all other owner values. No `External:100`, size-rule change, duplicate section/registration, foreign pairing drift, normalizer modification, or Black-Mesa-owner reverse-direction config change is authorized.

The runtime observation boundary remains post-native/read-only `EntranceTeleport.TeleportPlayer()` instrumentation with required IDs `0..3`; no teleport, pairing, renumbering or entrance-state write is introduced.

## Exact verification

Final source PR: **#198**
Final PR head: `2991341d46164e1bcb4e81f7ba34f4f3aeebc7f7`

Exact-head gates on that final head:

- `S1.42AK BMAFDIAG1 source static design gate` run `36708620109` / run number `2` — **success**;
- `Knowledge Architecture` run `36708620101` / run number `860` — **success**.

PR #198 merged to `main` at:

`eed4bcb426454bb88ac1ed70151cec454bbb8122`

Permanent exact-main Knowledge Architecture gate:

- run `36708806226`;
- run number `861`;
- event `push`;
- head SHA `eed4bcb426454bb88ac1ed70151cec454bbb8122`;
- result **success**.

The first BMAFDIAG1 source-static PR run on superseded head `dab9c1a3c62f2a7762dc3b25d61cd1762eb54812` failed only because the README omitted the explicit `S1.42AK-BMDSFIX1` profile-parent boundary required by the validator. The README was corrected on the final head above; that earlier validator-only failure is superseded and is not qualification evidence for the integrated source.

## Lifecycle consequence

- S1.42AK remains the sole accepted gameplay baseline.
- S1.42AK-BMDSFIX1 remains the active gameplay candidate / not accepted; its regular exact Black Mesa x `DeepSewersFlow` qualification remains passive, outstanding and unwaived with no dedicated reroll released.
- BMGHDIAG3 remains historical Black Mesa x Greenhouse runtime-compatibility PASS evidence / DIAGNOSTIC ONLY / NEVER ACCEPT and is not runtime-active.
- BMAFDIAG1 is source/static-integrated only. No compiled DLL, review profile, publication, Gale import, runtime arming or Black Mesa x Abandoned Foundry gameplay evidence exists yet.
- Black Mesa x Abandoned Foundry therefore remains `NOT_YET_PROVEN`; the current owner-rule NON-MATCH is an availability/matching gap, not a technical-incompatibility finding.
- The accepted S1.42AB InteriorWeightNormalization mechanism remains unchanged and must run before any BMAFDIAG1 deterministic reduction.
- Historical Phase-B3 classifications, Oxyde ordinary-generation exception, Shatteredrooms Experimentation/Embrion exclusions and the separate Black Mesa/Pikmin routing-recovery closure remain unchanged.
- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`.

## Exact next action

Prepare and execute a separately bounded **inactive review-build checkpoint** for `S1.42AK-BMAFDIAG1` from the exact source/static bytes integrated by PR #198, deriving the review profile directly from exact accepted `S1.42AK`.

That checkpoint may compile/test BMAFDIAG1 and construct/validate an inactive review artifact with the exact owner-default Foundry LLL section activation plus exact `Black Mesa:100` delta. It must fail closed on any unrelated package/config/pair/size drift. It must **not** publish reviewed bytes, modify/import Gale, runtime-arm BMAFDIAG1, start gameplay, waive/replace BMDSFIX1, or implement any universal availability override.

The live controllers remain unchanged until a later separately authorized lifecycle transition.
"""


def require(c, m):
    if not c:
        raise RuntimeError(m)


def update_state():
    s = json.loads(STATE.read_text(encoding="utf-8"))
    require(s["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline drift")
    require(s["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "active candidate drift")
    require(s["runtime_test_outstanding"] is True, "BMDSFIX1 outstanding gate drift")
    require(s["controllers"]["build_enabled"] is False, "build controller unexpectedly enabled")
    require(s["controllers"]["runtime_active_build"] == "S1.42AK-BMDSFIX1", "runtime pointer drift")
    scope = s["selected_scope"]
    phase = scope["phase_c"]
    if "bmafdiag1_source_static_reconciliation" not in phase:
        require("31 MATCH / 22 NON-MATCH / 0 UNRESOLVED" in scope["finding"], "owner closure finding drift")
        s["updated"] = "2026-09-30"
        scope["status"] = "PHASE_C3_BMAFDIAG1_SOURCE_STATIC_INTEGRATED_INACTIVE_REVIEW_BUILD_NEXT_BMDSFIX1_TARGET_PASSIVE_OUTSTANDING"
        scope["finding"] = (
            "Phase-C3 External owner-rule applicability remains closed at Black Mesa 31 MATCH / 22 NON-MATCH / 0 UNRESOLVED, selection-layer only. The bounded Black Mesa x Abandoned Foundry pre-runtime design and S1.42AK-BMAFDIAG1 source/static implementation are now repository-integrated via PR #198 without build/publication/runtime activation. Foundry remains a current Black Mesa NON-MATCH and NOT_YET_PROVEN pair; the supported later availability experiment is restricted to the owner-default LLL Foundry content-configuration section enabled with exactly Black Mesa:100 appended to Manual Level Names. The BMAFDIAG1 selector must see an already-viable post-normalizer FoundryFlow wrapper at rarity 100 before same-wrapper reduction and must fail closed otherwise. Existing Black Mesa pair evidence, Oxyde ordinary-generation exception, historical Phase-B3 matrix, Shatteredrooms exclusions and the passive/outstanding/unwaived BMDSFIX1 DeepSewersFlow gate remain unchanged."
        )
        scope["analysis_contract"] = (
            "Treat Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md as the authority for the integrated Black Mesa x Abandoned Foundry diagnostic source/static checkpoint. Any later BMAFDIAG1 review profile must derive directly from exact accepted S1.42AK, preserve the accepted S1.42AB InteriorWeightNormalization behavior, materialize only the repository-proven owner-default Abandoned Foundry LLL content-configuration section, set Enable Content Configuration = true and append exactly Black Mesa:100 while preserving every other owner value. The C# diagnostic must never register Foundry or repair missing viability: LLL must already return exactly one FoundryFlow wrapper at normalized rarity 100 before deterministic same-wrapper singleton reduction. Keep BMAFDIAG1 diagnostic-only/never-accept, keep BMDSFIX1 unaccepted with its regular DeepSewersFlow gate passive/outstanding/unwaived, preserve the historical B3 matrix, Oxyde ordinary-generation exception and Shatteredrooms exclusions, and keep the separate Black Mesa/Pikmin routing-recovery scope closed."
        )
        scope["next_action"] = NEXT
        phase.update({
            "bmafdiag1_source_static_reconciliation": "Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md",
            "bmafdiag1_source_static_status": "SOURCE_STATIC_PASS_MAIN_INTEGRATED_NOT_BUILT_NOT_PUBLISHED_NOT_ARMED_INACTIVE_REVIEW_BUILD_NEXT",
            "bmafdiag1_source_pr": 198,
            "bmafdiag1_source_exact_head": "2991341d46164e1bcb4e81f7ba34f4f3aeebc7f7",
            "bmafdiag1_source_static_run": 36708620109,
            "bmafdiag1_source_pr_knowledge_architecture_run": 36708620101,
            "bmafdiag1_source_main_integration_commit": "eed4bcb426454bb88ac1ed70151cec454bbb8122",
            "bmafdiag1_source_main_knowledge_architecture_run": 36708806226,
            "bmafdiag1_source_plan": "BuildSpecs/S1.42AK-BMAFDIAG1_PLAN.md",
            "bmafdiag1_source_implementation_evidence": "SourceEvidence/UniversalInteriorViability/PhaseC3F19_BMAFDIAG1/IMPLEMENTATION_FINDINGS.md",
            "black_mesa_abandoned_foundry_status": "SOURCE_STATIC_READY_PAIR_NOT_YET_PROVEN_INACTIVE_REVIEW_BUILD_NEXT"
        })
        s["next_action"] = NEXT
        STATE.write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
    else:
        require(phase["bmafdiag1_source_pr"] == 198, "existing BMAFDIAG1 reconciliation drift")
        require(s["next_action"] == NEXT, "existing next action drift")


def update_lifecycle():
    text = LIFECYCLE.read_text(encoding="utf-8")
    if "## BMAFDIAG1 source/static integration" not in text:
        text = text.replace("**Last-Validated:** 2026-09-29", "**Last-Validated:** 2026-09-30", 1)
        section = """
## BMAFDIAG1 source/static integration — PASS / inactive

`Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md` records the completed bounded Black Mesa x Abandoned Foundry source/static checkpoint.

PR #198 final head `2991341d46164e1bcb4e81f7ba34f4f3aeebc7f7` passed the BMAFDIAG1 source/static gate run `36708620109` (#2) and Knowledge Architecture run `36708620101` (#860). It merged to `main` at `eed4bcb426454bb88ac1ed70151cec454bbb8122`; permanent exact-head Knowledge Architecture push run `36708806226` (#861) passed.

BMAFDIAG1 is **source/static-integrated only**: no DLL has been compiled for review, no Foundry config delta has been materialized into a profile, no bytes have been published, no Gale profile has been imported, and no runtime test is armed. The plugin remains fail-closed: it may reduce only an already-viable exact `Abandoned Foundry` / `FoundryFlow` wrapper at post-normalizer rarity `100`; it never creates availability or duplicate registration.

For the separately authorized later review build, the exact supported availability delta is owner-default Foundry LLL content-configuration materialization, `Enable Content Configuration = true`, and exactly `Black Mesa:100` appended to the existing Manual Level Names mapping. The review profile must derive directly from exact accepted S1.42AK. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`; this checkpoint is not runtime compatibility evidence.

"""
        text = text.replace("## Live execution state\n", section + "## Live execution state\n", 1)
        text = text.replace(
            "- BMGHDIAG3: **Black Mesa x Greenhouse runtime-compatibility PASS / DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**.\n",
            "- BMGHDIAG3: **Black Mesa x Greenhouse runtime-compatibility PASS / DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**.\n- BMAFDIAG1: **Black Mesa x Abandoned Foundry source/static PASS / main-integrated / not built / not published / not runtime-active / pair NOT_YET_PROVEN**.\n",
            1,
        )
        pattern = re.compile(r"## Exact next project action\n\n.*?\n\nNo Gale replacement/import command", re.S)
        replacement = "## Exact next project action\n\n" + NEXT + "\n\nNo Gale replacement/import command"
        text, n = pattern.subn(replacement, text, count=1)
        require(n == 1, "CURRENT_LIFECYCLE next-action replacement failed")
        LIFECYCLE.write_text(text, encoding="utf-8")


def update_map():
    text = MAP.read_text(encoding="utf-8")
    if "BMAFDIAG1 source/static checkpoint" not in text:
        text = text.replace("**Last-Validated:** 2026-09-29", "**Last-Validated:** 2026-09-30", 1)
        anchor = "BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT** and is no longer runtime-active."
        para = (
            "The bounded **S1.42AK-BMAFDIAG1** Black Mesa x Abandoned Foundry source/static checkpoint is now integrated on `main` under `Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md`. It is not built, published, Gale-imported or runtime-active, and Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Any later review profile must derive directly from exact accepted S1.42AK and use only the proven owner-default Foundry LLL content-configuration activation plus exact `Black Mesa:100` Manual-Level-Names delta; the diagnostic may reduce only an already-viable post-normalizer `FoundryFlow` wrapper.\n\n"
        require(anchor in text, "knowledge-map anchor drift")
        text = text.replace(anchor, para + anchor, 1)
        text = re.sub(r"Exact next action: .*?\n\n## Authority rule", "Exact next action: " + NEXT + "\n\n## Authority rule", text, count=1, flags=re.S)
        MAP.write_text(text, encoding="utf-8")


def main():
    update_state()
    if not RECON.exists():
        RECON.write_text(RECON_TEXT, encoding="utf-8")
    else:
        require(RECON.read_text(encoding="utf-8") == RECON_TEXT, "reconciliation file drift")
    update_lifecycle()
    update_map()
    subprocess.run([sys.executable, str(ROOT / "RepositoryTools/render_current_navigation.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "RepositoryTools/render_current_navigation.py"), "--check"], cwd=ROOT, check=True)
    print("PASS: BMAFDIAG1 source/static lifecycle reconciliation rendered.")

if __name__ == "__main__":
    main()
