<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-14  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AH — Mouth Dog Pikmin Dual Prevention — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Acceptance: `Current/142_S1.42AH_RUNTIME_ACCEPTANCE_MOUTHDOG_DUAL_PREVENTION.md`  
Runtime evidence: `RuntimeEvidence/S1.42AH/20260909T162513Z/`

## Latest built artifact

**S1.42AI-DIAG1 — ShyGuy Isolation Diagnostic — RUNTIME DIAGNOSTIC FAILED REPAIR REQUIRED NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AI-DIAG1 ShyGuy Isolation.r2z`  
SHA-256: `22e2132669a790756f2a1e2bd10b14fd05144b3ecdd55233d8d57f1d6dd9f3fd`  
Candidate record: `Current/144_S1.42AI-DIAG1_BUILD_CANDIDATE_SHYGUY_ISOLATION.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **none**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AI-DIAG1_RUNTIME_FAILURE_AWAITING_REPAIR`)
- Guarded build base: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z` / `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1`

## Exact next action

Repair the S1.42AI-DIAG1 owner type-resolution contract and its static gate before any further gameplay test. Remove the hardcoded LethalMin.PikminType assumption, derive and validate the exact List<T> generic argument from the declared LethalMin.Onion.WithdrawPikminFromOnion method metadata with fail-closed checks, harden AnalysisTools/validate_s142ai_diag1_static.py to prove the corresponding CLR parameter contract against the materialized LethalMin DLL, then build and validate a successor diagnostic candidate repository-native. Do not rerun the current S1.42AI-DIAG1 profile unchanged.

No new runtime test is pending. A completed run may still require its build-specific PowerShell uploader before evidence ingestion; `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
