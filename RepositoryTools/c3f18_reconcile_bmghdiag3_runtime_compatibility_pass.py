#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "Current/CURRENT_STATE.json"
ACTIVE_PATH = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
INTEGRITY_JSON = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.json"
INTEGRITY_MD = ROOT / "Current/ARTIFACT_EVIDENCE_INTEGRITY.md"
LIFECYCLE = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
MAP_MD = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
ROADMAP = ROOT / "Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md"
DECISION_PATH = ROOT / "Current/199_S1.42AK_BMGHDIAG3_RUNTIME_COMPATIBILITY_PASS.md"
INDEX_PATH = ROOT / "RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/INDEX.json"
LOG_PATH = ROOT / "RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/raw/LogOutput.log"
BUILDSPEC_PATH = ROOT / "BuildSpecs/current.json"

BMG = "S1.42AK-BMGHDIAG3"
BMDS = "S1.42AK-BMDSFIX1"
ACCEPTED = "S1.42AK"
PROFILE_SHA = "7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace"
DLL_SHA = "d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352"
LOG_SHA = "e30858fcebce0fc51f092170b50bd439290cf4752bf0917ae28d66e29a37a9f8"
BMDS_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
DECISION_REL = "Current/199_S1.42AK_BMGHDIAG3_RUNTIME_COMPATIBILITY_PASS.md"
EVIDENCE_REL = "RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/"
INDEX_REL = EVIDENCE_REL + "INDEX.json"
SCOPE_STATUS = "PHASE_C3F18_BLACK_MESA_GREENHOUSE_RUNTIME_COMPATIBILITY_PASS_BMDSFIX1_TARGET_QUALIFICATION_PASSIVE_OUTSTANDING"
GREENHOUSE_STATUS = "PASS_RUNTIME_COMPATIBLE_BLACK_MESA_GREENHOUSE_DIAGNOSTIC_ONLY"

OLD_MARKER = "<!-- LIVE_STATE: accepted=S1.42AK latest=S1.42AK-BMDSFIX1 candidate=S1.42AK-BMDSFIX1 runtime_test_outstanding=true -->"
NEW_MARKER = OLD_MARKER

NEXT_ACTION = (
    "Continue the repository-native Phase C3 External target-moon semantics/topology analysis from the completed "
    "Black Mesa x Greenhouse runtime-compatibility PASS. Preserve the unchanged Phase-B3 availability matrix, "
    "accepted S1.42AK, and unaccepted S1.42AK-BMDSFIX1. No new BMGHDIAG3 run is authorized, and no dedicated "
    "BMDSFIX1 Black Mesa reroll is released: its regular exact-byte Black Mesa x DeepSewersFlow qualification "
    "remains passive, outstanding and unwaived. If unrelated normal exact-byte BMDSFIX1 evidence naturally selects "
    "DeepSewersFlow, ingest it against the existing gate. Do not implement a universal availability override until "
    "the remaining Phase C3 external-moon obligations are resolved."
)

FINDING = (
    "S1.42AK-BMGHDIAG3 completed its bounded Black Mesa x Greenhouse diagnostic contract using exact published/indexed "
    "profile SHA-256 7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace and diagnostic DLL "
    "SHA-256 d40966c23ac5eb17249d18be7e544a2a0e8ede52c9235abaac475d2372aa1352, directly over accepted S1.42AK. "
    "Ingested evidence at RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/ has raw LogOutput.log SHA-256 "
    "e30858fcebce0fc51f092170b50bd439290cf4752bf0917ae28d66e29a37a9f8. The diagnostic armed without invalidating "
    "refusal, deterministically selected Black Mesa Greenhouse / GreenhouseFlow from the normalized 31-flow viable "
    "pool at rarity 100, completed generation, reported TOPOLOGY_OK for entrance IDs 0,1,2,3 with four opposite-side "
    "pairs, and the second run recorded direct player traversal of all four IDs in both directions with final full "
    "coverage. The user independently reported successful visual/player use of the main entrance and all three fire "
    "exits in both directions in run 2, with no severe clipping, inaccessible required entrance geometry, or severe "
    "persistent routing/NavMesh problem observed. RuntimeNavMeshBuilder emitted Error-severity source-mesh read/"
    "validation messages during Greenhouse generation; these are retained as a non-blocking observation because "
    "generation completed, all required entrances were traversed, and no correlated severe/persistent target routing "
    "failure was observed. This is a Black Mesa x Greenhouse runtime-compatibility PASS only. BMGHDIAG3 remains "
    "DIAGNOSTIC ONLY / NEVER ACCEPT. Accepted S1.42AK remains unchanged. S1.42AK-BMDSFIX1 remains the separate active "
    "gameplay candidate / not accepted, and its regular Black Mesa x DeepSewersFlow gate remains passive, outstanding "
    "and unwaived."
)

