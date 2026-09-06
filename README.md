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

Latest built artifact: **S1.42AG — Mouth Dog Pikmin One-Way Protection — RUNTIME REJECTED PARTIAL FIX**  
SHA-256: `3ad605d813b2a484da53f97348414f1163bb73c40839319cddd33bb26c357fee`

Active candidate: **none**. Runtime test outstanding: **no**. Build successor armed: **no**.

Exact next action: Extend source evidence repository-natively before any successor: inspect the exact Vanilla V81 EnemyAI.OnCollideWithEnemy() base contract and exact LethalMin 1.1.108 PikminItem.CarryNumerator()/carry-item audio/noise callsites. Current V81 MouthDogAI evidence already proves DetectNoise is position-based and OnCollideWithEnemy can lunge/HitEnemy(2) against generic EnemyAI; exact LethalMin evidence proves PikminAI inherits EnemyAI and can emit PlayAudibleNoise while the current config has Dont Make Audible Noises=false. The observed Purple Pikmin carried GoldBar(Clone), but the GoldBar itself as the causal noise source is not yet proved or excluded. Do not repeat the successful MouthDog capture, do not build or arm a successor, and do not start a gameplay test until the base-method and carry/noise boundaries are proved and patch-safety review is complete.

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
