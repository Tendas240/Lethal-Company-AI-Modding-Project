#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "Current/CURRENT_STATE.json"
LIFECYCLE = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
MAP = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
CHECKPOINT = ROOT / "Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md"
MACHINE = ROOT / "BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json"

REVIEWED_HEAD = "47f2beca815c4d726fec8b85f4e9aac129519486"
REVIEW_MERGE_REF = "3a0d70ea0870afcf13fbe4a43efa1d1937b11959"
REVIEW_RUN = 36735131025
REVIEW_RUN_NUMBER = 2
KA_RUN = 36735130944
KA_RUN_NUMBER = 872
ARTIFACT_ID = 11106178288
ARTIFACT_NAME = "S1.42AK-BMAFDIAG1-review-3a0d70ea0870afcf13fbe4a43efa1d1937b11959"
ARTIFACT_ZIP_SHA = "e96b8de8084f051d74fcb06b05aa06ed3355419602c813b6021acb8a5b9f78b0"
ARTIFACT_SIZE = 1086673
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PROFILE_SHA = "b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2"
DLL_SHA = "c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"

NEXT = (
    "Prepare and execute a separately bounded exact-byte publication checkpoint for S1.42AK-BMAFDIAG1 using only the already reviewed bytes from GitHub Actions artifact 11106178288 produced by review run 36735131025. Verify artifact ZIP SHA-256 e96b8de8084f051d74fcb06b05aa06ed3355419602c813b6021acb8a5b9f78b0 and publish the exact reviewed profile SHA-256 b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2 with exact S142AKBMAFDiag1.dll SHA-256 c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1; do not rebuild. The publication checkpoint must not modify/import Gale, runtime-arm BMAFDIAG1, start gameplay, alter S1.42AB normalization, add External:100 or unrelated pairings/size rules, duplicate-register Foundry, change RuntimeInbox/ACTIVE_BUILD.txt from S1.42AK-BMDSFIX1, enable BuildSpecs/current.json, or change BMDSFIX1 acceptance. Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN until a later separately authorized runtime checkpoint."
)

FINDING = (
    "Phase-C3 External owner-rule applicability remains closed at Black Mesa 31 MATCH / 22 NON-MATCH / 0 UNRESOLVED, selection-layer only. The bounded S1.42AK-BMAFDIAG1 inactive review-build checkpoint is now technically qualified on PR #200 exact reviewed head 47f2beca815c4d726fec8b85f4e9aac129519486: review-build run 36735131025 (#2) and exact-head Knowledge Architecture run 36735130944 (#872) both passed. The exact reviewed Actions artifact is 11106178288 with ZIP SHA-256 e96b8de8084f051d74fcb06b05aa06ed3355419602c813b6021acb8a5b9f78b0; review profile SHA-256 b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2 and S142AKBMAFDiag1.dll SHA-256 c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1 were independently rehashed and match. The 337-member profile derives directly from exact accepted S1.42AK, adds only the diagnostic DLL, removes nothing, changes existing members only at BepInEx/config/LethalLevelLoader.cfg and export.r2x, has 0 package changes and 1 config change, and materializes the owner-default Abandoned Foundry section with Enable Content Configuration = true plus exactly Black Mesa:100 while preserving every other Foundry owner value. BMAFDIAG1 remains DIAGNOSTIC ONLY / NEVER ACCEPT, unpublished, not Gale-imported and not runtime-armed; Black Mesa x Abandoned Foundry remains NOT_YET_PROVEN. BMDSFIX1 and all existing external-owner boundaries remain unchanged."
)

ANALYSIS = (
    "Treat Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md as the source/static authority and Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md plus BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json as the exact inactive-review-build authority. Lock any later publication to GitHub Actions artifact 11106178288 from review run 36735131025: review profile SHA-256 b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2 and diagnostic DLL SHA-256 c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1. Do not rebuild those bytes for publication. Preserve the exact parent S1.42AK, accepted S1.42AB InteriorWeightNormalization SHA-256 901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06, exact LLL SHA-256 b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c, and the sole authorized availability semantic: owner-default Abandoned Foundry LLL content configuration enabled with exactly Black Mesa:100 added to the preserved Manual Level Names mapping. The C# diagnostic must never register Foundry or repair missing viability; it may reduce only the already-viable exact FoundryFlow wrapper at post-normalizer rarity 100. Keep BMAFDIAG1 diagnostic-only/never-accept, unpublished/not Gale-imported/not runtime-armed until later checkpoints; keep S1.42AK-BMDSFIX1 unaccepted with its regular DeepSewersFlow gate passive/outstanding/unwaived, preserve historical B3, the Oxyde ordinary-generation exception, Shatteredrooms exclusions and the closed Black Mesa/Pikmin routing scope."
)

