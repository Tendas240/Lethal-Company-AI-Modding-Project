#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "Current/CURRENT_STATE.json"
LIFECYCLE = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
MAP = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
ACTIVE = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
BUILDSPEC = ROOT / "BuildSpecs/current.json"
RECORD = ROOT / "Current/186_S1.42AK_BMDSFIX1_DIAG1PATH1_RUNTIME_SUPPORTING_PASS.md"
EVIDENCE = ROOT / "RuntimeEvidence/S1.42AK-BMDSFIX1-DIAG1PATH1/20260925T085104Z"
LOG = EVIDENCE / "raw/LogOutput.log"
INDEX = EVIDENCE / "INDEX.json"

EXPECTED_GAMEPLAY_PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
EXPECTED_GAMEPLAY_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
EXPECTED_PATH1_SHA = "0d4fc0b2031099617a43770b29ab1908a2be18a262df70a3322904f458cff5c6"
EXPECTED_DIAG_DLL_SHA = "3b9954b21fc2f1214e73b4021c8ab278f71420583e0e2e9f478f981fc64b20e1"
EXPECTED_LOG_SHA = "ec7631dc6baa3ef6cff502767d56356fe62943b362271f45add8807381a63ae4"
EVIDENCE_REL = "RuntimeEvidence/S1.42AK-BMDSFIX1-DIAG1PATH1/20260925T085104Z/"
RECORD_REL = "Current/186_S1.42AK_BMDSFIX1_DIAG1PATH1_RUNTIME_SUPPORTING_PASS.md"


def require(cond: bool, message: str) -> None:
    if not cond:
        raise SystemExit(message)


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = text.find(start_marker)
    require(start >= 0, f"missing start marker: {start_marker}")
    end = text.find(end_marker, start)
    require(end >= 0, f"missing end marker: {end_marker}")
    return text[:start] + replacement.rstrip() + "\n\n" + text[end:]


state = json.loads(STATE.read_text(encoding="utf-8"))
require(state["accepted_baseline"]["build_id"] == "S1.42AK", "accepted baseline drift")
require(state["active_candidate"]["build_id"] == "S1.42AK-BMDSFIX1", "active candidate drift")
require(state["active_candidate"]["sha256"] == EXPECTED_GAMEPLAY_PROFILE_SHA, "gameplay profile SHA drift")
require(state["runtime_test_outstanding"] is True, "runtime gate no longer outstanding")
require(state["controllers"]["runtime_active_build"] == "S1.42AK-BMDSFIX1-DIAG1PATH1", "runtime controller drift")
require(ACTIVE.read_text(encoding="utf-8").strip() == "S1.42AK-BMDSFIX1-DIAG1PATH1", "ACTIVE_BUILD drift")

scope = state["selected_scope"]
require(scope["status"] == "PHASE_C3F18_DIAG1PATH1_RUNTIME_ACTIVE_SUPPORTING_EVIDENCE_OUTSTANDING", "unexpected source lifecycle status")
diag = scope["diagnostic_revision"]
require(diag["build_id"] == "S1.42AK-BMDSFIX1-DIAG1PATH1", "diagnostic revision drift")
require(diag["status"] == "PUBLISHED_ACTIVE_DIAGNOSTIC_RUNTIME_TARGET_NOT_ACCEPTED", "diagnostic status drift")
require(diag["classification"] == "DIAGNOSTIC_SUPPORT_ONLY_NEVER_ACCEPT", "diagnostic classification drift")
require(diag["profile_sha256"] == EXPECTED_PATH1_SHA, "PATH1 profile SHA drift")
require(diag["diagnostic_dll_sha256"] == EXPECTED_DIAG_DLL_SHA, "diagnostic DLL SHA drift")
require(diag["bmdsfix1_dll_sha256"] == EXPECTED_GAMEPLAY_DLL_SHA, "BMDSFIX1 DLL SHA drift")
require(diag["runtime_armed"] is True, "PATH1 is not runtime armed")

