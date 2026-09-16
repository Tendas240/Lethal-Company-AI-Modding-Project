<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-16  
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

**S1.42AI-DIAG1R3 — ShyGuy Isolation Diagnostic Exact Identity Repair — BUILD PASS STATIC MATERIALIZED IDENTITY APPLICABILITY EQUIVALENCE PASS RUNTIME PENDING NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z`  
SHA-256: `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`  
Candidate record: `Current/150_S1.42AI-DIAG1R3_BUILD_CANDIDATE_EXACT_IDENTITY_REPAIR.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **S1.42AI-DIAG1R3**
- Runtime test outstanding: **yes**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AI-DIAG1R3_BUILD_AWAITING_RUNTIME`)
- Guarded build base: `Profiles/LC V1 S1.42AI-DIAG1R3 ShyGuy Identity Repair.r2z` / `13d73d8aa1b651bccfb80d8b242efe63eae7def3639df1ad949bfdf724424768`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AI-DIAG1R3`

## Exact next action

Run one exact S1.42AI-DIAG1R3 diagnostic gameplay gate. Require clean DIAG1 owner/applicability/guard-layer startup and repaired exact ShyGuy identity resolution, verify no unexpected non-ShyGuy enemy appears while isolation is armed, and verify an exterior ShyGuy is visible when that condition is exercised. Then upload the fresh complete R3 LogOutput.log for repository-native ingestion and decision. If no exterior ShyGuy is encountered, report it as not exercised rather than passed. Do not execute the deferred full-normal S1.42AI gate yet.

A runtime test is pending for S1.42AI-DIAG1R3. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
