<!-- GENERATED — DO NOT MANUALLY EDIT. Source: Current/CURRENT_STATE.json via RepositoryTools/render_current_navigation.py -->
# Lethal Company AI Modding Project

GitHub is the canonical Source of Truth and build/handover workspace for **Lethal Company V81**.

## Fast takeover

Read, in order:

1. `START_HERE_ChatGPT_Masterprompt.txt`
2. `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
3. `Current/00_CURRENT_STATE.md`
4. `Current/PROJECT_KNOWLEDGE_MAP.md`

Every ChatGPT chat performing project work must follow `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`: execute one bounded segment, report the checkpoint, then stop and wait for explicit user continuation before the next non-final segment. Short atomic work may be one segment.

Then open only the topic/evidence needed for the user's question. Do not read the entire historical repository by default.

Machine-readable live state: `Current/CURRENT_STATE.json`.

Current-chat handover procedure: `Current/HANDOVER_PREPARATION_PROMPT.md`. Handover work is also continuation-gated by `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`.

## Current state

Accepted baseline: **S1.42AF — Path-Length-Safe Microwave Packaging**  
Profile: `Profiles/LC V1 S1.42AF Microwave Fix.r2z`  
SHA-256: `6a82a42bfe010767f4f39aab4d108fa45268407d9658a3e2410162cf9f6f47d0`

Latest built artifact: **S1.42AH — Mouth Dog Pikmin Dual Prevention — BUILD PASS EXTENDED PARTIAL RUNTIME PASS FINAL NEIGHBOR REMAINDER OUTSTANDING**  
SHA-256: `06e07fe6805e5e41786c16b5c1ea2132c4f65b385517c902f8aa566ccf49cd4e`

Active candidate: **S1.42AH**. Runtime test outstanding: **yes**. Build successor armed: **no**.

Exact next action: Run only the final S1.42AH non-Pikmin neighbor remainder: deliberately exercise a MouthDog/Paw collision against a non-Pikmin EnemyAI and prove native Paw-initiated BiteKillEnemyAI / generic non-Pikmin collision behavior remains functional and is not filtered by the Pikmin-only prefix. Then upload the complete fresh S1.42AH LogOutput.log. Do not rebuild S1.42AH or repeat already-proven Pikmin -> MouthDog attack/death/cleanup, adapter protection, Vanilla Pikmin collision blocking, startup, or player-maul coverage. If this final required check passes, explicitly accept S1.42AH; if it fails, explicitly reject S1.42AH and return to an S1.42AF-derived follow-up.

## Semantic navigation

- ChatGPT segmented execution: `Current/CHATGPT_SEGMENTED_EXECUTION_POLICY.md`
- Topic router: `Current/PROJECT_KNOWLEDGE_MAP.md` / `.json`
- Chat handover procedure: `Current/HANDOVER_PREPARATION_PROMPT.md`
- Build history: `Current/BUILD_LINEAGE.md` / `.json`
- Authority/history classification: `Current/DOCUMENT_AUTHORITY.md` / `.json`
- Artifact/runtime-evidence integrity: `Current/ARTIFACT_EVIDENCE_INTEGRITY.md` / `.json`
- Deferred work: `Knowledge/ROADMAP_AND_DEFERRED_SCOPES.md`
- Patch safety: `Current/68_PROJECT_LOCAL_PATCH_SAFETY_AND_REGRESSION_POLICY.md`

Historical handovers, candidate notes, rejection records and runtime decisions are preserved as evidence, but they do not override the current state/topic authority graph or a later explicit acceptance decision.

## Repository overhaul

Status: **OVERHAUL_COMPLETE_VALIDATED**.  
Verified pre-overhaul recovery repository: `Tendas240/Lethal-Company-AI-Modding-Project-PreOverhaul-20260904` at frozen source commit `5dbd0e637a480d8591773e422bbca4b0654cad20`.  
Manifest: `Current/PRE_OVERHAUL_BACKUP_MANIFEST.json`.

No local repository clone or local profile build should be required from the user while repository-native artifacts and automation are sufficient.
