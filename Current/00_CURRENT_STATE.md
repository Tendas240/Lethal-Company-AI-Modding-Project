<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-10-08  
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

After the S1.42AK-FXDIAG1 exact-byte publication-authorization post-merge state/handover reconciliation has passed exact-final-PR-head CI, merged to main, and permanent exact-main-head Knowledge Architecture push CI is successful, perform ONE separately bounded S1.42AK-FXDIAG1 Exact-Byte Publication Checkpoint under Current/333_S1.42AK_FXDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_DECISION.md and Current/334_S1.42AK_FXDIAG1_EXACT_BYTE_PUBLICATION_AUTHORIZATION_POST_MERGE_RECONCILIATION.md. Transport/materialize ONLY the independently rehashed frozen GitHub Actions artifact ID 11561251337 (ZIP SHA-256 2805967a866ad8d88c4d80221c5bbd354a1a59adeaf1d7decfaa634d725c4b89; profile b2491e10811310661de76b71e7bf42cf259065e4b363e36d18abfa8457a14435; DLL 322774f531f87dc9b253e712e63d69ed39fb998017af75b6545cdc904d0b7705) after freshly retrieving by EXACT artifact ID, independently rehashing all three and enforcing exact immutable BMDSFIX1 parent (3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0), one-DLL plus export.r2x-only 337-to-338 member delta, inherited hashes and 255-character Gale path limit. Fail closed on any mismatch; never rebuild, construct replacement profile/DLL/archive, select newest artifact, canonically index ProfileSources or EXPECTED_HASHES, Gale-import, activate, run/test, accept FXDIAG1/BMDSFIX1, change controllers/gameplay/availability/owner rules, waive the passive selector-free BMDSFIX1 DeepSewersFlow gate, modify Phase-C residual 24=12 viable/equal-100 + 12 owner-hard-block or reopen completed/deferred scopes. Publication only: later index mapping/runtime decisions remain separate.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
