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

S1.42AK-TSDIAG1 NEXT SEPARATELY USER-GATED SEGMENT: integrate post-publication lifecycle-reconciliation PR only after exact-final-PR-head CI with pinned expected_head_sha and verify permanent exact-resulting-main-head Knowledge Architecture push. PR #399 exact final head 2c0eb2aa5b1a71fca4f16d302ad2ca6d5ee52223 had 2/2 pull_request CI success; merged with pinned expected head to main f2f3f5e3dd330befeef8187640a40157c6470b5c; permanent Knowledge Architecture push 37943625924/#1537 completed/success on same main head. The original frozen TSDIAG1 profile Profiles/LC V1 S1.42AK-TS1.r2z is now MAIN-PUBLISHED byte-identical to sole Actions artifact 11615262607 (review producer 37929246619/#2 head 24105017a0d98ccc05b878c809f84f93f4e87e37): profile SHA256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e, DLL SHA256 fff3b148fca3bc0bf6c175f38060a432a2992e7d6de4121df9a2556bb82ca201, ZIP SHA256 010b84c1ffaea1d5cda2e14cdb9580c049da2cd1790e929491e44d13e2c4f39f; exact 337->338 + export.r2x-name-only byte delta and 216/255 Gale reference-root guard PASS. Static snapshots 338 entries/331 readable. Auto-index push 37943625888/#59 failed closed intentionally because Profiles/EXPECTED_HASHES.json and Current/BUILD_LINEAGE.json have no canonical TS1 mapping; no PROFILE_INDEX_RESULT exists. This is correct guard behavior, not corrupt bytes, not a successful canonical index. Only AFTER the reconciliation PR is separately main-integrated/CI-verified is the later distinct TSDIAG1 canonical profile-index mapping authorization/checkpoint next: exact build ID S1.42AK-TSDIAG1, profile SHA256 d6bf5e5c185945e6aad85ec0dc1c4cda5628ff7d9335b93f53f7097c5a19b57e; do not add mapping/index in reconciliation. TSDIAG1 DIAGNOSTIC ONLY / NEVER ACCEPT, runtime_armed=false, no actual Toy Store generation/CullFactory/entrance/traversal proof. Accepted S1.42AK, BMDSFIX1 active NOT ACCEPTED and independent passive selector-free Black Mesa x DeepSewersFlow proof unwaived. Phase C residual 22=10 viable/equal100+12 owner-hard-block. BuildSpecs/current.json remains disabled/IDLE, RuntimeInbox/ACTIVE_BUILD.txt remains BMDSFIX1. No new build, profile recompile, replacement archive, canonical index, Gale import, runtime authorization/activation/test, gameplay acceptance or unrelated incident changes.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
