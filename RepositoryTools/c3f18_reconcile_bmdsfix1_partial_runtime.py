#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "Current/CURRENT_STATE.json"
LIFECYCLE = ROOT / "Knowledge/CURRENT_LIFECYCLE.md"
MAP = ROOT / "Current/PROJECT_KNOWLEDGE_MAP.md"
RECORD = ROOT / "Current/175_S1.42AK_BMDSFIX1_PARTIAL_RUNTIME_EVIDENCE_NON_TARGET_CONTROL.md"
EVIDENCE = ROOT / "RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z"
LOG = EVIDENCE / "raw/LogOutput.log"
INDEX = EVIDENCE / "INDEX.json"
BUILDSPEC = ROOT / "BuildSpecs/current.json"
ACTIVE = ROOT / "RuntimeInbox/ACTIVE_BUILD.txt"
EXPECTED_PROFILE_SHA = "3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0"
EXPECTED_DLL_SHA = "f337da49f4a0e75bf2753e17e3abc52cdbea56ba37eddec5f1065b17f4d75a92"
EXPECTED_LOG_SHA = "9a8cf28bbfc050cf9247cffacc890ea1b4e7215329db4ecfc9085f3f8f0ff2cb"
EVIDENCE_REL = "RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/"
RECORD_REL = "Current/175_S1.42AK_BMDSFIX1_PARTIAL_RUNTIME_EVIDENCE_NON_TARGET_CONTROL.md"


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
require(state["active_candidate"]["sha256"] == EXPECTED_PROFILE_SHA, "active profile SHA drift")
require(state["runtime_test_outstanding"] is True, "runtime gate is no longer outstanding")
require(state["selected_scope"]["status"] == "PHASE_C3F18_BMDSFIX1_RUNTIME_ACTIVE_TEST_OUTSTANDING", "unexpected source lifecycle status")
require(ACTIVE.read_text(encoding="utf-8").strip() == "S1.42AK-BMDSFIX1", "ACTIVE_BUILD drift")
buildspec = json.loads(BUILDSPEC.read_text(encoding="utf-8"))
require(buildspec["enabled"] is False, "BuildSpecs/current.json unexpectedly enabled")
require(buildspec["base_sha256"] == EXPECTED_PROFILE_SHA, "BuildSpecs base SHA drift")
require(LOG.is_file() and INDEX.is_file(), "expected ingested BMDSFIX1 evidence missing")
log_bytes = LOG.read_bytes()
actual_log_sha = hashlib.sha256(log_bytes).hexdigest()
require(actual_log_sha == EXPECTED_LOG_SHA, f"runtime log SHA drift: {actual_log_sha}")
idx = json.loads(INDEX.read_text(encoding="utf-8"))
require(idx["build_id"] == "S1.42AK-BMDSFIX1", "runtime index build attribution drift")
require(idx["files"][0]["sha256"] == EXPECTED_LOG_SHA, "runtime index log SHA drift")
text = log_bytes.decode("utf-8", errors="replace")
require("[BMDSFIX1] ARMED" in text, "BMDSFIX1 ARMED marker missing")
require("[BMDSFIX1] REFUSED TO ARM" not in text, "BMDSFIX1 refused to arm")
require("Created New Day History Log! PlanetName: Black Mesa ,Substation" in text, "Black Mesa x Substation selection missing")
require("[BMDSFIX1] APPLIED" not in text, "unexpected BMDSFIX1 APPLIED marker in non-target control")
require("Dungeon has finished generating on this client after multiple frames" in text, "dungeon completion missing")
require("Players finished generating the new floor" in text, "player generation completion missing")
require("CurrentLevel: Black Mesa DungeonSize Is: 6.343513 | Leaving DungeonSize As: 9.515268" in text, "Substation size observation missing")
require("Final length multiplier: 9.51" in text, "Substation final multiplier observation missing")
require("Hangar state changed -> OPEN; doorPower=1.000; landed=False" in text, "hangar-open landed=False observation missing")
require("Ship has landed" in text, "later ship-landed observation missing")
require(not RECORD.exists(), "partial runtime record already exists")

