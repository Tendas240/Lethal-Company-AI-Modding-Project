#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
LIFECYCLE_PATH = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
PROFILE_REL = "Profiles/LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic.r2z"
PROFILE_SHA = "7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace"
PUBLICATION_MAIN = "b40a497d9956993bc5d183bad36037e9175d9635"
PUBLICATION_PR_HEAD = "2c649cea0569f25fd80a25954c76667a21b8e445"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    require(count == 1, f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def main() -> None:
    profile_path = ROOT / PROFILE_REL
    profile_index_result = ROOT / "ProfileSources/S1.42AK-BMGHDIAG3/PROFILE_INDEX_RESULT.json"
    registry_path = ROOT / "Profiles/EXPECTED_HASHES.json"

    require(profile_path.is_file(), "published BMGHDIAG3 profile missing")
    require(hashlib.sha256(profile_path.read_bytes()).hexdigest() == PROFILE_SHA, "published BMGHDIAG3 profile SHA drift")
    require((ROOT / "Current/196_S1.42AK_BMGHDIAG3_EXACT_BYTE_PUBLICATION_CHECKPOINT.md").is_file(), "Current/196 publication authority missing")
    require(not profile_index_result.exists(), "BMGHDIAG3 PROFILE_INDEX_RESULT already exists; lifecycle repair assumptions are stale")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    require(PROFILE_REL not in registry, "BMGHDIAG3 already mapped in EXPECTED_HASHES; profile-index gate has advanced")

    spec = json.loads((ROOT / "BuildSpecs/current.json").read_text(encoding="utf-8"))
    require(spec["enabled"] is False and spec["build_id"] == "IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS", "BuildSpecs/current.json controller drift")
    require(spec["base_sha256"] == "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0", "BuildSpecs/current.json base drift")
    require((ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == "S1.42AK-BMDSFIX1", "RuntimeInbox/ACTIVE_BUILD.txt drift")

    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    require(state["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline drift")
    require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "active candidate drift")
    require(state["controllers"]["runtime_active_build"] == "S1.42AK-BMDSFIX1", "machine runtime controller drift")
    require(
        state["selected_scope"]["status"]
        == "PHASE_C3F18_BMDSFIX1_TARGET_QUALIFICATION_PASSIVE_OUTSTANDING_BMGHDIAG3_INACTIVE_REVIEW_BUILD_PASS_EXACT_BYTE_PUBLICATION_NEXT",
        "selected-scope pre-state drift",
    )

    next_action = (
        "Perform a separately bounded S1.42AK-BMGHDIAG3 profile-index reconciliation for the exact already-published profile "
        "Profiles/LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic.r2z with SHA-256 "
        "7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace. Add only the canonical diagnostic mapping to "
        "Profiles/EXPECTED_HASHES.json (build_id S1.42AK-BMGHDIAG3, exact SHA-256, canonical readable snapshot "
        "ProfileSources/S1.42AK-BMGHDIAG3/) following the existing diagnostic pattern, then let .github/workflows/profile-index.yml "
        "index those exact existing bytes and create ProfileSources/S1.42AK-BMGHDIAG3/PROFILE_INDEX_RESULT.json; verify the bot follow-up "
        "exact-head Knowledge Architecture workflow_dispatch required by that workflow. Do not rebuild or alter the profile/DLL, modify/import "
        "Gale, runtime-arm BMGHDIAG3, start gameplay, change RuntimeInbox/ACTIVE_BUILD.txt from S1.42AK-BMDSFIX1, enable "
        "BuildSpecs/current.json, or change BMDSFIX1 acceptance. Explicit BMGHDIAG3 runtime activation remains a later separate gate after successful indexing."
    )

    scope = state["selected_scope"]
    scope["status"] = "PHASE_C3F18_BMDSFIX1_TARGET_QUALIFICATION_PASSIVE_OUTSTANDING_BMGHDIAG3_EXACT_BYTE_PUBLICATION_INTEGRATED_PROFILE_INDEX_RECONCILIATION_NEXT"
    scope["finding"] = replace_once(
        scope["finding"],
        "BMGHDIAG3 remains unpublished, not Gale-imported and not runtime-armed; Black Mesa x Greenhouse remains NOT_YET_PROVEN.",
        "BMGHDIAG3 exact-byte publication is now integrated on main via PR #184 and Current/196_S1.42AK_BMGHDIAG3_EXACT_BYTE_PUBLICATION_CHECKPOINT.md: publication transport run 36316311432 revalidated and materialized exact reviewed profile SHA-256 7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace without rebuild; PR exact-head Knowledge Architecture run 36316631746 (#816) passed; main integration commit b40a497d9956993bc5d183bad36037e9175d9635 and permanent main Knowledge Architecture run 36316936811 (#817) passed. The exact profile remains not indexed, not Gale-imported and not runtime-armed; Black Mesa x Greenhouse remains NOT_YET_PROVEN.",
        "selected_scope.finding publication closure",
    )
    scope["analysis_contract"] = replace_once(
        scope["analysis_contract"],
        "The next Greenhouse checkpoint is exact-byte publication only; it must not modify/import Gale, runtime-arm BMGHDIAG3, start gameplay, or alter BMDSFIX1 acceptance or its passive target gate.",
        "Exact-byte publication is now complete under Current/196_S1.42AK_BMGHDIAG3_EXACT_BYTE_PUBLICATION_CHECKPOINT.md and main integration b40a497d9956993bc5d183bad36037e9175d9635. The next Greenhouse checkpoint is profile-index reconciliation only: add the canonical diagnostic mapping for the already-published exact profile and allow the existing profile-index workflow to produce PROFILE_INDEX_RESULT.json before any Gale import or runtime activation. Do not rebuild or alter the profile/DLL, modify/import Gale, runtime-arm BMGHDIAG3, start gameplay, or alter BMDSFIX1 acceptance or its passive target gate.",
        "selected_scope.analysis_contract next gate",
    )
    scope["next_action"] = next_action
    state["next_action"] = next_action

    phase = scope["phase_c"]
    phase["bmgdiag3_source_static_status"] = "SOURCE_STATIC_PASS_MAIN_INTEGRATED_REVIEW_BUILD_PASS_EXACT_BYTES_PUBLISHED_NOT_INDEXED_NOT_ARMED"
    phase["bmgdiag3_review_status"] = "INACTIVE_REVIEW_BUILD_PASS_EXACT_BYTES_PUBLISHED_NOT_INDEXED_NOT_ARMED_PROFILE_INDEX_RECONCILIATION_NEXT"
    phase["bmgdiag3_review_published"] = True
    phase["bmgdiag3_review_runtime_armed"] = False
    phase["bmgdiag3_publication_checkpoint"] = "Current/196_S1.42AK_BMGHDIAG3_EXACT_BYTE_PUBLICATION_CHECKPOINT.md"
    phase["bmgdiag3_publication_evidence"] = "BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
    phase["bmgdiag3_publication_status"] = "EXACT_BYTE_PUBLISHED_MAIN_INTEGRATED_NOT_INDEXED_NOT_GALE_IMPORTED_NOT_RUNTIME_ARMED_PROFILE_INDEX_RECONCILIATION_NEXT"
    phase["bmgdiag3_publication_branch"] = "c3f18-bmghdiag3-exact-publication"
    phase["bmgdiag3_publication_transport_run"] = 36316311432
    phase["bmgdiag3_published_profile_commit"] = "4fc4c20523f6860f65c47a983f5954a6f00a2d63"
    phase["bmgdiag3_publication_integration_pr"] = 184
    phase["bmgdiag3_publication_pr_head"] = PUBLICATION_PR_HEAD
    phase["bmgdiag3_publication_pr_knowledge_architecture_run"] = 36316631746
    phase["bmgdiag3_publication_main_integration_commit"] = PUBLICATION_MAIN
    phase["bmgdiag3_publication_main_knowledge_architecture_run"] = 36316936811
    phase["bmgdiag3_profile_indexed"] = False
    phase["bmgdiag3_profile_index_result"] = "ProfileSources/S1.42AK-BMGHDIAG3/PROFILE_INDEX_RESULT.json"

    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lifecycle = LIFECYCLE_PATH.read_text(encoding="utf-8")
    lifecycle = replace_once(
        lifecycle,
        "`Current/195_S1.42AK_BMGHDIAG3_INACTIVE_REVIEW_BUILD_CHECKPOINT.md`, `BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`",
        "`Current/195_S1.42AK_BMGHDIAG3_INACTIVE_REVIEW_BUILD_CHECKPOINT.md`, `BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`, `Current/196_S1.42AK_BMGHDIAG3_EXACT_BYTE_PUBLICATION_CHECKPOINT.md`, `BuildSpecs/S1.42AK-BMGHDIAG3_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md`",
        "lifecycle evidence list",
    )
    lifecycle = replace_once(
        lifecycle,
        "That source/static checkpoint did not itself establish compiler/build validity. The later bounded inactive review-build has now passed and is reconciled separately below; reviewed bytes remain unpublished, not Gale-imported and not runtime-armed. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.",
        "That source/static checkpoint did not itself establish compiler/build validity. The later bounded inactive review-build and exact-byte publication have now passed and are reconciled separately below; the exact published bytes remain not indexed, not Gale-imported and not runtime-armed. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.",
        "source/static lifecycle supersession",
    )
    lifecycle = replace_once(
        lifecycle,
        "This checkpoint proves compile/test/archive validity only. The reviewed profile is **not published**, not Gale-imported and not runtime-armed. The active gameplay candidate and runtime/evidence pointer remain S1.42AK-BMDSFIX1, and its regular Black Mesa x `DeepSewersFlow` qualification remains passive/outstanding. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.",
        "This checkpoint proves compile/test/archive validity only. At that review checkpoint the profile was **not published**, not Gale-imported and not runtime-armed; that publication state is now superseded by the separately integrated exact-byte publication below. The active gameplay candidate and runtime/evidence pointer remain S1.42AK-BMDSFIX1, and its regular Black Mesa x `DeepSewersFlow` qualification remains passive/outstanding. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.",
        "review lifecycle historical qualification",
    )

    publication_section = """## BMGHDIAG3 exact-byte publication — integrated / not indexed

`Current/196_S1.42AK_BMGHDIAG3_EXACT_BYTE_PUBLICATION_CHECKPOINT.md` records the completed exact-byte publication. The transport used only frozen reviewed artifact `10929208327`; publication run `36316311432` revalidated artifact ZIP SHA-256 `20f616e85585e10631c31e09844a27bb6bb7649843a98655ed70e37b89152198`, exact profile SHA-256 `7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace`, and exact `S142AKBMGHDiag3.dll` SHA-256 `d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352` before materialization. No profile or DLL rebuild occurred.

PR #184 exact head `2c649cea0569f25fd80a25954c76667a21b8e445` passed Knowledge Architecture run `36316631746` (#816) and merged to `main` as `b40a497d9956993bc5d183bad36037e9175d9635`; permanent main Knowledge Architecture push run `36316936811` (#817) passed. The temporary publication transport workflow was removed before integration.

The exact published profile and `ProfileSources/S1.42AK-BMGHDIAG3/` readable snapshot are now on `main`. The snapshot `FILE_INDEX.json` has 337 rows and matches the frozen review artifact. `Profiles/EXPECTED_HASHES.json` does not yet map this diagnostic profile and `ProfileSources/S1.42AK-BMGHDIAG3/PROFILE_INDEX_RESULT.json` does not yet exist, so the profile remains **not indexed**.

Publication did not modify/import Gale, runtime-arm BMGHDIAG3, start gameplay, alter `BuildSpecs/current.json`, change `RuntimeInbox/ACTIVE_BUILD.txt`, accept BMDSFIX1, or alter its passive Black Mesa x `DeepSewersFlow` qualification. BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT** and Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

The next bounded Greenhouse gate is a separate **BMGHDIAG3 profile-index reconciliation** using the existing diagnostic mapping/index workflow. Explicit runtime activation is later and remains unauthorized until indexing succeeds.

"""
    lifecycle = replace_once(
        lifecycle,
        "## BMDSFIX1 runtime — regular non-target evidence plus DIAG1PATH1 supporting PASS\n",
        publication_section + "## BMDSFIX1 runtime — regular non-target evidence plus DIAG1PATH1 supporting PASS\n",
        "publication lifecycle section insertion",
    )
    lifecycle = replace_once(
        lifecycle,
        "- Active Phase-C3 work: **BMGHDIAG3 inactive review-build PASS with exact reviewed bytes locked to Actions artifact `10929208327`; exact-byte publication is next; no BMGHDIAG3 publication/Gale import/runtime arm yet; Greenhouse remains `NOT_YET_PROVEN`**.",
        "- Active Phase-C3 work: **BMGHDIAG3 exact-byte publication is integrated on main from reviewed artifact `10929208327`; profile-index reconciliation is next; BMGHDIAG3 remains not indexed, not Gale-imported and not runtime-armed; Greenhouse remains `NOT_YET_PROVEN`**.",
        "live execution publication status",
    )

    start = lifecycle.find("## Exact next project action\n")
    end = lifecycle.find("## Permanent Gale workflow\n", start)
    require(start >= 0 and end > start, "exact next project action section boundaries not found")
    next_section = """## Exact next project action

Perform a separately bounded **S1.42AK-BMGHDIAG3 profile-index reconciliation** for the already-published exact profile `Profiles/LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic.r2z` / SHA-256 `7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace`.

Add only the canonical diagnostic mapping to `Profiles/EXPECTED_HASHES.json` (`build_id = S1.42AK-BMGHDIAG3`, exact SHA-256, canonical readable snapshot `ProfileSources/S1.42AK-BMGHDIAG3/`) following the established diagnostic-profile pattern. Then let `.github/workflows/profile-index.yml` index the exact existing profile bytes and create `ProfileSources/S1.42AK-BMGHDIAG3/PROFILE_INDEX_RESULT.json`. If the workflow creates its bot follow-up commit, verify the explicitly dispatched exact-head `Knowledge Architecture` `workflow_dispatch` run required by that workflow.

Do **not** rebuild or alter the profile/DLL, modify/import Gale, runtime-arm BMGHDIAG3, start gameplay, change `RuntimeInbox/ACTIVE_BUILD.txt` from `S1.42AK-BMDSFIX1`, enable `BuildSpecs/current.json`, or change BMDSFIX1 acceptance. Explicit BMGHDIAG3 runtime activation remains a later separate gate after successful indexing. Black Mesa x Greenhouse remains `NOT_YET_PROVEN`.

"""
    lifecycle = lifecycle[:start] + next_section + lifecycle[end:]
    LIFECYCLE_PATH.write_text(lifecycle, encoding="utf-8")

    print("PASS: canonical BMGHDIAG3 publication lifecycle state reconciled in source authorities.")


if __name__ == "__main__":
    main()
