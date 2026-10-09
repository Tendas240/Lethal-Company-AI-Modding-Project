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
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AK-SCDIAG1`

## Exact next action

Confirm the S1.42AK-SCDIAG1 post-activation lifecycle-navigation reconciliation is merged to main and permanent Knowledge Architecture push CI is completed/success on the exact main HEAD; if this reconciliation is still PR-staged, first integrate that PR with a pinned expected head SHA in its own separately bounded segment and verify exact-new-main-head push CI. Only after this gate, execute a separately user-gated S1.42AK-SCDIAG1 Runtime-Test Preparation / User Instructions segment. Activation PR #386 exact head 3675f9e0ae476ddfbaa5b0f14527f840e1d11b81 was merged as c689b7eca5c53f26c603943328defaab2b1b3a50 with permanent Knowledge Architecture push 37908458494/#1498 completed/success. Runtime controller S1.42AK-SCDIAG1 is armed for exactly ONE user-run Offense Storage Complex / StorageComplex diagnostic attempt, NOT gameplay acceptance. Before the user's attempt, reverify the exact already-published/indexed LC V1 S1.42AK-SCD1.r2z SHA-256 6be6865a7fde205280439503680ac910401c20b997f757ffbedbddc963c704f4, original byte/parent/provenance/LLL/normalizer/fail-closed safeguards, Gale v2.4.6 exact one-hop replacement/import and Windows path budget. Provide the exact repository-native Gale replacement/import command and a self-contained build-specific single-line PowerShell LogOutput.log uploader; instruct exactly one Offense attempt, no reroll even after refusal, wrong floor or failure, followed by raw log upload and separately gated evidence ingest/reconciliation. Do not yourself Gale-import, launch the game, perform a runtime test, upload/ingest logs, rebuild, compile, republish, alter owner/LLL/normalizer/RNG, or accept the diagnostic. Preserve accepted S1.42AK; BMDSFIX1 gameplay candidate NOT ACCEPTED with independent passive selector-free Black Mesa x DeepSewersFlow proof unwaived; residual Phase C 23=11 viable/equal-100+12 owner-hard-block; disabled/IDLE BuildSpecs/current.json. Actual StorageComplex generation, CullFactory materialization and observed PathfindingLib entrances remain unproven.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
