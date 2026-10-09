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

S1.42AK-TSDIAG1 cross-diagnostic CI LIFECYCLE DECISION IS MAIN-MERGED: PR #415 exact final reviewed head 5ea8b37b304a904f89cf6a0db779b94457ab7c81 merged with pinned expected SHA to main 478643a81203689ddd97e3e121945d7934be962b; permanent Knowledge Architecture push 37980944532/#1573 event=push completed/success on exact main SHA. Current/381 conditional-positive design decision is therefore no longer PR-STAGED. Current/382 documents the POST-MERGE LIFECYCLE RECONCILIATION; this new reconciliation is PR-STAGED pending its own exact-final-PR-head CI and a LATER, SEPARATELY USER-GATED pinned merge/permanent exact-new-main push CI. Only after those gates may a separate tightly scoped SCDIAG1/FXDIAG1 source-trigger and TSDIAG1 original-byte publication-stage CI REPAIR PR be prepared, with source/proof freeze and state-neutral immutable evidence protection, exact head + negative-mutation regressions, independent later pinned merge and renewed activation preflight. The repair is NOT implemented and TSDIAG1 activation remains FAIL-CLOSED under Current/380; frozen TS1 original profile d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e, original artifact 11615262607, indexed DLL fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201 and transparently DERIVED runtime metadata unchanged. Controllers build disabled/IDLE, runtime BMDSFIX1 in both file and machine, completed SCDIAG1 inactive diagnostic_revision, TS runtime_armed=false/test_authorized=false. S1.42AK accepted, BMDSFIX1 NOT ACCEPTED with passive selector-free Black Mesa x DeepSewersFlow proof still outstanding/unwaived; Phase C residual 22 (10 viable/equal 100 + 12 owner-hard-block), Toy Store actual generation/materialization not proven; TS1 DIAGNOSTIC ONLY / NEVER ACCEPT. Reference-root Gale 216/255 is not local Windows-root proof. No source implementation, build/recompile/repack, publication/index, Gale import, runtime activation/test, evidence ingest or gameplay acceptance.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
