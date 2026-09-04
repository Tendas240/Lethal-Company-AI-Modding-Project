<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-04  
**Game:** Lethal Company V81

## Accepted baseline

**S1.42AB — Interior Weight Normalization — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AB Interior Weight Normalization.r2z`  
SHA-256: `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`  
Acceptance: `Current/102_S1.42AB_RUNTIME_ACCEPTANCE_INTERIOR_WEIGHT_NORMALIZATION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AB/20260904T174010Z/`

## Latest built artifact

**S1.42AC — BCMER EventType Equal Distribution — FORMALLY REJECTED / NOT PROMOTED**

Profile: `Profiles/LC V1 S1.42AC BCMER EventType Equal Distribution.r2z`  
SHA-256: `0ce58ab1fa0f0d76d6fbe1a4bff1dce9defc92e3d4b70cfb3056306e617e47d9`  
Original rejection: `Current/106_S1.42AC_RUNTIME_REJECTION_BCMER_EVENTTYPE_EQUAL_DISTRIBUTION.md`  
Corrected source-path analysis: `Current/109_BCMER_1_71_0_EVENTTYPE_WEIGHT_PATH_ANALYSIS.md`

The old S1.42AC equality gate misread BCMER's logged values as aggregate EventType weights. `Current/109` proves they are per-event weights normalized by enabled event count. The equal 12.5 scales are therefore the correct static EventType-probability model; this technical correction does not silently promote the rejected artifact.

## Live execution state

- Active candidate: **none**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AC_WEIGHT_PATH_ANALYSIS_COMPLETE_NO_SUCCESSOR_ARMED`)
- Guarded build base: accepted S1.42AB / `3f2387886daaf68d0d55ddc1b3cffb913565a658db0072b11f3b975ff07860ca`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AB`

## Exact next action

If BCMER EventType work continues, reevaluate the existing S1.42AC artifact/evidence with the corrected static EventType acceptance model from Current/109. Do not build a compensation successor and do not require equal per-event log weights.

No PowerShell uploader is required now because no runtime test is pending.

## Where current truth lives

Use `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
