#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state_path = ROOT / "Current/CURRENT_STATE.json"
state = json.loads(state_path.read_text(encoding="utf-8"))

assert state["accepted_baseline"]["build_id"] == "S1.42AK"
assert state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1"
assert state["runtime_test_outstanding"] is True
assert state["controllers"]["runtime_active_build"] == "S1.42AK-BMDSFIX1-DIAG1"
assert (ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").read_text(encoding="utf-8").strip() == "S1.42AK-BMDSFIX1-DIAG1"
assert state["controllers"]["build_enabled"] is False
scope = state["selected_scope"]
assert scope["diagnostic_revision"]["build_id"] == "S1.42AK-BMDSFIX1-DIAG1"
assert scope["diagnostic_revision"]["profile_sha256"] == "31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e"
assert (ROOT / "Current/181_S1.42AK_BMDSFIX1_DIAG1_PATH_LENGTH_BLOCK_AND_DIAG1PATH1_SOURCE_STATIC.md").is_file()
assert (ROOT / "Current/182_S1.42AK_BMDSFIX1_DIAG1PATH1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md").is_file()

next_action = (
    "Perform the separate S1.42AK-BMDSFIX1-DIAG1PATH1 exact-byte publication checkpoint from the frozen "
    "review source Actions artifact 10835876163 / review run 36063701766, materializing only the reviewed "
    "profile bytes SHA-256 0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6 and readable "
    "snapshot, and revalidate the identity-only delta without changing runtime controllers. Do not import or rerun "
    "the long-name DIAG1 profile. Profile-index reconciliation and explicit DIAG1PATH1 runtime activation remain "
    "later gates; the regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived."
)

scope["status"] = "PHASE_C3F18_DIAG1_PRELOADER_BLOCKED_DIAG1PATH1_REVIEWED_PUBLICATION_OUTSTANDING"
scope["finding"] = (
    "The exact published/indexed S1.42AK-BMDSFIX1-DIAG1 remains the repository runtime/evidence pointer, but two "
    "consecutive local launches are now bounded preloader-block evidence: the long Gale profile identity produces "
    "260/262-character nested runtime paths and BepInEx/Mono fails before any diagnostic arming or selection evidence. "
    "The long-name DIAG1 must not be rerun. S1.42AK-BMDSFIX1-DIAG1PATH1 is the separately reviewed identity-only "
    "successor with short profile name LC V1 S1.42AK-D1P1; inactive review build passed from frozen artifact "
    "10835876163 with profile SHA-256 0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6, "
    "changing only export.r2x profileName while preserving all diagnostic/gameplay DLL, package and config bytes. "
    "DIAG1PATH1 is not yet published, indexed or runtime-armed. S1.42AK-BMDSFIX1 remains the active gameplay candidate "
    "/ not accepted and its regular exact-byte Black Mesa x DeepSewersFlow qualification is not waived."
)
scope["analysis_contract"] = (
    "Keep S1.42AK-BMDSFIX1 as the active gameplay candidate / not accepted. Treat S1.42AK-BMDSFIX1-DIAG1 as the "
    "still-routed historical diagnostic target that is locally preloader-blocked and must not be rerun. Treat "
    "S1.42AK-BMDSFIX1-DIAG1PATH1 only as the inactive reviewed identity-only successor until exact-byte publication, "
    "profile-index reconciliation and an explicit later runtime-activation checkpoint complete. Do not infer BMDSFIX1 "
    "acceptance from either diagnostic, do not waive the regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow gate, "
    "and do not mix the separate Black Mesa x Greenhouse/BMGHDIAG scope into this successor."
)
scope["next_action"] = next_action
scope["diagnostic_launch_block_record"] = "Current/181_S1.42AK_BMDSFIX1_DIAG1_PATH_LENGTH_BLOCK_AND_DIAG1PATH1_SOURCE_STATIC.md"
scope["diagnostic_successor_review_checkpoint"] = "Current/182_S1.42AK_BMDSFIX1_DIAG1PATH1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md"
scope["diagnostic_revision"]["runtime_validation_status"] = "PRELOADER_BLOCKED_BEFORE_DIAGNOSTIC_EXECUTION_DO_NOT_RERUN_DIAG1PATH1_PUBLICATION_OUTSTANDING"
scope["diagnostic_successor_revision"] = {
    "build_id": "S1.42AK-BMDSFIX1-DIAG1PATH1",
    "status": "INACTIVE_REVIEW_BUILD_PASS_NOT_PUBLISHED_NOT_INDEXED_NOT_ARMED",
    "classification": "DIAGNOSTIC_SUPPORT_ONLY_NEVER_ACCEPT",
    "base_build_id": "S1.42AK-BMDSFIX1-DIAG1",
    "base_profile": "Profiles/LC V1 S1.42AK-BMDSFIX1-DIAG1 Deterministic Deep Sewers Selector.r2z",
    "base_sha256": "31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e",
    "profile_name": "LC V1 S1.42AK-D1P1",
    "output_profile": "Profiles/LC V1 S1.42AK-D1P1.r2z",
    "reviewed_head": "8c6b5b60994985d15c087a72d52f8c178c15d697",
    "review_run": 36063701766,
    "review_artifact_id": 10835876163,
    "review_artifact_zip_sha256": "b38036a3ae1e7d49c9890a8d9343252d8d0e19cfcde854b2410a91519968b90d",
    "profile_sha256": "0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6",
    "diagnostic_dll_sha256": "3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1",
    "bmdsfix1_dll_sha256": "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92",
    "normalizer_sha256": "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06",
    "archive_members_verified": 338,
    "changed_existing_members": ["export.r2x"],
    "added_members": [],
    "removed_members": [],
    "package_changes": 0,
    "config_changes": 0,
    "local_plugin_builds": 0,
    "observed_old_path_lengths": [260, 262],
    "reviewed_new_path_lengths": [215, 217],
    "review_checkpoint": "Current/182_S1.42AK_BMDSFIX1_DIAG1PATH1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md",
    "published": False,
    "runtime_armed": False
}
state["next_action"] = next_action
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

lifecycle_path = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
lifecycle = lifecycle_path.read_text(encoding="utf-8")
if "## DIAG1 launch block and DIAG1PATH1 reviewed successor" not in lifecycle:
    marker = "## Live execution state\n"
    assert marker in lifecycle
    section = """## DIAG1 launch block and DIAG1PATH1 reviewed successor

Two consecutive local launches of the exact published/indexed `S1.42AK-BMDSFIX1-DIAG1` profile failed inside the BepInEx/Mono preloader before any `[BMDSFIX1-DIAG1] ARMED` or selection evidence. Read-only inspection proved the named LC Office preloader and SoundAPI DLLs were physically present, while the long Gale profile identity made the two failing full paths exactly 260 and 262 characters. Decision/preparation authority: `Current/181_S1.42AK_BMDSFIX1_DIAG1_PATH_LENGTH_BLOCK_AND_DIAG1PATH1_SOURCE_STATIC.md`. These launches are preloader-block evidence only; they neither accept nor reject BMDSFIX1, and the long-name DIAG1 must not be rerun.

The separately versioned `S1.42AK-BMDSFIX1-DIAG1PATH1` identity-only successor has passed its inactive review build under `Current/182_S1.42AK_BMDSFIX1_DIAG1PATH1_INACTIVE_REVIEW_BUILD_CHECKPOINT.md`. Frozen publication source is Actions artifact `10835876163` from review run `36063701766`; reviewed profile SHA-256 is `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`. It shortens the profile identity to `LC V1 S1.42AK-D1P1`, reducing the observed paths to 215/217 characters, while changing only `export.r2x` profile identity metadata and preserving all DLL/package/config bytes. DIAG1PATH1 is not yet published, indexed or runtime-armed.

"""
    lifecycle = lifecycle.replace(marker, section + marker, 1)

live_start = lifecycle.index("## Live execution state\n")
next_start = lifecycle.index("## Exact next project action\n", live_start)
perm_start = lifecycle.index("## Permanent Gale workflow\n", next_start)
live_block = """## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK-BMDSFIX1 — active runtime candidate / not accepted**.
- Active gameplay candidate: **S1.42AK-BMDSFIX1**.
- Runtime/evidence pointer: **S1.42AK-BMDSFIX1-DIAG1**, but the long-name profile is **preloader-blocked and must not be rerun**.
- Reviewed diagnostic successor: **S1.42AK-BMDSFIX1-DIAG1PATH1 — inactive review PASS / not published / not indexed / not armed / never accept**.
- Runtime test outstanding: **yes — regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow qualification remains outstanding and unwaived; no new DIAG1PATH1 runtime is authorized before publication/index/activation**.
- Preserved partial evidence: **Black Mesa x Substation non-target control PASS** at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/`.
- Selected scope: **Universal Interior Viability / Equal Availability — DIAG1PATH1 exact-byte publication next; gameplay candidate unchanged**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 candidate bytes.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1-DIAG1` remains unchanged until a later explicit successor activation; it is runtime/evidence routing, not acceptance authority.
- S1.42AK remains the accepted rollback baseline; BMDSFIX1 remains the unaccepted gameplay candidate; Greenhouse/BMGHDIAG remains separate.

"""
next_block = """## Exact next project action

Perform the separate `S1.42AK-BMDSFIX1-DIAG1PATH1` exact-byte publication checkpoint from frozen Actions artifact `10835876163` / review run `36063701766`. Materialize only the reviewed profile bytes SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6` and readable snapshot, then revalidate the identity-only delta without changing runtime controllers. Do **not** import or rerun the long-name DIAG1 profile. Profile-index reconciliation and explicit DIAG1PATH1 runtime activation remain later gates. BMDSFIX1 remains not accepted and its regular exact-byte Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived.

"""
perm_block = """## Permanent Gale workflow

The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`. `RuntimeInbox/ACTIVE_BUILD.txt` still points to `S1.42AK-BMDSFIX1-DIAG1`, so invoking the helper now would still resolve the preloader-blocked long-name diagnostic and is therefore **not authorized**. Do not change that controller merely to bypass publication/indexing. After DIAG1PATH1 is exact-byte-published, profile-index-reconciled and explicitly runtime-activated in later gates, the repository-driven helper must resolve the newly authorized successor exact bytes. None of these diagnostic lifecycle operations may promote or accept BMDSFIX1.
"""
lifecycle = lifecycle[:live_start] + live_block + next_block + perm_block
lifecycle_path.write_text(lifecycle, encoding="utf-8")

map_path = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
km = map_path.read_text(encoding="utf-8")
start_marker = "The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation remains the **active gameplay runtime candidate / not accepted**."
start = km.index(start_marker)
end = km.index("\n\n## Authority rule", start)
new_anchor = """The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation remains the **active gameplay runtime candidate / not accepted**. Exact runtime evidence is ingested at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/` with raw log SHA-256 `9a8cf28bbfc050cf9247cffacc890ea1b4e7215329db4ecfc9085f3f8f0ff2cb`. The run armed BMDSFIX1 but Black Mesa selected Substation, so no `APPLIED` marker occurred; this is preserved as the exact-byte non-target control. The remaining regular gameplay gate is only Black Mesa x `DeepSewersFlow`; decision authority: `Current/175_S1.42AK_BMDSFIX1_PARTIAL_RUNTIME_EVIDENCE_NON_TARGET_CONTROL.md`. `BuildSpecs/current.json` remains disabled while guarding the exact BMDSFIX1 candidate.

The published/indexed `S1.42AK-BMDSFIX1-DIAG1` still occupies the runtime/evidence pointer, but two consecutive launches are now documented as preloader-blocked before diagnostic execution because the long Gale profile identity produced 260/262-character nested runtime paths. It must not be rerun. `S1.42AK-BMDSFIX1-DIAG1PATH1` is the reviewed identity-only successor: inactive review build PASS, short profile identity `LC V1 S1.42AK-D1P1`, reviewed profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`, frozen publication source artifact `10835876163`; it is not yet published, indexed or armed. The immediate repository task is its separate exact-byte publication checkpoint, not a gameplay launch. BMDSFIX1 remains not accepted, its regular qualification remains outstanding and unwaived, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse/BMGHDIAG remains separate."""
km = km[:start] + new_anchor + km[end:]
map_path.write_text(km, encoding="utf-8")

print("DIAG1PATH1 handover lifecycle reconciliation prepared")