CHECKPOINT_TEXT = f"""# S1.42AK-BMAFDIAG1 Inactive Review-Build Checkpoint

**Date:** 2026-09-30
**Status:** INACTIVE REVIEW BUILD PASS / EXACT BYTES QUALIFIED / NOT PUBLISHED / NOT GALE-IMPORTED / NOT RUNTIME-ARMED / BLACK MESA x ABANDONED FOUNDRY NOT YET PROVEN
**Accepted gameplay baseline:** S1.42AK — unchanged
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted / passive target gate preserved
**Classification:** DIAGNOSTIC ONLY / NEVER ACCEPT

## Decision

The bounded repository-native inactive review-build checkpoint for `S1.42AK-BMAFDIAG1` is complete and passes. The diagnostic compiled, its isolated policy-test harness passed, exact LLL provenance passed, and an inactive review profile derived directly from exact accepted S1.42AK passed the archive/configuration-delta validator.

This decision qualifies only the exact reviewed bytes. It does **not** publish them, import/modify Gale, runtime-arm BMAFDIAG1, authorize gameplay, qualify Black Mesa x Abandoned Foundry, change the accepted S1.42AB normalization behavior, or alter BMDSFIX1 acceptance.

## Exact review identity

- Review PR: **#200**
- Exact reviewed head: `{REVIEWED_HEAD}`
- Review merge ref used in artifact name: `{REVIEW_MERGE_REF}`
- Review-build/archive-config-delta run: `{REVIEW_RUN}` / run number `{REVIEW_RUN_NUMBER}` — **success**
- Exact-head Knowledge Architecture run: `{KA_RUN}` / run number `{KA_RUN_NUMBER}` — **success**

## Exact reviewed bytes

- Direct parent: exact accepted `S1.42AK`
- Parent profile SHA-256: `{BASE_SHA}`
- Actions artifact ID: `{ARTIFACT_ID}`
- Artifact name: `{ARTIFACT_NAME}`
- Artifact ZIP SHA-256: `{ARTIFACT_ZIP_SHA}`
- Artifact size: `{ARTIFACT_SIZE}` bytes
- Review profile SHA-256: `{PROFILE_SHA}`
- `S142AKBMAFDiag1.dll` SHA-256: `{DLL_SHA}`
- Exact LLL 1.7.12 DLL SHA-256: `{LLL_SHA}`
- Accepted InteriorWeightNormalizer SHA-256: `{NORMALIZER_SHA}`
- Fresh independent downloaded-artifact rehash: **ZIP / profile / DLL match**

Canonical machine evidence: `BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`.

## Archive and configuration delta

The validated review profile contains **337** members. Relative to exact accepted S1.42AK:

- added: exactly `BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll`;
- removed: none;
- changed existing members: exactly `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`;
- package changes: **0**;
- config changes: **1**;
- Foundry owner-default section materialized: **true**;
- `Enable Content Configuration = true`;
- exact Manual Level Names availability delta: **`Black Mesa:100`**;
- all other Foundry owner values preserved;
- accepted normalizer bytes unchanged;
- exact LLL provenance preserved.

No `External:100`, foreign pairing, size-rule change, duplicate Foundry registration or unrelated config/package drift is present.

## Diagnostic consequence

The isolated policy-test harness passed the retained provenance, caller/runtime identity, exact Black Mesa and exact `Abandoned Foundry` / `FoundryFlow` identity, post-normalizer rarity-100, singleton-reduction and fail-closed boundaries. BMAFDIAG1 does not create Foundry availability: LLL must already return exactly one correct Foundry wrapper at rarity 100 before the same wrapper may be deterministically reduced to a singleton.

This checkpoint is compile/test/archive/configuration evidence only. It is **not** Black Mesa x Abandoned Foundry runtime-compatibility evidence.

## Controller preservation

- `BuildSpecs/current.json` remains disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`.
- S1.42AK remains the sole accepted gameplay baseline.
- S1.42AK-BMDSFIX1 remains active gameplay candidate / not accepted.
- Its regular Black Mesa x `DeepSewersFlow` qualification remains outstanding/passive/unwaived with no dedicated blind reroll release.
- BMAFDIAG1 is not an active runtime candidate.

## Exact next action

Execute a separately bounded **exact-byte publication checkpoint** from Actions artifact `{ARTIFACT_ID}`. Verify the artifact ZIP digest and publish the exact reviewed profile/DLL hashes above **without rebuilding**.

Do **not** modify/import Gale, runtime-arm BMAFDIAG1, start gameplay, switch `RuntimeInbox/ACTIVE_BUILD.txt`, enable `BuildSpecs/current.json`, alter S1.42AB normalization, add `External:100` or unrelated pairings/size rules, duplicate-register Foundry, or change BMDSFIX1 acceptance in that publication checkpoint. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN` until a later separately authorized runtime checkpoint.
"""

