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

S1.42AK-TSDIAG1 exact-original DERIVED runtime BUILD_RESULT plus narrow source/review CI stage repair are MAIN-MERGED and permanently CI-verified by PR #410 (merge c76ae7c12d0473cfe53b9b8eb7cf1b70d7bdb515, Knowledge Architecture push 37969600702/#1562 success), and their lifecycle reconciliation PR #411 is NOW ALSO MAIN-MERGED and exact-main-head CI-verified: final PR head 393fb1a008d50def4aefa068cbf1f413fab00089, pinned merge 1527f3dc6d49e35b01d5cda30ec7b5c3466c31cb, permanent Knowledge Architecture push 37970882345/#1564 event=push completed/success on exact main HEAD. Current/379_S1.42AK_TSDIAG1_POST_RECONCILIATION_HANDOVER_AUTHORITY_REPAIR.md corrects the former STAGED navigation; historical Current/375–378 documents retain their original checkpoint-stage truth, and historical staged wording is NOT current authority. No relevant PR remains open as of this handover repair preflight. NEXT SEPARATELY USER-GATED PROJECT SEGMENT AFTER THE REPOSITORY'S LATEST MAIN-HEAD AND CI ARE RECHECKED: prepare a separately bounded S1.42AK-TSDIAG1 original-byte diagnostic RUNTIME-ACTIVATION CHECKPOINT PR, with fresh canonical profile/index/DERIVED metadata/Gale v2.4.6 exact-parent resolver verification, explicit guarded rollback and exact final PR-head CI; do NOT merge that activation PR within its preparation segment. The original published indexed profile Profiles/LC V1 S1.42AK-TS1.r2z SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e, TSDIAG1 DLL SHA-256 fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201, frozen sole review artifact 11615262607 and BMDSFIX1 parent remain unchanged; BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json is DERIVED, not the 915-byte original prevalidation Evidence/BUILD_RESULT.json. Until separate activation integration, BuildSpecs/current.json disabled/IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS, RuntimeInbox/ACTIVE_BUILD.txt and CURRENT_STATE.controllers.runtime_active_build=S1.42AK-BMDSFIX1, existing selected_scope.diagnostic_revision=S1.42AK-SCDIAG1 inactive, toy_store_tsdiag1_runtime_armed=false and toy_store_runtime_test_authorized=false. Reference-root Gale budget 216/255 does NOT verify actual user Windows path; future Gale import/test/log upload are separate gates. No automatic build/rebuild, repack, upload, publication, index, gameplay/runtime test or acceptance. S1.42AK remains ACCEPTED, BMDSFIX1 NOT ACCEPTED with independent passive selector-free Black Mesa x DeepSewersFlow proof unwaived, Phase-C residual 22=10 viable/equal-100+12 owner-hard-block, Toy Store actual generation/materialization/entrance/traversal unproven, TSDIAG1 DIAGNOSTIC ONLY / NEVER ACCEPT.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