ANALYSIS_CONTRACT = (
    "Treat Current/199_S1.42AK_BMGHDIAG3_RUNTIME_COMPATIBILITY_PASS.md plus exact evidence "
    "RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/ as pair-specific Phase-C compatibility proof for Black Mesa x "
    "Greenhouse. Never promote BMGHDIAG3 to gameplay, never accept BMDSFIX1 from this evidence, and never use the "
    "Greenhouse result to satisfy or waive the regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow gate. Preserve "
    "the Phase-B3 matrix as its historical availability/effective-weight snapshot rather than rewriting it from this "
    "compatibility run. RuntimeNavMeshBuilder Error-severity source-mesh messages remain an explicit non-blocking "
    "observation unless stronger target-correlated user-facing evidence emerges. Continue Phase C3 narrowly and keep "
    "the separate Black Mesa/Pikmin routing-recovery scope closed."
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    if start not in text:
        raise RuntimeError(f"start marker missing: {start}")
    if end not in text:
        raise RuntimeError(f"end marker missing: {end}")
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement.rstrip() + "\n\n" + text[b:]


def replace_marker(text: str) -> str:
    if NEW_MARKER in text:
        return text
    if OLD_MARKER not in text:
        raise RuntimeError("live-state marker precondition missing")
    return text.replace(OLD_MARKER, NEW_MARKER, 1)


state = load_json(STATE_PATH)
buildspec = load_json(BUILDSPEC_PATH)
index = load_json(INDEX_PATH)

assert state["accepted_baseline"]["build_id"] == ACCEPTED
assert state["accepted_baseline"]["sha256"] == "b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee"
assert state["active_candidate"]["build_id"] == BMDS
assert state["active_candidate"]["status"] == "ACTIVE_RUNTIME_CANDIDATE_NOT_ACCEPTED"
assert state["active_candidate"]["sha256"] == BMDS_SHA
assert state["runtime_test_outstanding"] is True
assert state["controllers"]["runtime_active_build"] == BMG
assert ACTIVE_PATH.read_text(encoding="utf-8").strip() == BMG
assert buildspec["enabled"] is False
assert buildspec["base_sha256"] == BMDS_SHA
assert index["build_id"] == BMG
assert index["ingested_utc"] == "20260928T162539Z"
log_meta = [x for x in index["files"] if x.get("name") == "LogOutput.log"]
assert len(log_meta) == 1
assert log_meta[0]["sha256"] == LOG_SHA
assert log_meta[0]["size"] == 2534060
assert index["analysis"][0]["stats"]["line_count"] == 25795
assert sha256(LOG_PATH) == LOG_SHA

log_text = LOG_PATH.read_text(encoding="utf-8", errors="replace")
required_markers = [
    "[BMGHDIAG3] ARMED",
    "[BMGHDIAG3] SELECTED Black Mesa Greenhouse / GreenhouseFlow; normalized rarity=100; pool=31->1",
    "[BMGHDIAG3] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4",
    "id0=outside>inside:1,inside>outside:1;id1=outside>inside:1,inside>outside:1;id2=outside>inside:1,inside>outside:1;id3=outside>inside:1,inside>outside:1",
]
for marker in required_markers:
    assert marker in log_text, marker
assert log_text.count("[BMGHDIAG3] SELECTED Black Mesa Greenhouse / GreenhouseFlow") >= 2
assert "[BMGHDIAG3] REFUSED" not in log_text
assert "TOPOLOGY_INCONCLUSIVE" not in log_text
for entrance_id in range(4):
    assert f"[BMGHDIAG3] TRAVERSED id={entrance_id} sourceSide=outside targetSide=inside" in log_text
    assert f"[BMGHDIAG3] TRAVERSED id={entrance_id} sourceSide=inside targetSide=outside" in log_text

marker_json = load_json(ROOT / EVIDENCE_REL / "analysis/raw__LogOutput/MARKERS.json")
assert marker_json["work_state_no_task"]["count"] == 0
assert marker_json["leader_null_following"]["count"] == 0
assert marker_json["compatibility_fixes_error"]["count"] == 0
assert marker_json["fatal_marker"]["count"] == 0
navmesh_error_lines = [line for line in log_text.splitlines() if "RuntimeNavMeshBuilder" in line and "[Error" in line]
assert navmesh_error_lines, "expected RuntimeNavMeshBuilder Error-severity observation"

decision = f"""# S1.42AK-BMGHDIAG3 Black Mesa x Greenhouse Runtime Compatibility Pass

**Date:** 2026-09-28  
**Status:** RUNTIME COMPATIBILITY PASS / DIAGNOSTIC ONLY / NEVER ACCEPT  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged / not accepted / passive Deep Sewers gate outstanding and unwaived  
**Diagnostic:** S1.42AK-BMGHDIAG3 — completed diagnostic evidence / never accept  
**Diagnostic profile:** `Profiles/LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic.r2z`  
**Diagnostic profile SHA-256:** `{PROFILE_SHA}`  
**Diagnostic DLL SHA-256:** `{DLL_SHA}`  
**Direct diagnostic base:** exact accepted S1.42AK / `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
**Runtime evidence:** `{EVIDENCE_REL}`  
**Raw LogOutput.log SHA-256:** `{LOG_SHA}`

## Decision

The ingested exact BMGHDIAG3 evidence plus the user's bounded gameplay observation establishes a **Black Mesa x Greenhouse runtime-compatibility PASS** for the diagnostic contract in `Current/198_S1.42AK_BMGHDIAG3_RUNTIME_ACTIVATION.md`.

This decision is pair-specific compatibility evidence. It does not promote a build and does not rewrite the Phase-B3 availability matrix.

## Machine evidence

The exact persisted log establishes:

- `[BMGHDIAG3] ARMED` with no invalidating BMGHDIAG3 startup refusal;
- exact deterministic selection of `Black Mesa Greenhouse / GreenhouseFlow` at normalized rarity `100` with `pool=31->1`;
- at least two exact Greenhouse selections in the captured session;
- completed generation after each relevant selection;
- `[BMGHDIAG3] TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4`;
- direct native player traversal markers for entrance IDs `0`, `1`, `2` and `3` in both directions;
- final run-2 coverage `id0=outside>inside:1,inside>outside:1;id1=outside>inside:1,inside>outside:1;id2=outside>inside:1,inside>outside:1;id3=outside>inside:1,inside>outside:1`;
- no `[BMGHDIAG3] REFUSED`;
- no `TOPOLOGY_INCONCLUSIVE`;
- analyzer counts `Work state with no task assigned! = 0`, `Leader is null when following = 0`, `[Error  :S1.39 Compatibility Fixes] = 0`, and fatal marker `= 0`.

The runtime log contains `{len(navmesh_error_lines)}` Error-severity line(s) naming `RuntimeNavMeshBuilder`. These source-mesh read/validation messages are preserved as an explicit observation rather than hidden or reclassified.

## User-reported gameplay evidence

The following is manual gameplay evidence supplied by the user and is intentionally distinguished from log-derived facts.

Two Greenhouse runs were performed on Black Mesa. In run 1, the Greenhouse spawned, the main entrance was used in both directions, and one fire exit was used in both directions. In run 2, Greenhouse spawned again; the main entrance and all three fire exits were each exercised inward and outward. The user reported no severe persistent routing/NavMesh problem, no clipping problem, and no inaccessible required entrance geometry.

This manual observation supplies the visual/player-geometry portion that native teleport success alone must not be overclaimed to prove.

## RuntimeNavMeshBuilder observation

`RuntimeNavMeshBuilder` emitted Error-severity source-mesh read/validation messages during Greenhouse generation. Under `Knowledge/MONITOR_ONLY_ERRORS.md`, severity alone is not an automatic blocker. In this evidence the dungeon subsequently completed generation, topology resolved, every required entrance ID was directly traversed in both directions, and the user observed no severe persistent routing/NavMesh symptom or inaccessible required geometry.

The messages are therefore **non-blocking for this bounded Greenhouse compatibility gate**, while remaining documented evidence that may be revisited if stronger target-correlated symptoms appear later.

## Qualification boundary

- S1.42AK remains the sole accepted gameplay baseline.
- S1.42AK-BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT** and is not a gameplay candidate.
- S1.42AK-BMDSFIX1 remains the separate active gameplay candidate and remains **NOT ACCEPTED**.
- The regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains passive, outstanding and unwaived.
- This Greenhouse PASS neither satisfies nor weakens the Deep Sewers gate.
- The Phase-B3 30x53 availability/effective-weight matrix remains an unchanged historical snapshot; this decision adds Phase-C pair-specific compatibility evidence.
- The separate Black Mesa/Pikmin routing-recovery scope remains closed.
- No profile, DLL, package, config or gameplay bytes are changed by this reconciliation.

## Runtime/evidence routing

The bounded BMGHDIAG3 diagnostic is complete, so it is no longer the runtime/evidence target. Routing returns to exact `S1.42AK-BMDSFIX1`, matching the preserved gameplay-candidate controller lineage. This pointer reset does not release a dedicated Deep Sewers reroll and does not accept BMDSFIX1.

`BuildSpecs/current.json` remains disabled and pinned to exact BMDSFIX1 bytes.

## Next project action

{NEXT_ACTION}
"""
DECISION_PATH.write_text(decision, encoding="utf-8")

scope = state["selected_scope"]
phase_c = scope["phase_c"]
diag = scope["diagnostic_revision"]
state["runtime_test_outstanding"] = True
scope["status"] = SCOPE_STATUS
scope["finding"] = FINDING
scope["analysis_contract"] = ANALYSIS_CONTRACT
scope["next_action"] = NEXT_ACTION
phase_c["status"] = "C3_IN_PROGRESS_BLACK_MESA_GREENHOUSE_RUNTIME_COMPATIBILITY_PASS"
phase_c["phase_c3f18_runtime_decision"] = DECISION_REL
phase_c["phase_c3f18_runtime_evidence"] = EVIDENCE_REL
phase_c["phase_c3f18_runtime_log_sha256"] = LOG_SHA
phase_c["black_mesa_greenhouse_status"] = GREENHOUSE_STATUS
phase_c["black_mesa_greenhouse_runtime_decision"] = DECISION_REL
phase_c["black_mesa_greenhouse_runtime_evidence"] = EVIDENCE_REL
phase_c["black_mesa_greenhouse_runtime_log_sha256"] = LOG_SHA
phase_c["black_mesa_greenhouse_runtime_finding"] = (
    "Exact BMGHDIAG3 diagnostic armed and selected Greenhouse at normalized rarity 100 from Black Mesa's 31-flow viable "
    "pool, generation completed, topology resolved IDs 0..3, and run 2 recorded bidirectional direct traversal for all "
    "four IDs. User observation confirms the exercised entrance geometry was accessible without severe clipping or "
    "persistent routing/NavMesh failure. RuntimeNavMeshBuilder Error-severity source-mesh messages are retained as a "
    "non-blocking observation for this gate."
)
phase_c["bmgdiag3_runtime_status"] = "RUNTIME_COMPATIBILITY_PASS_DIAGNOSTIC_ONLY_NEVER_ACCEPT"
phase_c["bmgdiag3_runtime_decision"] = DECISION_REL
scope["bmgdiag3_review_runtime_armed"] = False
scope["bmgdiag3_runtime_activation_status"] = "COMPLETED_DIAGNOSTIC_RUNTIME_COMPATIBILITY_PASS_NEVER_ACCEPT_NOT_ACTIVE"
scope["diagnostic_runtime_finding"] = DECISION_REL
diag["status"] = "PUBLISHED_DIAGNOSTIC_RUNTIME_EVIDENCE_INGESTED_COMPATIBILITY_PASS_NOT_ACCEPTED"
diag["runtime_armed"] = False
diag["runtime_validation_status"] = "RUNTIME_COMPATIBILITY_PASS_NEVER_ACCEPT"
diag["runtime_result"] = "PASS_BLACK_MESA_GREENHOUSE_RUNTIME_COMPATIBILITY"
diag["runtime_evidence"] = EVIDENCE_REL
diag["runtime_index"] = INDEX_REL
diag["runtime_log_sha256"] = LOG_SHA
diag["runtime_decision"] = DECISION_REL
diag["manual_gameplay_evidence"] = (
    "User performed two Black Mesa x Greenhouse runs; run 2 exercised main entrance and all three fire exits in both "
    "directions with no severe clipping, inaccessible required entrance geometry, or severe persistent routing/NavMesh problem observed."
)
state["next_action"] = NEXT_ACTION
state["controllers"]["runtime_active_build"] = BMDS
write_json(STATE_PATH, state)
ACTIVE_PATH.write_text(BMDS + "\n", encoding="utf-8")

integrity = load_json(INTEGRITY_JSON)
pending = integrity["pending_profiles"]
matches = [x for x in pending if x.get("build_id") == BMG]
assert len(matches) == 1
entry = matches[0]
integrity["pending_profiles"] = [x for x in pending if x.get("build_id") != BMG]
entry["role"] = "RUNTIME_DIAGNOSTIC_PASS_NOT_GAMEPLAY_BASE"
entry.pop("runtime_evidence_required", None)
entry.pop("partial_runtime_evidence_present", None)
entry["decision"] = DECISION_REL
entry["runtime_index"] = INDEX_REL
entry["runtime_log_sha256"] = LOG_SHA
entry["runtime_result"] = "PASS_BLACK_MESA_GREENHOUSE_RUNTIME_COMPATIBILITY"
entry["note"] = (
    "Completed exact BMGHDIAG3 Black Mesa x Greenhouse diagnostic evidence. Diagnostic only / NEVER ACCEPT. "
    "Generation/topology and bidirectional IDs 0..3 traversal passed; user observation found no severe clipping, "
    "inaccessible required entrance geometry, or severe persistent routing/NavMesh issue. Does not accept BMDSFIX1 or waive its passive Deep Sewers gate."
)
assert not any(x.get("build_id") == BMG for x in integrity["profiles"])
integrity["profiles"].append(entry)
obs = integrity.get("verified_repository_api_observations", [])
obs = [x for x in obs if not str(x).startswith("S1.42AK-BMGHDIAG3 exact published/indexed profile")]
obs.append(
    "S1.42AK-BMGHDIAG3 exact profile SHA-256 7ab3dae8f5b215219d81bba37645853be0f253ac981118d176f5f9cfa28e7ace "
    "has completed diagnostic runtime evidence at RuntimeEvidence/S1.42AK-BMGHDIAG3/20260928T162539Z/ with raw log "
    "SHA-256 e30858fcebce0fc51f092170b50bd439290cf4752bf0917ae28d66e29a37a9f8. Black Mesa x Greenhouse passed the bounded "
    "runtime-compatibility gate; BMGHDIAG3 remains NEVER ACCEPT and is no longer runtime-active."
)
integrity["verified_repository_api_observations"] = obs
integrity["last_validated"] = "2026-09-28"
write_json(INTEGRITY_JSON, integrity)

text = replace_marker(INTEGRITY_MD.read_text(encoding="utf-8"))
replacement = f"""## Completed diagnostic evidence: S1.42AK-BMGHDIAG3

Profile: `Profiles/LC V1 S1.42AK-BMGHDIAG3 Black Mesa Greenhouse Diagnostic.r2z`  
SHA-256: `{PROFILE_SHA}`  
Diagnostic DLL SHA-256: `{DLL_SHA}`  
Readable snapshot: `ProfileSources/S1.42AK-BMGHDIAG3/`  
Runtime evidence: `{EVIDENCE_REL}`  
Runtime log SHA-256: `{LOG_SHA}`  
Decision: `{DECISION_REL}`

The exact diagnostic passed the bounded Black Mesa x Greenhouse runtime-compatibility contract: exact selection at normalized rarity 100, completed generation, topology IDs 0..3, and direct bidirectional traversal of all four IDs in run 2. The user's manual observation additionally reported accessible required entrance geometry without severe clipping or persistent routing/NavMesh failure. RuntimeNavMeshBuilder Error-severity source-mesh messages remain documented as a non-blocking observation for this gate. BMGHDIAG3 is completed diagnostic evidence only / NEVER ACCEPT.

## Pending / deferred unaccepted profiles

- **S1.42AJ** — deferred full-normal gate / retained exact balanced parent, not active.
- **S1.42AK-BMDSFIX1** — active gameplay candidate directly over accepted S1.42AK; profile SHA-256 `{BMDS_SHA}`; its regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding/unwaived; not accepted.
- **S1.42AK-BMDSFIX1-DIAG1** — preserved preloader-blocked diagnostic parent; profile SHA-256 `31c24a3752aefe040b74c5dc2c3b7f677c17068a91f8c8e2893ace615050b78e`; must not be rerun and is not the active runtime/evidence target.
- **S1.42AK-BMDSFIX1-DIAG1PATH1** — completed supporting diagnostic evidence using short identity `LC V1 S1.42AK-D1P1`; profile SHA-256 `0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6`; not runtime-active and never a gameplay base or acceptance candidate.

BMDSFIX1 exact reviewed bytes remain the active gameplay candidate and are unchanged. Runtime/evidence routing has returned to `S1.42AK-BMDSFIX1` after completion of the Greenhouse diagnostic, but no dedicated Deep Sewers reroll is released. `BuildSpecs/current.json` remains disabled. BMGHDIAG3 is no longer runtime-active and remains NEVER ACCEPT; its completed Greenhouse PASS does not accept BMDSFIX1 or waive the separate Deep Sewers target gate.
"""
text = replace_between(text, "## Pending / deferred unaccepted profiles", "## Completed diagnostic evidence: S1.42AI-DIAG1R3", replacement)
INTEGRITY_MD.write_text(text, encoding="utf-8")

text = replace_marker(MAP_MD.read_text(encoding="utf-8"))
anchor = f"""## Current lifecycle anchor

Accepted gameplay baseline: **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**. Active gameplay candidate / latest built gameplay artifact: **S1.42AK-BMDSFIX1 — not accepted**.

The selected **Universal Interior Viability / Equal Availability** scope remains in Phase C3. The fixed Phase-B3 30x53 availability/effective-weight matrix remains an unchanged historical snapshot at 662 `VIABLE_EQUAL_100`, 14 `AUTHOR_OR_OWNER_HARD_BLOCK`, 0 `CONFIG_GAP`, 0 `KNOWN_TECHNICAL_RESTRICTION`, and 914 `NOT_YET_PROVEN`; pair-specific Phase-C runtime compatibility evidence does not rewrite those historical classifications.

Exact `S1.42AK-BMGHDIAG3` evidence at `{EVIDENCE_REL}` / raw log SHA-256 `{LOG_SHA}` now establishes a **Black Mesa x Greenhouse runtime-compatibility PASS**. The diagnostic armed, selected `GreenhouseFlow` at normalized rarity 100 from the 31-flow Black Mesa viable pool, completed generation, reported topology IDs 0..3 with four opposite-side pairs, and run 2 recorded direct traversal of all four entrance IDs in both directions. The user's gameplay observation confirms accessible main/fire-exit geometry without severe clipping or a severe persistent routing/NavMesh issue. RuntimeNavMeshBuilder Error-severity source-mesh messages remain a documented non-blocking observation for this bounded gate. Decision: `{DECISION_REL}`.

BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT** and is no longer runtime-active. Runtime/evidence routing has returned to exact `S1.42AK-BMDSFIX1`. BMDSFIX1 remains the separate active gameplay candidate / **NOT ACCEPTED**; its regular exact-byte Black Mesa x `DeepSewersFlow` qualification remains passive, outstanding and unwaived, with no dedicated reroll released. `BuildSpecs/current.json` remains disabled. The global runtime-test flag remains outstanding only for the passive/unwaived BMDSFIX1 Deep Sewers gameplay gate; the completed BMGHDIAG3 diagnostic itself is no longer outstanding and no dedicated reroll is released.

Exact next action: continue the repository-native Phase C3 External target-moon semantics/topology analysis from the completed Greenhouse pair proof; do not authorize a universal availability override until the remaining external-moon obligations are resolved.
"""
text = replace_between(text, "## Current lifecycle anchor", "## Authority rule", anchor)
MAP_MD.write_text(text, encoding="utf-8")

text = replace_marker(ROADMAP.read_text(encoding="utf-8"))
road = f"""## Current position

Accepted gameplay baseline remains **S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**, SHA-256 `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`.

Latest built artifact and active gameplay candidate remains **S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix**, SHA-256 `{BMDS_SHA}`. It is not accepted and its exact regular Black Mesa x `DeepSewersFlow` gate remains passive/outstanding/unwaived.

The bounded `S1.42AK-BMGHDIAG3` Black Mesa x Greenhouse diagnostic is complete. Exact evidence `{EVIDENCE_REL}` / raw log SHA-256 `{LOG_SHA}` establishes the pair-specific runtime-compatibility PASS recorded in `{DECISION_REL}`. BMGHDIAG3 remains diagnostic only / NEVER ACCEPT and is no longer the runtime/evidence target. `RuntimeInbox/ACTIVE_BUILD.txt` has returned to exact BMDSFIX1; this routing reset does not release a dedicated Deep Sewers test and does not accept the candidate. `BuildSpecs/current.json` remains disabled.

## Selected scope

**Universal Interior Viability / Equal Availability — SELECTED / PHASE C3 IN PROGRESS / BLACK MESA x GREENHOUSE RUNTIME COMPATIBILITY PASS / BMDSFIX1 GAMEPLAY QUALIFICATION PASSIVE OUTSTANDING.**

The authoritative 30x53 B3 matrix and accepted S1.42AB post-viability normalizer remain unchanged. The Greenhouse decision adds pair-specific Phase-C compatibility evidence; it does not retroactively rewrite the B3 availability matrix and does not authorize a universal override.

Plan: `BuildSpecs/UNIVERSAL_INTERIOR_VIABILITY_EQUAL_AVAILABILITY_PLAN.md`.

## Exact next selected-scope action

{NEXT_ACTION}
"""
text = replace_between(text, "## Current position", "## Completed LC Office scrap scope", road)
text = text.replace("- Black Mesa x Greenhouse BMGHDIAG3 runtime evidence and decision (currently selected diagnostic gate, not a gameplay acceptance path).\n", "")
ROADMAP.write_text(text, encoding="utf-8")

text = replace_marker(LIFECYCLE.read_text(encoding="utf-8"))
new_runtime_section = f"""BMGHDIAG3 is therefore canonically indexed and exact-head CI-green at the pre-runtime checkpoint. That activation state is now superseded by the completed runtime decision below.

## BMGHDIAG3 Black Mesa x Greenhouse runtime compatibility — PASS / diagnostic complete

`{DECISION_REL}` records the completed bounded runtime decision. Exact evidence is `{EVIDENCE_REL}` with raw log SHA-256 `{LOG_SHA}`.

The exact BMGHDIAG3 diagnostic armed without invalidating refusal, selected `Black Mesa Greenhouse / GreenhouseFlow` at normalized rarity 100 from the 31-flow viable pool, completed generation, reported `TOPOLOGY_OK ids=0,1,2,3 uniqueOppositePairs=4`, and the second run directly traversed all four entrance IDs in both directions. Final coverage is complete for IDs 0..3. The user independently reported successful visual/player use of the main entrance and all three fire exits in both directions in run 2, with no severe clipping, inaccessible required entrance geometry, or severe persistent routing/NavMesh problem observed.

RuntimeNavMeshBuilder Error-severity source-mesh read/validation messages occurred during Greenhouse generation. They remain explicit non-blocking observations for this bounded gate because generation completed, every required entrance ID was traversed in both directions, and no correlated severe/persistent target routing symptom was observed. Error severity alone is not treated as automatic rejection under the current triage authority.

This is a **Black Mesa x Greenhouse runtime-compatibility PASS only**. BMGHDIAG3 remains **DIAGNOSTIC ONLY / NEVER ACCEPT** and cannot become a gameplay baseline or candidate. Accepted S1.42AK remains unchanged. S1.42AK-BMDSFIX1 remains the separate active gameplay candidate / not accepted, and its regular exact-byte Black Mesa x `DeepSewersFlow` gate remains passive, outstanding and unwaived.

The Phase-B3 matrix remains unchanged as its historical availability/effective-weight snapshot. This decision supplies Phase-C pair-specific compatibility proof instead.

Runtime/evidence routing has returned to exact `S1.42AK-BMDSFIX1`. No new runtime test is currently released; in particular, there is no BMGHDIAG3 rerun and no dedicated BMDSFIX1 Deep Sewers reroll.
"""
text = replace_between(text, "BMGHDIAG3 is therefore canonically indexed and exact-head CI-green.", "## BMDSFIX1 runtime — regular non-target evidence plus DIAG1PATH1 supporting PASS", new_runtime_section)
text = text.replace(
    "The regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` gameplay gate remains outstanding and unwaived. Runtime/evidence routing is exact `S1.42AK-BMDSFIX1`; the diagnostic selector is not allowed in the qualification run. No further non-target control is required solely for BMDSFIX1 qualification. Black Mesa x Greenhouse remains separate and `NOT_YET_PROVEN`.",
    "The regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` gameplay gate remains outstanding and unwaived. Runtime/evidence routing is exact `S1.42AK-BMDSFIX1`; the diagnostic selector is not allowed in any eventual qualification evidence. No further non-target control is required solely for BMDSFIX1 qualification. Black Mesa x Greenhouse is separately proven runtime-compatible by the completed BMGHDIAG3 diagnostic and does not satisfy this Deep Sewers gate."
)
tail = f"""## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact / active gameplay candidate: **S1.42AK-BMDSFIX1 — not accepted**.
- Runtime/evidence pointer: **S1.42AK-BMDSFIX1**.
- BMGHDIAG3: **Black Mesa x Greenhouse runtime-compatibility PASS / evidence ingested / DIAGNOSTIC ONLY / NEVER ACCEPT / not runtime-active**.
- Black Mesa x Greenhouse Phase-C status: **pair-specific compatibility proven**; the Phase-B3 availability matrix remains unchanged as its historical snapshot.
- Runtime test outstanding: **yes — solely the passive/unwaived regular BMDSFIX1 Black Mesa x `DeepSewersFlow` gameplay qualification**. The BMGHDIAG3 diagnostic is complete; no BMGHDIAG3 rerun and no dedicated BMDSFIX1 Deep Sewers reroll is released.
- BMDSFIX1 regular Black Mesa x `DeepSewersFlow` gameplay qualification: **passive / outstanding / unwaived**; unrelated natural exact-byte target evidence may still satisfy the existing gate if later encountered and ingested.
- DIAG1PATH1: **supporting Deep Sewers diagnostic PASS / NEVER ACCEPT / not runtime-active**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 base bytes.
- The separate Black Mesa/Pikmin routing-recovery scope remains closed.

## Exact next project action

{NEXT_ACTION}

No Gale replacement/import command or runtime-log uploader is released by this reconciliation because the only outstanding runtime gate is the passive BMDSFIX1 Deep Sewers qualification and no dedicated run is currently released.

## Permanent Gale workflow

The canonical Gale helper remains `RuntimeTools/ReplaceActiveGaleProfileV24.ps1`. The accepted-baseline direct-diagnostic resolver support introduced for BMGHDIAG3 remains valid infrastructure, but BMGHDIAG3 is no longer the active target. `RuntimeInbox/ACTIVE_BUILD.txt` now points back to exact `S1.42AK-BMDSFIX1` for known-build runtime/evidence routing. This pointer does not accept BMDSFIX1 and does not release its passive Deep Sewers gate.
"""
if "## Live execution state" not in text:
    raise RuntimeError("lifecycle live-state heading missing")
text = text[:text.index("## Live execution state")] + tail
LIFECYCLE.write_text(text, encoding="utf-8")

print("Reconciled BMGHDIAG3 runtime compatibility PASS and reset runtime/evidence routing.")
