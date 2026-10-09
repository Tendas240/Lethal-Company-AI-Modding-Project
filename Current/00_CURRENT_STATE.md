<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-10-10  
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

S1.42AK-TSDIAG1 cross-diagnostic CI REPAIR IS MAIN-INTEGRATED: prior post-decision reconciliation PR #416 exact reviewed head e13cb07ad0a04a803dea403adb20f09a90462db0 merged to main f0bc7b66819972cc766651ee494e59d57c606aa9, permanent Knowledge Architecture push 37994825764/#1575 exact-main completed/success. Cross-diagnostic source/publication CI repair PR #417 exact reviewed final head a78baae9a80298be7000611bf6f7a11b400e4ec8 passed all four exact pull_request gates (Knowledge Architecture 37995792618/#1577, TSDIAG1 publication 37995792685/#20, FXDIAG1 source 37995792573/#93, SCDIAG1 source 37995792568/#60); it was separately merged with pinned expected_head_sha to exact main b2722739ebdf9a54df9fea8483e1874b0a6fd859 and permanent Knowledge Architecture push 37997083695/#1578 event=push completed/success on that exact main. The conditional source/path and original-byte publication lifecycle CI repair is therefore IMPLEMENTED AND MAIN-VERIFIED, not pending; older Current/380/381/382 PR-STAGED or NOT IMPLEMENTED stage descriptions are historical only. Current/383 is the new POST-MERGE LIFECYCLE/HANDOVER RECONCILIATION PR-STAGED, requiring its own exact FINAL PR-head gates and LATER, SEPARATE user-gated pinned merge/new-main push CI. Only AFTER those gates, separately and from fresh canonical evidence, reassess TSDIAG1 diagnostic runtime-activation preflight and decide whether a distinct activation PR can be authorized; no activation is currently executed or authorized by CI repair alone. The frozen original indexed TS1 profile SHA d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e, original DLL SHA fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201, original review artifact 11615262607, independent original 915-byte prevalidation report and DERIVED runtime metadata are unchanged. Build controller disabled/IDLE; RuntimeInbox and machine runtime both S1.42AK-BMDSFIX1; completed SCDIAG1 historical proof disarmed; toy_store_tsdiag1_runtime_armed=false/toy_store_runtime_test_authorized=false. Accepted S1.42AK; active BMDSFIX1 NOT ACCEPTED with independent passive selector-free Black Mesa x DeepSewersFlow proof outstanding/unwaived. Phase-C residual 22 (10 viable/equal-100 + 12 owner-hard-block), actual Toy Store/ToystoreFlow generation/materialization/traversal unproven; TSDIAG1 DIAGNOSTIC ONLY / NEVER ACCEPT. Gale 216/255 is a reference-root path measurement, NOT verified local user installation. No build/recompile/repack, profile publication/index, Gale import, runtime activation/test, evidence ingest or gameplay acceptance.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
