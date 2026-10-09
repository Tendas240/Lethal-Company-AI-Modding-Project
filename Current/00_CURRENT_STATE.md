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

S1.42AK-TSDIAG1 conditional diagnostic runtime-activation AUTHORIZATION DECISION (PR #405) and subsequent post-merge lifecycle RECONCILIATION (PR #406) are BOTH ALREADY MAIN-MERGED and permanently exact-main-head CI verified. PR #405 final reviewed PR head 1ae4ca830934cb944639cbba3267260ce0e4068c merged as main 46096717993039e3b7b2b7cb8579fc4bcec9151c; its permanent Knowledge Architecture push 37960835253/#1551 passed. PR #406 exact final reviewed PR head 353844993ff57f40c9d869bd71e5bbef667e7eb3 passed 5/5 pull_request CI and merged with pinned expected_head_sha as main 97c6807ef58f697eb164d1acd20148f5e13d3588, ordered parents 46096717993039e3b7b2b7cb8579fc4bcec9151c and 353844993ff57f40c9d869bd71e5bbef667e7eb3; permanent Knowledge Architecture push 37963549905/#1553 completed/success on that exact SHA. Neither PR needs another merge. Current/374_S1.42AK_TSDIAG1_POST_RECONCILIATION_HANDOVER_AUTHORITY_REPAIR.md records the repair of the previously stale state navigation; any PR for this repair must itself be exact-final-PR-head CI verified, separately pinned-merged and permanent exact-new-main-head CI verified before the next project segment. THEN AND ONLY AFTER a fresh user continuation, NEXT SEGMENT is a bounded S1.42AK-TSDIAG1 DIAGNOSTIC RUNTIME-ACTIVATION CHECKPOINT ONLY: reverify the frozen unchanged original main-published, canonically indexed Profiles/LC V1 S1.42AK-TS1.r2z (SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e, artifact 11615262607), original DLL/source, index provenance, Windows Gale path safety, selector guards and actual unchanged runtime controller; fail closed and preserve rollback to BMDSFIX1 if any precondition fails. Prepare exact guarded activation/evidence-routing PR and verify its exact final head CI; DO NOT merge that activation PR in the preparation segment. Diagnostic activation is NOT a Gale import, test authorization, game execution, gameplay acceptance or natural Toy Store generation proof. TSDIAG1 remains DIAGNOSTIC ONLY / NEVER ACCEPT; toy_store_tsdiag1_built=false in gameplay-promotion semantics, runtime_armed=false and toy_store_runtime_test_authorized=false until distinct authorized gates; actual Toy Store/ToystoreFlow selection, generation, CullFactory, entrances and traversal unproven. Accepted S1.42AK and active BMDSFIX1 NOT ACCEPTED, with independent passive selector-free Black Mesa x DeepSewersFlow proof still outstanding/unwaived. Phase-C residual 22 = 10 viable/equal-100 plus 12 owner-hard-block. BuildSpecs/current.json disabled/IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS; RuntimeInbox/ACTIVE_BUILD.txt S1.42AK-BMDSFIX1. No rebuild, recompilation, new profile/repack, republish, reindex, Gale, runtime test, evidence ingest, runtime activation or incident acceptance during this handover repair.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
