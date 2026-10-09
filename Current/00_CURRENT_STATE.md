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

S1.42AK-TSDIAG1 NEXT SEPARATELY USER-GATED SEGMENT: integrate the pending TSDIAG1 post-index lifecycle-reconciliation PR only after exact-final-PR-head CI PASS, with pinned expected_head_sha, and verify permanent Knowledge Architecture push CI on the exact resulting main head. Do not repeat the already completed mapping/indexing. Original profile Profiles/LC V1 S1.42AK-TS1.r2z SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e is MAIN-PUBLISHED and CANONICALLY INDEXED: mapping PR #402 merged to main 4e8f5b421bcf80b95d23687b821a415ba8ed8d43; permanent Knowledge Architecture push 37957212392/#1544 success; automatic profile-index run 37957212854/#60 success; sole index bot commit 3e183c4be3c5831e62e4827192bdac4a9751be71 added only ProfileSources/S1.42AK-TSDIAG1/PROFILE_INDEX_RESULT.json; exact bot-head Knowledge Architecture workflow_dispatch 37957255828/#1545 success on that SHA. Result resolution EXPECTED_HASHES, 338 ZIP/snapshot entries, 331 text entries. Original frozen artifact ID 11615262607 and profile/DLL/ZIP hashes remain unchanged; old 37943625888/#59 missing-mapping failure is superseded historical fail-closed evidence. This reconciliation is documentation/state only, NOT runtime authorization. TSDIAG1 remains DIAGNOSTIC ONLY / NEVER ACCEPT, built=false as gameplay candidate, Gale-imported=false, runtime_armed=false, Toy Store/ToystoreFlow generation/CullFactory/entrance/traversal proof absent. Accepted S1.42AK, active BMDSFIX1 NOT ACCEPTED with its independent passive selector-free Black Mesa x DeepSewersFlow proof outstanding/unwaived. Phase-C residual 22=10 viable/equal-100 +12 owner-hard-block. BuildSpecs/current.json disabled/IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS and RuntimeInbox/ACTIVE_BUILD.txt S1.42AK-BMDSFIX1 unchanged. After reconciliation integration, only a new independently user-authorized diagnostic runtime-activation authorization decision/checkpoint may follow; no build, new profile, Gale import, runtime test, gameplay acceptance or unrelated incident work.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