scope = state["selected_scope"]
scope["status"] = "PHASE_C3F18_BMDSFIX1_RUNTIME_PARTIAL_NON_TARGET_CONTROL_PASS_TARGET_OUTSTANDING"
scope["finding"] = (
    "S1.42AK-BMDSFIX1 remains the exact active gameplay runtime candidate / not accepted. "
    f"Exact runtime evidence is ingested at {EVIDENCE_REL} with raw LogOutput.log SHA-256 {EXPECTED_LOG_SHA}. "
    "The candidate armed without refusal; Black Mesa selected Substation, not DeepSewersFlow, and no BMDSFIX1 APPLIED marker occurred, so this exact-byte run supplies the required non-target-control observation without an unintended BMDSFIX1 application. "
    "It does not qualify the target pair because DeepSewersFlow was not selected. The same run records an unusually large Black Mesa x Substation generation (6.343513->9.515268 / final 9.51), delayed generation completion overlapping an OPEN hangar while landed=False, and the user's severe stutter/freeze/second-landing observation; this is preserved as a separate runtime finding and is not attributed to BMDSFIX1 because the fix did not apply. "
    "Accepted baseline remains S1.42AK; Black Mesa x Greenhouse remains NOT_YET_PROVEN."
)
scope["analysis_contract"] = (
    "Treat S1.42AK-BMDSFIX1 as active but not accepted. Preserve exact profile SHA-256 " + EXPECTED_PROFILE_SHA + " and BMDSFIX1 DLL SHA-256 " + EXPECTED_DLL_SHA + ". "
    f"Preserve the partial runtime evidence and decision at {EVIDENCE_REL} and {RECORD_REL}. "
    "The non-target-control criterion is satisfied by exact identical candidate bytes and need not be repeated solely for qualification. The remaining runtime proof is Black Mesa x DeepSewersFlow: [BMDSFIX1] ARMED without refusal, APPLIED with multiplier ->1, successful generation/landing, no persistent retry/atmosphere failure, and no new severe target-attributable generation/entrance/routing/NavMesh regression. "
    "Evidence may accumulate across runs only when the exact candidate profile bytes remain identical; no qualification criterion is waived. Do not change gameplay/config/package/profile/plugin bytes, S1.42AB normalization, Dawn/native Black Mesa ownership, or the separate Greenhouse scope."
)
next_action = (
    "Keep exact active S1.42AK-BMDSFIX1 bytes unchanged and run only the remaining Black Mesa x DeepSewersFlow target gate: obtain a target selection showing [BMDSFIX1] ARMED and APPLIED with multiplier ->1, completed dungeon generation and normal landed gameplay without the prior persistent retry/Entering-the-atmosphere failure or a new severe target-attributable regression. "
    "Upload that run's exact BepInEx/LogOutput.log with the existing build-specific uploader. The already-ingested Black Mesa x Substation run is the preserved non-target control and does not need to be repeated solely for qualification."
)
scope["next_action"] = next_action
state["next_action"] = next_action
phase_c = scope["phase_c"]
phase_c["bmdsfix1_partial_runtime_decision"] = RECORD_REL
phase_c["bmdsfix1_partial_runtime_evidence"] = EVIDENCE_REL
phase_c["bmdsfix1_partial_runtime_log_sha256"] = EXPECTED_LOG_SHA
phase_c["bmdsfix1_non_target_control_status"] = "PASS_BLACK_MESA_SUBSTATION_NO_BMDSFIX1_APPLICATION"
phase_c["bmdsfix1_target_status"] = "OUTSTANDING_BLACK_MESA_DEEP_SEWERS"
phase_c["black_mesa_substation_runtime_finding"] = (
    "Black Mesa selected Substation. LLL reported DungeonSize 6.343513->9.515268 and ButteRyBalance final 9.51; generation completed, but hangar OPEN occurred while landed=False before Players finished generating the new floor, and Ship has landed was logged later. "
    "The user reported severe stutter/freezing and an apparent second landing. Preserve as a separate non-target runtime/performance finding; the evidence does not attribute it to BMDSFIX1 because no BMDSFIX1 APPLIED marker occurred."
)
review = scope["bmdsfix1_review"]
review["runtime_validation_status"] = "PARTIAL_RUNTIME_EVIDENCE_NON_TARGET_CONTROL_PASS_TARGET_OUTSTANDING_NOT_ACCEPTED"
review["runtime_evidence"] = EVIDENCE_REL
review["runtime_index"] = EVIDENCE_REL + "INDEX.json"
review["runtime_log_sha256"] = EXPECTED_LOG_SHA
review["runtime_decision"] = RECORD_REL
review["non_target_control_status"] = "PASS_BLACK_MESA_SUBSTATION_NO_BMDSFIX1_APPLICATION"
review["target_status"] = "OUTSTANDING_BLACK_MESA_DEEP_SEWERS"
scope["bmdsfix1_partial_runtime_decision"] = RECORD_REL
scope["bmdsfix1_partial_runtime_evidence"] = EVIDENCE_REL
STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

