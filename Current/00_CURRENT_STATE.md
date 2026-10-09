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

S1.42AK-TSDIAG1 NEXT SEPARATELY USER-GATED SEGMENT: canonical profile-index mapping checkpoint for the already-main-published original diagnostic profile; first freshly verify main, canonical registry/lineage schema and original profile SHA, then prepare a narrowly scoped mapping PR with exact-final-PR-head CI and STOP before merge. Do not perform profile indexing in this checkpoint. PR #400 S1.42AK-TSDIAG1 publication post-merge lifecycle reconciliation final PR head 828dd2fd8db8986ca747bb79e2f052eda4c01e71 passed 5/5 exact pull_request-head CI, was merged to main 8fb1c9f217c1eb3818d99395620b925e4a2fe203; permanent Knowledge Architecture push run 37946167007/#1540 completed/success on exactly that main SHA. The outdated prior instruction to integrate PR #400 is historical only. Original exact profile on main: Profiles/LC V1 S1.42AK-TS1.r2z, SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e, diagnostic build ID S1.42AK-TSDIAG1. Exclusive frozen Actions artifact ID 11615262607, ZIP SHA-256 010b84c1ffaea1d5cda2e14cdb9580c049da2cd1790e929491e44d13e2c4f39f, embedded diagnostic DLL SHA-256 fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201. Published original-byte PR #399 merged main f2f3f5e3dd330befeef8187640a40157c6470b5c with permanent Knowledge Architecture #1537 success. No new build, no substituted bytes. Automatic profile-index run 37943625888/#59 failed closed specifically because Profiles/EXPECTED_HASHES.json and Current/BUILD_LINEAGE.json lack a canonical TSDIAG1 mapping; no ProfileSources/S1.42AK-TSDIAG1/PROFILE_INDEX_RESULT.json exists and toy_store_tsdiag1_profile_indexed remains false. Mapping authorization/integration and subsequent bot profile index/result/its exact-head CI are independent future gates. No canonical mapping was added during lifecycle reconciliation or handover. TSDIAG1 remains DIAGNOSTIC ONLY / NEVER ACCEPT, runtime_armed=false, no trusted Toy Store / ToystoreFlow actual generation, CullFactory materialization, entrance or traversal proof. Gameplay accepted baseline S1.42AK; active BMDSFIX1 is NOT ACCEPTED with independent selector-free passive Black Mesa x DeepSewersFlow evidence still outstanding and unwaived. Residual 22 = 10 viable/equal-100 + 12 owner-hard-block. BuildSpecs/current.json remains disabled / IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS and RuntimeInbox/ACTIVE_BUILD.txt remains S1.42AK-BMDSFIX1. No new build, Gale import, activation, runtime test, gameplay acceptance or unrelated incident change.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
