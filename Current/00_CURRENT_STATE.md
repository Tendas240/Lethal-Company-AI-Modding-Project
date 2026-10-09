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

S1.42AK-TSDIAG1 NEXT SEPARATELY USER-GATED PROJECT GATE, ONLY AFTER THIS HANDOVER AUTHORITY REPAIR PR IS MAIN-INTEGRATED AND PERMANENT EXACT-MAIN-HEAD PUSH CI IS GREEN: diagnostic runtime-activation AUTHORIZATION DECISION ONLY for the already-main-published, canonically indexed, frozen original profile Profiles/LC V1 S1.42AK-TS1.r2z (SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e). Decide whether a later separately bounded runtime-activation checkpoint may be authorized; do not activate, import into Gale, build, index again, run a runtime test or accept gameplay during this decision. PR #403 post-index lifecycle reconciliation exact final PR head 35f8ccc2fae2a32d37f8e40d896e864ab7844b0b passed 5/5 pull_request CI and merged with pinned expected head to main 925a35bda8095e3521fb3164721f765084eb2533; permanent Knowledge Architecture push 37958503044/#1547 completed/success at exactly that main SHA. Mapping PR #402 pinned merge 4e8f5b421bcf80b95d23687b821a415ba8ed8d43, auto index 37957212854/#60, bot-only index result commit 3e183c4be3c5831e62e4827192bdac4a9751be71, exact bot-head Knowledge Architecture workflow_dispatch 37957255828/#1545 all successful. ProfileSources/S1.42AK-TSDIAG1/PROFILE_INDEX_RESULT.json matches original SHA, EXPECTED_HASHES, 338 ZIP/snapshot entries and 331 text entries. Frozen artifact ID 11615262607; NO replacement/rebuild. Historical missing-mapping failure 37943625888/#59 and older PR-staged instructions are superseded only as live next-action guidance, not erased. TSDIAG1 DIAGNOSTIC ONLY / NEVER ACCEPT, toy_store_tsdiag1_built=false, runtime_armed=false, toy_store_runtime_test_authorized=false; actual Toy Store generation/CullFactory materialization/entrance/traversal unproven. Accepted S1.42AK; active BMDSFIX1 NOT ACCEPTED with independent passive selector-free Black Mesa x DeepSewersFlow proof still outstanding/unwaived; residual 22 = 10 viable/equal-100 + 12 owner-hard-block. BuildSpecs/current.json remains disabled / IDLE_UNIVERSAL_INTERIOR_VIABILITY_ANALYSIS; RuntimeInbox/ACTIVE_BUILD.txt stays S1.42AK-BMDSFIX1. No unrelated incident or acceptance changes.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
