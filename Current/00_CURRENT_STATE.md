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

S1.42AK-TSDIAG1 diagnostic runtime-activation CHECKPOINT PRECHECK FAIL-CLOSED: the original main-published, canonically indexed profile Profiles/LC V1 S1.42AK-TS1.r2z (SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e; sole frozen artifact 11615262607) was independently rehashed on exact main and matched; exact DLL/normalizer and unique index mapping are preserved. However the Gale v2.4.6 explicit diagnostic resolver requires a repository-native build_result with exact output/base profile SHA and BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/BUILD_RESULT.json does not exist on main, while the frozen TSDIAG1 source-static workflow triggers on Current/CURRENT_STATE.json and its validator hard-requires BMDSFIX1 ACTIVE_BUILD/runtime controller and runtime_armed=false. The frozen review guard also watches BuildSpecs/S1.42AK-TSDIAG1_BUILD_EVIDENCE/** and hard-requires runtime_armed=false. These are stage-boundary preconditions to resolve separately; NEVER bypass validation or invent frozen build metadata. No activation/evidence-routing PR is safe until a separately user-gated exact-original-metadata and lifecycle-aware CI/guard boundary preflight is resolved and main-verified. Record Current/375_S1.42AK_TSDIAG1_RUNTIME_ACTIVATION_CHECKPOINT_FAIL_CLOSED.md; do not merge any pending preflight PR automatically. Keep BuildSpecs/current.json disabled/IDLE and RuntimeInbox/ACTIVE_BUILD.txt and CURRENT_STATE.controllers.runtime_active_build both S1.42AK-BMDSFIX1; toy_store_tsdiag1_runtime_armed=false; toy_store_runtime_test_authorized=false; TSDIAG1 DIAGNOSTIC ONLY / NEVER ACCEPT. The 216/255 Windows Gale path check covers only the canonical reference root and NOT the unknown actual user Gale root. No Gale import, runtime test, game execution, build, recompilation, new profile, republication, reindex or gameplay acceptance. S1.42AK accepted, BMDSFIX1 NOT ACCEPTED and its independent passive selector-free DeepSewersFlow proof unwaived; residual 22=10 viable/equal-100 plus 12 owner-hard-block. NEXT separately user-gated step after this documentation PR's pinned merge/permanent main CI: bounded frozen-original BUILD_RESULT provenance and source/review stage-aware CI preflight; only thereafter a new runtime-activation checkpoint.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
