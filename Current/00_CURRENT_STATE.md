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

Perform one separately bounded S1.42AK-FXDIAG1 canonical profile-index mapping/reconciliation ONLY. Publication PR #362 exact final head 492deeb52e0e2455653b2856752ccb8d79daf314 passed 9/9 required pull_request CI gates, merged into main as 375906b54d454ec717e08e1e4368d4c863582ef9, and permanent exact-merge-head Knowledge Architecture push run 37825301919/#1423 succeeded. Automatic profile-index push run 37825301824/#55 failed closed solely because Profiles/LC V1 S1.42AK-FXD1.r2z has no canonical build mapping in Profiles/EXPECTED_HASHES.json or Current/BUILD_LINEAGE.json; it created no index result. Using only exact frozen published profile SHA-256 b2491e10811310661de76b71e7bf42cf259065e4b363e36d18abfa8457a14435, add the narrow canonical EXPECTED_HASHES mapping for build S1.42AK-FXDIAG1, integrate it only after exact-PR-head CI, allow the existing profile-index workflow to produce ProfileSources/S1.42AK-FXDIAG1/PROFILE_INDEX_RESULT.json, and verify permanent exact-main and bot-head CI. Do not rebuild/reconstruct/replace bytes, Gale-import, runtime-arm/run/test or accept FXDIAG1 or BMDSFIX1; do not alter BuildSpecs/current.json, RuntimeInbox/ACTIVE_BUILD.txt, gameplay/config/LLL/owner/availability or other profiles. Preserve S1.42AK accepted, BMDSFIX1 active NOT ACCEPTED with passive selector-free Black Mesa x DeepSewersFlow gate outstanding/unwaived, Phase-C residual 24=12 viable/equal-100+12 owner-hard-block, and all completed/deferred scopes.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
