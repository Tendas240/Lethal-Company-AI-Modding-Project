<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-10-09  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AK — LC Office Camera Enemy Balance — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AK LC Office Camera Enemy Balance.r2z`  
SHA-256: `b39aa550a517ec727de6eb1ae825383933047d3c556cb6e8d4aa7611c9f89dee`  
Acceptance: `Current/158_S1.42AK_RUNTIME_ACCEPTANCE_LC_OFFICE_CAMERA_ENEMY_BALANCE.md`  
Runtime evidence: `RuntimeEvidence/S1.42AK/20260918T172838Z/`

## Latest built artifact

**S1.42AK-BMDSFIX1 — Black Mesa Deep Sewers Size Fix — ACTIVE RUNTIME CANDIDATE NOT ACCEPTED**

Profile: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z`  
SHA-256: `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`  
Candidate record: `Current/174_S1.42AK_BMDSFIX1_RUNTIME_ACTIVATION.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **S1.42AK-BMDSFIX1**
- Runtime test outstanding: **yes**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS`)
- Guarded build base: `Profiles/LC V1 S1.42AK-BMDSFIX1 Black Mesa Deep Sewers Size Fix.r2z` / `3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-BMDSFIX1`

## Exact next action

S1.42AK-TSDIAG1 frozen original BUILD_RESULT and CI-stage preflight is now independently evidence-verified in Current/376_S1.42AK_TSDIAG1_FROZEN_ORIGINAL_PROVENANCE_AND_CI_STAGE_PREFLIGHT.md: downloaded exact sole original artifact 11615262607, outer ZIP SHA-256 010b84c1ffaea1d5cda2e14cdb9580c049da2cd1790e929491e44d13e2c4f39f; its original Evidence/BUILD_RESULT.json SHA-256 9a34b7f1d7b5dd910913e1a39ed033de98f76d8542065f244e64e6f7f400235a has status COMPILE_INPUT_PRESENT_ARCHIVE_AWAITS_INDEPENDENT_VALIDATION and original parent/review fields but NOT Gale runtime base/output fields. Do not misrepresent, copy verbatim as a runtime BUILD_RESULT, or reconstruct the artifact. Frozen checkpoint, already published unchanged original profile SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e and canonical indexed provenance are independent inputs for a separately validated DERIVED diagnostic build-result. Frozen TSDIAG1 source workflow currently watches Current/CURRENT_STATE.json; source validator and frozen review guard require pre-activation BMDSFIX1/armed=false. Next only after this documentation PR's exact-final-PR-head CI, separate pinned merge and permanent exact-new-main CI: a bounded, user-gated original-anchored runtime metadata derivative plus exact source-workflow trigger-only / frozen-review guard lifecycle-boundary repair checkpoint, with negative mutation tests and final-head CI; no wider validator/source/build workflow relaxation, no recompilation, repack, republish, profile index or Gale action. Later activation requires a DISTINCT PR/gate, and future local Gale path checks and test authorization remain separate. All live controllers stay BMDSFIX1/IDLE; TSDIAG1 runtime_armed=false, toy_store_runtime_test_authorized=false, DIAGNOSTIC ONLY / NEVER ACCEPT. Accepted S1.42AK, BMDSFIX1 NOT ACCEPTED and independent passive selector-free Black Mesa x DeepSewersFlow proof outstanding; residual 22=10 viable/equal-100 plus 12 owner-hard-block.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
