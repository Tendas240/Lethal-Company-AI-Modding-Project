#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_ID = "S1.42AK-BMGHDIAG1"
BASE_ID = "S1.42AK"
BASE_PROFILE = "Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z"
BASE_SHA = "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
PROFILE = "Profiles/LC V1 S1.42AK-BMGHDIAG1 Black Mesa Greenhouse Diagnostic.r2z"
PROFILE_SHA = "7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90"
DLL_SHA = "4a1f304a716bf7cacb6496f5047bb0e498ed68bde00fc9f4128fa001adaa30b2"
NORMALIZER_SHA = "901c02a8e85d33af24d0aa906faa6052a7de33faa7dfbeeca590bbd8a8f59a06"
LLL_SHA = "b95aad3813dd7dc1d50aa29c9606660022b149790905a1589180e19d7c157c8c"
ACTIVATION = "Current/170_S1.42AK_BMGHDIAG1_RUNTIME_ACTIVATION.md"
BUILD_RESULT = "BuildSpecs/S1.42AK-BMGHDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json"
STATIC_EVIDENCE = "BuildSpecs/S1.42AK-BMGHDIAG1_BUILD_EVIDENCE/STATIC_VERIFICATION.json"
PUBLICATION_EVIDENCE = "BuildSpecs/S1.42AK-BMGHDIAG1_BUILD_EVIDENCE/PUBLICATION_VERIFICATION.md"
PROFILE_SOURCES = "ProfileSources/S1.42AK-BMGHDIAG1/"
FILE_INDEX = "ProfileSources/S1.42AK-BMGHDIAG1/FILE_INDEX.json"
EXPORT = "ProfileSources/S1.42AK-BMGHDIAG1/export.r2x"
TODAY = "2026-09-23"
MARKER_OLD = "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=false -->"
MARKER_NEW = "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK candidate=none runtime_test_outstanding=true -->"


