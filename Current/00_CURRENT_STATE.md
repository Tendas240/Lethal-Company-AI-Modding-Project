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

S1.42AK-TSDIAG1 original-bound DERIVED runtime BUILD_RESULT and narrow frozen source/review CI boundary repair from PR #410 are now MAIN-INTEGRATED and permanently exact-main-head CI-verified: PR head 1b3eab527226f4074c38d86ef4d173edc2fb615e, pinned merge c76ae7c12d0473cfe53b9b8eb7cf1b70d7bdb515, Knowledge Architecture push 37969600702/#1562 completed/success on that same head. Current/377_S1.42AK_TSDIAG1_DERIVED_BUILD_RESULT_AND_CI_BOUNDARY_REPAIR.md is historical PR-stage provenance; Current/378_S1.42AK_TSDIAG1_DERIVED_METADATA_CI_POST_MERGE_LIFECYCLE_RECONCILIATION.md records this lifecycle reconciliation. The distinct BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json is explicitly DERIVED, not the original 915-byte prevalidation Evidence/BUILD_RESULT.json (SHA-256 9a34b7f1d7b5dd910913e1a39ed033de98f76d8542065f244e64e6f7f400235a, status COMPILE_INPUT_PRESENT_ARCHIVE_AWAITS_INDEPENDENT_VALIDATION). Sole original artifact 11615262607, original published/indexed profile Profiles/LC V1 S1.42AK-TS1.r2z SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e, TSDIAG1 DLL fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201 and immutable BMDSFIX1 direct parent unchanged. The old TSDIAG1 source PR path filter Current/CURRENT_STATE.json was removed in exactly one line; frozen-review guard permits only this exact producer-workflow deletion and the derived provenance/schema validator rejected 20/20 negative mutations on final PR-head CI, with review build/repack/upload steps skipped. Reconciliation documentation must first pass exact-final-PR-head CI and separately pinned merge/permanent exact-new-main-head CI; after that, the next separately user-gated project segment is ONLY the TSDIAG1 original-byte diagnostic runtime-ACTIVATION CHECKPOINT PR preparation and exact-final-head CI. No automatic activation/merge, Gale import, runtime test or acceptance. Maintain BuildSpecs/current.json disabled/IDLE and RuntimeInbox/ACTIVE_BUILD.txt plus CURRENT_STATE.controllers.runtime_active_build=S1.42AK-BMDSFIX1; selected_scope.diagnostic_revision remains inactive completed SCDIAG1, toy_store_tsdiag1_runtime_armed=false, toy_store_runtime_test_authorized=false. TSDIAG1 DIAGNOSTIC ONLY / NEVER ACCEPT, actual Toy Store generation/materialization/entrance/traversal unproven; user-local Windows Gale root path still unverified (216/255 reference root only). Accepted S1.42AK; BMDSFIX1 NOT ACCEPTED with independent passive selector-free Black Mesa x DeepSewersFlow gate unwaived; Phase-C residual 22 = 10 viable/equal-100 + 12 owner-hard-block.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
