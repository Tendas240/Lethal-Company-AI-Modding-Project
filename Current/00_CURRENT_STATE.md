<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# 00 — Current State

**Status:** CURRENT / CANONICAL HUMAN STATE  
**Generated from:** `Current/CURRENT_STATE.json`  
**Updated:** 2026-09-08  
**Game:** Lethal Company V81

## Project execution policy

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`. This controls task segmentation/checkpoints, not gameplay lifecycle state.

## Accepted baseline

**S1.42AF — Path-Length-Safe Microwave Packaging — ACCEPTED FULL NORMAL STACK**

Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`  
Acceptance: `Current/128_S1.42AF_RUNTIME_ACCEPTANCE_PATH_LENGTH_SAFE_MICROWAVE_PACKAGING.md`  
Runtime evidence: `RuntimeEvidence/S1.42AF/20260905T223738Z/`

## Latest built artifact

**S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS EXTENDED PARTIAL RUNTIME PASS FINAL NEIGHBOR REMAINDER OUTSTANDING**

Profile: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z`  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`  
Candidate record: `Current/139_S1.42AH_BUILD_CANDIDATE_MOUTHDOG_DUAL_PREVENTION.md`  

A historical rejection can remain preserved even when a later explicit decision changes the build's live lifecycle status. Current status is controlled by `Current/CURRENT_STATE.json` plus the latest build-specific decision evidence.

## Live execution state

- Active candidate: **S1.42AH**
- Runtime test outstanding: **yes**
- Successor armed: **no**
- `BuildSpecs/current.json`: disabled (`IDLE_AFTER_S1.42AH_BUILD_AWAITING_RUNTIME_VALIDATION`)
- Guarded build base: `Profiles/LC V1 S1.42AH Mouth Dog Fix.r2z` / `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`
- `RuntimeInbox/ACTIVE_BUILD.txt = S1.42AH`

## Exact next action

Run only the final S1.42AH non-Pikmin neighbor remainder: deliberately exercise a MouthDog/Paw collision against a non-Pikmin EnemyAI and prove native Paw-initiated BiteKillEnemyAI / generic non-Pikmin collision behavior remains functional and is not filtered by the Pikmin-only prefix. Then upload the complete fresh S1.42AH LogOutput.log. Do not rebuild S1.42AH or repeat already-proven Pikmin -> MouthDog attack/death/cleanup, adapter protection, Vanilla Pikmin collision blocking, startup, or player-maul coverage. If this final required check passes, explicitly accept S1.42AH; if it fails, explicitly reject S1.42AH and return to an S1.42AF-derived follow-up.

A runtime test is pending for S1.42AH. `RuntimeInbox/ACTIVE_BUILD.txt` controls runtime-evidence attribution and does not itself promote a build.

## Where current truth lives

Use `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md` for execution cadence, `Current/PROJECT_KNOWLEDGE_MAP.md` for semantic routing and `Current/DOCUMENT_AUTHORITY.md` for current-vs-history precedence. Durable gameplay/config invariants live in the relevant `Knowledge/*.md` topic rather than being duplicated here.

Build history is indexed by `Current/BUILD_LINEAGE.md`; artifact and runtime-evidence readability is indexed by `Current/ARTIFACT_EVIDENCE_INTEGRITY.md`.

## Overhaul state

Repository knowledge-architecture status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904`.  
Frozen source commit: `5dbd0e637a480d8591773e422bbca4b0654cad20`.
