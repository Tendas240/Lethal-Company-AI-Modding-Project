<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-10-12  
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

NEXT SEPARATE BOUNDED PROJECT GATE: S1.42AK Phase-C Crimson Keep / CrimsonKeep (Offense, Custom C1 #21, Lead Interiors v0.0.7, owner asset leadinteriors:crimsonkeep, OWNER_ASSET_MATCHING_NO_DIRECT_LLL_CONFIG) source/config/existing-evidence-only generation-proof acquisition and deterministic-selector reuse PREFLIGHT as selected in Current/395. Priority decision PR #431 is main-integrated (exact reviewed head 294bf4ec14fcc8e26014d077e96f08c369acd9b6; pinned merge main 9c8e214909df48361b3b44a80f869e5c11f041b9; Knowledge Architecture push #1611 success) and its post-merge current authority reconciliation PR #432 is also main-integrated (exact reviewed head b0d3c2ef416c3dc3744a655c80c0c695e845897d; pinned merge main c26460c8df55edeff734623a5b229f36c857ae47; Knowledge Architecture push #1613/run 38231253768 completed/success on that head). Treat staged/merge-next wording in historical Current/395 and Current/396 as their stage-specific evidence, NOT current instructions to rerun CI or remerge those PRs. The preflight must verify exact registered Custom owner/asset/flow, original already-viable unique reference-equal rarity-100 wrapper and Offense owner matching, normal-stack LLL/day-history selection and generator/CullFactory/PathfindingLib proof observability, and possible fail-closed same-wrapper after-normalizer diagnostic-selector reuse; report independently any blockers and whether instrumentation would be needed. Do not assume Crimson Keep actual generation, materialization or traversal; do not approve a new diagnostic identity, selector implementation, owner-bypass, build, profile/index/publication, Gale import, runtime activation/test, acceptance or unrelated work. Residual proof gap stays 21 = 9 viable/equal-100 + 12 C2 owner-hard-block; Toy Store original-byte TSDIAG1 diagnostic-generated PASS is complete/inactive, 1/1 consumed, NEVER ACCEPT and cannot be rerun. S1.42AK remains ACCEPTED; S1.42AK-BMDSFIX1 active/NOT ACCEPTED with the distinct passive, unwaived selector-free Black Mesa x DeepSewersFlow proof outstanding. Build controller disabled/IDLE and runtime evidence pointer S1.42AK-BMDSFIX1. Runtime testing is NOT authorized by runtime_test_outstanding=true.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
