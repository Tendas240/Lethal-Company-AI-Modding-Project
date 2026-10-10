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

S1.42AK-TSDIAG1 activation CI self-test FAIL-CLOSED checkpoint PR #419 is MAIN-MERGED AND PERMANENT EXACT-MAIN-HEAD CI VERIFIED. PR #419 reviewed final head 97803cde36bd6df9666b89790809afb919e03749 passed exact pull_request gates Knowledge Architecture 38003865211/#1581 and TSDIAG1 original-byte publication lifecycle 38003865164/#22; merged with pinned expected_head_sha to exact main f92ecaa78d9599608c7d3a513886649f8c50dbde, parents previous main ee6e76b955c4bd9c089789eee77132b7cd16f588 and reviewed PR head, permanent Knowledge Architecture push 38008784760/#1582 event=push completed/success with head_sha exactly f92ecaa78d9599608c7d3a513886649f8c50dbde. Current/384 PR-STAGED wording is original-stage historical, superseded by Current/385 post-merge handover reconciliation. CURRENT NEXT SEPARATELY USER-GATED TASK: prepare a narrow stage-neutral TSDIAG1 publication self-test CI validator repair PR, preserving the real current-state original-byte validation, frozen profile/parent/index/DLL hashes, distinct DERIVED metadata versus original 915-byte prevalidation, cross-diagnostic source/closed-proof guard and all 24 synthetic negative mutations. Root defect: AnalysisTools/validate_s142ak_tsdiag1_publication.py route_self_test uses hardcoded active='S1.42AK-BMDSFIX1' and insists on the current live state being inactive, so an otherwise coherent active TSDIAG1 PR necessarily fails the mandatory --self-test. The actual self-test repair is NOT IMPLEMENTED, no activation PR is authorized before separate exact-final-PR-head green CI, later pinned integration/new-main push CI and a fresh activation preflight. No runtime activation/test, build, profile repack/publication/indexing, Gale import or gameplay acceptance. Accepted S1.42AK; BMDSFIX1 active NOT ACCEPTED with independent selector-free passive Black Mesa x DeepSewersFlow proof outstanding/unwaived, current build disabled/IDLE, TSDIAG1 inactive/NEVER ACCEPT, no Toy Store generation/traversal proof, residual 22 = 10 viable/equal-100 + 12 owner-hard-block. Reference Gale path budget 216/255 is not actual user Windows path proof.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
