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

Perform only the separately authorized S1.42AK-SCDIAG1 Exact-Byte Publication Checkpoint: retrieve ORIGINAL Actions artifact ID 11581745624 (producer head 3e1680298b794d392a6938c9b734ecb649b2eea1) by exact ID, independently rehash its outer ZIP SHA-256 9971c22f162ef61177b57f2e350bba5289f5fa09dd78cff65ccd82fcadb0d730, nested LC V1 S1.42AK-SCD1 profile SHA-256 6be6865a7fde205280439503680ac910401c20b997f757ffbedbddc963c704f4 and S142AKSCDiag1 DLL SHA-256 2bd49852973c04c89dceea5b8dc9e75b051bc9a95c16850af08fb37dc3113131. Require CRC, 337-to-338 one-added-DLL/export.r2x-only diff, immutable BMDSFIX1 parent SHA-256 3f9c7fd5c21c532528db1ddae36764ada73236b7527c6ab2ae1b982c3976b7b0 and unchanged inherited DLL hashes, plugin identity and Windows 255-character path-budget guard. Only if all fail-closed provenance checks succeed, transport/materialize exact original profile bytes and permitted readable static/provenance snapshots in a bounded publication PR, requiring exact-PR-head CI and later separate main integration/permanent exact-main-head push CI. NEVER recompile, rebuild, reconstruct, substitute, overwrite unrelated files, canonically map/index Profiles/EXPECTED_HASHES or PROFILE_INDEX_RESULT, Gale-import, activate, run/test, accept gameplay, or change source, build/runtime controllers, owner/LLL/normalizer/RNG. Preserve DIAGNOSTIC ONLY / NEVER ACCEPT; S1.42AK accepted, BMDSFIX1 active NOT ACCEPTED with passive selector-free Black Mesa x DeepSewersFlow gate unwaived; StorageComplex generation unproven and Phase-C residual 23 = 11 viable/equal-100 plus 12 unchanged owner-hard-block.

A runtime test is pending for S1.42AK-BMDSFIX1. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
