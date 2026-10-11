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

S1.42AK-TSDIAG1 original-byte publication CI self-test lifecycle-neutral repair PR #421 is MAIN-MERGED, EXACT-HEAD CI VERIFIED. Final reviewed PR head 19a236d31d6c63e556b0d3ce18f36f7784cdec3f passed Knowledge Architecture pull_request 38053024714/#1585 and TSDIAG1 original-byte publication lifecycle pull_request 38053024724/#24 (both completed/success, exact head). Pinned merge method=merge, expected_head_sha=19a236d31d6c63e556b0d3ce18f36f7784cdec3f produced main 016a660802f3c1dabccc08b03918f7eb497005e2; verified parents 510a270e2e434c7ffca6e4146cd8b8e027d5edd1 and 19a236d31d6c63e556b0d3ce18f36f7784cdec3f. Permanent Knowledge Architecture push 38142366937/#1586 completed/success event=push, head_sha exactly 016a660802f3c1dabccc08b03918f7eb497005e2. The repaired validator now separates actual live-stage check_lifecycle_route() from independent synthetic inactive/active fixtures and retains 24 negative mutations, mixed-state rejection, exact original profile/DLL/parent/index/ZIP bytes and original 915-byte prevalidation distinct from DERIVED_RUNTIME_BUILD_RESULT; frozen SCDIAG1/FXDIAG1 source/proof pins remain mandatory. Historical Current/384 and Current/385 self-test-unrepaired text is superseded for the CURRENT stage by Current/386_S1.42AK_TSDIAG1_SELFTEST_REPAIR_POST_MERGE_LIFECYCLE_RECONCILIATION.md, PR-STAGED documentation in this reconciliation only. CURRENT NEXT SEPARATELY USER-GATED: once this reconciliation PR is verified on its exact final head, merge only that PR with pinned expected_head_sha and verify permanent exact-new-main Knowledge Architecture push CI. Only AFTER that separate merge may another independently gated FRESH TSDIAG1 runtime-activation preflight assess whether a separately versioned activation PR can be authorized; no automatic activation, new build, re-archive, index, Gale import or runtime test. Accepted S1.42AK; BMDSFIX1 active NOT ACCEPTED with passive selector-free Black Mesa x DeepSewersFlow gate still outstanding/unwaived; BuildSpecs/current.json disabled/IDLE, runtime active BMDSFIX1, TSDIAG1 runtime_armed=false/test_authorized=false/activation_checkpoint_executed=false, DIAGNOSTIC ONLY / NEVER ACCEPT; no Toy Store generation/materialization/traversal proof; Phase-C residual 22=10 viable/equal-100+12 owner-hard-block. Gale Windows reference-root 216/255 does not prove actual user installation path.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