buildspec = json.loads(BUILDSPEC.read_text(encoding="utf-8"))
require(buildspec["enabled"] is False, "BuildSpecs/current.json unexpectedly enabled")
require(buildspec["base_sha256"] == EXPECTED_GAMEPLAY_PROFILE_SHA, "BuildSpecs gameplay base SHA drift")
require(LOG.is_file() and INDEX.is_file(), "expected ingested PATH1 evidence missing")
log_bytes = LOG.read_bytes()
actual_log_sha = hashlib.sha256(log_bytes).hexdigest()
require(actual_log_sha == EXPECTED_LOG_SHA, f"runtime log SHA drift: {actual_log_sha}")
idx = json.loads(INDEX.read_text(encoding="utf-8"))
require(idx["build_id"] == "S1.42AK-BMDSFIX1-DIAG1PATH1", "runtime index build attribution drift")
require(any(f.get("sha256") == EXPECTED_LOG_SHA for f in idx.get("files", [])), "runtime index log SHA drift")
text = log_bytes.decode("utf-8", errors="replace")

require("[BMDSFIX1-DIAG1] ARMED" in text, "diagnostic ARMED marker missing")
require("[BMDSFIX1-DIAG1] REFUSED TO ARM" not in text, "diagnostic refused to arm")
require("[BMDSFIX1-DIAG1] REFUSED selection" not in text, "diagnostic refused target selection")
require("[BMDSFIX1-DIAG1] SELECTED Black Mesa / DeepSewersFlow; normalized rarity=100; pool=31->1" in text, "deterministic DeepSewersFlow selection missing")
require("[BMDSFIX1] ARMED" in text, "BMDSFIX1 ARMED marker missing")
require("[BMDSFIX1] REFUSED TO ARM" not in text, "BMDSFIX1 refused to arm")
require("[BMDSFIX1] APPLIED Black Mesa / DeepSewersFlow multiplier=4.875->1" in text, "BMDSFIX1 target application missing")
require("Final length multiplier: 1 (Interior #29" in text, "final multiplier 1 proof missing")
require("Dungeon has finished generating on this client after multiple frames" in text, "dungeon completion missing")
require("Players finished generating the new floor" in text, "player generation completion missing")
require("Player exited ship" in text, "post-generation player activity missing")
require("Ship returned to orbit" in text, "completed played session / return-to-orbit evidence missing")
require("[Fatal" not in text, "fatal marker present in runtime log")
require(not RECORD.exists(), "supporting-pass decision record already exists")

scope["status"] = "PHASE_C3F18_DIAG1PATH1_SUPPORTING_PASS_BMDSFIX1_EXACT_TARGET_QUALIFICATION_OUTSTANDING"
scope["finding"] = (
    "Exact S1.42AK-BMDSFIX1-DIAG1PATH1 supporting runtime evidence is ingested at " + EVIDENCE_REL +
    " with raw LogOutput.log SHA-256 " + EXPECTED_LOG_SHA + ". The short-name diagnostic armed without refusal, deterministically reduced the Black Mesa viable pool from 31 to DeepSewersFlow only at normalized rarity 100, and the unchanged BMDSFIX1 DLL armed and applied its pair-scoped multiplier clamp 4.875->1. Dungeon generation then completed, Players finished generating the new floor, normal player activity continued, and the session later returned to orbit. The user independently reported no Entering-the-atmosphere problem and no noticeable gameplay issue. This is a supporting diagnostic PASS only: DIAG1PATH1 remains NEVER ACCEPT and cannot qualify or accept S1.42AK-BMDSFIX1. The regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow gameplay qualification remains outstanding and unwaived."
)
scope["analysis_contract"] = (
    "Treat the DIAG1PATH1 run as successful supporting evidence that deterministic Black Mesa x DeepSewersFlow selection plus the unchanged BMDSFIX1 clamp can complete generation and reach normal gameplay with multiplier 1. Preserve exact PATH1 profile SHA-256 " + EXPECTED_PATH1_SHA +
    " and exact BMDSFIX1 gameplay profile SHA-256 " + EXPECTED_GAMEPLAY_PROFILE_SHA + ". Do not accept DIAG1PATH1 and do not infer BMDSFIX1 acceptance from diagnostic-overlay evidence. Runtime/evidence routing must now return to exact S1.42AK-BMDSFIX1 before the regular gameplay qualification. Preserve the already-ingested Substation non-target control; the remaining qualification is exact BMDSFIX1 Black Mesa x DeepSewersFlow with ARMED, APPLIED ->1, completed generation, normal landed gameplay, no persistent atmosphere/retry failure, and no new severe target-attributable regression. Keep Black Mesa x Greenhouse/BMGHDIAG separate."
)
next_action = (
    "After this supporting-pass decision and runtime-routing reset are integrated and exact-head CI validated, import exact S1.42AK-BMDSFIX1 through the canonical repository-driven Gale v2.4 launcher and obtain the remaining regular exact-byte Black Mesa x DeepSewersFlow gameplay qualification. The diagnostic selector must not be present in that qualification. Preserve the existing exact-byte Substation non-target control; BMDSFIX1 remains not accepted until the target flow itself is observed with [BMDSFIX1] ARMED, APPLIED ...->1, completed generation and normal landed gameplay without the prior persistent Entering-the-atmosphere/retry failure or a new severe target-attributable regression."
)
scope["next_action"] = next_action
state["next_action"] = next_action

