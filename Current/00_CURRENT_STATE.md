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

S1.42AK-TSDIAG1 diagnostic runtime activation is FAIL-CLOSED at this PR-local checkpoint: original published profile/parent, DERIVED_RUNTIME_BUILD_RESULT and canonical index pass, but cross-diagnostic stage-aware CI preconditions do not. Current SCDIAG1 source validator and workflow are bound to BMDSFIX1 when SCDIAG1 is inactive; FXDIAG1 source workflow recognizes only BMDSFIX1 or active SCDIAG1; and TSDIAG1 publication-stage validator hard-requires runtime_armed=false and BMDSFIX1 ACTIVE_BUILD. An activation switch would invalidate required pull_request CI. This checkpoint changes DOCUMENTATION/NAVIGATION ONLY, preserving BuildSpecs/current.json disabled/IDLE, RuntimeInbox/ACTIVE_BUILD.txt and controllers.runtime_active_build=S1.42AK-BMDSFIX1, inactive SCDIAG1 diagnostic_revision, TSDIAG1 armed=false/test_authorized=false, immutable frozen original bytes and DERIVED metadata. Exact independent main-profile SHA-256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e and BMDSFIX1 parent 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0 match; original artifact 11615262607 remains available. After separately merging and exact-new-main CI of this documentation PR, NEXT USER-GATED SEGMENT: a narrowly bounded cross-diagnostic source/publication CI lifecycle-boundary remediation decision/preflight with strict original/source/rollback pinning and negative CI mutations; no activation or runtime change until later remediation is separately implemented/integrated and independently CI verified. Reference-root Gale path 216/255 is not the user's Windows root proof. S1.42AK accepted, BMDSFIX1 NOT ACCEPTED, passive selector-free DeepSewersFlow proof still outstanding; residual 22 (10 viable + 12 owner-hard-block), Toy Store generation/materialization unproven, TSDIAG1 NEVER ACCEPT. No rebuild, repack, publish/index, Gale import, runtime test or log ingest.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