def load_json(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def write_json(rel: str, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}")
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, body: str, label: str) -> str:
    pattern = re.escape(start) + r".*?" + re.escape(end)
    repl = start + body + end
    new, count = re.subn(pattern, repl, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: section replacement count={count}")
    return new


# Fail closed on the exact publication/base identities before writing lifecycle state.
result = load_json(BUILD_RESULT)
assert result["build_id"] == BUILD_ID
assert result["base_profile"] == BASE_PROFILE
assert result["base_sha256"] == BASE_SHA
assert result["output_profile"] == PROFILE
assert result["output_sha256"] == PROFILE_SHA
assert result["zip_members"] == 337
assert result["changed_existing_members"] == ["export.r2x"]
assert result["added_members"] == ["BepInEx/plugins/S142AKBMGHDiag1/S142AKBMGHDiag1.dll"]

state = load_json("Current/CURRENT_STATE.json")
assert state["accepted_baseline"]["build_id"] == BASE_ID
assert state["accepted_baseline"]["profile"] == BASE_PROFILE
assert state["accepted_baseline"]["sha256"] == BASE_SHA
assert state["latest_built_artifact"]["build_id"] == BASE_ID
assert state["active_candidate"] is None
assert state["runtime_test_outstanding"] is False
assert state["controllers"]["build_enabled"] is False
assert state["controllers"]["runtime_active_build"] == BASE_ID
assert state["selected_scope"]["scope_id"] == "UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY"
assert "diagnostic_revision" not in state["selected_scope"]

scope = state["selected_scope"]
state["updated"] = TODAY
state["runtime_test_outstanding"] = True
scope["status"] = "PHASE_C3F17_BLACK_MESA_GREENHOUSE_DIAGNOSTIC_PUBLISHED_ARMED_RUNTIME_OUTSTANDING"
scope["finding"] = (
    "Phase C3 static/source analysis has narrowed Black Mesa x Greenhouse to a targeted runtime-evidence boundary. "
    "The exact reviewed S1.42AK-BMGHDIAG1 publication is now integrated on main and is authorized only as a direct diagnostic runtime target over exact accepted S1.42AK. "
    "The diagnostic preserves Black Mesa Dawn/native ownership, existing Greenhouse availability, accepted S1.42AB normalization and the unchanged B3 matrix; it does not establish the pairing as viable until the runtime contract passes."
)
scope["analysis_contract"] = (
    "Runtime-test exact published S1.42AK-BMGHDIAG1 on Black Mesa. Require successful [BMGHDIAG1] ARMED and SELECTED markers for the existing Greenhouse / GreenhouseFlow wrapper at normalized rarity 100, successful DunGen generation, TOPOLOGY_OK ids=0,1,2,3 with unique opposite-side pairs, normal main-entrance entry and exit, direct player traversal of alternate IDs 1,2,3 where practical, no REFUSED or TOPOLOGY_INCONCLUSIVE marker, no generation abort, and no new severe persistent target-attributable routing/NavMesh failure. Preserve S1.42AK as accepted/latest, keep active_candidate null, do not modify the B3 matrix, do not duplicate-register Black Mesa, and do not open the separate Black-Mesa/Pikmin routing repair scope."
)
scope["next_action"] = (
    "Import and run exact published S1.42AK-BMGHDIAG1 on Black Mesa for the bounded Black Mesa x Greenhouse runtime qualification, exercise the main entrance plus alternate exits 1, 2 and 3 as required by the diagnostic contract, then upload the resulting LogOutput.log under S1.42AK-BMGHDIAG1 for repository ingestion."
)
scope["diagnostic_build_plan"] = "BuildSpecs/S1.42AK-BMGHDIAG1_PLAN.md"
scope["diagnostic_static_evidence"] = STATIC_EVIDENCE
scope["diagnostic_publication_evidence"] = PUBLICATION_EVIDENCE
scope["diagnostic_runtime_activation"] = ACTIVATION
scope["diagnostic_revision"] = {
    "build_id": BUILD_ID,
    "status": "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED",
    "base_build_id": BASE_ID,
    "base_profile": BASE_PROFILE,
    "base_sha256": BASE_SHA,
    "profile": PROFILE,
    "sha256": PROFILE_SHA,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC_EVIDENCE,
    "publication_evidence": PUBLICATION_EVIDENCE,
    "activation_record": ACTIVATION,
    "source_pr": 138,
    "reviewed_head": "f01b6d4f456d3ee133b30ac62f432de75ef3830b",
    "publication_pr_head": "bb5e05fa93bbf233f3faf829c80e450ffe9bc8b2",
    "main_publication_commit": "75326785bb5577956d581a57781af0f92022b1c3",
    "review_artifact_id": 10745290545,
    "review_artifact_zip_sha256": "f34ee6dcf06d2f803159554c1cef2e9f587ca0e38f837f96e287c28c13151947",
    "build_gate_run": 35849491391,
    "published_profile_commit": "587f15ec8615ec8bb6a7419c3905d2b84d18e396",
    "exact_head_lll_provenance_gate_run": 35854730486,
    "exact_head_source_static_gate_run": 35854730351,
    "exact_head_build_archive_gate_run": 35854730359,
    "profile_sha256": PROFILE_SHA,
    "diagnostic_dll_sha256": DLL_SHA,
    "lll_sha256": LLL_SHA,
    "normalizer_sha256": NORMALIZER_SHA,
    "runtime_role": "DIAGNOSTIC_ONLY_BLACK_MESA_GREENHOUSE_FORCE_SELECTION_AND_READ_ONLY_ENTRANCE_OBSERVATION",
    "runtime_validation_status": "PUBLISHED_ARMED_RUNTIME_BLACK_MESA_GREENHOUSE_QUALIFICATION_OUTSTANDING_NOT_ACCEPTED",
    "runtime_evidence": None,
}
state["next_action"] = scope["next_action"]
state["controllers"]["runtime_active_build"] = BUILD_ID
write_json("Current/CURRENT_STATE.json", state)

# Runtime evidence attribution pointer.
(ROOT / "RuntimeInbox/ACTIVE_BUILD.txt").write_text(BUILD_ID + "\n", encoding="utf-8")

# Register diagnostic identity so profile-indexing is canonical rather than filename-derived.
hashes = load_json("Profiles/EXPECTED_HASHES.json")
if PROFILE in hashes:
    raise RuntimeError("BMGHDIAG1 profile identity already registered unexpectedly")
hashes[PROFILE] = {
    "build_id": BUILD_ID,
    "sha256": PROFILE_SHA,
    "note": "Diagnostic-only active runtime target over accepted S1.42AK; canonical readable snapshot is ProfileSources/S1.42AK-BMGHDIAG1/. Not a gameplay lineage entry or gameplay base.",
}
write_json("Profiles/EXPECTED_HASHES.json", hashes)

# Artifact-evidence integrity index: keep diagnostics pending until an explicit runtime decision.
integrity = load_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json")
assert not any(p.get("build_id") == BUILD_ID for p in integrity.get("profiles", []))
assert not any(p.get("build_id") == BUILD_ID for p in integrity.get("pending_profiles", []))
integrity["updated"] = TODAY
integrity.setdefault("pending_profiles", []).append({
    "build_id": BUILD_ID,
    "role": "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING",
    "profile": PROFILE,
    "profile_sha256": PROFILE_SHA,
    "profile_sources": PROFILE_SOURCES,
    "file_index": FILE_INDEX,
    "export": EXPORT,
    "build_plan": "BuildSpecs/S1.42AK-BMGHDIAG1_PLAN.md",
    "build_result": BUILD_RESULT,
    "static_evidence": STATIC_EVIDENCE,
    "publication_evidence": PUBLICATION_EVIDENCE,
    "activation_record": ACTIVATION,
    "diagnostic_dll_sha256": DLL_SHA,
    "runtime_evidence_required": False,
    "note": "Direct diagnostic overlay over exact accepted S1.42AK for Black Mesa x Greenhouse runtime qualification only; not a gameplay lineage entry or gameplay base.",
})
integrity.setdefault("runtime_evidence_policy", {})["pending_diagnostic_role"] = "ACTIVE_RUNTIME_DIAGNOSTIC_PENDING"
integrity.setdefault("verified_repository_api_observations", []).append(
    "S1.42AK-BMGHDIAG1 is repository-published at SHA-256 7f494640f47210bf230a2f0950bd836d65b969a47be2af1252fc564463bc6d90 with readable ProfileSources/FILE_INDEX evidence and is tracked only as an active pending diagnostic until an explicit runtime decision."
)
write_json("Current/ARTIFACT_EVIDENCE_INTEGRITY.json", integrity)

activation = f"""# S1.42AK-BMGHDIAG1 Runtime Activation

**Date:** {TODAY}  
**Status:** PUBLISHED / ACTIVE DIAGNOSTIC RUNTIME TARGET / TEST OUTSTANDING / NOT ACCEPTED  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Diagnostic:** {BUILD_ID}  
**Diagnostic profile:** `{PROFILE}`  
**Diagnostic SHA-256:** `{PROFILE_SHA}`  
**Diagnostic DLL SHA-256:** `{DLL_SHA}`  
**Exact parent:** accepted S1.42AK / `{BASE_SHA}`  
**Publication evidence:** `{PUBLICATION_EVIDENCE}`

## Activation decision

The exact reviewed and repository-published S1.42AK-BMGHDIAG1 artifact is authorized as the active runtime-evidence target for the single Black Mesa x Greenhouse qualification required by Phase C3F17.

This is a diagnostic-only runtime target, not a gameplay successor. S1.42AK remains the accepted gameplay baseline and latest normal built artifact. `active_candidate` remains null and `BuildSpecs/current.json` remains disabled. The B3 matrix is unchanged.

The diagnostic is a direct overlay over exact accepted S1.42AK and uses the canonical Gale direct-diagnostic authority chain:

1. `RuntimeInbox/ACTIVE_BUILD.txt` identifies `{BUILD_ID}`;
2. `CURRENT_STATE.selected_scope.diagnostic_revision` identifies the same build/profile/SHA;
3. `{BUILD_RESULT}` identifies the same output profile/SHA;
4. its base build/profile/SHA identify exact accepted S1.42AK;
5. `Current/AUTO_BUILD_RESULT.json` identifies that same exact S1.42AK parent;
6. accepted/latest lifecycle identities remain S1.42AK.

No diagnostic-parent hop is required.

## Exact published bytes

- profile SHA-256: `{PROFILE_SHA}`;
- diagnostic DLL SHA-256: `{DLL_SHA}`;
- LethalLevelLoader 1.7.12 DLL SHA-256: `{LLL_SHA}`;
- accepted S1.42AB normalizer SHA-256: `{NORMALIZER_SHA}`;
- reviewed artifact ID: `10745290545`;
- reviewed artifact ZIP SHA-256: `f34ee6dcf06d2f803159554c1cef2e9f587ca0e38f837f96e287c28c13151947`;
- reviewed build/static gate: run `35849491391`;
- publication commit: `587f15ec8615ec8bb6a7419c3905d2b84d18e396`;
- PR #138 exact-head gates: LLL provenance `35854730486`, source/static `35854730351`, build/archive `35854730359`;
- main publication integration commit: `75326785bb5577956d581a57781af0f92022b1c3`.

The earlier main `Index uploaded profile` failure is resolved by registering this diagnostic in `Profiles/EXPECTED_HASHES.json`; the mapping is diagnostic-only and does not add a gameplay lineage entry.

## Runtime qualification contract

Run the exact diagnostic on **Black Mesa**. A sufficient run must establish all of the following:

1. `[BMGHDIAG1] ARMED` appears without a startup refusal;
2. `[BMGHDIAG1] SELECTED Black Mesa Greenhouse / GreenhouseFlow; normalized rarity=100; pool=<N>->1` appears;
3. DunGen completes without exhausted retries or fatal generation abort;
4. `[BMGHDIAG1] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4` appears;
5. the player normally enters and exits through the main entrance;
6. alternate IDs 1, 2 and 3 are directly traversed by the player; bidirectional use should be obtained where practical;
7. the player reports no severe clipping or inaccessible required entrance geometry at exercised endpoints;
8. no new severe/persistent target-attributable routing or NavMesh failure is present;
9. no `[BMGHDIAG1] REFUSED` or `TOPOLOGY_INCONCLUSIVE` marker invalidates the run.

Successful native teleport alone must not be overclaimed as visual geometry proof. The separate Black-Mesa/Pikmin routing-recovery scope remains closed during this test.

## Preserved boundaries

- S1.42AK remains accepted/latest;
- S1.42AB InteriorWeightNormalization remains unchanged;
- Black Mesa remains Dawn/native-owned and is not duplicate-registered;
- Greenhouse availability remains unchanged;
- B3 matrix remains unchanged;
- Shatteredrooms x Experimentation/Embrion remain untouched;
- no universal interior override is authorized by this diagnostic.

## Evidence attribution and rollback

Runtime evidence must be uploaded while `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD_ID}` so ingestion is attributed to the diagnostic namespace. The diagnostic is never promoted merely by being runtime-active.

Rollback is exact accepted S1.42AK through the canonical Gale replacement workflow.
"""
(ROOT / ACTIVATION).write_text(activation, encoding="utf-8")

# Generated navigation mirrors are regenerated from CURRENT_STATE, never hand-edited.
subprocess.run([sys.executable, "RepositoryTools/render_current_navigation.py"], cwd=ROOT, check=True)

# Canonical lifecycle router.
p = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
text = p.read_text(encoding="utf-8")
text = replace_once(text, MARKER_OLD, MARKER_NEW, str(p))
text = re.sub(r"\*\*Last-Validated:\*\* \d{4}-\d{2}-\d{2}", f"**Last-Validated:** {TODAY}", text, count=1)
insert = f"""## Active targeted runtime diagnostic — Black Mesa x Greenhouse

Exact published `{BUILD_ID}` is now the active diagnostic-only runtime target over accepted/latest S1.42AK. Profile: `{PROFILE}`; SHA-256 `{PROFILE_SHA}`. It force-selects only the already-viable Greenhouse wrapper on Black Mesa after accepted normalization and observes native EntranceTeleport use read-only. It does not alter Black Mesa ownership, Greenhouse availability, the B3 matrix or accepted S1.42AB normalization.

The runtime gate requires successful diagnostic arming/selection, DunGen completion, `TOPOLOGY_OK` for IDs 0..3, normal main-entry/exit traversal, direct use of alternate IDs 1..3 where practical, and no blocking diagnostic/refusal or severe target-attributable routing failure. Publication/runtime activation evidence is `{ACTIVATION}`.

"""
text = text.replace("## Live execution state\n", insert + "## Live execution state\n", 1)
text = replace_section(
    text,
    "## Live execution state\n",
    "## Exact next project action",
    f"\n- Accepted baseline: **S1.42AK**.\n- Latest built artifact: **S1.42AK**.\n- Active gameplay candidate: **none**.\n- Active diagnostic runtime target: **{BUILD_ID}**.\n- Runtime test outstanding: **yes**.\n- Selected scope: **Universal Interior Viability / Equal Availability — Phase C3F17 targeted Black Mesa x Greenhouse runtime qualification**.\n- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`.\n- `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD_ID}`.\n- No gameplay successor or universal override is armed.\n\n",
    str(p),
)
text = replace_section(
    text,
    "## Exact next project action\n",
    "## Permanent Gale workflow",
    f"\n{scope['next_action']}\n\n",
    str(p),
)
text = re.sub(
    r"The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24\.ps1`[^\n]*",
    "The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1` at helper revision `2026-09-18-import-uia-v2.4.2-one-hop-diagnostic-parent-chain`. The active BMGHDIAG1 target uses its fail-closed direct-diagnostic path over exact accepted/latest S1.42AK; no diagnostic-parent hop is required.",
    text,
    count=1,
)
p.write_text(text, encoding="utf-8")

# Human topic router.
p = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
text = p.read_text(encoding="utf-8")
text = replace_once(text, MARKER_OLD, MARKER_NEW, str(p))
text = re.sub(r"\*\*Last-Validated:\*\* \d{4}-\d{2}-\d{2}", f"**Last-Validated:** {TODAY}", text, count=1)
text, n = re.subn(
    r"No gameplay candidate, diagnostic target or runtime test is armed; `BuildSpecs/current\.json` remains disabled and `RuntimeInbox/ACTIVE_BUILD\.txt = S1\.42AK`\. The next action is Phase C3 External-moon semantics/topology analysis defined by `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN\.md`\.",
    f"No gameplay candidate or successor build is armed. Exact published `{BUILD_ID}` is the active diagnostic-only runtime target for the bounded Black Mesa x Greenhouse C3F17 qualification; `BuildSpecs/current.json` remains disabled and `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD_ID}`. The B3 matrix remains unchanged until this runtime evidence is ingested and interpreted.",
    text,
    count=1,
)
if n != 1:
    raise RuntimeError(f"{p}: failed to replace current lifecycle anchor")
p.write_text(text, encoding="utf-8")

# Live roadmap.
p = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
text = p.read_text(encoding="utf-8")
text = replace_once(text, MARKER_OLD, MARKER_NEW, str(p))
text = re.sub(r"\*\*Last-Validated:\*\* \d{4}-\d{2}-\d{2}", f"**Last-Validated:** {TODAY}", text, count=1)
text = replace_once(
    text,
    "There is no active gameplay candidate, no active diagnostic target, no armed successor build and no outstanding runtime test. `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK`; `BuildSpecs/current.json` remains disabled.",
    f"There is no active gameplay candidate or armed successor build. Exact published `{BUILD_ID}` is the active diagnostic-only runtime target and one runtime test is outstanding. `RuntimeInbox/ACTIVE_BUILD.txt = {BUILD_ID}`; `BuildSpecs/current.json` remains disabled.",
    str(p),
)
text = text.replace("**Universal Interior Viability / Equal Availability — SELECTED / BASELINE INVENTORY OUTSTANDING.**", "**Universal Interior Viability / Equal Availability — SELECTED / PHASE C3F17 TARGETED RUNTIME QUALIFICATION OUTSTANDING.**", 1)
text = replace_once(
    text,
    "Initial S1.42AK config extraction shows 28 LLL custom-dungeon sections, 27 already active with `Vanilla:100,Custom:100`; Black Mesa remains a separate owner case. This is not yet the complete current flow inventory. No build or runtime test is armed.",
    f"Phases A through C3F17 static analysis preserve the authoritative 30x53 B3 matrix while narrowing Black Mesa x Greenhouse to a targeted runtime proof boundary. `{BUILD_ID}` is armed only for that pair; no universal override or gameplay successor is armed.",
    str(p),
)
p.write_text(text, encoding="utf-8")

# Artifact integrity human index.
p = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
text = p.read_text(encoding="utf-8")
text = replace_once(text, MARKER_OLD, MARKER_NEW, str(p))
text = re.sub(r"\*\*Last-Validated:\*\* \d{4}-\d{2}-\d{2}", f"**Last-Validated:** {TODAY}", text, count=1)
needle = "- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.\n"
addition = needle + f"- **{BUILD_ID}** — active runtime diagnostic pending for Black Mesa x Greenhouse; profile `{PROFILE}`, SHA-256 `{PROFILE_SHA}`, readable snapshot `{PROFILE_SOURCES}`.\n"
text = replace_once(text, needle, addition, str(p))
text = replace_once(
    text,
    "There is currently no active runtime diagnostic or gameplay candidate.",
    f"`{BUILD_ID}` is the active diagnostic runtime target; there is no active gameplay candidate. It remains pending/unaccepted until an explicit runtime decision.",
    str(p),
)
p.write_text(text, encoding="utf-8")

# Canonical interiors topic: append only the lifecycle-relevant bounded runtime gate.
p = ROOT / "Knowledge/INTERIORS_AND_LLL.md"
text = p.read_text(encoding="utf-8")
heading = "## Selected universal viability / equal availability investigation\n"
if heading not in text:
    raise RuntimeError(f"{p}: selected-scope heading not found")
section = f"""## Active C3F17 targeted Black Mesa x Greenhouse runtime qualification

Exact published `{BUILD_ID}` is the active diagnostic-only runtime target over accepted S1.42AK. Its only gameplay mutation is deterministic selection of the already-viable `Greenhouse / GreenhouseFlow` wrapper on Black Mesa after accepted rarity normalization; its EntranceTeleport hook is read-only observation after native teleport behavior. Black Mesa remains Dawn/native-owned, Greenhouse availability is unchanged, and the B3 matrix is unchanged.

The pair remains `NOT_YET_PROVEN` until runtime evidence satisfies the contract in `{ACTIVATION}`: successful arming/selection, DunGen completion, unique opposite-side entrance pairs for IDs 0..3, main entrance entry/exit, alternate IDs 1..3 exercised where practical, acceptable geometry, and no blocking diagnostic/refusal or severe target-attributable routing/NavMesh failure. The separate Black-Mesa/Pikmin routing scope remains excluded.

"""
text = text.replace(heading, section + heading, 1)
p.write_text(text, encoding="utf-8")

# Remove the one-shot transformer/workflow from the final branch tree before commit.
for rel in (
    "RepositoryTools/arm_bmghdiag1_runtime.py",
    ".github/workflows/arm-bmghdiag1-runtime.yml",
):
    path = ROOT / rel
    if path.exists():
        path.unlink()

# Focused local gates before the workflow commits anything.
subprocess.run([sys.executable, "RepositoryTools/render_current_navigation.py", "--check"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "RepositoryTools/current_state_semantic_validator.py"], cwd=ROOT, check=True)
print("PASS: BMGHDIAG1 runtime arming transition rendered and semantically validated")
