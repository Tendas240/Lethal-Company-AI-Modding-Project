<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-18  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AI — BCMER ShyGuy Interior-Only Event Correction — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AI ShyGuy Interior Only.r2z`  
SHA-256: `d993bc0fca265fe7a2b069bd654b5e2c1f590623eaf7f4fabb325f8b4d863cb2`  
Acceptance: `Current/152_S1.42AI_RUNTIME_ACCEPTANCE_BCMER_SHYGUY_INTERIOR_ONLY.md`  
Runtime evidence: `RuntimeEvidence/S1.42AI/20260916T180452Z/`

## Latest built artifact

**S1.42AJ — LC Office V81 Integration — STATIC VALIDATED NOT ACCEPTED SUCCESSOR PREPARATION SELECTED**

Profile: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z`  
SHA-256: `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`  
Candidate record: `Current/153_S1.42AJ_BUILD_CANDIDATE_LC_OFFICE_V81_INTEGRATION.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **none**
- Runtime test outstanding: **no**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AJ_DIAG2_CONFIRMATION_AWAITING_S1.42AK_BUILD`)
- Guarded build base: `Profiles/LC V1 S1.42AJ LC Office V81 Integration.r2z` / `7c1441aeb0732208bb8e910d89348c2e0129ce202422103a025e8f8aea707dba`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AJ-DIAG2`

## Exact next action

Execute the repository-native atomic S1.42AK build from exact S1.42AJ according to BuildSpecs/S1.42AK_PLAN.md. BuildSpecs/current.json is intentionally disabled before that trigger. The authorized delta is only LC Office Camera Frame Speed = 0, YaBoiDucki-men_stalker 3.1.2 disabled, and Biodiversity Aloe PowerLevel = 0; RandomEnemiesSize and LC Office scrap settings must remain unchanged.

No new runtime test is pending. A completed run may still require its build-specific PowerShell uploader before evidence ingestion; `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