record = f'''# S1.42AK-BMDSFIX1 Partial Runtime Evidence — Non-Target Control

**Date:** 2026-09-24  
**Status:** PARTIAL RUNTIME EVIDENCE / NON-TARGET CONTROL PASS / TARGET OUTSTANDING / NOT ACCEPTED  
**Accepted gameplay baseline:** S1.42AK — unchanged  
**Active candidate:** S1.42AK-BMDSFIX1 — unchanged exact bytes  
**Profile SHA-256:** `{EXPECTED_PROFILE_SHA}`  
**BMDSFIX1 DLL SHA-256:** `{EXPECTED_DLL_SHA}`  
**Runtime evidence:** `{EVIDENCE_REL}`  
**Raw LogOutput.log SHA-256:** `{EXPECTED_LOG_SHA}`

## Decision

The ingested exact-byte BMDSFIX1 run is accepted as **partial qualification evidence only**.

It satisfies the non-target-control observation for the unchanged candidate bytes:

- `[BMDSFIX1] ARMED` appears and no `[BMDSFIX1] REFUSED TO ARM` was found;
- Black Mesa selected `Substation`, not `DeepSewersFlow`;
- no `[BMDSFIX1] APPLIED` marker occurred in the non-target generation;
- the dungeon ultimately completed and `Players finished generating the new floor` appeared.

It does **not** qualify Black Mesa x `DeepSewersFlow` because the target flow was not selected. BMDSFIX1 therefore remains active / not accepted and `runtime_test_outstanding` remains true.

Qualification evidence may accumulate across separate runtime logs only while the exact candidate profile bytes are unchanged. This preserves every criterion from `Current/174_S1.42AK_BMDSFIX1_RUNTIME_ACTIVATION.md`; it does not waive the target-generation requirements. The already-ingested Substation control does not need to be repeated solely to recreate the same non-target observation.

## Separate Black Mesa x Substation runtime finding

The same non-target run exposed a material runtime/performance symptom that must not be discarded:

- LethalLevelLoader reported Black Mesa `DungeonSize Is: 6.343513 | Leaving DungeonSize As: 9.515268`;
- ButteRyBalance reported final length multiplier `9.51`;
- DunGenPlus emitted placement-failure/retry diagnostics during generation;
- `Hangar state changed -> OPEN` was logged while `landed=False`;
- `Player exited ship` occurred before `Players finished generating the new floor`;
- dungeon generation nevertheless completed;
- the later `Ship has landed` event occurred substantially after the hangar-open transition.

The user independently reported a very long `Entering the atmosphere` period, severe stutter, a temporary frozen frame and an apparent second landing after the ship already seemed landed.

The log supports a delayed/overlapping landing-generation sequence, but this checkpoint does **not** claim a proven performance root cause. A similar two-stage hangar-open / later-landing pattern existed in earlier Black Mesa evidence. This run also does not attribute the Substation symptom to BMDSFIX1: the pair-scoped fix never emitted `APPLIED` for Substation.

The Substation finding is therefore preserved as a separate Black Mesa/runtime-performance observation and is not allowed to silently invalidate or qualify the Deep Sewers target gate.

## Remaining BMDSFIX1 target gate

Keep the exact candidate bytes unchanged and obtain Black Mesa x `DeepSewersFlow` evidence establishing:

1. `[BMDSFIX1] ARMED` without refusal;
2. target selection of `DeepSewersFlow`;
3. `[BMDSFIX1] APPLIED Black Mesa / DeepSewersFlow multiplier=...->1`;
4. completed dungeon generation and `Players finished generating the new floor`;
5. normal landed gameplay without the prior persistent `Entering the atmosphere` failure;
6. no persistent retry flood equivalent to the failing 4.875 incident;
7. no new severe target-attributable generation, entrance, routing or NavMesh regression.

The previously ingested Substation run supplies the unchanged-byte non-target-control criterion.

Black Mesa x Greenhouse remains a separate `NOT_YET_PROVEN` successor-diagnostic task.

## Preserved boundaries

- S1.42AK remains the sole accepted baseline.
- S1.42AK-BMDSFIX1 remains active / not accepted.
- No gameplay, config, package, profile or plugin bytes change in this reconciliation.
- `BuildSpecs/current.json` remains disabled and guards the exact BMDSFIX1 profile.
- `RuntimeInbox/ACTIVE_BUILD.txt` remains `S1.42AK-BMDSFIX1`.
- S1.42AB InteriorWeightNormalization remains unchanged.
- Black Mesa remains Dawn/native-owned.
'''
RECORD.write_text(record, encoding="utf-8")