MACHINE_DATA = {
    "status": "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED",
    "build_id": "S1.42AK-BMAFDIAG1",
    "classification": "DIAGNOSTIC_ONLY_NEVER_ACCEPT",
    "review_pr": 200,
    "reviewed_head": REVIEWED_HEAD,
    "review_merge_ref": REVIEW_MERGE_REF,
    "review_run": REVIEW_RUN,
    "review_run_number": REVIEW_RUN_NUMBER,
    "review_knowledge_architecture_run": KA_RUN,
    "review_knowledge_architecture_run_number": KA_RUN_NUMBER,
    "review_artifact_id": ARTIFACT_ID,
    "review_artifact_name": ARTIFACT_NAME,
    "review_artifact_zip_sha256": ARTIFACT_ZIP_SHA,
    "review_artifact_size_bytes": ARTIFACT_SIZE,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "base_profile_sha256": BASE_SHA,
    "lll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "archive_members_verified": 337,
    "added_members": ["BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll"],
    "changed_existing_members": ["BepInEx/config/LethalLevelLoader.cfg", "export.r2x"],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 1,
    "foundry_section_materialized": True,
    "foundry_content_configuration_enabled": True,
    "foundry_manual_level_names_delta": "Black Mesa:100",
    "foundry_owner_values_preserved": True,
    "independent_artifact_rehash_match": True,
    "independent_artifact_rehash_scope": ["artifact_zip", "review_profile", "S142AKBMAFDiag1.dll"],
    "published": False,
    "runtime_armed": False,
    "runtime_active_build": "S1.42AK-BMDSFIX1",
    "active_gameplay_candidate": "S1.42AK-BMDSFIX1",
    "runtime_test_outstanding": True,
    "black_mesa_abandoned_foundry_status": "NOT_YET_PROVEN",
    "next_publication_source_artifact_id": ARTIFACT_ID,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def update_state() -> None:
    s = json.loads(STATE.read_text(encoding="utf-8"))
    require(s["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline drift")
    require(s["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "active candidate drift")
    require(s["runtime_test_outstanding"] is True, "BMDSFIX1 outstanding gate drift")
    require(s["controllers"]["build_enabled"] is False, "build controller unexpectedly enabled")
    require(s["controllers"]["runtime_active_build"] == "S1.42AK-BMDSFIX1", "runtime pointer drift")
    scope = s["selected_scope"]
    phase = scope["phase_c"]
    require(phase["bmafdiag1_source_pr"] == 198, "BMAFDIAG1 source reconciliation drift")
    require(phase["bmafdiag1_source_exact_head"] == "2991341d46164e1bcb4e81f7ba34f4f3aeebc7f7", "BMAFDIAG1 source head drift")

    s["updated"] = "2026-09-30"
    scope["status"] = "PHASE_C3_BMAFDIAG1_INACTIVE_REVIEW_BUILD_PASS_EXACT_BYTE_PUBLICATION_NEXT_BMDSFIX1_TARGET_PASSIVE_OUTSTANDING"
    scope["finding"] = FINDING
    scope["analysis_contract"] = ANALYSIS
    scope["next_action"] = NEXT
    phase.update({
        "bmafdiag1_source_static_status": "SOURCE_STATIC_PASS_MAIN_INTEGRATED_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED_EXACT_BYTE_PUBLICATION_NEXT",
        "bmafdiag1_review_checkpoint": "Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md",
        "bmafdiag1_review_status": "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_ARMED_EXACT_BYTE_PUBLICATION_NEXT",
        "bmafdiag1_review_pr": 200,
        "bmafdiag1_reviewed_head": REVIEWED_HEAD,
        "bmafdiag1_review_merge_ref": REVIEW_MERGE_REF,
        "bmafdiag1_review_run": REVIEW_RUN,
        "bmafdiag1_review_run_number": REVIEW_RUN_NUMBER,
        "bmafdiag1_review_knowledge_architecture_run": KA_RUN,
        "bmafdiag1_review_knowledge_architecture_run_number": KA_RUN_NUMBER,
        "bmafdiag1_review_artifact_id": ARTIFACT_ID,
        "bmafdiag1_review_artifact_name": ARTIFACT_NAME,
        "bmafdiag1_review_artifact_zip_sha256": ARTIFACT_ZIP_SHA,
        "bmafdiag1_review_artifact_size_bytes": ARTIFACT_SIZE,
        "bmafdiag1_review_profile_sha256": PROFILE_SHA,
        "bmafdiag1_review_dll_sha256": DLL_SHA,
        "bmafdiag1_review_lll_sha256": LLL_SHA,
        "bmafdiag1_review_normalizer_sha256": NORMALIZER_SHA,
        "bmafdiag1_review_archive_members": 337,
        "bmafdiag1_review_evidence": "BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json",
        "bmafdiag1_review_published": False,
        "bmafdiag1_review_runtime_armed": False,
        "black_mesa_abandoned_foundry_status": "INACTIVE_REVIEW_BUILD_PASS_PAIR_NOT_YET_PROVEN_EXACT_BYTE_PUBLICATION_NEXT",
    })
    s["next_action"] = NEXT
    STATE.write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")


def update_evidence() -> None:
    CHECKPOINT.write_text(CHECKPOINT_TEXT, encoding="utf-8")
    MACHINE.parent.mkdir(parents=True, exist_ok=True)
    MACHINE.write_text(json.dumps(MACHINE_DATA, indent=2) + "\n", encoding="utf-8")


def update_lifecycle() -> None:
    text = LIFECYCLE.read_text(encoding="utf-8")
    evidence_anchor = "`Current/206_S1.42AK_EXTERNAL_OWNER_RULE_APPLICABILITY_CLOSURE_RECONCILIATION.md`"
    if "Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md" not in text.split("\n", 8)[6]:
        require(evidence_anchor in text, "lifecycle evidence anchor missing")
        text = text.replace(
            evidence_anchor,
            evidence_anchor + ", `Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md`, `Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md`, `BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`",
            1,
        )

    old_source = (
        "BMAFDIAG1 is **source/static-integrated only**: no DLL has been compiled for review, no Foundry config delta has been materialized into a profile, no bytes have been published, no Gale profile has been imported, and no runtime test is armed. The plugin remains fail-closed: it may reduce only an already-viable exact `Abandoned Foundry` / `FoundryFlow` wrapper at post-normalizer rarity `100`; it never creates availability or duplicate registration.\n\n"
        "For the separately authorized later review build, the exact supported availability delta is owner-default Foundry LLL content-configuration materialization, `Enable Content Configuration = true`, and exactly `Black Mesa:100` appended to the existing Manual Level Names mapping. The review profile must derive directly from exact accepted S1.42AK. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`; this checkpoint is not runtime compatibility evidence.\n"
    )
    new_source = (
        "That source/static checkpoint did not itself establish compiler/build validity. The later bounded inactive review-build has now passed and is reconciled separately below; the exact reviewed bytes remain unpublished, not Gale-imported and not runtime-armed. The plugin remains fail-closed and never creates availability or duplicate registration. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`.\n"
    )
    require(old_source in text, "lifecycle BMAFDIAG1 source block drift")
    text = text.replace(old_source, new_source, 1)

    review_section = f"""
## BMAFDIAG1 inactive review build — PASS / not published

`Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md` records the completed bounded inactive review-build checkpoint. Canonical machine evidence is `BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`.

PR #200 exact reviewed head `{REVIEWED_HEAD}` passed the BMAFDIAG1 review-build/archive-config-delta run `{REVIEW_RUN}` (#{REVIEW_RUN_NUMBER}) and Knowledge Architecture run `{KA_RUN}` (#{KA_RUN_NUMBER}). The exact reviewed Actions artifact is ID `{ARTIFACT_ID}`, name `{ARTIFACT_NAME}`, ZIP SHA-256 `{ARTIFACT_ZIP_SHA}`, size `{ARTIFACT_SIZE}` bytes. Fresh independent rehashing of the downloaded artifact ZIP, contained review profile and contained BMAFDIAG1 DLL matched the CI identities.

The review profile derives directly from exact accepted S1.42AK / SHA-256 `{BASE_SHA}`. Its SHA-256 is `{PROFILE_SHA}`; exact `S142AKBMAFDiag1.dll` SHA-256 is `{DLL_SHA}`. Exact LLL 1.7.12 DLL SHA-256 remains `{LLL_SHA}` and accepted InteriorWeightNormalizer SHA-256 remains `{NORMALIZER_SHA}`.

The validated profile has 337 members. It adds only `BepInEx/plugins/S142AKBMAFDiag1/S142AKBMAFDiag1.dll`, removes none, changes existing members only at `BepInEx/config/LethalLevelLoader.cfg` and `export.r2x`, has 0 package changes and exactly 1 config change. The owner-default Abandoned Foundry section is materialized with `Enable Content Configuration = true` and exactly `Black Mesa:100` added to the preserved Manual Level Names mapping; all other Foundry owner values remain unchanged. No `External:100`, unrelated pairing, size-rule change or duplicate registration is introduced.

This checkpoint proves compile/test/archive/configuration validity only. BMAFDIAG1 remains **DIAGNOSTIC ONLY / NEVER ACCEPT**, unpublished, not Gale-imported and not runtime-armed. Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`; BMDSFIX1 remains the separate active unaccepted gameplay candidate with its regular Deep Sewers gate passive/outstanding/unwaived.

"""
    live_anchor = "## Live execution state\n"
    require(live_anchor in text, "lifecycle live-state anchor missing")
    text = text.replace(live_anchor, review_section + live_anchor, 1)
    text = text.replace(
        "- BMAFDIAG1: **Black Mesa x Abandoned Foundry source/static PASS / main-integrated / not built / not published / not runtime-active / pair NOT_YET_PROVEN**.",
        "- BMAFDIAG1: **Black Mesa x Abandoned Foundry inactive review-build PASS / exact bytes qualified / not published / not Gale-imported / not runtime-active / DIAGNOSTIC ONLY / pair NOT_YET_PROVEN**.",
        1,
    )
    pattern = re.compile(r"## Exact next project action\n\n.*?\n\nNo Gale replacement/import command", re.S)
    replacement = "## Exact next project action\n\n" + NEXT + "\n\nNo Gale replacement/import command"
    text, count = pattern.subn(replacement, text, count=1)
    require(count == 1, "lifecycle next-action replacement failed")
    LIFECYCLE.write_text(text, encoding="utf-8")


def update_map() -> None:
    text = MAP.read_text(encoding="utf-8")
    old = (
        "The bounded **S1.42AK-BMAFDIAG1** Black Mesa x Abandoned Foundry source/static checkpoint is now integrated on `main` under `Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md`. It is not built, published, Gale-imported or runtime-active, and Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`. Any later review profile must derive directly from exact accepted S1.42AK and use only the proven owner-default Foundry LLL content-configuration activation plus exact `Black Mesa:100` Manual-Level-Names delta; the diagnostic may reduce only an already-viable post-normalizer `FoundryFlow` wrapper."
    )
    new = (
        "The bounded **S1.42AK-BMAFDIAG1** Black Mesa x Abandoned Foundry source/static checkpoint remains integrated on `main` under `Current/207_S1.42AK_BMAFDIAG1_SOURCE_STATIC_INTEGRATION_RECONCILIATION.md`, and its separately bounded inactive review build now passes under `Current/208_S1.42AK_BMAFDIAG1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md` with machine evidence at `BuildSpecs/S1.42AK-BMAFDIAG1_BUILD_EVIDENCE/REVIEW_BUILD_CHECKPOINT.json`. Exact reviewed bytes are locked to Actions artifact `11106178288`: profile SHA-256 `b8611f58678890065f214f788051c203f4d72c59040e53e51c64c89c5958fdc2` and BMAFDIAG1 DLL SHA-256 `c079368dd3736decadee00125a42319f5da29907aad207d7b82a6494f19a7ce1`. They remain unpublished, not Gale-imported and not runtime-active. The review profile derives directly from exact accepted S1.42AK and contains only the proven owner-default Foundry content-configuration activation plus exact `Black Mesa:100` availability delta; Black Mesa x Abandoned Foundry remains `NOT_YET_PROVEN`."
    )
    require(old in text, "knowledge-map BMAFDIAG1 anchor drift")
    text = text.replace(old, new, 1)
    text, count = re.subn(r"Exact next action: .*?(?=\n\n## Authority rule)", "Exact next action: " + NEXT, text, count=1, flags=re.S)
    require(count == 1, "knowledge-map next action replacement failed")
    MAP.write_text(text, encoding="utf-8")


def render_and_check() -> None:
    subprocess.run([sys.executable, "RepositoryTools/render_current_navigation.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "RepositoryTools/render_current_navigation.py", "--check"], cwd=ROOT, check=True)
    json.loads(STATE.read_text(encoding="utf-8"))
    json.loads(MACHINE.read_text(encoding="utf-8"))


def main() -> None:
    update_state()
    update_evidence()
    update_lifecycle()
    update_map()
    render_and_check()
    print("PASS: BMAFDIAG1 inactive review-build reconciliation rendered")


if __name__ == "__main__":
    main()