phase_c = scope["phase_c"]
phase_c["diag1path1_runtime_decision"] = RECORD_REL
phase_c["diag1path1_runtime_evidence"] = EVIDENCE_REL
phase_c["diag1path1_runtime_log_sha256"] = EXPECTED_LOG_SHA
phase_c["diag1path1_supporting_status"] = "PASS_SUPPORTING_DIAGNOSTIC_NEVER_ACCEPT"
phase_c["bmdsfix1_target_status"] = "OUTSTANDING_EXACT_GAMEPLAY_BLACK_MESA_DEEP_SEWERS"
phase_c["black_mesa_deep_sewers_supporting_finding"] = (
    "DIAG1PATH1 deterministically selected Black Mesa / DeepSewersFlow from a normalized 31-entry viable pool; BMDSFIX1 applied 4.875->1; final length multiplier was 1; dungeon generation and player floor generation completed; post-generation gameplay continued and the session returned to orbit. The user reported no Entering-the-atmosphere problem and no noticeable issue. This supports the mitigation mechanism but does not replace exact BMDSFIX1 gameplay qualification because the diagnostic selector DLL was present."
)

scope["diagnostic_runtime_finding"] = RECORD_REL
scope["diagnostic_supporting_runtime_decision"] = RECORD_REL
scope["diagnostic_supporting_runtime_evidence"] = EVIDENCE_REL

diag["status"] = "PUBLISHED_DIAGNOSTIC_RUNTIME_EVIDENCE_INGESTED_SUPPORTING_PASS_NOT_ACCEPTED"
diag["runtime_armed"] = False
diag["runtime_validation_status"] = "RUNTIME_EVIDENCE_INGESTED_SUPPORTING_PASS_NEVER_ACCEPT_BMDSFIX1_TARGET_GATE_OUTSTANDING"
diag["runtime_evidence"] = EVIDENCE_REL
diag["runtime_index"] = EVIDENCE_REL + "INDEX.json"
diag["runtime_log_sha256"] = EXPECTED_LOG_SHA
diag["runtime_decision"] = RECORD_REL
diag["supporting_result"] = "PASS"
diag["user_observation"] = "No Entering-the-atmosphere problem and no noticeable gameplay issue reported for this bounded run."

state["controllers"]["runtime_active_build"] = "S1.42AK-BMDSFIX1"
ACTIVE.write_text("S1.42AK-BMDSFIX1\n", encoding="utf-8")
STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