lifecycle = LIFECYCLE.read_text(encoding="utf-8")
new_bmds = f'''## BMDSFIX1 runtime — partial non-target evidence, target outstanding

The pair-scoped Deep Sewers mitigation `S1.42AK-BMDSFIX1` remains the exact active gameplay runtime candidate / not accepted. Exact profile SHA-256 remains `{EXPECTED_PROFILE_SHA}` and BMDSFIX1 DLL SHA-256 remains `{EXPECTED_DLL_SHA}`; no gameplay/config/package/profile/plugin bytes changed during this reconciliation.

Runtime evidence is ingested at `{EVIDENCE_REL}`, raw log SHA-256 `{EXPECTED_LOG_SHA}`. BMDSFIX1 armed without refusal. Black Mesa selected `Substation`, not `DeepSewersFlow`, and no `[BMDSFIX1] APPLIED` marker occurred. That exact-byte run is therefore preserved as the non-target control and does not need to be repeated solely for qualification. It does not qualify the target pair because Deep Sewers was not selected. Decision authority: `{RECORD_REL}`.

The same Substation run recorded `DungeonSize 6.343513 -> 9.515268` / final multiplier `9.51`, delayed generation completion overlapping an OPEN hangar while `landed=False`, and the user's severe stutter/freeze/apparent second-landing symptom. The finding is preserved separately without claiming a proven root cause or attributing it to BMDSFIX1, which did not apply to Substation.

The remaining runtime gate is only Black Mesa x `DeepSewersFlow`: `[BMDSFIX1] ARMED`, target `APPLIED ... ->1`, completed generation and normal landed gameplay without the prior persistent retry/atmosphere failure or a new severe target-attributable regression. Evidence may accumulate across exact identical candidate bytes; no qualification criterion is waived. Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task.'''
lifecycle = replace_between(lifecycle, "## BMDSFIX1 exact-byte publication — runtime activation", "## Live execution state", new_bmds)
new_live = '''## Live execution state

- Accepted baseline: **S1.42AK**.
- Latest built artifact: **S1.42AK-BMDSFIX1 — active runtime candidate / not accepted**.
- Active gameplay candidate: **S1.42AK-BMDSFIX1**.
- Active diagnostic runtime target: **none**.
- Runtime test outstanding: **yes — remaining Black Mesa x DeepSewersFlow target qualification only**.
- Preserved partial evidence: **Black Mesa x Substation non-target control PASS** at `RuntimeEvidence/S1.42AK-BMDSFIX1/20260924T170032Z/`.
- Selected scope: **Universal Interior Viability / Equal Availability — BMDSFIX1 partial runtime evidence ingested; target evidence outstanding**.
- `BuildSpecs/current.json`: disabled at `IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`, guarding exact BMDSFIX1 candidate bytes.
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`.
- S1.42AK remains the accepted rollback baseline; no Greenhouse diagnostic is armed.'''
lifecycle = replace_between(lifecycle, "## Live execution state", "## Exact next project action", new_live)
new_next = f'''## Exact next project action

{next_action}'''
lifecycle = replace_between(lifecycle, "## Exact next project action", "## Permanent Gale workflow", new_next)
LIFECYCLE.write_text(lifecycle, encoding="utf-8")

km = MAP.read_text(encoding="utf-8")
para_start = km.find("The separate pair-scoped `S1.42AK-BMDSFIX1`")
require(para_start >= 0, "knowledge-map BMDSFIX1 anchor paragraph missing")
para_end = km.find("\n\n## Authority rule", para_start)
require(para_end >= 0, "knowledge-map authority marker missing")
new_para = (
    "The separate pair-scoped `S1.42AK-BMDSFIX1` Deep Sewers mitigation remains the **active gameplay runtime candidate / not accepted**. "
    f"Exact runtime evidence is ingested at `{EVIDENCE_REL}` with raw log SHA-256 `{EXPECTED_LOG_SHA}`. The run armed BMDSFIX1 but Black Mesa selected Substation, so no `APPLIED` marker occurred; this is preserved as the exact-byte non-target control. "
    f"The remaining gate is only Black Mesa x `DeepSewersFlow`; decision authority: `{RECORD_REL}`. The same run preserves a separate Substation large-generation/landing-stutter finding without attributing it to BMDSFIX1. "
    "`BuildSpecs/current.json` remains disabled while guarding the candidate, `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`, accepted baseline remains S1.42AK, and Black Mesa x Greenhouse remains `NOT_YET_PROVEN` under its separate successor-diagnostic task."
)
km = km[:para_start] + new_para + km[para_end:]
MAP.write_text(km, encoding="utf-8")

print("PASS: BMDSFIX1 partial runtime reconciliation staged")
