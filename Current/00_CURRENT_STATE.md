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
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-TSDIAG1`

## Exact next action

S1.42AK-TSDIAG1 exact-original-byte diagnostic activation is PR-STAGED ONLY, NOT main-merged, Gale-imported, locally activated or runtime-tested. PR branch atomically sets active runtime file, machine runtime controller, diagnostic_revision and three activation/test/checkpoint flags to exact published/indexed S1.42AK-TSDIAG1 / profile Profiles/LC V1 S1.42AK-TS1.r2z SHA256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e / DLL SHA256 fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201 / BMDSFIX1 parent 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0; record Current/391_S1.42AK_TSDIAG1_RUNTIME_ACTIVATION.md. Require actual active-stage exact-final-PR-head Knowledge Architecture and TSDIAG1 original-byte publication CI, all 24 negative mutations and independent frozen SCDIAG1/FXDIAG1 source/proof. A synthetic active fixture is not enough. Original frozen artifact 11615262607, 915-byte PREVALIDATION distinct from DERIVED_RUNTIME_BUILD_RESULT, canonical index/profile/DLL/parent unchanged. FAIL CLOSED if any required CI fails: do not merge/import/activate/test. If successful, NEXT separately user-gated pinned PR merge and permanent exact-main-head Knowledge Architecture push; no local runtime test authorized by this checkpoint. S1.42AK ACCEPTED; BMDSFIX1 gameplay candidate NOT ACCEPTED, passive selector-free Black Mesa x DeepSewersFlow gate outstanding; TSDIAG1 DIAGNOSTIC ONLY / NEVER ACCEPT with Toy Store generation/traversal unproven; residual 22=10+12. BuildSpecs/current.json disabled/IDLE; reference Gale budget 216/255 does not prove user's actual Windows path.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