record = f'''# S1.42AK-BMDSFIX1-DIAG1PATH1 Runtime Supporting Pass

**Date:** 2026-09-25  
**Status:** SUPPORTING DIAGNOSTIC PASS / NEVER ACCEPT / BMDSFIX1 EXACT GAMEPLAY TARGET GATE OUTSTANDING  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active gameplay candidate:** S1.42AK-BMDSFIX1 — unchanged exact bytes / not accepted  
**Diagnostic:** S1.42AK-BMDSFIX1-DIAG1PATH1 — supporting evidence only / never accept  
**PATH1 profile SHA-256:** `{EXPECTED_PATH1_SHA}`  
**BMDSFIX1 gameplay profile SHA-256:** `{EXPECTED_GAMEPLAY_PROFILE_SHA}`  
**BMDSFIX1 DLL SHA-256:** `{EXPECTED_GAMEPLAY_DLL_SHA}`  
**Runtime evidence:** `{EVIDENCE_REL}`  
**Raw LogOutput.log SHA-256:** `{EXPECTED_LOG_SHA}`

## Decision

The ingested DIAG1PATH1 run is accepted as a **supporting diagnostic PASS** for the Black Mesa x `DeepSewersFlow` mitigation mechanism.

The exact log establishes the required diagnostic chain:

- `[BMDSFIX1-DIAG1] ARMED` appears and no diagnostic arm/selection refusal is present;
- Black Mesa's already-viable normalized pool contains 31 flows at effective rarity 100 and the diagnostic selects `DeepSewersFlow` with `pool=31->1`;
- `[BMDSFIX1] ARMED` appears without refusal;
- `[BMDSFIX1] APPLIED Black Mesa / DeepSewersFlow multiplier=4.875->1` appears;
- ButteRyBalance reports final length multiplier `1`;
- `Dungeon has finished generating on this client after multiple frames` appears;
- `Players finished generating the new floor` appears;
- normal post-generation player activity follows and the session later logs `Ship returned to orbit`;
- no `[Fatal` marker is present in the raw log.

The user independently reported that the `Entering the atmosphere` problem did not occur and that no gameplay problems were noticed during this bounded run.

DunGen/DunGenPlus still emitted a finite set of placement-failure/retry diagnostics while building Deep Sewers, but those retries resolved into successful generation within the same run. They are therefore not equivalent to the earlier failing 4.875 incident, which lacked a later generation-complete marker in the captured target evidence.

The raw log is not globally error-free. It contains unrelated/known stack noise, including a SoundAPI/HarmonyX `TypeLoadException` reporting error and other mod warnings/exceptions. These did not prevent the target selection, BMDSFIX1 application, dungeon completion or subsequent gameplay, and this decision does not reclassify them as fixed or attribute them to BMDSFIX1.

## Qualification boundary

This PASS is deliberately **supporting diagnostic evidence only**. DIAG1PATH1 contains the deterministic selector DLL and shortened diagnostic profile identity, so it can never be accepted as gameplay and cannot itself accept S1.42AK-BMDSFIX1.

The regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived. The already-ingested exact BMDSFIX1 Black Mesa x Substation run remains the non-target control and need not be repeated solely for that criterion.

Before any regular qualification run, runtime/evidence routing returns to exact `S1.42AK-BMDSFIX1`. No profile, DLL, package, config or gameplay bytes are changed by this reconciliation.

## Preserved boundaries

- S1.42AK remains the sole accepted gameplay baseline;
- S1.42AK-BMDSFIX1 remains the active gameplay candidate / not accepted;
- DIAG1PATH1 remains NEVER ACCEPT;
- the blocked long-name DIAG1 remains historical one-hop provenance and must not be rerun;
- exact PATH1, DIAG1 selector and BMDSFIX1 DLL/profile bytes remain unchanged;
- `BuildSpecs/current.json` remains disabled and pinned to exact BMDSFIX1;
- Black Mesa x Greenhouse/BMGHDIAG remains separate;
- no universal interior override is authorized.

## Next gate

After this decision/routing reset is integrated and exact-head validated, import exact `S1.42AK-BMDSFIX1` and obtain the regular exact-byte Black Mesa x `DeepSewersFlow` gameplay qualification without the diagnostic selector. Required evidence remains `[BMDSFIX1] ARMED`, target `APPLIED ...->1`, completed generation and normal landed gameplay without the prior persistent atmosphere/retry failure or a new severe target-attributable regression.
'''
RECORD.write_text(record, encoding="utf-8")

