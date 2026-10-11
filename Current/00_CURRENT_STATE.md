<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-10-11  
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

S1.42AK-TSDIAG1 original-byte publication CI self-test repair PR #421 and its post-merge lifecycle reconciliation PR #422 are BOTH MAIN-MERGED and exact-main CI VERIFIED. PR #422 exact reviewed final head c1ce1f899d5db609cb27492e6284a1c3437ac0bb passed Knowledge Architecture pull_request 38142810051/#1587 and TSDIAG1 original-byte publication lifecycle pull_request 38142809950/#25 (both completed/success, matching final head); pinned merge_method=merge expected_head_sha=c1ce1f899d5db609cb27492e6284a1c3437ac0bb produced main c32011bec90bd01972481daa8765a5a23df8a47c, parents 016a660802f3c1dabccc08b03918f7eb497005e2 and c1ce1f899d5db609cb27492e6284a1c3437ac0bb. Permanent Knowledge Architecture push 38143463797/#1588 event=push completed/success head_sha exactly c32011bec90bd01972481daa8765a5a23df8a47c. Earlier Current/386 PR-STAGED wording is immutable stage history, not the present merge status; Current/387_S1.42AK_TSDIAG1_POST_422_HANDOVER_AUTHORITY_CORRECTION.md reconciles that history. CURRENT NEXT SEPARATELY USER-GATED PROJECT TASK: conduct a FRESH bounded S1.42AK-TSDIAG1 runtime-activation authorization PRE-FLIGHT against current original-byte published/indexed profile, original DLL/parent/ZIP index and distinct DERIVED_RUNTIME_BUILD_RESULT vs original 915-byte prevalidation; require real inactive/active route validity, negative mutation and frozen SCDIAG1/FXDIAG1 source/proof guards, actual runtime controller consistency and all relevant safety contracts. Decide and document whether a future distinct diagnostic-only activation PR is authorized. Do NOT prepare or execute a runtime activation PR automatically in the preflight segment, and do not re-run a previously authorized activation attempt. This reconciliation is not activation authorization and does not establish active-stage CI PASS or Toy Store generation/traversal proof. Accepted S1.42AK; active S1.42AK-BMDSFIX1 NOT ACCEPTED with separate passive selector-free Black Mesa x DeepSewersFlow proof outstanding/unwaived; BuildSpecs/current.json disabled/IDLE; RuntimeInbox/ACTIVE_BUILD.txt and state runtime pointer S1.42AK-BMDSFIX1; TSDIAG1 runtime_armed=false, runtime_test_authorized=false, activation_checkpoint_executed=false, DIAGNOSTIC ONLY/NEVER ACCEPT; Phase-C residual 22=10 viable/equal-100+12 owner-hard-block. No build, profile repack/publication/indexing, Gale import, runtime test or gameplay acceptance; Gale 216/255 reference Windows path length is not proof of actual local installation path.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
