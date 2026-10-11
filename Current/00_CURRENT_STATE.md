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

S1.42AK-TSDIAG1 post-#424 lifecycle reconciliation PR #425 is MAIN-MERGED and exact-main-head CI VERIFIED. Exact final PR head f3a3d2f3e3649ffcf781b62d7355a45b13bc24b5 passed Knowledge Architecture pull_request 38146354505/#1593 and TSDIAG1 original-byte publication pull_request 38146354536/#28, both completed/success; pinned merge produced main 6ed8a4b6ef40da2199795d62600cd7389f89d26e, parents 353d374710b43b24d8693c7a8b3f8a3433fe92e2 and f3a3d2f3e3649ffcf781b62d7355a45b13bc24b5. Permanent Knowledge Architecture push 38147712227/#1594 event=push completed/success exact main. Prior Current/389 PR-STAGED text is historical stage evidence, NOT current merge authority; Current/390_S1.42AK_TSDIAG1_POST_425_HANDOVER_AUTHORITY_CORRECTION.md reconciles present navigation. NEXT user-gated: prepare one distinct original-byte S1.42AK-TSDIAG1 DIAGNOSTIC activation PR (DO NOT MERGE in its preparation segment), with coherent exact original-profile runtime/controller/diagnostic attribution and flags, actual active-route exact-final-PR-head CI, all 24 fail-closed negative mutations, independent frozen SCDIAG1/FXDIAG1 proof, immutable original profile/index/DLL/parent/ZIP, original 915-byte PREVALIDATION distinct from DERIVED_RUNTIME_BUILD_RESULT. Synthetic active fixtures do not prove real active CI or Toy Store materialization/traversal. S1.42AK ACCEPTED, BMDSFIX1 active NOT ACCEPTED; independent passive selector-free Black Mesa x DeepSewersFlow proof outstanding. Runtime file and state remain BMDSFIX1, TSDIAG1 all activation flags false, DIAGNOSTIC ONLY/NEVER ACCEPT, BuildSpecs/current.json disabled/IDLE, residual 22=10+12. No build, repack, index, Gale import, runtime activation/test or gameplay acceptance; reference-root Gale 216/255 is not actual user Windows path.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