lifecycle = LIFECYCLE.read_text(encoding="utf-8")
new_runtime = f'''## BMDSFIX1 runtime — partial exact-byte control plus DIAG1PATH1 supporting PASS

The pair-scoped Deep Sewers mitigation `S1.42AK-BMDSFIX1` remains the exact active gameplay candidate / not accepted. Exact gameplay profile SHA-256 remains `{EXPECTED_GAMEPLAY_PROFILE_SHA}` and BMDSFIX1 DLL SHA-256 remains `{EXPECTED_GAMEPLAY_DLL_SHA}`. The exact Black Mesa x Substation run at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/` remains the preserved non-target control.

The separately versioned `S1.42AK-BMDSFIX1-DIAG1PATH1` supporting run is now ingested at `{EVIDENCE_REL}`, raw log SHA-256 `{EXPECTED_LOG_SHA}`. The short-name diagnostic armed without refusal, selected Black Mesa / `DeepSewersFlow` deterministically from the normalized viable pool (`pool=31->1`), BMDSFIX1 armed and applied `4.875->1`, final length multiplier was `1`, dungeon generation completed, `Players finished generating the new floor` appeared, normal post-generation activity continued, and the session later returned to orbit. The user independently reported no `Entering the atmosphere` problem and no noticeable gameplay issue. Decision authority: `{RECORD_REL}`.

This is a **supporting diagnostic PASS only**. DIAG1PATH1 remains never acceptable as gameplay and does not accept or qualify BMDSFIX1. The finite DunGen placement retries resolved into successful generation; unrelated log noise such as the SoundAPI/HarmonyX TypeLoadException remains outside the pair-scoped finding.

The regular exact-byte BMDSFIX1 Black Mesa x `DeepSewersFlow` gameplay gate remains outstanding and unwaived. Runtime/evidence routing is returned to exact BMDSFIX1 before that gate; the diagnostic selector is not allowed in the qualification run. Black Mesa x Greenhouse remains separate and `NOT_YET_PROVEN`.
'''
lifecycle = replace_between(lifecycle, "## BMDSFIX1 runtime — partial non-target evidence, target outstanding", "## Live execution state", new_runtime)

new_live = f'''## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK-BMDSFIX1 — active gameplay candidate / not accepted**.
- Active gameplay candidate: **S1.42AK-BMDSFIX1**.
- Runtime/evidence pointer: **S1.42AK-BMDSFIX1** — restored after successful DIAG1PATH1 supporting evidence.
- DIAG1PATH1: **supporting diagnostic PASS / evidence ingested / NEVER ACCEPT / no longer runtime-armed**.
- Diagnostic parent DIAG1: **preloader-blocked historical one-hop provenance / must not be rerun**.
- Runtime test outstanding: **yes — regular exact-byte BMDSFIX1 Black Mesa x DeepSewersFlow gameplay qualification remains outstanding and unwaived**.
- Preserved exact-byte non-target control: **Black Mesa x Substation PASS** at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/`.
- Supporting target diagnostic: **Black Mesa x DeepSewersFlow PASS** at `{EVIDENCE_REL}` under DIAG1PATH1, supporting only.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 candidate bytes.
- S1.42AK remains the accepted rollback baseline; Greenhouse/BMGHDIAG remains separate.
'''
lifecycle = replace_between(lifecycle, "## Live execution state", "## Exact next project action", new_live)
lifecycle = replace_between(lifecycle, "## Exact next project action", "## Permanent Gale workflow", "## Exact next project action\n\n" + next_action)
LIFECYCLE.write_text(lifecycle, encoding="utf-8")

km = MAP.read_text(encoding="utf-8")
start = km.find("The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation remains")
require(start >= 0, "knowledge-map BMDSFIX1 anchor missing")
end = km.find("## Authority rule", start)
require(end >= 0, "knowledge-map authority anchor missing")
km_block = f'''The pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation remains the **active gameplay candidate / not accepted**. Its exact Black Mesa x Substation run remains the preserved non-target control. The identity-only `S1.42AK-BMDSFIX1-DIAG1PATH1` successor has now supplied successful supporting Black Mesa x `DeepSewersFlow` evidence at `{EVIDENCE_REL}` (raw log SHA-256 `{EXPECTED_LOG_SHA}`): selector ARMED and `pool=31->1`, BMDSFIX1 ARMED, target `APPLIED 4.875->1`, final multiplier 1, completed dungeon generation and normal post-generation gameplay; the user reported no atmosphere-screen problem or noticeable issue. Decision authority: `{RECORD_REL}`.

DIAG1PATH1 remains diagnostic support only / **NEVER ACCEPT** and cannot qualify BMDSFIX1 because the deterministic selector DLL was present. Runtime/evidence routing is therefore returned to exact `S1.42AK-BMDSFIX1`. The regular exact-byte gameplay Black Mesa x `DeepSewersFlow` qualification remains outstanding and unwaived. The long-name DIAG1 remains preloader-blocked historical provenance and must not be rerun. Black Mesa x Greenhouse/BMGHDIAG remains separate.

'''
MAP.write_text(km[:start] + km_block + km[end:], encoding="utf-8")

print("DIAG1PATH1 supporting PASS reconciled; runtime routing restored to exact BMDSFIX1 gameplay candidate")
